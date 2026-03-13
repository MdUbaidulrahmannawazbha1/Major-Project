"""
Advanced Resume Analyzer — upgraded with:
- Career-stage-aware skill gap detection
- Resume draft generation
- LinkedIn profile suggestions
- Portfolio recommendations
"""

import re
from typing import Dict, List, Optional
try:
    from PyPDF2 import PdfReader
    _PYPDF2_AVAILABLE = True
except ImportError:
    _PYPDF2_AVAILABLE = False
    PdfReader = None


# ─────────────────────────────────────────────────────────────────────
# Skill Dictionaries (expanded beyond original 14 skills)
# ─────────────────────────────────────────────────────────────────────

COMMON_SKILLS = [
    # Programming
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'go', 'rust', 'kotlin',
    # Data
    'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
    # ML / AI
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
    'nlp', 'computer vision', 'data analysis', 'data science', 'statistics',
    # Engineering
    'react', 'node', 'django', 'flask', 'spring boot', 'rest api', 'graphql',
    # DevOps / Cloud
    'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd', 'terraform', 'git',
    # Professional
    'communication', 'project management', 'agile', 'scrum', 'excel',
    # Design
    'figma', 'adobe xd', 'ui/ux', 'wireframing', 'prototyping',
    # Finance
    'financial modelling', 'accounting', 'economics', 'valuation',
    # Medical
    'clinical skills', 'patient care', 'pharmacology', 'anatomy',
    # Research
    'research methodology', 'academic writing', 'matlab', 'r',
]

# Career-stage specific skill requirements
CAREER_STAGE_SKILLS: Dict[str, Dict[str, List[str]]] = {
    "School": {
        "core": ["logical thinking", "mathematics", "communication", "english", "problem solving"],
        "recommended": ["basic programming", "critical thinking", "teamwork", "time management"],
        "gap_message": "Focus on building a strong academic foundation and exploring interests.",
    },
    "PUC": {
        "core": ["mathematics", "physics/chemistry/biology", "communication", "logical reasoning"],
        "recommended": ["basic python", "microsoft office", "presentation skills", "research skills"],
        "gap_message": "Start exploring programming and subject-specific skills for your chosen stream.",
    },
    "Undergraduate": {
        "core": ["programming", "data structures", "algorithms", "sql", "communication", "git"],
        "recommended": ["machine learning", "web development", "cloud basics", "internships", "projects"],
        "gap_message": "Build a project portfolio and seek internship experience alongside academics.",
    },
    "Postgraduate": {
        "core": ["advanced domain knowledge", "research methodology", "data analysis", "publications"],
        "recommended": ["machine learning", "academic writing", "conference presentations", "networking"],
        "gap_message": "Focus on research output, publications, and domain specialization.",
    },
    "PhD": {
        "core": ["research writing", "publications", "data analysis", "domain expertise", "grant writing"],
        "recommended": ["academic collaboration", "conference presentations", "mentoring", "teaching"],
        "gap_message": "Build a strong publication record and international research collaborations.",
    },
    "Professional": {
        "core": ["leadership", "strategic thinking", "stakeholder management", "communication", "domain expertise"],
        "recommended": ["ai tools", "digital transformation", "upskilling", "networking", "thought leadership"],
        "gap_message": "Stay ahead of industry trends; consider upskilling in AI and digital tools.",
    },
}

COURSE_RECOMMENDATIONS: Dict[str, List[str]] = {
    'python': ['Python for Everybody — Coursera (free audit)', 'Automate the Boring Stuff — Udemy'],
    'machine learning': ['Machine Learning Specialization — Coursera (Andrew Ng)', 'Hands-On ML — OReilly'],
    'deep learning': ['Deep Learning Specialization — Coursera', 'fast.ai Practical Deep Learning'],
    'sql': ['SQL for Data Science — Coursera', 'Mode Analytics SQL Tutorial (free)'],
    'aws': ['AWS Cloud Practitioner — AWS Training (free)', 'AWS Solutions Architect — Udemy'],
    'docker': ['Docker for Developers — Udemy', 'Play with Docker (free)'],
    'react': ['React — The Complete Guide — Udemy', 'Full Stack Open — University of Helsinki (free)'],
    'data analysis': ['Google Data Analytics Certificate — Coursera', 'DataCamp Data Analyst Track'],
    'git': ['Git & GitHub — Udemy', 'Learn Git Branching (free)'],
    'communication': ['Business English Communication — Coursera', 'Toastmasters (local club)'],
    'tensorflow': ['TensorFlow Developer Certificate — Coursera', 'TensorFlow Tutorials (free)'],
    'figma': ['Google UX Design Certificate — Coursera', 'Figma Tutorial — YouTube'],
    'research methodology': ['Research Methods — Coursera', 'Purdue OWL — Academic Writing (free)'],
    'financial modelling': ['Financial Modelling & Valuation — Udemy', 'Wall Street Prep'],
    'kubernetes': ['Kubernetes for Developers — Pluralsight', 'CNCF Kubernetes Fundamentals (free)'],
    'statistics': ['Statistics with Python — Coursera', 'Khan Academy Statistics (free)'],
}


# ─────────────────────────────────────────────────────────────────────
# Core Text Extraction
# ─────────────────────────────────────────────────────────────────────

def extract_text_from_pdf(path: str) -> str:
    if not _PYPDF2_AVAILABLE:
        return ""
    text = []
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    except Exception:
        return ""
    return "\n".join(text)


def extract_contact_info(text: str) -> Dict[str, List[str]]:
    email_re = r'[\w\.-]+@[\w\.-]+'
    phone_re = r'(?:\+\d{1,3}[- ]?)?\d{10,13}'
    emails = re.findall(email_re, text)
    phones = re.findall(phone_re, text)
    return {'emails': list(set(emails))[:2], 'phones': list(set(phones))[:2]}


def extract_education(text: str) -> List[str]:
    degrees = []
    patterns = [
        r'Bachelor\b.*', r'Master\b.*', r'B\.Sc\b.*', r'M\.Sc\b.*',
        r'BTech\b.*', r'MTech\b.*', r'MBBS\b.*', r'PhD\b.*',
        r'B\.Tech\b.*', r'M\.Tech\b.*', r'BCA\b.*', r'MCA\b.*',
        r'BBA\b.*', r'MBA\b.*', r'LLB\b.*', r'B\.Com\b.*',
    ]
    for pat in patterns:
        found = re.findall(pat, text, flags=re.IGNORECASE)
        for f in found:
            degrees.append(f.strip()[:100])
    return list(set(degrees))


def generate_roadmap(skill_gaps: List[str]) -> Dict[str, List[str]]:
    roadmap = {}
    for skill in skill_gaps:
        recs = COURSE_RECOMMENDATIONS.get(skill, [f'Intro to {skill} — Search online or YouTube'])
        roadmap[skill] = recs
    return roadmap


# ─────────────────────────────────────────────────────────────────────
# Advanced Skill Gap Detection (Career Stage Aware)
# ─────────────────────────────────────────────────────────────────────

def analyze_skill_gap_by_stage(
    found_skills: List[str],
    education_level: str,
    career_goal: Optional[str] = None,
) -> Dict:
    """
    Detect skill gaps based on the user's career stage.

    Returns stage-appropriate core gaps, recommended improvements,
    and prioritised learning actions.
    """
    stage_info = CAREER_STAGE_SKILLS.get(education_level, CAREER_STAGE_SKILLS["Undergraduate"])
    core_required = [s.lower() for s in stage_info["core"]]
    recommended = [s.lower() for s in stage_info["recommended"]]
    found_lower = {s.lower() for s in found_skills}

    core_gaps = [s for s in core_required if not any(s in f for f in found_lower)]
    recommended_gaps = [s for s in recommended if not any(s in f for f in found_lower)]

    gap_severity = "High" if len(core_gaps) > 3 else ("Medium" if len(core_gaps) > 1 else "Low")

    actions = []
    for gap in (core_gaps + recommended_gaps)[:5]:
        courses = COURSE_RECOMMENDATIONS.get(gap, [f'Search online for: {gap}'])
        actions.append({
            "skill": gap,
            "priority": "Critical" if gap in core_gaps else "Recommended",
            "courses": courses,
        })

    return {
        "education_level": education_level,
        "career_goal": career_goal,
        "core_skill_gaps": core_gaps,
        "recommended_improvements": recommended_gaps,
        "gap_severity": gap_severity,
        "gap_message": stage_info["gap_message"],
        "learning_actions": actions,
    }


# ─────────────────────────────────────────────────────────────────────
# Resume Draft Generator
# ─────────────────────────────────────────────────────────────────────

def generate_resume_draft(
    name: str,
    email: str,
    phone: str,
    education_level: str,
    career_goal: str,
    skills: List[str],
    experience: Optional[List[Dict]] = None,
    projects: Optional[List[Dict]] = None,
) -> str:
    """
    Generate a plain-text resume draft the user can copy and customise.
    """
    experience = experience or []
    projects = projects or []

    skills_str = " | ".join(skills[:12]) if skills else "Add your skills here"

    experience_section = ""
    if experience:
        lines = []
        for exp in experience:
            lines.append(f"  {exp.get('role', 'Role')} @ {exp.get('company', 'Company')} ({exp.get('duration', 'Duration')})")
            lines.append(f"  - {exp.get('description', 'Describe your key responsibilities and achievements.')}")
        experience_section = "\nEXPERIENCE\n" + "\n".join(lines)
    else:
        experience_section = "\nEXPERIENCE\n  [Add internships, part-time roles, volunteering, or freelance work]"

    projects_section = ""
    if projects:
        lines = []
        for proj in projects:
            lines.append(f"  {proj.get('title', 'Project Title')}")
            lines.append(f"  Tech: {proj.get('tech', 'Technologies used')}")
            lines.append(f"  - {proj.get('description', 'Describe the project and your contribution.')}")
            if proj.get('github'):
                lines.append(f"  GitHub: {proj['github']}")
        projects_section = "\nPROJECTS\n" + "\n".join(lines)
    else:
        projects_section = "\nPROJECTS\n  [Add 2-3 relevant projects with GitHub links]"

    objective = (
        f"Aspiring {career_goal} with a background in {education_level} studies. "
        f"Eager to leverage skills in {', '.join(skills[:3]) if skills else 'the domain'} "
        f"to contribute to impactful work."
    )

    draft = f"""
{'='*60}
{name.upper()}
{'='*60}
Email: {email}  |  Phone: {phone}
LinkedIn: linkedin.com/in/{name.lower().replace(' ', '-')}
GitHub:   github.com/{name.lower().replace(' ', '')}

OBJECTIVE
  {objective}

EDUCATION
  {education_level}
  [Add: Institution Name | Year | CGPA/Percentage]

TECHNICAL SKILLS
  {skills_str}

{experience_section}

{projects_section}

CERTIFICATIONS
  [Add relevant certifications with platform and year]

ACHIEVEMENTS
  [Add awards, hackathon wins, publications, or recognitions]

{'='*60}
Resume generated by AI Career Navigation Platform
{'='*60}
""".strip()

    return draft


# ─────────────────────────────────────────────────────────────────────
# LinkedIn Profile Suggestions
# ─────────────────────────────────────────────────────────────────────

def generate_linkedin_suggestions(
    name: str,
    career_goal: str,
    skills: List[str],
    education_level: str,
) -> Dict:
    """
    Return structured LinkedIn profile improvement suggestions.
    """
    headline = f"{career_goal} | {' | '.join(skills[:3])}" if skills else f"Aspiring {career_goal}"

    about = (
        f"I am a passionate {career_goal} with expertise in {', '.join(skills[:5]) if skills else 'my domain'}. "
        f"Currently at {education_level} level, I am focused on building practical skills through projects, "
        f"internships, and continuous learning. Open to opportunities and collaborations."
    )

    return {
        "headline": headline,
        "about_section": about,
        "skills_to_add": skills[:15],
        "sections_to_complete": [
            "Add a professional profile photo",
            "Write a compelling 'About' section (3-5 lines)",
            "List all education with CGPA and activities",
            "Add internships and work experience",
            "List projects with tech stack and GitHub links",
            "Request 3+ LinkedIn recommendations from professors/peers",
            "Follow thought leaders in your domain",
            "Share 1 post per week about what you are learning",
        ],
        "connection_strategy": [
            f"Connect with {career_goal}s at top companies",
            "Join LinkedIn Groups related to your field",
            "Engage with posts from your target companies",
        ],
    }


# ─────────────────────────────────────────────────────────────────────
# Portfolio Recommendations
# ─────────────────────────────────────────────────────────────────────

def generate_portfolio_recommendations(
    career_goal: str,
    skills: List[str],
    education_level: str,
) -> Dict:
    """
    Return portfolio project ideas tailored to the user's career goal and level.
    """
    project_ideas: Dict[str, List[Dict]] = {
        "Data Scientist": [
            {"title": "House Price Prediction", "tech": "Python, pandas, scikit-learn, Streamlit", "difficulty": "Beginner"},
            {"title": "Customer Churn Analysis", "tech": "Python, ML, Power BI", "difficulty": "Intermediate"},
            {"title": "NLP Sentiment Analyser", "tech": "Python, NLTK/spaCy, Flask", "difficulty": "Intermediate"},
        ],
        "Software Engineer": [
            {"title": "Task Manager Web App", "tech": "React, Node.js, MongoDB", "difficulty": "Beginner"},
            {"title": "E-commerce Platform", "tech": "Django, PostgreSQL, Docker", "difficulty": "Intermediate"},
            {"title": "Real-time Chat App", "tech": "WebSocket, Node.js, Redis", "difficulty": "Advanced"},
        ],
        "AI Engineer": [
            {"title": "AI Chatbot with RAG", "tech": "LangChain, OpenAI API, FAISS", "difficulty": "Intermediate"},
            {"title": "Image Classifier", "tech": "TensorFlow, CNN, Streamlit", "difficulty": "Intermediate"},
            {"title": "LLM Fine-tuning Project", "tech": "HuggingFace, LoRA, T4 GPU", "difficulty": "Advanced"},
        ],
        "UX Designer": [
            {"title": "Food Delivery App Redesign", "tech": "Figma, User Research", "difficulty": "Beginner"},
            {"title": "E-learning Platform UX", "tech": "Figma, Prototyping, Usability Test", "difficulty": "Intermediate"},
            {"title": "Accessibility Audit & Redesign", "tech": "Figma, WCAG 2.1", "difficulty": "Advanced"},
        ],
        "Financial Analyst": [
            {"title": "Stock Portfolio Tracker", "tech": "Excel, Python, yfinance", "difficulty": "Beginner"},
            {"title": "DCF Valuation Model", "tech": "Excel, Financial Modelling", "difficulty": "Intermediate"},
            {"title": "Credit Risk Model", "tech": "Python, scikit-learn, Logistic Regression", "difficulty": "Advanced"},
        ],
    }

    # Fuzzy match career goal to project ideas
    goal_lower = career_goal.lower()
    matched_ideas = []
    for career_key, ideas in project_ideas.items():
        if career_key.lower() in goal_lower or goal_lower in career_key.lower():
            matched_ideas = ideas
            break

    if not matched_ideas:
        matched_ideas = [
            {"title": f"{career_goal} Portfolio Project 1", "tech": " | ".join(skills[:3]), "difficulty": "Beginner"},
            {"title": f"{career_goal} Case Study", "tech": "Domain tools", "difficulty": "Intermediate"},
        ]

    return {
        "career_goal": career_goal,
        "education_level": education_level,
        "portfolio_projects": matched_ideas,
        "hosting_platforms": [
            "GitHub — code repositories",
            "Vercel / Netlify — web app hosting (free)",
            "Streamlit Cloud — Python ML apps (free)",
            "Behance — design portfolios",
            "Notion — project write-ups and case studies",
        ],
        "portfolio_tips": [
            "Write a clear README for every project",
            "Include a demo link or screenshots",
            "Explain the problem, approach, and results",
            "Add a personal portfolio website (GitHub Pages / Vercel)",
            "Keep projects updated and add new ones regularly",
        ],
    }


# ─────────────────────────────────────────────────────────────────────
# Main Analyze Function (backward compatible + extended)
# ─────────────────────────────────────────────────────────────────────

def analyze_resume(
    path: str,
    education_level: Optional[str] = None,
    career_goal: Optional[str] = None,
) -> Dict:
    """
    Full resume analysis: skills, gaps, contact, education, roadmap.
    Optionally includes career-stage-aware skill gap analysis.

    Backward compatible with the original return format.
    """
    text = extract_text_from_pdf(path).lower()
    found = []
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.append(skill)

    gaps = [s for s in COMMON_SKILLS if s not in found]
    contact = extract_contact_info(text)
    education = extract_education(text)
    # Limit roadmap to top 10 gaps to avoid overwhelming the user
    roadmap = generate_roadmap(gaps[:10])

    result = {
        "found_skills": found,
        "skill_gaps": gaps,
        "contact_info": contact,
        "education": education,
        "roadmap": roadmap,
    }

    # Extended analysis if education_level is provided
    if education_level:
        result["stage_analysis"] = analyze_skill_gap_by_stage(
            found_skills=found,
            education_level=education_level,
            career_goal=career_goal,
        )

    return result
