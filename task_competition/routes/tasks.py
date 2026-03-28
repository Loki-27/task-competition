from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models import db, Task, TaskCompletion, TaskVerification, User

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    """Display the main task dashboard."""
    today = datetime.utcnow().date()
    
    # Get all active tasks
    all_tasks = Task.query.filter_by(is_active=True).all()
    
    # Separate good and bad tasks
    good_tasks = [t for t in all_tasks if t.task_type == 'good']
    bad_tasks = [t for t in all_tasks if t.task_type == 'bad']
    
    # Get today's completions for current user
    today_completions = TaskCompletion.query.filter(
        TaskCompletion.user_id == current_user.id,
        db.func.date(TaskCompletion.completed_at) == today
    ).all()
    
    completed_task_ids = [c.task_id for c in today_completions]
    
    # Get current user's daily points
    daily_points = current_user.get_daily_points()
    
    return render_template('tasks/dashboard.html',
                         good_tasks=good_tasks,
                         bad_tasks=bad_tasks,
                         completed_task_ids=completed_task_ids,
                         daily_points=daily_points,
                         total_points=current_user.total_points)


@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create a new task."""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        task_type = request.form.get('task_type')  # 'good' or 'bad'
        points = request.form.get('points')
        requires_verification = request.form.get('requires_verification') == 'on'
        
        # Validation
        if not title or not task_type or not points:
            flash('Title, task type, and points are required.', 'danger')
            return redirect(url_for('tasks.create_task'))
        
        if task_type not in ['good', 'bad']:
            flash('Invalid task type.', 'danger')
            return redirect(url_for('tasks.create_task'))
        
        try:
            points = int(points)
        except ValueError:
            flash('Points must be a number.', 'danger')
            return redirect(url_for('tasks.create_task'))
        
        # For bad tasks, make points negative
        if task_type == 'bad' and points > 0:
            points = -points
        elif task_type == 'good' and points < 0:
            points = -points
        
        task = Task(
            user_id=current_user.id,
            title=title,
            description=description,
            task_type=task_type,
            points=points,
            requires_verification=requires_verification
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash(f'Task "{title}" created successfully!', 'success')
        return redirect(url_for('tasks.dashboard'))
    
    return render_template('tasks/create_task.html')


@tasks_bp.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    """Mark a task as completed."""
    task = Task.query.get_or_404(task_id)
    
    if not task.is_active:
        flash('This task is no longer active.', 'danger')
        return redirect(url_for('tasks.dashboard'))
    
    today = datetime.utcnow().date()
    
    # Check if already completed today
    existing = TaskCompletion.query.filter(
        TaskCompletion.user_id == current_user.id,
        TaskCompletion.task_id == task_id,
        db.func.date(TaskCompletion.completed_at) == today
    ).first()
    
    if existing:
        flash(f'You already completed "{task.title}" today!', 'info')
        return redirect(url_for('tasks.dashboard'))
    
    # Create completion record
    completion = TaskCompletion(
        user_id=current_user.id,
        task_id=task_id,
        needs_verification=task.requires_verification
    )
    
    # If no verification is required, mark as verified immediately
    if not task.requires_verification:
        completion.is_verified = True
        current_user.total_points += task.points
    
    db.session.add(completion)
    db.session.commit()
    
    if task.requires_verification:
        flash(f'Task "{task.title}" submitted for verification!', 'info')
    else:
        flash(f'Great! You completed "{task.title}" and earned {task.points} points!', 'success')
    
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/undo/<int:task_id>', methods=['POST'])
@login_required
def undo_task(task_id):
    """Undo a completed task (remove today's completion)."""
    task = Task.query.get_or_404(task_id)
    today = datetime.utcnow().date()
    
    completion = TaskCompletion.query.filter(
        TaskCompletion.user_id == current_user.id,
        TaskCompletion.task_id == task_id,
        db.func.date(TaskCompletion.completed_at) == today
    ).first()
    
    if completion:
        # Only refund points if it was verified
        if completion.is_verified:
            current_user.total_points -= task.points
        
        db.session.delete(completion)
        db.session.commit()
        flash(f'Undid completion of "{task.title}".', 'info')
    else:
        flash('Task completion not found.', 'danger')
    
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/pending-verifications')
@login_required
def pending_verifications():
    """Show tasks pending verification."""
    pending = TaskCompletion.query.filter(
        TaskCompletion.is_verified == False,
        TaskCompletion.needs_verification == True
    ).all()
    
    return render_template('tasks/pending_verifications.html', pending=pending)


@tasks_bp.route('/verify/<int:completion_id>/<action>', methods=['POST'])
@login_required
def verify_task(completion_id, action):
    """Approve or reject a task verification."""
    if action not in ['approve', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400
    
    completion = TaskCompletion.query.get_or_404(completion_id)
    
    # Check if user can verify (not the original completer)
    if completion.user_id == current_user.id:
        flash('You cannot verify your own completed tasks.', 'danger')
        return redirect(url_for('tasks.pending_verifications'))
    
    # Create or get verification record
    verification = TaskVerification.query.filter_by(
        task_completion_id=completion_id,
        verifier_id=current_user.id
    ).first()
    
    if verification:
        flash('You have already verified this task.', 'info')
        return redirect(url_for('tasks.pending_verifications'))
    
    verification = TaskVerification(
        task_completion_id=completion_id,
        task_id=completion.task_id,
        verifier_id=current_user.id
    )
    
    if action == 'approve':
        verification.approve()
        completion.is_verified = True
        completion.user.total_points += completion.task.points
        flash(f'Task verified and approved!', 'success')
    else:
        verification.reject()
        flash(f'Task verification rejected.', 'info')
    
    db.session.add(verification)
    db.session.commit()
    
    return redirect(url_for('tasks.pending_verifications'))
