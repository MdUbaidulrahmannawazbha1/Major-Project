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


# Feature 5: Advanced Skill Gap Analysis — skills expected at each career stage
STAGE_SKILLS = {
    'School': {
        'core': ['logical thinking', 'math foundation', 'communication', 'english',
                 'basic computer skills', 'time management'],
        'recommended': ['public speaking', 'teamwork', 'curiosity', 'reading habit'],
    },
    'PUC': {
        'core': ['logical thinking', 'math foundation', 'communication', 'english',
                 'basic programming', 'science fundamentals'],
        'recommended': ['critical thinking', 'research skills', 'self-study'],
    },
    'Undergraduate': {
        'core': ['programming', 'data structures', 'algorithms', 'projects',
                 'internships', 'git', 'sql'],
        'recommended': ['open source contributions', 'hackathons', 'technical writing',
                        'presentation skills'],
    },
    'Postgraduate': {
        'core': ['advanced programming', 'research methodology', 'data analysis',
                 'domain expertise', 'project management', 'publications'],
        'recommended': ['conference presentations', 'peer review', 'mentoring',
                        'industry collaboration'],
    },
    'PhD': {
        'core': ['research writing', 'publications', 'data analysis', 'statistical methods',
                 'literature review', 'grant writing', 'peer review'],
        'recommended': ['teaching', 'conference presentations', 'patent writing',
                        'interdisciplinary collaboration'],
    },
    'Professional': {
        'core': ['domain expertise', 'leadership', 'project management', 'communication',
                 'strategic thinking', 'mentoring'],
        'recommended': ['public speaking', 'networking', 'continuous learning',
                        'cross-functional collaboration'],
    },
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


# Feature 5: Advanced Skill Gap Analysis by career stage
def analyze_skill_gaps_by_stage(found_skills, education_level='Undergraduate'):
    """Detect skill gaps based on the user's career stage.

    Returns: {stage, core_gaps, recommended_gaps, coverage_percent}
    """
    found_lower = [s.lower().strip() for s in (found_skills or [])]
    stage_data = STAGE_SKILLS.get(education_level, STAGE_SKILLS['Undergraduate'])

    core_gaps = [s for s in stage_data['core']
                 if not any(sk in s or s in sk for sk in found_lower)]
    recommended_gaps = [s for s in stage_data['recommended']
                        if not any(sk in s or s in sk for sk in found_lower)]
    total = len(stage_data['core'])
    covered = total - len(core_gaps)
    coverage = round((covered / total) * 100, 1) if total else 0

    return {
        'stage': education_level,
        'core_gaps': core_gaps,
        'recommended_gaps': recommended_gaps,
        'coverage_percent': coverage,
    }


# Feature 10: AI Resume + Profile Builder
def generate_resume_draft(user_data):
    """Generate a structured resume draft from user data.

    user_data: dict with keys name, email, education, skills, experience, projects, certifications
    """
    name = user_data.get('name', 'Your Name')
    email = user_data.get('email', 'email@example.com')
    education = user_data.get('education', 'Not specified')
    skills = user_data.get('skills', [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    experience = user_data.get('experience', '')
    projects = user_data.get('projects', [])
    certifications = user_data.get('certifications', [])

    sections = {
        'header': {'name': name, 'email': email},
        'summary': f'Motivated professional with skills in {", ".join(skills[:5]) if skills else "various domains"}.',
        'education': education,
        'skills': skills,
        'experience': experience or 'Add your work experience here.',
        'projects': projects if projects else ['Add your key projects here.'],
        'certifications': certifications if certifications else ['Add relevant certifications.'],
    }
    return sections


def generate_linkedin_suggestions(user_data):
    """Generate LinkedIn profile improvement suggestions."""
    skills = user_data.get('skills', [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    career_goal = user_data.get('career_goal', '')

    suggestions = []
    suggestions.append({
        'section': 'Headline',
        'suggestion': f'Use a descriptive headline like: "{career_goal} | {" | ".join(skills[:3])}"'
        if career_goal and skills
        else 'Add a clear headline with your role and top skills.',
    })
    suggestions.append({
        'section': 'About',
        'suggestion': 'Write a 3-4 sentence summary highlighting your career goals, key skills, and achievements.',
    })
    suggestions.append({
        'section': 'Skills',
        'suggestion': f'Add these skills to your profile: {", ".join(skills[:10])}'
        if skills else 'Add at least 5-10 relevant skills to your profile.',
    })
    suggestions.append({
        'section': 'Experience',
        'suggestion': 'Add quantifiable achievements for each role (e.g., "Increased efficiency by 25%").',
    })
    suggestions.append({
        'section': 'Projects',
        'suggestion': 'Showcase 2-3 key projects with descriptions and links.',
    })
    return suggestions


def generate_portfolio_recommendations(user_data):
    """Generate portfolio recommendations based on user profile."""
    skills = user_data.get('skills', [])
    if isinstance(skills, str):
        skills = [s.strip().lower() for s in skills.split(',') if s.strip()]
    education_level = user_data.get('education_level', 'Undergraduate')

    recommendations = []

    # Tech-related suggestions
    tech_skills = ['python', 'java', 'javascript', 'react', 'node', 'machine learning', 'ai']
    has_tech = any(s in tech_skills for s in skills)
    if has_tech:
        recommendations.append({
            'type': 'GitHub Portfolio',
            'description': 'Create a well-organized GitHub profile with pinned repositories showcasing your best work.',
        })
        recommendations.append({
            'type': 'Technical Blog',
            'description': 'Write technical articles on Medium or dev.to to demonstrate expertise.',
        })

    recommendations.append({
        'type': 'Personal Website',
        'description': 'Build a personal portfolio website with your bio, projects, and contact info.',
    })

    if education_level in ('PhD', 'Postgraduate'):
        recommendations.append({
            'type': 'Research Portfolio',
            'description': 'Maintain a Google Scholar profile and list publications on your website.',
        })

    recommendations.append({
        'type': 'Project Showcase',
        'description': 'Document 3-5 key projects with problem statement, approach, and results.',
    })

    return recommendations
