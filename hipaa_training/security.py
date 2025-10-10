# hipaa_training/security.py
import os
import logging
import base64
import secrets
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .models import Config

class SecurityManager:
    def __init__(self):
        self.setup_logging()
        self._setup_encryption()

    def setup_logging(self):
        """Configure logging for audit trail"""
        logging.basicConfig(
            filename='hipaa_audit.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - USER_%(user_id)s - %(action)s - %(message)s'
        )
        self.logger = logging.getLogger('HIPAA_Audit')

    def _setup_encryption(self):
        """Setup encryption with random salt"""
        encryption_key = Config.ENCRYPTION_KEY.encode()
        # In production, store salt securely
        salt = os.getenv('HIPAA_SALT', secrets.token_bytes(16)).encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(encryption_key))
        self.cipher = Fernet(key)

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        if not data:
            return data
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data:
            return encrypted_data
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def log_action(self, user_id: int, action: str, details: str):
        """Log an action for audit trail"""
        ip_address = '127.0.0.1'  # Replace with dynamic IP in production
        self.logger.info(details, extra={'user_id': user_id, 'action': action})
        with sqlite3.connect(Config.DB_PATH) as conn:
            conn.execute(
                "INSERT INTO audit_log (user_id, action, details, timestamp, ip_address) "
                "VALUES (?, ?, ?, ?, ?)",
                (user_id, action, details, datetime.now(), ip_address)
            )
            conn.commit()
