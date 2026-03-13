"""
AI Personal Learning Engine — generates structured, phase-based learning roadmaps
tailored to career goal, education level, and existing skills.
"""

from typing import Dict, List, Optional

PHASE_TEMPLATES: Dict[str, Dict] = {
    "Technology": {
        "phases": [
            {
                "phase": 1,
                "title": "Foundations",
                "duration": "2 months",
                "topics": [
                    "Python Programming Basics",
                    "Mathematics for Computing (Algebra, Statistics)",
                    "Problem Solving & Logic",
                    "Version Control with Git",
                ],
                "resources": [
                    "Python for Everybody — Coursera (free audit)",
                    "Khan Academy — Mathematics",
                    "CS50 — Harvard OpenCourseWare (free)",
                ],
                "milestone": "Build a simple CLI application in Python",
            },
            {
                "phase": 2,
                "title": "Core Skills",
                "duration": "3 months",
                "topics": [
                    "Data Structures and Algorithms",
                    "Object-Oriented Programming",
                    "Database Basics (SQL)",
                    "Web Fundamentals (HTML, CSS, JS) or ML Fundamentals",
                ],
                "resources": [
                    "LeetCode (Easy 100 problems)",
                    "GeeksForGeeks DSA Course",
                    "SQLZoo",
                    "freeCodeCamp",
                ],
                "milestone": "Complete 50 LeetCode problems + build a small database-backed app",
            },
            {
                "phase": 3,
                "title": "Specialization Projects",
                "duration": "3 months",
                "topics": [
                    "Machine Learning / Full Stack / Cloud",
                    "APIs and Integration",
                    "Real-world Dataset Projects",
                    "System Design Basics",
                ],
                "resources": [
                    "Andrew Ng ML Course — Coursera",
                    "Full Stack Open — University of Helsinki",
                    "AWS Free Tier",
                ],
                "milestone": "Build 2 end-to-end projects and publish on GitHub",
            },
            {
                "phase": 4,
                "title": "Career Preparation",
                "duration": "2 months",
                "topics": [
                    "Portfolio Website Creation",
                    "Resume Writing and LinkedIn Optimization",
                    "Technical Interview Preparation",
                    "Mock Interviews",
                ],
                "resources": [
                    "NeetCode.io — Interview Prep",
                    "Pramp — Mock Interviews",
                    "LinkedIn Learning",
                ],
                "milestone": "Apply to 20 companies and clear at least 2 technical interviews",
            },
        ]
    },
    "Finance": {
        "phases": [
            {
                "phase": 1,
                "title": "Financial Fundamentals",
                "duration": "2 months",
                "topics": [
                    "Accounting Basics (Debit/Credit, Balance Sheet)",
                    "Economics Principles",
                    "Mathematics for Finance (Interest, NPV)",
                    "MS Excel for Finance",
                ],
                "resources": [
                    "Khan Academy Economics",
                    "Coursera Financial Accounting",
                    "Excel for Finance — Udemy",
                ],
                "milestone": "Pass a basic accounting quiz with 80%+ score",
            },
            {
                "phase": 2,
                "title": "Core Finance Skills",
                "duration": "3 months",
                "topics": [
                    "Financial Analysis and Modelling",
                    "Investment Valuation (DCF, Comparables)",
                    "Risk Management",
                    "Corporate Finance",
                ],
                "resources": [
                    "CFA Institute Learning Portal",
                    "Damodaran Valuation (NYU free)",
                    "Investopedia",
                ],
                "milestone": "Build a DCF model for a real company",
            },
            {
                "phase": 3,
                "title": "Certification & Specialization",
                "duration": "4 months",
                "topics": [
                    "CA Foundation / CFA Level 1 / CPA",
                    "Taxation and Compliance",
                    "Financial Technology (FinTech)",
                ],
                "resources": [
                    "ICAI study material",
                    "CFA Institute materials",
                    "Bloomberg Market Concepts (free)",
                ],
                "milestone": "Register and attempt CA Foundation / CFA Level 1",
            },
            {
                "phase": 4,
                "title": "Career Preparation",
                "duration": "2 months",
                "topics": [
                    "Interview Preparation for Finance",
                    "Networking via LinkedIn",
                    "Case Study Practice",
                ],
                "resources": [
                    "Wall Street Prep",
                    "Breaking Into Wall Street",
                ],
                "milestone": "Land a finance internship or entry-level analyst role",
            },
        ]
    },
    "Healthcare": {
        "phases": [
            {
                "phase": 1,
                "title": "Medical Foundation",
                "duration": "3 months",
                "topics": [
                    "Human Anatomy and Physiology",
                    "Biochemistry Basics",
                    "Medical Terminology",
                    "Communication in Healthcare",
                ],
                "resources": [
                    "Osmosis Medical Education (YouTube)",
                    "Kenhub Anatomy",
                    "NCERT Biology",
                ],
                "milestone": "Complete anatomy and physiology chapters with self-tests",
            },
            {
                "phase": 2,
                "title": "Clinical Knowledge",
                "duration": "4 months",
                "topics": [
                    "Pathology and Pharmacology",
                    "Clinical Examination Techniques",
                    "Evidence-Based Medicine",
                    "Patient Safety",
                ],
                "resources": [
                    "Geeky Medics",
                    "TeachMeMedicine",
                    "PubMed",
                ],
                "milestone": "Complete 100 clinical MCQs with 75%+ accuracy",
            },
            {
                "phase": 3,
                "title": "Certification and Practice",
                "duration": "4 months",
                "topics": [
                    "Clinical Training (internship/observership)",
                    "Specialization Entrance (PG exams)",
                    "Research and Publications",
                ],
                "resources": [
                    "NEXT exam prep (India)",
                    "USMLE Step 1 resources (for US aspirants)",
                ],
                "milestone": "Obtain clinical certification and complete one research project",
            },
            {
                "phase": 4,
                "title": "Career Advancement",
                "duration": "2 months",
                "topics": [
                    "Residency / Postgraduate Applications",
                    "Medical Conferences and Networking",
                    "Leadership in Healthcare",
                ],
                "resources": [
                    "Indian Medical Association",
                    "BMJ Careers",
                ],
                "milestone": "Apply for PG programs or specialist roles",
            },
        ]
    },
    "Research": {
        "phases": [
            {
                "phase": 1,
                "title": "Research Fundamentals",
                "duration": "2 months",
                "topics": [
                    "Research Methodology",
                    "Literature Review Techniques",
                    "Academic Writing",
                    "Statistics for Research",
                ],
                "resources": [
                    "Coursera Research Methods",
                    "Purdue OWL — Academic Writing",
                    "SPSS / R / Python for statistics",
                ],
                "milestone": "Write a structured literature review on a chosen topic",
            },
            {
                "phase": 2,
                "title": "Domain Deep Dive",
                "duration": "4 months",
                "topics": [
                    "Advanced domain knowledge",
                    "Experimental Design",
                    "Data Collection and Analysis",
                    "Use of research tools",
                ],
                "resources": [
                    "ArXiv, Google Scholar, Semantic Scholar",
                    "MATLAB / Python / R",
                ],
                "milestone": "Submit a paper to a workshop or pre-print a research article",
            },
            {
                "phase": 3,
                "title": "Publication and Conferences",
                "duration": "3 months",
                "topics": [
                    "Peer-reviewed journal submission",
                    "Conference presentations",
                    "Collaboration and networking",
                ],
                "resources": [
                    "Springer, Elsevier, IEEE for submission",
                    "ResearchGate",
                ],
                "milestone": "Get at least one paper accepted or presented",
            },
        ]
    },
}

CAREER_SWITCH_TEMPLATES: Dict[str, Dict] = {
    "Mechanical to AI": {
        "from": "Mechanical Engineering",
        "to": "AI Engineer",
        "months": 6,
        "roadmap": [
            {"month": 1, "focus": "Python Programming — core syntax, data handling"},
            {"month": 2, "focus": "Statistics & Linear Algebra for ML"},
            {"month": 3, "focus": "Machine Learning fundamentals — scikit-learn"},
            {"month": 4, "focus": "Deep Learning basics — TensorFlow / PyTorch"},
            {"month": 5, "focus": "Build 2 AI projects (NLP, Computer Vision, or Recommendation)"},
            {"month": 6, "focus": "Apply for AI Engineer roles, portfolio polish, interview prep"},
        ],
    },
    "Finance to Data Science": {
        "from": "Finance Professional",
        "to": "Data Scientist",
        "months": 6,
        "roadmap": [
            {"month": 1, "focus": "Python for data analysis — pandas, numpy"},
            {"month": 2, "focus": "Statistics (leverage existing finance knowledge)"},
            {"month": 3, "focus": "Machine Learning — regression, classification, clustering"},
            {"month": 4, "focus": "Data visualization — Tableau, Power BI, Matplotlib"},
            {"month": 5, "focus": "Real-world projects — financial data analysis + ML"},
            {"month": 6, "focus": "Apply for Data Scientist / Analyst roles"},
        ],
    },
    "Healthcare to Data Science": {
        "from": "Healthcare Professional",
        "to": "Health Data Scientist",
        "months": 6,
        "roadmap": [
            {"month": 1, "focus": "Python basics + Excel for healthcare data"},
            {"month": 2, "focus": "Healthcare informatics and EHR systems"},
            {"month": 3, "focus": "Statistics + clinical trial data analysis"},
            {"month": 4, "focus": "ML for medicine — predictive diagnostics"},
            {"month": 5, "focus": "Build healthcare ML project (disease prediction)"},
            {"month": 6, "focus": "Apply for health informatics / data science roles"},
        ],
    },
}


def generate_learning_roadmap(
    career_goal: str,
    education_level: str,
    current_skills: Optional[List[str]] = None,
    career_switch_from: Optional[str] = None,
) -> Dict:
    """
    Generate a phase-based learning roadmap.

    Args:
        career_goal: Target career (e.g., 'AI Engineer', 'Data Analyst').
        education_level: e.g., 'School', 'Undergraduate', 'Professional'.
        current_skills: Skills the user already has.
        career_switch_from: Previous domain for career switchers.

    Returns:
        dict with phase-wise roadmap, timeline, and resources.
    """
    current_skills = current_skills or []

    # Career switch detection
    if career_switch_from:
        for switch_key, switch_data in CAREER_SWITCH_TEMPLATES.items():
            if (
                career_switch_from.lower() in switch_data["from"].lower()
                or (
                    career_goal.lower() in switch_data["to"].lower()
                    and career_switch_from.lower() in switch_data["from"].lower()
                )
            ):
                return {
                    "type": "career_switch",
                    "from": switch_data["from"],
                    "to": switch_data["to"],
                    "total_months": switch_data["months"],
                    "monthly_roadmap": switch_data["roadmap"],
                    "message": f"Switching from {switch_data['from']} to {switch_data['to']} in {switch_data['months']} months.",
                }

    # Map career goal to a domain template
    domain = "Technology"
    goal_lower = career_goal.lower()
    if any(kw in goal_lower for kw in ["finance", "accounting", "ca", "banking", "investment"]):
        domain = "Finance"
    elif any(kw in goal_lower for kw in ["doctor", "medical", "nurse", "health", "pharma", "clinical"]):
        domain = "Healthcare"
    elif any(kw in goal_lower for kw in ["research", "phd", "scientist", "publish", "academic"]):
        domain = "Research"

    template = PHASE_TEMPLATES.get(domain, PHASE_TEMPLATES["Technology"])
    phases = template["phases"]

    # Skip Phase 1 if user has foundational skills (reduce roadmap for advanced users)
    if len(current_skills) >= 5 and education_level in ["Undergraduate", "Postgraduate", "PhD", "Professional"]:
        phases = phases[1:]  # Skip foundation phase

    def _parse_months(duration_str: str) -> int:
        """Parse a duration string like '2 months', '2-3 months', '1 year' safely."""
        try:
            parts = duration_str.strip().split()
            if not parts:
                return 3
            first = parts[0]
            if "-" in first:
                low, high = first.split("-", 1)
                val = (int(low) + int(high)) // 2
            else:
                val = int(first)
            if len(parts) > 1 and "year" in parts[1]:
                return val * 12
            return val
        except (ValueError, IndexError):
            return 3

    total_months = sum(_parse_months(p["duration"]) for p in phases)

    return {
        "type": "phased_roadmap",
        "career_goal": career_goal,
        "education_level": education_level,
        "domain": domain,
        "total_months": total_months,
        "phases": phases,
        "current_skills_recognized": current_skills,
        "message": f"Personalized {total_months}-month roadmap to become a {career_goal}.",
    }
