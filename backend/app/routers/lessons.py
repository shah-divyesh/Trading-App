from fastapi import APIRouter

router = APIRouter()

lessons = {
    "basic": [
        "What is a stock?",
        "How do stocks work?",
        "Basic stock market terminologies.",
    ],
    "intermediate": [
        "What is technical analysis?",
        "Understanding candlestick patterns.",
        "Moving averages and RSI.",
    ],
    "advanced": [
        "Options and futures trading.",
        "Risk management techniques.",
        "Creating and backtesting a strategy.",
    ],
}

@router.get("/{level}")
async def get_lessons(level: str):
    if level not in lessons:
        return {"error": "Invalid level. Choose 'basic', 'intermediate', or 'advanced'."}
    return {"level": level, "lessons": lessons[level]}