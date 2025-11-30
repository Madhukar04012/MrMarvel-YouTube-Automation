#!/usr/bin/env python3
"""
YouTube Shorts Auto-Generator from Gaming Videos
Extracts highlights, adds captions, music, and uploads automatically
"""

import os
import json
import subprocess
import random
from datetime import datetime
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class YouTubeShortsGenerator:
    def __init__(self):
        self.channel_id = "UCF1kVN_SXtMiPYsB3hP9mlQ"
        self.service = build("youtube", "v3", credentials=Credentials.from_authorized_user_file("token.json"))
    
    def extract_highlights(self, video_path, num_clips=5):
        """Extract highlight moments from gaming video"""
        highlights = []
        cmd = ["ffmpeg", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1:0", video_path]
        duration = float(subprocess.check_output(cmd).decode().strip())
        
        for i in range(num_clips):
            start_time = random.randint(0, int(duration - 65))
            highlights.append({"start": start_time, "duration": 60})
        return highlights
    
    def generate_captions(self, content_description):
        """Generate captions using Gemini"""
        prompt = f"Create 3 engaging YouTube Shorts captions (max 50 chars each) for: {content_description}"
        response = genai.generate_text(prompt)
        try:
            return json.loads(response.text).get("captions", ["🔥 Gaming #Shorts"])
        except:
            return ["🔥 Check this out! #Gaming #Shorts"]
    
    def create_shorts_clip(self, video_path, start_time, output_path, caption):
        """Create vertical 1080x1920 Shorts clip"""
        cmd = [
            "ffmpeg", "-i", video_path,
            "-ss", str(start_time), "-t", "60",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
            "-c:v", "libx264", "-preset", "fast", output_path
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Shorts created: {output_path}")
        return output_path
    
    def upload_shorts(self, video_path, metadata):
        """Upload Shorts to YouTube"""
        try:
            request_body = {
                "snippet": {
                    "title": metadata["title"],
                    "description": metadata["description"],
                    "tags": metadata["tags"],
                    "categoryId": "20"
                },
                "status": {"privacyStatus": "public"}
            }
            media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
            request = self.service.videos().insert(part="snippet,status", body=request_body, media_body=media)
            response = request.execute()
            print(f"✅ Upload successful! Video ID: {response['id']}")
            return response["id"]
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def run_daily_batch(self, num_shorts=2):
        """Generate and upload daily Shorts batch"""
        print(f"🚀 Generating {num_shorts} Shorts...")
        video_dir = "./gaming_videos"
        os.makedirs("./shorts_output", exist_ok=True)
        
        if not os.path.exists(video_dir):
            print(f"❌ Video directory not found: {video_dir}")
            return
        
        video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.mkv', '.avi'))]
        if not video_files:
            print("❌ No videos found!")
            return
        
        for i in range(num_shorts):
            video_file = random.choice(video_files)
            video_path = os.path.join(video_dir, video_file)
            highlights = self.extract_highlights(video_path, 1)
            captions = self.generate_captions(video_file)
            
            output_path = f"./shorts_output/shorts_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.mp4"
            self.create_shorts_clip(video_path, highlights[0]["start"], output_path, captions[0])
            
            metadata = {"title": f"🔥 Gaming Highlight | {captions[0][:40]}", "description": "Check out this gaming moment!\n\nSubscribe for more!", "tags": ["gaming", "shorts", "f1", "snowrunner"]}
            self.upload_shorts(output_path, metadata)

if __name__ == "__main__":
    generator = YouTubeShortsGenerator()
    generator.run_daily_batch(num_shorts=2)
