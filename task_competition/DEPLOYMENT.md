# Setup and Deployment Guide - Daily Task Competition

A complete guide for setting up, running, and deploying your Daily Task Competition platform.

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Running the Application](#running-the-application)
3. [Deployment on Render](#deployment-on-render)
4. [Database Configuration](#database-configuration)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### System Requirements
- **Python**: 3.8 or higher
- **pip**: Latest version
- **Virtual Environment**: Recommended but optional
- **OS**: macOS, Linux, or Windows

### Step 1: Clone/Download the Project
```bash
cd task_competition
```

### Step 2: Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Setup Environment File
```bash
cp .env.example .env
```

Edit `.env` if needed (defaults are fine for local development):
```
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///task_competition.db
DEBUG=True
```

### Step 5: Initialize Database (Create Sample Data)
```bash
python init_db.py
```

Output:
```
Creating sample users...
Created 3 users
Creating sample tasks...
Created 7 tasks

✅ Database initialized successfully!

Test Users:
  Username: alice | Password: password123
  Username: bob   | Password: password123
  Username: charlie | Password: password123
```

---

## Running the Application

### Option 1: Direct Execution
```bash
python app.py
```

Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Option 2: Using the Shell Script
```bash
chmod +x run.sh
./run.sh
```

### Option 3: Using Flask CLI
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Accessing the Application
- **URL**: http://localhost:5000
- **Login**: Use any test user (alice, bob, charlie) with password `password123`

---

## Deployment on Render

### Prerequisites
1. Render account (free tier available at render.com)
2. GitHub repository with your project code
3. PostgreSQL database connection string (from Render)

### Step 1: Create PostgreSQL Database on Render

1. Go to **render.com** and create account
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - Name: `task-competition-db`
   - Region: Choose closest to you
   - PostgreSQL Version: Latest
4. Create database
5. Copy the **External Database URL** (you'll need this)

### Step 2: Create Web Service on Render

1. Click **"New +"** → **"Web Service"**
2. **Connect Repository**:
   - Select your GitHub repository
   - Branch: main
3. **Configure Service**:
   - Name: `task-competition`
   - Environment: Python
   - Region: Same as database (important!)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`

### Step 3: Set Environment Variables

In Render dashboard, go to Environment section and add:

```
FLASK_ENV=production
SECRET_KEY=<GENERATE-THIS>
DATABASE_URL=<PASTE-YOUR-POSTGRES-URL>
DEBUG=False
```

#### Generate Strong Secret Key
```python
# Run this locally
python -c "import secrets; print(secrets.token_hex(32))"
```

Then copy the output and paste as `SECRET_KEY` in Render.

### Step 4: Deploy

1. Push code to GitHub main branch
2. Render automatically deploys on push
3. Check deployment logs in Render dashboard
4. Once "✓ Deploy successful", access your live site!

---

## Database Configuration

### Local Development (SQLite)
- Default: `sqlite:///task_competition.db`
- Auto-created on first run
- Great for testing and development
- Single file: `task_competition.db`

### Production (PostgreSQL)
- Set in Render PostgreSQL service
- Connection string format:
  ```
  postgresql://user:password@host:port/database
  ```
- More reliable and scalable
- Better for team collaboration

### Database Migrations

For production updates, you may want to add migrations:

```bash
pip install Flask-Migrate
flask db init
flask db migrate -m "Add new feature"
flask db upgrade
```

---

## Environment Variables

### Development (.env file)

```env
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=dev-secret-key-only-for-local-testing
DEBUG=True

# Database (SQLite for development)
DATABASE_URL=sqlite:///task_competition.db
```

### Production (Render Environment Settings)

```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=<your-generated-secret-key>
DEBUG=False

# Database (PostgreSQL)
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

---

## Project Structure for Deployment

```
task_competition/
├── app.py                 # Application factory
├── wsgi.py                # WSGI entry point for gunicorn
├── config.py              # Configuration
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment config
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # Full documentation
├── routes/
│   ├── auth.py
│   ├── tasks.py
│   └── leaderboard.py
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── tasks/
│   └── leaderboard/
└── static/
    ├── style.css
    └── script.js
```

---

## Troubleshooting

### "Module not found" Error

**Symptom**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt
```

### Database Errors

**Symptom**: Database locked or not found

**Solution**:
```bash
# Delete SQLite database and reinitialize
rm task_competition.db
python init_db.py
```

### Port Already in Use

**Symptom**: `Address already in use`

**Solution - Option 1**:
```bash
# Use different port
python app.py --port 5001
```

**Solution - Option 2** (Kill the existing process):
```bash
# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

### Static Files Not Loading

**Symptom**: CSS/JS not available, 404 errors

**Solution**:
```bash
# Ensure you're in project root
pwd  # should show: .../task_competition

# Check static files exist
ls -la static/

# Restart server
python app.py
```

### Login Issues

**Symptom**: Can't login even with test credentials

**Solution**:
```bash
# Recreate database with sample data
rm task_competition.db
python init_db.py
```

### Render Deployment Fails

**Check**:
1. PostgreSQL database is running
2. Connection string is correct (test locally with `DATABASE_URL`)
3. All environment variables are set
4. Python version is 3.8+ (check Render build logs)
5. No syntax errors (test locally first)

**Debug**:
```bash
# View Render logs
# In Render dashboard: Your Web Service → Logs
```

---

## Performance Tips

1. **Database Indexes**: Add indexes for frequently queried columns
2. **Caching**: Use Flask-Caching for leaderboards
3. **Connection Pooling**: Render PostgreSQL handles this
4. **Monitoring**: Enable Render's monitoring/error notifications

---

## Security Checklist

- [ ] Changed `SECRET_KEY` in production
- [ ] Using PostgreSQL in production (not SQLite)
- [ ] `FLASK_ENV=production`
- [ ] `DEBUG=False` in production
- [ ] HTTPS enabled (Render default)
- [ ] Environment variables set in Render (not in code)
- [ ] `.env` file in `.gitignore`

---

## Next Steps After Deployment

1. **Test the live site**: Login and create content
2. **Setup monitoring**: Enable alerts in Render
3. **Configure domain**: Add custom domain in Render settings
4. **Plan backups**: Enable Render backup for PostgreSQL
5. **Monitor performance**: Check metrics in Render dashboard

---

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Render Documentation](https://render.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**You're all set! Start competing! 🏆**
