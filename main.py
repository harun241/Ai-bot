from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai_agent import run_agent
import uvicorn

app = FastAPI(title="AI Chat Bot API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Chat Bot API"}

@app.post("/chat")
def chat(request: ChatRequest):
    response = run_agent(request.user_input)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
