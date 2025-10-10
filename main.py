#!/usr/bin/env python3
"""
HIPAA Training System V3.0 - Main Entry Point
"""

import os
from hipaa_training.cli import CLI


def setup_production_environment():
    """Setup production directories and permissions"""
    # Create necessary directories
    directories = [
        "content", "reports", "certificates",
        "evidence", "data", "logs"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Set secure permissions (Unix-like systems)
    for directory in directories:
        try:
            os.chmod(directory, 0o700)
        except Exception:
            pass  # Permission setting might fail on Windows

    # Initialize database
    from hipaa_training.models import DatabaseManager
    DatabaseManager()

    print("✅ Production environment setup complete!")


if __name__ == "__main__":
    setup_production_environment()
    cli = CLI()
    cli.cmdloop()
