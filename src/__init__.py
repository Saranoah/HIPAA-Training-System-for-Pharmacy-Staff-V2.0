# Make 'src' a package and ensure relative imports work correctly
import os
import sys

# Add the parent directory to sys.path so 'src' can be imported anywhere
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

