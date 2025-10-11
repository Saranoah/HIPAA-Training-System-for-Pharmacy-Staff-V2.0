import pytest
from hipaa_training.security import SecurityManager
from unittest.mock import patch, mock_open
import base64
from cryptography.fernet import Fernet

@pytest.fixture
def security_manager():
    with patch('os.getenv') as mock_getenv:
        mock_getenv.side_effect = lambda key, default=None: 'test-key-32-characters-long-enough' if key == 'HIPAA_ENCRYPTION_KEY' else default
        return SecurityManager()

def test_encrypt_decrypt_round_trip(security_manager):
    """Test that encryption and decryption work correctly"""
    original_data = "Sensitive HIPAA compliance data"
    
    encrypted = security_manager.encrypt_data(original_data)
    decrypted = security_manager.decrypt_data(encrypted)
    
    assert decrypted == original_data
    assert encrypted != original_data
    assert isinstance(encrypted, str)

def test_encrypt_empty_string(security_manager):
    """Test encryption handles empty strings"""
    result = security_manager.encrypt_data("")
    assert result == ""

def test_decrypt_empty_string(security_manager):
    """Test decryption handles empty strings"""
    result = security_manager.decrypt_data("")
    assert result == ""

def test_log_action(security_manager):
    """Test audit logging functionality"""
    with patch('logging.Logger.info') as mock_log:
        security_manager.log_action(123, "TEST_ACTION", "Test details for audit")
        
        mock_log.assert_called_once()
        call_args = mock_log.call_args[0][0]
        assert "USER_123" in call_args
        assert "TEST_ACTION" in call_args
        assert "Test details for audit" in call_args

def test_encryption_with_special_characters(security_manager):
    """Test encryption handles special characters"""
    test_data = 'Special chars: ñáéíóú 测试 🚀'
    encrypted = security_manager.encrypt_data(test_data)
    decrypted = security_manager.decrypt_data(encrypted)
    assert decrypted == test_data
