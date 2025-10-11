import pytest
from unittest.mock import Mock, patch
from hipaa_system_v3 import EnhancedTrainingEngine, ContentManager
import json

@pytest.fixture
def training_engine():
    engine = EnhancedTrainingEngine()
    # Mock the database and security to avoid side effects
    engine.db = Mock()
    engine.security = Mock()
    engine.user_manager = Mock()
    return engine

@pytest.fixture
def sample_lesson():
    return {
        "content": "Test lesson content",
        "key_points": ["Point 1", "Point 2"],
        "comprehension_questions": [
            {
                "question": "Test question 1?",
                "options": ["A", "B", "C", "D"],
                "correct_index": 0
            },
            {
                "question": "Test question 2?",
                "options": ["A", "B", "C", "D"],
                "correct_index": 1
            }
        ]
    }

def test_mini_quiz_all_correct(training_engine, sample_lesson):
    """Test mini quiz with all correct answers"""
    with patch('builtins.input', side_effect=['1', '2']):
        result = training_engine._mini_quiz(sample_lesson)
        assert result is True

def test_mini_quiz_some_incorrect(training_engine, sample_lesson):
    """Test mini quiz with some incorrect answers"""
    with patch('builtins.input', side_effect=['2', '2']):  # First wrong, second right
        result = training_engine._mini_quiz(sample_lesson)
        assert result is False  # 50% correct, below 70% threshold

def test_adaptive_quiz_scoring(training_engine):
    """Test adaptive quiz scoring calculation"""
    with patch.object(training_engine, 'content') as mock_content:
        mock_content.quiz_questions = [
            {
                "question": "Q1",
                "options": ["A", "B", "C", "D"],
                "correct_index": 0,
                "explanation": "Test"
            }
        ] * 10  # 10 identical questions
        
        # Mock user getting 8 out of 10 correct
        with patch('builtins.input', side_effect=['1'] * 8 + ['2'] * 2):
            with patch('hipaa_system_v3.random.shuffle'):
                score = training_engine.adaptive_quiz(1)
                assert score == 80.0

def test_content_manager_loading():
    """Test content manager loads files correctly"""
    with patch('builtins.open') as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = '{"test": "data"}'
        cm = ContentManager()
        assert hasattr(cm, 'lessons')
        assert hasattr(cm, 'quiz_questions')
        assert hasattr(cm, 'checklist_items')
