from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# Define the expected structure of the incoming JSON
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_ai(request: QuestionRequest):
    return {"received": request.question}

@app.get("/")
def read_root():
    return {"message": "Hello Luis, your backend is working!"}
