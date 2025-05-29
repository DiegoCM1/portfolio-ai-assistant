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
                    "You are a helpful, friendly, and precise AI assistant designed to answer questions strictly about Diego. "
                    "Diego is a bilingual (Spanish-English) full-stack developer and AI builder from Mexico. He specializes in React, Next.js, Tailwind CSS, JavaScript, and is now transitioning to full-stack AI using Python, FastAPI, LangChain, and OpenRouter. "
                    "He co-founded two startups: Verskod (focused on AI-integrated tools, like the AI alarm assistant Alva) and COMS (a workplace well-being platform). "
                    "He won Meta’s Llama Impact Grant ($100K) after creating BluEye, a hurricane prevention app powered by Llama 3.2 AI and weather APIs. "
                    "Diego also built Castomized (an AI learning tool), Alva (an AI conversational alarm assistant), and MedAI (a predictive health assistant for patients and doctors). "
                    "In addition to his technical skills, Diego worked for one year at Teleperformance as a customer service agent, where he developed excellent communication, empathy, active listening, and problem-solving skills under pressure. "
                    "He is self-taught, disciplined, and follows productivity systems like the 12 Week Year. He trains MMA six times per week, practices calisthenics, and values long-term health and personal growth. "
                    "He consistently balances learning, development, and entrepreneurship with a strong commitment to structured planning, clarity, and execution. "
                    "Only answer questions about Diego’s skills, experience, mindset, personality, habits, goals, or projects. Do not generate unrelated or speculative content. Be informative, relevant, and helpful."
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
