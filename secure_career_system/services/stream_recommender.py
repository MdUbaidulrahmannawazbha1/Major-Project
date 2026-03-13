"""
Stream Recommender — suggests Science / Commerce / Arts / Diploma
for students who have completed Class 10.
"""

from typing import Dict, List

# Subjects associated with each stream
STREAM_SUBJECT_WEIGHTS: Dict[str, List[str]] = {
    "Science": [
        "mathematics", "physics", "chemistry", "biology", "science",
        "computer", "coding", "programming", "technology"
    ],
    "Commerce": [
        "accountancy", "economics", "business", "commerce", "finance",
        "marketing", "statistics", "maths", "entrepreneurship"
    ],
    "Arts": [
        "history", "geography", "civics", "literature", "language",
        "art", "music", "psychology", "sociology", "political science",
        "philosophy", "drama", "design"
    ],
    "Diploma": [
        "technical", "mechanical", "electrical", "civil", "electronics",
        "vocational", "iti", "polytechnic", "automobile", "manufacturing"
    ],
}

# Career interests mapped to streams
INTEREST_STREAM_MAP: Dict[str, str] = {
    "doctor": "Science",
    "engineer": "Science",
    "scientist": "Science",
    "ai": "Science",
    "data": "Science",
    "programming": "Science",
    "research": "Science",
    "pharma": "Science",
    "nurse": "Science",
    "ca": "Commerce",
    "chartered accountant": "Commerce",
    "banker": "Commerce",
    "finance": "Commerce",
    "business": "Commerce",
    "entrepreneur": "Commerce",
    "marketing": "Commerce",
    "lawyer": "Arts",
    "journalist": "Arts",
    "writer": "Arts",
    "designer": "Arts",
    "teacher": "Arts",
    "psychologist": "Arts",
    "artist": "Arts",
    "actor": "Arts",
    "musician": "Arts",
    "social worker": "Arts",
    "technician": "Diploma",
    "mechanic": "Diploma",
    "electrician": "Diploma",
    "operator": "Diploma",
}

# Personality traits that align with each stream
PERSONALITY_STREAM_MAP: Dict[str, str] = {
    "analytical": "Science",
    "logical": "Science",
    "mathematical": "Science",
    "problem-solving": "Science",
    "innovative": "Science",
    "entrepreneurial": "Commerce",
    "organized": "Commerce",
    "detail-oriented": "Commerce",
    "leadership": "Commerce",
    "communicative": "Arts",
    "creative": "Arts",
    "empathetic": "Arts",
    "expressive": "Arts",
    "practical": "Diploma",
    "hands-on": "Diploma",
    "technical": "Diploma",
}

STREAM_DESCRIPTIONS = {
    "Science": {
        "description": "Science stream opens paths to engineering, medicine, research, and technology careers.",
        "courses": ["Physics", "Chemistry", "Mathematics", "Biology", "Computer Science"],
        "careers": ["Engineer", "Doctor", "Scientist", "Data Analyst", "AI Engineer", "Pharmacist"],
        "next_steps": ["JEE / NEET preparation", "B.Tech / MBBS / B.Sc programs"],
    },
    "Commerce": {
        "description": "Commerce stream leads to finance, business, accounting, and management careers.",
        "courses": ["Accountancy", "Business Studies", "Economics", "Mathematics"],
        "careers": ["CA", "Banker", "Financial Analyst", "Entrepreneur", "Marketing Manager"],
        "next_steps": ["CA Foundation", "BBA / B.Com programs", "Economics honours"],
    },
    "Arts": {
        "description": "Arts stream nurtures creativity, communication, and social awareness for diverse careers.",
        "courses": ["History", "Political Science", "Psychology", "Literature", "Fine Arts"],
        "careers": ["Lawyer", "Journalist", "Psychologist", "Designer", "Civil Servant", "Actor"],
        "next_steps": ["BA / LLB programs", "CLAT preparation", "Design colleges", "UPSC foundation"],
    },
    "Diploma": {
        "description": "Diploma programs provide practical technical skills for immediate employment.",
        "courses": ["Mechanical", "Electrical", "Civil", "Electronics", "Computer Technology"],
        "careers": ["Technician", "Field Engineer", "IT Support", "Manufacturing Operator"],
        "next_steps": ["Polytechnic enrollment", "ITI programs", "Lateral entry to B.Tech"],
    },
}


def recommend_stream(
    favorite_subjects: List[str],
    interests: List[str],
    logical_reasoning_score: float,
    personality_traits: List[str],
) -> Dict:
    """
    Recommend a stream for Class 10 students.

    Args:
        favorite_subjects: List of subjects the student likes most.
        interests: List of career interest keywords.
        logical_reasoning_score: Score 0–10 on logical reasoning.
        personality_traits: List of personality descriptors.

    Returns:
        dict with recommended stream, confidence score, and all stream scores.
    """
    scores: Dict[str, float] = {s: 0.0 for s in STREAM_DESCRIPTIONS}

    # 1. Subject matching (weight 40%)
    for subject in favorite_subjects:
        subject_lower = subject.lower()
        for stream, keywords in STREAM_SUBJECT_WEIGHTS.items():
            if any(kw in subject_lower for kw in keywords):
                scores[stream] += 40.0

    # Normalize subject score across subjects (total_subjects is always >= 1)
    total_subjects = max(len(favorite_subjects), 1)
    for s in scores:
        scores[s] = scores[s] / total_subjects

    # 2. Interest matching (weight 30%)
    for interest in interests:
        interest_lower = interest.lower()
        for keyword, stream in INTEREST_STREAM_MAP.items():
            if keyword in interest_lower:
                scores[stream] += 30.0 / max(len(interests), 1)
                break

    # 3. Logical reasoning bias (weight 15%)
    # High logical score → Science bonus; low → Arts bonus
    normalized_logic = max(0.0, min(10.0, logical_reasoning_score)) / 10.0
    scores["Science"] += normalized_logic * 15.0
    scores["Arts"] += (1.0 - normalized_logic) * 7.5
    scores["Commerce"] += (1.0 - normalized_logic) * 7.5

    # 4. Personality traits (weight 15%)
    for trait in personality_traits:
        trait_lower = trait.lower()
        for keyword, stream in PERSONALITY_STREAM_MAP.items():
            if keyword in trait_lower:
                scores[stream] += 15.0 / max(len(personality_traits), 1)
                break

    # Determine recommendation
    recommended = max(scores, key=lambda s: scores[s])
    total_score = sum(scores.values()) or 1.0
    confidence = round(scores[recommended] / total_score * 100, 1)

    # Build ranked alternatives
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return {
        "recommended_stream": recommended,
        "confidence": confidence,
        "stream_scores": {s: round(v, 2) for s, v in ranked},
        "stream_info": STREAM_DESCRIPTIONS[recommended],
        "all_streams": {
            s: STREAM_DESCRIPTIONS[s] for s in STREAM_DESCRIPTIONS
        },
    }
