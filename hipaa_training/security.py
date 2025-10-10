import logging
import os
import re
from datetime import datetime


class SecurityManager:
    """
    Handles security, auditing, and input validation for HIPAA.
    """

    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Setup HIPAA-compliant audit logging"""
        os.makedirs("logs", exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/hipaa_audit.log'),
                logging.StreamHandler()
            ]
        )

    def log_action(
        self, user_id: int, action: str, details: str = ""
    ):
        """Enhanced audit logging for HIPAA compliance"""
        log_entry = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }

        logging.info(f"USER_{user_id} - {action} - {details}")

        # Store in database
        from .models import DatabaseManager
        with DatabaseManager()._get_connection() as conn:
            conn.execute(
                """INSERT INTO audit_log
                   (user_id, action, details)
                   VALUES (?, ?, ?)""",
                (user_id, action, details)
            )

    def sanitize_input(
        self,
        text: str,
        max_length: int = 255,
        allow_spaces: bool = True
    ) -> str:
        """Sanitize user input to prevent injection attacks"""
        if not text:
            return text

        text = str(text).strip()
        if len(text) > max_length:
            text = text[:max_length]

        # Allow only alphanumeric, spaces, and basic punctuation
        if allow_spaces:
            text = re.sub(r'[^a-zA-Z0-9\s\.\-_,!@]', '', text)
        else:
            text = re.sub(r'[^a-zA-Z0-9\.\-_@]', '', text)

        return text
