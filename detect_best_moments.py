import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def detect_moments_from_transcript(transcript_file):
    """
    Takes livestream transcript (.txt) and returns timestamps of hype moments.
    """
    if not os.path.exists(transcript_file):
        print(f"⚠️ Transcript file not found: {transcript_file}")
        return [60, 180, 300] # Fallback

    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    # Use Gemini Pro model
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Analyze this livestream transcript and identify the TOP 3 hype, funny, intense, or emotional moments.
    Return ONLY a valid JSON object with the timestamps in seconds. Do not include markdown formatting like ```json.
    
    Transcript:
    {transcript[:10000]} # Limit context to avoid token limits if transcript is huge

    Format:
    {{
      "moments": [
        {{ "timestamp": 123 }},
        {{ "timestamp": 842 }},
        {{ "timestamp": 1550 }}
      ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean up potential markdown code blocks
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
            
        data = json.loads(result_text)
        return [m["timestamp"] for m in data["moments"]]
    except Exception as e:
        print(f"⚠️  AI detection failed: {e}. Using fallback moments.")
        return [60, 180, 300]

if __name__ == "__main__":
    # Create a dummy transcript if it doesn't exist for testing
    if not os.path.exists("livestream_transcript.txt"):
        with open("livestream_transcript.txt", "w") as f:
            f.write("0:00 Stream starting...\n1:00 This game is intense!\n2:00 OH MY GOD WHAT A PLAY!\n5:00 GG everyone.")
            
    print(detect_moments_from_transcript("livestream_transcript.txt"))
