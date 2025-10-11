def test_content_manager_fallback():
    cm = ContentManager()
    assert isinstance(cm.lessons, dict)
    # Check that we have at least one lesson with expected structure
    assert len(cm.lessons) > 0
    first_lesson_key = list(cm.lessons.keys())[0]
    lesson = cm.lessons[first_lesson_key]
    
    # Verify lesson structure
    assert "content" in lesson
    assert "key_points" in lesson  
    assert "comprehension_questions" in lesson
