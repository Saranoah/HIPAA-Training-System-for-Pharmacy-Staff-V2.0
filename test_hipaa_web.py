#!/usr/bin/env python3
"""
Unit tests for HIPAA Training System
"""

import pytest
from app import app, USERS, LESSONS, QUIZ_QUESTIONS, CHECKLIST_ITEMS
from security_middleware import HIPAASecurity
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['HIPAA_SECURITY']['SESSION_TIMEOUT_MINUTES'] = 30
    with app.test_client() as client:
        yield client

@pytest.fixture
def hipaa_security():
    return HIPAASecurity(app)

def test_login_success(client, hipaa_security):
    response = client.post('/login', data={
        'username': 'pharmacist1',
        'password': 'secure123'
    })
    assert response.status_code == 302
    assert response.location.endswith('/')

def test_login_failed(client, hipaa_security):
    response = client.post('/login', data={
        'username': 'pharmacist1',
        'password': 'wrong'
    })
    assert response.status_code == 200
    assert b'Invalid credentials' in response.data

def test_brute_force_protection(client, hipaa_security):
    for _ in range(5):
        client.post('/login', data={
            'username': 'pharmacist1',
            'password': 'wrong'
        })
    response = client.post('/login', data={
        'username': 'pharmacist1',
        'password': 'secure123'
    })
    assert b'Too many failed attempts' in response.data

def test_session_timeout(client, hipaa_security):
    with client.session_transaction() as sess:
        sess['user_id'] = 'PHARMACIST_001'
        sess['user_role'] = 'Pharmacist'
        sess['facility'] = 'General Hospital Pharmacy'
        sess['last_activity'] = (datetime.now() - timedelta(minutes=31)).isoformat()
    
    response = client.get('/')
    assert response.status_code == 302
    assert response.location.endswith('/login')

def test_complete_lesson(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 'PHARMACIST_001'
        sess['user_role'] = 'Pharmacist'
        sess['last_activity'] = datetime.now().isoformat()
    
    response = client.post('/api/complete_lesson', json={
        'lesson_name': 'Privacy Rule Basics'
    })
    assert response.status_code == 200
    assert response.json['success'] == True

def test_quiz_submission(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 'PHARMACIST_001'
        sess['user_role'] = 'Pharmacist'
        sess['last_activity'] = datetime.now().isoformat()
    
    answers = {str(q['id']): q['answer'] for q in QUIZ_QUESTIONS}
    response = client.post('/api/submit_quiz', json={'answers': answers})
    assert response.status_code == 200
    assert response.json['score'] == 100
    assert response.json['passed'] == True

def test_checklist_update(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 'PHARMACIST_001'
        sess['user_role'] = 'Pharmacist'
        sess['last_activity'] = datetime.now().isoformat()
    
    response = client.post('/api/update_checklist', json={
        'item_id': 1,
        'completed': True
    })
    assert response.status_code == 200
    assert response.json['success'] == True

def test_mfa_setup(client, hipaa_security):
    with client.session_transaction() as sess:
        sess['user_id'] = 'PHARMACIST_001'
        sess['user_role'] = 'Pharmacist'
        sess['last_activity'] = datetime.now().isoformat()
    
    response = client.post('/mfa_setup')
    assert response.status_code == 200
    assert b'MFA QR Code' in response.data

def test_mfa_verify(client, hipaa_security):
    with client.session_transaction() as sess:
        sess['user_id'] = 'PHARMACIST_001'
        sess['user_role'] = 'Pharmacist'
        sess['last_activity'] = datetime.now().isoformat()
        sess['mfa_pending'] = 'PHARMACIST_001'
    
    # Mock MFA secret in database
    with hipaa_security._get_db_connection() as conn:
        secret = pyotp.random_base32()
        conn.execute('UPDATE users SET mfa_secret = %s WHERE user_id = %s', (secret, 'PHARMACIST_001'))
    
    totp = pyotp.TOTP(secret)
    response = client.post('/mfa_verify', data={'mfa_code': totp.now()})
    assert response.status_code == 302
    assert response.location.endswith('/')

def test_admin_audit_logs(client, hipaa_security):
    with client.session_transaction() as sess:
        sess['user_id'] = 'ADMIN_001'
        sess['user_role'] = 'Admin'
        sess['last_activity'] = datetime.now().isoformat()
    
    response = client.get('/admin/audit_logs')
    assert response.status_code == 200
    assert b'Audit Logs' in response.data
