import requests

def Cohere(prompt):
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Gemini error: {response.status_code} {response.text}"
    except Exception as e:
        return f"Gemini exception: {str(e)}"
