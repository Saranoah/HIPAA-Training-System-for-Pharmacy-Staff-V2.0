#!/usr/bin/env python3
"""
HIPAA Training System - Project Setup Script
Automatically creates all necessary GitHub files and project structure
"""

import os
import stat
from pathlib import Path

def create_project_structure():
    """Create the complete project directory structure"""
    directories = [
        '.github/workflows',
        '.devcontainer',
        'hipaa_training',
        'tests',
        'content',
        'docs',
        'scripts',
        'data',
        'reports',
        'certificates',
        'evidence'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_file(path, content):
    """Create a file with the given content"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created file: {path}")

def main():
    print("🏥 HIPAA Training System V3.0 - Project Setup")
    print("=" * 50)
    
    # Create directory structure
    create_project_structure()
    
    # Create essential files
    create_file('.gitignore', '''__pycache__/
*.pyc
*.db
*.log
*.gz
data/
reports/
certificates/
evidence/
.env
''')
    
    create_file('.env.example', '''HIPAA_ENCRYPTION_KEY=your-secure-key-here-32-characters-minimum
DB_URL=sqlite:///data/hipaa_training.db
''')
    
    print("\n🎉 Project setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and set secure values")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: git init")
    print("4. Run: git add .")
    print("5. Run: git commit -m 'Initial commit: HIPAA Training System V3.0'")
    print("6. Create GitHub repository and push")
    print("7. Run: python main.py")

if __name__ == "__main__":
    main()
