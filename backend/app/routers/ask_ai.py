from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()
HF_API_KEY = os.getenv("Trading_App")  # Ensure this API key is in your .env file
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # MongoDB Connection

router = APIRouter()

# Initialize Hugging Face Inference Client
client = InferenceClient(token=HF_API_KEY)

# MongoDB Connection
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["stock_ai"]
collection = db["ai_responses"]
ai_collection = db["ai_responses"]
lessons_collection = db["lessons"]


class Question(BaseModel):
    question: str
    
class LessonEntry(BaseModel):
    question: str
    answer: str
    level: str  # "basic", "intermediate", "advanced"

def get_lesson_level(question):
    """Determine lesson level based on keywords"""
    keywords = {
        "basic": ["what is", "how do", "beginner", "simple", "intro"],
        "intermediate": ["technical", "fundamental", "analysis", "strategy"],
        "advanced": ["algorithmic", "high-frequency", "machine learning", "quantitative"]
    }
    for level, words in keywords.items():
        if any(word in question.lower() for word in words):
            return level
    return None  # Prompt user if no match

@router.post("/")
async def ask_ai(data: Question):
    try:
        question = data.question.strip().lower()  # Normalize question format

        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Check if question exists in MongoDB
        existing_entry = collection.find_one({"question": question})

        if existing_entry:
            last_updated = existing_entry["updated_at"]
            one_day_ago = datetime.utcnow() - timedelta(days=1)

            # If the response is less than 1 day old, return cached response
            if last_updated > one_day_ago:
                return {"answer": existing_entry["answer"]}

        # Query the AI model if no valid cached response
        messages = [{"role": "user", "content": question}]
        completion = client.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=messages,
            max_tokens=500
        )

        new_answer = completion["choices"][0]["message"]["content"]

        # Store AI response in cache
        ai_collection.update_one(
            {"question": question},
            {"$set": {"answer": new_answer, "updated_at": datetime.utcnow()}},
            upsert=True
        )

        # Check if this question exists in lessons
        existing_lesson = lessons_collection.find_one({"question": question})
        if not existing_lesson:
            lesson_level = get_lesson_level(question)
            return {
                "answer": new_answer,
                "prompt_add_lesson": True,
                "suggested_level": lesson_level
            }

        return {"answer": new_answer}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/add-lesson")
async def add_lesson(lesson: LessonEntry):
    """Allows users to add AI-generated responses to lessons"""
    try:
        if lesson.level not in ["basic", "intermediate", "advanced"]:
            raise HTTPException(status_code=400, detail="Invalid level")

        # Log received data
        print(f"Received lesson: {lesson.dict()}")

        existing_lesson = lessons_collection.find_one({"question": lesson.question})
        if existing_lesson:
            print("Lesson already exists in the database.")
            return {"message": "Lesson already exists"}

        # Insert into MongoDB and log the operation
        result = lessons_collection.insert_one({
            "level": lesson.level,
            "question": lesson.question,
            "answer": lesson.answer,
            "timestamp": datetime.utcnow()
        })

        if result.inserted_id:
            print(f"Lesson insert result: {result.inserted_id}") 
            return {"message": "Lesson added successfully"}
        else:
            print("Insertion failed")
            raise HTTPException(status_code=500, detail="Failed to insert lesson")

    except Exception as e:
        print(f"Error inserting lesson: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")