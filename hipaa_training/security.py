import logging
import os
import re
import base64
import sqlite3  # noqa: F401  # Used indirectly by DatabaseManager
from cryptography.fernet import Fernet


class SecurityManager:
    """
    Handles security, encryption, auditing, and input validation for HIPAA compliance.
    """

    def __init__(self):
        self.setup_logging()
        self.encryption_key = self._load_encryption_key()

    # ---------- Logging ---------- #
    def setup_logging(self):
        """Setup HIPAA-compliant audit logging"""
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)

        self.logger = logging.getLogger("hipaa_audit")
        self.logger.setLevel(logging.INFO)

        # Avoid duplicate handlers if reinitialized
        if not self.logger.handlers:
            file_handler = logging.FileHandler(os.path.join(log_dir, "hipaa_audit.log"))
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def log_action(self, user_id: int, action: str, details: str = ""):
        """Enhanced audit logging for HIPAA compliance"""
        self.logger.info(f"USER_{user_id} - {action} - {details}")

        # Example DB logging hook (optional)
        try:
            from .models import DatabaseManager
            db_path = os.path.join(os.path.dirname(__file__), "data", "hipaa_training.db")
            if os.path.exists(db_path):
                with DatabaseManager()._get_connection() as conn:
                    conn.execute(
                        """INSERT INTO audit_log (user_id, action, details)
                           VALUES (?, ?, ?)""",
                        (user_id, action, details),
                    )
        except Exception as e:
            self.logger.warning(f"DB log_action failed: {e}")

    # ---------- Encryption ---------- #
    def _load_encryption_key(self) -> bytes:
        """Load or generate encryption key from environment"""
        key_str = os.getenv("HIPAA_ENCRYPTION_KEY")

        try:
            if not key_str:
                key = Fernet.generate_key()
                os.environ["HIPAA_ENCRYPTION_KEY"] = key.decode()
                return key

            if len(key_str) != 44:  # Fernet key must be 32 bytes (base64 = 44 chars)
                key = base64.urlsafe_b64encode(key_str.encode("utf-8")[:32])
            else:
                key = key_str.encode("utf-8")

            # Validate the key
            Fernet(key)
            return key
        except Exception:
            # Fallback to a valid random key
            new_key = Fernet.generate_key()
            os.environ["HIPAA_ENCRYPTION_KEY"] = new_key.decode()
            return new_key

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data using Fernet symmetric encryption"""
        if not data:
            return ""
        f = Fernet(self.encryption_key)
        encrypted = f.encrypt(data.encode("utf-8"))
        return encrypted.decode("utf-8")

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data encrypted by encrypt_data()"""
        if not encrypted_data:
            return ""
        f = Fernet(self.encryption_key)
        try:
            decrypted = f.decrypt(encrypted_data.encode("utf-8"))
            return decrypted.decode("utf-8")
        except Exception:
            return ""

    # ---------- Input Sanitization ---------- #
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
            text = re.sub(r"[^a-zA-Z0-9\s\.\-_,!@]", "", text)
        else:
            text = re.sub(r"[^a-zA-Z0-9\.\-_@]", "", text)

        return text

