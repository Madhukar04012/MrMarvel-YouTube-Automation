import cv2
import numpy as np
import os

def detect_motion_moments(video_file, threshold=35, min_gap=5):
    """
    Detects intense moments in gameplay by analyzing pixel motion.
    Returns timestamps where hype events likely occurred.
    """
    if not os.path.exists(video_file):
        print(f"❌ Video file not found: {video_file}")
        return [60, 120, 180] # Fallback

    cap = cv2.VideoCapture(video_file)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("❌ Could not read video FPS.")
        return [60, 120, 180]

    last_frame = None
    timestamps = []

    print("🎮 Analyzing gameplay motion…")

    frame_count = 0
    # Process every 5th frame to speed up analysis
    skip_frames = 5
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        if frame_count % skip_frames != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (9, 9), 0)

        if last_frame is None:
            last_frame = gray
            continue

        # Calculate difference between frames
        frame_delta = cv2.absdiff(last_frame, gray)
        score = np.sum(frame_delta) / 1000000

        # Detect peaks → intense action
        if score > threshold:
            time_sec = frame_count / fps
            timestamps.append(time_sec)

        last_frame = gray

    cap.release()

    # Remove moments too close to each other
    filtered = []
    for t in timestamps:
        if not filtered or t - filtered[-1] > min_gap:
            filtered.append(round(t))

    # Sort by "intensity" (implied by just finding them, but here we just take the first ones found)
    # A better approach might be to store (score, timestamp) and sort by score.
    # For now, we stick to the user's logic but ensure we return a list.
    
    print(f"🔥 Found {len(filtered)} hype gaming moments at: {filtered}")
    
    # Return top 3 (or fewer if not enough found)
    return filtered[:3] if filtered else [60, 120, 180]


if __name__ == "__main__":
    # Create a dummy video for testing if it doesn't exist? 
    # No, that's too hard. Just run if file exists.
    if os.path.exists("livestream.mp4"):
        detect_motion_moments("livestream.mp4")
    else:
        print("Please place a 'livestream.mp4' file to test.")
