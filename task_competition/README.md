# Daily Task Competition Platform

A web-based task competition system for small groups of friends. Track your daily habits, compete on points, and validate each other's progress!

## 🎯 Core Features

### User Authentication
- Simple signup/login system for your friend group
- Secure password hashing with Werkzeug
- Session management with Flask-Login

### Task Management
- **Good Tasks**: Complete positive actions to earn points
- **Bad Tasks**: Avoid bad habits for penalty deductions
- Create unlimited tasks with descriptions and custom point values
- Daily task reset with persistent total points

### Validation System
- **Auto-approved tasks**: Instant point awards for standard tasks
- **Peer-verification**: Optional approval system where friends must validate claimed tasks before points are awarded

### Leaderboard
- Real-time all-time rankings based on total points
- Daily leaderboard showing today's top performers
- Automatic rank calculation

### Data Persistence
- Tasks reset every 24 hours
- Points accumulate over time
- Historical tracking of all completions

## 🛠️ Technical Stack

- **Backend**: Flask 3.0 with Python 3.8+
- **Database**: SQLAlchemy ORM with SQLite (development) or PostgreSQL (production)
- **Frontend**: Bootstrap 5 with responsive design
- **Authentication**: Flask-Login with werkzeug password hashing
- **Deployment**: Gunicorn + Render

## 📋 Project Structure

```
task_competition/
├── app.py                 # Flask application factory
├── config.py              # Configuration management
├── models.py              # SQLAlchemy database models
├── wsgi.py                # WSGI entry point for production
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── Procfile              # Heroku/Render deployment config
├── run.sh                # Local development startup script
├── routes/
│   ├── __init__.py
│   ├── auth.py           # Authentication routes (signup, login, logout)
│   ├── tasks.py          # Task management routes (create, complete, verify)
│   └── leaderboard.py    # Leaderboard and ranking routes
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── 404.html          # 404 error page
│   ├── 500.html          # 500 error page
│   ├── auth/
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── profile.html
│   ├── tasks/
│   │   ├── dashboard.html
│   │   ├── create_task.html
│   │   └── pending_verifications.html
│   └── leaderboard/
│       └── index.html
└── static/
    ├── style.css         # Custom CSS styles
    └── script.js         # Custom JavaScript
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Local Setup

1. **Clone the repository**
   ```bash
   cd task_competition
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```
   
   Or use the provided script:
   ```bash
   chmod +x run.sh && ./run.sh
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🚀 Deployment on Render

### Prerequisites
- Render account (free tier available)
- GitHub repository with your code

### Steps

1. **Create a PostgreSQL database** on Render (Free tier)
   - Save the connection string

2. **Create a new Web Service** on Render
   - Connect your GitHub repository
   - Set the following environment variables in Render dashboard:
     ```
     FLASK_ENV=production
     SECRET_KEY=<generate-a-strong-random-key>
     DATABASE_URL=<your-postgres-connection-string>
     ```

3. **Configure build and start commands**
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn wsgi:app`

4. **Deploy**
   - Render will automatically deploy on push to main branch

## 🔐 Security Notes

1. **Change SECRET_KEY**: Generate a strong secret key in production
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Use HTTPS**: Always use HTTPS in production (Render handles this)

3. **Database URL**: Use PostgreSQL in production, not SQLite

4. **Secure cookies**: Session cookies are automatically secure in production

## 📚 API Routes

### Authentication
- `GET/POST /auth/login` - User login
- `GET/POST /auth/signup` - User registration
- `GET /auth/logout` - User logout
- `GET /auth/profile` - View user profile

### Tasks
- `GET /tasks/dashboard` - Main dashboard
- `GET/POST /tasks/create` - Create new task
- `POST /tasks/complete/<task_id>` - Mark task as completed
- `POST /tasks/undo/<task_id>` - Undo task completion
- `GET /tasks/pending-verifications` - View tasks pending peer approval
- `POST /tasks/verify/<completion_id>/<action>` - Approve/reject verification

### Leaderboard
- `GET /leaderboard/` - All-time leaderboard
- `GET /leaderboard/daily` - Today's leaderboard

## 🎮 Usage Guide

### For Users
1. **Sign up** with your friend group
2. **Create tasks** - good tasks for habits to start, bad tasks for habits to avoid
3. **Complete tasks** - click "Complete" on the dashboard daily
4. **Earn points** - get instant points for auto-approved tasks
5. **Request verification** - submit tasks requiring peer approval
6. **Verify others** - approve or reject friends' submitted tasks
7. **Compete** - check the leaderboard to see standings

### For Administrators
- The system is self-managed by the group
- All users can create tasks for others to complete
- No admin panel needed for small friend groups

## 🧪 Testing

Run the development server and test:
1. Create an account
2. Create both good and bad tasks
3. Complete tasks from the dashboard
4. Verify another user's tasks
5. Check leaderboard rankings

## 🐛 Troubleshooting

### Database issues
- Delete `task_competition.db` to reset the database
- Ensure `DATABASE_URL` is set correctly

### Import errors
- Make sure all requirements are installed: `pip install -r requirements.txt`
- Verify you're in the virtual environment

### Static files not loading
- Ensure you're running from the project root directory
- Check that `static/` folder exists with CSS and JS files

## 📄 License

Open source for educational and personal use.

## 🤝 Contributing

Feel free to customize and extend this project!

### Feature ideas
- Time-based task streaks
- Achievement badges
- Weekly/monthly reports
- Mobile app integration
- Task categories and filtering
- Recurring tasks

## 💡 Tips for Your Group

1. **Set consistent point values** - agree on point scales across the group
2. **Use clear descriptions** - make tasks specific and measurable
3. **Regular verification** - review pending verifications daily
4. **Weekly reviews** - discuss progress and adjust tasks
5. **Have fun** - keep it light and competitive!

---

**Happy competing! 🏆**
