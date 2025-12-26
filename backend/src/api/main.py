"""Main FastAPI application for RAG Chatbot."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from .chat_routes import router as chat_router

app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG chatbot integrated with Docusaurus textbook",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-12-26"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)