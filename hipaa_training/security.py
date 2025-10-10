import base64
from cryptography.fernet import Fernet


class SecurityManager:
    """Handles encryption and security utilities for HIPAA compliance."""

    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()
        if isinstance(key, str):
            key = key.encode()
        self.key = key
        self.cipher = Fernet(self.key)

    def encrypt_data(self, data: str) -> str:
        """Encrypt text using Fernet symmetric encryption."""
        if not data:
            return ""
        token = self.cipher.encrypt(data.encode())
        return token.decode()

    def decrypt_data(self, token: str) -> str:
        """Decrypt text encrypted with Fernet."""
        if not token:
            return ""
        try:
            decrypted = self.cipher.decrypt(token.encode())
            return decrypted.decode()
        except Exception:
            return ""

    def get_key(self) -> str:
        """Return the current encryption key (base64 encoded)."""
        return base64.urlsafe_b64encode(self.key).decode()
