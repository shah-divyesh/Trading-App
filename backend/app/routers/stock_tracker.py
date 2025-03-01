from fastapi import APIRouter
import requests
import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load API Key from .env

router = APIRouter()

# Initialize Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")  # Secure API key
BASE_URL = "https://www.alphavantage.co/query"

# Fetch stock price with Redis caching
@router.post("/stock_price")
def get_stock_price(data: dict):
    symbol = data.get("symbol", "").upper()
    cache_key = f"stock:{symbol}"
    cached_data = r.get(cache_key)

    if cached_data:
        return json.loads(cached_data)  # Return cached data if available
    
    # Fetch fresh stock price
    url = f"{BASE_URL}?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url).json()

    if "Global Quote" in response:
        stock_data = {
            "symbol": symbol,
            "price": response["Global Quote"]["05. price"]
        }
        r.setex(cache_key, 60, json.dumps(stock_data))  # Cache for 60 sec
        return stock_data
    
    return {"error": "Stock not found"}

# Fetch historical stock data
@router.post("/stock_history")
def get_stock_history(data: dict):
    symbol = data.get("symbol", "").upper()
    cache_key = f"history:{symbol}"
    cached_data = r.get(cache_key)

    if cached_data:
        return json.loads(cached_data)

    url = f"{BASE_URL}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url).json()

    if "Time Series (Daily)" in response:
        data = [
            {"date": date, "price": float(values["4. close"])}
            for date, values in response["Time Series (Daily)"].items()
        ][:30]

        r.setex(cache_key, 3600, json.dumps(data))  # Cache for 1 hour
        return data
    
    return {"error": "Stock history not found"}