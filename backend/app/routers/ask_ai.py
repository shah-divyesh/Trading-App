# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import requests
# import os
# from dotenv import load_dotenv
# import traceback

# # Load environment variables
# load_dotenv()
# HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/mistral-7b"  # Update with Mistral 7B model
# HF_API_TOKEN = os.getenv("Trading_App")  # Use the appropriate environment variable name
# print(f"Loaded token: {HF_API_TOKEN}")

# router = APIRouter()

# # Add Authorization headers
# headers = {
#     "Authorization": f"Bearer {HF_API_TOKEN}"
# }

# class Question(BaseModel):
#     question: str

# @router.post("/")
# async def ask_ai(data: Question):
#     try:
#         # Add a structured prompt for better results
#         prompt = f"As a knowledgeable assistant, answer this question concisely: {data.question}"
        
#         # Send the request to Hugging Face Inference API
#         response = requests.post(
#             HF_API_URL,
#             headers=headers,
#             json={"inputs": prompt}  # Mistral requires "inputs" for text input
#         )
#         response.raise_for_status()
        
#         # Parse the response
#         result = response.json()
#         if isinstance(result, dict) and "error" in result:
#             raise HTTPException(status_code=400, detail=result["error"])
        
#         # Return the generated text
#         return {"answer": result[0]["generated_text"]}

#     except requests.exceptions.HTTPError as e:
#         print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
#         raise HTTPException(status_code=e.response.status_code, detail="Hugging Face API error.")
#     except requests.exceptions.RequestException as e:
#         print(f"Request exception: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to communicate with Hugging Face API")
#     except Exception as e:
#         print(f"Unexpected error: {traceback.format_exc()}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

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