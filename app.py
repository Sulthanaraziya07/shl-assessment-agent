from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

# Load catalog
with open("catalog.json", "r") as f:
    catalog = json.load(f)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):

    user_query = req.messages[-1].content.lower()

    matched_items = []

    for item in catalog:

        name = item["name"].lower()

        keywords = user_query.split()

        if any(word in name for word in keywords):
            matched_items.append(item)

    recommendations = []

    for item in matched_items[:5]:

        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]
        })

    return {
        "reply": "Here are recommended SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }