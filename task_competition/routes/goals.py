"""Goals management routes - Weekly and Monthly goals."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from ..models import db, Task, TaskCompletion, User
import logging

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')
logger = logging.getLogger(__name__)


def get_week_key(date=None):
    """Get ISO week key (YYYY-Www)."""
    if date is None:
        date = datetime.utcnow()
    return f"{date.year}-W{date.isocalendar()[1]:02d}"


def get_month_key(date=None):
    """Get month key (YYYY-MM)."""
    if date is None:
        date = datetime.utcnow()
    return date.strftime("%Y-%m")


def parse_week_key(week_key):
    """Parse week key (YYYY-Www) to datetime."""
    try:
        year, week = week_key.split('-W')
        return datetime.strptime(f"{year}-W{int(week)}-1", "%Y-W%W-%w")
    except (ValueError, AttributeError):
        return datetime.utcnow()


def parse_month_key(month_key):
    """Parse month key (YYYY-MM) to datetime."""
    try:
        return datetime.strptime(month_key, "%Y-%m")
    except (ValueError, TypeError):
        return datetime.utcnow()


def format_week_display(week_key):
    """Format week key like 'Mar 24 - Mar 30, 2024'."""
    date = parse_week_key(week_key)
    week_start = date
    week_end = week_start + timedelta(days=6)
    
    if week_start.month == week_end.month:
        return f"{week_start.strftime('%b %d')} - {week_end.strftime('%d, %Y')}"
    else:
        return f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"


def format_month_display(month_key):
    """Format month key like 'March 2024'."""
    date = parse_month_key(month_key)
    return date.strftime("%B %Y")


@goals_bp.route('/weekly')
@login_required
def weekly_dashboard():
    """Display weekly goals dashboard."""
    try:
        week_key = request.args.get('week', get_week_key())
        
        # Navigate weeks
        current_date = parse_week_key(week_key)
        prev_date = current_date - timedelta(weeks=1)
        next_date = current_date + timedelta(weeks=1)
        
        prev_week = get_week_key(prev_date)
        next_week = get_week_key(next_date)
        
        # Get weekly goals for current user
        weekly_goals = Task.query.filter_by(
            user_id=current_user.id,
            category='weekly',
            is_active=True
        ).order_by(Task.order).all()
        
        return render_template('goals/weekly.html',
                              weekly_goals=weekly_goals,
                              current_week=week_key,
                              prev_week=prev_week,
                              next_week=next_week,
                              week_display=format_week_display(week_key))
    except Exception as e:
        logger.error(f"Error in weekly_dashboard: {e}")
        flash('Error loading weekly goals', 'danger')
        return redirect(url_for('tasks.dashboard'))


@goals_bp.route('/monthly')
@login_required
def monthly_dashboard():
    """Display monthly goals dashboard."""
    try:
        month_key = request.args.get('month', get_month_key())
        
        # Navigate months
        current_date = parse_month_key(month_key)
        if current_date.month == 1:
            prev_date = current_date.replace(year=current_date.year - 1, month=12)
        else:
            prev_date = current_date.replace(month=current_date.month - 1)
        
        if current_date.month == 12:
            next_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            next_date = current_date.replace(month=current_date.month + 1)
        
        prev_month = get_month_key(prev_date)
        next_month = get_month_key(next_date)
        
        # Get monthly goals for current user
        monthly_goals = Task.query.filter_by(
            user_id=current_user.id,
            category='monthly',
            is_active=True
        ).order_by(Task.order).all()
        
        return render_template('goals/monthly.html',
                              monthly_goals=monthly_goals,
                              current_month=month_key,
                              prev_month=prev_month,
                              next_month=next_month,
                              month_display=format_month_display(month_key))
    except Exception as e:
        logger.error(f"Error in monthly_dashboard: {e}")
        flash('Error loading monthly goals', 'danger')
        return redirect(url_for('tasks.dashboard'))


@goals_bp.route('/statistics')
@login_required
def statistics():
    """Display goals statistics and progress."""
    try:
        # Get all goals
        all_goals = Task.query.filter_by(
            user_id=current_user.id,
            is_active=True
        ).all()
        
        # Separate by category
        weekly_goals = [g for g in all_goals if g.category == 'weekly']
        monthly_goals = [g for g in all_goals if g.category == 'monthly']
        
        # Calculate statistics for weekly goals
        weekly_stats = []
        for goal in weekly_goals:
            try:
                completions = TaskCompletion.query.filter_by(
                    user_id=current_user.id,
                    task_id=goal.id
                ).all()
                
                progress_count = sum(c.progress_count or 0 for c in completions if c.completion_type == 'full')
                is_completed = len([c for c in completions if c.completion_type == 'full']) > 0
            except Exception as e:
                logger.warning(f"Error calculating stats for goal {goal.id}: {e}")
                progress_count = 0
                is_completed = False
            
            weekly_stats.append({
                'id': goal.id,
                'title': goal.title,
                'target': goal.target,
                'progress_count': progress_count,
                'is_completed': is_completed,
                'points': goal.points
            })
        
        # Calculate statistics for monthly goals
        monthly_stats = []
        for goal in monthly_goals:
            try:
                completions = TaskCompletion.query.filter_by(
                    user_id=current_user.id,
                    task_id=goal.id
                ).all()
                
                progress_count = sum(c.progress_count or 0 for c in completions if c.completion_type == 'full')
                is_completed = len([c for c in completions if c.completion_type == 'full']) > 0
            except Exception as e:
                logger.warning(f"Error calculating stats for goal {goal.id}: {e}")
                progress_count = 0
                is_completed = False
            
            monthly_stats.append({
                'id': goal.id,
                'title': goal.title,
                'target': goal.target,
                'progress_count': progress_count,
                'is_completed': is_completed,
                'points': goal.points
            })
        
        # Calculate totals
        total_goals = len(all_goals)
        completed_goals = sum(1 for g in weekly_stats + monthly_stats if g['is_completed'])
        in_progress_goals = total_goals - completed_goals
        completion_rate = int((completed_goals / total_goals * 100) if total_goals > 0 else 0)
        
        return render_template('goals/statistics.html',
                              weekly_stats=weekly_stats,
                              monthly_stats=monthly_stats,
                              total_goals=total_goals,
                              completed_goals=completed_goals,
                              in_progress_goals=in_progress_goals,
                              completion_rate=completion_rate)
    except Exception as e:
        logger.error(f"Error in statistics: {e}")
        flash('Error loading statistics', 'danger')
        return redirect(url_for('tasks.dashboard'))


@goals_bp.route('/create/<goal_type>', methods=['GET', 'POST'])
@login_required
def create_goal(goal_type):
    """Create a new weekly or monthly goal."""
    try:
        if goal_type not in ['weekly', 'monthly']:
            flash('Invalid goal type.', 'danger')
            return redirect(url_for('tasks.dashboard'))
        
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            points = request.form.get('points', type=int, default=10)
            target = request.form.get('target', type=int, default=0)
            duration_minutes = request.form.get('duration_minutes', type=int, default=0)
            goal_type_choice = request.form.get('goal_type_choice', 'completion')
            
            if not title:
                flash('Goal title is required.', 'danger')
                return redirect(url_for('goals.create_goal', goal_type=goal_type))
            
            if goal_type_choice == 'target' and not target:
                flash('Target count is required for target-based goals.', 'danger')
                return redirect(url_for('goals.create_goal', goal_type=goal_type))
            
            # Get highest order number
            highest_order = db.session.query(db.func.max(Task.order)).filter_by(
                user_id=current_user.id,
                category=goal_type
            ).scalar() or -1
            
            goal = Task(
                user_id=current_user.id,
                title=title,
                description=description,
                points=points,
                task_type='goal',
                category=goal_type,
                is_active=True,
                order=highest_order + 1,
                target=target if goal_type_choice == 'target' else 0,
                duration_minutes=duration_minutes if duration_minutes > 0 else None
            )
            
            db.session.add(goal)
            db.session.commit()
            
            flash(f'{goal_type.capitalize()} goal "{title}" created!', 'success')
            return redirect(url_for('goals.weekly_dashboard' if goal_type == 'weekly' else 'goals.monthly_dashboard'))
        
        return render_template('goals/create.html', goal_type=goal_type)
    except Exception as e:
        logger.error(f"Error in create_goal: {e}")
        flash(f'Error creating goal: {str(e)}', 'danger')
        return redirect(url_for('tasks.dashboard'))


@goals_bp.route('/<int:goal_id>/complete', methods=['POST'])
@login_required
def complete_goal(goal_id):
    """Mark a goal as complete."""
    goal = Task.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Create completion record
    completion = TaskCompletion(
        user_id=current_user.id,
        task_id=goal_id,
        progress_count=goal.target if goal.target > 0 else 1,
        completion_type='full',
        week_key=get_week_key() if goal.category == 'weekly' else None,
        month_key=get_month_key() if goal.category == 'monthly' else None
    )
    
    db.session.add(completion)
    
    # Update user points
    current_user.total_points += goal.points
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Goal completed!',
        'points': goal.points
    })


@goals_bp.route('/<int:goal_id>/progress', methods=['POST'])
@login_required
def update_progress(goal_id):
    """Update progress on a target-based goal."""
    goal = Task.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    increment = request.json.get('increment', 1)
    
    # Get or create completion for this week/month
    if goal.category == 'weekly':
        key_filter = {'week_key': get_week_key()}
    elif goal.category == 'monthly':
        key_filter = {'month_key': get_month_key()}
    else:
        key_filter = {}
    
    completion = TaskCompletion.query.filter_by(
        user_id=current_user.id,
        task_id=goal_id,
        **key_filter
    ).first()
    
    if not completion:
        completion = TaskCompletion(
            user_id=current_user.id,
            task_id=goal_id,
            progress_count=increment,
            completion_type='partial',
            week_key=get_week_key() if goal.category == 'weekly' else None,
            month_key=get_month_key() if goal.category == 'monthly' else None
        )
        db.session.add(completion)
    else:
        completion.progress_count = (completion.progress_count or 0) + increment
    
    # Check if goal is complete
    if goal.target > 0 and completion.progress_count >= goal.target:
        # Only award points once when goal is completed
        if completion.completion_type != 'full':  # Only add if wasn't already full
            current_user.total_points += goal.points
        completion.completion_type = 'full'
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'progress_count': completion.progress_count,
        'target': goal.target,
        'complete': completion.completion_type == 'full',
        'points': goal.points
    })
