from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai4free import chat, search
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Mistral model locally
model_id = "mistralai/Mistral-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.get("/translate")
def translate(text: str):
    # Step 1: Translate Kinyarwanda → English
    translated_input = chat("Translate this to English: " + text)

    # Step 2: Optional web search (if needed)
    search_results = search(translated_input)

    # Step 3: Generate response in English
    response_en = generator(translated_input + "\n" + search_results, max_length=300, do_sample=True)[0]["generated_text"]

    # Step 4: Translate English → Kinyarwanda
    translated_output = chat("Translate this to Kinyarwanda: " + response_en)

    return {"translated": translated_output}
