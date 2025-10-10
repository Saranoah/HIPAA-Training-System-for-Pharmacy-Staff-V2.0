import json
import os


class ContentManager:
    """Manages loading and providing training content."""

    def __init__(self):
        self.base_path = os.path.join(os.getcwd(), "content")

    def _load_content(self, filename):
        """Load content from JSON file; fallback to sample data if missing."""
        file_path = os.path.join(self.base_path, filename)

        if not os.path.exists(file_path):
            print(f"Warning: Content file {filename} not found.")
            # Fallback sample content for missing files
            if "lesson" in filename.lower():
                return {"Sample Lesson": "This is a placeholder lesson about HIPAA basics."}
            elif "quiz" in filename.lower():
                return {"Sample Question": "What does HIPAA protect?"}
            elif "checklist" in filename.lower():
                return {"Sample Checklist Item": "Ensure patient data confidentiality."}
            else:
                return {"Sample": "Default content"}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return {}

    def load_lessons(self):
        """Load lesson content."""
        return self._load_content("lessons.json")

    def load_quiz_questions(self):
        """Load quiz questions."""
        return self._load_content("quiz_questions.json")

    def load_checklist_items(self):
        """Load checklist items."""
        return self._load_content("checklist_items.json")
