import os
import pytest
from hipaa_training.security import SecurityManager
from hipaa_training.models import DatabaseManager
from hipaa_training.content_manager import ContentManager


def test_encryption_cycle():
    sec = SecurityManager()
    text = "HIPAA"
    encrypted = sec.encrypt_data(text)
    decrypted = sec.decrypt_data(encrypted)
    assert decrypted == text


def test_database_initialization(tmp_path):
    db_path = tmp_path / "test.db"
    DatabaseManager.db_path = str(db_path)
    db = DatabaseManager()
    assert os.path.exists(db_path)


def test_content_manager_fallback():
    cm = ContentManager()
    assert isinstance(cm.lessons, dict)
    assert "Sample Lesson" in cm.lessons


def test_sanitize_input():
    sec = SecurityManager()
    dirty = "<script>alert('x')</script>"
    clean = sec.sanitize_input(dirty)
    assert "<" not in clean and ">" not in clean
