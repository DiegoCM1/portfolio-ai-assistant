from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# ✅ Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Allow frontend access from local + deployed portfolio
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

# ✅ Define expected request schema
class QuestionRequest(BaseModel):
    question: str

# ✅ Define the /ask endpoint
@app.post("/ask")
async def ask_ai(request: QuestionRequest):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",  # Swap here if using llama-4-scout
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful and friendly AI assistant designed to answer questions about Diego, "
                    "a bilingual (Spanish-English) full-stack developer and AI builder from Mexico. "
                    "Diego co-founded two startups: Verskod (AI-integrated tools) and COMS (well-being at work). "
                    "He won Meta’s Llama Impact Grant ($100K) with BluEye, a hurricane prevention app using Llama 3.2 and weather APIs. "
                    "Diego also created Castomized (AI learning), Alva (AI alarm), and MedAI (predictive health). "
                    "He’s transitioning from front-end (React, Tailwind) to full-stack AI (Python, FastAPI), trains MMA 6 days/week, "
                    "and applies structured planning (like the 12 Week Year). "
                    "Only answer questions about Diego’s experience, habits, goals, or projects."
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

        # ✅ Log raw result for debugging (comment out in prod if needed)
        print("OpenRouter raw response:", result)

        if "choices" in result:
            ai_reply = result["choices"][0]["message"]["content"]
            return {"response": ai_reply}
        else:
            raise HTTPException(
                status_code=500,
                detail=f"OpenRouter response missing 'choices': {result.get('error', result)}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
