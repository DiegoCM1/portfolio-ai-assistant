from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# ✅ Allow frontend access from local + Vercel deploy
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.1.8:1287",
        "https://diegocm2025-portfolio.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request body model
class QuestionRequest(BaseModel):
    question: str

# ✅ Load API key from .env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ✅ POST endpoint
@app.post("/ask")
async def ask_ai(request: QuestionRequest):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",  # or llama-4-scout
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful and friendly AI assistant designed to answer questions about Diego, "
                    "a bilingual (Spanish-English) full-stack developer and AI builder from Mexico. "
                    "Diego co-founded two startups: Verskod, focused on AI-integrated tools, and COMS, "
                    "a workplace well-being platform. He won Meta’s Llama Impact Grant ($100K) with BluEye, "
                    "a hurricane prevention app using Llama 3.2 and weather APIs. "
                    "Diego actively builds projects like Castomized (AI learning), Alva (AI alarm), and MedAI (predictive health), "
                    "and is currently shifting from front-end (React, Tailwind) to full-stack AI (Python, FastAPI). "
                    "He’s disciplined, trains MMA 6 days/week, and applies structured planning like the 12 Week Year. "
                    "Answer only questions about Diego’s skills, journey, habits, or projects."
                )
            },
            {"role": "user", "content": request.question}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body
            )

        result = response.json()

        # ✅ Handle errors from OpenRouter
        if "choices" in result:
            ai_reply = result["choices"][0]["message"]["content"]
            return {"response": ai_reply}
        else:
            raise HTTPException(status_code=500, detail=f"OpenRouter error: {result.get('error', 'Unknown')}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
