# main.py
import os
from hipaa_training.cli import CLI

def setup_production_environment():
    """Setup production directories and permissions"""
    os.makedirs("content", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("certificates", exist_ok=True)
    os.makedirs("evidence", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Set secure permissions
    for directory in ["content", "reports", "certificates", "evidence", "data"]:
        os.chmod(directory, 0o700)
    
    # Initialize database if not exists
    from hipaa_training.models import DatabaseManager
    DatabaseManager()

if __name__ == "__main__":
    setup_production_environment()
    cli = CLI()
    cli.run()
