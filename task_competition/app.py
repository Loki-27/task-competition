import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, current_user, login_required
from .models import db, User
from .config import config
from datetime import datetime

# Import route blueprints
from .routes.auth import auth_bp
from .routes.tasks import tasks_bp
from .routes.leaderboard import leaderboard_bp
from .routes.goals import goals_bp

def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(goals_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Home route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('tasks.dashboard'))
        return redirect(url_for('auth.login'))
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
