from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from patched_ai4free.Cohere import Cohere as chat
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Phi-2 model (public, lightweight, no token needed)
model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.get("/translate")
def translate(text: str):
    # Step 1: Translate Kinyarwanda → English
    translated_input = chat("Translate this to English: " + text)

    # Step 2: Generate response in English
    response_en = generator(translated_input, max_length=300, do_sample=True)[0]["generated_text"]

    # Step 3: Translate English → Kinyarwanda
    translated_output = chat("Translate this to Kinyarwanda: " + response_en)

    return {"translated": translated_output}
