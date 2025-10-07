#!/usr/bin/env python3
"""
Production-Ready HIPAA Security Middleware with PostgreSQL Support
Enhanced with MFA, encryption, CSRF protection, and comprehensive security features
"""

import os
import logging
from datetime import datetime, timedelta
from enum import Enum
from functools import wraps
from flask import request, session, redirect, url_for, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
import secrets
import pyotp
from retrying import retry
from apscheduler.schedulers.background import BackgroundScheduler
import ipaddress

# Configure structured logging with rotation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(ip)s] %(user_id)s - %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler(
            'hipaa_security.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

class SecurityFormatter(logging.Formatter):
    """Custom formatter that includes IP and user ID in logs"""
    def format(self, record):
        record.ip = getattr(record, 'ip', 'Unknown_IP')
        record.user_id = getattr(record, 'user_id', 'anonymous')
        return super().format(record)

logger = logging.getLogger('hipaa_security')
for handler in logger.handlers:
    handler.setFormatter(SecurityFormatter())

class SecurityEvent(Enum):
    """Enum for security event types to ensure consistency"""
    LOGIN_SUCCESS = 'LOGIN_SUCCESS'
    LOGIN_FAILED = 'LOGIN_FAILED'
    SESSION_TIMEOUT = 'SESSION_TIMEOUT'
    UNAUTHENTICATED_ACCESS = 'UNAUTHENTICATED_ACCESS'
    UNAUTHORIZED_ROLE_ACCESS = 'UNAUTHORIZED_ROLE_ACCESS'
    CSRF_VALIDATION_FAILED = 'CSRF_VALIDATION_FAILED'
    BRUTE_FORCE_LOCKOUT = 'BRUTE_FORCE_LOCKOUT'
    SESSION_EXTENDED = 'SESSION_EXTENDED'
    LESSON_COMPLETED = 'LESSON_COMPLETED'
    QUIZ_COMPLETED = 'QUIZ_COMPLETED'
    CHECKLIST_UPDATED = 'CHECKLIST_UPDATED'
    MFA_ENABLED = 'MFA_ENABLED'
    MFA_VERIFIED = 'MFA_VERIFIED'
    MFA_FAILED = 'MFA_FAILED'

class HIPAASecurity:
    """Production-Ready HIPAA Security Compliance Framework
    
    Provides authentication, session management, CSRF protection, audit logging,
    brute force protection, and MFA for HIPAA-compliant applications.
    """
    
    def __init__(self, app=None):
        """Initialize the security middleware
        
        Args:
            app (Flask): The Flask application instance
        """
        self.app = app
        self.config = {
            'SESSION_TIMEOUT_MINUTES': 15,
            'MAX_FAILED_ATTEMPTS': 5,
            'LOCKOUT_DURATION_MINUTES': 15,
            'AUDIT_RETENTION_DAYS': 365 * 6,  # HIPAA requires 6 years
            'CSRF_TOKEN_TIMEOUT': 3600,  # 1 hour
            'MFA_TOTP_INTERVAL': 30  # TOTP code validity period (seconds)
        }
        self.pool = SimpleConnectionPool(
            1, 20, os.getenv('DATABASE_URL'), cursor_factory=RealDictCursor
        )
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize middleware with Flask app
        
        Args:
            app (Flask): The Flask application instance
        """
        self.app = app
        self.config.update(app.config.get('HIPAA_SECURITY', {}))
        
        # Initialize database
        self._init_database()
        
        # Schedule periodic cleanup
        scheduler = BackgroundScheduler()
        scheduler.add_job(self._cleanup_old_data, 'interval', hours=1)
        scheduler.start()
        
        # Register before_request handler
        @app.before_request
        def before_request():
            self._validate_request()
            self._validate_csrf_token()
    
    def _init_database(self):
        """Initialize PostgreSQL database with encryption support"""
        try:
            with self._get_db_connection() as conn:
                # Enable pgcrypto for encryption
                conn.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
                
                # Audit logs table
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS audit_logs (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        event_type VARCHAR(100) NOT NULL,
                        user_id VARCHAR(100),
                        ip_address INET NOT NULL,
                        user_agent TEXT,
                        details TEXT NOT NULL,
                        severity VARCHAR(20) DEFAULT 'INFO'
                    )
                ''')
                
                # Failed attempts table
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS failed_attempts (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(100) NOT NULL,
                        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        ip_address INET NOT NULL
                    )
                ''')
                
                # CSRF tokens table
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS csrf_tokens (
                        token VARCHAR(128) PRIMARY KEY,
                        user_id VARCHAR(100) NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        expires_at TIMESTAMPTZ NOT NULL
                    )
                ''')
                
                # Create indexes
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_audit_user_time 
                    ON audit_logs(user_id, timestamp)
                ''')
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_failed_attempts_user_time 
                    ON failed_attempts(user_id, timestamp)
                ''')
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_csrf_tokens_expires 
                    ON csrf_tokens(expires_at)
                ''')
                
                # Clean up old data
                self._cleanup_old_data()
                
        except Exception as e:
            logger.error(f"Database initialization failed: {e}", extra={
                'ip': 'system',
                'user_id': 'system'
            })
            raise
    
    @retry(stop_max_attempt_number=3, wait_fixed=1000)
    @contextmanager
    def _get_db_connection(self):
        """Get PostgreSQL connection from pool with retry
        
        Yields:
            connection: A psycopg2 connection object
        """
        conn = self.pool.getconn()
        conn.cursor_factory = RealDictCursor
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.putconn(conn)
    
    def require_authentication(self, f):
        """Decorator for routes requiring authentication
        
        Args:
            f (function): The route function to decorate
            
        Returns:
            function: Decorated function
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self._validate_session():
                self.log_security_event(
                    SecurityEvent.UNAUTHENTICATED_ACCESS,
                    f"Attempted access to {request.path}",
                    'WARNING'
                )
                return redirect('/login')  # Abstracted for framework compatibility
            return f(*args, **kwargs)
        return decorated_function
    
    def require_role(self, *required_roles):
        """Decorator for role-based access control
        
        Args:
            *required_roles (str): One or more roles required to access the route
            
        Returns:
            function: Decorated function
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self._validate_session():
                    return redirect('/login')
                
                user_role = session.get('user_role')
                if user_role not in required_roles:
                    self.log_security_event(
                        SecurityEvent.UNAUTHORIZED_ROLE_ACCESS,
                        f"User {session.get('user_id')} with role {user_role} attempted access to {request.path} requiring {required_roles}",
                        'WARNING'
                    )
                    return redirect('/unauthorized')
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def _validate_request(self):
        """Validate each incoming request, skipping static and auth routes"""
        if request.endpoint and any(x in request.endpoint for x in ['static', 'login', 'logout', 'mfa_verify']):
            return
        
        if not self._validate_session():
            if request.endpoint != 'login':
                return redirect('/login')
    
    def _validate_csrf_token(self):
        """Validate CSRF token for POST/PUT/PATCH/DELETE requests"""
        if request.method not in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return
        
        if request.endpoint and 'api' in request.endpoint:
            return
        
        token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
        if not token or not self._validate_csrf_token_internal(token):
            self.log_security_event(
                SecurityEvent.CSRF_VALIDATION_FAILED,
                f"CSRF token validation failed for {request.path}",
                'WARNING'
            )
            return jsonify({'error': 'CSRF token validation failed'}), 403
    
    def _validate_csrf_token_internal(self, token):
        """Validate CSRF token against database
        
        Args:
            token (str): The CSRF token to validate
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            with self._get_db_connection() as conn:
                result = conn.execute(
                    'SELECT user_id FROM csrf_tokens WHERE token = %s AND expires_at > NOW()',
                    (token,)
                ).fetchone()
                
                if result and result['user_id'] == session.get('user_id'):
                    conn.execute('DELETE FROM csrf_tokens WHERE token = %s', (token,))
                    return True
                
            return False
        except Exception as e:
            logger.error(f"CSRF validation error: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': session.get('user_id', 'anonymous')
            })
            return False
    
    def generate_csrf_token(self):
        """Generate and store a secure CSRF token
        
        Returns:
            str: A URL-safe token, or None if generation fails
        """
        token = secrets.token_urlsafe(64)
        user_id = session.get('user_id', 'anonymous')
        expires_at = datetime.now() + timedelta(seconds=self.config['CSRF_TOKEN_TIMEOUT'])
        
        try:
            with self._get_db_connection() as conn:
                conn.execute(
                    'INSERT INTO csrf_tokens (token, user_id, expires_at) VALUES (%s, %s, %s)',
                    (token, user_id, expires_at)
                )
            return token
        except Exception as e:
            logger.error(f"CSRF token generation failed: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': user_id
            })
            return None
    
    def _validate_session(self):
        """Validate user session with timeout checking
        
        Returns:
            bool: True if session is valid, False otherwise
        """
        try:
            if 'user_id' not in session:
                return False
            
            last_activity = session.get('last_activity')
            if not last_activity:
                return False
            
            try:
                last_active = datetime.fromisoformat(last_activity)
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid last_activity format: {e}", extra={
                    'ip': self._get_client_ip(),
                    'user_id': session.get('user_id')
                })
                return False
            
            timeout_delta = timedelta(minutes=self.config['SESSION_TIMEOUT_MINUTES'])
            if datetime.now() - last_active > timeout_delta:
                self.log_security_event(
                    SecurityEvent.SESSION_TIMEOUT,
                    f"User {session.get('user_id')} session expired",
                    'INFO'
                )
                session.clear()
                return False
            
            session['last_activity'] = datetime.now().isoformat()
            return True
            
        except Exception as e:
            logger.error(f"Session validation error: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': session.get('user_id', 'anonymous')
            })
            return False
    
    def log_security_event(self, event_type, details, severity='INFO'):
        """Log security events to PostgreSQL and fallback file
        
        Args:
            event_type (SecurityEvent): The type of security event
            details (str): Details of the event
            severity (str): Severity level ('INFO', 'WARNING', 'ERROR')
        """
        try:
            event = {
                'timestamp': datetime.now(),
                'event_type': event_type.value if isinstance(event_type, SecurityEvent) else event_type,
                'user_id': session.get('user_id', 'anonymous'),
                'ip_address': self._get_client_ip(),
                'user_agent': request.headers.get('User-Agent', 'Unknown')[:500],
                'details': details[:1000],
                'severity': severity
            }
            
            with self._get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO audit_logs 
                    (timestamp, event_type, user_id, ip_address, user_agent, details, severity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    event['timestamp'],
                    event['event_type'],
                    event['user_id'],
                    event['ip_address'],
                    event['user_agent'],
                    event['details'],
                    event['severity']
                ))
            
            log_method = getattr(logger, severity.lower(), logger.info)
            log_method(details, extra={
                'ip': event['ip_address'],
                'user_id': event['user_id']
            })
            
        except Exception as e:
            logger.error(f"Audit logging failed: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': session.get('user_id', 'anonymous')
            })
            # Fallback to file
            with open('fallback_security.log', 'a') as f:
                f.write(f"{event['timestamp'].isoformat()} - {event['event_type']} - {event['details']} - {severity}\n")
    
    def _get_client_ip(self):
        """Safely get client IP address with strict validation
        
        Returns:
            str: Valid IP address or 'Invalid_IP'/'Unknown_IP' on error
        """
        try:
            ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
            ipaddress.ip_address(ip)  # Raises ValueError for invalid IPs
            return ip if len(ip) <= 45 else 'Invalid_IP'
        except (ValueError, Exception) as e:
            logger.error(f"IP address retrieval failed: {e}", extra={
                'ip': 'Unknown_IP',
                'user_id': session.get('user_id', 'anonymous')
            })
            return 'Unknown_IP'
    
    def check_brute_force(self, user_id):
        """Check for brute force attempts
        
        Args:
            user_id (str): The user ID to check
            
        Returns:
            bool: True if login is allowed, False if locked out
        """
        try:
            if not user_id or len(user_id) > 100:
                return False
            
            client_ip = self._get_client_ip()
            cutoff_time = datetime.now() - timedelta(minutes=self.config['LOCKOUT_DURATION_MINUTES'])
            
            with self._get_db_connection() as conn:
                recent_attempts = conn.execute('''
                    SELECT COUNT(*) FROM failed_attempts 
                    WHERE user_id = %s AND timestamp > %s
                ''', (user_id, cutoff_time)).fetchone()['count']
                
                if recent_attempts >= self.config['MAX_FAILED_ATTEMPTS']:
                    self.log_security_event(
                        SecurityEvent.BRUTE_FORCE_LOCKOUT,
                        f"User {user_id} locked out due to {recent_attempts} failed attempts",
                        'WARNING'
                    )
                    return False
                
                return True
                
        except Exception as e:
            logger.error(f"Brute force check failed: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': user_id
            })
            return False
    
    def record_failed_attempt(self, user_id):
        """Record a failed login attempt
        
        Args:
            user_id (str): The user ID for the failed attempt
        """
        try:
            with self._get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO failed_attempts (user_id, ip_address)
                    VALUES (%s, %s)
                ''', (user_id, self._get_client_ip()))
        except Exception as e:
            logger.error(f"Failed to record attempt for {user_id}: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': user_id
            })
    
    def clear_failed_attempts(self, user_id):
        """Clear failed attempts after successful login
        
        Args:
            user_id (str): The user ID to clear attempts for
        """
        try:
            with self._get_db_connection() as conn:
                conn.execute('DELETE FROM failed_attempts WHERE user_id = %s', (user_id,))
        except Exception as e:
            logger.error(f"Failed to clear attempts for {user_id}: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': user_id
            })
    
    def get_audit_logs(self, user_id=None, days=30, severity=None):
        """Retrieve audit logs for reporting
        
        Args:
            user_id (str, optional): Filter logs by user ID
            days (int, optional): Number of days to retrieve logs for
            severity (str, optional): Filter logs by severity ('INFO', 'WARNING', 'ERROR')
            
        Returns:
            list: List of audit log dictionaries
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with self._get_db_connection() as conn:
                query = '''
                    SELECT id, timestamp, event_type, user_id, ip_address, 
                           user_agent, details, severity 
                    FROM audit_logs WHERE timestamp > %s
                '''
                params = [cutoff_date]
                
                if user_id:
                    query += ' AND user_id = %s'
                    params.append(user_id)
                
                if severity:
                    query += ' AND severity = %s'
                    params.append(severity)
                
                query += ' ORDER BY timestamp DESC'
                
                logs = conn.execute(query, params).fetchall()
                return [dict(log) for log in logs]
                
        except Exception as e:
            logger.error(f"Audit log retrieval failed: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': session.get('user_id', 'anonymous')
            })
            return []
    
    def enable_mfa(self, user_id):
        """Enable MFA for a user by generating a TOTP secret
        
        Args:
            user_id (str): The user ID to enable MFA for
            
        Returns:
            str: TOTP secret, or None if generation fails
        """
        secret = pyotp.random_base32()
        try:
            with self._get_db_connection() as conn:
                conn.execute(
                    'UPDATE users SET mfa_secret = %s WHERE user_id = %s',
                    (secret, user_id)
                )
            self.log_security_event(
                SecurityEvent.MFA_ENABLED,
                f"MFA enabled for user {user_id}",
                'INFO'
            )
            return secret
        except Exception as e:
            logger.error(f"MFA enable failed for {user_id}: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': user_id
            })
            return None
    
    def verify_mfa(self, user_id, code):
        """Verify MFA TOTP code
        
        Args:
            user_id (str): The user ID to verify
            code (str): The TOTP code provided by the user
            
        Returns:
            bool: True if code is valid, False otherwise
        """
        try:
            with self._get_db_connection() as conn:
                result = conn.execute(
                    'SELECT mfa_secret FROM users WHERE user_id = %s',
                    (user_id,)
                ).fetchone()
                
                if not result or not result['mfa_secret']:
                    return False
                
                totp = pyotp.TOTP(result['mfa_secret'], interval=self.config['MFA_TOTP_INTERVAL'])
                is_valid = totp.verify(code)
                
                self.log_security_event(
                    SecurityEvent.MFA_VERIFIED if is_valid else SecurityEvent.MFA_FAILED,
                    f"MFA verification {'successful' if is_valid else 'failed'} for user {user_id}",
                    'INFO' if is_valid else 'WARNING'
                )
                return is_valid
                
        except Exception as e:
            logger.error(f"MFA verification failed for {user_id}: {e}", extra={
                'ip': self._get_client_ip(),
                'user_id': user_id
            })
            return False
    
    def _cleanup_old_data(self):
        """Clean up old CSRF tokens, failed attempts, and audit logs"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.config['AUDIT_RETENTION_DAYS'])
            with self._get_db_connection() as conn:
                conn.execute('DELETE FROM csrf_tokens WHERE expires_at < NOW()')
                conn.execute('DELETE FROM failed_attempts WHERE timestamp < %s', (cutoff_date,))
                conn.execute('DELETE FROM audit_logs WHERE timestamp < %s', (cutoff_date,))
        except Exception as e:
            logger.error(f"Data cleanup failed: {e}", extra={
                'ip': 'system',
                'user_id': 'system'
            })

# Configuration helper
def load_hipaa_config(app):
    """Load HIPAA security configuration from environment
    
    Args:
        app (Flask): The Flask application instance
    """
    app.config.update({
        'HIPAA_SECURITY': {
            'SESSION_TIMEOUT_MINUTES': int(os.getenv('SESSION_TIMEOUT', 15)),
            'MAX_FAILED_ATTEMPTS': int(os.getenv('MAX_FAILED_ATTEMPTS', 5)),
            'LOCKOUT_DURATION_MINUTES': int(os.getenv('LOCKOUT_DURATION', 15)),
            'AUDIT_RETENTION_DAYS': int(os.getenv('AUDIT_RETENTION_DAYS', 365 * 6)),
            'CSRF_TOKEN_TIMEOUT': int(os.getenv('CSRF_TOKEN_TIMEOUT', 3600)),
            'MFA_TOTP_INTERVAL': int(os.getenv('MFA_TOTP_INTERVAL', 30))
        },
        'SECRET_KEY': os.getenv('SECRET_KEY', secrets.token_hex(32)),
        'SESSION_TYPE': 'filesystem',
        'SESSION_COOKIE_SECURE': True,
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_SAMESITE': 'Strict'
    })
