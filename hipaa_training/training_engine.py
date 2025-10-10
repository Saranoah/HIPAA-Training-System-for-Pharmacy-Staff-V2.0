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

    def interactive_lesson(
        self, user_id: int, lesson_title: str
    ) -> bool:
        """Deliver interactive lesson with comprehension check"""
        lesson = self.content.lessons.get(lesson_title)
        if not lesson:
            return False

        print(f"\n🎓 LESSON: {lesson_title}")
        print("=" * 60)
        print(lesson['content'])

        # Display key points
        if 'key_points' in lesson:
            print("\nKey Points:")
            for point in lesson['key_points']:
                print(f"  • {point}")

        # Comprehension check
        if self._mini_quiz(lesson):
            self._mark_lesson_complete(user_id, lesson_title)
            self.security.log_action(
                user_id,
                "LESSON_COMPLETED",
                f"Lesson: {lesson_title}"
            )
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
            print(f"\nQ{i}: {q['question']}")
            for j, option in enumerate(q['options'], 1):
                print(f"  {j}. {option}")

            try:
                answer = int(input("\nYour answer (1-4): ")) - 1
                is_correct = (
                    0 <= answer < len(q['options']) and
                    answer == q['correct_index']
                )
                if is_correct:
                    print("✅ Correct!")
                    correct_answers += 1
                else:
                    correct_option = q['options'][
                        q['correct_index']
                    ]
                    print(
                        f"❌ Incorrect. The answer was: "
                        f"{correct_option}"
                    )
            except (ValueError, IndexError):
                print("❌ Invalid input.")

        return correct_answers >= len(questions) * 0.7

    def _mark_lesson_complete(
        self, user_id: int, lesson_title: str
    ):
        """Record lesson completion in database"""
        with self.db._get_connection() as conn:
            conn.execute(
                "INSERT INTO training_progress "
                "(user_id, lesson_completed, completed_at) "
                "VALUES (?, ?, ?)",
                (user_id, lesson_title, datetime.now())
            )

    def adaptive_quiz(self, user_id: int) -> float:
        """Administer adaptive quiz with randomized questions"""
        questions = self.content.quiz_questions.copy()

        if not questions:
            return 0.0

        random.shuffle(questions)
        selected_questions = questions[:10]  # Use 10 questions

        score = 0
        num_questions = len(selected_questions)
        print(
            f"\n🧠 HIPAA KNOWLEDGE QUIZ "
            f"({num_questions} questions)"
        )
        print("=" * 60)

        for i, q in enumerate(selected_questions, 1):
            print(f"\nQ{i}: {q['question']}")

            # Randomize options
            options = q['options'].copy()
            correct_answer = options[q['correct_index']]
            random.shuffle(options)
            new_correct_index = options.index(correct_answer)

            for j, option in enumerate(options):
                print(f"  {chr(65 + j)}. {option}")

            answer = ""
            while answer not in ["A", "B", "C", "D"]:
                answer = input(
                    "\nYour answer (A/B/C/D): "
                ).strip().upper()

            user_answer_index = ord(answer) - ord('A')
            if user_answer_index == new_correct_index:
                print("✅ Correct!")
                score += 1
            else:
                correct_letter = chr(65 + new_correct_index)
                print(
                    f"❌ Incorrect. Correct answer: "
                    f"{correct_letter}"
                )
                print(f"Explanation: {q['explanation']}")

        percentage = (score / len(selected_questions)) * 100
        self._save_quiz_results(user_id, percentage)
        self.security.log_action(
            user_id, "QUIZ_COMPLETED", f"Score: {percentage}%"
        )

        return percentage

    def _save_quiz_results(self, user_id: int, score: float):
        """Save quiz results to database"""
        with self.db._get_connection() as conn:
            conn.execute(
                "INSERT INTO training_progress "
                "(user_id, quiz_score, completed_at) "
                "VALUES (?, ?, ?)",
                (user_id, score, datetime.now())
            )
