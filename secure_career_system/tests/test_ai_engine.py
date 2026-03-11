"""Tests for the central AI engine module."""
from secure_career_system import ai_engine


# ---------------------------------------------------------------------------
# Career Prediction
# ---------------------------------------------------------------------------
def test_predict_career_returns_required_keys():
    result = ai_engine.predict_career({'q1': '5', 'q2': '4', 'q3': '2', 'q4': '1'})
    assert 'career_id' in result
    assert 'career_name' in result
    assert 'confidence' in result
    assert 'scores' in result


def test_predict_career_tech_bias():
    # Strong tech answers should yield career_id 0 (Technology)
    responses = {f'q{i}': '3' for i in range(1, 16)}
    responses['q1'] = '5'
    responses['q2'] = '5'
    responses['q7'] = '5'
    responses['q12'] = '5'
    result = ai_engine.predict_career(responses)
    assert result['career_id'] == 0
    assert result['career_name'] == 'Technology'


def test_predict_career_finance_bias():
    responses = {f'q{i}': '1' for i in range(1, 16)}
    responses['q3'] = '5'
    responses['q4'] = '5'
    responses['q8'] = '5'
    responses['q14'] = '5'
    result = ai_engine.predict_career(responses)
    assert result['career_id'] == 1
    assert result['career_name'] == 'Finance'


def test_predict_career_healthcare_bias():
    responses = {f'q{i}': '1' for i in range(1, 16)}
    responses['q5'] = '5'
    responses['q6'] = '5'
    responses['q13'] = '5'
    result = ai_engine.predict_career(responses)
    assert result['career_id'] == 2
    assert result['career_name'] == 'Healthcare'


def test_predict_career_with_cgpa():
    responses = {f'q{i}': '3' for i in range(1, 16)}
    result = ai_engine.predict_career(responses, cgpa=9.0)
    assert 0 <= result['confidence'] <= 1.0


def test_predict_career_empty_responses():
    result = ai_engine.predict_career({})
    assert result['career_id'] in (0, 1, 2)
    assert result['confidence'] >= 0


# ---------------------------------------------------------------------------
# Skill Gap Analysis
# ---------------------------------------------------------------------------
def test_analyze_skill_gaps_no_skills():
    result = ai_engine.analyze_skill_gaps([], 0)
    assert len(result['missing_skills']) > 0
    assert result['gap_score'] > 0


def test_analyze_skill_gaps_full_coverage():
    all_skills = ai_engine.CAREER_SKILLS[0]
    result = ai_engine.analyze_skill_gaps(all_skills, 0)
    assert result['gap_score'] == 0.0
    assert result['missing_skills'] == []


def test_analyze_skill_gaps_partial():
    result = ai_engine.analyze_skill_gaps(['python', 'sql'], 0)
    assert 'python' not in result['missing_skills']
    assert 'sql' not in result['missing_skills']
    assert len(result['recommendations']) == len(result['missing_skills'])


def test_analyze_skill_gaps_recommendations_have_courses():
    result = ai_engine.analyze_skill_gaps([], 1)
    for rec in result['recommendations']:
        assert 'skill' in rec
        assert 'course' in rec


# ---------------------------------------------------------------------------
# Placement Prediction
# ---------------------------------------------------------------------------
def test_predict_placement_returns_probability():
    result = ai_engine.predict_placement(3.5, 8.0, 5)
    assert 'probability' in result
    assert 0 <= result['probability'] <= 1.0


def test_predict_placement_factors():
    result = ai_engine.predict_placement(4.0, 9.0, 10)
    assert 'factors' in result
    assert 'assessment_score' in result['factors']
    assert 'cgpa' in result['factors']


def test_predict_placement_zero_inputs():
    result = ai_engine.predict_placement(0, 0, 0)
    assert result['probability'] == 0.0


# ---------------------------------------------------------------------------
# Job Matching
# ---------------------------------------------------------------------------
def test_match_jobs_returns_list():
    jobs = ai_engine.match_jobs(0, ['python', 'git'])
    assert isinstance(jobs, list)
    assert len(jobs) > 0


def test_match_jobs_has_required_fields():
    jobs = ai_engine.match_jobs(1, ['excel'])
    for job in jobs:
        assert 'title' in job
        assert 'company' in job
        assert 'matching_score' in job


def test_match_jobs_sorted_by_score():
    jobs = ai_engine.match_jobs(0, ['python'])
    scores = [j['matching_score'] for j in jobs]
    assert scores == sorted(scores, reverse=True)


# ---------------------------------------------------------------------------
# Roadmap Generation
# ---------------------------------------------------------------------------
def test_generate_roadmap_returns_milestones():
    roadmap = ai_engine.generate_roadmap(0, [])
    assert 'milestones' in roadmap
    assert len(roadmap['milestones']) > 0


def test_generate_roadmap_certifications():
    roadmap = ai_engine.generate_roadmap(1, [])
    assert 'certifications' in roadmap
    assert len(roadmap['certifications']) > 0


def test_generate_roadmap_timeline():
    roadmap_low = ai_engine.generate_roadmap(0, [])
    roadmap_high = ai_engine.generate_roadmap(0, ai_engine.CAREER_SKILLS[0])
    # More skills should mean shorter or equal timeline
    assert roadmap_high['timeline_months'] <= roadmap_low['timeline_months']


# ---------------------------------------------------------------------------
# Mentorship Matching
# ---------------------------------------------------------------------------
def test_match_mentors_empty():
    result = ai_engine.match_mentors(0, ['python'], [])
    assert result == []


def test_match_mentors_scoring():
    mentors = [
        {'user_id': 1, 'expertise': 'python, java, technology', 'availability': 'available'},
        {'user_id': 2, 'expertise': 'accounting, excel', 'availability': 'available'},
    ]
    result = ai_engine.match_mentors(0, ['python', 'java'], mentors)
    assert len(result) == 2
    assert result[0]['match_score'] >= result[1]['match_score']
    assert result[0]['user_id'] == 1  # tech mentor should rank higher


# ---------------------------------------------------------------------------
# Portfolio Feedback
# ---------------------------------------------------------------------------
def test_portfolio_feedback_empty():
    result = ai_engine.get_portfolio_feedback([], 0, ['python'])
    assert 'suggestions' in result
    assert len(result['suggestions']) > 0


def test_portfolio_feedback_with_items():
    items = [
        {'title': 'Web App', 'description': 'Built a web app', 'skills_used': 'python, react', 'url': 'http://example.com'},
    ]
    result = ai_engine.get_portfolio_feedback(items, 0, ['docker', 'aws'])
    assert 'strength_areas' in result
    assert 'improvement_areas' in result
