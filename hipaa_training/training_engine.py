# hipaa_training/training_engine.py
import os
import json
import random
import shutil
from typing import Dict, Optional
from datetime import datetime
from rich.console import Console
from .models import Config, DatabaseManager
from .security import SecurityManager
from .content_manager import ContentManager

class EnhancedTrainingEngine:
    def __init__(self):
        self.console = Console()
        self.config = Config()
        self.db = DatabaseManager()
        self.security = SecurityManager()
        self.content = ContentManager()
        self.checklist = {}

    def display_lesson(self, user_id: int, lesson_title: str):
        """Display a lesson and its key points"""
        lesson = self.content.lessons.get(lesson_title)
        if not lesson:
            self.console.print(f"[red]Lesson '{lesson_title}' not found.[/red]")
            return
        
        self.console.print(f"\n[bold cyan]Lesson: {lesson_title}[/bold cyan]")
        self.console.print(lesson['content'])
        self.console.print("\n[bold]Key Points:[/bold]")
        for point in lesson['key_points']:
            self.console.print(f"  - {point}")
        self.security.log_action(user_id, "LESSON_VIEWED", f"Lesson: {lesson_title}")
        input("\nPress Enter to continue...")

    def _mini_quiz(self, lesson: Dict) -> bool:
        """Conduct a mini-quiz for a lesson"""
        questions = lesson.get('comprehension_questions', [])
        if not questions:
            return True
        
        correct = 0
        total = len(questions)
        for q in questions:
            self.console.print(f"\n[bold]Question: {q['question']}[/bold]")
            options = q['options']
            random.shuffle(options)
            correct_answer = options.index(q['options'][q['correct_index']])
            
            for i, option in enumerate(options, 1):
                self.console.print(f"{i}. {option}")
            
            while True:
                answer = input("Enter your answer (1-4): ").strip()
                if answer in ['1', '2', '3', '4']:
                    break
                self.console.print("[red]Invalid input. Enter a number 1-4.[/red]")
            
            if int(answer) - 1 == correct_answer:
                self.console.print("[green]Correct![/green]")
                correct += 1
            else:
                self.console.print(f"[red]Incorrect.[/red] Correct answer: {q['options'][q['correct_index']]}")
        
        score = (correct / total) * 100
        self.console.print(f"Score: {score}%")
        return score >= 70  # Configurable threshold

    def adaptive_quiz(self, user_id: int) -> float:
        """Conduct an adaptive quiz with randomized questions"""
        questions = random.sample(self.content.quiz_questions, min(10, len(self.content.quiz_questions)))
        correct = 0
        answers = {}
        
        for q in questions:
            self.console.print(f"\n[bold]Question: {q['question']}[/bold]")
            options = q['options']
            random.shuffle(options)
            correct_answer = options.index(q['options'][q['correct_index']])
            
            for i, option in enumerate(options, 1):
                self.console.print(f"{i}. {option}")
            
            while True:
                answer = input("Enter your answer (1-4): ").strip()
                if answer in ['1', '2', '3', '4']:
                    break
                self.console.print("[red]Invalid input. Enter a number 1-4.[/red]")
            
            user_answer = int(answer) - 1
            answers[q['question']] = {
                'selected': options[user_answer],
                'correct': q['options'][q['correct_index']],
                'is_correct': user_answer == correct_answer
            }
            if user_answer == correct_answer:
                self.console.print("[green]Correct![/green]")
                correct += 1
            else:
                self.console.print(f"[red]Incorrect.[/red] {q['explanation']}")
        
        score = (correct / len(questions)) * 100
        self.console.print(f"\nQuiz Score: {score}%")
        self.db.save_sensitive_progress(user_id, answers, score)
        self.security.log_action(user_id, "QUIZ_COMPLETED", f"Score: {score}%")
        return score

    def complete_enhanced_checklist(self, user_id: int):
        """Enhanced checklist with file upload validation"""
        self.console.print("\n" + "="*70)
        self.console.print("ENHANCED COMPLIANCE CHECKLIST")
        self.console.print("="*70)
        
        for item_data in self.content.checklist_items:
            text = item_data["text"]
            category = item_data["category"]
            validation_hint = item_data.get("validation_hint", "")
            
            self.console.print(f"\n[{category}] {text}")
            if validation_hint:
                self.console.print(f"   💡 {validation_hint}")
            
            response = ""
            while response not in ["y", "n", "yes", "no"]:
                response = input("Completed? (yes/no): ").strip().lower()
            
            evidence_path = None
            if response in ["y", "yes"] and any(keyword in validation_hint.lower() 
                                              for keyword in ['upload', 'file', 'document']):
                while True:
                    evidence_path = input("Enter path to evidence file (PDF/JPG/PNG, <5MB, or Enter to skip): ").strip()
                    if not evidence_path:
                        break
                    if not os.path.exists(evidence_path):
                        self.console.print("❌ File not found.")
                        continue
                    if os.path.getsize(evidence_path) > 5 * 1024 * 1024:  # 5MB limit
                        self.console.print("❌ File too large. Must be <5MB.")
                        continue
                    if not evidence_path.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                        self.console.print("❌ Invalid file type. Use PDF, JPG, or PNG.")
                        continue
                    
                    evidence_dir = f"evidence/user_{user_id}"
                    os.makedirs(evidence_dir, exist_ok=True)
                    filename = f"{category}_{text[:20].replace(' ', '_')}.{evidence_path.split('.')[-1]}"
                    dest_path = os.path.join(evidence_dir, filename)
                    
                    # Encrypt evidence file
                    with open(evidence_path, 'rb') as f:
                        encrypted_data = self.security.cipher.encrypt(f.read())
                    with open(dest_path, 'wb') as f:
                        f.write(encrypted_data)
                    
                    self.console.print(f"✅ Evidence saved: {filename}")
                    evidence_path = filename
                    break
            
            self.checklist[text] = response in ["y", "yes"]
            
            log_details = f"Item: {text}, Response: {response}"
            if evidence_path:
                log_details += f", Evidence: {evidence_path}"
            self.security.log_action(user_id, "CHECKLIST_ITEM_COMPLETED", log_details)
        
        self.console.print("\n✅ Checklist completed!")
        input("Press Enter to continue...")
