"""
HIPAA Training System V3.0
A comprehensive, secure training system for pharmacy staff compliance.
"""

__version__ = "3.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import key classes for easier access
from .models import DatabaseManager
from .security import SecurityManager
from .content_manager import ContentManager
from .training_engine import EnhancedTrainingEngine
from .cli import CLI

__all__ = [
    "DatabaseManager",
    "SecurityManager", 
    "ContentManager",
    "EnhancedTrainingEngine",
    "CLI"
]
