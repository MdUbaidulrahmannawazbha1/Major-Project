"""
Stream Recommender — recommends academic streams for Class 10 students.

Inputs: favorite_subjects, interests, logical_reasoning_score, personality_traits
Output: ranked list of recommended streams (Science, Commerce, Arts, Diploma)
"""


STREAM_PROFILES = {
    'Science': {
        'subjects': ['mathematics', 'physics', 'chemistry', 'biology', 'science', 'computer'],
        'interests': ['technology', 'engineering', 'medicine', 'research', 'space',
                      'robotics', 'programming', 'lab', 'experiments', 'innovation'],
        'traits': ['analytical', 'curious', 'logical', 'problem-solver', 'detail-oriented'],
        'min_reasoning': 60,
        'description': 'Ideal for students interested in engineering, medicine, research, or technology.',
    },
    'Commerce': {
        'subjects': ['mathematics', 'economics', 'business', 'accounting', 'commerce'],
        'interests': ['finance', 'business', 'entrepreneurship', 'banking', 'stock market',
                      'trading', 'marketing', 'management', 'economics'],
        'traits': ['organized', 'numerical', 'strategic', 'leadership', 'communicative'],
        'min_reasoning': 45,
        'description': 'Ideal for students interested in business, finance, accounting, or management.',
    },
    'Arts': {
        'subjects': ['history', 'geography', 'political science', 'literature', 'english',
                     'hindi', 'psychology', 'sociology', 'languages', 'arts'],
        'interests': ['writing', 'social work', 'law', 'politics', 'journalism',
                      'teaching', 'culture', 'design', 'creative', 'civil services'],
        'traits': ['creative', 'empathetic', 'communicative', 'expressive', 'social'],
        'min_reasoning': 30,
        'description': 'Ideal for students interested in humanities, law, civil services, or creative fields.',
    },
    'Diploma': {
        'subjects': ['mathematics', 'science', 'computer', 'technical', 'workshop'],
        'interests': ['hands-on', 'mechanical', 'electrical', 'automobile', 'construction',
                      'practical', 'technical', 'vocational'],
        'traits': ['practical', 'hands-on', 'technical', 'focused', 'independent'],
        'min_reasoning': 35,
        'description': 'Ideal for students who prefer hands-on technical training and early career entry.',
    },
}


def _normalize(items):
    """Lower-case and strip a list of strings."""
    if not items:
        return []
    if isinstance(items, str):
        items = [s.strip() for s in items.split(',')]
    return [s.lower().strip() for s in items if s and s.strip()]


def recommend_streams(favorite_subjects=None, interests=None,
                      logical_reasoning_score=None, personality_traits=None):
    """Return a list of stream recommendations sorted by match score (descending).

    Each item: {stream, score, description, reasons}
    """
    subjects = _normalize(favorite_subjects)
    interest_list = _normalize(interests)
    traits = _normalize(personality_traits)
    reasoning = logical_reasoning_score if logical_reasoning_score is not None else 50  # default: average ability

    results = []
    for stream, profile in STREAM_PROFILES.items():
        score = 0
        reasons = []

        # Subject match (max 40 pts)
        subj_matches = [s for s in subjects if any(k in s for k in profile['subjects'])]
        subj_score = min(len(subj_matches) * 10, 40)
        score += subj_score
        if subj_matches:
            reasons.append(f"Subject match: {', '.join(subj_matches)}")

        # Interest match (max 30 pts)
        int_matches = [i for i in interest_list if any(k in i for k in profile['interests'])]
        int_score = min(len(int_matches) * 8, 30)
        score += int_score
        if int_matches:
            reasons.append(f"Interest match: {', '.join(int_matches)}")

        # Personality trait match (max 15 pts)
        trait_matches = [t for t in traits if any(k in t for k in profile['traits'])]
        trait_score = min(len(trait_matches) * 5, 15)
        score += trait_score
        if trait_matches:
            reasons.append(f"Personality match: {', '.join(trait_matches)}")

        # Logical reasoning (max 15 pts)
        if reasoning >= profile['min_reasoning']:
            reasoning_score = min(int((reasoning - profile['min_reasoning']) / 4), 15)
            score += reasoning_score
            reasons.append(f"Logical reasoning score ({reasoning}) meets threshold ({profile['min_reasoning']})")

        results.append({
            'stream': stream,
            'score': min(score, 100),
            'description': profile['description'],
            'reasons': reasons,
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results
