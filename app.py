from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

# Load catalog
with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/")
def root():
    return {"message": "SHL Assessment Recommendation API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):

    user_query = req.messages[-1].content.lower()

    recommendations = []

    for item in catalog:

        name = item.get("name", "").lower()

        if any(word in name for word in user_query.split()):

            recommendations.append({
                "name": item.get("name"),
                "url": item.get("url"),
                "test_type": item.get("test_type", "Unknown")
            })

    if recommendations:

        return {
            "reply": "Here are recommended SHL assessments.",
            "recommendations": recommendations[:10],
            "end_of_conversation": False
        }

    return {
        "reply": "Can you provide more details about the role or skills required?",
        "recommendations": [],
        "end_of_conversation": False
    }