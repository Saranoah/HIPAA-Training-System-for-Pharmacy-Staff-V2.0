# Deployment Guide

Comprehensive guide for deploying the HIPAA Training System in various environments.

## 📋 Table of Contents

- [Quick Deployment](#quick-deployment)
- [Single-User Deployment](#single-user-deployment)
- [Multi-User Deployment](#multi-user-deployment)
- [Enterprise Deployment](#enterprise-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Security Hardening](#security-hardening)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Deployment

### For Testing/Development

```bash
# 1. Clone repository
git clone https://github.com/Saranoah/HIPAA-Training-System-for-Pharmacy-Staff-V2.0.git
cd hipaa-training-system

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Start program
python hipaa_ai_pharmacy_production.py
```

### For Windows

```batch
REM 1. Clone repository
git clone https://github.com/Saranoah/HIPAA-Training-System-for-Pharmacy-Staff-V2.0.git
cd hipaa-training-system

REM 2. Run setup script
setup.bat

REM 3. Start program
python hipaa_ai_pharmacy_production.py
```

## 💻 Single-User Deployment

### Requirements

- Python 3.8 or higher
- 50MB free disk space
- Read/write permissions in installation directory

### Installation Steps

1. **Download and Extract**
   ```bash
   wget https://github.com/Saranoah/HIPAA-Training-System-for-Pharmacy-Staff-V2.0/archive/main.zip
   unzip main.zip
   cd hipaa-training-system-main
   ```

2. **Set Permissions**
   ```bash
   chmod 755 hipaa_ai_pharmacy_production.py
   chmod 755 test_hipaa_training.py
   ```

3. **Run Initial Test**
   ```bash
   python test_hipaa_training.py
   ```

4. **Create Desktop Shortcut (Optional)**
   
   **Linux/Mac:**
   ```bash
   cat > ~/Desktop/HIPAA-Training.sh << 'EOF'
   #!/bin/bash
   cd /path/to/hipaa-training-system
   python hipaa_ai_pharmacy_production.py
   EOF
   chmod +x ~/Desktop/HIPAA-Training.sh
   ```
   
   **Windows:**
   ```batch
   REM Create shortcut manually or use this PowerShell script
   $WshShell = New-Object -comObject WScript.Shell
   $Shortcut = $WshShell.CreateShortcut("$Home\Desktop\HIPAA Training.lnk")
   $Shortcut.TargetPath = "python.exe"
   $Shortcut.Arguments = "C:\path\to\hipaa_ai_pharmacy_production.py"
   $Shortcut.Save()
   ```

## 👥 Multi-User Deployment

### Shared Computer Setup

For multiple users on the same computer:

1. **Install in Shared Location**
   ```bash
   sudo mkdir /opt/hipaa-training
   sudo cp -r . /opt/hipaa-training/
   sudo chown -R root:users /opt/hipaa-training/
   ```

2. **Configure User-Specific Data**
   
   Modify the code to use user-specific directories:
   
   ```python
   import os
   from pathlib import Path
   
   # Add at top of hipaa_ai_pharmacy_production.py
   USER_HOME = Path.home()
   USER_DATA_DIR = USER_HOME / ".hipaa_training"
   USER_DATA_DIR.mkdir(exist_ok=True)
   
   PROGRESS_FILE = str(USER_DATA_DIR / "hipaa_progress.json")
   ```

3. **Set Permissions**
   ```bash
   sudo chmod 755 /opt/hipaa-training/*.py
   sudo chmod 644 /opt/hipaa-training/*.md
   ```

4. **Create Wrapper Script**
   ```bash
   sudo cat > /usr/local/bin/hipaa-training << 'EOF'
   #!/bin/bash
   cd /opt/hipaa-training
   python hipaa_ai_pharmacy_production.py
   EOF
   sudo chmod +x /usr/local/bin/hipaa-training
   ```

### Network Share Deployment

For deployment on a network share:

1. **Copy to Network Location**
   ```bash
   # Map network drive
   sudo mount -t cifs //server/share /mnt/network -o username=admin
   
   # Copy files
   cp -r hipaa-training-system /mnt/network/
   ```

2. **User Configuration**
   - Each user should copy `hipaa_ai_pharmacy_production.py` to their local drive
   - Or run from network with local data storage

## 🏢 Enterprise Deployment

### Centralized Deployment Architecture

```
┌─────────────────────────────────────┐
│     Central Training Server         │
│  (Python app + Database backend)    │
└─────────────────┬───────────────────┘
                  │
          ┌───────┴───────┐
          │               │
    ┌─────▼─────┐   ┌─────▼─────┐
    │  Pharmacy │   │  Pharmacy │
    │  Location │   │  Location │
    │     #1    │   │     #2    │
    └───────────┘   └───────────┘
```

### Steps

1. **Server Setup**
   
   Install on Ubuntu Server 22.04:
   
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3 python3-pip python3-venv -y
   
   # Create service user
   sudo useradd -r -s /bin/false hipaa-training
   
   # Install application
   sudo mkdir /opt/hipaa-training
   sudo chown hipaa-training:hipaa-training /opt/hipaa-training
   cd /opt/hipaa-training
   sudo -u hipaa-training git clone https://github.com/yourusername/hipaa-training-system.git .
   ```

2. **Database Integration (Optional)**
   
   For tracking multiple users, integrate SQLite:
   
   ```python
   import sqlite3
   
   def init_database():
       conn = sqlite3.connect('hipaa_training.db')
       c = conn.cursor()
       c.execute('''
           CREATE TABLE IF NOT EXISTS user_progress (
               user_id TEXT PRIMARY KEY,
               username TEXT,
               last_updated TEXT,
               checklist_data TEXT,
               compliance_score REAL,
               quiz_scores TEXT
           )
       ''')
       conn.commit()
       conn.close()
   ```

3. **Create Systemd Service**
   
   ```bash
   sudo cat > /etc/systemd/system/hipaa-training.service << 'EOF'
   [Unit]
   Description=HIPAA Training System
   After=network.target
   
   [Service]
   Type=simple
   User=hipaa-training
   WorkingDirectory=/opt/hipaa-training
   ExecStart=/usr/bin/python3 hipaa_ai_pharmacy_production.py
   Restart=on-failure
   
   [Install]
   WantedBy=multi-user.target
   EOF
   
   sudo systemctl daemon-reload
   sudo systemctl enable hipaa-training
   sudo systemctl start hipaa-training
   ```

4. **User Access Management**
   
   Create admin interface for tracking:
   
   ```python
   def generate_admin_report():
       """Generate organization-wide compliance report"""
       conn = sqlite3.connect('hipaa_training.db')
       c = conn.cursor()
       
       # Get all user scores
       c.execute('SELECT username, compliance_score FROM user_progress')
       users = c.fetchall()
       
       # Calculate statistics
       total_users = len(users)
       avg_score = sum(score for _, score in users) / total_users
       passing_users = sum(1 for _, score in users if score >= 80)
       
       print(f"Total Users: {total_users}")
       print(f"Average Score: {avg_score:.1f}%")
       print(f"Passing Rate: {passing_users/total_users*100:.1f}%")
       
       conn.close()
   ```

## ☁️ Cloud Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   ```bash
   # Use Ubuntu 22.04 AMI
   # Instance type: t2.micro (free tier)
   # Security group: Allow SSH (22)
   ```

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update and install Python
   sudo apt update
   sudo apt install python3 python3-pip git -y
   
   # Clone and setup
   git clone https://github.com/yourusername/hipaa-training-system.git
   cd hipaa-training-system
   ./setup.sh
   ```

3. **Configure Access**
   - Set up VPN for secure access
   - Or use AWS Systems Manager Session Manager
   - Configure CloudWatch for monitoring

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN python -m pip install --no-cache-dir -r requirements.txt || true

# Create non-root user
RUN useradd -m -u 1000 hipaa && \
    chown -R hipaa:hipaa /app

USER hipaa

EXPOSE 8000

CMD ["python", "hipaa_ai_pharmacy_production.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  hipaa-training:
    build: .
    container_name: hipaa-training
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - PROGRESS_FILE=/app/data/hipaa_progress.json
```

Deploy:

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🔒 Security Hardening

### File Permissions

```bash
# Application files (read-only)
chmod 644 hipaa_ai_pharmacy_production.py
chmod 644 test_hipaa_training.py

# Progress files (user-only)
chmod 600 hipaa_progress.json

# Configuration files (user-only)
chmod 600 config.json
```

### Data Encryption

Add encryption for sensitive data:

```python
from cryptography.fernet import Fernet
import json

def encrypt_progress(data: dict, key: bytes) -> bytes:
    """Encrypt progress data"""
    f = Fernet(key)
    json_data = json.dumps(data).encode()
    return f.encrypt(json_data)

def decrypt_progress(encrypted_data: bytes, key: bytes) -> dict:
    """Decrypt progress data"""
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_data)
    return json.loads(decrypted)

# Generate and store key securely
key = Fernet.generate_key()
# Store in environment variable or secure key management system
```

### Audit Logging

Add comprehensive logging:

```python
import logging
from datetime import datetime

logging.basicConfig(
    filename='hipaa_training_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def log_user_action(username: str, action: str, details: str = ""):
    """Log user actions for audit trail"""
    logging.info(f"User: {username} | Action: {action} | Details: {details}")

# Example usage
log_user_action("john.doe", "completed_quiz", "Score: 85%")
log_user_action("jane.smith", "viewed_lessons", "Privacy Rule")
```

### Session Timeout

Add inactivity timeout:

```python
import time

TIMEOUT_SECONDS = 900  # 15 minutes
last_activity = time.time()

def check_timeout():
    """Check for session timeout"""
    global last_activity
    if time.time() - last_activity > TIMEOUT_SECONDS:
        print("\n⚠️  Session timeout due to inactivity")
        print("Please restart the program to continue.")
        exit(0)

def update_activity():
    """Update last activity timestamp"""
    global last_activity
    last_activity = time.time()

# Call check_timeout() before each user interaction
# Call update_activity() after each user input
```

## 🔧 Maintenance

### Regular Updates

```bash
# Update from repository
cd hipaa-training-system
git pull origin main

# Run tests
python test_hipaa_training.py

# Backup user data
cp hipaa_progress.json hipaa_progress.json.backup.$(date +%Y%m%d)
```

### Backup Strategy

**Daily Backups**:
```bash
#!/bin/bash
# backup_hipaa.sh
BACKUP_DIR="/backups/hipaa-training"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp hipaa_progress.json $BACKUP_DIR/progress_$DATE.json
cp hipaa_training_audit.log $BACKUP_DIR/audit_$DATE.log

# Keep only last 30 days
find $BACKUP_DIR -name "*.json" -mtime +30 -delete
find $BACKUP_DIR -name "*.log" -mtime +30 -delete
```

Add to crontab:
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup_hipaa.sh
```

### Monitoring

**Health Check Script**:
```bash
#!/bin/bash
# health_check.sh

# Check if program can start
timeout 5 echo "7" | python hipaa_ai_pharmacy_production.py > /dev/null 2>&1
if [ $? -eq 0 ] || [ $? -eq 124 ]; then
    echo "[OK] Application healthy"
    exit 0
else
    echo "[ERROR] Application unhealthy"
    # Send alert email
    echo "HIPAA Training System health check failed" | mail -s "Alert" admin@example.com
    exit 1
fi
```

## 🐛 Troubleshooting

### Common Issues

**Issue: Program won't start**
```bash
# Check Python version
python --version

# Run tests
python test_hipaa_training.py

# Check for errors
python -v hipaa_ai_pharmacy_production.py
```

**Issue: Progress not saving**
```bash
# Check file permissions
ls -l hipaa_progress.json

# Check disk space
df -h

# Check write permissions
touch hipaa_progress.json
```

**Issue: Corrupted progress file**
```bash
# Validate JSON
python -m json.tool hipaa_progress.json

# Restore from backup
cp hipaa_progress.json.backup hipaa_progress.json
```

### Performance Issues

**Slow startup**:
- Check disk I/O
- Verify Python version (3.8+ recommended)
- Check for antivirus interference

**Memory issues**:
```bash
# Monitor memory usage
/usr/bin/time -l python hipaa_ai_pharmacy_production.py
```

### Getting Help

1. Check logs: `cat hipaa_training_audit.log`
2. Run diagnostics: `python test_hipaa_training.py -v`
3. Review documentation: `cat README.md`
4. Open GitHub issue with details

---

**Last Updated**: October 2, 2025  
**Version**: 1.0.0

For additional support, contact: your.email@example.com
