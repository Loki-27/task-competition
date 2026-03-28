"""
WSGI entry point for production deployment.
"""
import os
from task_competition.app import create_app

app = create_app(os.getenv('FLASK_ENV', 'production'))
