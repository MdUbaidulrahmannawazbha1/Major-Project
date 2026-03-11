"""
Career Simulator — generates step-by-step career paths from current education
level to target career.
"""

CAREER_SIMULATIONS = {
    'AI Engineer': {
        'School': [
            {'step': 1, 'action': 'Choose Science stream (PCM)', 'duration': '2 years'},
            {'step': 2, 'action': 'Score well in 12th; prepare for JEE/entrance exams', 'duration': '1 year'},
            {'step': 3, 'action': 'B.Tech in Computer Science / AI', 'duration': '4 years'},
            {'step': 4, 'action': 'Learn Python, Mathematics, Statistics', 'duration': 'During college'},
            {'step': 5, 'action': 'Complete ML & Deep Learning courses', 'duration': '6 months'},
            {'step': 6, 'action': 'Build AI projects & contribute to open source', 'duration': '6 months'},
            {'step': 7, 'action': 'AI/ML internship', 'duration': '3-6 months'},
            {'step': 8, 'action': 'AI Engineer role', 'duration': 'Career start'},
        ],
        'Undergraduate': [
            {'step': 1, 'action': 'Learn Python and Mathematics fundamentals', 'duration': '3 months'},
            {'step': 2, 'action': 'Complete ML & Deep Learning courses', 'duration': '6 months'},
            {'step': 3, 'action': 'Build AI projects & portfolio', 'duration': '4 months'},
            {'step': 4, 'action': 'AI/ML internship', 'duration': '3-6 months'},
            {'step': 5, 'action': 'AI Engineer role', 'duration': 'Career start'},
        ],
        'Professional': [
            {'step': 1, 'action': 'Learn Python basics', 'duration': '1 month'},
            {'step': 2, 'action': 'Statistics & Linear Algebra refresher', 'duration': '2 months'},
            {'step': 3, 'action': 'Machine Learning fundamentals', 'duration': '3 months'},
            {'step': 4, 'action': 'Deep Learning & AI projects', 'duration': '3 months'},
            {'step': 5, 'action': 'Apply for AI roles / internal transition', 'duration': '2 months'},
        ],
    },
    'Data Scientist': {
        'School': [
            {'step': 1, 'action': 'Choose Science stream with Mathematics', 'duration': '2 years'},
            {'step': 2, 'action': 'B.Tech/B.Sc in CS or Statistics', 'duration': '3-4 years'},
            {'step': 3, 'action': 'Learn Python, R, SQL', 'duration': 'During college'},
            {'step': 4, 'action': 'Statistics & probability mastery', 'duration': '6 months'},
            {'step': 5, 'action': 'Data Science projects & Kaggle competitions', 'duration': '6 months'},
            {'step': 6, 'action': 'Data Science internship', 'duration': '3-6 months'},
            {'step': 7, 'action': 'Data Scientist role', 'duration': 'Career start'},
        ],
        'Undergraduate': [
            {'step': 1, 'action': 'Master Python, SQL, and statistics', 'duration': '3 months'},
            {'step': 2, 'action': 'Machine Learning & data visualization', 'duration': '4 months'},
            {'step': 3, 'action': 'Real-world data projects', 'duration': '3 months'},
            {'step': 4, 'action': 'Internship in data analytics', 'duration': '3-6 months'},
            {'step': 5, 'action': 'Data Scientist role', 'duration': 'Career start'},
        ],
        'Professional': [
            {'step': 1, 'action': 'Learn Python & SQL', 'duration': '2 months'},
            {'step': 2, 'action': 'Statistics refresher', 'duration': '1 month'},
            {'step': 3, 'action': 'ML algorithms & tools', 'duration': '3 months'},
            {'step': 4, 'action': 'Portfolio projects', 'duration': '2 months'},
            {'step': 5, 'action': 'Apply for Data Scientist roles', 'duration': '2 months'},
        ],
    },
    'Software Engineer': {
        'School': [
            {'step': 1, 'action': 'Choose Science stream', 'duration': '2 years'},
            {'step': 2, 'action': 'B.Tech CS / BCA', 'duration': '3-4 years'},
            {'step': 3, 'action': 'Master DSA & programming languages', 'duration': 'During college'},
            {'step': 4, 'action': 'Build projects & contribute to open source', 'duration': '1 year'},
            {'step': 5, 'action': 'Software engineering internship', 'duration': '3-6 months'},
            {'step': 6, 'action': 'Software Engineer role', 'duration': 'Career start'},
        ],
        'Undergraduate': [
            {'step': 1, 'action': 'Master a programming language (Python/Java/C++)', 'duration': '2 months'},
            {'step': 2, 'action': 'Data Structures & Algorithms', 'duration': '4 months'},
            {'step': 3, 'action': 'System design basics', 'duration': '2 months'},
            {'step': 4, 'action': 'Build portfolio projects', 'duration': '3 months'},
            {'step': 5, 'action': 'Coding internship', 'duration': '3-6 months'},
            {'step': 6, 'action': 'Software Engineer role', 'duration': 'Career start'},
        ],
        'Professional': [
            {'step': 1, 'action': 'Learn a modern language and framework', 'duration': '2 months'},
            {'step': 2, 'action': 'DSA practice on LeetCode', 'duration': '3 months'},
            {'step': 3, 'action': 'Build side projects', 'duration': '2 months'},
            {'step': 4, 'action': 'Apply for SWE roles', 'duration': '2 months'},
        ],
    },
    'Doctor': {
        'School': [
            {'step': 1, 'action': 'Choose Science stream (PCB)', 'duration': '2 years'},
            {'step': 2, 'action': 'Prepare for NEET UG', 'duration': '1-2 years'},
            {'step': 3, 'action': 'MBBS program', 'duration': '5.5 years'},
            {'step': 4, 'action': 'Internship at hospital', 'duration': '1 year'},
            {'step': 5, 'action': 'Specialization (MD/MS) or practice', 'duration': '3+ years'},
        ],
        'Undergraduate': [
            {'step': 1, 'action': 'Prepare for NEET if not in medical school', 'duration': '1 year'},
            {'step': 2, 'action': 'MBBS / medical program', 'duration': '5.5 years'},
            {'step': 3, 'action': 'Hospital internship', 'duration': '1 year'},
            {'step': 4, 'action': 'Specialization or practice', 'duration': '3+ years'},
        ],
    },
    'Business Analyst': {
        'School': [
            {'step': 1, 'action': 'Choose Commerce stream', 'duration': '2 years'},
            {'step': 2, 'action': 'BBA / B.Com degree', 'duration': '3 years'},
            {'step': 3, 'action': 'Learn Excel, SQL, data visualization', 'duration': 'During college'},
            {'step': 4, 'action': 'MBA (optional but recommended)', 'duration': '2 years'},
            {'step': 5, 'action': 'Business Analyst internship', 'duration': '3-6 months'},
            {'step': 6, 'action': 'Business Analyst role', 'duration': 'Career start'},
        ],
        'Undergraduate': [
            {'step': 1, 'action': 'Learn SQL, Excel, Tableau/Power BI', 'duration': '3 months'},
            {'step': 2, 'action': 'Business case study practice', 'duration': '2 months'},
            {'step': 3, 'action': 'BA internship', 'duration': '3-6 months'},
            {'step': 4, 'action': 'Business Analyst role', 'duration': 'Career start'},
        ],
        'Professional': [
            {'step': 1, 'action': 'Learn data tools (SQL, Tableau)', 'duration': '2 months'},
            {'step': 2, 'action': 'Business domain knowledge', 'duration': '2 months'},
            {'step': 3, 'action': 'Transition to BA role', 'duration': '2 months'},
        ],
    },
}

# Default simulation for unknown careers
DEFAULT_SIMULATION = {
    'School': [
        {'step': 1, 'action': 'Identify interests and strengths through assessments', 'duration': '1 month'},
        {'step': 2, 'action': 'Choose appropriate stream after 10th', 'duration': '2 years'},
        {'step': 3, 'action': 'Select relevant undergraduate course', 'duration': '3-4 years'},
        {'step': 4, 'action': 'Build skills through courses and projects', 'duration': 'Ongoing'},
        {'step': 5, 'action': 'Gain experience through internships', 'duration': '3-6 months'},
        {'step': 6, 'action': 'Start career in chosen field', 'duration': 'Career start'},
    ],
    'Undergraduate': [
        {'step': 1, 'action': 'Identify target career path', 'duration': '1 month'},
        {'step': 2, 'action': 'Build relevant skills', 'duration': '6 months'},
        {'step': 3, 'action': 'Work on projects and portfolio', 'duration': '3 months'},
        {'step': 4, 'action': 'Internship experience', 'duration': '3-6 months'},
        {'step': 5, 'action': 'Apply for entry-level roles', 'duration': 'Career start'},
    ],
    'Professional': [
        {'step': 1, 'action': 'Assess skill gaps for target role', 'duration': '1 month'},
        {'step': 2, 'action': 'Upskill through online courses', 'duration': '3-6 months'},
        {'step': 3, 'action': 'Build side projects', 'duration': '2 months'},
        {'step': 4, 'action': 'Transition to target role', 'duration': '2-3 months'},
    ],
}


def simulate_career(target_career, education_level=None):
    """Generate a step-by-step career simulation.

    Returns: {career, education_level, steps, total_estimated_duration}
    """
    education_level = education_level or 'Undergraduate'

    # Normalize education level
    level_mapping = {
        'school': 'School',
        'puc': 'School',
        'undergraduate': 'Undergraduate',
        'postgraduate': 'Professional',
        'phd': 'Professional',
        'professional': 'Professional',
    }
    normalized_level = level_mapping.get(education_level.lower(), 'Undergraduate')

    career_data = CAREER_SIMULATIONS.get(target_career)
    if career_data and normalized_level in career_data:
        steps = career_data[normalized_level]
    else:
        # Try partial match
        for career_name, data in CAREER_SIMULATIONS.items():
            if target_career.lower() in career_name.lower() or career_name.lower() in target_career.lower():
                if normalized_level in data:
                    steps = data[normalized_level]
                    target_career = career_name
                    break
        else:
            steps = DEFAULT_SIMULATION.get(normalized_level, DEFAULT_SIMULATION['Undergraduate'])

    return {
        'career': target_career,
        'education_level': education_level,
        'steps': steps,
        'total_steps': len(steps),
    }
