import pytest
from hipaa_training.content_manager import ContentManager
from unittest.mock import patch, mock_open
import json

@pytest.fixture
def content_manager():
    return ContentManager()

def test_load_lessons_success(content_manager):
    """Test successful loading of lessons"""
    mock_lessons_data = {
        "Privacy Rule Basics": {
            "content": "Test content",
            "key_points": ["Point 1", "Point 2"],
            "comprehension_questions": []
        }
    }
    
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_lessons_data))):
        with patch('os.path.exists', return_value=True):
            lessons = content_manager._load_content('lessons.json')
            assert "Privacy Rule Basics" in lessons
            assert lessons["Privacy Rule Basics"]["content"] == "Test content"

def test_load_content_file_not_found(content_manager):
    """Test fallback when content file is missing"""
    with patch('os.path.exists', return_value=False):
        with patch('builtins.open', create=True):
            result = content_manager._load_content('lessons.json')
            assert isinstance(result, dict)
            assert "Sample Lesson" in result

def test_content_manager_initialization(content_manager):
    """Test that ContentManager initializes all content attributes"""
    assert hasattr(content_manager, 'lessons')
    assert hasattr(content_manager, 'quiz_questions') 
    assert hasattr(content_manager, 'checklist_items')
    assert isinstance(content_manager.lessons, dict)
    assert isinstance(content_manager.quiz_questions, list)
    assert isinstance(content_manager.checklist_items, list)
