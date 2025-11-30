import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_captions(context):
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Create a short caption for this gaming moment (max 40 characters).
    Style: hype, fun, engaging. Return JSON only.

    Context:
    {context}

    Output Format:
    {{
        "caption": "text here"
    }}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up markdown
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text)["caption"]
    except Exception as e:
        print(f"⚠️ Caption generation error: {e}")
        return "🔥 Insane moment!"

if __name__ == "__main__":
    print(generate_captions("Player gets a triple kill in Valorant"))
