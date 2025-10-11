import os
import json


class ContentManager:
    """Handles loading and management of training content such as lessons, quizzes, and checklists."""

    def __init__(self):
        """Initialize content attributes with data or safe fallbacks."""
        self.lessons = self._load_content("lessons.json")
        self.quiz_questions = self._load_content("quiz_questions.json")
        self.checklist_items = self._load_content("checklist_items.json")

    def _load_content(self, filename):
        """Loads content from JSON file or returns fallback data if missing or invalid."""
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)
        path = os.path.join(data_dir, filename)

        if not os.path.exists(path):
            print(f"⚠️ Warning: {filename} not found. Using fallback content.")
            return self._fallback_content(filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print(f"⚠️ Warning: Failed to load {filename}. Using fallback content.")
            return self._fallback_content(filename)

    def _fallback_content(self, filename):
        """Provide fallback content based on file type."""
        if "lesson" in filename:
            return {
                "Sample Lesson": {
                    "content": "Fallback content",
                    "key_points": [],
                    "comprehension_questions": []
                }
            }
        elif "quiz" in filename:
            return [{"question": "Sample question?", "answer": "Sample answer"}]
        elif "checklist" in filename:
            return ["Sample checklist item"]
        return {}

