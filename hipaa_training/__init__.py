"""
HIPAA Training System V3.0
A comprehensive, secure training system for pharmacy staff compliance.
"""

__version__ = "3.0.0"
__author__ = "Israa Ali"
__email__ = "israaali2019@yahoo.com"

# Import key classes/functions for easier access
from .cli import CLI
from .models import DatabaseManager, UserManager, ComplianceDashboard
from .security import SecurityManager
from .training_engine import EnhancedTrainingEngine
from .content_manager import ContentManager

__all__ = [
    "DatabaseManager",
    "UserManager",
    "ComplianceDashboard",
    "SecurityManager",
    "ContentManager",
    "EnhancedTrainingEngine",
    "CLI"
]
