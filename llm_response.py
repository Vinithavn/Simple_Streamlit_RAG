import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

grok_api_key = os.getenv("GROK_OPENROUTER_API_KEY")

def generate_grok(query):

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {grok_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps({
        "model": "x-ai/grok-4-fast:free",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": query
            },
            
            ]
        }
        ],
        
    })
    )
    return response.json()["choices"][0]["message"]["content"]