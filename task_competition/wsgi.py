"""
WSGI entry point for production deployment.
"""
import os
import sys

# Add parent directory to path so task_competition can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_competition.app import create_app

app = create_app(os.getenv('FLASK_ENV', 'production'))
