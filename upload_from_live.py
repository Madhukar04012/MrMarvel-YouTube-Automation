from live_clip_extractor import extract_live_clip
from upload_youtube_short import upload_youtube_short
from upload_instagram_reel import upload_instagram_reel

# 1. Create short from livestream
extract_live_clip(
    "livestream.mp4",
    "live_short.mp4",
    start_sec=120,   # adjust timestamp
    duration_sec=60
)

# 2. Upload to YouTube
upload_youtube_short("live_short.mp4")

# 3. Upload to Instagram
upload_instagram_reel("live_short.mp4")

print("🎉 Done! Uploaded to YouTube + Instagram.")
