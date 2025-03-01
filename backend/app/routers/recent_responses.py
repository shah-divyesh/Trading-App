from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["stock_ai"]
collection = db["ai_responses"]

router = APIRouter()

@router.get("/recent-ai-responses")
async def get_recent_responses():
    """Fetch the most recent AI responses from MongoDB (limit: 10)"""
    responses = collection.find().sort("updated_at", -1).limit(10)
    
    data = []
    for response in responses:
        data.append({
            "question": response["question"],
            "answer": response["answer"],
            "updated_at": response["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
        })

    if not data:
        raise HTTPException(status_code=404, detail="No recent AI responses found.")

    return {"recent_responses": data}