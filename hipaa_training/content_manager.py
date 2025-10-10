import os
import json


class ContentManager:
    """Handles loading and management of training content such as lessons and quizzes."""

    def __init__(self):
        """Initialize content attributes with data or defaults."""
        self.lessons = self._load_content("lessons.json")
        self.quiz_questions = self._load_content("quiz_questions.json")
        self.checklist_items = self._load_content("checklist_items.json")

    def _load_content(self, filename):
        """Loads content from JSON file or returns fallback data if missing."""
        path = os.path.join(os.path.dirname(__file__), "data", filename)

        if not os.path.exists(path):
            # Provide fallback content if file not found
            if "lesson" in filename:
                return {
                    "Sample Lesson": {
                        "content": "Fallback",
                        "key_points": [],
                        "comprehension_questions": []
                    }
                }
            elif "quiz" in filename:
                return [{"question": "Sample question?", "answer": "Sample answer"}]
            elif "checklist" in filename:
                return ["Sample checklist item"]
            return {}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

