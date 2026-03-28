from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup."""
    if current_user.is_authenticated:
        return redirect(url_for('tasks.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        display_name = request.form.get('display_name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validation
        if not all([username, email, display_name, password, password_confirm]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('auth.signup'))
        
        if password != password_confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.signup'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.signup'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            display_name=display_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created successfully! Welcome, {display_name}!', 'success')
        login_user(user)
        return redirect(url_for('tasks.dashboard'))
    
    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('tasks.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('This account has been deactivated.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=request.form.get('remember_me'))
        flash(f'Welcome back, {user.display_name}!', 'success')
        return redirect(url_for('tasks.dashboard'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """Display user profile."""
    daily_points = current_user.get_daily_points()
    rank = current_user.get_leaderboard_rank()
    
    return render_template('auth/profile.html', 
                         daily_points=daily_points,
                         rank=rank)
