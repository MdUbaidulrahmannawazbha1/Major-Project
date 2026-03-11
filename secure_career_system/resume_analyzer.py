import re
from typing import Dict, List
from PyPDF2 import PdfReader

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    # Ensure required NLTK data is available
    for resource in ('punkt_tab', 'stopwords', 'averaged_perceptron_tagger_eng'):
        try:
            nltk.data.find(f'tokenizers/{resource}' if 'punkt' in resource
                           else f'corpora/{resource}' if 'stop' in resource
                           else f'taggers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)
    _NLTK_AVAILABLE = True
except Exception:
    _NLTK_AVAILABLE = False


# Extended skill taxonomy grouped by category
SKILL_TAXONOMY: Dict[str, List[str]] = {
    'programming': [
        'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'ruby',
        'go', 'rust', 'kotlin', 'swift', 'php', 'r', 'scala', 'perl',
    ],
    'web': [
        'html', 'css', 'react', 'angular', 'vue', 'node', 'express',
        'django', 'flask', 'spring', 'rest api',
    ],
    'data': [
        'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'data analysis',
        'data visualization', 'tableau', 'power bi', 'excel', 'pandas',
    ],
    'ai_ml': [
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'statistics',
    ],
    'devops_cloud': [
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd', 'jenkins',
        'terraform', 'ansible', 'linux', 'git',
    ],
    'soft_skills': [
        'communication', 'project management', 'leadership', 'teamwork',
        'problem solving', 'agile', 'scrum',
    ],
}

# Flatten for quick lookup
COMMON_SKILLS: List[str] = []
for skills in SKILL_TAXONOMY.values():
    COMMON_SKILLS.extend(skills)
COMMON_SKILLS = sorted(set(COMMON_SKILLS))


# Career-specific required skills
CAREER_REQUIRED_SKILLS: Dict[str, List[str]] = {
    'Technology': [
        'python', 'java', 'sql', 'git', 'docker', 'aws', 'react', 'node',
        'machine learning', 'linux', 'agile', 'data analysis',
    ],
    'Finance': [
        'excel', 'sql', 'python', 'data analysis', 'statistics',
        'communication', 'project management', 'r',
    ],
    'Healthcare': [
        'data analysis', 'statistics', 'python', 'r', 'excel',
        'communication', 'project management',
    ],
}


COURSE_RECOMMENDATIONS: Dict[str, List[str]] = {
    'python': ['Python for Everybody - Coursera', 'Automate the Boring Stuff - Udemy'],
    'java': ['Java Programming Masterclass - Udemy'],
    'machine learning': ['Machine Learning by Andrew Ng - Coursera', 'Hands-On ML - OReilly'],
    'sql': ['SQL for Data Science - Coursera', 'The Complete SQL Bootcamp - Udemy'],
    'aws': ['AWS Cloud Practitioner - AWS Training'],
    'docker': ['Docker for Developers - Udemy'],
    'react': ['React - The Complete Guide - Udemy'],
    'git': ['Git & GitHub Crash Course - Udemy'],
    'data analysis': ['Google Data Analytics Certificate - Coursera'],
    'statistics': ['Statistics with Python - Coursera'],
    'excel': ['Excel Skills for Business - Coursera'],
    'communication': ['Business Communication - Coursera'],
    'linux': ['Linux Command Line Basics - Udacity'],
    'agile': ['Agile with Atlassian Jira - Coursera'],
    'node': ['The Complete Node.js Developer Course - Udemy'],
    'deep learning': ['Deep Learning Specialization - Coursera'],
    'tensorflow': ['TensorFlow Developer Certificate - Coursera'],
    'r': ['R Programming - Coursera (Johns Hopkins)'],
    'project management': ['Google Project Management Certificate - Coursera'],
}


def extract_text_from_pdf(path: str) -> str:
    """Extract plain text from a PDF file."""
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


def extract_contact_info(text: str) -> Dict[str, list]:
    """Extract email addresses and phone numbers from text."""
    email_re = r'[\w\.-]+@[\w\.-]+'
    phone_re = r'(?:\+\d{1,3}[- ]?)?\d{10,13}'
    emails = re.findall(email_re, text)
    phones = re.findall(phone_re, text)
    return {'emails': list(set(emails))[:2], 'phones': list(set(phones))[:2]}


def extract_education(text: str) -> List[str]:
    """Extract degree mentions from text."""
    degrees: List[str] = []
    patterns = [
        r'Bachelor\b.*', r'Master\b.*', r'B\.Sc\b.*', r'M\.Sc\b.*',
        r'BTech\b.*', r'MTech\b.*', r'B\.E\b.*', r'M\.E\b.*',
        r'MBA\b.*', r'PhD\b.*', r'B\.Com\b.*', r'BCA\b.*', r'MCA\b.*',
    ]
    for pat in patterns:
        found = re.findall(pat, text, flags=re.IGNORECASE)
        for f in found:
            degrees.append(f.strip())
    return degrees


def _nlp_extract_skills(text: str) -> List[str]:
    """Use NLTK tokenization to extract skills via n-gram matching.

    Tokenizes the text, generates unigrams and bigrams, then matches
    against the skill taxonomy.  Falls back to simple regex when NLTK
    is not available.
    """
    text_lower = text.lower()

    if not _NLTK_AVAILABLE:
        # Fallback: simple regex matching
        found = []
        for skill in COMMON_SKILLS:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found.append(skill)
        return found

    tokens = word_tokenize(text_lower)
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t.isalnum() or t in {'c++', 'c#'}]

    # Generate bigrams for multi-word skills
    bigrams = [f'{tokens[i]} {tokens[i + 1]}' for i in range(len(tokens) - 1)]
    trigrams = [f'{tokens[i]} {tokens[i + 1]} {tokens[i + 2]}' for i in range(len(tokens) - 2)]
    all_ngrams = set(tokens) | set(bigrams) | set(trigrams)

    found = []
    for skill in COMMON_SKILLS:
        # Check direct n-gram match
        if skill in all_ngrams:
            found.append(skill)
        # Also check with regex for cases like ci/cd
        elif re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill)

    return sorted(set(found))


def generate_roadmap(skill_gaps: List[str]) -> Dict[str, List[str]]:
    """Generate a learning roadmap with course recommendations for each gap."""
    roadmap = {}
    for skill in skill_gaps:
        recs = COURSE_RECOMMENDATIONS.get(skill, [f'Intro to {skill} - Search online'])
        roadmap[skill] = recs
    return roadmap


def analyze_resume(path: str, target_career: str = 'Technology') -> Dict:
    """Analyze a resume PDF: extract skills via NLP, identify gaps and recommend courses.

    Parameters
    ----------
    path : str
        Path to the PDF file.
    target_career : str
        Career to compare skills against (default ``'Technology'``).

    Returns
    -------
    dict
        Keys: ``found_skills``, ``skill_categories``, ``skill_gaps``,
        ``contact_info``, ``education``, ``roadmap``, ``match_percentage``.
    """
    text = extract_text_from_pdf(path)
    text_lower = text.lower()

    # NLP-based skill extraction
    found = _nlp_extract_skills(text_lower)

    # Categorise found skills
    categories: Dict[str, List[str]] = {}
    for cat, cat_skills in SKILL_TAXONOMY.items():
        matched = [s for s in found if s in cat_skills]
        if matched:
            categories[cat] = matched

    # Compute career-specific skill gap
    career_key = target_career.strip().title()
    required = CAREER_REQUIRED_SKILLS.get(career_key, CAREER_REQUIRED_SKILLS['Technology'])
    gaps = [s for s in required if s not in found]
    match_pct = ((len(required) - len(gaps)) / len(required) * 100) if required else 0

    contact = extract_contact_info(text)
    education = extract_education(text)
    roadmap = generate_roadmap(gaps)

    return {
        "found_skills": found,
        "skill_categories": categories,
        "skill_gaps": gaps,
        "match_percentage": round(match_pct, 1),
        "contact_info": contact,
        "education": education,
        "roadmap": roadmap,
    }
