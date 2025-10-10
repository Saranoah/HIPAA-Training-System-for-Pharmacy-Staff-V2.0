#!/bin/bash

# HIPAA Training System V3.0 - Production Setup Script
set -e

echo "🏥 HIPAA Training System V3.0 - Production Setup"
echo "================================================"

# Check Python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python version: $python_version"

if [[ "$python_version" < "3.8" ]]; then
    echo "❌ Python 3.8 or higher required"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p content reports certificates evidence backup data

# Check if content files exist
if [[ ! -f "content/lessons.json" ]]; then
    echo "❌ Missing content/lessons.json - please ensure content files are present"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Generate encryption key if not set
if [[ -z "$HIPAA_ENCRYPTION_KEY" ]]; then
    echo "🔑 Generating encryption key..."
    export HIPAA_ENCRYPTION_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo "⚠️  IMPORTANT: Add to your environment:"
    echo "export HIPAA_ENCRYPTION_KEY=\"$HIPAA_ENCRYPTION_KEY\""
fi

# Generate random salt
if [[ -z "$HIPAA_ENCRYPTION_SALT" ]]; then
    export HIPAA_ENCRYPTION_SALT=$(python3 -c "import secrets; print(secrets.token_hex(16))")
    echo "export HIPAA_ENCRYPTION_SALT=\"$HIPAA_ENCRYPTION_SALT\""
fi

# Set secure permissions
echo "🔒 Setting secure file permissions..."
chmod 700 certificates reports evidence data
chmod 600 .env 2>/dev/null || true

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "
from hipaa_system_v3 import DatabaseManager
db = DatabaseManager()
print('✓ Database initialized successfully')
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Review content/ files for your organization"
echo "2. Run: python3 hipaa_system_v3.py"
echo "3. Access the system and create admin users"
echo ""
echo "For production:"
echo "- Set HIPAA_ENCRYPTION_KEY in your environment"
echo "- Configure regular backups"
echo "- Monitor audit logs"
