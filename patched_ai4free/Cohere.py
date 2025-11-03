import json
import tls_client

def Cohere(prompt, model="command-r", temperature=0.7):
    session = tls_client.Session(client_identifier="chrome_120")
    session.headers = {
        "authority": "cohere.com",
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://cohere.com",
        "referer": "https://cohere.com/",
        "user-agent": "Mozilla/5.0"
    }

    url = "https://cohere.com/api/v1/chat"
    payload = {
        "message": prompt,
        "chat_history": [],
        "model": model,
        "temperature": temperature,
        "stream": False
    }

    try:
        response = session.post(url, json=payload)
        return response.json().get("text", "").strip()
    except Exception as e:
        return f"Exception: {str(e)}"
