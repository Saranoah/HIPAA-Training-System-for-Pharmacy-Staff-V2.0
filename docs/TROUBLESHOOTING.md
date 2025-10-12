# HIPAA Training System V3.0 - Troubleshooting Guide

Common issues and solutions for the HIPAA Training System.

---

## 🔴 Installation Issues

### Error: "No module named 'hipaa_training'"

**Cause:** Python can't find the package.

**Solution:**
```bash
# Make sure you're in the project root directory
cd /path/to/hipaa-training-v3

# Verify directory structure
ls hipaa_training/

# Run from correct location
python main.py
Error: "HIPAA_ENCRYPTION_KEY environment variable must be set"
Cause: Required encryption key not configured.

Solution:

bash
Copy code
# Generate a secure key
python -c 'import secrets; print(secrets.token_urlsafe(32))'

# Set in environment (Linux/macOS)
export HIPAA_ENCRYPTION_KEY='your-generated-key-here'

# Set in environment (Windows)
set HIPAA_ENCRYPTION_KEY=your-generated-key-here

# OR add to .env file
echo 'HIPAA_ENCRYPTION_KEY="your-generated-key-here"' >> .env
Error: "ModuleNotFoundError: No module named 'cryptography'"
Cause: Dependencies not installed.

Solution:

bash
Copy code
# Install all dependencies
pip install -r requirements.txt

# If that fails, install individually
pip install cryptography rich pytest pytest-cov
Error: "Permission denied" when creating directories
Cause: Insufficient permissions.

Solution:

bash
Copy code
# Linux/macOS - change ownership
sudo chown -R $USER:$USER .

# Or run with proper permissions
chmod 755 .
python main.py --setup-only
🔴 Runtime Errors
Error: "Database is locked"
Cause: Another process is accessing the database or improper shutdown.

Solution:

bash
Copy code
# Check for running processes
ps aux | grep python

# Kill any hanging processes
kill -9 <process_id>

# If persistent, remove lock file
rm data/hipaa_training.db-shm
rm data/hipaa_training.db-wal

# Restart application
python main.py
Error: "Failed to decrypt data"
Cause: Encryption key changed or data corrupted.

Solutions:

If key was changed:

bash
Copy code
# Restore original HIPAA_ENCRYPTION_KEY
# Check .env file or environment variables

# If key is lost, data cannot be recovered
# You'll need to reinitialize
rm data/hipaa_training.db
python main.py --setup-only
If data is corrupted:

bash
Copy code
# Restore from backup
cp backups/hipaa_training_YYYYMMDD_HHMMSS.db.gz .
gunzip hipaa_training_YYYYMMDD_HHMMSS.db.gz
mv hipaa_training_YYYYMMDD_HHMMSS.db data/hipaa_training.db
Error: "Invalid user ID"
Cause: User doesn't exist in database.

Solution:

bash
Copy code
# List all users
sqlite3 data/hipaa_training.db "SELECT * FROM users;"

# Create a new user
python main.py
# Select option 1: Create New User
Quiz shows incorrect answers as correct (or vice versa)
Cause: Old version with randomization bug.

Solution:

bash
Copy code
# Update to latest version
git pull origin main

# Or replace training_engine.py with fixed version
# Make sure this line exists in _mini_quiz and adaptive_quiz:
# options = q['options'].copy()  # Must have .copy()!
🔴 Test Failures
Error: "No module named 'conftest'"
Cause: Missing pytest configuration file.

Solution:

bash
Copy code
# Create tests/conftest.py
cat > tests/conftest.py << 'EOF'
import pytest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ['HIPAA_ENCRYPTION_KEY'] = 'test-key-32-chars'
os.environ['HIPAA_SALT'] = 'test-salt-hex'
EOF

# Run tests again
pytest tests/ -v
Error: "fixture 'security_manager' not found"
Cause: Test file missing proper imports or fixtures.

Solution:

python
Copy code
# Add to top of test file
import pytest
from unittest.mock import patch

@pytest.fixture
def security_manager():
    with patch.dict('os.environ', {
        'HIPAA_ENCRYPTION_KEY': 'test-key-32-chars',
        'HIPAA_SALT': 'test-salt-hex'
    }):
        from hipaa_training.security import SecurityManager
        return SecurityManager()
Tests pass locally but fail in CI/CD
Cause: Environment differences.

Solution:

yaml
Copy code
# Check .github/workflows/ci.yml has:
env:
  HIPAA_ENCRYPTION_KEY: test-key-for-ci
  HIPAA_SALT: test-salt-12345678

# Ensure Python version matches
python-version: ['3.9', '3.10', '3.11', '3.12']
🔴 Content Issues
Error: "Lesson 'X' not found"
Cause: Content files missing or corrupted.

Solution:

bash
Copy code
# Check if files exist
ls -la content/

# Validate JSON syntax
python -m json.tool content/lessons.json

# If invalid, restore from backup or let system recreate
rm content/lessons.json
python main.py  # Will create default content
Content files have wrong encoding
Cause: Non-UTF-8 characters.

Solution:

bash
Copy code
# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 content/lessons.json > content/lessons_utf8.json
mv content/lessons_utf8.json content/lessons.json
🔴 Performance Issues
Database queries are slow
Cause: Missing indexes or large dataset.

Solution:

bash
Copy code
# Check if indexes exist
sqlite3 data/hipaa_training.db ".schema"

# Should see indexes like idx_user_id, idx_cert_user, etc.

# If missing, recreate database
python main.py --setup-only

# Or manually add indexes
sqlite3 data/hipaa_training.db "CREATE INDEX idx_user_id ON training_progress(user_id);"
Application freezes during file encryption
Cause: Large files being encrypted in memory.

Solution:

python
Copy code
# Check training_engine.py uses chunked encryption
# Should call security.encrypt_file() not cipher.encrypt()

# Verify in training_engine.py:
self.security.encrypt_file(evidence_path, dest_path)
# NOT: encrypted = self.security.cipher.encrypt(file_data)
🔴 Logging Issues
No audit logs being created
Cause: Logs directory doesn't exist or permissions issue.

Solution:

bash
Copy code
# Create logs directory
mkdir -p logs
chmod 700 logs

# Restart application
python main.py
Log files growing too large
Cause: Log rotation not working.

Solution:

python
Copy code
# Check security.py has RotatingFileHandler
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/hipaa_audit.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
🔴 Security Issues
Warning: "Using random salt - decryption may fail"
Cause: HIPAA_SALT not set in environment.

Solution:

bash
Copy code
# Generate and set salt
python -c 'import secrets; print(secrets.token_hex(16))'

# Add to .env
echo 'HIPAA_SALT="generated-salt-here"' >> .env

# Or export
export HIPAA_SALT='generated-salt-here'
Evidence files can't be decrypted
Cause: Salt or key changed since encryption.

Solution:

bash
Copy code
# You MUST use the same HIPAA_ENCRYPTION_KEY and HIPAA_SALT
# that were used during encryption

# If keys are lost, encrypted files cannot be recovered
# Restore from unencrypted backup if available
🔴 Backup/Restore Issues
Backup script fails: "sqlite3: command not found"
Cause: SQLite3 CLI not installed.

Solution:

bash
Copy code
# Install SQLite3
# Ubuntu/Debian
sudo apt-get install sqlite3

# macOS
brew install sqlite3

# Windows
# Download from https://www.sqlite.org/download.html

# Or use Python fallback in backup script
python -c "import sqlite3; import shutil; shutil.copy('data/hipaa_training.db', 'backups/manual_backup.db')"
Restore fails: "database disk image is malformed"
Cause: Corrupted backup file.

Solution:

bash
Copy code
# Try to repair database
sqlite3 data/hipaa_training.db ".recover" | sqlite3 recovered.db

# If that fails, restore from earlier backup
ls -lt backups/

# Use an older backup
gunzip -c backups/hipaa_training_YYYYMMDD_HHMMSS.db.gz > data/hipaa_training.db
Automated backups not running
Cause: Cron job not set up or incorrect path.

Solution:

bash
Copy code
# Check cron jobs
crontab -l

# Add cron job (run daily at 2 AM)
crontab -e

# Add this line:
0 2 * * * /full/path/to/scripts/backup_database.sh >> /var/log/hipaa_backup.log 2>&1

# Make script executable
chmod +x scripts/backup_database.sh

# Test manually
./scripts/backup_database.sh
🔴 Certificate Issues
Certificate not being issued after passing quiz
Cause: Score calculation error or database issue.

Solution:

bash
Copy code
# Check quiz score in database
sqlite3 data/hipaa_training.db "SELECT user_id, quiz_score FROM training_progress WHERE quiz_score IS NOT NULL;"

# Manually issue certificate if score is valid
sqlite3 data/hipaa_training.db << EOF
INSERT INTO certificates (user_id, certificate_id, score, issue_date, expiry_date)
VALUES (1, 'manual-cert-$(uuidgen)', 85.0, datetime('now'), datetime('now', '+365 days'));
EOF
Certificate expired but training still valid
Cause: System clock issue or training completed >365 days ago.

Solution:

bash
Copy code
# Check certificate expiry
sqlite3 data/hipaa_training.db "SELECT certificate_id, issue_date, expiry_date FROM certificates WHERE user_id = 1;"

# If training is still valid, extend certificate
sqlite3 data/hipaa_training.db "UPDATE certificates SET expiry_date = datetime('now', '+365 days') WHERE certificate_id = 'YOUR-CERT-ID';"

# Or issue new certificate
# User must retake training
🔴 Docker Issues
Docker build fails: "No such file or directory"
Cause: Missing files or incorrect context.

Solution:

bash
Copy code
# Make sure you're in project root
ls Dockerfile

# Build with proper context
docker build -t hipaa-training:v3 .

# If still fails, check .dockerignore
cat .dockerignore
Container exits immediately
Cause: Missing environment variables.

Solution:

bash
Copy code
# Run with required env vars
docker run -it --rm \
  -e HIPAA_ENCRYPTION_KEY="your-key-here" \
  -e HIPAA_SALT="your-salt-here" \
  hipaa-training:v3

# Or use docker-compose with .env file
docker-compose up
Can't access database in container
Cause: Volume not mounted.

Solution:

bash
Copy code
# Mount data directory as volume
docker run -it --rm \
  -e HIPAA_ENCRYPTION_KEY="your-key" \
  -e HIPAA_SALT="your-salt" \
  -v $(pwd)/data:/app/data \
  hipaa-training:v3
🔴 Import Errors
Error: "cannot import name 'X' from 'hipaa_training'"
Cause: Missing import in init.py or circular import.

Solution:

python
Copy code
# Check hipaa_training/__init__.py has all exports
__all__ = [
    'CLI',
    'DatabaseManager',
    'UserManager',
    'ComplianceDashboard',
    'SecurityManager',
    'EnhancedTrainingEngine',
    'ContentManager'
]

# Verify import order (avoid circular imports)
# In __init__.py, import in this order:
from .security import SecurityManager
from .models import DatabaseManager, UserManager, ComplianceDashboard
from .content_manager import ContentManager
from .training_engine import EnhancedTrainingEngine
from .cli import CLI
🔴 Platform-Specific Issues
Windows: "OSError: [WinError 123] The filename, directory name, or volume label syntax is incorrect"
Cause: Path separator issues.

Solution:

python
Copy code
# Use os.path.join instead of manual path construction
import os
filepath = os.path.join('data', 'hipaa_training.db')

# Or use pathlib
from pathlib import Path
filepath = Path('data') / 'hipaa_training.db'
Windows: chmod not working
Cause: chmod is Unix-only.

Solution:

python
Copy code
# Already fixed in main.py - checks platform
import platform
if platform.system() != 'Windows':
    os.chmod(directory, 0o700)
macOS: "Operation not permitted"
Cause: macOS security restrictions.

Solution:

bash
Copy code
# Grant terminal full disk access
# System Preferences > Security & Privacy > Privacy > Full Disk Access
# Add Terminal.app

# Or run from user directory
cd ~/Documents/hipaa-training-v3
python main.py
🔴 CI/CD Issues
GitHub Actions: "Authentication failed"
Cause: Missing or expired GitHub secrets.

Solution:

bash
Copy code
# Add secrets in GitHub repository
# Settings > Secrets and variables > Actions > New repository secret

# Required secrets:
# - DOCKER_USERNAME
# - DOCKER_PASSWORD
# - CODECOV_TOKEN (optional)
CI tests pass but fail on main
Cause: Branch protection or merge conflicts.

Solution:

bash
Copy code
# Update your branch
git checkout main
git pull origin main

# Rebase your changes
git checkout your-branch
git rebase main

# Fix conflicts if any
git add .
git rebase --continue

# Push
git push --force-with-lease
🔴 Common Usage Errors
"Cannot create user with special characters"
Cause: Input sanitization removing characters.

Solution:
Special characters are preserved in names like "O'Brien" or "José"
Truly dangerous characters (HTML/script tags) are escaped
If legitimate character is removed, file a bug report

Training progress not saving
Cause: Database connection issue or improper shutdown.

Solution:

bash
Copy code
# Check database integrity
sqlite3 data/hipaa_training.db "PRAGMA integrity_check;"

# Check logs for errors
tail -f logs/hipaa_audit.log

# Verify progress is being recorded
sqlite3 data/hipaa_training.db "SELECT * FROM training_progress ORDER BY completed_at DESC LIMIT 5;"
🛠️ Debug Mode
Enable debug mode for verbose output:

bash
Copy code
# Run with debug flag
python main.py --debug

# Or set environment variable
export DEBUG=true
python main.py
📊 Health Check
Run the health check script to diagnose issues:

bash
Copy code
python scripts/health_check.py
Checks:

✅ Database integrity

✅ Content files

✅ Directory structure

✅ Environment variables

✅ Dependencies

✅ Audit logs

🔍 Collecting Diagnostic Information
bash
Copy code
# System information
python --version
pip list | grep -E "cryptography|rich|pytest"
uname -a  # Linux/macOS
systeminfo  # Windows

# Check database
sqlite3 data/hipaa_training.db ".schema"

# Check logs
tail -n 100 logs/hipaa_audit.log

# Run health check
python scripts/health_check.py > health_check_output.txt

# Run tests with verbose output
pytest tests/ -v --tb=long > test_output.txt 2>&1
📞 Getting Help
If none of these solutions work:

Check GitHub Issues: https://github.com/Saranoah/HIPAA-Training-System-for-Pharmacy-Staff-V3.0/issues

Create New Issue: Include:

Python version

Operating system

Complete error message

Output from python scripts/health_check.py

Steps to reproduce

Review Documentation:

README.md

SETUP_GUIDE.md

API.md

🚑 Emergency Recovery
bash
Copy code
# 1. Backup everything
mkdir emergency_backup
cp -r data/ evidence/ logs/ emergency_backup/

# 2. Clean install
rm -rf hipaa_training/__pycache__
rm -rf data/hipaa_training.db
rm -rf logs/*

# 3. Reinstall dependencies
pip uninstall -y cryptography rich pytest
pip install -r requirements.txt

# 4. Reinitialize
python main.py --setup-only

# 5. Restore data from backup
cp emergency_backup/data/hipaa_training.db data/

# 6. Verify
python scripts/health_check.py
📝 Known Issues
Evidence files over 5MB rejected
Status: By design
Workaround: Compress files or split into smaller chunks

No web interface
Status: Planned for V4.0
Workaround: Use CLI for now

Email notifications not sent
Status: Not implemented
Workaround: Monitor logs manually or implement custom notification

✅ Preventive Measures
Regular Backups

bash
Copy code
# Set up automated daily backups
crontab -e
0 2 * * * /path/to/scripts/backup_database.sh
Monitor Logs

bash
Copy code
# Check logs weekly
tail -f logs/hipaa_audit.log
Test Restores

bash
Copy code
# Test backup restore monthly
./scripts/backup_database.sh
# Then restore to test environment
Keep Updated

bash
Copy code
git pull origin main
pip install -r requirements.txt --upgrade
Regular Health Checks

bash
Copy code
# Run weekly
python scripts/health_check.py
📚 Additional Resources
HIPAA Guidance: https://www.hhs.gov/hipaa

Python Documentation: https://docs.python.org/3/

SQLite Documentation: https://www.sqlite.org/docs.html

Cryptography Library: https://cryptography.io/

Last Updated: 2025-01-11
Version: 3.0.1

Still having issues? Create a GitHub issue with detailed information!
