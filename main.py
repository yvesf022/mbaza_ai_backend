from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from patched_ai4free.Cohere import Cohere as chat  # Gemini translation
from patched_ai4free.groq import Groq  # Groq for reasoning

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/translate")
def translate(text: str):
    # Step 1: Translate Kinyarwanda → English
    translated_input = chat("Translate this to English: " + text)

    # Step 2: Generate response in English using Groq
    response_en = Groq(translated_input)

    # Step 3: Translate English → Kinyarwanda
    translated_output = chat("Translate this to Kinyarwanda: " + response_en)

    return {"translated": translated_output}
