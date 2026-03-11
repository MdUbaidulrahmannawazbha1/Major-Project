"""AI Skill Gap Analyzer module.

Compares a student's current skills against the skills required for a
specific career path and identifies missing skills with learning
recommendations.
"""

from typing import Dict, List

# Required skills per career path
CAREER_SKILL_REQUIREMENTS: Dict[str, List[str]] = {
    'Technology': [
        'python', 'java', 'c++', 'sql', 'git', 'data structures',
        'algorithms', 'machine learning', 'docker', 'aws', 'react',
        'node', 'linux', 'agile',
    ],
    'Finance': [
        'excel', 'sql', 'financial modeling', 'accounting', 'statistics',
        'data analysis', 'python', 'risk management', 'communication',
        'economics', 'project management',
    ],
    'Healthcare': [
        'biology', 'chemistry', 'patient care', 'medical terminology',
        'research', 'data analysis', 'communication', 'empathy',
        'project management', 'public health', 'statistics',
    ],
}

# Skill importance (higher = more critical for the career)
SKILL_IMPORTANCE: Dict[str, Dict[str, int]] = {
    'Technology': {
        'python': 5, 'java': 4, 'c++': 3, 'sql': 5, 'git': 5,
        'data structures': 5, 'algorithms': 5, 'machine learning': 4,
        'docker': 3, 'aws': 3, 'react': 3, 'node': 3, 'linux': 4, 'agile': 3,
    },
    'Finance': {
        'excel': 5, 'sql': 4, 'financial modeling': 5, 'accounting': 5,
        'statistics': 4, 'data analysis': 4, 'python': 3, 'risk management': 4,
        'communication': 5, 'economics': 4, 'project management': 3,
    },
    'Healthcare': {
        'biology': 5, 'chemistry': 4, 'patient care': 5,
        'medical terminology': 5, 'research': 4, 'data analysis': 3,
        'communication': 5, 'empathy': 4, 'project management': 3,
        'public health': 4, 'statistics': 3,
    },
}

# Learning resources per skill
SKILL_RESOURCES: Dict[str, List[str]] = {
    'python': ['Python for Everybody - Coursera', 'Automate the Boring Stuff - Udemy'],
    'java': ['Java Programming - Coursera', 'Java Masterclass - Udemy'],
    'c++': ['C++ Nanodegree - Udacity', 'Beginning C++ Programming - Udemy'],
    'sql': ['SQL for Data Science - Coursera', 'The Complete SQL Bootcamp - Udemy'],
    'git': ['Git & GitHub Crash Course - Udemy', 'Version Control with Git - Coursera'],
    'data structures': ['Data Structures - Coursera (UCSD)', 'Grokking Algorithms - Book'],
    'algorithms': ['Algorithms Specialization - Coursera (Stanford)', 'LeetCode Practice'],
    'machine learning': ['Machine Learning by Andrew Ng - Coursera', 'Hands-On ML - OReilly'],
    'docker': ['Docker for Developers - Udemy', 'Docker Deep Dive - Pluralsight'],
    'aws': ['AWS Cloud Practitioner - AWS Training', 'AWS Solutions Architect - Udemy'],
    'react': ['React - The Complete Guide - Udemy', 'Full Stack Open - University of Helsinki'],
    'node': ['The Complete Node.js Developer Course - Udemy'],
    'linux': ['Linux Command Line Basics - Udacity', 'Introduction to Linux - edX'],
    'agile': ['Agile with Atlassian Jira - Coursera', 'Scrum Master Certification - Scrum.org'],
    'excel': ['Excel Skills for Business - Coursera', 'Advanced Excel - Udemy'],
    'financial modeling': ['Financial Modeling - CFI', 'Excel to Python for Finance - Udemy'],
    'accounting': ['Introduction to Financial Accounting - Coursera (Wharton)'],
    'statistics': ['Statistics with Python - Coursera', 'Khan Academy Statistics'],
    'data analysis': ['Google Data Analytics Certificate - Coursera', 'Data Analysis with Python - freeCodeCamp'],
    'risk management': ['Financial Risk Manager (FRM) - GARP'],
    'communication': ['Business Communication - Coursera', 'Toastmasters Practice'],
    'economics': ['Principles of Economics - Coursera (MIT)', 'Khan Academy Economics'],
    'project management': ['Google Project Management Certificate - Coursera'],
    'biology': ['Biology Foundations - Khan Academy', 'Introduction to Biology - MIT OCW'],
    'chemistry': ['General Chemistry - Khan Academy', 'Organic Chemistry - Coursera'],
    'patient care': ['Patient Safety - Coursera (Johns Hopkins)'],
    'medical terminology': ['Medical Terminology - Coursera'],
    'research': ['Understanding Clinical Research - Coursera'],
    'empathy': ['Empathy and Emotional Intelligence at Work - edX'],
    'public health': ['Foundations of Public Health - Coursera (Johns Hopkins)'],
}


def analyze_skill_gap(user_skills: List[str], career: str) -> Dict:
    """Compare *user_skills* against required skills for *career*.

    Returns a dict with ``matched_skills``, ``missing_skills`` (sorted by
    importance descending), ``match_percentage`` and ``recommendations``.
    """
    career = career.strip().title()
    required = CAREER_SKILL_REQUIREMENTS.get(career, [])
    importance = SKILL_IMPORTANCE.get(career, {})

    user_lower = [s.strip().lower() for s in user_skills if s.strip()]

    matched = [s for s in required if s.lower() in user_lower]
    missing = [s for s in required if s.lower() not in user_lower]

    # Sort missing by importance (highest first)
    missing.sort(key=lambda s: importance.get(s, 0), reverse=True)

    match_pct = (len(matched) / len(required) * 100) if required else 0

    recommendations = {}
    for skill in missing:
        recommendations[skill] = {
            'importance': importance.get(skill, 0),
            'resources': SKILL_RESOURCES.get(skill, [f'Search for "{skill}" courses online']),
        }

    return {
        'career': career,
        'matched_skills': matched,
        'missing_skills': missing,
        'match_percentage': round(match_pct, 1),
        'total_required': len(required),
        'recommendations': recommendations,
    }
