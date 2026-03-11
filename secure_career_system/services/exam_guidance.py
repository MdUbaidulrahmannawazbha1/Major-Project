"""
Entrance Exam Guidance — maps careers to entrance exams and generates
preparation roadmaps.
"""

EXAM_DATABASE = {
    'Engineering': {
        'exams': [
            {
                'name': 'JEE Main',
                'description': 'National-level entrance for NITs, IIITs and CFTIs',
                'eligibility': '12th pass with Physics, Chemistry, Mathematics (75%)',
                'frequency': 'Twice a year (January & April)',
                'mode': 'Computer Based Test (CBT)',
                'website': 'https://jeemain.nta.nic.in',
            },
            {
                'name': 'JEE Advanced',
                'description': 'Entrance for IITs; requires qualifying JEE Main',
                'eligibility': 'Top 2.5 lakh JEE Main qualifiers',
                'frequency': 'Once a year',
                'mode': 'Computer Based Test (CBT)',
                'website': 'https://jeeadv.ac.in',
            },
            {
                'name': 'KCET',
                'description': 'Karnataka Common Entrance Test',
                'eligibility': '12th pass from Karnataka with PCM',
                'frequency': 'Once a year',
                'mode': 'Offline (OMR)',
                'website': 'https://cetonline.karnataka.gov.in',
            },
            {
                'name': 'BITSAT',
                'description': 'BITS Pilani entrance exam',
                'eligibility': '12th pass with 75% aggregate in PCM',
                'frequency': 'Once a year',
                'mode': 'Computer Based Test',
                'website': 'https://www.bitsadmission.com',
            },
        ],
        'preparation_roadmap': [
            {'month': '12 months before', 'tasks': ['Complete NCERT syllabus', 'Start with basic problem sets']},
            {'month': '9 months before', 'tasks': ['Solve previous year papers', 'Join mock test series']},
            {'month': '6 months before', 'tasks': ['Focus on weak areas', 'Revise formulas and concepts']},
            {'month': '3 months before', 'tasks': ['Full-length mock tests weekly', 'Time management practice']},
            {'month': '1 month before', 'tasks': ['Revision only', 'Solve 2-3 mock tests per week']},
        ],
    },
    'Medical': {
        'exams': [
            {
                'name': 'NEET UG',
                'description': 'National Eligibility cum Entrance Test for medical courses',
                'eligibility': '12th pass with Physics, Chemistry, Biology (50%)',
                'frequency': 'Once a year',
                'mode': 'Pen and Paper',
                'website': 'https://neet.nta.nic.in',
            },
        ],
        'preparation_roadmap': [
            {'month': '12 months before', 'tasks': ['Complete NCERT Biology, Physics, Chemistry']},
            {'month': '9 months before', 'tasks': ['Solve topic-wise questions', 'Focus on Biology']},
            {'month': '6 months before', 'tasks': ['Previous year NEET papers', 'Mock tests']},
            {'month': '3 months before', 'tasks': ['Full syllabus revision', 'Weekly mock tests']},
            {'month': '1 month before', 'tasks': ['NCERT revision', 'Formula sheets review']},
        ],
    },
    'MBA': {
        'exams': [
            {
                'name': 'CAT',
                'description': 'Common Admission Test for IIMs and top B-schools',
                'eligibility': 'Graduate with 50% marks',
                'frequency': 'Once a year (November)',
                'mode': 'Computer Based Test',
                'website': 'https://iimcat.ac.in',
            },
            {
                'name': 'XAT',
                'description': 'Xavier Aptitude Test for XLRI and associate colleges',
                'eligibility': 'Graduate degree',
                'frequency': 'Once a year (January)',
                'mode': 'Computer Based Test',
                'website': 'https://xatonline.in',
            },
        ],
        'preparation_roadmap': [
            {'month': '8 months before', 'tasks': ['Start Quantitative Aptitude basics', 'Build vocabulary']},
            {'month': '6 months before', 'tasks': ['Solve sectional tests', 'Read newspapers daily']},
            {'month': '3 months before', 'tasks': ['Full-length mocks', 'Analyze performance']},
            {'month': '1 month before', 'tasks': ['Revision', 'Focus on time management']},
        ],
    },
    'Law': {
        'exams': [
            {
                'name': 'CLAT',
                'description': 'Common Law Admission Test for NLUs',
                'eligibility': '12th pass with 45% marks',
                'frequency': 'Once a year',
                'mode': 'Computer Based Test',
                'website': 'https://consortiumofnlus.ac.in',
            },
            {
                'name': 'AILET',
                'description': 'All India Law Entrance Test for NLU Delhi',
                'eligibility': '12th pass with 50% marks',
                'frequency': 'Once a year',
                'mode': 'Computer Based Test',
                'website': 'https://nludelhi.ac.in',
            },
        ],
        'preparation_roadmap': [
            {'month': '6 months before', 'tasks': ['Study Legal Reasoning', 'Current affairs reading']},
            {'month': '4 months before', 'tasks': ['English comprehension', 'Logical reasoning practice']},
            {'month': '2 months before', 'tasks': ['Mock tests', 'GK revision']},
            {'month': '1 month before', 'tasks': ['Full-length tests', 'Time management']},
        ],
    },
    'Government Jobs': {
        'exams': [
            {
                'name': 'UPSC CSE',
                'description': 'Civil Services Examination (IAS/IPS/IFS)',
                'eligibility': 'Graduate degree from recognized university',
                'frequency': 'Once a year',
                'mode': 'Written + Interview',
                'website': 'https://upsc.gov.in',
            },
            {
                'name': 'SSC CGL',
                'description': 'Staff Selection Commission Combined Graduate Level',
                'eligibility': 'Graduate degree',
                'frequency': 'Once a year',
                'mode': 'Computer Based Test',
                'website': 'https://ssc.nic.in',
            },
        ],
        'preparation_roadmap': [
            {'month': '12 months before', 'tasks': ['Choose optional subject', 'Start NCERT reading']},
            {'month': '9 months before', 'tasks': ['Current affairs', 'Answer writing practice']},
            {'month': '6 months before', 'tasks': ['Previous year papers', 'Mock tests']},
            {'month': '3 months before', 'tasks': ['Revision', 'Essay writing practice']},
        ],
    },
    'Design': {
        'exams': [
            {
                'name': 'NID DAT',
                'description': 'NID Design Aptitude Test',
                'eligibility': '12th pass',
                'frequency': 'Once a year',
                'mode': 'Written + Studio Test',
                'website': 'https://admissions.nid.edu',
            },
            {
                'name': 'UCEED',
                'description': 'Undergraduate Common Entrance Exam for Design (IIT)',
                'eligibility': '12th pass',
                'frequency': 'Once a year',
                'mode': 'Computer Based Test',
                'website': 'https://uceed.iitb.ac.in',
            },
        ],
        'preparation_roadmap': [
            {'month': '6 months before', 'tasks': ['Build design portfolio', 'Sketch daily']},
            {'month': '3 months before', 'tasks': ['Study design principles', 'Mock tests']},
            {'month': '1 month before', 'tasks': ['Portfolio refinement', 'Practice studio tests']},
        ],
    },
}

# Map career keywords to exam categories
CAREER_EXAM_MAPPING = {
    'software': 'Engineering',
    'engineer': 'Engineering',
    'technology': 'Engineering',
    'developer': 'Engineering',
    'data scientist': 'Engineering',
    'ai': 'Engineering',
    'doctor': 'Medical',
    'medical': 'Medical',
    'healthcare': 'Medical',
    'surgeon': 'Medical',
    'mba': 'MBA',
    'business': 'MBA',
    'manager': 'MBA',
    'finance': 'MBA',
    'lawyer': 'Law',
    'law': 'Law',
    'legal': 'Law',
    'judge': 'Law',
    'ias': 'Government Jobs',
    'ips': 'Government Jobs',
    'civil services': 'Government Jobs',
    'government': 'Government Jobs',
    'upsc': 'Government Jobs',
    'designer': 'Design',
    'design': 'Design',
    'ux': 'Design',
    'graphic': 'Design',
}


def get_exam_guidance(career=None, category=None):
    """Return exam guidance for a career or category.

    Returns: {category, exams, preparation_roadmap}
    """
    if category and category in EXAM_DATABASE:
        data = EXAM_DATABASE[category]
        return {
            'category': category,
            'exams': data['exams'],
            'preparation_roadmap': data['preparation_roadmap'],
        }

    if career:
        career_lower = career.lower()
        for keyword, cat in CAREER_EXAM_MAPPING.items():
            if keyword in career_lower:
                data = EXAM_DATABASE[cat]
                return {
                    'category': cat,
                    'exams': data['exams'],
                    'preparation_roadmap': data['preparation_roadmap'],
                }

    # Return all categories if no match
    return {
        'category': 'All',
        'categories': list(EXAM_DATABASE.keys()),
        'message': 'Specify a career or category for targeted guidance.',
    }


def list_all_categories():
    """Return all available exam categories."""
    return list(EXAM_DATABASE.keys())
