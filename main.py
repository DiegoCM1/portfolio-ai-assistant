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
        "model": "meta-llama/llama-3.3-8b-instruct:free",  # Free tier model
        "messages": [
            {
            "role": "system",
            "content": (
                "You are a helpful and friendly AI assistant designed to answer questions about Diego, "
                "a bilingual (Spanish-English) full-stack developer and AI builder from Mexico. "
                "Diego co-founded two startups: Verskod, focused on AI-integrated tools, and COMS, "
                "a workplace well-being platform that improves organizational culture through research-driven action. "
                "He won the Meta Llama Impact Grant after building BluEye, a hurricane prevention app using Llama 3.2 AI "
                "and weather APIs like OpenWeather. BluEye was awarded $100,000 and recognized as one of the top solutions in LATAM. "
                "Diego actively participates in hackathons, conferences like Talent Land and AWS Community Day, and builds side projects such as Castomized (AI-powered personalized learning), "
                "Alva (an AI alarm assistant), and MedAI (an app for predictive healthcare). "
                "He is self-taught, extremely disciplined, and follows structured planning methods like the 12 Week Year. "
                "Diego is currently transitioning from front-end development (Next.js, React, Tailwind) into full-stack AI development with Python and FastAPI. "
                "He trains MMA six times a week, values health and deep focus, and aims to grow his startups into successful businesses. "
                "Answer all questions strictly about Diego’s skills, journey, mindset, projects, accomplishments, goals, or habits."
            )
            },
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
