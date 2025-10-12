# hipaa_training/content_manager.py
import json
import os
from typing import Any


class ContentManager:
    """
    Manages training content (lessons, quizzes, checklists)
    
    FIXES APPLIED:
    - Better error handling for missing files
    - Creates default content if files don't exist
    - Type hints added
    - Validates JSON structure
    """

    def __init__(self, content_dir: str = "content"):
        self.content_dir = content_dir
        self.lessons = self._load_content("lessons.json")
        self.quiz_questions = self._load_content("quiz_questions.json")
        self.checklist_items = self._load_content("checklist_items.json")
        self._validate_content()

    def _load_content(self, filename: str) -> Any:
        """
        Load content from JSON file with fallback to defaults
        """
        filepath = os.path.join(self.content_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = json.load(f)
                print(f"✓ Loaded {filename}")
                return content
        except FileNotFoundError:
            print(f"⚠ {filename} not found. Creating default content...")
            self._create_default_content(filename)
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing {filename}: {e}")
            print("⚠ Creating default content...")
            self._create_default_content(filename)
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)

    def _create_default_content(self, filename: str) -> None:
        os.makedirs(self.content_dir, exist_ok=True)
        filepath = os.path.join(self.content_dir, filename)
        default_content = self._get_default_content(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(default_content, f, indent=2, ensure_ascii=False)
        print(f"✓ Created default {filename}")

    def _get_default_content(self, filename: str) -> Any:
        """Get default content structure based on filename"""
        if filename == "lessons.json":
            return {
                "What is PHI?": {
                    "content": (
                        "Protected Health Information (PHI) is any information in a medical "
                        "record that can be used to identify an individual and was created, "
                        "used, or disclosed in the course of providing healthcare services.\n\n"
                        "PHI includes 18 identifiers such as name, address, dates, phone numbers, "
                        "email addresses, social security numbers, medical record numbers, and more."
                    ),
                    "key_points": [
                        "PHI must be protected under HIPAA regulations",
                        "18 specific identifiers are considered PHI",
                        "Both electronic and paper PHI must be secured",
                        "Unauthorized access to PHI can result in penalties",
                    ],
                    "comprehension_questions": [
                        {
                            "question": "Which of the following is NOT considered PHI?",
                            "options": [
                                "Patient's name",
                                "De-identified medical data",
                                "Medical record number",
                                "Patient's email address",
                            ],
                            "correct_index": 1,
                        },
                        {
                            "question": "How many identifiers does HIPAA define as PHI?",
                            "options": [
                                "10 identifiers",
                                "15 identifiers",
                                "18 identifiers",
                                "20 identifiers",
                            ],
                            "correct_index": 2,
                        },
                    ],
                },
                "HIPAA Privacy Rule": {
                    "content": (
                        "The HIPAA Privacy Rule establishes national standards to protect "
                        "individuals' medical records and other personal health information.\n\n"
                        "It gives patients rights over their health information and sets rules on "
                        "who can access and receive your health information."
                    ),
                    "key_points": [
                        "Protects all individually identifiable health information",
                        "Applies to covered entities and business associates",
                        "Gives patients rights to access their records",
                        "Limits use and disclosure of PHI",
                    ],
                    "comprehension_questions": [
                        {
                            "question": "What does the Privacy Rule primarily protect?",
                            "options": [
                                "Financial information",
                                "Medical records and PHI",
                                "Employee records",
                                "Business contracts",
                            ],
                            "correct_index": 1,
                        }
                    ],
                },
                "Security Rule": {
                    "content": (
                        "The HIPAA Security Rule establishes national standards to protect "
                        "electronic protected health information (ePHI) that is created, "
                        "received, maintained, or transmitted electronically."
                    ),
                    "key_points": [
                        "Applies specifically to ePHI",
                        "Requires administrative, physical, and technical safeguards",
                        "Mandates risk assessments",
                        "Requires encryption for data at rest and in transit",
                    ],
                    "comprehension_questions": [
                        {
                            "question": "What type of PHI does the Security Rule specifically address?",
                            "options": [
                                "Paper records",
                                "Verbal communications",
                                "Electronic PHI (ePHI)",
                                "All forms of PHI",
                            ],
                            "correct_index": 2,
                        }
                    ],
                },
            }

        elif filename == "quiz_questions.json":
            return [
                {
                    "question": "What is the minimum necessary standard under HIPAA?",
                    "options": [
                        "Access all patient records freely",
                        "Only access PHI needed to perform your job",
                        "Share PHI with all staff members",
                        "Keep PHI on your desk",
                    ],
                    "correct_index": 1,
                    "explanation": (
                        "The minimum necessary standard requires that only the minimum amount of PHI "
                        "needed to accomplish a task should be accessed or disclosed."
                    ),
                },
                {
                    "question": "How soon must a breach affecting 500+ individuals be reported to HHS?",
                    "options": ["Immediately", "Within 30 days", "Within 60 days", "Within 90 days"],
                    "correct_index": 2,
                    "explanation": "Breaches affecting 500 or more individuals must be reported within 60 days.",
                },
            ]

        elif filename == "checklist_items.json":
            return [
                {"text": "Privacy Rule training completed", "category": "Training", "validation_hint": "Verify completion certificate or records"},
                {"text": "Security Rule requirements reviewed", "category": "Training", "validation_hint": "Confirm understanding of technical safeguards"},
                {"text": "Understand breach notification timeline (60 days)", "category": "Knowledge", "validation_hint": "Can explain reporting requirements"},
                {"text": "Can identify unauthorized PHI access", "category": "Knowledge", "validation_hint": "Knows when to report incidents"},
            ]

        return {}

    def _validate_content(self) -> None:
        if not isinstance(self.lessons, dict):
            raise ValueError("Lessons content must be a dictionary")
        if not isinstance(self.quiz_questions, list):
            raise ValueError("Quiz questions must be a list")
        if not isinstance(self.checklist_items, list):
            raise ValueError("Checklist items must be a list")
