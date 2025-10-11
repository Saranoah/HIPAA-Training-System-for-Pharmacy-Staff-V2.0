#!/usr/bin/env python3
"""
HIPAA Training System V3.0 - Main Entry Point
"""

import os
from hipaa_training.cli import CLI


def setup_production_environment():
    """Setup production directories and permissions"""
    directories = ["content", "reports", "certificates", "evidence", "data", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    if os.name != "nt":  # Unix-like systems
        os.umask(0o077)  # owner-only permissions
        for directory in directories:
            try:
                os.chmod(directory, 0o700)
            except Exception:
                pass

    # Initialize database
    from hipaa_training.models import DatabaseManager
    DatabaseManager()
    print("✅ Production environment setup complete!")


if __name__ == "__main__":
    try:
        setup_production_environment()
        cli = CLI()
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully...")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

