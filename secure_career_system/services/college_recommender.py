"""
College / University Recommender — suggests colleges based on course, location,
fees, entrance exams, and eligibility.
"""

COLLEGE_DATABASE = [
    # Engineering – Top Tier
    {
        'name': 'IIT Bombay',
        'courses': ['B.Tech (Computer Science)', 'B.Tech (Electronics)', 'B.Sc (Physics/Chemistry/Biology)'],
        'location': 'Mumbai, Maharashtra',
        'fees': '₹2-3 LPA',
        'entrance_exams': ['JEE Advanced'],
        'eligibility': '75% in 12th (PCM), JEE Advanced rank',
        'tier': 'Tier 1',
        'type': 'Government',
    },
    {
        'name': 'IIT Delhi',
        'courses': ['B.Tech (Computer Science)', 'B.Tech (Electronics)'],
        'location': 'New Delhi',
        'fees': '₹2-3 LPA',
        'entrance_exams': ['JEE Advanced'],
        'eligibility': '75% in 12th (PCM), JEE Advanced rank',
        'tier': 'Tier 1',
        'type': 'Government',
    },
    {
        'name': 'NIT Karnataka (Surathkal)',
        'courses': ['B.Tech (Computer Science)', 'B.Tech (Electronics)'],
        'location': 'Surathkal, Karnataka',
        'fees': '₹1.5-2.5 LPA',
        'entrance_exams': ['JEE Main'],
        'eligibility': '75% in 12th (PCM), JEE Main rank',
        'tier': 'Tier 1',
        'type': 'Government',
    },
    {
        'name': 'NIT Trichy',
        'courses': ['B.Tech (Computer Science)', 'B.Tech (Electronics)'],
        'location': 'Tiruchirappalli, Tamil Nadu',
        'fees': '₹1.5-2.5 LPA',
        'entrance_exams': ['JEE Main'],
        'eligibility': '75% in 12th (PCM), JEE Main rank',
        'tier': 'Tier 1',
        'type': 'Government',
    },
    {
        'name': 'IIIT Hyderabad',
        'courses': ['B.Tech (Computer Science)', 'BCA'],
        'location': 'Hyderabad, Telangana',
        'fees': '₹2-3.5 LPA',
        'entrance_exams': ['JEE Main', 'IIIT Entrance'],
        'eligibility': '75% in 12th (PCM)',
        'tier': 'Tier 1',
        'type': 'Government',
    },
    # Private Universities
    {
        'name': 'REVA University',
        'courses': ['B.Tech (Computer Science)', 'B.Tech (Electronics)', 'BCA', 'BBA',
                    'B.Com', 'B.Des (Design)', 'B.Sc Animation & Multimedia'],
        'location': 'Bangalore, Karnataka',
        'fees': '₹2-5 LPA',
        'entrance_exams': ['KCET', 'University Entrance Test'],
        'eligibility': '50% in 12th',
        'tier': 'Tier 2',
        'type': 'Private',
    },
    {
        'name': 'Christ University',
        'courses': ['BCA', 'BBA', 'B.Com', 'BA LLB (Law)', 'B.Sc (Computer Science)',
                    'B.Sc (Physics/Chemistry/Biology)'],
        'location': 'Bangalore, Karnataka',
        'fees': '₹1.5-4 LPA',
        'entrance_exams': ['Christ University Entrance Test'],
        'eligibility': '50% in 12th',
        'tier': 'Tier 2',
        'type': 'Private',
    },
    {
        'name': 'VIT Vellore',
        'courses': ['B.Tech (Computer Science)', 'B.Tech (Electronics)'],
        'location': 'Vellore, Tamil Nadu',
        'fees': '₹3-5 LPA',
        'entrance_exams': ['VITEEE'],
        'eligibility': '60% in 12th (PCM)',
        'tier': 'Tier 2',
        'type': 'Private',
    },
    # Medical
    {
        'name': 'AIIMS Delhi',
        'courses': ['MBBS'],
        'location': 'New Delhi',
        'fees': '₹0.1-0.5 LPA',
        'entrance_exams': ['NEET UG'],
        'eligibility': '60% in 12th (PCB), NEET rank',
        'tier': 'Tier 1',
        'type': 'Government',
    },
    # Law
    {
        'name': 'NLSIU Bangalore',
        'courses': ['BA LLB (Law)'],
        'location': 'Bangalore, Karnataka',
        'fees': '₹2-3 LPA',
        'entrance_exams': ['CLAT'],
        'eligibility': '50% in 12th, CLAT rank',
        'tier': 'Tier 1',
        'type': 'Government',
    },
    # Design
    {
        'name': 'NID Ahmedabad',
        'courses': ['B.Des (Design)'],
        'location': 'Ahmedabad, Gujarat',
        'fees': '₹3-4 LPA',
        'entrance_exams': ['NID DAT'],
        'eligibility': '50% in 12th',
        'tier': 'Tier 1',
        'type': 'Government',
    },
    # Arts / Civil Services
    {
        'name': 'Delhi University',
        'courses': ['BA (Civil Services Preparation)', 'B.Com', 'B.Sc (Computer Science)',
                    'B.Sc (Physics/Chemistry/Biology)'],
        'location': 'New Delhi',
        'fees': '₹0.1-0.5 LPA',
        'entrance_exams': ['CUET'],
        'eligibility': '60% in 12th',
        'tier': 'Tier 1',
        'type': 'Government',
    },
]


def recommend_colleges(course=None, location=None, max_fees=None, college_type=None):
    """Return colleges matching the given filters.

    Each item includes: name, courses, location, fees, entrance_exams, eligibility, tier, type
    """
    results = []

    for college in COLLEGE_DATABASE:
        score = 0
        reasons = []

        # Course match
        if course:
            matching_courses = [c for c in college['courses']
                                if course.lower() in c.lower() or c.lower() in course.lower()]
            if matching_courses:
                score += 40
                reasons.append(f"Offers: {', '.join(matching_courses)}")
            else:
                continue  # Skip colleges that don't offer the requested course

        # Location preference
        if location and location.lower() in college['location'].lower():
            score += 20
            reasons.append(f"Located in preferred area: {college['location']}")

        # Type preference
        if college_type and college_type.lower() == college['type'].lower():
            score += 15
            reasons.append(f"College type: {college['type']}")

        # Tier bonus
        tier_scores = {'Tier 1': 25, 'Tier 2': 15}
        score += tier_scores.get(college['tier'], 5)

        results.append({
            'name': college['name'],
            'course': course or ', '.join(college['courses'][:3]),
            'location': college['location'],
            'fees': college['fees'],
            'entrance_exams': college['entrance_exams'],
            'eligibility': college['eligibility'],
            'tier': college['tier'],
            'type': college['type'],
            'score': score,
            'reasons': reasons,
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results
