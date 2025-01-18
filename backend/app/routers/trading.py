from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Trade(BaseModel):
    stock: str
    price: float
    quantity: int

portfolio = []

@router.post("/buy")
async def buy_stock(trade: Trade):
    portfolio.append(trade)
    return {"message": f"Bought {trade.quantity} of {trade.stock} at ${trade.price}."}

@router.get("/portfolio")
async def get_portfolio():
    return {"portfolio": portfolio}