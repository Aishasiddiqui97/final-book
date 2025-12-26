"""Data models for chat sessions."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ChatMode(str, Enum):
    """Enumeration for different chat modes."""
    FULL_BOOK = "full_book"
    SELECTED_TEXT = "selected_text"


class ChatSession(BaseModel):
    """Model for a chat session."""
    session_id: str
    created_at: datetime
    updated_at: datetime
    mode: ChatMode
    selected_text: Optional[str] = None
    user_id: Optional[str] = None  # Anonymous identifier, no personal data
    metadata: Optional[Dict[str, Any]] = None


class ChatMessage(BaseModel):
    """Model for a chat message."""
    message_id: str
    session_id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    citations: Optional[List[Dict[str, str]]] = None
    query_type: Optional[str] = None  # "general" or "selected_text"
    metadata: Optional[Dict[str, Any]] = None


class Citation(BaseModel):
    """Model for a citation."""
    citation_id: str
    chapter: str
    section: str
    subsection: Optional[str] = None
    url: Optional[str] = None
    text_preview: str
    relevance_score: float
    metadata: Optional[Dict[str, Any]] = None