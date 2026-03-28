from flask import Blueprint, render_template
from flask_login import login_required
from ..models import User, TaskCompletion, db
from datetime import datetime

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@leaderboard_bp.route('/')
def index():
    """Display the leaderboard."""
    # Get all users sorted by total points (descending)
    users = User.query.filter_by(is_active=True).order_by(User.total_points.desc()).all()
    
    # Get today's top performers
    today = datetime.utcnow().date()
    today_completions = TaskCompletion.query.filter(
        TaskCompletion.is_verified == True,
        db.func.date(TaskCompletion.completed_at) == today
    ).all()
    
    # Calculate daily points per user
    daily_points = {}
    for completion in today_completions:
        user_id = completion.user_id
        if user_id not in daily_points:
            daily_points[user_id] = 0
        daily_points[user_id] += completion.task.points
    
    # Sort users for daily leaderboard
    daily_leaderboard = sorted(
        [(User.query.get(uid), points) for uid, points in daily_points.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    return render_template('leaderboard/index.html',
                         users=users,
                         daily_leaderboard=daily_leaderboard)

@leaderboard_bp.route('/daily')
def daily():
    """Display today's leaderboard."""
    today = datetime.utcnow().date()
    
    # Get today's verified completions
    today_completions = TaskCompletion.query.filter(
        TaskCompletion.is_verified == True,
        db.func.date(TaskCompletion.completed_at) == today
    ).all()
    
    # Calculate daily points per user
    daily_points = {}
    for completion in today_completions:
        user_id = completion.user_id
        if user_id not in daily_points:
            daily_points[user_id] = 0
        daily_points[user_id] += completion.task.points
    
    # Get user objects and sort
    leaderboard = sorted(
        [(User.query.get(uid), points) for uid, points in daily_points.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    return render_template('leaderboard/daily.html', leaderboard=leaderboard)

