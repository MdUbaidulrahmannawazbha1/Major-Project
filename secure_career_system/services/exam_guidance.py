"""
Entrance Exam Guidance — maps career goals to relevant entrance exams
and generates preparation roadmaps.
"""

from typing import Dict, List, Optional

EXAM_DATABASE: Dict[str, Dict] = {
    "JEE Main": {
        "full_name": "Joint Entrance Examination (Main)",
        "careers": ["Engineering", "B.Tech", "Computer Science", "Mechanical", "Civil", "Electrical"],
        "eligibility": "Class 12 with PCM (Physics, Chemistry, Mathematics)",
        "frequency": "Twice a year (January and April)",
        "mode": "Online (Computer Based Test)",
        "duration": "3 hours",
        "subjects": ["Mathematics", "Physics", "Chemistry"],
        "colleges": ["NITs", "IIITs", "GFTIs"],
        "preparation_months": 12,
        "preparation_roadmap": [
            {"month": 1, "focus": "Build NCERT foundation — Physics, Chemistry, Maths basics"},
            {"month": 2, "focus": "Mechanics and Algebra — deep practice"},
            {"month": 3, "focus": "Electricity, Thermodynamics, Trigonometry"},
            {"month": 4, "focus": "Modern Physics, Organic Chemistry, Coordinate Geometry"},
            {"month": 5, "focus": "Inorganic Chemistry, Calculus, Waves"},
            {"month": 6, "focus": "Full-length mock tests and weak area revision"},
        ],
        "resources": ["Allen Kota", "Aakash", "Unacademy", "PW (Physics Wallah)", "NCERT Books"],
        "website": "https://jeemain.nta.nic.in",
    },
    "JEE Advanced": {
        "full_name": "Joint Entrance Examination (Advanced)",
        "careers": ["Engineering", "B.Tech (IIT)", "Research"],
        "eligibility": "Top 2.5 lakh JEE Main qualifiers",
        "frequency": "Once a year (May-June)",
        "mode": "Online",
        "duration": "3 hours × 2 papers",
        "subjects": ["Mathematics", "Physics", "Chemistry"],
        "colleges": ["All 23 IITs"],
        "preparation_months": 24,
        "preparation_roadmap": [
            {"month": 1, "focus": "Master JEE Main syllabus first"},
            {"month": 3, "focus": "Advanced-level problem solving — IIT archives"},
            {"month": 6, "focus": "Timed full-length JEE Advanced mock tests"},
            {"month": 9, "focus": "Identify and eliminate weak areas"},
            {"month": 12, "focus": "Final revision and stress management"},
        ],
        "resources": ["IIT archive papers", "HC Verma", "Irodov", "ML Khanna"],
        "website": "https://jeeadvanced.ac.in",
    },
    "KCET": {
        "full_name": "Karnataka Common Entrance Test",
        "careers": ["Engineering", "B.Tech", "B.Pharma", "B.Arch (Karnataka)"],
        "eligibility": "Karnataka domicile; 12th PCM / PCB",
        "frequency": "Once a year (April-May)",
        "mode": "Offline (OMR Based)",
        "duration": "80 minutes per subject",
        "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"],
        "colleges": ["Government Engineering Colleges Karnataka", "Private Engineering Colleges Karnataka"],
        "preparation_months": 6,
        "preparation_roadmap": [
            {"month": 1, "focus": "Complete NCERT Class 11 & 12 equations and theorems"},
            {"month": 2, "focus": "Previous year KCET papers — analyse patterns"},
            {"month": 3, "focus": "Focus on Maths — Integration, Matrices, Algebra"},
            {"month": 4, "focus": "Physics formulas and Chemistry reactions"},
            {"month": 5, "focus": "Full-length KCET mock tests daily"},
            {"month": 6, "focus": "Weak area revision + final mock series"},
        ],
        "resources": ["KEA official website", "Target KCET books", "DigiNerve", "CET Ninja"],
        "website": "https://kea.kar.nic.in",
    },
    "NEET": {
        "full_name": "National Eligibility cum Entrance Test",
        "careers": ["MBBS", "BDS", "BAMS", "BHMS", "Nursing"],
        "eligibility": "Class 12 with PCB (Physics, Chemistry, Biology)",
        "frequency": "Once a year (May)",
        "mode": "Offline (Pen & Paper)",
        "duration": "3 hours 20 minutes",
        "subjects": ["Physics", "Chemistry", "Botany", "Zoology"],
        "colleges": ["All Medical Colleges in India (Government + Private)"],
        "preparation_months": 12,
        "preparation_roadmap": [
            {"month": 1, "focus": "Biology — Cell Biology, Plant Kingdom, Animal Kingdom"},
            {"month": 2, "focus": "Human Physiology — all organ systems"},
            {"month": 3, "focus": "Chemistry — Organic reactions and mechanisms"},
            {"month": 4, "focus": "Physics — Mechanics, Optics, Modern Physics"},
            {"month": 5, "focus": "Genetics, Ecology, Inorganic Chemistry"},
            {"month": 6, "focus": "NEET mock tests — full syllabus revision"},
        ],
        "resources": ["Aakash", "Allen Kota", "NCERT Biology", "DC Pandey", "PW"],
        "website": "https://neet.nta.nic.in",
    },
    "CAT": {
        "full_name": "Common Admission Test",
        "careers": ["MBA", "Management", "Business Administration", "Finance", "HR"],
        "eligibility": "Bachelor's degree with 50% marks",
        "frequency": "Once a year (November)",
        "mode": "Online (Computer Based)",
        "duration": "2 hours",
        "subjects": ["Verbal Ability", "Data Interpretation", "Quantitative Aptitude"],
        "colleges": ["All 20 IIMs", "Top private B-schools"],
        "preparation_months": 6,
        "preparation_roadmap": [
            {"month": 1, "focus": "Quantitative Aptitude — Number systems, Algebra"},
            {"month": 2, "focus": "Data Interpretation — Charts, tables, case lets"},
            {"month": 3, "focus": "Verbal Ability — Reading Comprehension strategies"},
            {"month": 4, "focus": "Mock CAT series and time management"},
            {"month": 5, "focus": "Sectional tests and weak area elimination"},
            {"month": 6, "focus": "Full-length CAT mocks + GD/PI prep"},
        ],
        "resources": ["IMS", "TIME", "Career Launcher", "Arun Sharma books"],
        "website": "https://iimcat.ac.in",
    },
    "CLAT": {
        "full_name": "Common Law Admission Test",
        "careers": ["Law (LLB)", "BA LLB", "Legal Practice", "Judiciary"],
        "eligibility": "12th pass (45% marks); For LLM: LLB with 55%",
        "frequency": "Once a year (December)",
        "mode": "Online (Computer Based)",
        "duration": "2 hours",
        "subjects": ["English", "Current Affairs & GK", "Legal Reasoning", "Logical Reasoning", "Quantitative Techniques"],
        "colleges": ["All 24 National Law Universities (NLUs)"],
        "preparation_months": 6,
        "preparation_roadmap": [
            {"month": 1, "focus": "Legal Reasoning fundamentals + read bare acts"},
            {"month": 2, "focus": "Current Affairs — 6 months history, GK"},
            {"month": 3, "focus": "Logical Reasoning — analogies, syllogisms"},
            {"month": 4, "focus": "English — Reading Comprehension + vocabulary"},
            {"month": 5, "focus": "CLAT mock tests and legal passages practice"},
            {"month": 6, "focus": "Full-length CLAT mocks + NLU-specific prep"},
        ],
        "resources": ["Clat Possible", "LegalEdge", "Vajiram & Ravi", "The Hindu newspaper"],
        "website": "https://consortiumofnlus.ac.in",
    },
    "UPSC CSE": {
        "full_name": "UPSC Civil Services Examination",
        "careers": ["IAS", "IPS", "IFS", "IRS", "Government Officer", "Civil Services"],
        "eligibility": "Graduation in any discipline; Age 21–32 years",
        "frequency": "Once a year (Prelims: June, Mains: September)",
        "mode": "Offline (Written + Interview)",
        "duration": "Prelims: 2 papers × 2h; Mains: 9 papers over 5 days",
        "subjects": ["General Studies (I–IV)", "CSAT", "Optional Subject", "Essay"],
        "colleges": ["LBSNAA (Training Academy for IAS)"],
        "preparation_months": 24,
        "preparation_roadmap": [
            {"month": 1, "focus": "NCERT books (6th to 12th) — all subjects"},
            {"month": 3, "focus": "Indian Polity, History, Geography — standard books"},
            {"month": 6, "focus": "Economy, Environment, Science & Technology"},
            {"month": 9, "focus": "Optional subject — complete first reading"},
            {"month": 12, "focus": "Current affairs integration + Prelims mock tests"},
            {"month": 18, "focus": "Mains answer writing practice daily"},
            {"month": 24, "focus": "Full mock tests + interview preparation"},
        ],
        "resources": ["Vajiram & Ravi", "Vision IAS", "Insights IAS", "ForumIAS", "The Hindu"],
        "website": "https://upsc.gov.in",
    },
    "GATE": {
        "full_name": "Graduate Aptitude Test in Engineering",
        "careers": ["M.Tech", "PSU Jobs", "Research", "PhD Engineering"],
        "eligibility": "B.Tech / B.Sc Engineering",
        "frequency": "Once a year (February)",
        "mode": "Online (Computer Based)",
        "duration": "3 hours",
        "subjects": ["Engineering Mathematics", "General Aptitude", "Core Engineering Subject"],
        "colleges": ["IITs", "NITs", "IIITs", "PSUs"],
        "preparation_months": 6,
        "preparation_roadmap": [
            {"month": 1, "focus": "Engineering Mathematics — Linear Algebra, Calculus"},
            {"month": 2, "focus": "Core subject — fundamentals and theory"},
            {"month": 3, "focus": "Previous year GATE papers (15 years)"},
            {"month": 4, "focus": "Subject-wise mock tests"},
            {"month": 5, "focus": "Full-length GATE mocks + revision"},
            {"month": 6, "focus": "Weak area elimination + final strategy"},
        ],
        "resources": ["Made Easy", "ACE Academy", "NPTEL lectures", "GATEForum"],
        "website": "https://gate.iitk.ac.in",
    },
    "GRE": {
        "full_name": "Graduate Record Examination",
        "careers": ["MS Abroad", "PhD Abroad", "MBA Abroad", "Research"],
        "eligibility": "Bachelor's degree (any discipline)",
        "frequency": "Year-round (on demand)",
        "mode": "Online and Test Center",
        "duration": "3 hours 45 minutes",
        "subjects": ["Verbal Reasoning", "Quantitative Reasoning", "Analytical Writing"],
        "colleges": ["Top US/European Universities (MIT, Stanford, CMU)"],
        "preparation_months": 3,
        "preparation_roadmap": [
            {"month": 1, "focus": "Vocabulary building + Quants fundamentals"},
            {"month": 2, "focus": "Reading Comprehension + AWA essay practice"},
            {"month": 3, "focus": "Full-length ETS GRE mocks + review"},
        ],
        "resources": ["ETS Official Guide", "Magoosh", "Princeton Review", "Manhattan Prep"],
        "website": "https://www.ets.org/gre",
    },
}

CAREER_EXAM_MAP: Dict[str, List[str]] = {
    "Engineering": ["JEE Main", "JEE Advanced", "KCET", "GATE"],
    "Medical": ["NEET"],
    "MBA": ["CAT", "GRE"],
    "Law": ["CLAT"],
    "Government Jobs": ["UPSC CSE"],
    "Research": ["GATE", "GRE", "JEE Advanced"],
    "Technology": ["JEE Main", "JEE Advanced", "GATE", "GRE"],
    "Design": [],
    "Animation": [],
}


def get_exam_guidance(career_goal: str, education_level: Optional[str] = None) -> Dict:
    """
    Return relevant entrance exams and preparation roadmaps for a career goal.

    Args:
        career_goal: Career or field the student is targeting.
        education_level: Current education level (e.g., 'School', 'PUC', 'Undergraduate').

    Returns:
        dict with relevant exams, preparation plans, and resources.
    """
    career_lower = career_goal.lower()
    relevant_exams = []

    # Direct career-to-exam mapping
    for career_key, exams in CAREER_EXAM_MAP.items():
        if career_key.lower() in career_lower:
            relevant_exams.extend(exams)

    # Fuzzy match on exam keywords
    for exam_name, exam_info in EXAM_DATABASE.items():
        for career_kw in exam_info["careers"]:
            if career_kw.lower() in career_lower and exam_name not in relevant_exams:
                relevant_exams.append(exam_name)
                break

    # Deduplicate
    relevant_exams = list(dict.fromkeys(relevant_exams))

    if not relevant_exams:
        return {
            "career_goal": career_goal,
            "exams": [],
            "message": "No specific entrance exams mapped for this career. Explore general aptitude tests or university-specific tests.",
        }

    exam_details = []
    for exam_name in relevant_exams:
        if exam_name in EXAM_DATABASE:
            exam_details.append({"name": exam_name, **EXAM_DATABASE[exam_name]})

    return {
        "career_goal": career_goal,
        "education_level": education_level,
        "recommended_exams": relevant_exams,
        "exam_details": exam_details,
        "total_exams": len(exam_details),
    }


def get_all_exams() -> List[Dict]:
    """Return all available exam entries for display."""
    return [{"name": name, **info} for name, info in EXAM_DATABASE.items()]
