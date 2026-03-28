"""
Initialize the database with sample data for testing.
Run this script to populate the database with test users and tasks.
"""

import sys
import os

# Add parent directory to path so task_competition can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_competition.app import create_app
from task_competition.models import db, User, Task

def init_db():
    """Initialize database with sample data."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if users already exist
        if User.query.first():
            print("Database already initialized. Skipping sample data.")
            return
        
        print("Creating sample users...")
        
        # Create sample users
        users_data = [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'display_name': 'Alice',
                'password': 'password123'
            },
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'display_name': 'Bob',
                'password': 'password123'
            },
            {
                'username': 'charlie',
                'email': 'charlie@example.com',
                'display_name': 'Charlie',
                'password': 'password123'
            }
        ]
        
        users = []
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                display_name=user_data['display_name']
            )
            user.set_password(user_data['password'])
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"Created {len(users)} users")
        
        print("Creating sample tasks...")
        
        # Create sample tasks
        tasks_data = [
            {
                'user_id': users[0].id,
                'title': 'Morning Jog',
                'description': 'Run or jog for at least 20 minutes',
                'task_type': 'good',
                'points': 10
            },
            {
                'user_id': users[0].id,
                'title': 'Read for 30 minutes',
                'description': 'Read a book or interesting article',
                'task_type': 'good',
                'points': 5
            },
            {
                'user_id': users[1].id,
                'title': 'Skip Dessert',
                'description': 'Avoid sugary desserts for the day',
                'task_type': 'good',
                'points': 5
            },
            {
                'user_id': users[1].id,
                'title': 'Drink 8 glasses of water',
                'description': 'Stay hydrated throughout the day',
                'task_type': 'good',
                'points': 3
            },
            {
                'user_id': users[2].id,
                'title': 'Sleep before midnight',
                'description': 'Go to bed before 12 AM',
                'task_type': 'good',
                'points': 8,
                'requires_verification': True
            },
            {
                'user_id': users[0].id,
                'title': 'No social media',
                'description': 'Avoid social media for 24 hours',
                'task_type': 'bad',
                'points': -15
            },
            {
                'user_id': users[1].id,
                'title': 'Stayed up late',
                'description': 'Staying up past 1 AM',
                'task_type': 'bad',
                'points': -5
            }
        ]
        
        for task_data in tasks_data:
            task = Task(**task_data)
            db.session.add(task)
        
        db.session.commit()
        print(f"Created {len(tasks_data)} tasks")
        
        print("\n✅ Database initialized successfully!")
        print("\nTest Users:")
        print("  Username: alice | Password: password123")
        print("  Username: bob   | Password: password123")
        print("  Username: charlie | Password: password123")
        print("\nYou can now login and test the application!")

if __name__ == '__main__':
    init_db()
