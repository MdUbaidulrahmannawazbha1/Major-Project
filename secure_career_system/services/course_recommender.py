"""
Course Recommender — recommends courses/degrees for Class 12 students.

Uses assessment results, skills, interests, and marks to suggest suitable courses.
"""

COURSE_DATABASE = [
    {
        'course': 'B.Tech (Computer Science)',
        'streams': ['Science'],
        'subjects': ['mathematics', 'physics', 'computer', 'science'],
        'interests': ['technology', 'programming', 'engineering', 'software', 'ai', 'robotics'],
        'min_marks': 60,
        'career_paths': ['Software Engineer', 'Data Scientist', 'AI Engineer', 'DevOps'],
        'duration': '4 years',
    },
    {
        'course': 'B.Tech (Electronics)',
        'streams': ['Science'],
        'subjects': ['mathematics', 'physics', 'electronics'],
        'interests': ['electronics', 'circuits', 'hardware', 'iot', 'embedded'],
        'min_marks': 60,
        'career_paths': ['Electronics Engineer', 'VLSI Designer', 'IoT Developer'],
        'duration': '4 years',
    },
    {
        'course': 'BCA',
        'streams': ['Science', 'Commerce'],
        'subjects': ['mathematics', 'computer', 'science'],
        'interests': ['programming', 'software', 'web development', 'technology'],
        'min_marks': 50,
        'career_paths': ['Software Developer', 'Web Developer', 'System Administrator'],
        'duration': '3 years',
    },
    {
        'course': 'B.Sc (Computer Science)',
        'streams': ['Science'],
        'subjects': ['mathematics', 'computer', 'science', 'physics'],
        'interests': ['research', 'programming', 'data', 'science'],
        'min_marks': 50,
        'career_paths': ['Data Analyst', 'Researcher', 'Software Developer'],
        'duration': '3 years',
    },
    {
        'course': 'B.Sc (Physics/Chemistry/Biology)',
        'streams': ['Science'],
        'subjects': ['physics', 'chemistry', 'biology', 'science'],
        'interests': ['research', 'lab', 'experiments', 'science'],
        'min_marks': 50,
        'career_paths': ['Research Scientist', 'Lab Technician', 'Science Educator'],
        'duration': '3 years',
    },
    {
        'course': 'MBBS',
        'streams': ['Science'],
        'subjects': ['biology', 'chemistry', 'physics'],
        'interests': ['medicine', 'healthcare', 'doctor', 'hospital', 'surgery'],
        'min_marks': 80,
        'career_paths': ['Doctor', 'Surgeon', 'Medical Researcher'],
        'duration': '5.5 years',
    },
    {
        'course': 'BBA',
        'streams': ['Commerce', 'Arts'],
        'subjects': ['business', 'economics', 'commerce', 'management'],
        'interests': ['business', 'management', 'entrepreneurship', 'marketing', 'leadership'],
        'min_marks': 45,
        'career_paths': ['Business Analyst', 'Manager', 'Entrepreneur'],
        'duration': '3 years',
    },
    {
        'course': 'B.Com',
        'streams': ['Commerce'],
        'subjects': ['accounting', 'economics', 'commerce', 'mathematics'],
        'interests': ['finance', 'accounting', 'banking', 'taxation'],
        'min_marks': 45,
        'career_paths': ['Accountant', 'Financial Analyst', 'Auditor'],
        'duration': '3 years',
    },
    {
        'course': 'BA LLB (Law)',
        'streams': ['Arts', 'Commerce'],
        'subjects': ['political science', 'history', 'english', 'law'],
        'interests': ['law', 'justice', 'politics', 'debate', 'legal'],
        'min_marks': 55,
        'career_paths': ['Lawyer', 'Judge', 'Legal Advisor'],
        'duration': '5 years',
    },
    {
        'course': 'B.Des (Design)',
        'streams': ['Arts', 'Science'],
        'subjects': ['arts', 'drawing', 'design', 'english'],
        'interests': ['design', 'creative', 'ux', 'ui', 'graphic', 'fashion', 'architecture'],
        'min_marks': 50,
        'career_paths': ['UX Designer', 'Graphic Designer', 'Fashion Designer'],
        'duration': '4 years',
    },
    {
        'course': 'B.Sc Animation & Multimedia',
        'streams': ['Arts', 'Science'],
        'subjects': ['arts', 'computer', 'drawing'],
        'interests': ['animation', 'vfx', 'gaming', 'multimedia', 'creative', 'film'],
        'min_marks': 45,
        'career_paths': ['Animator', 'VFX Artist', 'Game Designer'],
        'duration': '3 years',
    },
    {
        'course': 'BA (Civil Services Preparation)',
        'streams': ['Arts'],
        'subjects': ['history', 'geography', 'political science', 'sociology'],
        'interests': ['civil services', 'upsc', 'government', 'politics', 'public service'],
        'min_marks': 50,
        'career_paths': ['IAS Officer', 'IPS Officer', 'Civil Servant'],
        'duration': '3 years',
    },
]


def _normalize(items):
    if not items:
        return []
    if isinstance(items, str):
        items = [s.strip() for s in items.split(',')]
    return [s.lower().strip() for s in items if s and s.strip()]


def recommend_courses(stream=None, subjects=None, interests=None,
                      marks=None, skills=None, assessment_result=None):
    """Return ranked list of course recommendations.

    Each item: {course, score, duration, career_paths, reasons}
    """
    subj_list = _normalize(subjects)
    int_list = _normalize(interests)
    skill_list = _normalize(skills)
    combined_interests = int_list + skill_list
    marks_val = marks if marks is not None else 60  # default: assume average marks

    results = []
    for entry in COURSE_DATABASE:
        score = 0
        reasons = []

        # Stream match (25 pts)
        if stream and stream in entry['streams']:
            score += 25
            reasons.append(f"Matches your stream: {stream}")
        elif not stream:
            score += 10  # neutral if no stream given

        # Subject overlap (max 30 pts)
        subj_matches = [s for s in subj_list if any(k in s for k in entry['subjects'])]
        subj_score = min(len(subj_matches) * 10, 30)
        score += subj_score
        if subj_matches:
            reasons.append(f"Subject match: {', '.join(subj_matches)}")

        # Interest/skill overlap (max 30 pts)
        int_matches = [i for i in combined_interests if any(k in i for k in entry['interests'])]
        int_score = min(len(int_matches) * 8, 30)
        score += int_score
        if int_matches:
            reasons.append(f"Interest/skill match: {', '.join(int_matches)}")

        # Marks eligibility (max 15 pts)
        if marks_val >= entry['min_marks']:
            marks_score = min(int((marks_val - entry['min_marks']) / 3), 15)
            score += marks_score
            reasons.append(f"Marks ({marks_val}%) meet minimum ({entry['min_marks']}%)")
        else:
            score -= 10
            reasons.append(f"Marks ({marks_val}%) below minimum ({entry['min_marks']}%)")

        results.append({
            'course': entry['course'],
            'score': max(min(score, 100), 0),
            'duration': entry['duration'],
            'career_paths': entry['career_paths'],
            'reasons': reasons,
        })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results
