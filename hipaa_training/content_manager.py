# hipaa_training/content_manager.py
import json
import os
from typing import Dict, List

class ContentManager:
    def __init__(self):
        self.content_dir = "content"
        self.lessons = self._load_content("lessons.json")
        self.quiz_questions = self._load_content("quiz_questions.json")
        self.checklist_items = self._load_content("checklist_items.json")

    def _load_content(self, filename: str) -> Dict:
        """Load content from JSON file with fallback"""
        filepath = os.path.join(self.content_dir, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._create_default_content(filename)
            with open(filepath, 'r') as f:
                return json.load(f)

    def _create_default_content(self, filename: str):
        """Create default content if file is missing"""
        os.makedirs(self.content_dir, exist_ok=True)
        filepath = os.path.join(self.content_dir, filename)
        default_content = {}
        if filename == "lessons.json":
            default_content = {
                "Sample Lesson": {
                    "content": "This is a sample lesson.",
                    "key_points": ["Point 1", "Point 2"],
                    "comprehension_questions": [
                        {
                            "question": "Sample question?",
                            "options": ["A", "B", "C", "D"],
                            "correct_index": 0
                        }
                    ]
                }
            }
        elif filename == "quiz_questions.json":
            default_content = [
                {
                    "question": "Sample quiz question?",
                    "options": ["A", "B", "C", "D"],
                    "correct_index": 0,
                    "explanation": "Sample explanation"
                }
            ]
        elif filename == "checklist_items.json":
            default_content = [
                {
                    "text": "Sample checklist item",
                    "category": "Sample",
                    "validation_hint": "Verify completion"
                }
            ]
        
        with open(filepath, 'w') as f:
            json.dump(default_content, f, indent=2)
