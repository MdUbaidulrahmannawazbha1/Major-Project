import re
from typing import Dict, List
from PyPDF2 import PdfReader


COMMON_SKILLS = [
    'python', 'java', 'c++', 'sql', 'machine learning', 'data analysis', 'excel',
    'communication', 'project management', 'aws', 'docker', 'react', 'node', 'git'
]


COURSE_RECOMMENDATIONS = {
    'python': ['Python for Everybody - Coursera', 'Automate the Boring Stuff - Udemy'],
    'machine learning': ['Machine Learning by Andrew Ng - Coursera', 'Hands-On ML - OReilly'],
    'sql': ['SQL for Data Science - Coursera'],
    'aws': ['AWS Cloud Practitioner - AWS Training'],
    'docker': ['Docker for Developers - Udemy'],
    'react': ['React - The Complete Guide - Udemy']
}


def extract_text_from_pdf(path: str) -> str:
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


def extract_contact_info(text: str) -> Dict[str, str]:
    email_re = r'[\w\.-]+@[\w\.-]+'
    phone_re = r'(?:\+\d{1,3}[- ]?)?\d{10,13}'
    emails = re.findall(email_re, text)
    phones = re.findall(phone_re, text)
    return {'emails': list(set(emails))[:2], 'phones': list(set(phones))[:2]}


def extract_education(text: str) -> List[str]:
    degrees = []
    patterns = [r'Bachelor\b.*', r'Master\b.*', r'B\.Sc\b.*', r'M\.Sc\b.*', r'BTech\b.*', r'MTech\b.*']
    for pat in patterns:
        found = re.findall(pat, text, flags=re.IGNORECASE)
        for f in found:
            degrees.append(f.strip())
    return degrees


def generate_roadmap(skill_gaps: List[str]) -> Dict[str, List[str]]:
    roadmap = {}
    for skill in skill_gaps:
        recs = COURSE_RECOMMENDATIONS.get(skill, [f'Intro to {skill} - Search online'])
        roadmap[skill] = recs
    return roadmap


def analyze_resume(path: str) -> Dict:
    """Resume analyzer that extracts skills, contact info, education and recommends courses for gaps."""
    text = extract_text_from_pdf(path).lower()
    found = []
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.append(skill)

    gaps = [s for s in COMMON_SKILLS if s not in found]

    contact = extract_contact_info(text)
    education = extract_education(text)
    roadmap = generate_roadmap(gaps)

    return {
        "found_skills": found,
        "skill_gaps": gaps,
        "contact_info": contact,
        "education": education,
        "roadmap": roadmap
    }
