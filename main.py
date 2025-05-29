from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

# Define the expected structure of the incoming JSON
class QuestionRequest(BaseModel):
    question: str

# API key in code 
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.post("/ask")
async def ask_ai(request: QuestionRequest):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct:free",  # Free tier model
        "messages": [
            {"role": "system", "content": "You are an assistant that only answers questions about Luis. Luis is a bilingual full-stack developer and AI builder. He co-founded Verskod and COMS, won Meta's Llama Impact Grant with BluEye ($100K), and regularly attends hackathons and conferences."},
            {"role": "user", "content": request.question}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body
        )

    result = response.json()
    ai_reply = result["choices"][0]["message"]["content"]
    return {"response": ai_reply}
