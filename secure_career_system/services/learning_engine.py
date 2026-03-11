"""
AI Personal Learning Engine — generates structured, phased learning roadmaps
based on target career, current skills, and education level.
"""

LEARNING_TEMPLATES = {
    'AI Engineer': {
        'phases': [
            {
                'phase': 'Phase 1 – Foundations',
                'duration': '2 months',
                'topics': [
                    {'topic': 'Python Programming', 'resources': ['Python for Everybody (Coursera)', 'Automate the Boring Stuff']},
                    {'topic': 'Mathematics (Linear Algebra, Calculus)', 'resources': ['Khan Academy', '3Blue1Brown YouTube']},
                    {'topic': 'Statistics & Probability', 'resources': ['Statistics with Python (Coursera)']},
                ],
            },
            {
                'phase': 'Phase 2 – Core Skills',
                'duration': '3 months',
                'topics': [
                    {'topic': 'Machine Learning', 'resources': ['Machine Learning by Andrew Ng (Coursera)', 'Hands-On ML (O\'Reilly)']},
                    {'topic': 'Data Analysis with Pandas & NumPy', 'resources': ['Kaggle Learn']},
                    {'topic': 'Deep Learning', 'resources': ['Deep Learning Specialization (Coursera)', 'Fast.ai']},
                ],
            },
            {
                'phase': 'Phase 3 – Projects',
                'duration': '2 months',
                'topics': [
                    {'topic': 'AI Chatbot Project', 'resources': ['Build with Hugging Face Transformers']},
                    {'topic': 'Image Classifier', 'resources': ['TensorFlow/PyTorch tutorials']},
                    {'topic': 'NLP Text Analyzer', 'resources': ['spaCy documentation', 'NLTK tutorials']},
                ],
            },
            {
                'phase': 'Phase 4 – Career Preparation',
                'duration': '1 month',
                'topics': [
                    {'topic': 'Portfolio & GitHub Profile', 'resources': ['GitHub Portfolio Guide']},
                    {'topic': 'Interview Preparation', 'resources': ['LeetCode', 'ML Interview Questions']},
                    {'topic': 'Resume Building', 'resources': ['Resume tips for AI roles']},
                ],
            },
        ],
    },
    'Data Scientist': {
        'phases': [
            {
                'phase': 'Phase 1 – Foundations',
                'duration': '2 months',
                'topics': [
                    {'topic': 'Python & SQL', 'resources': ['Python for Data Science (Coursera)', 'SQLBolt']},
                    {'topic': 'Statistics', 'resources': ['Statistics Fundamentals (StatQuest YouTube)']},
                ],
            },
            {
                'phase': 'Phase 2 – Core Skills',
                'duration': '3 months',
                'topics': [
                    {'topic': 'Data Wrangling', 'resources': ['Pandas documentation', 'Kaggle courses']},
                    {'topic': 'Machine Learning', 'resources': ['Scikit-learn tutorials', 'Andrew Ng ML course']},
                    {'topic': 'Data Visualization', 'resources': ['Matplotlib/Seaborn', 'Tableau Public']},
                ],
            },
            {
                'phase': 'Phase 3 – Projects',
                'duration': '2 months',
                'topics': [
                    {'topic': 'Exploratory Data Analysis Project', 'resources': ['Kaggle datasets']},
                    {'topic': 'Predictive Modeling Project', 'resources': ['Kaggle competitions']},
                ],
            },
            {
                'phase': 'Phase 4 – Career Preparation',
                'duration': '1 month',
                'topics': [
                    {'topic': 'Portfolio & Blog', 'resources': ['Medium', 'GitHub']},
                    {'topic': 'Interview Preparation', 'resources': ['Data Science interview guides']},
                ],
            },
        ],
    },
    'Software Engineer': {
        'phases': [
            {
                'phase': 'Phase 1 – Foundations',
                'duration': '2 months',
                'topics': [
                    {'topic': 'Programming Language (Python/Java)', 'resources': ['freeCodeCamp', 'Codecademy']},
                    {'topic': 'Git & Version Control', 'resources': ['Git documentation', 'GitHub Learning Lab']},
                ],
            },
            {
                'phase': 'Phase 2 – Core Skills',
                'duration': '3 months',
                'topics': [
                    {'topic': 'Data Structures & Algorithms', 'resources': ['LeetCode', 'NeetCode YouTube']},
                    {'topic': 'Web Development (HTML/CSS/JS)', 'resources': ['The Odin Project', 'MDN Web Docs']},
                    {'topic': 'Database Fundamentals', 'resources': ['SQLBolt', 'MongoDB University']},
                ],
            },
            {
                'phase': 'Phase 3 – Projects',
                'duration': '2 months',
                'topics': [
                    {'topic': 'Full Stack Web App', 'resources': ['Build with React + Node.js']},
                    {'topic': 'REST API Project', 'resources': ['Flask/Express tutorials']},
                ],
            },
            {
                'phase': 'Phase 4 – Career Preparation',
                'duration': '1 month',
                'topics': [
                    {'topic': 'System Design Basics', 'resources': ['System Design Primer (GitHub)']},
                    {'topic': 'Interview Preparation', 'resources': ['LeetCode', 'Pramp mock interviews']},
                ],
            },
        ],
    },
    'Cybersecurity Analyst': {
        'phases': [
            {
                'phase': 'Phase 1 – Foundations',
                'duration': '2 months',
                'topics': [
                    {'topic': 'Networking Basics', 'resources': ['CompTIA Network+ study guide']},
                    {'topic': 'Linux Fundamentals', 'resources': ['Linux Journey', 'OverTheWire Bandit']},
                ],
            },
            {
                'phase': 'Phase 2 – Core Skills',
                'duration': '3 months',
                'topics': [
                    {'topic': 'Security Fundamentals', 'resources': ['CompTIA Security+ guide']},
                    {'topic': 'Ethical Hacking', 'resources': ['TryHackMe', 'HackTheBox']},
                    {'topic': 'Python for Security', 'resources': ['Violent Python (book)']},
                ],
            },
            {
                'phase': 'Phase 3 – Projects',
                'duration': '2 months',
                'topics': [
                    {'topic': 'Vulnerability Assessment Lab', 'resources': ['OWASP WebGoat']},
                    {'topic': 'Security Audit Report', 'resources': ['Practice with Metasploitable']},
                ],
            },
            {
                'phase': 'Phase 4 – Career Preparation',
                'duration': '1 month',
                'topics': [
                    {'topic': 'Certification Prep (CEH/Security+)', 'resources': ['Official study guides']},
                    {'topic': 'Interview Preparation', 'resources': ['Cybersecurity interview questions']},
                ],
            },
        ],
    },
}

# Default template for careers not explicitly listed
DEFAULT_TEMPLATE = {
    'phases': [
        {
            'phase': 'Phase 1 – Foundations',
            'duration': '2 months',
            'topics': [
                {'topic': 'Core concepts of the field', 'resources': ['Search for introductory courses on Coursera/edX']},
                {'topic': 'Essential tools and software', 'resources': ['Official documentation and tutorials']},
            ],
        },
        {
            'phase': 'Phase 2 – Core Skills',
            'duration': '3 months',
            'topics': [
                {'topic': 'Advanced domain knowledge', 'resources': ['Specialized courses on Udemy/Coursera']},
                {'topic': 'Practical applications', 'resources': ['Project-based learning platforms']},
            ],
        },
        {
            'phase': 'Phase 3 – Projects',
            'duration': '2 months',
            'topics': [
                {'topic': 'Portfolio project 1', 'resources': ['Build a real-world application']},
                {'topic': 'Portfolio project 2', 'resources': ['Contribute to open source']},
            ],
        },
        {
            'phase': 'Phase 4 – Career Preparation',
            'duration': '1 month',
            'topics': [
                {'topic': 'Resume and portfolio', 'resources': ['Resume writing guides']},
                {'topic': 'Interview preparation', 'resources': ['Domain-specific interview resources']},
            ],
        },
    ],
}


def generate_learning_roadmap(target_career, current_skills=None, education_level=None):
    """Generate a structured learning roadmap.

    Returns: {career, education_level, phases, total_duration}
    """
    current_skills = current_skills or []
    if isinstance(current_skills, str):
        current_skills = [s.strip().lower() for s in current_skills.split(',') if s.strip()]

    # Look up template
    template = None
    for career_name, tmpl in LEARNING_TEMPLATES.items():
        if target_career.lower() in career_name.lower() or career_name.lower() in target_career.lower():
            template = tmpl
            target_career = career_name
            break

    if not template:
        template = DEFAULT_TEMPLATE

    phases = template['phases']

    # Mark topics as "already known" if user has the skill
    for phase in phases:
        for topic in phase['topics']:
            topic_lower = topic['topic'].lower()
            topic['already_known'] = any(s in topic_lower for s in current_skills)

    total_months = sum(int(p['duration'].split()[0]) for p in phases if p['duration'].split()[0].isdigit())

    return {
        'career': target_career,
        'education_level': education_level or 'Not specified',
        'phases': phases,
        'total_duration': f'{total_months} months',
    }
