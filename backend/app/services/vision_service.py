
import base64
import json
import os
from io import BytesIO

from dotenv import load_dotenv
from groq import Groq
from PIL import Image


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Check backend/.env."
    )

client = Groq(api_key=GROQ_API_KEY)

VISION_MODEL = "qwen/qwen3.8-27b"


def analyze_image(image_bytes: bytes) -> dict:
    """
    Analyze a validated image using Groq's vision-capable model.
    Returns a structured description of visible evidence.
    """

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image_format = image.format

            if image_format not in {"JPEG", "PNG", "WEBP"}:
                return {
                    "status": "error",
                    "message": "Unsupported image format.",
                }

            image = image.convert("RGB")

            # Resize oversized images to keep requests manageable.
            image.thumbnail((1600, 1600))

            buffer = BytesIO()
            image.save(buffer, format="JPEG", quality=85)
            processed_bytes = buffer.getvalue()

        encoded_image = base64.b64encode(
            processed_bytes
        ).decode("utf-8")

        image_url = (
            f"data:image/jpeg;base64,{encoded_image}"
        )

        prompt = """
You are Sahayak AI, a civic evidence image analyst.

Examine the supplied image for visible civic or public-safety
issues, such as potholes, damaged roads, overflowing garbage,
water leaks, damaged streetlights, or other infrastructure
problems.

Return ONLY a valid JSON object containing these fields:

{
  "image_summary": "",
  "detected_issue": "",
  "problem_category": "",
  "visible_evidence": [],
  "potential_safety_concerns": [],
  "recommended_next_steps": [],
  "additional_evidence_needed": [],
  "limitations": ""
}

Rules:
- Describe only what is visibly supported by the image.
- Do not assume the location, date, owner, or cause of damage.
- Do not claim that an issue is confirmed if the image is unclear.
- Mention uncertainty when an object or issue cannot be identified.
- Do not invent laws, authorities, contact details, or measurements.
- Do not treat image analysis as a professional safety inspection.
- Keep recommendations practical and concise.
- If no civic issue is visible, say so clearly.
"""

        completion = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyze images carefully and return "
                        "only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                },
            ],
            response_format={"type": "json_object"},
            temperature=1,
            max_tokens=1500,
        )

        content = completion.choices[0].message.content

        if not content:
            return {
                "status": "error",
                "message": "The vision model returned an empty response.",
            }

        result = json.loads(content)

        return {
            "status": "success",
            "model": VISION_MODEL,
            "analysis": result,
        }

    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "The vision model returned invalid JSON.",
        }

    except Exception:
        # Avoid exposing API credentials or internal details.
        return {
            "status": "error",
            "message": (
                "Image analysis failed. Check the backend "
                "terminal for diagnostic details."
            ),
        }
