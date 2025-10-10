import logging
import os
import re
import base64
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
        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger("hipaa_audit")
        self.logger.setLevel(logging.INFO)

        # Avoid duplicate handlers if reinitialized
        if not self.logger.handlers:
            file_handler = logging.FileHandler("logs/hipaa_audit.log")
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
        if not key_str:
            key = Fernet.generate_key()
            os.environ["HIPAA_ENCRYPTION_KEY"] = key.decode()
            return key

        # Ensure it’s a valid 32-byte base64 key
        try:
            # If the key provided in env isn’t base64, encode it
            if len(key_str) != 44:  # 32-byte key encoded in base64 = 44 chars
                key = base64.urlsafe_b64encode(key_str.encode("utf-8")[:32])
            else:
                key = key_str.encode("utf-8")
            # Validate
            Fernet(key)
            return key
        except Exception:
            # Fall back to a valid key
            return Fernet.generate_key()

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
