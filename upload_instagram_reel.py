import requests
import time

INSTAGRAM_USER_ID = "YOUR_IG_USER_ID"
ACCESS_TOKEN = "YOUR_LONG_LIVED_IG_TOKEN"

def upload_instagram_reel(video_path, caption="🔥 Live stream highlight! #reels"):
    # Step 1: Upload container
    print("⏳ Uploading to Instagram…")

    upload_url = (
        f"https://graph.facebook.com/v18.0/{INSTAGRAM_USER_ID}/media"
        f"?access_token={ACCESS_TOKEN}"
    )

    files = {
        "video": open(video_path, "rb")
    }

    data = {
        "media_type": "VIDEO",
        "caption": caption
    }

    res = requests.post(upload_url, data=data, files=files).json()
    print(res)

    creation_id = res.get("id")
    if not creation_id:
        print("❌ Upload failed:", res)
        return

    time.sleep(3)

    # Step 2: Publish
    publish_url = (
        f"https://graph.facebook.com/v18.0/{INSTAGRAM_USER_ID}/media_publish"
    )

    pub_res = requests.post(publish_url, data={
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }).json()

    print("📤 Uploaded to Instagram:", pub_res)


if __name__ == "__main__":
    upload_instagram_reel("live_short.mp4")
