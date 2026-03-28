# 🎮 Multiplayer Tracker - Mac & Windows Setup Guide

## Overview
Play competitively with your friend across different operating systems (Mac and Windows). The app uses file-based data storage that can be synced via cloud services.

---

## ⚠️ Important: Cross-Platform Data Sharing

Since you're on **macOS** and your friend is on **Windows**, you need to sync the game data folder. Here are the recommended approaches:

### Option 1: Google Drive (Easiest) ⭐ RECOMMENDED
1. **Create a Google Drive folder**: `fitness-tracker-game`
2. **Install Google Drive Desktop**: 
   - Mac: https://support.google.com/drive/answer/7329379
   - Windows: https://support.google.com/drive/answer/7329379
3. **Create the app in Drive**: 
   - Move `multiplayer_tracker.py` to your shared Drive folder
   - The `multiplayer_data` folder will auto-sync between both computers
4. **Run from Drive**:
   - Mac: `cd ~/Google\ Drive\ \(file\ stream\)/My\ Drive/fitness-tracker-game && python3 multiplayer_tracker.py`
   - Windows: `cd "C:\Users\YourName\Google Drive\MyDrive\fitness-tracker-game" && python multiplayer_tracker.py`

### Option 2: Dropbox
1. **Create a Dropbox folder**: `fitness-tracker`
2. **Install Dropbox**:
   - Mac: https://www.dropbox.com/install?os=mac
   - Windows: https://www.dropbox.com/install?os=win
3. **Move files to Dropbox** and run from there

### Option 3: OneDrive
1. Similar to Dropbox - use Microsoft's cloud sync
2. Both Mac and Windows have native OneDrive support

### Option 4: Manual USB/Email Sync (Not Recommended)
- Before each session, manually share the `multiplayer_data` folder
- Not real-time, can cause conflicts

---

## 📋 Step-by-Step Setup

### For You (macOS):
```bash
# 1. Install Python 3 (if not already installed)
# Download from python.org or use: brew install python3

# 2. Verify Python is installed
python3 --version

# 3. Set up Google Drive folder (recommended)
# Move multiplayer_tracker.py to your Google Drive "My Drive" folder

# 4. Run the app
cd ~/Google\ Drive/My\ Drive/multiplayer_tracker
python3 multiplayer_tracker.py
```

### For Your Friend (Windows):
```bash
# 1. Install Python 3
# Download from python.org

# 2. Verify Python is installed
python --version

# 3. Set up Google Drive folder (same as you)
# Move multiplayer_tracker.py to their Google Drive "My Drive" folder

# 4. Run the app
cd C:\Users\YourName\Google Drive\My Drive\multiplayer_tracker
python multiplayer_tracker.py
```

---

## 🚀 First-Time Setup

**You BOTH need to do this (on your respective machines):**

1. **Launch the app**
   ```bash
   # Mac:
   python3 multiplayer_tracker.py
   
   # Windows:
   python multiplayer_tracker.py
   ```

2. **Player Creation** (You first):
   - Click "Create New Player"
   - Enter your name (e.g., "Krishan")
   - Click "Create New Player"

3. **Player Creation** (Your friend, same app or new instance):
   - Click "Create New Player" 
   - Enter their name (e.g., "John")
   - Click "Create New Player"

4. **Start Playing**:
   - You select your player, then select your friend as rival
   - Your friend does the same (selects themselves, then you as rival)
   - Both apps will now sync scores!

---

## 📊 How Data Syncs

- **Data Location**: `multiplayer_data/` folder in the app directory
- **What's Synced**:
  - `players.json` - Player profiles
  - `{player_id}_logs.json` - Daily progress
  - `{player_id}_weekly_logs.json` - Weekly progress
  - `{player_id}_monthly_logs.json` - Monthly progress
  - `{player_id}_tasks.json` - Task configurations

**Sync Timing**:
- Google Drive/Dropbox syncs every few seconds
- Check the "Leaderboard" tab to see latest scores
- Sometimes refresh by closing and reopening the app

---

## 🔧 Troubleshooting

### "File not found" errors
- Check that both computers have access to the shared folder
- Verify Google Drive/Dropbox is running and synced
- Wait 10-30 seconds for cloud sync to complete

### Data looks outdated
- Close and reopen the app
- Check cloud service status (Google Drive/Dropbox)
- Ensure both computers have the same Python files

### Scores not showing for friend
- Both players need to be created first
- Each player needs to select the other as rival
- Wait for cloud sync (usually instant)

### Different Python versions
- Use `python3` on Mac
- Use `python` on Windows
- Both should work with Python 3.7+

---

## 📱 Which Cloud Service to Choose?

| Service | Mac | Windows | Setup Time | Cost |
|---------|-----|---------|-----------|------|
| **Google Drive** | ⭐⭐⭐ | ⭐⭐⭐ | 5 min | Free |
| **Dropbox** | ⭐⭐⭐ | ⭐⭐⭐ | 5 min | Free (2GB) |
| **OneDrive** | ⭐⭐ | ⭐⭐⭐ | 5 min | Free (5GB) |

**Recommendation**: Use **Google Drive** - easiest on both Mac and Windows

---

## 🎮 Playing the Game

1. **Daily Tab**: See tasks side-by-side, click to complete, watch scores update
2. **Leaderboard Tab**: Compare overall rankings (Today/Week/Month/All-Time)
3. **Weekly/Monthly**: Configure long-term goals

**First person to highest score wins!** 🏆

---

## ❓ Questions?

If something doesn't work:
- Ensure both copies of the app are in the same cloud sync folder
- Verify both computers can access the cloud service
- Check that Python 3 is installed on both computers
- Try restarting the app to force a sync

Enjoy competing! 🎯
