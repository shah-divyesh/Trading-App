from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["stock_ai"]  # Database Name
collection = db["ai_responses"]  # Collection Name

def get_db():
    return collection  # Return database connection