from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import lessons, ask_ai, trading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(lessons.router, prefix="/api/lessons", tags=["Lessons"])
app.include_router(ask_ai.router, prefix="/api/ask", tags=["Ask AI"])
app.include_router(trading.router, prefix="/api/trading", tags=["Trading"])

@app.get("/")
def root():
    return {"message": "Welcome to the Stock Trading Learning App!"}