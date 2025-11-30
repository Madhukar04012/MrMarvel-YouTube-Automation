#!/usr/bin/env python3
"""
Automated YouTube Community Posts Scheduler
Schedules daily polls, behind-the-scenes posts, and engagement content
"""

import os
import json
from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class CommunityPostsScheduler:
    def __init__(self):
        self.channel_id = "UCF1kVN_SXtMiPYsB3hP9mlQ"
        self.service = build("youtube", "v3", credentials=Credentials.from_authorized_user_file("token.json"))
        self.scheduler = BackgroundScheduler()
    
    def generate_poll_post(self, day):
        """Generate daily poll content"""
        polls = {
            "Monday": "🏁 THIS OR THAT: F1 Team? Ferrari or Red Bull?",
            "Tuesday": "🎮 Which game mode do you prefer? Career or Free Play?",
            "Wednesday": "❓ Hot Take: What's the hardest game mechanic?",
            "Thursday": "🏆 Challenge: Hardest difficulty or Easy mode?",
            "Friday": "🎯 Would you stream with us this weekend?",
            "Saturday": "⭐ Best gaming moment this week?",
            "Sunday": "📊 Subscribe and let's hit 1K together!"
        }
        return polls.get(day, "What's your gaming take?")
    
    def generate_caption(self, post_type):
        """Generate AI captions for posts"""
        prompts = {
            "poll": "Generate 2 engaging poll options for YouTube community (max 30 chars each)",
            "behind-scenes": "Create a behind-the-scenes caption for gaming setup (max 100 chars)",
            "tip": "Generate a quick gaming tip for community (max 80 chars)"
        }
        response = genai.generate_text(prompts.get(post_type, ""))
        return response.text[:150] if response else "Check this out!"
    
    def schedule_post(self, content, post_time="11:00"):
        """Schedule community post"""
        try:
            request_body = {
                "snippet": {
                    "textContent": content
                },
                "channelId": self.channel_id
            }
            request = self.service.activities().insert(part="snippet", body=request_body)
            response = request.execute()
            print(f"✅ Post scheduled: {content[:50]}...")
            return response
        except Exception as e:
            print(f"❌ Failed to schedule post: {e}")
            return None
    
    def run_daily_schedule(self):
        """Setup daily scheduling"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for i, day in enumerate(days):
            trigger = CronTrigger(day_of_week=i, hour=11, minute=0)
            content = self.generate_poll_post(day)
            self.scheduler.add_job(
                self.schedule_post,
                trigger,
                args=[content],
                id=f"post_{day.lower()}"
            )
            print(f"📅 Scheduled: {day} at 11:00 IST")
        
        self.scheduler.start()
        print("🚀 Community scheduler is running...")
    
    def post_manually(self, content):
        """Post manually without scheduling"""
        return self.schedule_post(content)

if __name__ == "__main__":
    scheduler = CommunityPostsScheduler()
    print("🚀 Starting community posts scheduler...")
    scheduler.run_daily_schedule()
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped")
