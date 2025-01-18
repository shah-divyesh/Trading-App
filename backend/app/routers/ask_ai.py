from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/")
async def ask_ai(data: Question):
    try:
        # Use gpt-3.5-turbo instead of gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Switching to GPT-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a stock trading teacher."},
                {"role": "user", "content": data.question},
            ],
        )
        return {"answer": response['choices'][0]['message']['content']}
    except Exception as e:
        # Log the exception for debugging
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")