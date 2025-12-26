"""Data models for textbook content and embeddings."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class TextbookContent(BaseModel):
    """Represents a chunk of textbook content."""
    content_id: str
    chapter: str
    section: str
    subsection: Optional[str] = None
    content_text: str
    content_type: str  # prose, code, callout, heading
    source_file: str
    hierarchy_path: str
    token_count: int
    metadata: Optional[Dict[str, Any]] = None

class EmbeddingChunk(BaseModel):
    """Represents a semantically coherent chunk with embedding."""
    chunk_id: str
    content_id: str
    text: str
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None
    semantic_boundary: bool = True

class ContentIngestionRequest(BaseModel):
    """Request model for content ingestion."""
    source_path: str
    recursive: bool = True
    file_pattern: str = "*.md"

class ContentIngestionResponse(BaseModel):
    """Response model for content ingestion."""
    success: bool
    processed_files: int
    indexed_chunks: int
    timestamp: datetime