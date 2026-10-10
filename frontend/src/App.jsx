import { useEffect, useState } from "react";



const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";



const LANGUAGES = [

  { code: "en", label: "English" },

  { code: "hi", label: "हिन्दी (Hindi)" },

  { code: "te", label: "తెలుగు (Telugu)" },

  { code: "ta", label: "தமிழ் (Tamil)" },

  { code: "kn", label: "ಕನ್ನಡ (Kannada)" },

  { code: "bn", label: "বাংলা (Bengali)" },

];



const UI_TEXT = {

  en: {

    consolidated: "Consolidated civic report",

    severity: { Low: "Low", Medium: "Medium", High: "High", Critical: "Critical" },

    severityWhy: "Why this severity?",

    immediate: "Immediate actions",

    observations: "Confirmed observations",

    evidence: "Evidence checklist",

    uncertainties: "Uncertainties",

    authority: "Recommended authority",

    complaint: "Complaint draft",

    reviewDraft: "Review and edit this draft before sending it to the appropriate authority.",

    verifyAuthority: "Verify the responsible authority for your location before submitting the complaint.",

    simple: "In simple terms",

    copy: "Copy complaint",

    copied: "✓ Copied!",

    another: "Create another report",

    noDetails: "No additional details provided.",

    noUncertainties: "No additional uncertainties were identified by the model. Verify the details independently.",

    authorityFallback: "Please identify the appropriate local authority.",

    disclaimer: "This report is AI-generated and has not been submitted to any government authority. Confirm facts, location, and safety advice before taking action.",

  },

  hi: {

    consolidated: "समेकित नागरिक रिपोर्ट",

    severity: { Low: "कम", Medium: "मध्यम", High: "उच्च", Critical: "अत्यंत गंभीर" },

    severityWhy: "यह गंभीरता क्यों है?",

    immediate: "तत्काल कार्रवाई",

    observations: "पुष्ट अवलोकन",

    evidence: "साक्ष्य की सूची",

    uncertainties: "अनिश्चितताएँ",

    authority: "अनुशंसित प्राधिकरण",

    complaint: "शिकायत का मसौदा",

    reviewDraft: "इस मसौदे को संबंधित प्राधिकरण को भेजने से पहले पढ़ें और संपादित करें।",

    verifyAuthority: "शिकायत भेजने से पहले अपने क्षेत्र के लिए जिम्मेदार प्राधिकरण की पुष्टि करें।",

    simple: "सरल शब्दों में",

    copy: "शिकायत कॉपी करें",

    copied: "✓ कॉपी हो गया!",

    another: "दूसरी रिपोर्ट बनाएँ",

    noDetails: "कोई अतिरिक्त विवरण नहीं दिया गया।",

    noUncertainties: "मॉडल ने कोई अतिरिक्त अनिश्चितता नहीं बताई। विवरणों की स्वतंत्र रूप से पुष्टि करें।",

    authorityFallback: "कृपया उचित स्थानीय प्राधिकरण की पहचान करें।",

    disclaimer: "यह रिपोर्ट AI द्वारा बनाई गई है और किसी सरकारी प्राधिकरण को नहीं भेजी गई है। कार्रवाई से पहले तथ्यों, स्थान और सुरक्षा सलाह की पुष्टि करें।",

  },

  te: {

    consolidated: "సమగ్ర పౌర నివేదిక",

    severity: { Low: "తక్కువ", Medium: "మధ్యస్థం", High: "అధికం", Critical: "అత్యంత తీవ్రమైనది" },

    severityWhy: "ఈ తీవ్రతకు కారణం ఏమిటి?",

    immediate: "తక్షణ చర్యలు",

    observations: "నిర్ధారించిన పరిశీలనలు",

    evidence: "ఆధారాల జాబితా",

    uncertainties: "అనిశ్చిత అంశాలు",

    authority: "సిఫార్సు చేసిన అధికారం",

    complaint: "ఫిర్యాదు ముసాయిదా",

    reviewDraft: "సంబంధిత అధికారికి పంపే ముందు ఈ ముసాయిదాను పరిశీలించి సవరించండి.",

    verifyAuthority: "ఫిర్యాదు సమర్పించే ముందు మీ ప్రాంతానికి బాధ్యత వహించే అధికారిని నిర్ధారించండి.",

    simple: "సులభమైన మాటల్లో",

    copy: "ఫిర్యాదును కాపీ చేయండి",

    copied: "✓ కాపీ అయింది!",

    another: "మరో నివేదిక రూపొందించండి",

    noDetails: "అదనపు వివరాలు ఇవ్వలేదు.",

    noUncertainties: "మోడల్ అదనపు అనిశ్చిత అంశాలను గుర్తించలేదు. వివరాలను స్వతంత్రంగా ధృవీకరించండి.",

    authorityFallback: "దయచేసి సరైన స్థానిక అధికారిని గుర్తించండి.",

    disclaimer: "ఈ నివేదిక AI రూపొందించినది; ఏ ప్రభుత్వ అధికారిక సంస్థకూ సమర్పించలేదు. చర్య తీసుకునే ముందు వాస్తవాలు, స్థలం, భద్రతా సూచనలను నిర్ధారించండి.",

  },

  ta: {

    consolidated: "ஒருங்கிணைந்த குடிமக்கள் அறிக்கை",

    severity: { Low: "குறைவு", Medium: "மிதமானது", High: "அதிகம்", Critical: "மிகவும் தீவிரமானது" },

    severityWhy: "இந்த தீவிரத்திற்கான காரணம் என்ன?",

    immediate: "உடனடி நடவடிக்கைகள்",

    observations: "உறுதிப்படுத்தப்பட்ட கவனிப்புகள்",

    evidence: "ஆதாரப் பட்டியல்",

    uncertainties: "உறுதியற்ற விவரங்கள்",

    authority: "பரிந்துரைக்கப்படும் அதிகார அமைப்பு",

    complaint: "புகார் வரைவு",

    reviewDraft: "சம்பந்தப்பட்ட அதிகாரிக்கு அனுப்புவதற்கு முன் இந்த வரைவைக் கவனித்து திருத்தவும்.",

    verifyAuthority: "புகாரைச் சமர்ப்பிப்பதற்கு முன் உங்கள் பகுதிக்குப் பொறுப்பான அதிகார அமைப்பை உறுதிப்படுத்தவும்.",

    simple: "எளிய சொற்களில்",

    copy: "புகாரை நகலெடு",

    copied: "✓ நகலெடுக்கப்பட்டது!",

    another: "மற்றொரு அறிக்கையை உருவாக்கு",

    noDetails: "கூடுதல் விவரங்கள் வழங்கப்படவில்லை.",

    noUncertainties: "மாதிரி கூடுதல் உறுதியற்ற விவரங்களைக் கண்டறியவில்லை. விவரங்களைத் தனியாகச் சரிபார்க்கவும்.",

    authorityFallback: "சரியான உள்ளூர் அதிகார அமைப்பைக் கண்டறியவும்.",

    disclaimer: "இந்த அறிக்கை AI மூலம் உருவாக்கப்பட்டது; எந்த அரசு அதிகார அமைப்புக்கும் சமர்ப்பிக்கப்படவில்லை. நடவடிக்கை எடுப்பதற்கு முன் உண்மைகள், இடம் மற்றும் பாதுகாப்பு ஆலோசனைகளை உறுதிப்படுத்தவும்.",

  },

  kn: {

    consolidated: "ಸಂಯೋಜಿತ ನಾಗರಿಕ ವರದಿ",

    severity: { Low: "ಕಡಿಮೆ", Medium: "ಮಧ್ಯಮ", High: "ಹೆಚ್ಚು", Critical: "ಅತ್ಯಂತ ಗಂಭೀರ" },

    severityWhy: "ಈ ತೀವ್ರತೆಗೆ ಕಾರಣವೇನು?",

    immediate: "ತಕ್ಷಣದ ಕ್ರಮಗಳು",

    observations: "ದೃಢೀಕರಿಸಿದ ಗಮನಿಕೆಗಳು",

    evidence: "ಸಾಕ್ಷ್ಯಗಳ ಪಟ್ಟಿ",

    uncertainties: "ಅನಿಶ್ಚಿತತೆಗಳು",

    authority: "ಶಿಫಾರಸು ಮಾಡಿದ ಪ್ರಾಧಿಕಾರ",

    complaint: "ದೂರು ಕರಡು",

    reviewDraft: "ಸಂಬಂಧಿತ ಪ್ರಾಧಿಕಾರಕ್ಕೆ ಕಳುಹಿಸುವ ಮೊದಲು ಈ ಕರಡನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ತಿದ್ದುಪಡಿ ಮಾಡಿ.",

    verifyAuthority: "ದೂರು ಸಲ್ಲಿಸುವ ಮೊದಲು ನಿಮ್ಮ ಪ್ರದೇಶದ ಜವಾಬ್ದಾರಿಯುತ ಪ್ರಾಧಿಕಾರವನ್ನು ದೃಢೀಕರಿಸಿ.",

    simple: "ಸರಳವಾಗಿ ಹೇಳುವುದಾದರೆ",

    copy: "ದೂರನ್ನು ನಕಲಿಸಿ",

    copied: "✓ ನಕಲಿಸಲಾಗಿದೆ!",

    another: "ಮತ್ತೊಂದು ವರದಿ ರಚಿಸಿ",

    noDetails: "ಹೆಚ್ಚುವರಿ ವಿವರಗಳನ್ನು ನೀಡಲಾಗಿಲ್ಲ.",

    noUncertainties: "ಮಾದರಿಯು ಹೆಚ್ಚುವರಿ ಅನಿಶ್ಚಿತತೆಗಳನ್ನು ಗುರುತಿಸಿಲ್ಲ. ವಿವರಗಳನ್ನು ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸಿ.",

    authorityFallback: "ದಯವಿಟ್ಟು ಸೂಕ್ತ ಸ್ಥಳೀಯ ಪ್ರಾಧಿಕಾರವನ್ನು ಗುರುತಿಸಿ.",

    disclaimer: "ಈ ವರದಿಯನ್ನು AI ರಚಿಸಿದೆ; ಯಾವುದೇ ಸರ್ಕಾರಿ ಪ್ರಾಧಿಕಾರಕ್ಕೆ ಸಲ್ಲಿಸಲಾಗಿಲ್ಲ. ಕ್ರಮ ಕೈಗೊಳ್ಳುವ ಮೊದಲು ವಾಸ್ತವಾಂಶಗಳು, ಸ್ಥಳ ಮತ್ತು ಸುರಕ್ಷತಾ ಸಲಹೆಯನ್ನು ದೃಢೀಕರಿಸಿ.",

  },

  bn: {

    consolidated: "সমন্বিত নাগরিক প্রতিবেদন",

    severity: { Low: "কম", Medium: "মাঝারি", High: "উচ্চ", Critical: "অত্যন্ত গুরুতর" },

    severityWhy: "এই মাত্রার কারণ কী?",

    immediate: "তাৎক্ষণিক পদক্ষেপ",

    observations: "নিশ্চিত পর্যবেক্ষণ",

    evidence: "প্রমাণের তালিকা",

    uncertainties: "অনিশ্চয়তা",

    authority: "প্রস্তাবিত কর্তৃপক্ষ",

    complaint: "অভিযোগের খসড়া",

    reviewDraft: "সংশ্লিষ্ট কর্তৃপক্ষের কাছে পাঠানোর আগে খসড়াটি পর্যালোচনা ও সম্পাদনা করুন।",

    verifyAuthority: "অভিযোগ জমা দেওয়ার আগে আপনার এলাকার দায়িত্বপ্রাপ্ত কর্তৃপক্ষ নিশ্চিত করুন।",

    simple: "সহজ ভাষায়",

    copy: "অভিযোগ কপি করুন",

    copied: "✓ কপি হয়েছে!",

    another: "আরেকটি প্রতিবেদন তৈরি করুন",

    noDetails: "অতিরিক্ত কোনো বিবরণ দেওয়া হয়নি।",

    noUncertainties: "মডেল অতিরিক্ত অনিশ্চয়তা শনাক্ত করেনি। তথ্যগুলো স্বাধীনভাবে যাচাই করুন।",

    authorityFallback: "অনুগ্রহ করে উপযুক্ত স্থানীয় কর্তৃপক্ষ শনাক্ত করুন।",

    disclaimer: "এই প্রতিবেদনটি AI তৈরি করেছে এবং কোনো সরকারি কর্তৃপক্ষের কাছে জমা দেওয়া হয়নি। পদক্ষেপ নেওয়ার আগে তথ্য, অবস্থান ও নিরাপত্তা পরামর্শ যাচাই করুন।",

  },

};



const SEVERITY_STYLES = {

  Low: "border-emerald-400/30 bg-emerald-400/10 text-emerald-300",

  Medium: "border-amber-400/30 bg-amber-400/10 text-amber-300",

  High: "border-orange-400/30 bg-orange-400/10 text-orange-300",

  Critical: "border-red-400/30 bg-red-400/10 text-red-300",

};



function Section({ title, children, className = "" }) {

  return (

    <section

      className={`rounded-2xl border border-white/10 bg-white/[0.04] p-5 sm:p-6 ${className}`}

    >

      <h3 className="mb-4 text-lg font-semibold text-white">{title}</h3>

      {children}

    </section>

  );

}



function BulletList({

  items,

  emptyMessage = "No additional details provided.",

}) {

  if (!Array.isArray(items) || items.length === 0) {

    return <p className="text-sm text-slate-400">{emptyMessage}</p>;

  }



  return (

    <ul className="space-y-3">

      {items.map((item, index) => (

        <li

          key={`${index}-${item}`}

          className="flex gap-3 text-sm leading-6 text-slate-300"

        >

          <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-400" />

          <span>{item}</span>

        </li>

      ))}

    </ul>

  );

}



function formatComplaintDraft(draft = "") {
  // Normalize the generated text, then put each complaint section on its own line.
  let text = String(draft).replace(/\r\n?/g, "\n").replace(/\s+/g, " ").trim();

  const sectionBreaks = [
    [/Subject:/gi, "\n\nSubject:"],
    [/Dear Sir\/Madam,?/gi, "\n\nDear Sir/Madam,"],
    [/I would like to report a civic issue\./gi, "\n\nI would like to report a civic issue."],
    [/Please complete the following details before submitting:/gi, "\nPlease complete the following details before submitting:"],
    [/Issue description:/gi, "\n\nIssue description:"],
    [/Exact location:/gi, "\nExact location:"],
    [/Date observed:/gi, "\nDate observed:"],
    [/Supporting evidence:/gi, "\nSupporting evidence:"],
    [/Please inspect\b/gi, "\n\nPlease inspect"],
    [/Thank you\./gi, "\n\nThank you."],
    [/Sincerely,?/gi, "\n\nSincerely,"],
    [/\[your name\]/gi, "\n[your name]"],
    [/\[contact information, optional\]/gi, "\n[contact information, optional]"],
  ];

  for (const [pattern, replacement] of sectionBreaks) {
    text = text.replace(pattern, replacement);
  }

  return text
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n[ \t]+/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}



export default function App() {

  const [description, setDescription] = useState("");

  const [location, setLocation] = useState("");

  const [isListening, setIsListening] = useState(false);

  const [speechLanguage, setSpeechLanguage] = useState("en-IN");

  const [language, setLanguage] = useState("en");

  const [selectedImage, setSelectedImage] = useState(null);

  const [imagePreview, setImagePreview] = useState("");

  const [report, setReport] = useState(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [error, setError] = useState("");

  const [copied, setCopied] = useState(false);

  const [backendOnline, setBackendOnline] = useState(false);



  const ui = UI_TEXT[language] || UI_TEXT.en;



  useEffect(() => {

    let active = true;



    fetch(`${API_URL}/api/health`)

      .then((response) => {

        if (!response.ok) throw new Error("Backend unavailable");

        return response.json();

      })

      .then((data) => {

        if (active) setBackendOnline(data.status === "healthy");

      })

      .catch(() => {

        if (active) setBackendOnline(false);

      });



    return () => {

      active = false;

    };

  }, []);



  function startVoiceInput() {

    const SpeechRecognition =

      window.SpeechRecognition || window.webkitSpeechRecognition;



    if (!SpeechRecognition) {

      setError(

        "Voice input is not supported in this browser. Please use a recent version of Chrome or Edge."

      );

      return;

    }



    const recognition = new SpeechRecognition();

    recognition.lang = speechLanguage;

    recognition.continuous = false;

    recognition.interimResults = false;



    recognition.onstart = () => {

      setIsListening(true);

      setError("");

    };



    recognition.onresult = (event) => {

      const spokenText = event.results?.[0]?.[0]?.transcript?.trim();



      if (spokenText) {

        setDescription((previous) =>

          previous.trim()

            ? `${previous.trim()} ${spokenText}`

            : spokenText

        );

      }

    };



    recognition.onerror = (event) => {

      if (

        event.error === "not-allowed" ||

        event.error === "service-not-allowed"

      ) {

        setError(

          "Microphone access was blocked. Allow microphone access in your browser and try again."

        );

      } else if (

        event.error !== "no-speech" &&

        event.error !== "aborted"

      ) {

        setError(

          `Voice input failed (${event.error}). Please try again or type your description.`

        );

      }



      setIsListening(false);

    };



    recognition.onend = () => setIsListening(false);



    try {

      recognition.start();

    } catch {

      setIsListening(false);

      setError("Voice input could not start. Please try again.");

    }

  }



  function handleImageChange(event) {

    const file = event.target.files?.[0];



    setError("");

    setReport(null);

    setSelectedImage(null);

    setImagePreview("");



    if (!file) return;



    const allowedTypes = ["image/jpeg", "image/png", "image/webp"];



    if (!allowedTypes.includes(file.type)) {

      setError("Please upload a JPG, PNG, or WebP image.");

      event.target.value = "";

      return;

    }



    if (file.size > 5 * 1024 * 1024) {

      setError("The image must be 5 MB or smaller.");

      event.target.value = "";

      return;

    }



    setSelectedImage(file);

    setImagePreview(URL.createObjectURL(file));

  }



  async function handleAnalyze(event) {

    event.preventDefault();

    setError("");

    setReport(null);

    setCopied(false);



    if (!description.trim() && !selectedImage) {

      setError(

        "Please describe the civic issue, upload an image, or do both."

      );

      return;

    }



    const formData = new FormData();

    formData.append("description", description.trim());

    formData.append("language", language);

    formData.append("location", location.trim());



    if (selectedImage) {

      formData.append("file", selectedImage);

    }



    setIsAnalyzing(true);



    try {

      const response = await fetch(`${API_URL}/api/analyze-unified`, {

        method: "POST",

        body: formData,

      });



      const data = await response.json();



      if (!response.ok) {

        throw new Error(

          typeof data.detail === "string"

            ? data.detail

            : "Unable to analyze the issue. Please try again."

        );

      }



      if (data.status !== "success" || !data.unified_report) {

        throw new Error(

          data.message || "The report could not be generated."

        );

      }



      console.log(

        "RAW COMPLAINT:",

        JSON.stringify(data.unified_report.report_draft)

      );

      console.log(

        "COMPLAINT LENGTH:",

        data.unified_report.report_draft?.length

      );



      setReport(data.unified_report);

    } catch (err) {

      setError(

        err.message ||

          "Could not connect to Sahayak AI. Make sure the backend is running."

      );

    } finally {

      setIsAnalyzing(false);

    }

  }



  async function handleCopy() {

    if (!report?.report_draft) return;



    try {

      await navigator.clipboard.writeText(

        formatComplaintDraft(report.report_draft)

      );

      setCopied(true);

      setTimeout(() => setCopied(false), 2000);

    } catch {

      setError(

        "Unable to copy automatically. Please select and copy the complaint manually."

      );

    }

  }



  function handleReset() {

    setDescription("");

    setLocation("");

    setSelectedImage(null);

    setImagePreview("");

    setReport(null);

    setError("");

    setCopied(false);



    const fileInput = document.getElementById("issue-image");

    if (fileInput) fileInput.value = "";

  }



  const severity = report?.severity || "Medium";

  const severityStyle =

    SEVERITY_STYLES[severity] || SEVERITY_STYLES.Medium;



  return (

    <div className="min-h-screen bg-[#080b16] text-slate-200">

      <div className="pointer-events-none fixed inset-0 overflow-hidden">

        <div className="absolute -left-40 -top-40 h-96 w-96 rounded-full bg-violet-600/10 blur-3xl" />

        <div className="absolute -right-40 top-40 h-96 w-96 rounded-full bg-cyan-500/10 blur-3xl" />

      </div>



      <main className="relative mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">

        <header className="mb-10 flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

          <div>

            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-xs font-medium text-cyan-300">

              <span className="h-2 w-2 animate-pulse rounded-full bg-cyan-400" />

              AI-POWERED CIVIC ASSISTANCE

            </div>



            <h1 className="text-4xl font-black tracking-tight text-white sm:text-5xl">

              Sahayak <span className="text-cyan-400">AI</span>

            </h1>



            <p className="mt-3 max-w-xl text-sm leading-6 text-slate-400 sm:text-base">

              Understand civic problems, analyze visual evidence, and prepare

              actionable reports in your preferred language.

            </p>

          </div>



          <div className="flex items-center gap-2 self-start rounded-full border border-white/10 bg-white/[0.04] px-3 py-2 text-xs">

            <span

              className={`h-2.5 w-2.5 rounded-full ${

                backendOnline ? "bg-emerald-400" : "bg-red-400"

              }`}

            />

            <span className="text-slate-300">

              Backend {backendOnline ? "Connected" : "Offline"}

            </span>

          </div>

        </header>



        <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">

          <section className="h-fit rounded-3xl border border-white/10 bg-white/[0.035] p-5 shadow-2xl shadow-black/20 sm:p-7">

            <div className="mb-6">

              <p className="text-xs font-bold uppercase tracking-[0.2em] text-violet-300">

                Report a problem

              </p>

              <h2 className="mt-2 text-2xl font-bold text-white">

                Tell us what happened

              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">

                Describe the issue, attach a photo if available, and receive

                one consolidated civic report.

              </p>

            </div>



            <form onSubmit={handleAnalyze} className="space-y-6">

              <div>

                <label

                  htmlFor="language"

                  className="mb-2 block text-sm font-semibold text-slate-200"

                >

                  Report language

                </label>



                <select

                  id="language"

                  value={language}

                  onChange={(event) => {

                    setLanguage(event.target.value);

                    setReport(null);

                    setError("");

                  }}

                  className="w-full rounded-xl border border-white/10 bg-[#111627] px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20"

                >

                  {LANGUAGES.map((item) => (

                    <option key={item.code} value={item.code}>

                      {item.label}

                    </option>

                  ))}

                </select>



                <p className="mt-2 text-xs text-slate-500">

                  The generated report will use this language.

                </p>

              </div>



              <div>

                <label

                  htmlFor="location"

                  className="mb-2 block text-sm font-semibold text-slate-200"

                >

                  Location{" "}

                  <span className="font-normal text-slate-500">(optional)</span>

                </label>



                <input

                  id="location"

                  type="text"

                  value={location}

                  onChange={(event) => setLocation(event.target.value)}

                  maxLength={300}

                  placeholder="Example: Near college main gate, Gachibowli, Hyderabad"

                  className="w-full rounded-xl border border-white/10 bg-[#0b1020] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20"

                />



                <p className="mt-2 text-xs leading-5 text-slate-500">

                  Enter a nearby landmark, street, area, or city to help

                  contextualize the report. Your location is not detected

                  automatically.

                </p>

              </div>



              <div>

                <label

                  htmlFor="description"

                  className="mb-2 block text-sm font-semibold text-slate-200"

                >

                  Describe the civic issue

                </label>



                <textarea

                  id="description"

                  rows={6}

                  value={description}

                  onChange={(event) => setDescription(event.target.value)}

                  placeholder="Example: There is a large pothole near my college. It is dangerous for people riding bikes at night..."

                  className="w-full resize-y rounded-xl border border-white/10 bg-[#0b1020] px-4 py-3 text-sm leading-6 text-white outline-none transition placeholder:text-slate-600 focus:border-violet-400 focus:ring-2 focus:ring-violet-400/20"

                />



                <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center">

                  <div className="flex flex-1 items-center gap-3">

                    <label

                      htmlFor="speech-language"

                      className="shrink-0 text-xs font-medium text-slate-400"

                    >

                      Voice language

                    </label>



                    <select

                      id="speech-language"

                      value={speechLanguage}

                      onChange={(event) =>

                        setSpeechLanguage(event.target.value)

                      }

                      disabled={isListening}

                      className="min-w-0 flex-1 rounded-lg border border-white/10 bg-[#111627] px-3 py-2 text-sm text-white outline-none focus:border-cyan-400 disabled:opacity-50"

                    >

                      <option value="en-IN">English (India)</option>

                      <option value="te-IN">తెలుగు (Telugu)</option>

                      <option value="hi-IN">हिन्दी (Hindi)</option>

                      <option value="ta-IN">தமிழ் (Tamil)</option>

                      <option value="kn-IN">ಕನ್ನಡ (Kannada)</option>

                      <option value="bn-IN">বাংলা (Bengali)</option>

                    </select>

                  </div>



                  <button

                    type="button"

                    onClick={startVoiceInput}

                    disabled={isListening || isAnalyzing}

                    className="inline-flex items-center justify-center gap-2 rounded-xl border border-violet-400/30 bg-violet-400/10 px-4 py-2.5 text-sm font-semibold text-violet-200 transition hover:bg-violet-400/20 disabled:cursor-not-allowed disabled:opacity-60"

                  >

                    <span aria-hidden="true">🎙️</span>

                    {isListening

                      ? "Listening… speak now"

                      : "Speak description"}

                  </button>

                </div>



                <p className="mt-2 text-xs leading-5 text-slate-500">

                  Tap “Speak description” and allow microphone access if

                  prompted. Your speech will be added to the description above.

                </p>



                <p className="mt-2 text-right text-xs text-slate-500">

                  {description.length} characters

                </p>

              </div>



              <div>

                <label

                  htmlFor="issue-image"

                  className="mb-2 block text-sm font-semibold text-slate-200"

                >

                  Upload visual evidence{" "}

                  <span className="font-normal text-slate-500">(optional)</span>

                </label>



                <label

                  htmlFor="issue-image"

                  className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-white/15 bg-[#0b1020] px-5 py-7 text-center transition hover:border-cyan-400/50 hover:bg-cyan-400/[0.03]"

                >

                  <span className="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-400/10 text-2xl">

                    ↑

                  </span>



                  <span className="text-sm font-semibold text-white">

                    {selectedImage ? "Change image" : "Choose an image"}

                  </span>



                  <span className="mt-2 text-xs text-slate-500">

                    JPG, PNG, or WebP · Maximum 5 MB

                  </span>



                  <input

                    id="issue-image"

                    type="file"

                    accept="image/jpeg,image/png,image/webp"

                    onChange={handleImageChange}

                    className="sr-only"

                  />

                </label>



                {imagePreview && (

                  <div className="mt-4 overflow-hidden rounded-xl border border-white/10">

                    <img

                      src={imagePreview}

                      alt="Selected civic issue evidence"

                      className="max-h-64 w-full object-contain"

                    />



                    <div className="flex items-center justify-between gap-3 bg-white/[0.04] px-3 py-2">

                      <span className="truncate text-xs text-slate-400">

                        {selectedImage?.name}

                      </span>



                      <button

                        type="button"

                        onClick={() => {

                          setSelectedImage(null);

                          setImagePreview("");

                          const input = document.getElementById("issue-image");

                          if (input) input.value = "";

                        }}

                        className="shrink-0 text-xs font-semibold text-red-300 hover:text-red-200"

                      >

                        Remove

                      </button>

                    </div>

                  </div>

                )}

              </div>



              {error && (

                <div

                  role="alert"

                  className="rounded-xl border border-red-400/20 bg-red-400/10 p-4 text-sm leading-6 text-red-200"

                >

                  {error}

                </div>

              )}



              <button

                type="submit"

                disabled={isAnalyzing}

                className="flex w-full items-center justify-center gap-3 rounded-xl bg-gradient-to-r from-violet-600 to-cyan-600 px-5 py-4 text-sm font-bold text-white shadow-lg shadow-violet-950/30 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"

              >

                {isAnalyzing ? (

                  <>

                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />

                    Analyzing your report...

                  </>

                ) : (

                  <>✦ Generate Civic Report</>

                )}

              </button>



              <p className="text-center text-xs leading-5 text-slate-500">

                AI-generated guidance can contain errors. Verify important

                details before submitting an official complaint.

              </p>

            </form>

          </section>



          <section className="min-w-0">

            {!report && !isAnalyzing && (

              <div className="flex min-h-[440px] flex-col items-center justify-center rounded-3xl border border-dashed border-white/10 bg-white/[0.02] px-8 py-12 text-center">

                <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-3xl border border-violet-400/20 bg-violet-400/10 text-4xl">

                  ✧

                </div>



                <h2 className="text-2xl font-bold text-white">

                  Your report starts here

                </h2>



                <p className="mt-3 max-w-sm text-sm leading-6 text-slate-400">

                  Submit a description or an image to receive issue

                  classification, severity, practical next steps, evidence

                  guidance, and a complaint draft.

                </p>



                <div className="mt-8 flex flex-wrap justify-center gap-2">

                  {[

                    "Text + image AI",

                    "6 languages",

                    "Voice input",

                    "Location context",

                    "Complaint draft",

                  ].map((item) => (

                    <span

                      key={item}

                      className="rounded-full border border-white/10 bg-white/[0.04] px-3 py-2 text-xs text-slate-400"

                    >

                      {item}

                    </span>

                  ))}

                </div>

              </div>

            )}



            {isAnalyzing && (

              <div className="flex min-h-[440px] flex-col items-center justify-center rounded-3xl border border-white/10 bg-white/[0.025] p-8 text-center">

                <div className="h-12 w-12 animate-spin rounded-full border-2 border-violet-400/20 border-t-cyan-400" />



                <h2 className="mt-6 text-xl font-bold text-white">

                  Building your civic report

                </h2>



                <p className="mt-3 max-w-sm text-sm leading-6 text-slate-400">

                  Sahayak AI is processing the available information and

                  preparing a consolidated report in your selected language.

                </p>



                <div className="mt-6 flex flex-wrap justify-center gap-2 text-xs text-slate-500">

                  <span>Analyzing evidence</span>

                  <span>·</span>

                  <span>Assessing severity</span>

                  <span>·</span>

                  <span>Preparing actions</span>

                </div>

              </div>

            )}



            {report && !isAnalyzing && (

              <div className="space-y-5">

                <div className="rounded-3xl border border-cyan-400/20 bg-gradient-to-br from-cyan-400/[0.08] to-violet-500/[0.08] p-5 sm:p-7">

                  <div className="flex flex-wrap items-start justify-between gap-4">

                    <div className="min-w-0 flex-1">

                      <p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-300">

                        {ui.consolidated}

                      </p>



                      <h2 className="mt-3 break-words text-2xl font-bold leading-tight text-white sm:text-3xl">

                        {report.title || "Civic issue report"}

                      </h2>



                      <p className="mt-3 text-sm leading-6 text-slate-300">

                        {report.summary}

                      </p>

                    </div>



                    <span

                      className={`inline-flex shrink-0 items-center rounded-full border px-3 py-2 text-xs font-bold ${severityStyle}`}

                    >

                      {ui.severity[severity] || ui.severity.Medium}

                    </span>

                  </div>



                  {report.severity_reason && (

                    <div className="mt-5 rounded-xl border border-white/10 bg-black/10 p-4">

                      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">

                        {ui.severityWhy}

                      </p>

                      <p className="mt-2 text-sm leading-6 text-slate-300">

                        {report.severity_reason}

                      </p>

                    </div>

                  )}



                  <div className="mt-6 flex flex-wrap items-center gap-4">

                    {report.problem_category && (

                      <span className="inline-flex max-w-full items-center break-words rounded-full border border-violet-300/20 bg-violet-300/10 px-4 py-2 text-xs font-medium leading-5 text-violet-200">

                        {report.problem_category}

                      </span>

                    )}



                    <span className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-xs font-medium text-cyan-200">

                      <span aria-hidden="true">文</span>

                      {LANGUAGES.find((item) => item.code === language)?.label}

                    </span>



                    {location.trim() && (

                      <span className="inline-flex max-w-full items-center gap-2 break-words rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs text-slate-300">

                        <span aria-hidden="true">📍</span>

                        {location.trim()}

                      </span>

                    )}

                  </div>

                </div>



                <div className="grid gap-5 sm:grid-cols-2">

                  <Section title={ui.immediate}>

                    <BulletList items={report.immediate_actions} />

                  </Section>



                  <Section title={ui.observations}>

                    <BulletList

                      items={report.confirmed_observations}

                      emptyMessage={ui.noDetails}

                    />

                  </Section>



                  <Section title={ui.evidence}>

                    <BulletList items={report.evidence_needed} />

                  </Section>



                  <Section title={ui.uncertainties}>

                    <BulletList

                      items={report.uncertainties}

                      emptyMessage={ui.noUncertainties}

                    />

                  </Section>

                </div>



                <Section title={ui.authority}>

                  <p className="text-sm leading-6 text-slate-300">

                    {report.recommended_authority || ui.authorityFallback}

                  </p>

                  <p className="mt-3 text-xs leading-5 text-slate-500">

                    {ui.verifyAuthority}

                  </p>

                </Section>



                <Section title={ui.complaint}>

                  <p className="mb-4 text-sm leading-6 text-slate-400">

                    {ui.reviewDraft}

                  </p>



                  <div style={{ whiteSpace: "pre-wrap" }} className="break-words rounded-xl border border-white/10 bg-[#090d19] p-4 text-sm leading-7 text-slate-300">

                    {formatComplaintDraft(

                      report.report_draft ||

                        "No complaint draft was generated."

                    )}

                  </div>



                  <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:gap-4">

                    <button

                      type="button"

                      onClick={handleCopy}

                      disabled={!report.report_draft}

                      className="rounded-xl border border-cyan-400/30 bg-cyan-400/10 px-4 py-2.5 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-400/20 disabled:opacity-50"

                    >

                      {copied ? ui.copied : ui.copy}

                    </button>



                    <button

                      type="button"

                      onClick={handleReset}

                      className="rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm font-semibold text-slate-300 transition hover:bg-white/[0.08]"

                    >

                      {ui.another}

                    </button>

                  </div>

                </Section>



                {report.citizen_explanation && (

                  <Section title={ui.simple}>

                    <p className="text-sm leading-7 text-slate-300">

                      {report.citizen_explanation}

                    </p>

                  </Section>

                )}



                <p className="px-2 text-xs leading-5 text-slate-500">

                  {ui.disclaimer}

                </p>

              </div>

            )}

          </section>

        </div>



        <footer className="mt-12 border-t border-white/10 pt-6 text-center text-xs leading-6 text-slate-500">

          Sahayak AI · Multimodal civic assistance · Built for VORTEX 2K26

        </footer>

      </main>

    </div>

  );

}
