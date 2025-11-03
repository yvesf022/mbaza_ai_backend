import requests

def Groq(prompt, model="mixtral-8x7b"):
    try:
        response = requests.post(
            "https://groq.com/api/chat",
            json={"prompt": prompt, "model": model}
        )
        return response.json().get("text", "").strip()
    except Exception as e:
        return f"Exception: {str(e)}"
