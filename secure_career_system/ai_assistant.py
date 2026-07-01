"""AI Career Assistant module.

Provides an intelligent career guidance chatbot that leverages the existing
ML models and a curated knowledge base to answer student career questions.
"""

import re

# ---------------------------------------------------------------------------
# Career knowledge base
# ---------------------------------------------------------------------------

CAREER_PATHS = {
    "technology": {
        "description": "Technology careers involve developing software, managing systems, and working with data.",
        "roles": [
            "Software Developer", "Data Scientist", "Cloud Engineer",
            "DevOps Engineer", "Frontend Developer", "Backend Developer",
            "Machine Learning Engineer", "Cybersecurity Analyst",
        ],
        "skills": [
            "python", "java", "javascript", "sql", "git", "docker",
            "aws", "react", "node", "machine learning", "data analysis",
        ],
        "courses": [
            "CS50 – Introduction to Computer Science (Harvard/edX)",
            "Python for Everybody (Coursera)",
            "AWS Cloud Practitioner (AWS Training)",
            "The Odin Project (Free full-stack curriculum)",
        ],
        "roadmap": [
            "Learn programming fundamentals (Python / JavaScript)",
            "Build small projects and contribute to open source",
            "Learn databases & SQL",
            "Pick a specialization (web, data, cloud, security)",
            "Earn relevant certifications",
            "Apply for internships / junior roles",
        ],
    },
    "finance": {
        "description": "Finance careers focus on managing money, investments, and financial planning.",
        "roles": [
            "Financial Analyst", "Investment Banker", "Accountant",
            "Risk Manager", "Financial Planner", "Auditor",
        ],
        "skills": [
            "excel", "financial modeling", "accounting", "data analysis",
            "sql", "communication", "project management",
        ],
        "courses": [
            "Financial Markets (Yale/Coursera)",
            "Excel Skills for Business (Macquarie/Coursera)",
            "CFA Level I Preparation",
            "Introduction to Corporate Finance (Wharton/Coursera)",
        ],
        "roadmap": [
            "Master Excel and financial modeling",
            "Understand accounting principles",
            "Learn about capital markets and instruments",
            "Pursue CFA / CPA certifications",
            "Gain internship experience in banking or consulting",
            "Build a network through finance communities",
        ],
    },
    "healthcare": {
        "description": "Healthcare careers involve patient care, research, and medical technology.",
        "roles": [
            "Doctor", "Nurse", "Pharmacist", "Biomedical Engineer",
            "Health Informatics Specialist", "Clinical Researcher",
        ],
        "skills": [
            "biology", "chemistry", "communication", "data analysis",
            "research methodology", "patient care", "empathy",
        ],
        "courses": [
            "Anatomy & Physiology (Khan Academy)",
            "Introduction to Biology (MIT OpenCourseWare)",
            "Health Informatics (Johns Hopkins/Coursera)",
            "Clinical Research (Vanderbilt/Coursera)",
        ],
        "roadmap": [
            "Excel in science subjects (biology, chemistry)",
            "Volunteer at hospitals or clinics",
            "Prepare for entrance exams (NEET / MCAT)",
            "Complete a degree in your chosen healthcare field",
            "Pursue residencies or specializations",
            "Stay current with continuing education",
        ],
    },
}

SKILL_TIPS = {
    "python": "Practice on LeetCode or HackerRank and build projects like web scrapers or REST APIs.",
    "java": "Study object-oriented design patterns and build a Spring Boot application.",
    "sql": "Practice with real datasets on Mode Analytics or SQLZoo.",
    "machine learning": "Start with Andrew Ng's course on Coursera, then implement models on Kaggle.",
    "data analysis": "Learn pandas, matplotlib, and work through exploratory data analysis notebooks.",
    "react": "Follow the official React tutorial, then build a portfolio site.",
    "node": "Build a REST API with Express.js and connect it to a database.",
    "aws": "Use the AWS Free Tier to get hands-on experience with EC2, S3, and Lambda.",
    "docker": "Containerize an existing project and learn Docker Compose for multi-service apps.",
    "git": "Contribute to an open-source project to practice branching, merging, and pull requests.",
    "communication": "Join a public speaking club (Toastmasters) and practice writing technical blogs.",
    "project management": "Learn Agile/Scrum basics and try managing a small team project.",
    "excel": "Take an advanced Excel course and practice building financial models.",
}

GENERAL_TIPS = [
    "Set clear short-term and long-term career goals.",
    "Build a professional portfolio showcasing your best work.",
    "Network actively – attend meetups, webinars, and career fairs.",
    "Keep learning – dedicate time each week to pick up new skills.",
    "Seek mentorship from experienced professionals in your field.",
    "Tailor your resume for each job application.",
    "Practice mock interviews to build confidence.",
]

# ---------------------------------------------------------------------------
# Intent detection helpers
# ---------------------------------------------------------------------------

_INTENT_PATTERNS = [
    ("career_info", re.compile(
        r"\b(career|path|field|domain|industry|sector)\b", re.I)),
    ("skill_advice", re.compile(
        r"\b(skill|learn|improve|study|practice|tip)\b", re.I)),
    ("job_roles", re.compile(
        r"\b(job|role|position|title|opening|hire)\b", re.I)),
    ("course_recommend", re.compile(
        r"\b(course|certificate|certification|training|class|learn)\b", re.I)),
    ("roadmap", re.compile(
        r"\b(roadmap|step|plan|guide|milestone|path)\b", re.I)),
    ("resume_help", re.compile(
        r"\b(resume|cv|cover letter|portfolio)\b", re.I)),
    ("placement", re.compile(
        r"\b(placement|placed|intern|internship|package|salary)\b", re.I)),
    ("mentor", re.compile(
        r"\b(mentor|mentorship|guidance|coach)\b", re.I)),
    ("greeting", re.compile(
        r"\b(hi|hello|hey|good morning|good evening|howdy)\b", re.I)),
    ("thanks", re.compile(
        r"\b(thank|thanks|thankyou|thx)\b", re.I)),
    ("help", re.compile(
        r"\b(help|assist|support|what can you)\b", re.I)),
]


def _detect_intents(query):
    """Return a list of matched intent names."""
    intents = []
    for name, pattern in _INTENT_PATTERNS:
        if pattern.search(query):
            intents.append(name)
    return intents or ["general"]


def _detect_career_domain(query):
    """Try to identify which career domain the user is asking about."""
    q = query.lower()
    if any(kw in q for kw in ("tech", "software", "developer", "programming",
                               "data science", "cloud", "devops", "coding")):
        return "technology"
    if any(kw in q for kw in ("finance", "banking", "accounting", "investment",
                               "financial", "cpa", "cfa")):
        return "finance"
    if any(kw in q for kw in ("health", "medical", "doctor", "nurse",
                               "pharmacy", "clinical", "biology")):
        return "healthcare"
    return None


def _detect_skill(query):
    """Try to identify a specific skill the user is asking about."""
    q = query.lower()
    for skill in SKILL_TIPS:
        if skill in q:
            return skill
    return None

# ---------------------------------------------------------------------------
# Response builder
# ---------------------------------------------------------------------------


def get_reply(query, user_skills=None, career_path=None):
    """Generate a career-guidance reply for the given *query*.

    Parameters
    ----------
    query : str
        The user's message.
    user_skills : list[str] | None
        Skills extracted from the user's profile (optional).
    career_path : str | None
        The user's predicted/chosen career path (optional).

    Returns
    -------
    str
        The assistant's reply.
    """
    if not query or not query.strip():
        return ("Hello! I'm your AI Career Assistant. "
                "Ask me about career paths, skills, courses, or job roles.")

    intents = _detect_intents(query)
    domain = _detect_career_domain(query) or career_path
    skill = _detect_skill(query)

    # ------------------------------------------------------------------
    # Greeting / thanks / help
    # ------------------------------------------------------------------
    if "greeting" in intents and len(intents) == 1:
        return ("Hello! 👋 I'm your AI Career Assistant. "
                "I can help you with career paths, skill advice, course "
                "recommendations, resume tips, and more. How can I help?")

    if "thanks" in intents and len(intents) == 1:
        return ("You're welcome! 😊 Feel free to ask me anything else about "
                "your career journey.")

    if "help" in intents and len(intents) == 1:
        return (
            "Here are some things I can help you with:\n"
            "• **Career paths** – Learn about Technology, Finance, or Healthcare careers\n"
            "• **Skill advice** – Get tips on improving specific skills\n"
            "• **Course recommendations** – Find courses to boost your knowledge\n"
            "• **Job roles** – Discover roles that match your skills\n"
            "• **Career roadmap** – Get a step-by-step plan for your career\n"
            "• **Resume tips** – Improve your resume and portfolio\n"
            "• **Placement guidance** – Understand placement preparation\n"
            "• **Mentorship** – Learn how to find and work with mentors\n\n"
            "Just type your question!"
        )

    # ------------------------------------------------------------------
    # Skill-specific advice
    # ------------------------------------------------------------------
    if skill and "skill_advice" in intents:
        tip = SKILL_TIPS.get(skill, f"Keep practicing {skill} through projects and online resources.")
        return f"**Tip for {skill}:** {tip}"

    # ------------------------------------------------------------------
    # Career domain information
    # ------------------------------------------------------------------
    if domain and domain in CAREER_PATHS:
        info = CAREER_PATHS[domain]

        if "roadmap" in intents:
            steps = "\n".join(f"{i+1}. {s}" for i, s in enumerate(info["roadmap"]))
            return f"**{domain.title()} Career Roadmap:**\n{steps}"

        if "job_roles" in intents:
            roles = ", ".join(info["roles"])
            return f"**Popular {domain.title()} roles:** {roles}"

        if "course_recommend" in intents:
            courses = "\n".join(f"• {c}" for c in info["courses"])
            return f"**Recommended {domain.title()} courses:**\n{courses}"

        if "skill_advice" in intents:
            skills_list = ", ".join(info["skills"])
            return f"**Key skills for {domain.title()}:** {skills_list}"

        # General career info
        roles = ", ".join(info["roles"][:4])
        return (f"**{domain.title()} careers:** {info['description']} "
                f"Some popular roles include {roles}. "
                "Ask me about roadmaps, skills, or courses for more details!")

    # ------------------------------------------------------------------
    # Resume / portfolio help
    # ------------------------------------------------------------------
    if "resume_help" in intents:
        return (
            "Here are some resume tips:\n"
            "• Keep it to 1-2 pages, focusing on relevant experience\n"
            "• Use action verbs (Built, Designed, Led, Implemented)\n"
            "• Quantify achievements where possible\n"
            "• Tailor your resume for each job application\n"
            "• Include a skills section that matches the job description\n"
            "• Upload your resume in this platform for an AI-powered analysis!"
        )

    # ------------------------------------------------------------------
    # Placement guidance
    # ------------------------------------------------------------------
    if "placement" in intents:
        return (
            "**Placement preparation tips:**\n"
            "• Maintain a strong CGPA (aim for 7.0+)\n"
            "• Practice coding problems on LeetCode / HackerRank\n"
            "• Prepare for aptitude tests and group discussions\n"
            "• Work on real-world projects to strengthen your portfolio\n"
            "• Use our Placement Probability tool to check your readiness!\n"
            "• Network with alumni who have been through the process"
        )

    # ------------------------------------------------------------------
    # Mentorship
    # ------------------------------------------------------------------
    if "mentor" in intents:
        return (
            "**Mentorship guidance:**\n"
            "• Browse available mentors on our Mentorship page\n"
            "• Look for mentors whose expertise matches your career goals\n"
            "• When requesting mentorship, be clear about what you want to learn\n"
            "• Be respectful of your mentor's time and come prepared\n"
            "• You can also become a mentor yourself to help others!"
        )

    # ------------------------------------------------------------------
    # Personalized suggestions using user profile
    # ------------------------------------------------------------------
    if user_skills:
        clean = [s.strip() for s in user_skills if s.strip()]
        if clean:
            skills_str = ", ".join(clean[:5])
            tips = []
            for s in clean[:3]:
                if s.lower() in SKILL_TIPS:
                    tips.append(f"• **{s}**: {SKILL_TIPS[s.lower()]}")
            tip_text = "\n".join(tips) if tips else ""
            reply = f"Based on your skills ({skills_str}), here are some suggestions:\n{tip_text}"
            if not tips:
                reply += "Keep building projects and consider exploring related technologies."
            return reply

    # ------------------------------------------------------------------
    # Fallback
    # ------------------------------------------------------------------
    if "career_info" in intents or "job_roles" in intents:
        domains = ", ".join(d.title() for d in CAREER_PATHS)
        return (f"I can provide guidance on these career domains: {domains}. "
                "Which one interests you?")

    if "course_recommend" in intents:
        return ("I can recommend courses for Technology, Finance, or Healthcare. "
                "Which field are you interested in?")

    return (
        "I'm your AI Career Assistant! I can help with:\n"
        "• Career path exploration (Technology, Finance, Healthcare)\n"
        "• Skill improvement tips\n"
        "• Course and certification recommendations\n"
        "• Resume and portfolio advice\n"
        "• Placement preparation\n"
        "• Mentorship guidance\n\n"
        "Try asking something like: *'What skills do I need for a tech career?'*"
    )
