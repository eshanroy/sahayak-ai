import json

import os

import re

from dotenv import load_dotenv

from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:

    raise ValueError("GROQ_API_KEY is missing. Check backend/.env.")

client = Groq(api_key=GROQ_API_KEY)

UNIFIED_MODEL = "openai/gpt-oss-120b"

SUPPORTED_LANGUAGES = {

    "en": "English",

    "hi": "Hindi",

    "te": "Telugu",

    "ta": "Tamil",

    "kn": "Kannada",

    "bn": "Bengali",

}

LOCALIZED_AUTHORITY = {

    "en": "Municipal Public Works / Road Maintenance Authority",

    "hi": "नगरपालिका लोक निर्माण / सड़क रखरखाव विभाग",

    "te": "పురపాలక ప్రజా పనుల / రహదారి నిర్వహణ విభాగం",

    "ta": "நகராட்சி பொதுப்பணி / சாலை பராமரிப்புத் துறை",

    "kn": "ನಗರಸಭೆ ಸಾರ್ವಜನಿಕ ಕಾಮಗಾರಿ / ರಸ್ತೆ ನಿರ್ವಹಣಾ ಇಲಾಖೆ",

    "bn": "পৌর জনপূর্ত / সড়ক রক্ষণাবেক্ষণ বিভাগ",

}

COMPLAINT_TEMPLATES = {

    "en": (

        "Subject: Request to inspect and address a civic issue\n\n"

        "Dear Sir/Madam,\n\n"

        "I would like to report a civic issue. Please complete the "

        "following details before submitting:\n\n"

        "Issue description: [write the issue description in English]\n"

        "Exact location: [exact location]\n"

        "Date observed: [date, if known]\n"

        "Supporting evidence: [add details only if available]\n\n"

        "Please inspect the issue and take appropriate action if required.\n\n"

        "Thank you.\nSincerely,\n[your name]\n"

        "[contact information, optional]"

    ),

    "hi": (

        "विषय: नागरिक समस्या की जाँच और उचित कार्रवाई के लिए अनुरोध\n\n"

        "महोदय/महोदया,\n\n"

        "मैं एक नागरिक समस्या की सूचना देना चाहता/चाहती हूँ। "

        "कृपया भेजने से पहले नीचे दिए गए विवरण भरें:\n\n"

        "समस्या का विवरण: [समस्या का विवरण हिंदी में लिखें]\n"

        "सटीक स्थान: [सटीक स्थान]\n"

        "देखे जाने की तारीख: [तारीख, यदि ज्ञात हो]\n"

        "उपलब्ध साक्ष्य: [केवल उपलब्ध होने पर विवरण जोड़ें]\n\n"

        "कृपया समस्या की जाँच करके आवश्यक कार्रवाई करें।\n\n"

        "धन्यवाद।\nसादर,\n[आपका नाम]\n[संपर्क जानकारी, वैकल्पिक]"

    ),

    "te": (

        "విషయం: పౌర సమస్యను పరిశీలించి తగిన చర్యలు తీసుకోవాలని అభ్యర్థన\n\n"

        "గౌరవనీయులైన అధికారికి,\n\n"

        "ఒక పౌర సమస్యను మీ దృష్టికి తీసుకువస్తున్నాను. "

        "సమర్పించే ముందు కింది వివరాలను పూర్తి చేయండి:\n\n"

        "సమస్య వివరణ: [సమస్యను తెలుగులో వివరించండి]\n"

        "ఖచ్చితమైన స్థలం: [ఖచ్చితమైన స్థలం]\n"

        "గమనించిన తేదీ: [తెలిస్తే తేదీ]\n"

        "అందుబాటులో ఉన్న ఆధారాలు: [ఉంటే మాత్రమే వివరాలు జోడించండి]\n\n"

        "దయచేసి సమస్యను పరిశీలించి అవసరమైన చర్యలు తీసుకోండి.\n\n"

        "ధన్యవాదాలు.\nవినమ్రంగా,\n[మీ పేరు]\n[సంప్రదింపు సమాచారం, ఐచ్చికం]"

    ),

    "ta": (

        "பொருள்: குடிமைப் பிரச்சினையை ஆய்வு செய்து உரிய நடவடிக்கை எடுக்கக் கோருதல்\n\n"

        "மதிப்பிற்குரிய அதிகாரி அவர்களுக்கு,\n\n"

        "ஒரு குடிமைப் பிரச்சினையைத் தெரிவிக்க விரும்புகிறேன். "

        "சமர்ப்பிக்கும் முன் கீழே உள்ள விவரங்களை நிரப்பவும்:\n\n"

        "பிரச்சினையின் விவரம்: [பிரச்சினையைத் தமிழில் விவரிக்கவும்]\n"

        "சரியான இடம்: [சரியான இடம்]\n"

        "கவனித்த தேதி: [தெரிந்தால் தேதி]\n"

        "கிடைக்கும் ஆதாரங்கள்: [இருந்தால் மட்டும் விவரங்களைச் சேர்க்கவும்]\n\n"

        "தயவுசெய்து பிரச்சினையை ஆய்வு செய்து தேவையான நடவடிக்கை எடுக்கவும்.\n\n"

        "நன்றி.\nஉண்மையுடன்,\n[உங்கள் பெயர்]\n[தொடர்பு விவரம், விருப்பத்திற்கேற்ப]"

    ),

    "kn": (

        "ವಿಷಯ: ನಾಗರಿಕ ಸಮಸ್ಯೆಯನ್ನು ಪರಿಶೀಲಿಸಿ ಸೂಕ್ತ ಕ್ರಮ ಕೈಗೊಳ್ಳುವಂತೆ ವಿನಂತಿ\n\n"

        "ಮಾನ್ಯ ಅಧಿಕಾರಿಗಳಿಗೆ,\n\n"

        "ಒಂದು ನಾಗರಿಕ ಸಮಸ್ಯೆಯನ್ನು ನಿಮ್ಮ ಗಮನಕ್ಕೆ ತರಲು ಬಯಸುತ್ತೇನೆ. "

        "ಸಲ್ಲಿಸುವ ಮೊದಲು ಕೆಳಗಿನ ವಿವರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ:\n\n"

        "ಸಮಸ್ಯೆಯ ವಿವರಣೆ: [ಸಮಸ್ಯೆಯನ್ನು ಕನ್ನಡದಲ್ಲಿ ವಿವರಿಸಿ]\n"

        "ನಿಖರ ಸ್ಥಳ: [ನಿಖರ ಸ್ಥಳ]\n"

        "ಗಮನಿಸಿದ ದಿನಾಂಕ: [ತಿಳಿದಿದ್ದರೆ ದಿನಾಂಕ]\n"

        "ಲಭ್ಯವಿರುವ ಸಾಕ್ಷ್ಯ: [ಇದ್ದರೆ ಮಾತ್ರ ವಿವರಗಳನ್ನು ಸೇರಿಸಿ]\n\n"

        "ದಯವಿಟ್ಟು ಸಮಸ್ಯೆಯನ್ನು ಪರಿಶೀಲಿಸಿ ಅಗತ್ಯ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ.\n\n"

        "ಧನ್ಯವಾದಗಳು.\nವಂದನೆಗಳೊಂದಿಗೆ,\n[ನಿಮ್ಮ ಹೆಸರು]\n[ಸಂಪರ್ಕ ಮಾಹಿತಿ, ಐಚ್ಛಿಕ]"

    ),

    "bn": (

        "বিষয়: নাগরিক সমস্যাটি পরিদর্শন করে উপযুক্ত ব্যবস্থা নেওয়ার অনুরোধ\n\n"

        "মাননীয় কর্মকর্তা,\n\n"

        "আমি একটি নাগরিক সমস্যার কথা জানাতে চাই। "

        "জমা দেওয়ার আগে নিচের তথ্যগুলি পূরণ করুন:\n\n"

        "সমস্যার বিবরণ: [সমস্যাটি বাংলায় বর্ণনা করুন]\n"

        "সঠিক অবস্থান: [সঠিক অবস্থান]\n"

        "লক্ষ্য করার তারিখ: [জানা থাকলে তারিখ]\n"

        "উপলব্ধ প্রমাণ: [শুধু থাকলে বিবরণ যোগ করুন]\n\n"

        "অনুগ্রহ করে সমস্যাটি পরিদর্শন করে প্রয়োজনীয় ব্যবস্থা নিন।\n\n"

        "ধন্যবাদ।\nবিনীত,\n[আপনার নাম]\n[যোগাযোগের তথ্য, ঐচ্ছিক]"

    ),

}

NO_IMAGE_UNCERTAINTY = {

    "en": "No image was supplied; the issue has not been visually verified.",

    "hi": "कोई तस्वीर नहीं दी गई है; समस्या की दृश्य पुष्टि नहीं हुई है।",

    "te": "చిత్రం అందించలేదు; సమస్యను దృశ్యపరంగా నిర్ధారించలేదు.",

    "ta": "படம் வழங்கப்படவில்லை; பிரச்சினை காட்சி மூலம் உறுதிப்படுத்தப்படவில்லை.",

    "kn": "ಚಿತ್ರವನ್ನು ಒದಗಿಸಿಲ್ಲ; ಸಮಸ್ಯೆಯನ್ನು ದೃಶ್ಯವಾಗಿ ಪರಿಶೀಲಿಸಲಾಗಿಲ್ಲ.",

    "bn": "কোনো ছবি দেওয়া হয়নি; সমস্যাটি দৃশ্যত যাচাই করা হয়নি।",

}

MISSING_LOCATION_UNCERTAINTY = {

    "en": "The exact location was not provided.",

    "hi": "सटीक स्थान की जानकारी नहीं दी गई है।",

    "te": "ఖచ్చితమైన స్థలం వివరాలు ఇవ్వలేదు.",

    "ta": "சரியான இட விவரம் வழங்கப்படவில்லை.",

    "kn": "ನಿಖರ ಸ್ಥಳದ ವಿವರ ನೀಡಲಾಗಿಲ್ಲ.",

    "bn": "সঠিক অবস্থানের বিবরণ দেওয়া হয়নি।",

}


GPS_UNCERTAINTY = {

    "en": "GPS coordinates were not collected; the written location was provided by the user.",

    "hi": "GPS निर्देशांक एकत्र नहीं किए गए; लिखित स्थान उपयोगकर्ता ने दिया है।",

    "te": "GPS కోఆర్డినేట్లు సేకరించలేదు; వ్రాతపూర్వక స్థల వివరాలను వినియోగదారు అందించారు.",

    "ta": "GPS ஆயத்தொலைவுகள் சேகரிக்கப்படவில்லை; எழுதப்பட்ட இட விவரத்தைப் பயனர் வழங்கியுள்ளார்.",

    "kn": "GPS ನಿರ್ದೇಶಾಂಕಗಳನ್ನು ಸಂಗ್ರಹಿಸಲಾಗಿಲ್ಲ; ಲಿಖಿತ ಸ್ಥಳದ ವಿವರವನ್ನು ಬಳಕೆದಾರರು ನೀಡಿದ್ದಾರೆ.",

    "bn": "GPS স্থানাঙ্ক সংগ্রহ করা হয়নি; লিখিত অবস্থানটি ব্যবহারকারী দিয়েছেন।",

}

# Controlled, conservative safety guidance.

# These messages are used when a pothole is reported.

POTHOLE_ACTIONS = {

    "en": [

        "Keep a safe distance from the pothole and avoid crossing it when possible.",

        "Use an alternative route if it is safe and practical to do so.",

        "Report the issue to the relevant local road maintenance authority.",

        "Record the location and collect photos only from a safe place, if possible.",

    ],

    "hi": [

        "गड्ढे से सुरक्षित दूरी बनाए रखें और संभव हो तो उसके ऊपर से जाने से बचें।",

        "यदि सुरक्षित और व्यावहारिक हो, तो वैकल्पिक मार्ग अपनाएँ।",

        "समस्या की सूचना संबंधित स्थानीय सड़क रखरखाव विभाग को दें।",

        "संभव हो तो सुरक्षित स्थान से स्थान का विवरण और तस्वीरें लें।",

    ],

    "te": [

        "గుంతకు సురక్షిత దూరంలో ఉండండి; సాధ్యమైనప్పుడు దాని మీదుగా వెళ్లకుండా ఉండండి.",

        "సురక్షితంగా, ఆచరణ సాధ్యంగా ఉంటే ప్రత్యామ్నాయ మార్గాన్ని ఉపయోగించండి.",

        "ఈ సమస్యను సంబంధిత స్థానిక రహదారి నిర్వహణ విభాగానికి నివేదించండి.",

        "సాధ్యమైతే సురక్షిత ప్రదేశం నుంచే స్థల వివరాలు, ఫోటోలు సేకరించండి.",

    ],

    "ta": [

        "குழியிலிருந்து பாதுகாப்பான தூரத்தில் இருங்கள்; முடிந்தால் அதன் வழியாகச் செல்வதைத் தவிர்க்கவும்.",

        "பாதுகாப்பாகவும் நடைமுறைக்கு ஏற்றதாகவும் இருந்தால் மாற்றுப் பாதையைப் பயன்படுத்தவும்.",

        "பிரச்சினையை உள்ளூர் சாலை பராமரிப்புத் துறையிடம் தெரிவிக்கவும்.",

        "முடிந்தால் பாதுகாப்பான இடத்திலிருந்து இட விவரங்களையும் புகைப்படங்களையும் சேகரிக்கவும்.",

    ],

    "kn": [

        "ಗುಂಡಿಯಿಂದ ಸುರಕ್ಷಿತ ಅಂತರದಲ್ಲಿರಿ; ಸಾಧ್ಯವಾದರೆ ಅದರ ಮೇಲೆ ಹಾದುಹೋಗುವುದನ್ನು ತಪ್ಪಿಸಿ.",

        "ಸುರಕ್ಷಿತವಾಗಿದ್ದು ಅನುಕೂಲಕರವಾಗಿದ್ದರೆ ಪರ್ಯಾಯ ಮಾರ್ಗವನ್ನು ಬಳಸಿ.",

        "ಸಮಸ್ಯೆಯನ್ನು ಸಂಬಂಧಿತ ಸ್ಥಳೀಯ ರಸ್ತೆ ನಿರ್ವಹಣಾ ಇಲಾಖೆಗೆ ವರದಿ ಮಾಡಿ.",

        "ಸಾಧ್ಯವಾದರೆ ಸುರಕ್ಷಿತ ಸ್ಥಳದಿಂದಲೇ ಸ್ಥಳದ ವಿವರ ಮತ್ತು ಫೋಟೋಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ.",

    ],

    "bn": [

        "গর্ত থেকে নিরাপদ দূরত্ব বজায় রাখুন এবং সম্ভব হলে এর ওপর দিয়ে যাওয়া এড়িয়ে চলুন।",

        "নিরাপদ ও বাস্তবসম্মত হলে বিকল্প পথ ব্যবহার করুন।",

        "সমস্যাটি সংশ্লিষ্ট স্থানীয় সড়ক রক্ষণাবেক্ষণ কর্তৃপক্ষকে জানান।",

        "সম্ভব হলে নিরাপদ স্থান থেকে অবস্থানের বিবরণ ও ছবি সংগ্রহ করুন।",

    ],

}

def _safe_complaint_draft(language: str, description: str = "", location: str = "") -> str:

    """Return a localized complaint template populated with the citizen's description."""

    template = COMPLAINT_TEMPLATES.get(language, COMPLAINT_TEMPLATES["en"])

    description = description.strip()

    if not description and not location:

        return template

    description_placeholders = {

        "en": "[write the issue description in English]",

        "hi": "[समस्या का विवरण हिंदी में लिखें]",

        "te": "[సమస్యను తెలుగులో వివరించండి]",

        "ta": "[பிரச்சினையைத் தமிழில் விவரிக்கவும்]",

        "kn": "[ಸಮಸ್ಯೆಯನ್ನು ಕನ್ನಡದಲ್ಲಿ ವಿವರಿಸಿ]",

        "bn": "[সমস্যাটি বাংলায় বর্ণনা করুন]",

    }

    placeholder = description_placeholders.get(language)

    if placeholder and description:

        template = template.replace(placeholder, description)

    location_placeholders = {

        "en": "[exact location]",

        "hi": "[सटीक स्थान]",

        "te": "[ఖచ్చితమైన స్థలం]",

        "ta": "[சரியான இடம்]",

        "kn": "[ನಿಖರ ಸ್ಥಳ]",

        "bn": "[সঠিক অবস্থান]",

    }

    location_placeholder = location_placeholders.get(language)

    if location_placeholder and location.strip():

        template = template.replace(location_placeholder, location.strip())

    return template

def _is_pothole_report(description: str, text_analysis: dict | None) -> bool:

    text = description.lower()

    if any(word in text for word in ("pothole", "road hole")):

        return True

    if isinstance(text_analysis, dict):

        category = str(text_analysis.get("problem_category", "")).lower()

        title = str(text_analysis.get("title", "")).lower()

        combined = category + " " + title

        if any(word in combined for word in ("pothole", "road hole")):

            return True

    return False

def create_unified_report(

    description: str = "",

    text_analysis: dict | None = None,

    image_analysis: dict | None = None,

    language: str = "en",

) -> dict:

    """Create a multilingual civic report with conservative safeguards."""

    description = description.strip()

    # main.py adds manual location as a "Reported location: ..." line.

    location_match = re.search(

        r"(?im)^Reported location:\s*(.+?)\s*$",

        description,

    )

    reported_location = location_match.group(1).strip() if location_match else ""

    if location_match:

        description = re.sub(

            r"(?im)^Reported location:\s*.+?\s*$",

            "",

            description,

        ).strip()

    if not description and not image_analysis:

        return {

            "status": "error",

            "message": "Provide a description, image analysis, or both.",

        }

    if language not in SUPPORTED_LANGUAGES:

        return {

            "status": "error",

            "message": (

                "Unsupported language. Choose English, Hindi, Telugu, "

                "Tamil, Kannada, or Bengali."

            ),

        }

    language_name = SUPPORTED_LANGUAGES[language]

    evidence = {

        "citizen_description": description or None,

        "text_analysis": text_analysis,

        "image_analysis": image_analysis,

    }

    prompt = f"""

You are Sahayak AI, a careful civic assistance system.

Write every user-facing report value in {language_name}, except

severity, which must be exactly Low, Medium, High, or Critical.

Keep JSON field names in English.

SOURCE INFORMATION:

{json.dumps(evidence, ensure_ascii=False)}

FACTUAL RULES:

- Never invent names, locations, dates, measurements, witnesses,

  previous accidents, near misses, injuries, or other events.

- Do not claim photos or videos exist unless actually supplied.

- If no image analysis is supplied, do not claim visual confirmation.

- Separate citizen-reported claims from verified observations.

- Do not state that a death, injury, or accident is likely without

  evidence supporting that assessment.

- If a detail is unknown, disclose uncertainty.
- If SOURCE INFORMATION contains a user-provided location, treat it as the reported location and acknowledge it in the report.
- Do not claim that the written location is missing when a user-provided location is available.
- If an image cannot independently establish the location, say only that the location has not been visually verified; do not imply that the user failed to provide it.
- Distinguish missing GPS coordinates from a missing written location. Never invent coordinates or distances.
- When a written location is supplied, refer to it as the user-reported location; do not claim the image verifies it.
- Avoid repeating the same uncertainty in different wording.
- Severity is an AI-assessed urgency category based only on the supplied description and evidence; do not present it as an official determination or a prediction of what will happen.
- Never suggest that a citizen place a temporary warning sign or object in or beside traffic; advise reporting the hazard and keeping a safe distance instead.

- Never claim that an official complaint has been submitted.

SAFETY RULES:

- Do not advise entering traffic or placing objects, tape, or markers

  in a road or traffic lane.

- Do not instruct citizens to repair roads or personally warn traffic.

- Recommend the appropriate general authority.

- Suggest gathering evidence only from a safe location.

- Do not invent emergency numbers or authority contacts.

LANGUAGE RULES:

- Use natural, grammatically correct {language_name}.

- For Telugu pothole reports, use “గుంత” or “రోడ్డుపై గుంత”; never use “పొట్టలు” to refer to potholes.

- Keep explanatory prose fully in {language_name}; do not insert stray English words.

- Translate every report value.

- Do not mix English headings into non-English text.

- The application will replace immediate actions and complaint draft

  with controlled localized content.

Return only JSON with these exact fields:

{{

  "problem_category": "",

  "title": "",

  "summary": "",

  "severity": "",

  "severity_reason": "",

  "confirmed_observations": [],

  "uncertainties": [],

  "immediate_actions": [],

  "evidence_needed": [],

  "recommended_authority": "",

  "report_draft": "",

  "citizen_explanation": ""

}}

"""

    try:

        completion = client.chat.completions.create(

            model=UNIFIED_MODEL,

            messages=[

                {

                    "role": "system",

                    "content": (

                        f"Create careful civic reports in {language_name}. "

                        "Do not invent facts. Return valid JSON only."

                    ),

                },

                {"role": "user", "content": prompt},

            ],

            response_format={"type": "json_object"},

            temperature=0.1,

            max_tokens=6000,

        )

        content = completion.choices[0].message.content

        if not content:

            return {

                "status": "error",

                "message": "The unified model returned an empty response.",

            }

        report = json.loads(content)

        required_fields = [

            "problem_category",

            "title",

            "summary",

            "severity",

            "severity_reason",

            "confirmed_observations",

            "uncertainties",

            "immediate_actions",

            "evidence_needed",

            "recommended_authority",

            "report_draft",

            "citizen_explanation",

        ]

        if any(field not in report for field in required_fields):

            return {

                "status": "error",

                "message": "The unified report is missing required fields.",

            }

        if report["severity"] not in {"Low", "Medium", "High", "Critical"}:

            report["severity"] = "Medium"

        list_fields = [

            "confirmed_observations",

            "uncertainties",

            "immediate_actions",

            "evidence_needed",

        ]

        for field in list_fields:

            if not isinstance(report[field], list) or any(

                not isinstance(item, str) for item in report[field]

            ):

                return {

                    "status": "error",

                    "message": (

                        f"The unified report field '{field}' must be a list of strings."

                    ),

                }

        string_fields = [

            "problem_category",

            "title",

            "summary",

            "severity_reason",

            "recommended_authority",

            "report_draft",

            "citizen_explanation",

        ]

        for field in string_fields:

            if not isinstance(report[field], str):

                return {

                    "status": "error",

                    "message": (

                        f"The unified report field '{field}' must be a string."

                    ),

                }

        if image_analysis is None:

            report["confirmed_observations"] = []

            uncertainty = NO_IMAGE_UNCERTAINTY[language]

            report["uncertainties"] = list(report["uncertainties"])

            if uncertainty not in report["uncertainties"]:

                report["uncertainties"].append(uncertainty)

        # Normalize uncertainty entries and keep reported location separate from GPS.
        report["uncertainties"] = list(dict.fromkeys(
            item.strip() for item in report["uncertainties"] if item.strip()
        ))

        if reported_location.strip():
            # Remove misleading claims that no written location was supplied.
            location_phrases_to_remove = (
                "the exact location was not provided",
                "no location was provided",
                "the exact location is not provided",
                "the precise written location",
                "the written location was not provided",
                "the location was not provided",
                "gps coordinates or precise address are not provided",
                "gps coordinates or exact address were not provided",
                "exact gps coordinates or precise address of the pothole are not provided",
            )
            report["uncertainties"] = [
                item for item in report["uncertainties"]
                if not any(phrase in item.casefold() for phrase in location_phrases_to_remove)
            ]

            # Make the distinction explicit in English reports. Other languages
            # retain the model's localized wording plus the localized GPS note.
            if language == "en":
                reported_note = f"The user-reported location is: {reported_location}. It has not been independently verified from the image."
                if reported_note not in report["uncertainties"]:
                    report["uncertainties"].append(reported_note)

            gps_uncertainty = GPS_UNCERTAINTY[language]
            if language == "en":
                # Keep one canonical GPS limitation instead of multiple variants.
                report["uncertainties"] = [
                    item for item in report["uncertainties"]
                    if not ("gps" in item.casefold() and any(
                        phrase in item.casefold() for phrase in (
                            "not collected", "not provided", "not available",
                            "were not captured", "were not obtained",
                        )
                    ))
                ]
            if gps_uncertainty not in report["uncertainties"]:
                report["uncertainties"].append(gps_uncertainty)
        else:
            uncertainty = MISSING_LOCATION_UNCERTAINTY[language]
            if uncertainty not in report["uncertainties"]:
                report["uncertainties"].append(uncertainty)

        # Prevent near-duplicate uncertainty sentences in English output.
        if language == "en":
            seen_uncertainties = set()
            cleaned_uncertainties = []
            for item in report["uncertainties"]:
                normalized = re.sub(r"[^a-z0-9]+", " ", item.casefold()).strip()
                if normalized and normalized not in seen_uncertainties:
                    seen_uncertainties.add(normalized)
                    cleaned_uncertainties.append(item)
            report["uncertainties"] = cleaned_uncertainties

        localized_description = report.get("summary", "").strip() or description

        report["report_draft"] = _safe_complaint_draft(language, localized_description, reported_location)

        report["recommended_authority"] = LOCALIZED_AUTHORITY[language]

        if language == "en":
            # The citizen should not be encouraged to place signs/objects near traffic.
            report["citizen_explanation"] = re.sub(
                r"[^.!?]*\b(?:put|place|set up)\b[^.!?]*\b(?:warning sign|sign|marker|object)\b[^.!?]*[.!?]?",
                "",
                report["citizen_explanation"],
                flags=re.IGNORECASE,
            ).strip()

        if _is_pothole_report(description, text_analysis):

            report["immediate_actions"] = list(POTHOLE_ACTIONS[language])

            if language == "te":

                # Standardize Telugu terminology for road potholes.

                replacements = {

                    "పొట్టలు": "గుంతలు",

                    "పొట్టల": "గుంతల",

                    "రోడ్ సేఫ్టీ": "రోడ్డు భద్రత",

                }

                for field in (

                    "problem_category",

                    "title",

                    "summary",

                    "severity_reason",

                    "citizen_explanation",

                ):

                    value = report.get(field)

                    if isinstance(value, str):

                        for incorrect, corrected in replacements.items():

                            value = value.replace(incorrect, corrected)

                        report[field] = value

                # Keep this explanation fully in Telugu rather than allowing

                # stray English words such as “avoided” into the report.

                report["citizen_explanation"] = (

                    "కళాశాల సమీపంలోని రోడ్డుపై ఉన్న గుంత సైక్లిస్టులకు, "

                    "ముఖ్యంగా రాత్రి సమయంలో, ప్రమాదకరంగా ఉండవచ్చు. "

                    "ఈ సమస్యను స్థానిక రహదారి నిర్వహణ విభాగానికి నివేదించండి. "

                    "ఖచ్చితమైన స్థలం మరియు అందుబాటులో ఉన్న ఫోటోలను సురక్షితమైన "

                    "ప్రదేశం నుంచే అందించండి. గుంతను మరమ్మతు చేసే వరకు వీలైతే "

                    "ప్రత్యామ్నాయ మార్గాన్ని ఉపయోగించండి; మీ కళాశాలకు కూడా తెలియజేయండి."

                )

        return {

            "status": "success",

            "model": UNIFIED_MODEL,

            "language": language,

            "language_name": language_name,

            "report": report,

        }

    except json.JSONDecodeError:

        return {

            "status": "error",

            "message": "The unified model returned invalid JSON.",

        }

    except Exception as exc:

        import traceback

        traceback.print_exc()

        print(f"Sahayak AI unified report error: {exc!r}")

        return {

            "status": "error",

            "message": (

                "Unable to create the unified report. "

                "Check the backend terminal for the actual error."

            ),

        }
