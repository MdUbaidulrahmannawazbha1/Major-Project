"""Tests for the Flask AI API endpoints."""
import json
import os
import sys

import pytest

# Ensure the package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from secure_career_system.app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def _login(client):
    """Register and log in a test user (bypasses OTP for simplicity)."""
    from secure_career_system.models import User
    with app.app_context():
        user = User(username='testuser', email='test@test.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        # Directly set the session to simulate login
        with client.session_transaction() as sess:
            sess['user'] = 'testuser'
            sess['_user_id'] = str(user.id)


def test_ai_career_recommend_page_requires_auth(client):
    resp = client.get('/ai/career-recommend')
    assert resp.status_code in (302, 308)


def test_ai_skill_gap_page_requires_auth(client):
    resp = client.get('/ai/skill-gap')
    assert resp.status_code in (302, 308)


def test_ai_placement_predict_page_requires_auth(client):
    resp = client.get('/ai/placement-predict')
    assert resp.status_code in (302, 308)


def test_ai_career_recommend_api_requires_auth(client):
    resp = client.post('/api/ai/career-recommend',
                       data=json.dumps({'features': [3] * 10}),
                       content_type='application/json')
    assert resp.status_code in (401, 302)


def test_ai_skill_gap_api_requires_auth(client):
    resp = client.post('/api/ai/skill-gap',
                       data=json.dumps({'career': 'Technology', 'skills': 'python'}),
                       content_type='application/json')
    assert resp.status_code in (401, 302)


def test_ai_placement_predict_api_requires_auth(client):
    resp = client.post('/api/ai/placement-predict',
                       data=json.dumps({'cgpa': 7.5, 'num_skills': 3}),
                       content_type='application/json')
    assert resp.status_code in (401, 302)
