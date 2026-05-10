from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load catalog
with open("mapping.json", "r") as f:
    catalog = json.load(f)

# Load FAISS index
index = faiss.read_index("shl_index.faiss")

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

    vague_queries = [
        "assessment",
        "test",
        "hiring",
        "job",
        "developer"
    ]

    # Ask clarification for vague queries
    if user_query.strip() in vague_queries:

        return {
            "reply": "Can you provide more details about the role, skills, or personality traits you are hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Semantic search
    query_embedding = model.encode([user_query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, 5)

    recommendations = []

    for idx in indices[0]:

        item = catalog[idx]

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