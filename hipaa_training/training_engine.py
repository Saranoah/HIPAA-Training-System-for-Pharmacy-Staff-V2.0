import random
from datetime import datetime


class EnhancedTrainingEngine:
    """
    Core training logic with interactive lessons, quizzes,
    and compliance tracking.
    """

    def __init__(self):
        from .content_manager import ContentManager
        from .models import DatabaseManager
        from .security import SecurityManager

        self.content = ContentManager()
        self.db = DatabaseManager()
        self.security = SecurityManager()
        self.checklist = {}

    # ---------- LESSONS ---------- #
    def interactive_lesson(self, user_id: int, lesson_title: str) -> bool:
        """Deliver interactive lesson with comprehension check"""
        lesson = self.content.lessons.get(lesson_title)
        if not lesson:
            print(f"⚠️ Lesson not found: {lesson_title}")
            return False

        print(f"\n🎓 LESSON: {lesson_title}")
        print("=" * 60)
        print(lesson.get('content', 'No content available.'))

        # Display key points
        key_points = lesson.get('key_points', [])
        if key_points:
            print("\nKey Points:")
            for point in key_points:
                print(f"  • {point}")

        # Comprehension check
        if self._mini_quiz(lesson):
            self._mark_lesson_complete(user_id, lesson_title)
            self.security.log_action(user_id, "LESSON_COMPLETED", f"Lesson: {lesson_title}")
            return True
        else:
            print("\n❌ Please review the lesson and try again.")
            return False

    def _mini_quiz(self, lesson: dict) -> bool:
        """Mini quiz after each lesson"""
        questions = lesson.get('comprehension_questions', [])
        if not questions:
            return True

        correct_answers = 0
        for i, q in enumerate(questions, 1):
            if not all(k in q for k in ("question", "options", "correct_index")):
                print(f"⚠️ Skipping invalid question: {q}")
                continue

            print(f"\nQ{i}: {q['question']}")
            for j, option in enumerate(q['options']):
                print(f"  {j+1}. {option}")

            try:
                answer = int(input("\nYour answer (1-4): ")) - 1
            except EOFError:
                print("⚠️ No input detected, skipping question.")
                answer = -1
            except ValueError:
                print("❌ Invalid input.")
                answer = -1

            is_correct = 0 <= answer < len(q['options']) and answer == q['correct_index']
            if is_correct:
                print("✅ Correct!")
                correct_answers += 1
            else:
                correct_option = q['options'][q['correct_index']]
                print(f"❌ Incorrect. The correct answer was: {correct_option}")

        return correct_answers >= len(questions) * 0.7

    # ---------- DATABASE OPERATIONS ---------- #
    def _mark_lesson_complete(self, user_id: int, lesson_title: str):
        """Record lesson completion in database"""
        self.db._init_db()  # ensure tables exist
        with self.db._get_connection() as conn:
            conn.execute(
                "INSERT INTO training_progress (user_id, lesson_completed, completed_at) VALUES (?, ?, ?)",
                (user_id, lesson_title, datetime.now())
            )

    def _save_quiz_results(self, user_id: int, score: float):
        """Save quiz results to database"""
        self.db._init_db()
        with self.db._get_connection() as conn:
            conn.execute(
                "INSERT INTO training_progress (user_id, quiz_score, completed_at) VALUES (?, ?, ?)",
                (user_id, score, datetime.now())
            )

    # ---------- QUIZ LOGIC ---------- #
    def adaptive_quiz(self, user_id: int) -> float:
        """Administer adaptive quiz with randomized questions"""
        questions = self.content.quiz_questions.copy()
        if not questions:
            print("⚠️ No quiz questions available.")
            return 0.0

        random.shuffle(questions)
        selected_questions = questions[:10]

        score = 0
        print(f"\n🧠 HIPAA KNOWLEDGE QUIZ ({len(selected_questions)} questions)")
        print("=" * 60)

        for i, q in enumerate(selected_questions, 1):
            if not all(k in q for k in ("question", "options", "correct_index")):
                print(f"⚠️ Skipping invalid question: {q}")
                continue

            print(f"\nQ{i}: {q['question']}")
            options = q['options'].copy()
            correct_answer = options[q['correct_index']]
            random.shuffle(options)
            new_correct_index = options.index(correct_answer)

            for j, option in enumerate(options):
                print(f"  {chr(65 + j)}. {option}")

            try:
                answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            except EOFError:
                answer = "A"  # fallback for CI

            user_answer_index = ord(answer) - ord('A')
            if 0 <= user_answer_index < len(options) and user_answer_index == new_correct_index:
                print("✅ Correct!")
                score += 1
            else:
                correct_letter = chr(65 + new_correct_index)
                explanation = q.get("explanation", "No explanation available.")
                print(f"❌ Incorrect. Correct answer: {correct_letter}")
                print(f"Explanation: {explanation}")

        percentage = (score / len(selected_questions)) * 100
        self._save_quiz_results(user_id, percentage)
        self.security.log_action(user_id, "QUIZ_COMPLETED", f"Score: {percentage}%")
        return percentage
