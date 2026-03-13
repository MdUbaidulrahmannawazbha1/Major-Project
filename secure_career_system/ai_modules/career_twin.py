"""
Career Twin — predicts multiple possible career futures for a user
based on their assessment results, skills, interests, and education level.
"""

import math
from typing import Dict, List, Optional

# Skill affinity maps: career → required core skills
CAREER_SKILL_AFFINITY: Dict[str, List[str]] = {
    "Data Scientist": [
        "python", "machine learning", "statistics", "sql", "data analysis",
        "deep learning", "pandas", "numpy", "visualization",
    ],
    "Software Engineer": [
        "python", "java", "c++", "javascript", "data structures", "algorithms",
        "git", "sql", "system design", "testing",
    ],
    "AI Engineer": [
        "python", "tensorflow", "pytorch", "machine learning", "deep learning",
        "nlp", "computer vision", "mlops", "cloud",
    ],
    "Cybersecurity Analyst": [
        "network security", "ethical hacking", "penetration testing", "python",
        "siem", "incident response", "linux", "cryptography",
    ],
    "Financial Analyst": [
        "excel", "financial modelling", "accounting", "economics", "valuation",
        "python", "sql", "communication", "risk analysis",
    ],
    "Doctor": [
        "biology", "anatomy", "physiology", "pharmacology", "clinical skills",
        "patient care", "communication", "chemistry",
    ],
    "Lawyer": [
        "legal reasoning", "research", "communication", "drafting",
        "negotiation", "critical thinking", "political science",
    ],
    "UX Designer": [
        "figma", "user research", "wireframing", "prototyping",
        "design thinking", "adobe xd", "html", "css",
    ],
    "Research Scientist": [
        "research methodology", "academic writing", "statistics", "python",
        "matlab", "r", "data analysis", "domain expertise",
    ],
    "Civil Servant (IAS)": [
        "general studies", "current affairs", "essay writing", "leadership",
        "decision making", "history", "polity", "economics",
    ],
    "Business Analyst": [
        "sql", "excel", "communication", "requirements gathering",
        "process mapping", "python", "power bi", "stakeholder management",
    ],
    "Cloud Engineer": [
        "aws", "azure", "gcp", "docker", "kubernetes", "linux",
        "networking", "terraform", "python",
    ],
    "Product Manager": [
        "product thinking", "user research", "data analysis", "communication",
        "roadmapping", "agile", "stakeholder management", "sql",
    ],
    "Digital Marketer": [
        "seo", "social media", "content creation", "google analytics",
        "ppc advertising", "email marketing", "communication",
    ],
    "Biotech Researcher": [
        "biology", "chemistry", "research methodology", "pcr",
        "data analysis", "lab skills", "bioinformatics",
    ],
}

# Interest-to-career boosters
INTEREST_CAREER_BOOST: Dict[str, List[str]] = {
    "technology": ["Software Engineer", "AI Engineer", "Cloud Engineer", "Cybersecurity Analyst"],
    "data": ["Data Scientist", "Business Analyst", "Research Scientist"],
    "medicine": ["Doctor", "Biotech Researcher"],
    "finance": ["Financial Analyst", "Business Analyst"],
    "law": ["Lawyer", "Civil Servant (IAS)"],
    "design": ["UX Designer", "Digital Marketer"],
    "research": ["Research Scientist", "AI Engineer", "Biotech Researcher"],
    "management": ["Product Manager", "Business Analyst", "Civil Servant (IAS)"],
    "government": ["Civil Servant (IAS)"],
    "marketing": ["Digital Marketer", "Product Manager"],
}

# Education level multipliers: ensures appropriate careers surface for each level
EDUCATION_CAREER_MULTIPLIER: Dict[str, Dict[str, float]] = {
    "School": {
        "Software Engineer": 0.6,
        "Data Scientist": 0.5,
        "AI Engineer": 0.5,
        "Doctor": 0.7,
        "Lawyer": 0.6,
    },
    "PUC": {
        "Software Engineer": 0.75,
        "Data Scientist": 0.65,
        "Doctor": 0.8,
    },
    "Undergraduate": {
        "Software Engineer": 1.0,
        "Data Scientist": 0.9,
        "AI Engineer": 0.9,
        "Doctor": 0.95,
    },
    "Postgraduate": {
        "Research Scientist": 1.2,
        "AI Engineer": 1.1,
        "Data Scientist": 1.1,
    },
    "PhD": {
        "Research Scientist": 1.5,
        "AI Engineer": 1.2,
        "Biotech Researcher": 1.4,
    },
    "Professional": {
        "Product Manager": 1.2,
        "Business Analyst": 1.2,
        "Financial Analyst": 1.1,
    },
}


def predict_career_twins(
    skills: List[str],
    interests: List[str],
    education_level: str,
    assessment_responses: Optional[Dict] = None,
    top_n: int = 5,
) -> Dict:
    """
    Predict multiple possible career futures with probability scores.

    Args:
        skills: List of skills the user has.
        interests: List of interest keywords.
        education_level: Current education level.
        assessment_responses: Optional dict from career assessment.
        top_n: Number of top predictions to return.

    Returns:
        dict with ranked career predictions and confidence percentages.
    """
    skills_lower = {s.lower() for s in skills}
    interests_lower = [i.lower() for i in interests]

    raw_scores: Dict[str, float] = {}

    # 1. Skill affinity scoring (0–100 based on % skills matched)
    for career, required_skills in CAREER_SKILL_AFFINITY.items():
        matched = sum(1 for rs in required_skills if any(rs in s for s in skills_lower))
        skill_ratio = matched / max(len(required_skills), 1)
        raw_scores[career] = skill_ratio * 60.0  # 60% weight from skills

    # 2. Interest boosting (up to 25 points)
    for interest_kw in interests_lower:
        for interest_key, careers in INTEREST_CAREER_BOOST.items():
            if interest_key in interest_kw:
                for career in careers:
                    if career in raw_scores:
                        raw_scores[career] += 25.0 / max(len(interests_lower), 1)

    # 3. Education level multipliers
    edu_multipliers = EDUCATION_CAREER_MULTIPLIER.get(education_level, {})
    for career, multiplier in edu_multipliers.items():
        if career in raw_scores:
            raw_scores[career] *= multiplier

    # 4. Assessment domain score boosting (up to 15 points)
    if assessment_responses:
        domain_scores = assessment_responses.get("domain_scores", {})
        tech_score = domain_scores.get("technology", 0)
        fin_score = domain_scores.get("finance", 0)
        health_score = domain_scores.get("healthcare", 0)

        for career in ["Software Engineer", "AI Engineer", "Data Scientist", "Cloud Engineer", "Cybersecurity Analyst"]:
            if career in raw_scores:
                raw_scores[career] += tech_score * 0.15

        for career in ["Financial Analyst", "Business Analyst"]:
            if career in raw_scores:
                raw_scores[career] += fin_score * 0.15

        for career in ["Doctor", "Biotech Researcher"]:
            if career in raw_scores:
                raw_scores[career] += health_score * 0.15

    # 5. Normalize to 0–100 scale using sigmoid-like transformation
    max_score = max(raw_scores.values()) if raw_scores else 1.0
    normalized: Dict[str, float] = {}
    for career, score in raw_scores.items():
        normalized_val = (score / max_score) * 100 if max_score > 0 else 0
        # Sigmoid smoothing to avoid perfect 100%
        smoothed = 100 / (1 + math.exp(-0.05 * (normalized_val - 50)))
        normalized[career] = round(smoothed, 1)

    # Sort and get top N
    ranked = sorted(normalized.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Build rich output
    predictions = []
    for rank, (career, confidence) in enumerate(ranked, 1):
        required = CAREER_SKILL_AFFINITY.get(career, [])
        matched_skills = [rs for rs in required if any(rs in s for s in skills_lower)]
        missing_skills = [rs for rs in required if not any(rs in s for s in skills_lower)]

        predictions.append({
            "rank": rank,
            "career": career,
            "confidence": confidence,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills[:3],
            "fit_label": _confidence_label(confidence),
        })

    return {
        "education_level": education_level,
        "skills_analysed": len(skills),
        "interests_analysed": len(interests),
        "predictions": predictions,
        "primary_career": ranked[0][0] if ranked else "Undetermined",
        "message": f"Based on your profile, your top career match is {ranked[0][0]} with {ranked[0][1]}% fit." if ranked else "Insufficient data for prediction.",
    }


def _confidence_label(confidence: float) -> str:
    if confidence >= 75:
        return "Excellent Fit"
    if confidence >= 55:
        return "Strong Fit"
    if confidence >= 40:
        return "Good Fit"
    if confidence >= 25:
        return "Potential Fit"
    return "Aspiring"
