"""
College / University Recommender — suggests institutions based on
course, location preference, budget, and entrance exam scores.
"""

from typing import Dict, List, Optional

COLLEGE_DATABASE: List[Dict] = [
    # Engineering / Technology
    {
        "name": "IIT Bombay",
        "type": "Government",
        "courses": ["B.Tech", "M.Tech", "B.Sc", "PhD"],
        "locations": ["Mumbai", "Maharashtra"],
        "fees_per_year": 250000,
        "entrance_exams": ["JEE Advanced"],
        "eligibility": "Top ~2500 JEE Advanced ranks",
        "ranking": 1,
        "tags": ["premier", "engineering", "research"],
        "website": "https://www.iitb.ac.in",
    },
    {
        "name": "IIT Delhi",
        "type": "Government",
        "courses": ["B.Tech", "M.Tech", "B.Sc", "PhD"],
        "locations": ["New Delhi", "Delhi"],
        "fees_per_year": 250000,
        "entrance_exams": ["JEE Advanced"],
        "eligibility": "Top ~2500 JEE Advanced ranks",
        "ranking": 2,
        "tags": ["premier", "engineering", "research"],
        "website": "https://home.iitd.ac.in",
    },
    {
        "name": "NIT Trichy",
        "type": "Government",
        "courses": ["B.Tech", "M.Tech"],
        "locations": ["Tiruchirappalli", "Tamil Nadu"],
        "fees_per_year": 150000,
        "entrance_exams": ["JEE Main"],
        "eligibility": "JEE Main top ranks; Category-wise cutoffs",
        "ranking": 8,
        "tags": ["engineering", "government", "nit"],
        "website": "https://www.nitt.edu",
    },
    {
        "name": "IIIT Hyderabad",
        "type": "Government-Aided",
        "courses": ["B.Tech", "M.Tech", "PhD"],
        "locations": ["Hyderabad", "Telangana"],
        "fees_per_year": 300000,
        "entrance_exams": ["JEE Main", "UGEE"],
        "eligibility": "JEE Main / UGEE exam",
        "ranking": 15,
        "tags": ["iiit", "computer science", "engineering", "ai"],
        "website": "https://www.iiit.ac.in",
    },
    # Medical
    {
        "name": "AIIMS New Delhi",
        "type": "Government",
        "courses": ["MBBS", "MD", "MS", "PhD"],
        "locations": ["New Delhi", "Delhi"],
        "fees_per_year": 5000,
        "entrance_exams": ["NEET-UG"],
        "eligibility": "NEET top ranks (All India Quota)",
        "ranking": 1,
        "tags": ["medical", "premier", "government"],
        "website": "https://www.aiims.edu",
    },
    {
        "name": "CMC Vellore",
        "type": "Private (Deemed)",
        "courses": ["MBBS", "Nursing", "Allied Health"],
        "locations": ["Vellore", "Tamil Nadu"],
        "fees_per_year": 50000,
        "entrance_exams": ["NEET-UG", "CMC Entrance"],
        "eligibility": "NEET rank + CMC entrance test",
        "ranking": 3,
        "tags": ["medical", "premier"],
        "website": "https://www.cmch-vellore.edu",
    },
    # Management
    {
        "name": "IIM Ahmedabad",
        "type": "Government",
        "courses": ["MBA", "Executive MBA", "PhD"],
        "locations": ["Ahmedabad", "Gujarat"],
        "fees_per_year": 1100000,
        "entrance_exams": ["CAT"],
        "eligibility": "CAT 99+ percentile + WAT/PI",
        "ranking": 1,
        "tags": ["mba", "management", "premier"],
        "website": "https://www.iima.ac.in",
    },
    # Law
    {
        "name": "National Law School, Bangalore",
        "type": "Government",
        "courses": ["Law (LLB)", "BA LLB", "LLM"],
        "locations": ["Bangalore", "Karnataka"],
        "fees_per_year": 250000,
        "entrance_exams": ["CLAT"],
        "eligibility": "CLAT top ranks",
        "ranking": 1,
        "tags": ["law", "premier", "nlu"],
        "website": "https://www.nls.ac.in",
    },
    # Bangalore Private Universities
    {
        "name": "REVA University",
        "type": "Private",
        "courses": ["B.Tech", "BCA", "MBA", "MCA", "B.Sc", "BBA", "Law (LLB)"],
        "locations": ["Bangalore", "Karnataka"],
        "fees_per_year": 280000,
        "entrance_exams": ["REVA CET", "JEE Main", "KCET"],
        "eligibility": "Min 45% in Class 12; REVA CET or JEE",
        "ranking": 45,
        "tags": ["private", "multidisciplinary", "bangalore"],
        "website": "https://www.reva.edu.in",
    },
    {
        "name": "Christ University",
        "type": "Deemed",
        "courses": ["BCA", "B.Sc", "BBA", "B.Com", "BA", "MBA", "MCA", "Law (LLB)"],
        "locations": ["Bangalore", "Karnataka"],
        "fees_per_year": 200000,
        "entrance_exams": ["CUET", "Christ University Entrance"],
        "eligibility": "Min 50% in Class 12 + Entrance + Interview",
        "ranking": 30,
        "tags": ["private", "multidisciplinary", "bangalore"],
        "website": "https://christuniversity.in",
    },
    {
        "name": "PES University",
        "type": "Deemed",
        "courses": ["B.Tech", "BCA", "MBA", "MCA"],
        "locations": ["Bangalore", "Karnataka"],
        "fees_per_year": 350000,
        "entrance_exams": ["PESSAT", "JEE Main", "KCET"],
        "eligibility": "Min 60% in PCM; PESSAT score",
        "ranking": 40,
        "tags": ["engineering", "private", "bangalore"],
        "website": "https://pes.edu",
    },
    # Design
    {
        "name": "National Institute of Design (NID), Ahmedabad",
        "type": "Government",
        "courses": ["Design", "M.Des"],
        "locations": ["Ahmedabad", "Gujarat"],
        "fees_per_year": 150000,
        "entrance_exams": ["NID DAT"],
        "eligibility": "12th pass + NID DAT + Studio Test",
        "ranking": 1,
        "tags": ["design", "premier", "government"],
        "website": "https://www.nid.edu",
    },
    {
        "name": "NIFT, New Delhi",
        "type": "Government",
        "courses": ["Design", "Fashion Design", "Textile Design"],
        "locations": ["New Delhi", "Delhi"],
        "fees_per_year": 200000,
        "entrance_exams": ["NIFT Entrance"],
        "eligibility": "12th pass + NIFT Entrance Test",
        "ranking": 1,
        "tags": ["design", "fashion", "premier"],
        "website": "https://www.nift.ac.in",
    },
]


def recommend_colleges(
    course: str,
    location_preference: Optional[str] = None,
    max_fees_per_year: Optional[float] = None,
    college_type: Optional[str] = None,
) -> Dict:
    """
    Return ranked college recommendations for a given course and filters.

    Args:
        course: Desired course (e.g., 'B.Tech', 'MBBS').
        location_preference: Preferred state or city (optional).
        max_fees_per_year: Maximum annual fee budget in INR (optional).
        college_type: 'Government', 'Private', 'Deemed', 'Government-Aided' (optional).

    Returns:
        dict with ranked list of matching colleges.
    """
    results: List[Dict] = []

    for college in COLLEGE_DATABASE:
        # Course filter
        if not any(course.lower() in c.lower() for c in college["courses"]):
            continue

        # Location filter
        if location_preference:
            loc_match = any(
                location_preference.lower() in loc.lower()
                for loc in college["locations"]
            )
            if not loc_match:
                continue

        # Fees filter
        if max_fees_per_year and college["fees_per_year"] > max_fees_per_year:
            continue

        # Type filter
        if college_type and college["type"].lower() != college_type.lower():
            continue

        results.append(college)

    # Sort by ranking (lower = better)
    results.sort(key=lambda c: c["ranking"])

    return {
        "course": course,
        "total_found": len(results),
        "colleges": results,
        "filters_applied": {
            "location": location_preference,
            "max_fees": max_fees_per_year,
            "type": college_type,
        },
    }
