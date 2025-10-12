# hipaa_training/content_manager.py
import os
from typing import Dict, List
from .models import Config


class ContentManager:
    """
    Manages lessons, quizzes, and checklist content for HIPAA training.
    """

    def __init__(self):
        self.lessons: Dict[str, Dict] = self.load_lessons()
        self.quiz_questions: List[Dict] = self.load_quiz_questions()
        self.checklist_items: List[Dict] = self.load_checklist_items()

    def load_lessons(self) -> Dict[str, Dict]:
        """Load lessons from JSON or other source"""
        lessons = {}
        # Example: Load lessons from a JSON file
        path = os.path.join(Config.CONTENT_DIR, "lessons.json")
        if os.path.exists(path):
            import json
            with open(path, "r", encoding="utf-8") as f:
                lessons = json.load(f)
        return lessons

    def load_quiz_questions(self) -> List[Dict]:
        """Load quiz questions from JSON"""
        questions = []
        path = os.path.join(Config.CONTENT_DIR, "quiz_questions.json")
        if os.path.exists(path):
            import json
            with open(path, "r", encoding="utf-8") as f:
                questions = json.load(f)
        return questions

    def load_checklist_items(self) -> List[Dict]:
        """Load checklist items from JSON"""
        items = []
        path = os.path.join(Config.CONTENT_DIR, "checklist_items.json")
        if os.path.exists(path):
            import json
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
        return items

    def get_lesson_titles(self) -> List[str]:
        """Return list of lesson titles"""
        return list(self.lessons.keys())

    def get_quiz_summary(self) -> List[str]:
        """Return a brief summary of quiz questions"""
        summaries = []
        for q in self.quiz_questions:
            question_text = q.get("question", "")
            if len(question_text) > 80:
                question_text = question_text[:77] + "..."
            summaries.append(question_text)
        return summaries

    def get_checklist_summary(self) -> List[str]:
        """Return a brief summary of checklist items"""
        summaries = []
        for item in self.checklist_items:
            text = item.get("text", "")
            if len(text) > 80:
                text = text[:77] + "..."
            summaries.append(text)
        return summaries
