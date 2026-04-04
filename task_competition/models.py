from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pytz

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and tracking points."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_points = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    tasks = db.relationship('Task', backref='creator', lazy=True, foreign_keys='Task.user_id')
    completions = db.relationship('TaskCompletion', backref='user', lazy=True)
    verifications = db.relationship('TaskVerification', backref='verifier', lazy=True)
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password."""
        return check_password_hash(self.password_hash, password)
    
    def get_daily_points(self):
        """Get points earned today."""
        today = datetime.utcnow().date()
        today_completions = TaskCompletion.query.filter(
            TaskCompletion.user_id == self.id,
            db.func.date(TaskCompletion.completed_at) == today,
            TaskCompletion.is_verified == True
        ).all()
        
        points = sum(completion.task.points for completion in today_completions)
        return points
    
    def get_leaderboard_rank(self):
        """Get user's rank on leaderboard (1-indexed)."""
        users_ahead = User.query.filter(User.total_points > self.total_points).count()
        return users_ahead + 1
    
    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    """Task model for Good Tasks, Bad Tasks, Weekly and Monthly Goals."""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    points = db.Column(db.Integer, nullable=False)  # Positive for good tasks, negative for bad tasks
    task_type = db.Column(db.String(20), nullable=False, default='good')  # 'good' or 'bad'
    category = db.Column(db.String(20), nullable=False, default='daily')  # 'daily', 'weekly', 'monthly'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    requires_verification = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)  # For task ordering
    duration_minutes = db.Column(db.Integer, default=0)  # Timer duration (0 = no timer)
    target = db.Column(db.Integer, default=0)  # Target count (0 = checkbox only)
    
    # Relationships
    completions = db.relationship('TaskCompletion', backref='task', lazy=True, cascade='all, delete-orphan')
    verifications = db.relationship('TaskVerification', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def get_today_completions(self):
        """Get completions for this task today."""
        today = datetime.utcnow().date()
        return TaskCompletion.query.filter(
            TaskCompletion.task_id == self.id,
            db.func.date(TaskCompletion.completed_at) == today
        ).all()
    
    def __repr__(self):
        return f'<Task {self.title}>'


class TaskCompletion(db.Model):
    """Track when a user completes a task."""
    __tablename__ = 'task_completions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    needs_verification = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    progress_count = db.Column(db.Integer, default=0)  # For goals with targets (e.g., 3 out of 7)
    elapsed_seconds = db.Column(db.Integer, default=0)  # Time spent on timed tasks
    completion_type = db.Column(db.String(20), default='full')  # 'full' or 'partial'
    week_key = db.Column(db.String(10))  # ISO week key (YYYY-Www) for weekly goal tracking
    month_key = db.Column(db.String(7))  # Month key (YYYY-MM) for monthly goal tracking
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'task_id', 'completed_at', name='unique_daily_completion'),
    )
    
    def __repr__(self):
        return f'<TaskCompletion user_id={self.user_id} task_id={self.task_id}>'


class TaskVerification(db.Model):
    """Track peer verification of completed tasks."""
    __tablename__ = 'task_verifications'
    
    id = db.Column(db.Integer, primary_key=True)
    task_completion_id = db.Column(db.Integer, db.ForeignKey('task_completions.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    verifier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'approved', 'rejected', 'pending'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    
    completion = db.relationship('TaskCompletion', backref='verifications')
    
    def approve(self):
        """Approve the verification."""
        self.status = 'approved'
        self.verified_at = datetime.utcnow()
        
        # Update the completion and user points
        completion = TaskCompletion.query.get(self.task_completion_id)
        if completion:
            completion.is_verified = True
            user = User.query.get(completion.user_id)
            if user:
                user.total_points += completion.task.points
                db.session.commit()
    
    def reject(self):
        """Reject the verification."""
        self.status = 'rejected'
        self.verified_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<TaskVerification task_completion_id={self.task_completion_id} status={self.status}>'


def reset_daily_tasks():
    """Reset daily tasks (mark old completions as inactive for new day)."""
    # This is called once per day to reset available tasks
    # Note: total_points persist, only daily task completions are reset
    today = datetime.utcnow().date()
    
    # Completions from yesterday are already in the past and won't be shown
    # This is handled by filtering in the route queries
    pass
