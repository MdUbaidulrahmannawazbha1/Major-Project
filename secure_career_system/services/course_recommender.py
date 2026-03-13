"""
Course Recommender — suggests undergraduate courses (B.Tech, BCA, MBBS, etc.)
for Class 12 / PUC graduates based on stream, marks, skills, and interests.
"""

from typing import Dict, List, Optional

COURSE_CATALOG: Dict[str, Dict] = {
    "B.Tech": {
        "streams": ["Science"],
        "min_marks": 60,
        "duration": "4 years",
        "description": "Bachelor of Technology — core engineering and technology degree.",
        "specializations": ["Computer Science", "Mechanical", "Electrical", "Civil", "Electronics"],
        "entrance_exams": ["JEE Main", "JEE Advanced", "KCET", "COMEDK"],
        "careers": ["Software Engineer", "Systems Engineer", "Data Engineer", "Hardware Engineer"],
        "top_colleges": ["IITs", "NITs", "IIITs", "RVCE", "PES University"],
        "salary_range": "₹4–40 LPA",
        "interest_keywords": ["engineering", "technology", "coding", "programming", "software",
                               "hardware", "robotics", "electronics", "ai", "machine learning"],
    },
    "BCA": {
        "streams": ["Science", "Commerce"],
        "min_marks": 50,
        "duration": "3 years",
        "description": "Bachelor of Computer Applications — software and IT focused degree.",
        "specializations": ["Software Development", "Data Science", "Cybersecurity", "AI"],
        "entrance_exams": ["University Entrance Tests"],
        "careers": ["Software Developer", "Web Developer", "Data Analyst", "IT Support"],
        "top_colleges": ["Christ University", "Symbiosis", "REVA University"],
        "salary_range": "₹3–15 LPA",
        "interest_keywords": ["computer", "coding", "programming", "web", "app development", "software"],
    },
    "B.Sc": {
        "streams": ["Science"],
        "min_marks": 50,
        "duration": "3 years",
        "description": "Bachelor of Science — foundational science and research degree.",
        "specializations": ["Physics", "Chemistry", "Mathematics", "Biology", "Data Science", "Biotechnology"],
        "entrance_exams": ["University Entrance Tests", "CUET"],
        "careers": ["Scientist", "Researcher", "Teacher", "Lab Analyst", "Data Analyst"],
        "top_colleges": ["St. Xavier's", "Christ University", "Lady Shri Ram College", "DU"],
        "salary_range": "₹2–12 LPA",
        "interest_keywords": ["science", "research", "laboratory", "biology", "physics", "chemistry"],
    },
    "MBBS": {
        "streams": ["Science"],
        "min_marks": 80,
        "duration": "5.5 years",
        "description": "Bachelor of Medicine and Bachelor of Surgery — primary medical degree.",
        "specializations": ["General Medicine", "Surgery", "Pediatrics", "Psychiatry", "Radiology"],
        "entrance_exams": ["NEET-UG"],
        "careers": ["Doctor", "Surgeon", "Specialist", "Researcher"],
        "top_colleges": ["AIIMS", "CMC Vellore", "JIPMER", "Government Medical Colleges"],
        "salary_range": "₹8–60 LPA",
        "interest_keywords": ["medicine", "doctor", "health", "biology", "patient care", "surgery", "hospital"],
    },
    "BBA": {
        "streams": ["Commerce", "Arts"],
        "min_marks": 50,
        "duration": "3 years",
        "description": "Bachelor of Business Administration — management and business degree.",
        "specializations": ["Finance", "Marketing", "HR", "International Business", "Entrepreneurship"],
        "entrance_exams": ["IPU CET", "SET", "University Tests"],
        "careers": ["Manager", "Entrepreneur", "Marketing Executive", "HR Manager", "Business Analyst"],
        "top_colleges": ["Christ University", "Symbiosis", "NMIMS", "Amity"],
        "salary_range": "₹3–12 LPA",
        "interest_keywords": ["business", "management", "marketing", "finance", "entrepreneurship", "leadership"],
    },
    "B.Com": {
        "streams": ["Commerce"],
        "min_marks": 45,
        "duration": "3 years",
        "description": "Bachelor of Commerce — accounting, finance, and business fundamentals.",
        "specializations": ["Accounting", "Finance", "Taxation", "Banking"],
        "entrance_exams": ["CUET", "University Tests"],
        "careers": ["Accountant", "CA Aspirant", "Financial Analyst", "Tax Consultant"],
        "top_colleges": ["SRCC Delhi", "Christ University", "Loyola Chennai"],
        "salary_range": "₹2–10 LPA",
        "interest_keywords": ["accounting", "finance", "commerce", "ca", "banking", "taxation"],
    },
    "Law (LLB)": {
        "streams": ["Arts", "Commerce"],
        "min_marks": 45,
        "duration": "3 years (after graduation) or 5 years (BA LLB)",
        "description": "Bachelor of Laws — legal studies and practice.",
        "specializations": ["Corporate Law", "Criminal Law", "Constitutional Law", "Cyber Law"],
        "entrance_exams": ["CLAT", "AILET", "LSAT India"],
        "careers": ["Lawyer", "Judge", "Legal Consultant", "Corporate Counsel"],
        "top_colleges": ["NLUs", "Delhi University Faculty of Law", "Symbiosis Law School"],
        "salary_range": "₹4–30 LPA",
        "interest_keywords": ["law", "justice", "legal", "court", "constitution", "rights", "advocacy"],
    },
    "Design": {
        "streams": ["Arts", "Science", "Commerce"],
        "min_marks": 50,
        "duration": "4 years",
        "description": "Bachelor of Design — creative and user experience design programs.",
        "specializations": ["Fashion Design", "Graphic Design", "UI/UX", "Product Design", "Interior Design"],
        "entrance_exams": ["NID DAT", "NIFT Entrance", "UCeed"],
        "careers": ["UI/UX Designer", "Fashion Designer", "Graphic Designer", "Product Designer"],
        "top_colleges": ["NID", "NIFT", "MIT Institute of Design", "Pearl Academy"],
        "salary_range": "₹3–20 LPA",
        "interest_keywords": ["design", "art", "creative", "visual", "fashion", "graphic", "ux", "ui"],
    },
    "Animation": {
        "streams": ["Arts", "Science"],
        "min_marks": 45,
        "duration": "3–4 years",
        "description": "Bachelor in Animation and Visual Effects — media and entertainment creation.",
        "specializations": ["3D Animation", "VFX", "Game Design", "Film Production"],
        "entrance_exams": ["University Entrance Tests", "Portfolio Review"],
        "careers": ["Animator", "VFX Artist", "Game Designer", "Motion Graphics Artist"],
        "top_colleges": ["Arena Animation", "Whistling Woods", "MIT"],
        "salary_range": "₹3–15 LPA",
        "interest_keywords": ["animation", "vfx", "game", "film", "3d", "media", "creative", "drawing"],
    },
    "Civil Services (BA)": {
        "streams": ["Arts", "Science", "Commerce"],
        "min_marks": 50,
        "duration": "3 years",
        "description": "Humanities degree focused on preparing for civil services examinations.",
        "specializations": ["Political Science", "History", "Public Administration", "Sociology"],
        "entrance_exams": ["UPSC", "State PSC"],
        "careers": ["IAS/IPS/IFS Officer", "Government Officer", "Policy Analyst"],
        "top_colleges": ["DU", "JNU", "Hyderabad Central University", "AMU"],
        "salary_range": "₹6–20 LPA (Government Pay Scale)",
        "interest_keywords": ["civil service", "government", "ias", "policy", "administration", "upsc"],
    },
}


def recommend_courses(
    stream: str,
    marks_percentage: float,
    interests: List[str],
    skills: Optional[List[str]] = None,
    assessment_results: Optional[Dict] = None,
) -> Dict:
    """
    Suggest courses for a student finishing Class 12 / PUC.

    Args:
        stream: The student's Class 12 stream (Science / Commerce / Arts / Diploma).
        marks_percentage: Aggregate marks percentage (0–100).
        interests: List of interest keywords from the student.
        skills: Optional list of existing skills.
        assessment_results: Optional dict from career assessment.

    Returns:
        dict with primary recommendation, alternatives, and full course details.
    """
    scored: List[tuple] = []
    interests_lower = [i.lower() for i in interests]
    skills_lower = [s.lower() for s in (skills or [])]

    for course, info in COURSE_CATALOG.items():
        # Stream eligibility
        if stream not in info["streams"]:
            continue
        # Marks eligibility
        if marks_percentage < info["min_marks"]:
            continue

        score = 0.0

        # Interest match
        for kw in info["interest_keywords"]:
            if any(kw in i for i in interests_lower):
                score += 20.0
                break

        # Skill affinity
        for kw in info["interest_keywords"]:
            if any(kw in s for s in skills_lower):
                score += 10.0
                break

        # Marks bonus (higher marks → more options open at top score)
        score += (marks_percentage - info["min_marks"]) * 0.3

        scored.append((course, score, info))

    # Sort descending
    scored.sort(key=lambda x: x[1], reverse=True)

    if not scored:
        return {
            "primary_recommendation": None,
            "message": "No courses found matching your stream and marks. Consider Diploma or open university programs.",
            "alternatives": [],
        }

    primary_course, primary_score, primary_info = scored[0]
    alternatives = [
        {
            "course": c,
            "score": round(s, 1),
            "duration": i["duration"],
            "careers": i["careers"],
            "entrance_exams": i["entrance_exams"],
        }
        for c, s, i in scored[1:5]
    ]

    return {
        "primary_recommendation": {
            "course": primary_course,
            "score": round(primary_score, 1),
            **primary_info,
        },
        "alternatives": alternatives,
        "all_eligible": [c for c, *_ in scored],
        "message": f"Based on your {stream} stream, {marks_percentage}% marks, and interests.",
    }
