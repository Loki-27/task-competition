# Developer Guide - Daily Task Competition

A comprehensive guide for understanding and extending the codebase.

## Architecture Overview

The application follows a modular Flask architecture:

```
Request → Flask App → Blueprint Routes → Database Models → Response
                           ↓
                      (auth, tasks, leaderboard)
```

## Code Structure

### 1. Application Factory Pattern (`app.py`)

```python
def create_app(config_name=None):
    """Create Flask app with all extensions initialized."""
    # Creates Flask instance
    # Initializes SQLAlchemy
    # Sets up Flask-Login
    # Registers blueprints
    # Creates database tables
    return app
```

**Key Points:**
- All extensions initialized in `create_app()`
- Database tables auto-created on startup
- Blueprints registered for routing
- Login manager configured

### 2. Database Models (`models.py`)

#### User Model
```python
class User(UserMixin, db.Model):
    id, username, email, password_hash, display_name
    total_points, created_at, is_active
    
    Methods:
    - set_password(password)       # Hash password
    - check_password(password)     # Verify password
    - get_daily_points()           # Calculate today's points
    - get_leaderboard_rank()       # Get user ranking
```

#### Task Model
```python
class Task(db.Model):
    id, user_id, title, description
    points, task_type ('good'/'bad')
    requires_verification
    
    Methods:
    - get_today_completions()      # Get today's completions
```

#### TaskCompletion Model
```python
class TaskCompletion(db.Model):
    id, user_id, task_id
    completed_at, is_verified, needs_verification
    
    Purpose: Track when users complete tasks
```

#### TaskVerification Model
```python
class TaskVerification(db.Model):
    id, task_completion_id, verifier_id
    status ('pending'/'approved'/'rejected')
    
    Methods:
    - approve()                    # Mark as approved
    - reject()                     # Mark as rejected
```

### 3. Routes (Blueprints in `routes/`)

#### Authentication Routes (`routes/auth.py`)
```python
/auth/signup          - Register new user
/auth/login           - Login user
/auth/logout          - Logout user
/auth/profile         - View user profile
```

**Key Logic:**
- Password validation (min 6 chars)
- Duplicate username/email check
- Session management with remember_me
- User stats calculation on profile

#### Task Routes (`routes/tasks.py`)
```python
/tasks/dashboard                    - View all tasks
/tasks/create                       - Create new task
/tasks/complete/<task_id>           - Mark task completed
/tasks/undo/<task_id>               - Revert completion
/tasks/pending-verifications        - View tasks needing approval
/tasks/verify/<completion_id>/<action> - Approve/reject
```

**Key Logic:**
- Daily task deduplication (one completion per task per day)
- Points awarded immediately or after verification
- Verification prevents self-approval
- Undo refunds points

#### Leaderboard Routes (`routes/leaderboard.py`)
```python
/leaderboard/              - All-time rankings
/leaderboard/daily         - Today's top performers
```

**Key Logic:**
- Dynamic rank calculation
- Daily point aggregation
- Real-time sorting by total_points

### 4. Templates (Jinja2)

#### Base Template Structure
```html
base.html
├── Navigation bar (with current_user)
├── Flash messages
├── Content block
└── Footer

{% block content %} - Where page content goes
```

#### Template Inheritance
```html
{% extends "base.html" %}
{% block content %}
    <!-- Page-specific HTML -->
{% endblock %}
```

### 5. Configuration (`config.py`)

```python
class Config:
    SECRET_KEY              # Encryption key
    SQLALCHEMY_DATABASE_URI # Database connection
    SESSION_COOKIE_*        # Security settings
    DEBUG, TESTING          # Environment flags
```

---

## Common Development Tasks

### 1. Add a New Column to User

```python
# In models.py
class User(db.Model):
    # ... existing columns ...
    bio = db.Column(db.String(500))  # NEW!

# Delete database and reinitialize
# db.create_all() will add the column
```

### 2. Add a New Route

```python
# In routes/tasks.py (or new file)
@tasks_bp.route('/new-endpoint', methods=['GET', 'POST'])
@login_required  # If authentication required
def new_endpoint():
    if request.method == 'POST':
        # Handle form submission
        return redirect(url_for('tasks.dashboard'))
    
    return render_template('tasks/template.html')
```

### 3. Add a New Template

```html
<!-- In templates/tasks/new_page.html -->
{% extends "base.html" %}

{% block title %}Page Title - Daily Task Competition{% endblock %}

{% block content %}
<div class="container">
    <!-- Your HTML here -->
</div>
{% endblock %}
```

### 4. Query the Database

```python
# In any route
from models import User, Task, TaskCompletion

# Get single user
user = User.query.get(user_id)
user = User.query.filter_by(username='alice').first()

# Get multiple
all_users = User.query.all()
active_users = User.query.filter_by(is_active=True).all()

# Order and limit
top_users = User.query.order_by(User.total_points.desc()).limit(10).all()

# Count
user_count = User.query.count()

# With join
user_tasks = Task.query.filter_by(user_id=current_user.id).all()
```

### 5. Update Database Record

```python
# Modify and save
user = User.query.get(user_id)
user.display_name = "New Name"
user.total_points += 10
db.session.commit()

# Or bulk update
User.query.filter_by(is_active=False).update({'total_points': 0})
db.session.commit()
```

### 6. Add Input Validation

```python
# In route handler
if not all([title, points, task_type]):
    flash('All fields required', 'danger')
    return redirect(request.referrer)

if len(password) < 6:
    flash('Password too short', 'warning')
    return redirect(url_for('auth.signup'))
```

### 7. Style a Component

```css
/* In static/style.css */
.my-component {
    background-color: #f0f0f0;
    padding: 1rem;
    border-radius: 0.375rem;
}

/* Responsive */
@media (max-width: 768px) {
    .my-component {
        padding: 0.5rem;
    }
}
```

---

## Key Patterns Used

### 1. Login Required Pattern
```python
from flask_login import login_required

@app.route('/protected')
@login_required
def protected():
    # User must be logged in
    return render_template('page.html')
```

### 2. Flash Messages Pattern
```python
flash('Success message', 'success')  # Green
flash('Error message', 'danger')     # Red
flash('Info message', 'info')        # Blue

# In template:
{% for category, message in get_flashed_messages(with_categories=true) %}
    <div class="alert alert-{{ category }}">{{message}}</div>
{% endfor %}
```

### 3. Form Handling Pattern
```python
if request.method == 'POST':
    field = request.form.get('field_name')
    # Validate
    # Process
    # Redirect
    return redirect(url_for('route_name'))

return render_template('form.html')
```

### 4. Bootstrap Grid Pattern
```html
<div class="row">
    <div class="col-lg-8"><!-- 8 out of 12 columns --></div>
    <div class="col-lg-4"><!-- 4 out of 12 columns --></div>
</div>

<!-- Responsive -->
<div class="col-md-6 col-lg-4"><!-- Changes at breakpoints --></div>
```

---

## Testing Checklist

Before deploying new features:

- [ ] Create new user, test signup
- [ ] Login with test user
- [ ] Create a task
- [ ] Complete a task
- [ ] Check points updated
- [ ] View leaderboard
- [ ] Test peer verification
- [ ] Undo a task
- [ ] Logout and back in

---

## Performance Considerations

### Database Query Optimization
```python
# ❌ Bad: N+1 query problem
for task in tasks:
    creator = User.query.get(task.user_id)  # Query per task!

# ✅ Good: Use relationship
task.creator.display_name  # Already loaded via relationship
```

### Caching (Future Enhancement)
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/leaderboard')
@cache.cached(timeout=300)  # Cache 5 minutes
def leaderboard():
    return render_template('leaderboard.html')
```

### Database Indexing
```python
# In models.py
username = db.Column(db.String(80), unique=True, nullable=False, index=True)
# Speeds up username lookups
```

---

## Security Best Practices

### 1. Never Trust User Input
```python
# ❌ Bad
sql = f"SELECT * FROM users WHERE username = '{username}'"

# ✅ Good - SQLAlchemy prevents SQL injection
user = User.query.filter_by(username=username).first()
```

### 2. Always Hash Passwords
```python
# ✅ Good
user.set_password(password)  # Uses werkzeug.security

# ✅ Verify password
if user.check_password(password):
    login_user(user)
```

### 3. Use Secure Cookies
```python
# In config.py
SESSION_COOKIE_SECURE = True      # HTTPS only
SESSION_COOKIE_HTTPONLY = True    # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection
```

### 4. Protect Forms with CSRF
```html
<!-- In Flask, automatic with Flask-WTF -->
<!-- Or manual token -->
<form method="POST">
    {{ csrf_token() }}
    <!-- form fields -->
</form>
```

---

## Deployment Checklist

### Before Production
- [ ] Change SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set FLASK_ENV = production
- [ ] Configure secure session cookies
- [ ] Test with production database locally
- [ ] Run all tests
- [ ] Clear browser cache

### After Deployment
- [ ] Test signup/login
- [ ] Test task creation
- [ ] Monitor error logs
- [ ] Check database backups
- [ ] Setup alerting

---

## Extending the Project

### Add Achievements System
```python
class Achievement(db.Model):
    id, name, description, icon
    condition  # e.g., "total_points > 100"

# Award achievement
achievement = Achievement.query.filter_by(name='First Task').first()
if # condition met:
    user.achievements.append(achievement)
```

### Add Task Categories
```python
class Category(db.Model):
    id, name, icon, color

class Task(db.Model):
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
```

### Add Email Notifications
```python
from flask_mail import Mail, Message

mail = Mail(app)

def notify_user(user, message):
    msg = Message(subject='Task Update', recipients=[user.email])
    mail.send(msg)
```

---

## Debugging Tips

### Print Debug Info
```python
from flask import current_app

current_app.logger.info(f"User login: {user.username}")
current_app.logger.error(f"Database error: {error}")
```

### Database Inspection
```python
# In Flask shell
flask shell
>>> from models import *
>>> User.query.all()
>>> Task.query.filter_by(user_id=1).all()
```

### Flask Debug Toolbar
```python
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)
# Shows SQL queries, templates, etc.
```

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/orm/)
- [Bootstrap Components](https://getbootstrap.com/docs/5.0/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)

---

**Happy coding! 🚀**
