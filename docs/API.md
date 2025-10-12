```bash
# Install SQLite3
# Ubuntu/Debian
sudo apt-get install sqlite3

# macOS
brew install sqlite3

# Windows
# Download from https://www.sqlite.org/download.html

# Or use Python fallback in backup script
python -c "import sqlite3; import shutil; shutil.copy('data/hipaa_training.db', 'backups/manual_backup.db')"
```

---

### Restore fails: "database disk image is malformed"

**Cause:** Corrupted backup file.

**Solution:**
```bash
# Try to repair database
sqlite3 data/hipaa_training.db ".recover" | sqlite3 recovered.db

# If that fails, restore from earlier backup
ls -lt backups/

# Use an older backup
gunzip -c backups/hipaa_training_YYYYMMDD_HHMMSS.db.gz > data/hipaa_training.db
```

---

### Automated backups not running

**Cause:** Cron job not set up or incorrect path.

**Solution:**
```bash
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
```

---

## 🔴 Certificate Issues

### Certificate not being issued after passing quiz

**Cause:** Score calculation error or database issue.

**Solution:**
```bash
# Check quiz score in database
sqlite3 data/hipaa_training.db "SELECT user_id, quiz_score FROM training_progress WHERE quiz_score IS NOT NULL;"

# Manually issue certificate if score is valid
sqlite3 data/hipaa_training.db << EOF
INSERT INTO certificates (user_id, certificate_id, score, issue_date, expiry_date)
VALUES (1, 'manual-cert-$(uuidgen)', 85.0, datetime('now'), datetime('now', '+365 days'));
EOF
```

---

### Certificate expired but training still valid

**Cause:** System clock issue or training completed >365 days ago.

**Solution:**
```bash
# Check certificate expiry
sqlite3 data/hipaa_training.db "SELECT certificate_id, issue_date, expiry_date FROM certificates WHERE user_id = 1;"

# If training is still valid, extend certificate
sqlite3 data/hipaa_training.db "UPDATE certificates SET expiry_date = datetime('now', '+365 days') WHERE certificate_id = 'YOUR-CERT-ID';"

# Or issue new certificate
# User must retake training
```

---

## 🔴 Docker Issues

### Docker build fails: "No such file or directory"

**Cause:** Missing files or incorrect context.

**Solution:**
```bash
# Make sure you're in project root
ls Dockerfile

# Build with proper context
docker build -t hipaa-training:v3 .

# If still fails, check .dockerignore
cat .dockerignore
```

---

### Container exits immediately

**Cause:** Missing environment variables.

**Solution:**
```bash
# Run with required env vars
docker run -it --rm \
  -e HIPAA_ENCRYPTION_KEY="your-key-here" \
  -e HIPAA_SALT="your-salt-here" \
  hipaa-training:v3

# Or use docker-compose with .env file
docker-compose up
```

---

### Can't access database in container

**Cause:** Volume not mounted.

**Solution:**
```bash
# Mount data directory as volume
docker run -it --rm \
  -e HIPAA_ENCRYPTION_KEY="your-key" \
  -e HIPAA_SALT="your-salt" \
  -v $(pwd)/data:/app/data \
  hipaa-training:v3
```

---

## 🔴 Import Errors

### Error: "cannot import name 'X' from 'hipaa_training'"

**Cause:** Missing import in `__init__.py` or circular import.

**Solution:**
```python
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
```

---

## 🔴 Platform-Specific Issues

### Windows: "OSError: [WinError 123] The filename, directory name, or volume label syntax is incorrect"

**Cause:** Path separator issues.

**Solution:**
```python
# Use os.path.join instead of manual path construction
import os
filepath = os.path.join('data', 'hipaa_training.db')

# Or use pathlib
from pathlib import Path
filepath = Path('data') / 'hipaa_training.db'
```

---

### Windows: chmod not working

**Cause:** chmod is Unix-only.

**Solution:**
```python
# Already fixed in main.py - checks platform
import platform
if platform.system() != 'Windows':
    os.chmod(directory, 0o700)
```

---

### macOS: "Operation not permitted"

**Cause:** macOS security restrictions.

**Solution:**
```bash
# Grant terminal full disk access
# System Preferences > Security & Privacy > Privacy > Full Disk Access
# Add Terminal.app

# Or run from user directory
cd ~/Documents/hipaa-training-v3
python main.py
```

---

## 🔴 CI/CD Issues

### GitHub Actions: "Authentication failed"

**Cause:** Missing or expired GitHub secrets.

**Solution:**
```bash
# Add secrets in GitHub repository
# Settings > Secrets and variables > Actions > New repository secret

# Required secrets:
# - DOCKER_USERNAME
# - DOCKER_PASSWORD
# - CODECOV_TOKEN (optional)
```

---

### CI tests pass but fail on main

**Cause:** Branch protection or merge conflicts.

**Solution:**
```bash
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
```

---

## 🔴 Common Usage Errors

### "Cannot create user with special characters"

**Cause:** Input sanitization removing characters.

**Solution:**
- Special characters are preserved in names like "O'Brien" or "José"
- Truly dangerous characters (HTML/script tags) are escaped
- If legitimate character is removed, file a bug report

---

### Training progress not saving

**Cause:** Database connection issue or improper shutdown.

**Solution:**
```bash
# Check database integrity
sqlite3 data/hipaa_training.db "PRAGMA integrity_check;"

# Check logs for errors
tail -f logs/hipaa_audit.log

# Verify progress is being recorded
sqlite3 data/hipaa_training.db "SELECT * FROM training_progress ORDER BY completed_at DESC LIMIT 5;"
```

---

## 🛠️ Debug Mode

Enable debug mode for verbose output:

```bash
# Run with debug flag
python main.py --debug

# Or set environment variable
export DEBUG=true
python main.py
```

---

## 📊 Health Check

Run the health check script to diagnose issues:

```bash
python scripts/health_check.py
```

This checks:
- ✅ Database integrity
- ✅ Content files
- ✅ Directory structure
- ✅ Environment variables
- ✅ Dependencies
- ✅ Audit logs

---

## 🔍 Collecting Diagnostic Information

For bug reports, collect this information:

```bash
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
```

---

## 📞 Getting Help

If none of these solutions work:

1. **Check GitHub Issues:** https://github.com/Saranoah/HIPAA-Training-System-for-Pharmacy-Staff-V3.0/issues

2. **Create New Issue:** Include:
   - Python version
   - Operating system
   - Complete error message
   - Output from `python scripts/health_check.py`
   - Steps to reproduce

3. **Review Documentation:**
   - README.md
   - SETUP_GUIDE.md
   - API.md

---

## 🚑 Emergency Recovery

If system is completely broken:

```bash
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
```

---

## 📝 Known Issues

### Issue: Evidence files over 5MB rejected
**Status:** By design  
**Workaround:** Compress files or split into smaller chunks

### Issue: No web interface
**Status:** Planned for V4.0  
**Workaround:** Use CLI for now

### Issue: Email notifications not sent
**Status:** Not implemented  
**Workaround:** Monitor logs manually or implement custom notification

---

## ✅ Preventive Measures

To avoid issues:

1. **Regular Backups:**
   ```bash
   # Set up automated daily backups
   crontab -e
   0 2 * * * /path/to/scripts/backup_database.sh
   ```

2. **Monitor Logs:**
   ```bash
   # Check logs weekly
   tail -f logs/hipaa_audit.log
   ```

3. **Test Restores:**
   ```bash
   # Test backup restore monthly
   ./scripts/backup_database.sh
   # Then restore to test environment
   ```

4. **Keep Updated:**
   ```bash
   git pull origin main
   pip install -r requirements.txt --upgrade
   ```

5. **Regular Health Checks:**
   ```bash
   # Run weekly
   python scripts/health_check.py
   ```

---

## 📚 Additional Resources

- **HIPAA Guidance:** https://www.hhs.gov/hipaa
- **Python Documentation:** https://docs.python.org/3/
- **SQLite Documentation:** https://www.sqlite.org/docs.html
- **Cryptography Library:** https://cryptography.io/

---

**Last Updated:** 2025-01-11  
**Version:** 3.0.1

**Still having issues? Create a GitHub issue with detailed information!**
```

---


