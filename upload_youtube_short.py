from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def upload_youtube_short(path):
    creds = Credentials.from_authorized_user_file("token.json")

    yt = build("youtube", "v3", credentials=creds)

    request_body = {
        "snippet": {
            "title": "🔥 Highlight from my livestream!",
            "description": "Live stream moment! #shorts",
            "tags": ["gaming", "live", "shorts"]
        },
        "status": {"privacyStatus": "public"}
    }

    media = MediaFileUpload(path, chunksize=-1, resumable=True)

    request = yt.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    print("📤 Uploaded to YouTube:", response["id"])


if __name__ == "__main__":
    upload_youtube_short("live_short.mp4")
