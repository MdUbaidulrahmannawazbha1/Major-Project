"""Tests for the universal AI career navigation platform modules."""
import json
import pytest

from secure_career_system.services.stream_recommender import recommend_streams
from secure_career_system.services.course_recommender import recommend_courses
from secure_career_system.services.college_recommender import recommend_colleges
from secure_career_system.services.exam_guidance import get_exam_guidance, list_all_categories
from secure_career_system.services.learning_engine import generate_learning_roadmap
from secure_career_system.services.career_map import get_career_map, list_all_careers
from secure_career_system.ai_modules.career_simulator import simulate_career
from secure_career_system.ai_modules.career_twin import predict_career_twins
from secure_career_system.ai_modules.market_analysis import get_skill_demand, get_top_skills
from secure_career_system.resume_analyzer import (
    analyze_skill_gaps_by_stage,
    generate_resume_draft,
    generate_linkedin_suggestions,
    generate_portfolio_recommendations,
)


# ---- Feature 1: Stream Recommender ----

class TestStreamRecommender:
    def test_returns_list(self):
        result = recommend_streams()
        assert isinstance(result, list)
        assert len(result) == 4  # Science, Commerce, Arts, Diploma

    def test_science_top_for_math_physics(self):
        result = recommend_streams(
            favorite_subjects=['mathematics', 'physics'],
            interests=['technology', 'engineering'],
            logical_reasoning_score=80,
            personality_traits=['analytical', 'curious'],
        )
        assert result[0]['stream'] == 'Science'

    def test_commerce_for_business_interests(self):
        result = recommend_streams(
            favorite_subjects=['economics', 'business'],
            interests=['finance', 'entrepreneurship'],
        )
        assert any(r['stream'] == 'Commerce' and r['score'] > 0 for r in result)

    def test_each_item_has_required_keys(self):
        result = recommend_streams(favorite_subjects=['history'])
        for item in result:
            assert 'stream' in item
            assert 'score' in item
            assert 'description' in item
            assert 'reasons' in item


# ---- Feature 2: Course Recommender ----

class TestCourseRecommender:
    def test_returns_list(self):
        result = recommend_courses()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_btech_for_science_stream(self):
        result = recommend_courses(
            stream='Science',
            subjects=['mathematics', 'physics'],
            interests=['programming', 'technology'],
            marks=80,
        )
        top_courses = [r['course'] for r in result[:3]]
        assert any('B.Tech' in c for c in top_courses)

    def test_each_item_has_required_keys(self):
        result = recommend_courses()
        for item in result:
            assert 'course' in item
            assert 'score' in item
            assert 'career_paths' in item


# ---- Feature 3: College Recommender ----

class TestCollegeRecommender:
    def test_returns_list(self):
        result = recommend_colleges(course='B.Tech')
        assert isinstance(result, list)
        assert len(result) > 0

    def test_filters_by_course(self):
        result = recommend_colleges(course='MBBS')
        for r in result:
            assert 'MBBS' in r.get('course', '') or 'MBBS' in str(r.get('name', ''))

    def test_each_item_has_required_keys(self):
        result = recommend_colleges(course='B.Tech')
        for item in result:
            assert 'name' in item
            assert 'fees' in item
            assert 'entrance_exams' in item
            assert 'eligibility' in item


# ---- Feature 4: Exam Guidance ----

class TestExamGuidance:
    def test_engineering_category(self):
        result = get_exam_guidance(category='Engineering')
        assert result['category'] == 'Engineering'
        assert 'exams' in result
        assert len(result['exams']) > 0

    def test_career_mapping(self):
        result = get_exam_guidance(career='Software Engineer')
        assert result['category'] == 'Engineering'

    def test_list_categories(self):
        categories = list_all_categories()
        assert 'Engineering' in categories
        assert 'Medical' in categories

    def test_unknown_career_returns_all(self):
        result = get_exam_guidance(career='Unknown Career')
        assert 'categories' in result


# ---- Feature 5: Advanced Skill Gap Analysis ----

class TestAdvancedSkillGap:
    def test_school_gaps(self):
        result = analyze_skill_gaps_by_stage(['communication'], 'School')
        assert result['stage'] == 'School'
        assert 'core_gaps' in result
        assert 'coverage_percent' in result

    def test_phd_gaps(self):
        result = analyze_skill_gaps_by_stage(['research writing', 'data analysis'], 'PhD')
        assert result['stage'] == 'PhD'
        assert isinstance(result['core_gaps'], list)

    def test_coverage_percent_range(self):
        result = analyze_skill_gaps_by_stage([], 'Undergraduate')
        assert 0 <= result['coverage_percent'] <= 100


# ---- Feature 6: Career Simulator ----

class TestCareerSimulator:
    def test_known_career(self):
        result = simulate_career('AI Engineer', 'School')
        assert result['career'] == 'AI Engineer'
        assert 'steps' in result
        assert len(result['steps']) > 0

    def test_unknown_career_uses_default(self):
        result = simulate_career('Alien Scientist', 'Undergraduate')
        assert 'steps' in result

    def test_each_step_has_action(self):
        result = simulate_career('Software Engineer', 'Undergraduate')
        for step in result['steps']:
            assert 'step' in step
            assert 'action' in step


# ---- Feature 7: Career Twin ----

class TestCareerTwin:
    def test_returns_list(self):
        result = predict_career_twins(skills='python, machine learning')
        assert isinstance(result, list)
        assert len(result) > 0

    def test_probability_range(self):
        result = predict_career_twins(skills='python', interests='technology')
        for item in result:
            assert 0 <= item['probability'] <= 99

    def test_sorted_by_probability(self):
        result = predict_career_twins(skills='python, sql', education_level='Undergraduate')
        probs = [r['probability'] for r in result]
        assert probs == sorted(probs, reverse=True)


# ---- Feature 8: Market Analysis ----

class TestMarketAnalysis:
    def test_skill_demand_structure(self):
        result = get_skill_demand()
        assert 'top_skills' in result
        assert 'fastest_growing_careers' in result
        assert 'declining_industries' in result

    def test_top_skills_limit(self):
        result = get_top_skills(limit=5)
        assert len(result) == 5


# ---- Feature 9: Learning Engine ----

class TestLearningEngine:
    def test_known_career(self):
        result = generate_learning_roadmap('AI Engineer')
        assert 'phases' in result
        assert len(result['phases']) > 0

    def test_unknown_career_uses_default(self):
        result = generate_learning_roadmap('Space Colonist')
        assert 'phases' in result
        assert len(result['phases']) > 0

    def test_marks_known_skills(self):
        result = generate_learning_roadmap('Software Engineer', current_skills='git,python')
        for phase in result['phases']:
            for topic in phase['topics']:
                assert 'already_known' in topic


# ---- Feature 10: Resume + Profile Builder ----

class TestResumeBuilder:
    def test_resume_draft(self):
        result = generate_resume_draft({'name': 'Test', 'email': 'test@example.com', 'skills': 'python,sql'})
        assert 'header' in result
        assert 'skills' in result

    def test_linkedin_suggestions(self):
        result = generate_linkedin_suggestions({'skills': 'python,react', 'career_goal': 'AI Engineer'})
        assert isinstance(result, list)
        assert len(result) > 0

    def test_portfolio_recommendations(self):
        result = generate_portfolio_recommendations({'skills': 'python,javascript', 'education_level': 'PhD'})
        assert isinstance(result, list)
        assert any('Research' in r.get('type', '') for r in result)


# ---- Feature 11: Career Map ----

class TestCareerMap:
    def test_known_career(self):
        result = get_career_map('Data Scientist')
        assert result['career'] == 'Data Scientist'
        assert 'required_skills' in result
        assert 'average_salary' in result

    def test_unknown_career(self):
        result = get_career_map('Banana Expert')
        assert 'available_careers' in result

    def test_list_all(self):
        careers = list_all_careers()
        assert len(careers) > 5


# ---- API Endpoint Tests ----

class TestAPIEndpoints:
    @pytest.fixture
    def client(self):
        from secure_career_system.app import app
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        with app.test_client() as client:
            with app.app_context():
                from secure_career_system.extensions import db
                db.create_all()
            yield client

    def test_stream_recommendation(self, client):
        resp = client.post('/api/stream-recommendation',
                           data=json.dumps({'favorite_subjects': ['math']}),
                           content_type='application/json')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'recommendations' in data

    def test_course_recommendation(self, client):
        resp = client.post('/api/course-recommendation',
                           data=json.dumps({'stream': 'Science'}),
                           content_type='application/json')
        assert resp.status_code == 200
        assert 'recommendations' in resp.get_json()

    def test_college_recommendation(self, client):
        resp = client.post('/api/college-recommendation',
                           data=json.dumps({'course': 'B.Tech'}),
                           content_type='application/json')
        assert resp.status_code == 200
        assert 'recommendations' in resp.get_json()

    def test_exam_guidance(self, client):
        resp = client.post('/api/exam-guidance',
                           data=json.dumps({'career': 'Engineer'}),
                           content_type='application/json')
        assert resp.status_code == 200

    def test_career_simulation(self, client):
        resp = client.post('/api/career-simulation',
                           data=json.dumps({'target_career': 'AI Engineer', 'education_level': 'School'}),
                           content_type='application/json')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'steps' in data

    def test_career_twin(self, client):
        resp = client.post('/api/career-twin',
                           data=json.dumps({'skills': 'python,sql'}),
                           content_type='application/json')
        assert resp.status_code == 200
        assert 'career_twins' in resp.get_json()

    def test_skill_demand(self, client):
        resp = client.get('/api/skill-demand')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'top_skills' in data

    def test_learning_roadmap(self, client):
        resp = client.post('/api/learning-roadmap',
                           data=json.dumps({'target_career': 'Software Engineer'}),
                           content_type='application/json')
        assert resp.status_code == 200
        assert 'phases' in resp.get_json()

    def test_resume_builder(self, client):
        resp = client.post('/api/resume-builder',
                           data=json.dumps({'name': 'Test', 'skills': 'python'}),
                           content_type='application/json')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'resume_draft' in data
        assert 'linkedin_suggestions' in data

    def test_career_map(self, client):
        resp = client.post('/api/career-map',
                           data=json.dumps({'career': 'Data Scientist'}),
                           content_type='application/json')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'required_skills' in data

    def test_career_switch_roadmap(self, client):
        resp = client.post('/api/career-switch-roadmap',
                           data=json.dumps({'target_career': 'AI Engineer', 'current_skills': 'java,sql'}),
                           content_type='application/json')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'phases' in data
        assert data.get('switch_mode') is True

    def test_advanced_skill_gap(self, client):
        resp = client.post('/api/advanced-skill-gap',
                           data=json.dumps({'found_skills': ['python'], 'education_level': 'PhD'}),
                           content_type='application/json')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'core_gaps' in data
