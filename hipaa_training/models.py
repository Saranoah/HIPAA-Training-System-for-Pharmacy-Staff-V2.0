import sqlite3
import os
from contextlib import contextmanager


class DatabaseManager:
    """
    Manages database connections and schema with safe isolation.
    Uses SQLite for persistent local storage.
    """

    def __init__(self):
        # Use absolute path inside package
        self.db_path = os.path.join(os.path.dirname(__file__), "data", "hipaa_training.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize all required database tables if they don't exist."""
        with self._get_connection() as conn:
            # Users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Training progress table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS training_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    lesson_completed TEXT,
                    quiz_score REAL,
                    checklist_data TEXT,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)

            # Audit log table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
                )
            """)

            # Certificates table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS certificates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    certificate_id TEXT UNIQUE NOT NULL,
                    score REAL NOT NULL,
                    issue_date TIMESTAMP,
                    expiry_date TIMESTAMP,
                    revoked BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)
            """)

    @contextmanager
    def _get_connection(self):
        """Provide a safe, temporary database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
