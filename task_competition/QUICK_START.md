# Quick Start Guide - Daily Task Competition

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
cd task_competition
pip install -r requirements.txt
```

### 2. Initialize Database (Optional - with sample data)
```bash
python init_db.py
```

This creates 3 test users:
- Username: `alice` | Password: `password123`
- Username: `bob` | Password: `password123`
- Username: `charlie` | Password: `password123`

### 3. Run the Server
```bash
python app.py
```

The app will be available at: **http://localhost:5000**

---

## 🎯 First Steps

1. **Sign Up** (if you didn't use init_db.py)
   - Click "Create Account"
   - Fill in username, email, display name, and password
   - Click "Create Account"

2. **Create Your First Task**
   - Click "Create Task" in navigation
   - Add a task title (e.g., "Morning Exercise")
   - Choose type: "Good Task" for positive points
   - Set points (e.g., 10)
   - Click "Create Task"

3. **Complete a Task**
   - Go to Dashboard
   - Click "Complete" on any task in Good Tasks section
   - See your points increase!

4. **View Rankings**
   - Click "Leaderboard" to see all-time standings
   - Click "Today" tab to see daily standings

5. **Verify Others' Tasks** (coming soon with peer verification)
   - When someone submits a task requiring verification
   - Click "Verify Tasks" in navigation
   - Approve or reject their completion

---

## 📝 Task Types Explained

### Good Tasks
- **Positive habits** to build (e.g., exercise, reading, cooking)
- Award **positive points**
- Encourage self-improvement

### Bad Tasks
- **Negative habits** to avoid (e.g., no social media, early sleep)
- Apply **penalty points** (shown as negative)
- Help track behavioral goals

---

## 🎮 Example Task Setup

A typical friend group might have:

**Good Tasks:**
- Morning Jog (10 pts)
- Read for 30 min (5 pts)
- Drink 8 glasses water (3 pts)
- Prepare healthy meal (7 pts)

**Bad Tasks:**
- Stay up past 1 AM (-5 pts)
- Skip exercise (-10 pts)
- Eat junk food (-3 pts)

---

## 🔧 Deployment Checklist

Before deploying to Render:

- [ ] Create a `.env` file with:
  ```
  FLASK_ENV=production
  SECRET_KEY=<generate strong key>
  DATABASE_URL=<postgresURL>
  ```
- [ ] Test locally with `python app.py`
- [ ] Commit all files to Git
- [ ] Create Render Web Service
- [ ] Set environment variables in Render
- [ ] Deploy!

---

## 🐛 Common Issues

**"Module not found" error**
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`

**Database errors**
- Delete `task_competition.db`: `rm task_competition.db`
- Restart the server: `python app.py`

**Port already in use**
- Change port: `python app.py --port 5001`

---

## 📞 Need Help?

1. Check the full [README.md](README.md) for detailed documentation
2. Review the code comments in `routes/` and `models.py`
3. Test with sample data using `python init_db.py`

---

Happy competing! 🏆
