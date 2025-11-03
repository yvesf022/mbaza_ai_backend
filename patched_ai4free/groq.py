import requests

def Groq(prompt, model="mixtral-8x7b"):
    try:
        response = requests.post(
            "https://api.groq.com/v1/chat/completions",  # Replace with working proxy if needed
            headers={"Authorization": "Bearer YOUR_KEY"},  # Only if you have one
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Groq error: {response.status_code} {response.text}"
    except Exception as e:
        return f"Groq exception: {str(e)}"
