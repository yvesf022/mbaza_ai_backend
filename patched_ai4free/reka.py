import requests

def Reka(prompt, model="reka-core"):
    try:
        response = requests.post(
            "https://reka.ai/api/chat",
            json={"prompt": prompt, "model": model}
        )
        return response.json().get("text", "").strip()
    except Exception as e:
        return f"Exception: {str(e)}"
