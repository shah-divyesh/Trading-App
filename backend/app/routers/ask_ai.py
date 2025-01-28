from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()
HF_API_KEY = os.getenv("Trading_App")  # Make sure the API key is in your .env file

router = APIRouter()

# Initialize the Hugging Face Inference Client with the correct parameter
client = InferenceClient(token=HF_API_KEY)

class Question(BaseModel):
    question: str

@router.post("/")
async def ask_ai(data: Question):
    try:
        # Prepare input messages for the chat model
        messages = [
            {
                "role": "user",
                "content": data.question
            }
        ]

        # Perform inference using the Hugging Face model
        completion = client.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.2",  # Replace with the correct model name
            messages=messages,
            max_tokens=500
        )

        # Return the generated response
        return {"answer": completion["choices"][0]["message"]["content"]}

    except Exception as e:
        # Handle and log errors
        print(f"Unexpected error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal Server Error")