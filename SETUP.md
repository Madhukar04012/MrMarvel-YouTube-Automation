# 🚀 MrMarvel YouTube Automation - Complete Setup Guide

## ⚡ Quick Start (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/Madhukar04012/MrMarvel-YouTube-Automation.git
cd MrMarvel-YouTube-Automation
```

### 2. Create Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and add your API keys
```

---

## 🔐 Step 1: Get YouTube API Credentials (10 min)

1. Go to: https://console.cloud.google.com
2. Click "Select a Project" → "New Project"
3. Project name: `MrMarvel-YouTube-Automation`
4. Wait for creation
5. Search for "YouTube Data API v3"
6. Click Enable
7. Click "Create Credentials" (OAuth 2.0, Desktop)
8. Download JSON file
9. Rename to `client_secret.json`
10. Place in project root

**First Run:**
```bash
python shorts_generator.py
# Opens browser for auth
# Creates token.json automatically
```

---

## 🔑 Step 2: Get Gemini API Key (2 min)

1. Go to: https://ai.google.dev
2. Click "Get API Key"
3. Select your Google project
4. Copy the key
5. Add to .env: `GEMINI_API_KEY=your_key_here`

---

## 📁 Step 3: Prepare Directories

```bash
# Create folders
mkdir gaming_videos shorts_output music logs

# Copy your gaming videos
cp /path/to/your/videos/* ./gaming_videos/

# Download background music from YouTube Audio Library
# Search "gaming" and download royalty-free tracks
# Place in ./music/ folder
```

---

## ▶️ Step 4: Run Your First Shorts Batch

```bash
# Generate 2 Shorts immediately
python shorts_generator.py

# Expected output:
# 🚀 Generating 2 Shorts...
# 📹 Extracting clip...
# 📝 Adding captions...
# 🎵 Adding music...
# ✅ Shorts created!
# 📤 Upload successful! Video ID: ...
```

---

## 📱 Step 5: Start Community Posts Automation

```bash
# In a new terminal
python community_posts_scheduler.py

# Runs daily at 11:00 AM IST
# Posts auto-generated polls & engagement content
```

---

## ⏰ Step 6: Setup Automated Scheduling (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add these lines:
# Daily Shorts at 9:00 AM IST (2:30 AM UTC)
30 2 * * * cd /path/to/MrMarvel-YouTube-Automation && python shorts_generator.py >> logs/shorts.log 2>&1

# Daily Community Posts at 11:00 AM IST
30 5 * * * cd /path/to/MrMarvel-YouTube-Automation && python community_posts_scheduler.py >> logs/posts.log 2>&1
```

---

## 🪟 Step 6 (Windows): Setup Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "YouTube Shorts Generator"
4. Trigger: Daily at 9:00 AM
5. Action: Start program
6. Program: `python.exe`
7. Arguments: `shorts_generator.py`
8. Repeat for `community_posts_scheduler.py` at 11:00 AM

---

## ✅ Verification

Check if everything works:

```bash
# Test Shorts generator
python -c "from shorts_generator import YouTubeShortsGenerator; print('✅ Shorts generator OK')"

# Test Community scheduler
python -c "from community_posts_scheduler import CommunityPostsScheduler; print('✅ Community scheduler OK')"

# Check logs
cat logs/shorts.log
cat logs/posts.log
```

---

## 🆘 Troubleshooting

**Issue: "No module named google"**
Solution: `pip install -r requirements.txt`

**Issue: "FFmpeg not found"**
Solution: Install FFmpeg
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`
- Windows: Download from ffmpeg.org

**Issue: "YouTube API quota exceeded"**
Solution: Wait 24 hours or increase quota in Google Cloud Console

**Issue: No shorts generated**
Solution: Ensure gaming_videos folder has .mp4, .mkv, or .avi files

---

## 📊 Expected Results (30 Days)

- ✅ 60+ Shorts published
- ✅ 30+ Community posts
- ✅ 3,000-5,000 views
- ✅ 400-500 new subscribers
- ✅ 200+ watch hours

---

## 🎯 Next Steps

1. ✅ Follow setup above
2. ✅ Run `python shorts_generator.py` first time
3. ✅ Monitor logs in ./logs/
4. ✅ Add more gaming videos to ./gaming_videos/
5. ✅ Track metrics in YouTube Analytics

---

**Questions? Check GitHub Issues or YouTube Documentation**
