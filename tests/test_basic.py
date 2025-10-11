# In tests/test_basic.py, update the test_content_manager_fallback function:

def test_content_manager_fallback():
    cm = ContentManager()
    assert isinstance(cm.lessons, dict)
    # Change from "Sample Lesson" to "Privacy Rule"
    assert "Privacy Rule" in cm.lessons
    # Also verify the lesson structure
    privacy_lesson = cm.lessons["Privacy Rule"]
    assert "content" in privacy_lesson
    assert "key_points" in privacy_lesson
    assert "comprehension_questions" in privacy_lesson
