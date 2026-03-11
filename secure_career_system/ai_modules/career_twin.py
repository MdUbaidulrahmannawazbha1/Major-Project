"""
AI Career Twin — predicts multiple possible career futures based on
user profile, assessment results, skills, and education level.
"""

CAREER_PROFILES = {
    'Data Scientist': {
        'skills': ['python', 'machine learning', 'statistics', 'sql', 'data analysis',
                   'r', 'deep learning', 'tensorflow', 'pandas', 'numpy'],
        'interests': ['data', 'research', 'analytics', 'ai', 'mathematics'],
        'education_bonus': {'PhD': 20, 'Postgraduate': 15, 'Undergraduate': 5},
        'assessment_bias': {'tech': 0.9, 'finance': 0.3, 'healthcare': 0.2},
    },
    'Software Engineer': {
        'skills': ['python', 'java', 'c++', 'javascript', 'git', 'sql', 'react',
                   'node', 'docker', 'aws', 'data structures'],
        'interests': ['programming', 'technology', 'software', 'development', 'web'],
        'education_bonus': {'Undergraduate': 10, 'Postgraduate': 10, 'Professional': 5},
        'assessment_bias': {'tech': 1.0, 'finance': 0.1, 'healthcare': 0.1},
    },
    'AI Researcher': {
        'skills': ['python', 'deep learning', 'machine learning', 'research',
                   'publications', 'tensorflow', 'pytorch', 'mathematics'],
        'interests': ['research', 'ai', 'innovation', 'academics', 'science'],
        'education_bonus': {'PhD': 25, 'Postgraduate': 15, 'Undergraduate': 5},
        'assessment_bias': {'tech': 0.8, 'finance': 0.1, 'healthcare': 0.2},
    },
    'Financial Analyst': {
        'skills': ['excel', 'sql', 'financial modeling', 'data analysis', 'accounting',
                   'power bi', 'statistics'],
        'interests': ['finance', 'economics', 'banking', 'stock market', 'investment'],
        'education_bonus': {'Postgraduate': 15, 'Undergraduate': 10},
        'assessment_bias': {'tech': 0.2, 'finance': 1.0, 'healthcare': 0.1},
    },
    'Healthcare Professional': {
        'skills': ['biology', 'chemistry', 'patient care', 'medical terminology',
                   'communication', 'research'],
        'interests': ['medicine', 'healthcare', 'hospital', 'biology', 'helping'],
        'education_bonus': {'Postgraduate': 15, 'Undergraduate': 10, 'PhD': 20},
        'assessment_bias': {'tech': 0.1, 'finance': 0.1, 'healthcare': 1.0},
    },
    'UX Designer': {
        'skills': ['design', 'figma', 'user research', 'prototyping', 'css',
                   'html', 'javascript', 'adobe'],
        'interests': ['design', 'creative', 'ux', 'ui', 'user experience', 'art'],
        'education_bonus': {'Undergraduate': 10, 'Postgraduate': 10},
        'assessment_bias': {'tech': 0.6, 'finance': 0.1, 'healthcare': 0.1},
    },
    'Cybersecurity Analyst': {
        'skills': ['networking', 'linux', 'security', 'python', 'penetration testing',
                   'firewalls', 'encryption'],
        'interests': ['security', 'hacking', 'networking', 'technology', 'protection'],
        'education_bonus': {'Undergraduate': 10, 'Postgraduate': 15},
        'assessment_bias': {'tech': 0.9, 'finance': 0.2, 'healthcare': 0.1},
    },
    'Product Manager': {
        'skills': ['communication', 'project management', 'data analysis', 'sql',
                   'leadership', 'agile', 'strategy'],
        'interests': ['business', 'technology', 'strategy', 'management', 'product'],
        'education_bonus': {'Postgraduate': 15, 'Professional': 15, 'Undergraduate': 5},
        'assessment_bias': {'tech': 0.5, 'finance': 0.5, 'healthcare': 0.2},
    },
    'Cloud Architect': {
        'skills': ['aws', 'azure', 'docker', 'kubernetes', 'linux', 'networking',
                   'terraform', 'python'],
        'interests': ['cloud', 'infrastructure', 'devops', 'technology', 'scalability'],
        'education_bonus': {'Undergraduate': 10, 'Professional': 15},
        'assessment_bias': {'tech': 1.0, 'finance': 0.1, 'healthcare': 0.1},
    },
    'Civil Servant (IAS/IPS)': {
        'skills': ['communication', 'general knowledge', 'writing', 'leadership',
                   'current affairs', 'history', 'geography'],
        'interests': ['government', 'civil services', 'public service', 'politics',
                      'administration', 'upsc'],
        'education_bonus': {'Undergraduate': 10, 'Postgraduate': 15},
        'assessment_bias': {'tech': 0.2, 'finance': 0.3, 'healthcare': 0.3},
    },
}


def _normalize(items):
    if not items:
        return []
    if isinstance(items, str):
        items = [s.strip() for s in items.split(',')]
    return [s.lower().strip() for s in items if s and s.strip()]


def predict_career_twins(skills=None, interests=None, education_level=None,
                         assessment_scores=None):
    """Predict multiple career futures with probability scores.

    Parameters:
        skills: list or comma-separated string of user skills
        interests: list or comma-separated string of user interests
        education_level: one of School, PUC, Undergraduate, Postgraduate, PhD, Professional
        assessment_scores: dict with keys tech, finance, healthcare (0-5 each)

    Returns: list of {career, probability, matched_skills, reasons}
    """
    user_skills = _normalize(skills)
    user_interests = _normalize(interests)
    education_level = education_level or 'Undergraduate'
    scores = assessment_scores or {}

    results = []
    for career, profile in CAREER_PROFILES.items():
        probability = 0
        reasons = []

        # Skill match (max 40%)
        skill_matches = [s for s in user_skills
                         if any(k in s for k in profile['skills'])]
        skill_score = min(len(skill_matches) * 8, 40)
        probability += skill_score
        if skill_matches:
            reasons.append(f"Skills: {', '.join(skill_matches[:5])}")

        # Interest match (max 25%)
        int_matches = [i for i in user_interests
                       if any(k in i for k in profile['interests'])]
        int_score = min(len(int_matches) * 7, 25)
        probability += int_score
        if int_matches:
            reasons.append(f"Interests: {', '.join(int_matches[:3])}")

        # Education bonus (max 25%)
        edu_bonus = profile['education_bonus'].get(education_level, 0)
        probability += edu_bonus
        if edu_bonus:
            reasons.append(f"Education level ({education_level}) bonus: +{edu_bonus}%")

        # Assessment bias (max 10%)
        if scores:
            bias = profile['assessment_bias']
            assessment_bonus = 0
            for key, weight in bias.items():
                val = scores.get(key, 0)
                if isinstance(val, (int, float)):
                    assessment_bonus += (val / 5.0) * weight * 10
            assessment_bonus = min(assessment_bonus, 10)
            probability += assessment_bonus
            if assessment_bonus > 2:
                reasons.append(f"Assessment alignment: +{assessment_bonus:.0f}%")

        probability = min(max(int(probability), 0), 99)  # cap at 99 – no single prediction is absolute

        results.append({
            'career': career,
            'probability': probability,
            'matched_skills': skill_matches[:5],
            'reasons': reasons,
        })

    results.sort(key=lambda x: x['probability'], reverse=True)
    return results
