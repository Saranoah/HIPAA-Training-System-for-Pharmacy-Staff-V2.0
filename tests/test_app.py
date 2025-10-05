import json
import pytest
from src.hipaa_ai_pharmacy_production import app, load_user_progress, create_new_user_progress, calculate_level

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """Test that homepage loads successfully"""
    response = client.get('/')
    assert response.status_code == 200


def test_get_lessons(client):
    """Ensure lessons endpoint returns valid JSON"""
    response = client.get('/api/lessons')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "Privacy Rule" in data


def test_get_quiz(client):
    """Ensure quiz returns a list of questions"""
    response = client.get('/api/quiz')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert "question" in data[0]


def test_submit_quiz(client):
    """Simulate submitting quiz answers"""
    # Send all answers as '0' to simulate user attempt
    answers = [0] * 15
    response = client.post('/api/submit-quiz', json={'answers': answers})
    assert response.status_code == 200
    data = response.get_json()
    assert "percentage" in data
    assert "badge" in data
    assert isinstance(data["results"], list)


def test_update_checklist(client):
    """Test updating a checklist item"""
    response = client.post('/api/update-checklist', json={
        "item_id": "privacy_training",
        "checked": True
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "compliance_percentage" in data
    assert data["success"] is True


def test_complete_lesson(client):
    """Test completing a lesson"""
    response = client.post('/api/complete-lesson', json={
        "lesson_name": "Privacy Rule"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "xp_earned" in data
    assert data["success"] is True


def test_calculate_level():
    """Ensure XP translates to proper level"""
    assert calculate_level(0) == 1
    assert calculate_level(50) == 2
    assert calculate_level(100) == 3


def test_load_and_create_user_progress():
    """Check user progress creation"""
    progress = create_new_user_progress()
    assert "xp" in progress
    assert isinstance(progress["checklist"], dict)
    assert isinstance(progress["lessons_completed"], list)
