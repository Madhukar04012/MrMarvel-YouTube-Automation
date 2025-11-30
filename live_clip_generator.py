import subprocess
import os

def create_clip(input_video, output_video, timestamp, duration=60):
    """
    Creates 1080x1920 vertical short from livestream.
    """
    if not os.path.exists(input_video):
        print(f"❌ Input video not found: {input_video}")
        return

    cmd = [
        "ffmpeg",
        "-y", # Overwrite output file
        "-ss", str(timestamp),
        "-i", input_video,
        "-t", str(duration),
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        output_video,
    ]

    print(f"🎬 Creating clip at {timestamp}s → {output_video}")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Clip created successfully: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed: {e}")

if __name__ == "__main__":
    # Test
    create_clip("livestream.mp4", "test_clip.mp4", 30)
