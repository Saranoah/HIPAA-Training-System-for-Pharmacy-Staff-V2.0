import os
import sqlite3
from datetime import datetime


class DatabaseManager:
    """
    Handles database initialization, connection, and basic persistence
    for HIPAA training system.
    """

    db_path = os.path.join("data", "hipaa_training.db")
    connection = None

    def __init__(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            self._init_db()
        else:
            self._get_connection()  # reuse if exists

    # ---------- Connection Handling ---------- #
    def _get_connection(self):
        """Get a shared SQLite connection."""
        if DatabaseManager.connection is None:
            DatabaseManager.connection = sqlite3.connect(self.db_path)
            DatabaseManager.connection.row_factory = sqlite3.Row
        return DatabaseManager.connection

    # ---------- Database Initialization ---------- #
    def _init_db(self):
        """Initialize database tables (creates file if missing)."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self._get_connection()

        # Create schema
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS training_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lesson_completed TEXT,
                quiz_score REAL,
                checklist_data TEXT,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                certificate_id TEXT UNIQUE NOT NULL,
                score REAL NOT NULL,
                issue_date TIMESTAMP,
                expiry_date TIMESTAMP,
                revoked BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()

    # ---------- Utility Functions ---------- #
    def add_user(self, username: str, full_name: str, role: str = "staff"):
        """Add a user to the system."""
        conn = self._get_connection()
        conn.execute(
            "INSERT OR IGNORE INTO users (username, full_name, role) VALUES (?, ?, ?)",
            (username, full_name, role),
        )
        conn.commit()

    def get_user(self, username: str):
        """Fetch a user by username."""
        conn = self._get_connection()
        cur = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

    def record_audit(self, user_id: int, action: str, details: str = "", ip: str = None):
        """Record user actions in audit_log."""
        conn = self._get_connection()
        conn.execute(
            "INSERT INTO audit_log (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)",
            (user_id, action, details, ip),
        )
        conn.commit()

    def save_quiz_result(self, user_id: int, score: float):
        """Save quiz score for user."""
        conn = self._get_connection()
        conn.execute(
            "INSERT INTO training_progress (user_id, quiz_score, completed_at) VALUES (?, ?, ?)",
            (user_id, score, datetime.now()),
        )
        conn.commit()

    def close(self):
        """Close the SQLite connection safely."""
        if DatabaseManager.connection:
            DatabaseManager.connection.close()
            DatabaseManager.connection = None

