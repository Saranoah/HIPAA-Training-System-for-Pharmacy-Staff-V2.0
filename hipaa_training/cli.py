import cmd
from .models import DatabaseManager
from .training_engine import EnhancedTrainingEngine
from .security import SecurityManager


class CLI(cmd.Cmd):
    """Command-line interface for the HIPAA Training System."""

    prompt = "HIPAA >> "
    intro = "Welcome to HIPAA Training System V3.0. Type 'help' for commands."

    def __init__(self):
        super().__init__()
        self.training_engine = EnhancedTrainingEngine()
        self.security = SecurityManager()
        self.current_user = None

    # -------------------------------
    # Core Commands
    # -------------------------------
    def do_login(self, line):
        """Login: login <username> <full_name> <role>"""
        try:
            args = line.split()
            if len(args) < 3:
                print("Usage: login <username> <full_name> <role>")
                return None

            username = args[0]
            full_name = " ".join(args[1:-1])
            role = args[-1]

            # Sanitize inputs
            username = self.security.sanitize_input(username, 50, False)
            full_name = self.security.sanitize_input(full_name, 100)
            role = self.security.sanitize_input(role, 50)

            with DatabaseManager()._get_connection() as conn:
                conn.row_factory = None
                cursor = conn.execute(
                    "INSERT OR IGNORE INTO users (username, full_name, role) VALUES (?, ?, ?)",
                    (username, full_name, role)
                )

                if cursor.lastrowid:
                    user_id = cursor.lastrowid
                else:
                    user = conn.execute(
                        "SELECT id FROM users WHERE username = ?",
                        (username,)
                    ).fetchone()
                    user_id = user["id"] if isinstance(user, dict) else user[0]

            self.current_user = {
                "id": user_id,
                "username": username,
                "full_name": full_name,
                "role": role,
            }

            self.security.log_action(user_id, "USER_LOGIN", f"Role: {role}")
            print(f"✅ Welcome, {full_name}!")

        except Exception as e:
            print(f"❌ Login error: {e}")

    def do_training(self, line):
        """Start complete training path"""
        if not self._check_auth():
            return None

        print("\n🎯 COMPLETE TRAINING PATH")
        print("=" * 50)

        user_id = self.current_user["id"]

        for lesson_title in self.training_engine.content.lessons.keys():
            success = self.training_engine.interactive_lesson(user_id, lesson_title)
            if not success:
                print("Training path incomplete. Please retry.")
                return None

        score = self.training_engine.adaptive_quiz(user_id)
        print(f"\n📊 Final Score: {score:.1f}%")

        if score >= 80:
            print("🎉 Congratulations! You passed the HIPAA training!")
        else:
            print("📚 Please review the materials and try again.")

    def do_quiz(self, line):
        """Take standalone quiz"""
        if not self._check_auth():
            return None

        score = self.training_engine.adaptive_quiz(self.current_user["id"])
        print(f"\n📊 Quiz Score: {score:.1f}%")

    def do_exit(self, line):
        """Exit the application"""
        print("Thank you for using HIPAA Training System!")
        return True

    # -------------------------------
    # Helpers
    # -------------------------------
    def _check_auth(self):
        if not self.current_user:
            print("❌ Please login first using 'login' command")
            return False
        return True

    def preloop(self):
        print("Initializing HIPAA Training System...")

    def postloop(self):
        print("Session ended.")
