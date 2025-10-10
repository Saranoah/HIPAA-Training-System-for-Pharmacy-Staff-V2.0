# hipaa_training/models.py
import os
import sqlite3
from datetime import datetime, timedelta
import json
from typing import Dict, Optional
from .security import SecurityManager

class Config:
    DB_PATH = os.getenv('DB_URL', 'hipaa_training.db')
    PASS_THRESHOLD = int(os.getenv('PASS_THRESHOLD', 80))
    TRAINING_EXPIRY_DAYS = int(os.getenv('TRAINING_EXPIRY_DAYS', 365))
    AUDIT_RETENTION_YEARS = int(os.getenv('AUDIT_RETENTION_YEARS', 6))
    ENCRYPTION_KEY = os.getenv('HIPAA_ENCRYPTION_KEY', 'default_key_change_in_production')

class DatabaseManager:
    def __init__(self, db_path: str = Config.DB_PATH):
        self.db_path = db_path
        self.security = SecurityManager()
        self._initialize_database()

    def _initialize_database(self):
        """Initialize SQLite database with necessary tables"""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS training_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    lesson_title TEXT,
                    quiz_score REAL,
                    checklist_data TEXT,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS certificates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    certificate_id TEXT UNIQUE,
                    score REAL,
                    issue_date TIMESTAMP,
                    expiry_date TIMESTAMP,
                    revoked BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT,
                    details TEXT,
                    timestamp TIMESTAMP,
                    ip_address TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

    def _get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.commit()
            conn.close()

    def save_progress(self, user_id: int, lesson_title: str, score: Optional[float], checklist_data: Optional[Dict]):
        """Save training progress"""
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO training_progress (user_id, lesson_title, quiz_score, checklist_data, completed_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (user_id, lesson_title, score, json.dumps(checklist_data) if checklist_data else None, datetime.now())
            )
            self.security.log_action(user_id, "PROGRESS_SAVED", f"Lesson: {lesson_title}")

    def save_sensitive_progress(self, user_id: int, checklist_data: Dict, score: Optional[float]):
        """Save progress with encrypted sensitive data"""
        encrypted_checklist = self.security.encrypt_data(json.dumps(checklist_data))
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO training_progress (user_id, quiz_score, checklist_data, completed_at) "
                "VALUES (?, ?, ?, ?)",
                (user_id, score, encrypted_checklist, datetime.now())
            )
            self.security.log_action(user_id, "SENSITIVE_PROGRESS_SAVED", "Checklist completed")

    def issue_certificate(self, user_id: int, score: float) -> str:
        """Issue a training certificate"""
        import uuid
        certificate_id = str(uuid.uuid4())
        issue_date = datetime.now()
        expiry_date = issue_date + timedelta(days=Config.TRAINING_EXPIRY_DAYS)
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO certificates (user_id, certificate_id, score, issue_date, expiry_date) "
                "VALUES (?, ?, ?, ?, ?)",
                (user_id, certificate_id, score, issue_date, expiry_date)
            )
            self.security.log_action(user_id, "CERTIFICATE_ISSUED", f"Certificate ID: {certificate_id}")
        return certificate_id

    def get_compliance_stats(self) -> Dict:
        """Retrieve compliance statistics for reporting"""
        with self._get_connection() as conn:
            user_stats = conn.execute(
                "SELECT COUNT(*) as total_users, AVG(quiz_score) as avg_score, "
                "SUM(CASE WHEN quiz_score >= ? THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as pass_rate "
                "FROM training_progress WHERE quiz_score IS NOT NULL",
                (Config.PASS_THRESHOLD,)
            ).fetchone()
            cert_stats = conn.execute(
                "SELECT COUNT(*) as total_certs, "
                "SUM(CASE WHEN expiry_date > ? AND revoked = FALSE THEN 1 ELSE 0 END) as active_certs, "
                "SUM(CASE WHEN expiry_date <= ? THEN 1 ELSE 0 END) as expired_certs "
                "FROM certificates",
                (datetime.now(), datetime.now())
            ).fetchone()
        return {
            "total_users": user_stats["total_users"],
            "avg_score": user_stats["avg_score"] or 0,
            "pass_rate": user_stats["pass_rate"] or 0,
            "total_certs": cert_stats["total_certs"],
            "active_certs": cert_stats["active_certs"],
            "expired_certs": cert_stats["expired_certs"]
        }

class UserManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.security = SecurityManager()

    def _sanitize_input(self, input_str: str, max_length: int) -> str:
        """Sanitize user input to prevent injection"""
        import re
        sanitized = re.sub(r'[^\w\s]', '', input_str.strip())
        return sanitized[:max_length]

    def create_user(self, username: str, full_name: str, role: str) -> int:
        """Create a new user"""
        username = self._sanitize_input(username, 50)
        full_name = self._sanitize_input(full_name, 100)
        if role not in ['admin', 'staff', 'auditor']:
            raise ValueError("Invalid role. Use 'admin', 'staff', or 'auditor'.")
        if not username or not full_name:
            raise ValueError("Username and full name cannot be empty.")
        
        with self.db._get_connection() as conn:
            try:
                cursor = conn.execute(
                    "INSERT INTO users (username, full_name, role) VALUES (?, ?, ?)",
                    (username, full_name, role)
                )
                user_id = cursor.lastrowid
                self.security.log_action(user_id, "USER_CREATED", f"Username: {username}")
                return user_id
            except sqlite3.IntegrityError:
                raise ValueError("Username already exists.")

    def user_exists(self, user_id: int) -> bool:
        """Check if user exists"""
        with self.db._get_connection() as conn:
            result = conn.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone()
            return bool(result)

class ComplianceDashboard:
    def __init__(self):
        self.db = DatabaseManager()

    def generate_enterprise_report(self, format_type: str) -> str:
        """Generate compliance report in CSV or JSON"""
        stats = self.db.get_compliance_stats()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/compliance_dashboard_{timestamp}.{format_type}"
        
        os.makedirs("reports", exist_ok=True)
        if format_type == "csv":
            import csv
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=stats.keys())
                writer.writeheader()
                writer.writerow(stats)
        else:  # json
            with open(filename, 'w') as f:
                json.dump(stats, f, indent=2)
        
        return filename
