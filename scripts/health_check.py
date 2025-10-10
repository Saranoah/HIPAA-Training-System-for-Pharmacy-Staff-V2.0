#!/usr/bin/env python3
"""
HIPAA Training System - Health Check Script
Run this script to verify system health and compliance status
"""

import os
import sqlite3
import json
from datetime import datetime
from pathlib import Path

def health_check():
    """Comprehensive system health check"""
    checks = {}
    
    print("🏥 HIPAA Training System - Health Check")
    print("=" * 50)
    
    # Check database
    try:
        conn = sqlite3.connect('data/hipaa_training.db')
        integrity = conn.execute('PRAGMA integrity_check').fetchone()[0]
        checks['database'] = integrity == 'ok'
        print(f"📊 Database: {'✅ OK' if checks['database'] else '❌ CORRUPTED'}")
        
        # Check user count
        user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        print(f"   Users: {user_count}")
        
        # Check training completion
        training_count = conn.execute('SELECT COUNT(*) FROM training_progress WHERE quiz_score IS NOT NULL').fetchone()[0]
        print(f"   Training Sessions: {training_count}")
        
        conn.close()
    except Exception as e:
        checks['database'] = False
        print(f"📊 Database: ❌ ERROR - {e}")
    
    # Check content files
    content_files = ['lessons.json', 'quiz_questions.json', 'checklist_items.json']
    checks['content'] = all(Path(f'content/{f}').exists() for f in content_files)
    print(f"📚 Content Files: {'✅ OK' if checks['content'] else '❌ MISSING'}")
    
    # Check directories
    directories = ['certificates', 'reports', 'evidence', 'data']
    for directory in directories:
        exists = Path(directory).exists()
        print(f"📁 {directory}/: {'✅ EXISTS' if exists else '❌ MISSING'}")
    
    # Check encryption key
    encryption_key = os.getenv('HIPAA_ENCRYPTION_KEY')
    checks['encryption'] = bool(encryption_key and len(encryption_key) >= 32)
    print(f"🔐 Encryption Key: {'✅ SET' if checks['encryption'] else '❌ MISSING/INSECURE'}")
    
    # Check audit log
    audit_log_exists = Path('hipaa_audit.log').exists()
    print(f"📋 Audit Log: {'✅ EXISTS' if audit_log_exists else '❌ MISSING'}")
    
    # Overall status
    all_checks_passed = all(checks.values())
    print("\n" + "=" * 50)
    print(f"Overall Status: {'✅ HEALTHY' if all_checks_passed else '❌ NEEDS ATTENTION'}")
    
    return all_checks_passed

if __name__ == '__main__':
    try:
        health_check()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
