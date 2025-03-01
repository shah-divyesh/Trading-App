from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import lessons, ask_ai, trading, stock_tracker, recent_responses

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(lessons.router, prefix="/api", tags=["Lessons"])
app.include_router(ask_ai.router, prefix="/api/ask-ai", tags=["Ask AI"])
app.include_router(trading.router, prefix="/api/trading", tags=["Trading"])
app.include_router(stock_tracker.router, prefix="/api/stocks", tags=["Stock Tracker"])
app.include_router(recent_responses.router, prefix="/api", tags=["Recent AI Responses"])
app.include_router(ask_ai.router, prefix="/api/add-lesson", tags=["Add Question to database"])

@app.get("/")
def root():
    return {"message": "Welcome to the Stock Trading Learning App!"}