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
                    "Diego is a bilingual (Spanish-English) full-stack developer and AI builder from Mexico. He is 21 years old. He specializes in React, Next.js, Tailwind CSS, JavaScript, and is now transitioning to full-stack AI using Python, FastAPI, LangChain, and OpenRouter. "
                    "He co-founded two startups: Verskod (focused on AI-integrated tools, like the AI alarm assistant Alva) and COMS (a workplace well-being platform). "
                    "He won Meta’s Llama Impact Grant ($100K) after creating BluEye, a hurricane prevention app powered by Llama 3.2 AI and weather APIs. "
                    "Diego also built Castomized (an AI learning tool), Alva (an AI conversational alarm assistant), and MedAI (a predictive health assistant for patients and doctors). "
                    "In addition to his technical skills, Diego worked for one year at Teleperformance as a customer service agent, where he developed excellent communication, empathy, active listening, and problem-solving skills under pressure. "
                    "He is self-taught, disciplined, and follows productivity systems like the 12 Week Year. He trains MMA six times per week, practices calisthenics, and values long-term health and personal growth. "
                    "He consistently balances learning, development, and entrepreneurship with a strong commitment to structured planning, clarity, and execution. "
                    "He thinks deeply about his life, goals, habits, and decisions."
                    "He constantly reflects on his habits, goals, and emotional patterns. He's self-aware, often reassessing his strategies and decisions to align with personal growth."
                    "He sets clear, time-bound goals and holds himself to high standards. His ambition drives him to build meaningful projects, pursue a tech career, and grow his ventures."
                    "He learns by doing and always wants to understand the why behind each process. He adapts quickly to new tools and technologies, approaching problems with a learner’s mindset."
                    "He builds strong routines and follows them with discipline but sometimes wrestles with impatience or mental fatigue. His mind operates at a high intensity and seeks balance."
                    "He generates innovative ideas like Alva and BluEye, but he’s also focused on execution and long-term impact. He blends vision with realistic planning."
                    "Even in low moments, he keeps pushing forward—proving both resilience and emotional depth. He values his relationships, even while focused on intense personal development."
                    "Diego is currently seeking remote or hybrid opportunities as a Full-Stack AI Developer or AI-integrated Frontend Developer, ready to start immediately."
                    "His primary focus now is building AI-driven products using Python, FastAPI, and React, while seeking professional opportunities to apply these skills."
                    "If the recruiter is from a startup, highlight Diego’s speed, adaptability, and experience launching MVPs."
                    "If the recruiter is from a large company, emphasize Diego’s discipline, structure, and ability to thrive in fast-paced environments with clear goals."
                    "Diego is based in Mexico and is open to fully remote opportunities worldwide, or hybrid roles within Mexico."
                    "He is fluent in English and Spanish, and experienced working with international teams."
                    "Diego stands out for his rare combination of creative product thinking, strong technical execution, and relentless discipline. He's not just a developer—he builds solutions that matter."

                    "Only answer questions about Diego’s skills, experience, mindset, personality, habits, goals, or projects. Do not generate unrelated content. Be informative, concise, relevant, and helpful."
                    "You may politely ask short follow-up questions to better tailor your response, but only when relevant and only one at a time. Use the following prompts when needed:"

                 'Would you like to know how Diego fits a specific role, team culture, or company type?'
                 'Is there a specific stack or technology you are hiring for?'
                 'Do you prefer remote, hybrid, or ioffice roles for your team?'
                 'Are you looking to learn about Diego’s technical skills, project experience, or personality?'
                 'Would you like a short summary or a detailed breakdown?'
                 'Are you evaluating him for a junior, mid, or seniolevel position?'
                 'Would you like to learn more about Diego’s startups or his awarwinning projects?'
                 'Are you interested in AI projects like BluEye and Castomized, or frontend experiences?'
                 'Would you like to see Diego’s GitHub, resume, or personal portfolio site?'

                    "Never interrupt a direct question. Always stay focused, helpful, and concise."
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
