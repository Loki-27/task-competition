# 🎮 Multiplayer Daily Tracker - Beautiful Edition

A completely redesigned multiplayer activity tracker with a modern, beautiful interface!

## ✨ What's New

### 🎨 Beautiful Modern Design
- **Modern Dark Theme**: GitHub-inspired dark color scheme that's easy on the eyes
- **Clean UI Elements**: Professional-looking buttons, cards, and layouts
- **Visual Feedback**: Color-coded tasks (green for rewards, red for penalties)
- **Responsive Layout**: Automatically adjusts to your window size

### ⚔️ Competitive Gameplay
- **Split-View Daily Tasks**: See your tasks vs your friend's tasks side-by-side
- **Live Score Display**: Real-time score comparison with winner indicator
- **Beautiful Scoreboard**: Shows current scores with visual winner highlight
- **Task Cards**: Modern card design with status checkmarks and point values

### 🏆 Features
- ✅ Create multiple player profiles
- ✅ Choose a rival to compete against
- ✅ Click tasks to mark as complete
- ✅ Automatic score calculation
- ✅ Data persistence (saved to `multiplayer_data/` folder)
- ✅ Easy Mac ↔ Windows synchronization via cloud storage

## 🚀 How to Run

```bash
cd /Users/krishan/stuf/tracker
python3 multiplayer_tracker.py
```

## 📋 How to Use

### 1️⃣ **Welcome Screen**
- Create a new player profile or select existing one
- Enter your name and create account

### 2️⃣ **Select Your Rival**
- Choose which friend to compete against
- Click "⚔ Battle [Name]" to start

### 3️⃣ **Daily Battle**
- See your tasks on the left, your friend's tasks on the right
- **Click any task to mark it complete** ✓
- Completed tasks show green checkmark
- Your score updates instantly
- Points are added based on task value:
  - Green tasks = +points (rewards)
  - Red tasks = -points (penalties)

### 4️⃣ **Scoreboard Display**
- Real-time score comparison
- Winner is highlighted in yellow
- Loser gets "Catch up!" message

### 5️⃣ **Navigation**
- Click "← Back to Players" to switch profiles or rivals
- Use "Leaderboard" tab to view detailed statistics (coming soon)

## 🎮 Game Features

### Task System
Each task has:
- **Name**: What you need to do
- **Points**: How many points it's worth
- **Status**: Completed (✓) or Incomplete (○)
- **Type**: Reward (green) or Penalty (red)

### Default Tasks
- Morning Exercise (15 pts)
- Study/Work (20 pts)
- Reading (10 pts)
- Meditation (5 pts)
- Good Meal (5 pts)
- Sleep 8hrs (10 pts)
- Skipped Workout (-15 pts)
- Junk Food (-10 pts)

## 🔄 Cross-Platform Setup (Mac + Windows)

**Best Option: Google Drive**

1. Both players move `multiplayer_tracker.py` to shared Google Drive folder
2. Install Google Drive sync on both computers
3. Run from the same location
4. Data automatically syncs when either player updates progress

**Commands:**
```bash
# Mac
cd ~/Google\ Drive/My\ Drive/fitness-tracker
python3 multiplayer_tracker.py

# Windows
cd "C:\Users\YourName\Google Drive\My Drive\fitness-tracker"
python multiplayer_tracker.py
```

See **MULTIPLAYER_SETUP.md** for complete cloud sync instructions.

## 📁 File Structure

```
tracker/
├── multiplayer_tracker.py      # Main app (run this!)
├── MULTIPLAYER_SETUP.md        # Setup guide
└── multiplayer_data/           # Auto-created
    ├── players.json            # All player profiles
    ├── [player_id]_tasks.json  # Tasks for each player
    └── [player_id]_logs.json   # Daily progress for each player
```

## 🎨 Color Scheme

- **Accent Blue** (#58A6FF): Main title, scores
- **Accent Green** (#3FB950): Rewards, completed tasks
- **Accent Red** (#F85149): Penalties, defeats
- **Accent Yellow** (#D29922): Today's winner highlight
- **Dark Background**: Professional dark theme

## 💾 Data Storage

All progress is saved automatically:
- Tasks saved when created
- Scores saved when updated
- Data stored as JSON files
- Easy to backup or sync via cloud

## 🐛 Troubleshooting

**App won't start?**
- Make sure Python 3.7+ is installed
- Run: `python3 multiplayer_tracker.py`

**Scores not updating?**
- Click a task to save progress
- Close and reopen to sync

**No rival players showing?**
- Have your friend create their account first
- Both need accounts in `players.json`

**Cloud sync not working?**
- Ensure Google Drive/Dropbox is actually syncing
- Wait 10-30 seconds for file sync
- Check that both computers access the same folder

## 📝 Notes

- This is the clean, beautiful version of multiplayer tracker
- All data is stored locally in the `multiplayer_data/` folder
- Perfect for friendly competition with your friend
- Works on Mac, Windows, and Linux

**Enjoy competing! 🏆**
