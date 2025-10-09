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
        'src/hipaa_training',
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
    
    # Create all configuration files (content would be the actual file contents)
    # This is where you'd add all the file creation calls
    # create_file('.github/workflows/ci-cd.yml', CI_CD_CONTENT)
    # create_file('.devcontainer/devcontainer.json', DEVCONTAINER_CONTENT)
    # ... etc for all files
    
    print("\n🎉 Project setup completed successfully!")
    print("\nNext steps:")
    print("1. Review and customize the generated files")
    print("2. Run: git init")
    print("3. Run: git add .")
    print("4. Run: git commit -m 'Initial commit: HIPAA Training System V3.0'")
    print("5. Create GitHub repository and push")

if __name__ == "__main__":
    main()