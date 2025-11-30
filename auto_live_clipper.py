import os
import time
from movement_detector import detect_motion_moments
from live_clip_generator import create_clip
from caption_generator import generate_captions
from upload_youtube_short import upload_youtube_short
from upload_instagram_reel import upload_instagram_reel

LIVESTREAM_FILE = "livestream.mp4"
TRANSCRIPT_FILE = "livestream_transcript.txt"

def main():
    print("🚀 Starting Auto Live Clipper...")
    
    # Check if files exist
    if not os.path.exists(LIVESTREAM_FILE):
        print(f"❌ Error: {LIVESTREAM_FILE} not found. Please place your livestream recording in this folder.")
        return

    print("🎮 Analyzing gameplay for hype moments…")
    timestamps = detect_motion_moments(LIVESTREAM_FILE)
    print(f"✅ Found moments at: {timestamps}")

    for i, ts in enumerate(timestamps):
        clip_filename = f"clip_{i+1}.mp4"
        
        print(f"\n--- Processing Clip {i+1} ---")

        # 1. Create clip
        create_clip(LIVESTREAM_FILE, clip_filename, ts)
        
        if not os.path.exists(clip_filename):
            print("❌ Clip generation failed. Skipping upload.")
            continue

        # 2. Caption generation
        caption_text = generate_captions(f"Clip at {ts} sec from livestream.")
        print(f"📝 Generated Caption: {caption_text}")

        # 3. Upload to YouTube
        try:
            upload_youtube_short(clip_filename)
        except Exception as e:
            print(f"⚠️ YouTube upload failed: {e}")

        # 4. Upload to Instagram
        try:
            upload_instagram_reel(clip_filename, caption=caption_text)
        except Exception as e:
            print(f"⚠️ Instagram upload failed: {e}")

    print("\n🎉 All clips processed!")


if __name__ == "__main__":
    main()
