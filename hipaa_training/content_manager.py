import json
import os


class ContentManager:
    """Manages loading and access to HIPAA training content from JSON."""

    def __init__(self):
        self.lessons = self._load_content("content/lessons.json")
        self.quiz_questions = self._load_content(
            "content/quiz_questions.json"
        )
        self.checklist_items = self._load_content(
            "content/checklist_items.json"
        )

    def _load_content(self, file_path: str):
        """Load content from JSON files with error handling."""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"Warning: Content file {file_path} not found.")
                return {} if 'lessons' in file_path else []
        except json.JSONDecodeError as e:
            print(f"Error loading {file_path}: {e}")
            return {} if 'lessons' in file_path else []
