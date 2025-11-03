from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import MarianMTModel, MarianTokenizer, pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load translation models
en_to_rw_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-rw")
en_to_rw_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-rw")

rw_to_en_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-rw-en")
rw_to_en_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-rw-en")

# Load reasoning model (English)
reasoning = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

def translate_to_en(text):
    tokens = rw_to_en_tokenizer(text, return_tensors="pt", padding=True)
    output = rw_to_en_model.generate(**tokens)
    return rw_to_en_tokenizer.decode(output[0], skip_special_tokens=True)

def translate_to_rw(text):
    tokens = en_to_rw_tokenizer(text, return_tensors="pt", padding=True)
    output = en_to_rw_model.generate(**tokens)
    return en_to_rw_tokenizer.decode(output[0], skip_special_tokens=True)

@app.get("/translate")
def translate(text: str):
    try:
        # Step 1: Translate Kinyarwanda → English
        en_input = translate_to_en(text)

        # Step 2: Reasoning in English
        response_en = reasoning(en_input, max_length=200)[0]["generated_text"]

        # Step 3: Translate back to Kinyarwanda
        final_output = translate_to_rw(response_en)

        return {"translated": final_output}
    except Exception as e:
        return {"translated": f"Error: {str(e)}"}
