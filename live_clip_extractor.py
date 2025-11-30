import os
import subprocess

def extract_live_clip(input_file, output_file, start_sec=0, duration_sec=60):
    """
    Cut a 60-second vertical clip from livestream recording.
    """
    cmd = [
        "ffmpeg",
        "-ss", str(start_sec),
        "-i", input_file,
        "-t", str(duration_sec),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,"
               "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        output_file
    ]

    subprocess.run(cmd, check=True)
    print(f"🎬 Clip created: {output_file}")


if __name__ == "__main__":
    extract_live_clip(
        "livestream.mp4",
        "live_short.mp4",
        start_sec=30,   # change to your moment timestamp
        duration_sec=60
    )
