from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_agent
import subprocess
import os
app = FastAPI()
# Run ingestion on startup if the database doesn't exist yet
if not os.path.exists("./chroma_db"):
    print("No database found, running ingestion...")
    subprocess.run(["python", "ingest.py"])
    print("Ingestion complete.")

# Allow the frontend HTML file to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    answer = ask_agent(request.message)
    return {"answer": answer}

@app.get("/")
def health_check():
    return {"status": "Kreo support agent is running"}  