import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Please add it to backend/.env"
    )

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-120b"


def analyze_problem(description: str) -> dict:
    """
    Analyze a citizen's problem using the Groq LLM
    and return structured civic assistance.
    """

    prompt = f"""
You are Sahayak AI, a multilingual civic and emergency assistance
system designed to help citizens understand problems and take
appropriate next steps.

Analyze the following citizen report:

"{description}"

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
    "problem_category": "",
    "title": "",
    "summary": "",
    "severity": "",
    "severity_reason": "",
    "location_needed": true,
    "evidence_needed": [],
    "immediate_actions": [],
    "recommended_authority": "",
    "report_draft": "",
    "citizen_explanation": ""
}}

Rules:

1. problem_category should be a short category such as:
   Road Safety, Public Infrastructure, Water Supply,
   Electricity, Waste Management, Public Safety,
   Emergency, Healthcare, Education, Transport, Other.

2. title should be a concise title for the issue.

3. summary should explain the issue clearly in 1-3 sentences.

4. severity must be exactly one of:
   Low, Medium, High, Critical.

5. severity_reason should briefly explain why that severity
   was selected.

6. location_needed should be true if knowing the location would
   materially help resolve the issue.

7. evidence_needed should contain useful evidence a citizen
   could provide, such as photographs, videos, documents,
   timestamps, or reference numbers.

8. immediate_actions should contain practical steps the citizen
   can take.

9. recommended_authority should identify the relevant type of
   authority or service, not invent a specific office.

10. report_draft should be a professional complaint/report that
    the citizen could adapt and submit.

11. citizen_explanation should explain the result in simple,
    citizen-friendly language.

12. Do not invent laws, case numbers, government contacts,
    phone numbers, addresses, or factual details that were not
    provided.

13. If the issue appears to be an immediate danger to life,
    prioritize contacting appropriate emergency services.

14. Keep the response practical and concise.

Return JSON only. Do not use Markdown.
"""

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Sahayak AI. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=1800,
        )

        content = completion.choices[0].message.content.strip()

        # Remove accidental Markdown code fences if the model adds them.
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        result = json.loads(content)

        return {
            "status": "success",
            "analysis": result,
        }

    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "The AI returned an invalid response format.",
        }

    except Exception as error:
        return {
            "status": "error",
            "message": f"AI analysis failed: {str(error)}",
        }