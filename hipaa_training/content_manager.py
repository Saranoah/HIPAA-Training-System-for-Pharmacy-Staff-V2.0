import json
import os
from rich.console import Console

console = Console()


class ContentManager:
    """
    Loads and manages training content (lessons, quizzes, checklists).
    Falls back to default content if files are missing.
    """

    def __init__(self):
        self.lessons = self._load_json("content/lessons.json", self._default_lessons())
        self.quiz_questions = self._load_json("content/quiz_questions.json", self._default_quiz_questions())
        self.checklist_items = self._load_json("content/checklist_items.json", self._default_checklist_items())

    def _load_json(self, path, fallback):
        """Load JSON content with fallback."""
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                console.print(f"⚠️ Warning: {os.path.basename(path)} not found. Using fallback content.")
                return fallback
        except Exception as e:
            console.print(f"⚠️ Error loading {path}: {e}")
            return fallback

    # ---------- Fallback Content ---------- #
    def _default_lessons(self):
        return {
            "Sample Lesson": {
                "content": "Welcome to the HIPAA Training System! This is a sample fallback lesson.",
                "key_points": [
                    "Understand patient privacy.",
                    "Protect PHI under HIPAA.",
                    "Report any data breach immediately."
                ],
                "comprehension_questions": [
                    {
                        "question": "What is PHI?",
                        "options": ["Protected Health Information", "Public Health Info", "Patient Hospital ID", "Private Healthcare Insurance"],
                        "correct_index": 0
                    }
                ]
            },
            "Privacy Rule": {
                "content": "The HIPAA Privacy Rule protects individuals' medical records and other personal health information.",
                "key_points": [
                    "Covers all forms of PHI",
                    "Requires patient authorization for disclosure"
                ],
                "comprehension_questions": [
                    {
                        "question": "What does the Privacy Rule protect?",
                        "options": ["PHI", "Social Media", "Credit Scores", "Employment Records"],
                        "correct_index": 0
                    }
                ]
            }
        }

    def _default_quiz_questions(self):
        return [
            {
                "question": "What should you do if you suspect a HIPAA violation?",
                "options": ["Ignore it", "Report to Privacy Officer", "Post about it", "Tell a friend"],
                "correct_index": 1
            }
        ]

    def _default_checklist_items(self):
        return [
            "Completed HIPAA Privacy training",
            "Reviewed PHI storage procedures",
            "Understands breach reporting protocol"
        ]

