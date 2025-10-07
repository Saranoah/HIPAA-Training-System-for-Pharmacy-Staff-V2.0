#!/usr/bin/env python3
"""
Configuration for HIPAA Training System
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    HIPAA_SECURITY = {
        'SESSION_TIMEOUT_MINUTES': int(os.getenv('SESSION_TIMEOUT', 15)),
        'MAX_FAILED_ATTEMPTS': int(os.getenv('MAX_FAILED_ATTEMPTS', 5)),
        'LOCKOUT_DURATION_MINUTES': int(os.getenv('LOCKOUT_DURATION', 15)),
        'AUDIT_RETENTION_DAYS': int(os.getenv('AUDIT_RETENTION_DAYS', 365 * 6)),
        'CSRF_TOKEN_TIMEOUT': int(os.getenv('CSRF_TOKEN_TIMEOUT', 3600))
    }
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/hipaa_training')
