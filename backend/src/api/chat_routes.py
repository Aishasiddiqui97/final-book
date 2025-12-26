"""FastAPI routes for chat functionality."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio

from ..services.chat_service import ChatService, SelectedTextChatService
from ..services.content_ingestion import ContentIngestionService
from ..models.session_models import ChatMode


router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str
    mode: str = "full_book"  # "full_book" or "selected_text"
    selected_text: Optional[str] = None
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    session_id: str
    response: str
    citations: List[Dict[str, Any]]  # Changed to Any to accommodate more complex citation data
    sources: List[str]
    query: str
    mode: str


class IngestionRequest(BaseModel):
    """Request model for content ingestion."""
    source_path: str
    reindex: bool = False


class IngestionResponse(BaseModel):
    """Response model for content ingestion."""
    success: bool
    processed_files: int
    indexed_embeddings: int
    timestamp: str


# Lazy initialization of services to avoid issues at module load time
_chat_service = None
_selected_text_service = None
_ingestion_service = None

def get_chat_service():
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service

def get_selected_text_service():
    global _selected_text_service
    if _selected_text_service is None:
        _selected_text_service = SelectedTextChatService()
    return _selected_text_service

def get_ingestion_service():
    global _ingestion_service
    if _ingestion_service is None:
        _ingestion_service = ContentIngestionService()
    return _ingestion_service


@router.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for the RAG chatbot."""
    try:
        # Validate mode
        if request.mode not in ["full_book", "selected_text"]:
            raise HTTPException(status_code=400, detail="Mode must be 'full_book' or 'selected_text'")

        # Validate selected_text if mode is selected_text
        if request.mode == "selected_text" and not request.selected_text:
            raise HTTPException(status_code=400, detail="selected_text is required for selected_text mode")

        # Process the query
        chat_service = get_chat_service()
        result = await chat_service.process_query(
            query=request.query,
            session_id=request.session_id,
            mode=request.mode,
            selected_text=request.selected_text
        )

        return ChatResponse(**result)

    except Exception as e:
        # Handle specific error cases
        if "Not found in this book" in str(e) or "Not found in selected text" in str(e):
            # These are expected responses, not errors
            return ChatResponse(
                session_id=request.session_id or str(hash(request.query)),
                response=str(e),
                citations=[],
                sources=[],
                query=request.query,
                mode=request.mode
            )
        else:
            raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/ingest", response_model=IngestionResponse, tags=["ingestion"])
async def ingest_content(request: IngestionRequest):
    """Endpoint to ingest content from a directory."""
    try:
        ingestion_service = get_ingestion_service()
        result = await ingestion_service.ingest_directory(
            directory_path=request.source_path,
            reindex=request.reindex
        )

        return IngestionResponse(
            success=result["success"],
            processed_files=result["processed_files"],
            indexed_embeddings=result["indexed_embeddings"],
            timestamp=result["timestamp"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting content: {str(e)}")


@router.post("/retrieve", tags=["retrieval"])
async def retrieve_context(query: str, top_k: int = 5, selected_text: Optional[str] = None):
    """Endpoint to retrieve relevant context without generating a response."""
    from ..services.retrieval_service import RetrievalService

    retrieval_service = RetrievalService()
    context = await retrieval_service.retrieve_relevant_chunks(
        query, top_k=top_k, selected_text=selected_text
    )

    return {"context": context, "query": query}


@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "chat-api", "timestamp": "2025-12-26"}


# Additional endpoints for the selected-text functionality
@router.post("/chat-selected-text", response_model=ChatResponse, tags=["chat"])
async def chat_selected_text_endpoint(request: ChatRequest):
    """Specialized endpoint for selected-text-only QA."""
    if request.mode != "selected_text":
        raise HTTPException(status_code=400, detail="This endpoint is for selected_text mode only")

    if not request.selected_text:
        raise HTTPException(status_code=400, detail="selected_text is required")

    try:
        selected_text_service = get_selected_text_service()
        result = await selected_text_service.process_selected_text_query(
            query=request.query,
            selected_text=request.selected_text,
            session_id=request.session_id
        )

        return ChatResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing selected text query: {str(e)}")


@router.post("/validate-selected-text", tags=["validation"])
async def validate_selected_text_endpoint(query: str, selected_text: str):
    """Endpoint to validate if selected text is relevant to the query."""
    from ..services.selected_text_service import SelectedTextChatService

    service = SelectedTextChatService()
    is_relevant = await service.selected_text_service.validate_selected_text_relevance(query, selected_text)

    return {"is_relevant": is_relevant, "query": query}


# Update the main.py to include this router
# The router is already included in main.py with prefix "/api"