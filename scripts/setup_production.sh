#!/usr/bin/env bash
# HIPAA Training System V3.0 - Production Setup Script

set -euo pipefail  # safer: exit on error, unset var, or failed pipe

echo "🏥 HIPAA Training System V3.0 - Production Setup"
echo "================================================"

# --- Check Python version ---
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python version: $python_version"

# Numeric version check
min_version=3.8
if (( $(echo "$python_version < $min_version" | bc -l) )); then
    echo "❌ Python $min_version or higher required"
    exit 1
fi

# --- Verify required files ---
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Missing requirements.txt"
    exit 1
fi

if [[ ! -f "content/lessons.json" ]]; then
    echo "❌ Missing content/lessons.json - please ensure content files are present"
    exit 1
fi

# --- Create directories ---
echo "📁 Creating directory structure..."
mkdir -p content reports certificates evidence backup data

# --- Install dependencies ---
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# --- Generate encryption key ---
if [[ -z "${HIPAA_ENCRYPTION_KEY:-}" ]]; then
    echo "🔑 Generating encryption key..."
    HIPAA_ENCRYPTION_KEY="$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")"
    export HIPAA_ENCRYPTION_KEY
    echo "⚠️  IMPORTANT: Add to your .env or environment:"
    echo "HIPAA_ENCRYPTION_KEY=\"$HIPAA_ENCRYPTION_KEY\""
fi

# --- Generate salt ---
if [[ -z "${HIPAA_SALT:-}" ]]; then
    HIPAA_SALT="$(python3 -c "import secrets; print(secrets.token_hex(16))")"
    export HIPAA_SALT
    echo "HIPAA_SALT=\"$HIPAA_SALT\""
fi

# --- Secure file permissions ---
echo "🔒 Setting secure file permissions..."
chmod 700 certificates reports evidence data
[[ -f ".env" ]] && chmod 600 .env

# --- Initialize database ---
echo "🗄️  Initializing database..."
python3 - <<'PYCODE'
from hipaa_training.models import DatabaseManager
db = DatabaseManager()
print("✓ Database initialized successfully")
PYCODE

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and set secure values"
echo "2. Review content/ files for your organization"
echo "3. Run: python main.py"
echo "4. Access the system and create admin users"
echo ""
echo "For production:"
echo "- Set HIPAA_ENCRYPTION_KEY and HIPAA_SALT in .env"
echo "- Configure regular backups (scripts/backup_database.sh)"
echo "- Monitor audit logs (hipaa_audit.log)"

