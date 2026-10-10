
from io import BytesIO

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel

from app.services.ai_service import analyze_problem
from app.services.vision_service import analyze_image
from app.services.unified_service import (
    SUPPORTED_LANGUAGES,
    create_unified_report,
)


app = FastAPI(
    title="Sahayak AI",
    description="Multimodal AI Civic & Emergency Assistant",
    version="0.7.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://sahayak-ai-five-blush.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProblemRequest(BaseModel):
    description: str


@app.get("/")
def root():
    return {
        "message": "Sahayak AI is running 🚨",
        "status": "online",
    }


@app.get("/api/health")
def health_check():
    return {
        "service": "Sahayak AI",
        "status": "healthy",
        "version": "0.7.0",
    }


@app.post("/api/analyze")
def analyze(request: ProblemRequest):
    description = request.description.strip()

    if not description:
        raise HTTPException(
            status_code=400,
            detail="Problem description cannot be empty.",
        )

    result = analyze_problem(description)

    if result.get("status") == "error":
        raise HTTPException(
            status_code=502,
            detail=result.get("message", "Text analysis failed."),
        )

    return result


async def read_valid_image(file: UploadFile) -> bytes:
    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail="Upload a JPG, PNG, or WebP image.",
        )

    max_size = 5 * 1024 * 1024
    contents = await file.read(max_size + 1)

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty.",
        )

    if len(contents) > max_size:
        raise HTTPException(
            status_code=413,
            detail="Image must be 5 MB or smaller.",
        )

    try:
        with Image.open(BytesIO(contents)) as image:
            image.verify()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image.",
        )

    return contents


@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    contents = await read_valid_image(file)
    result = analyze_image(contents)

    if result.get("status") == "error":
        raise HTTPException(
            status_code=502,
            detail=result.get("message", "Image analysis failed."),
        )

    return {
        "status": "success",
        "message": "Image analyzed successfully.",
        "filename": file.filename,
        "size_bytes": len(contents),
        "model": result.get("model"),
        "analysis": result.get("analysis"),
    }


@app.post("/api/analyze-unified")
async def analyze_unified(
    description: str = Form(default=""),
    language: str = Form(default="en"),
    location: str = Form(default=""),
    file: UploadFile | None = File(default=None),
):
    description = description.strip()
    location = location.strip()

    if len(location) > 300:
        raise HTTPException(
            status_code=400,
            detail="Location must be 300 characters or fewer.",
        )

    if not description and file is None:
        raise HTTPException(
            status_code=400,
            detail="Provide a description, an image, or both.",
        )

    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported language. Choose one of: "
                + ", ".join(SUPPORTED_LANGUAGES.keys())
            ),
        )

    text_analysis = None
    image_analysis = None

    if description:
        text_result = analyze_problem(description)

        if text_result.get("status") == "error":
            raise HTTPException(
                status_code=502,
                detail=text_result.get("message", "Text analysis failed."),
            )

        text_analysis = text_result.get("analysis")

    if file is not None:
        contents = await read_valid_image(file)
        image_result = analyze_image(contents)

        if image_result.get("status") == "error":
            raise HTTPException(
                status_code=502,
                detail=image_result.get("message", "Image analysis failed."),
            )

        image_analysis = image_result.get("analysis")

    report_description = description

    if location:
        report_description = (
            f"{description}\n\nReported location: {location}"
            if description
            else f"Reported location: {location}"
        )

    unified_result = create_unified_report(
        description=report_description,
        text_analysis=text_analysis,
        image_analysis=image_analysis,
        language=language,
    )

    if unified_result.get("status") == "error":
        raise HTTPException(
            status_code=502,
            detail=unified_result.get("message", "Unified analysis failed."),
        )

    return {
        "status": "success",
        "message": "Unified civic report generated successfully.",
        "language": unified_result.get("language"),
        "language_name": unified_result.get("language_name"),
        "location": location or None,
        "text_analysis": text_analysis,
        "image_analysis": image_analysis,
        "unified_report": unified_result.get("report"),
    }
