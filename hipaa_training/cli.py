# hipaa_training/cli.py
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from .models import UserManager, DatabaseManager, ComplianceDashboard
from .training_engine import EnhancedTrainingEngine
from .security import SecurityManager

class CLI:
    def __init__(self):
        self.console = Console()
        self.db = DatabaseManager()
        self.user_manager = UserManager()
        self.training_engine = EnhancedTrainingEngine()
        self.compliance_dashboard = ComplianceDashboard()
        self.security = SecurityManager()

    def run(self):
        """Main CLI loop"""
        self._display_welcome()
        while True:
            self._display_menu()
            choice = input("Enter your choice (1-5): ").strip()
            self.security.log_action(0, "MENU_ACCESS", f"Selected option: {choice}")

            if choice == "1":
                self._create_user()
            elif choice == "2":
                self._start_training()
            elif choice == "3":
                self._complete_checklist()
            elif choice == "4":
                self._generate_report()
            elif choice == "5":
                self.console.print("[green]Exiting HIPAA Training System. Goodbye![/green]")
                break
            else:
                self.console.print("[red]Invalid choice. Please try again.[/red]")

    def _display_welcome(self):
        """Display welcome message with system info"""
        self.console.print(Panel.fit(
            "[bold cyan]Welcome to HIPAA Training System V3.0[/bold cyan]\n"
            "Enterprise-grade compliance training for pharmacies\n"
            f"Version: 3.0.0 | Date: {datetime.now().strftime('%Y-%m-%d')}",
            title="HIPAA Training",
            border_style="blue"
        ))

    def _display_menu(self):
        """Display main menu"""
        self.console.print("\n[bold]Main Menu[/bold]")
        self.console.print("1. Create New User")
        self.console.print("2. Start Training")
        self.console.print("3. Complete Compliance Checklist")
        self.console.print("4. Generate Compliance Report")
        self.console.print("5. Exit")

    def _create_user(self):
        """Create a new user"""
        username = input("Enter username: ").strip()
        full_name = input("Enter full name: ").strip()
        role = input("Enter role (admin/staff/auditor): ").strip().lower()
        try:
            user_id = self.user_manager.create_user(username, full_name, role)
            self.console.print(f"[green]User created successfully! ID: {user_id}[/green]")
        except ValueError as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def _start_training(self):
        """Start training session for a user"""
        user_id = input("Enter user ID: ").strip()
        if not user_id.isdigit() or not self.user_manager.user_exists(int(user_id)):
            self.console.print("[red]Invalid user ID.[/red]")
            return
        
        user_id = int(user_id)
        lessons = self.training_engine.content.lessons.keys()
        for lesson in lessons:
            self.training_engine.display_lesson(user_id, lesson)
            if not self.training_engine._mini_quiz(self.training_engine.content.lessons[lesson]):
                self.console.print("[red]Failed comprehension quiz. Please review the lesson.[/red]")
                continue
            self.db.save_progress(user_id, lesson, None, None)
        
        score = self.training_engine.adaptive_quiz(user_id)
        if score >= self.training_engine.config.PASS_THRESHOLD:
            certificate_id = self.db.issue_certificate(user_id, score)
            self.console.print(f"[green]Training completed! Certificate ID: {certificate_id}[/green]")
        else:
            self.console.print(f"[red]Failed quiz with score {score}%. Retake required.[/red]")

    def _complete_checklist(self):
        """Complete compliance checklist for a user"""
        user_id = input("Enter user ID: ").strip()
        if not user_id.isdigit() or not self.user_manager.user_exists(int(user_id)):
            self.console.print("[red]Invalid user ID.[/red]")
            return
        
        user_id = int(user_id)
        self.training_engine.complete_enhanced_checklist(user_id)
        self.db.save_sensitive_progress(user_id, self.training_engine.checklist, None)

    def _generate_report(self):
        """Generate compliance report"""
        format_type = input("Enter report format (csv/json): ").strip().lower()
        if format_type not in ['csv', 'json']:
            self.console.print("[red]Invalid format. Use 'csv' or 'json'.[/red]")
            return
        filename = self.compliance_dashboard.generate_enterprise_report(format_type)
        self.console.print(f"[green]Report generated: {filename}[/green]")
