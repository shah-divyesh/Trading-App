from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["stock_ai"]
collection = db["lessons"]

router = APIRouter()

# Pydantic model for lesson entries
class LessonEntry(BaseModel):
    level: str  # "basic", "intermediate", "advanced"
    question: str
    answer: str

# Store lessons in MongoDB (Ensures no duplicates)
@router.post("/store-lessons/")
async def store_lessons():
    """Stores predefined lessons if they don't already exist"""
    lessons_data = [
        {"level": "basic", "question": "What is a stock?", "answer": "A stock represents ownership in a company."},
        {"level": "basic", "question": "How do stocks work?", "answer": "Stocks are traded in the stock market, where prices fluctuate based on demand and supply."},
        {"level": "basic", "question": "Basic stock market terminologies?", "answer": "Common terms include IPO, dividends, and market capitalization."},
        {"level": "intermediate", "question": "What are technical indicators?", "answer": "Technical indicators help traders analyze price movements using past data."},
        {"level": "intermediate", "question": "What is fundamental analysis?", "answer": "Fundamental analysis evaluates a company's financial health using earnings, assets, and liabilities."},
        {"level": "advanced", "question": "What is algorithmic trading?", "answer": "Algorithmic trading uses automated systems to execute trades at high speeds based on predefined criteria."},
    ]

    inserted_count = 0
    for lesson in lessons_data:
        existing_lesson = collection.find_one({"level": lesson["level"], "question": lesson["question"]})
        if not existing_lesson:
            collection.insert_one(lesson)
            inserted_count += 1

    return {"message": f"{inserted_count} new lessons added"}

# Fetch lessons by level
@router.get("/lessons/{level}")
async def get_lessons(level: str):
    """Fetches lessons dynamically by level"""
    valid_levels = ["basic", "intermediate", "advanced"]
    if level not in valid_levels:
        raise HTTPException(status_code=400, detail="Invalid level. Choose from: basic, intermediate, advanced.")

    lessons = list(collection.find({"level": level}, {"_id": 0, "question": 1, "answer": 1}))

    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found for this level.")

    return {"lessons": lessons}