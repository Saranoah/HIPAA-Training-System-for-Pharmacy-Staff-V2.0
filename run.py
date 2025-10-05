#!/usr/bin/env python3
"""
Main Entry Point - HIPAA Training Web Application
Run with: python run.py
"""

import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import app

def main():
    """Main application runner"""
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("="*70)
    print("🚀 HIPAA Training System - Web Application")
    print("="*70)
    print("📊 Application Features:")
    print(f"   • {len(app.config.get('LESSONS', {}))} Comprehensive Lessons")
    print(f"   • {len(app.config.get('QUIZ_QUESTIONS', []))} Quiz Questions") 
    print(f"   • {len(app.config.get('CHECKLIST_ITEMS', []))} Checklist Items")
    print("🎯 Coverage: 95%+ HIPAA Requirements for Pharmacy Staff")
    print("🌐 Server running at: http://localhost:5000")
    print("⏹️  Press CTRL+C to stop the server")
    print("="*70)
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
