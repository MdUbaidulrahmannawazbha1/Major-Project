"""
Central AI Engine for the Career Guidance System.

Provides career prediction, skill gap analysis, placement prediction,
job matching, roadmap generation, mentorship matching, and portfolio feedback.
"""

import os
import json
import logging
import numpy as np

try:
    import joblib
except ImportError:
    from sklearn.externals import joblib

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Directory & Model Loading
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = None
encoder = None
placement_model = None
placement_scaler = None

try:
    model = joblib.load(os.path.join(BASE_DIR, 'ai_model.pkl'))
    logger.info("Career prediction model loaded successfully.")
except Exception as e:
    logger.warning("Could not load ai_model.pkl: %s", e)

try:
    encoder = joblib.load(os.path.join(BASE_DIR, 'encoder.pkl'))
    logger.info("Feature encoder loaded successfully.")
except Exception as e:
    logger.warning("Could not load encoder.pkl: %s", e)

try:
    placement_model = joblib.load(os.path.join(BASE_DIR, 'placement_model.pkl'))
    logger.info("Placement model loaded successfully.")
except Exception as e:
    logger.warning("Could not load placement_model.pkl: %s", e)

try:
    placement_scaler = joblib.load(os.path.join(BASE_DIR, 'placement_scaler.pkl'))
    logger.info("Placement scaler loaded successfully.")
except Exception as e:
    logger.warning("Could not load placement_scaler.pkl: %s", e)

# ---------------------------------------------------------------------------
# Career Path Reference Data
# ---------------------------------------------------------------------------
CAREER_PATHS = {0: 'Technology', 1: 'Finance', 2: 'Healthcare'}

CAREER_SKILLS = {
    0: [
        'python', 'java', 'javascript', 'sql', 'git', 'docker', 'aws',
        'react', 'node', 'machine learning', 'data analysis', 'linux',
        'api design', 'cloud computing',
    ],
    1: [
        'excel', 'financial modeling', 'accounting', 'sql', 'python',
        'data analysis', 'risk management', 'statistics',
        'bloomberg terminal', 'communication', 'project management',
    ],
    2: [
        'biology', 'chemistry', 'patient care', 'communication',
        'research methodology', 'data analysis', 'medical terminology',
        'public health', 'empathy', 'critical thinking',
    ],
}

CAREER_CERTIFICATIONS = {
    0: [
        'AWS Solutions Architect',
        'Google Cloud Professional',
        'Microsoft Azure',
        'Certified Kubernetes Administrator',
        'CompTIA Security+',
    ],
    1: [
        'CFA Level I',
        'CPA',
        'FRM',
        'Bloomberg Market Concepts',
        'Financial Modeling & Valuation Analyst',
    ],
    2: [
        'BLS Certification',
        'ACLS Certification',
        'CNA',
        'Certified Clinical Research Professional',
        'Public Health Certificate',
    ],
}

CAREER_JOBS = {
    0: [
        {'title': 'Software Engineer',    'company': 'Tech Corp',       'description': 'Design and develop software applications and systems.'},
        {'title': 'Data Scientist',       'company': 'DataTech Inc',    'description': 'Analyze complex datasets and build predictive models.'},
        {'title': 'DevOps Engineer',      'company': 'CloudOps Ltd',    'description': 'Manage CI/CD pipelines and cloud infrastructure.'},
        {'title': 'Full Stack Developer', 'company': 'WebDev Co',       'description': 'Build end-to-end web applications with modern frameworks.'},
        {'title': 'ML Engineer',          'company': 'AI Solutions',    'description': 'Develop and deploy machine learning models at scale.'},
        {'title': 'Cloud Architect',      'company': 'CloudFirst Inc',  'description': 'Design scalable cloud infrastructure and migration strategies.'},
        {'title': 'Backend Developer',    'company': 'ServerSide LLC',  'description': 'Build robust server-side applications and APIs.'},
        {'title': 'Frontend Developer',   'company': 'PixelPerfect Co', 'description': 'Create responsive and accessible user interfaces.'},
    ],
    1: [
        {'title': 'Financial Analyst',    'company': 'Goldman Group',    'description': 'Analyze financial data and prepare investment reports.'},
        {'title': 'Investment Banker',    'company': 'Morgan Finance',   'description': 'Advise on mergers, acquisitions, and capital raising.'},
        {'title': 'Risk Analyst',         'company': 'RiskWise Corp',    'description': 'Assess and mitigate financial and operational risks.'},
        {'title': 'Portfolio Manager',    'company': 'Asset Management', 'description': 'Manage investment portfolios and asset allocation.'},
        {'title': 'Quantitative Analyst', 'company': 'QuantFin Ltd',     'description': 'Develop quantitative models for trading strategies.'},
        {'title': 'Compliance Officer',   'company': 'RegTech Inc',      'description': 'Ensure regulatory compliance across financial operations.'},
        {'title': 'Audit Associate',      'company': 'AuditPro LLC',     'description': 'Conduct financial audits and internal reviews.'},
        {'title': 'Tax Consultant',       'company': 'TaxAdvisors Co',   'description': 'Provide tax planning and compliance advisory services.'},
    ],
    2: [
        {'title': 'Clinical Research Associate', 'company': 'MedResearch Inc',  'description': 'Coordinate and monitor clinical trials.'},
        {'title': 'Healthcare Administrator',    'company': 'HealthSys Corp',   'description': 'Manage healthcare facility operations and staff.'},
        {'title': 'Public Health Analyst',       'company': 'CDC Partners',     'description': 'Analyze public health data and develop interventions.'},
        {'title': 'Medical Lab Technician',      'company': 'LabCorp',          'description': 'Perform diagnostic laboratory tests and analysis.'},
        {'title': 'Health Informatics Specialist','company': 'HealthIT Inc',    'description': 'Manage health information systems and data analytics.'},
        {'title': 'Patient Care Coordinator',    'company': 'CareBridge LLC',   'description': 'Coordinate patient care plans across providers.'},
        {'title': 'Biostatistician',             'company': 'BioStat Corp',     'description': 'Apply statistical methods to biological research.'},
        {'title': 'Epidemiologist',              'company': 'Global Health Co', 'description': 'Study disease patterns and develop prevention strategies.'},
    ],
}

CAREER_MILESTONES = {
    0: [
        'Learn Programming Fundamentals',
        'Build Portfolio Projects',
        'Complete Certifications',
        'Land Internship',
        'Junior Developer Role',
        'Senior Developer Role',
    ],
    1: [
        'Master Financial Fundamentals',
        'Build Financial Models',
        'Obtain Certifications',
        'Analyst Internship',
        'Junior Analyst',
        'Senior Analyst/Manager',
    ],
    2: [
        'Complete Pre-Clinical Education',
        'Clinical Rotations/Lab Work',
        'Professional Certifications',
        'Entry-Level Clinical Role',
        'Specialist Development',
        'Leadership/Research',
    ],
}

COURSE_SUGGESTIONS = {
    'python':               'Python for Everybody (Coursera)',
    'java':                 'Java Programming Masterclass (Udemy)',
    'javascript':           'The Complete JavaScript Course (Udemy)',
    'sql':                  'SQL for Data Science (Coursera)',
    'git':                  'Git & GitHub Bootcamp (Udemy)',
    'docker':               'Docker Mastery (Udemy)',
    'aws':                  'AWS Certified Cloud Practitioner (AWS Training)',
    'react':                'React – The Complete Guide (Udemy)',
    'node':                 'The Complete Node.js Developer Course (Udemy)',
    'machine learning':     'Machine Learning by Andrew Ng (Coursera)',
    'data analysis':        'Google Data Analytics Certificate (Coursera)',
    'linux':                'Linux Administration Bootcamp (Udemy)',
    'api design':           'RESTful API Design (Pluralsight)',
    'cloud computing':      'Cloud Computing Specialization (Coursera)',
    'excel':                'Excel Skills for Business (Coursera)',
    'financial modeling':   'Financial Modeling & Valuation (CFI)',
    'accounting':           'Introduction to Financial Accounting (Coursera)',
    'risk management':      'Financial Risk Management (edX)',
    'statistics':           'Statistics with Python (Coursera)',
    'bloomberg terminal':   'Bloomberg Market Concepts (Bloomberg)',
    'communication':        'Business Communication Skills (Coursera)',
    'project management':   'Google Project Management Certificate (Coursera)',
    'biology':              'Introduction to Biology (MIT OpenCourseWare)',
    'chemistry':            'General Chemistry (Coursera)',
    'patient care':         'Patient Care Technician Training (edX)',
    'research methodology': 'Research Methods (Coursera)',
    'medical terminology':  'Medical Terminology Course (Coursera)',
    'public health':        'Public Health Specialization (Coursera)',
    'empathy':              'Empathy and Emotional Intelligence at Work (edX)',
    'critical thinking':    'Critical Thinking & Problem Solving (Coursera)',
}

# ---------------------------------------------------------------------------
# Helper Utilities
# ---------------------------------------------------------------------------

def _safe_int(value, default=0):
    """Convert a value to int, returning *default* on failure."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_skills(skills):
    """Return a list of lowercased, stripped skill strings."""
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    return [s.lower().strip() for s in skills]

# ---------------------------------------------------------------------------
# 1. Career Prediction
# ---------------------------------------------------------------------------

def predict_career(assessment_responses: dict, cgpa: float = None, skills: str = '') -> dict:
    """Predict a career path from assessment responses and student profile.

    Returns
    -------
    dict
        career_id   – 0 (Technology), 1 (Finance), or 2 (Healthcare)
        career_name – human-readable label
        confidence  – 0.0 … 1.0
        scores      – per-domain raw scores
    """
    try:
        # Extract question responses as integers
        q = {f'q{i}': _safe_int(assessment_responses.get(f'q{i}'), 3) for i in range(1, 15)}

        tech_score     = q['q1'] + q['q2'] + q['q7'] + q['q12']
        finance_score  = q['q3'] + q['q4'] + q['q8'] + q['q14']
        health_score   = q['q5'] + q['q6'] + q['q13']

        scores = {
            'technology': tech_score,
            'finance':    finance_score,
            'healthcare': health_score,
        }

        # Determine heuristic prediction from domain scores
        domain_list = [tech_score, finance_score, health_score]
        heuristic_pred = int(np.argmax(domain_list))

        prediction = heuristic_pred

        # Attempt ML model prediction
        if model is not None:
            try:
                response_values = [q[f'q{i}'] for i in range(1, 15)]
                model_pred = int(model.predict([response_values])[0])
                if model_pred in CAREER_PATHS:
                    prediction = model_pred
            except Exception as e:
                logger.warning("ML model prediction failed, using heuristic: %s", e)

        # Confidence from domain scores
        total = max(sum(domain_list), 1)
        confidence = float(domain_list[prediction]) / total

        # Boost confidence with CGPA (up to 20 %)
        if cgpa is not None:
            try:
                cgpa_val = float(cgpa)
                cgpa_norm = min(cgpa_val / 10.0, 1.0)
                confidence = 0.8 * confidence + 0.2 * cgpa_norm
            except (TypeError, ValueError):
                pass

        confidence = round(min(max(confidence, 0.0), 1.0), 4)

        return {
            'career_id':   prediction,
            'career_name': CAREER_PATHS.get(prediction, 'Technology'),
            'confidence':  confidence,
            'scores':      scores,
        }

    except Exception as e:
        logger.error("predict_career error: %s", e)
        return {
            'career_id':   0,
            'career_name': 'Technology',
            'confidence':  0.0,
            'scores':      {'technology': 0, 'finance': 0, 'healthcare': 0},
        }

# ---------------------------------------------------------------------------
# 2. Skill Gap Analysis
# ---------------------------------------------------------------------------

def analyze_skill_gaps(user_skills: list, career_id: int) -> dict:
    """Identify missing skills and recommend courses for a career path.

    Returns
    -------
    dict
        missing_skills  – list of skill names the user lacks
        recommendations – list of dicts with skill / course pairs
        gap_score       – 0.0 (no gaps) … 1.0 (all missing)
    """
    try:
        required = CAREER_SKILLS.get(career_id, CAREER_SKILLS[0])
        normalized_user = set(_normalize_skills(user_skills))

        missing = [s for s in required if s not in normalized_user]

        recommendations = [
            {
                'skill': skill,
                'course': COURSE_SUGGESTIONS.get(skill, f'Search online courses for {skill}'),
            }
            for skill in missing
        ]

        gap_score = round(len(missing) / max(len(required), 1), 4)

        return {
            'missing_skills':  missing,
            'recommendations': recommendations,
            'gap_score':       gap_score,
        }

    except Exception as e:
        logger.error("analyze_skill_gaps error: %s", e)
        return {'missing_skills': [], 'recommendations': [], 'gap_score': 0.0}

# ---------------------------------------------------------------------------
# 3. Placement Prediction
# ---------------------------------------------------------------------------

def predict_placement(assessment_score: float, cgpa: float, skills_count: int) -> dict:
    """Predict the probability of placement.

    Returns
    -------
    dict
        probability – 0.0 … 1.0
        factors     – contribution breakdown
    """
    try:
        score_val  = float(assessment_score)
        cgpa_val   = float(cgpa)
        skills_val = int(skills_count)

        # Attempt model-based prediction
        if placement_model is not None and placement_scaler is not None:
            try:
                features = np.array([[score_val, cgpa_val / 10.0]])
                features_scaled = placement_scaler.transform(features)
                probability = float(placement_model.predict_proba(features_scaled)[0][1])

                return {
                    'probability': round(min(max(probability, 0.0), 1.0), 4),
                    'factors': {
                        'assessment_score': round(score_val, 2),
                        'cgpa':            round(cgpa_val, 2),
                        'skills_count':    skills_val,
                        'method':          'model',
                    },
                }
            except Exception as e:
                logger.warning("Placement model prediction failed, using heuristic: %s", e)

        # Heuristic fallback
        score_norm  = min(score_val / 100.0, 1.0)
        cgpa_norm   = min(cgpa_val / 10.0, 1.0)
        skills_norm = min(skills_val / 10.0, 1.0)

        probability = 0.4 * score_norm + 0.35 * cgpa_norm + 0.25 * skills_norm
        probability = round(min(max(probability, 0.0), 1.0), 4)

        return {
            'probability': probability,
            'factors': {
                'assessment_score': round(score_val, 2),
                'cgpa':            round(cgpa_val, 2),
                'skills_count':    skills_val,
                'method':          'heuristic',
            },
        }

    except Exception as e:
        logger.error("predict_placement error: %s", e)
        return {'probability': 0.0, 'factors': {}}

# ---------------------------------------------------------------------------
# 4. Job Matching
# ---------------------------------------------------------------------------

def match_jobs(career_id: int, user_skills: list) -> list:
    """Generate job recommendations ranked by skill overlap.

    Returns
    -------
    list[dict]
        Each dict contains title, company, required_skills, matching_score,
        and description.
    """
    try:
        jobs = CAREER_JOBS.get(career_id, CAREER_JOBS[0])
        required = CAREER_SKILLS.get(career_id, CAREER_SKILLS[0])
        normalized_user = set(_normalize_skills(user_skills))

        results = []
        for job in jobs:
            # Each job "requires" a subset of career skills – distribute evenly
            n_skills = max(len(required), 1)
            overlap  = len(normalized_user.intersection(set(required)))
            matching_score = round(overlap / n_skills, 4)

            results.append({
                'title':           job['title'],
                'company':         job['company'],
                'required_skills': ', '.join(required),
                'matching_score':  matching_score,
                'description':     job['description'],
            })

        results.sort(key=lambda x: x['matching_score'], reverse=True)
        return results

    except Exception as e:
        logger.error("match_jobs error: %s", e)
        return []

# ---------------------------------------------------------------------------
# 5. Roadmap Generation
# ---------------------------------------------------------------------------

def generate_roadmap(career_id: int, current_skills: list) -> dict:
    """Build a career roadmap with milestones, certifications, and timeline.

    Returns
    -------
    dict
        milestones      – ordered list of milestone strings
        certifications  – recommended certifications
        timeline_months – estimated months to reach senior level
    """
    try:
        milestones = CAREER_MILESTONES.get(career_id, CAREER_MILESTONES[0])
        certifications = CAREER_CERTIFICATIONS.get(career_id, CAREER_CERTIFICATIONS[0])
        required = CAREER_SKILLS.get(career_id, CAREER_SKILLS[0])

        normalized_user = set(_normalize_skills(current_skills))
        coverage = len(normalized_user.intersection(set(required))) / max(len(required), 1)

        # More skills covered → shorter timeline (base 24 months, min 6)
        timeline_months = max(int(24 * (1 - coverage * 0.5)), 6)

        return {
            'milestones':      milestones,
            'certifications':  certifications,
            'timeline_months': timeline_months,
        }

    except Exception as e:
        logger.error("generate_roadmap error: %s", e)
        return {'milestones': [], 'certifications': [], 'timeline_months': 24}

# ---------------------------------------------------------------------------
# 6. Mentorship Matching
# ---------------------------------------------------------------------------

def match_mentors(career_id: int, skill_gaps: list, mentors: list) -> list:
    """Score and rank mentors by relevance to the student's needs.

    Parameters
    ----------
    mentors : list[dict]
        Each dict should have at minimum 'user_id', 'expertise', and
        'availability'.  'expertise' can be a comma-separated string or a
        list of skill/domain keywords.

    Returns
    -------
    list[dict]
        Same mentor dicts with an added 'match_score' field, sorted
        descending.
    """
    try:
        career_name = CAREER_PATHS.get(career_id, 'Technology').lower()
        gap_set = set(_normalize_skills(skill_gaps))

        scored = []
        for mentor in mentors:
            expertise_raw = mentor.get('expertise', '')
            if isinstance(expertise_raw, list):
                expertise_tokens = set(_normalize_skills(expertise_raw))
            else:
                expertise_tokens = set(_normalize_skills(str(expertise_raw).split(',')))

            # Points for gap coverage (60 %) and career alignment (40 %)
            gap_overlap = len(expertise_tokens.intersection(gap_set))
            gap_component = gap_overlap / max(len(gap_set), 1)

            career_component = 1.0 if career_name in expertise_tokens else 0.0

            match_score = round(0.6 * gap_component + 0.4 * career_component, 4)

            mentor_copy = dict(mentor)
            mentor_copy['match_score'] = match_score
            scored.append(mentor_copy)

        scored.sort(key=lambda m: m['match_score'], reverse=True)
        return scored

    except Exception as e:
        logger.error("match_mentors error: %s", e)
        return []

# ---------------------------------------------------------------------------
# 7. Portfolio Feedback
# ---------------------------------------------------------------------------

def get_portfolio_feedback(portfolio_items: list, career_id: int, skill_gaps: list) -> dict:
    """Analyze portfolio items and suggest improvements.

    Parameters
    ----------
    portfolio_items : list[dict]
        Each item may contain 'title', 'description', 'skills_used', and
        'url'.

    Returns
    -------
    dict
        suggestions        – actionable improvement tips
        strength_areas     – skills demonstrated well
        improvement_areas  – areas that need work
    """
    try:
        required = CAREER_SKILLS.get(career_id, CAREER_SKILLS[0])
        gap_set = set(_normalize_skills(skill_gaps))

        demonstrated_skills: set = set()
        for item in portfolio_items:
            skills_used = item.get('skills_used', [])
            if isinstance(skills_used, str):
                skills_used = [s.strip() for s in skills_used.split(',') if s.strip()]
            demonstrated_skills.update(_normalize_skills(skills_used))

        strength_areas = [s for s in required if s in demonstrated_skills]
        improvement_areas = [s for s in required if s not in demonstrated_skills and s in gap_set]

        suggestions: list = []

        if not portfolio_items:
            suggestions.append('Start building portfolio projects to showcase your skills.')

        if improvement_areas:
            suggestions.append(
                f'Add projects demonstrating: {", ".join(improvement_areas[:5])}.'
            )

        career_name = CAREER_PATHS.get(career_id, 'Technology')
        if len(portfolio_items) < 3:
            suggestions.append(
                f'Aim for at least 3 portfolio projects relevant to {career_name}.'
            )

        has_description = all(item.get('description') for item in portfolio_items)
        if portfolio_items and not has_description:
            suggestions.append(
                'Add detailed descriptions to each portfolio item explaining '
                'your role and the technologies used.'
            )

        has_url = any(item.get('url') for item in portfolio_items)
        if portfolio_items and not has_url:
            suggestions.append(
                'Include live demo links or repository URLs for your projects.'
            )

        if not suggestions:
            suggestions.append(
                'Great portfolio! Consider adding case studies or metrics to '
                'demonstrate project impact.'
            )

        return {
            'suggestions':       suggestions,
            'strength_areas':    strength_areas,
            'improvement_areas': improvement_areas,
        }

    except Exception as e:
        logger.error("get_portfolio_feedback error: %s", e)
        return {'suggestions': [], 'strength_areas': [], 'improvement_areas': []}
