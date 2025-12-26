"""Service for handling selected-text-only QA functionality."""
import re
from typing import List, Dict, Any, Optional
from .embedding_service import EmbeddingService
from .chunking_service import ChunkingService


class SelectedTextService:
    """Service for handling queries specifically against user-selected text."""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.chunker = ChunkingService(min_tokens=100, max_tokens=500)  # Smaller chunks for selected text

    async def process_selected_text_query(self, query: str, selected_text: str) -> List[Dict[str, Any]]:
        """Process a query against selected text only."""
        if not selected_text or not selected_text.strip():
            return []

        # For selected text mode, we need to find the most relevant parts of the selected text
        # relative to the query

        # Simple approach: if the selected text is short, return it as is
        # If it's long, we might want to chunk it and find the most relevant chunks
        if len(selected_text) < 1000:  # If less than ~500 words
            return [{
                'chunk_id': 'selected_text_chunk',
                'text': selected_text,
                'metadata': {'source': 'user_selected_text'},
                'similarity_score': 1.0,
                'source': 'Selected Text',
                'token_count': len(selected_text.split())
            }]
        else:
            # For longer selected text, we'll chunk it and potentially find relevant parts
            # For now, we'll return the full selected text
            return [{
                'chunk_id': 'selected_text_chunk',
                'text': selected_text,
                'metadata': {'source': 'user_selected_text'},
                'similarity_score': 0.8,  # High relevance since user selected it
                'source': 'Selected Text',
                'token_count': len(selected_text.split())
            }]

    async def find_relevant_segments(self, query: str, selected_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find the most relevant segments within the selected text for the query."""
        # This is a more sophisticated version that would identify specific segments
        # within the selected text that are most relevant to the query

        # For now, we'll implement a simple keyword-based approach
        # In a more advanced implementation, we could:
        # 1. Chunk the selected text into smaller segments
        # 2. Generate embeddings for those segments
        # 3. Compare with the query embedding
        # 4. Return the most relevant segments

        # Simple keyword matching approach
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        text_segments = self._split_text_into_segments(selected_text)

        scored_segments = []
        for i, segment in enumerate(text_segments):
            segment_words = set(re.findall(r'\b\w+\b', segment.lower()))
            overlap = len(query_words.intersection(segment_words))
            score = overlap / len(query_words) if query_words else 0

            scored_segments.append({
                'chunk_id': f'selected_segment_{i}',
                'text': segment,
                'metadata': {'source': 'user_selected_text_segment'},
                'similarity_score': score,
                'source': f'Selected Text Segment {i+1}',
                'token_count': len(segment.split())
            })

        # Sort by score and return top_k
        scored_segments.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scored_segments[:top_k]

    def _split_text_into_segments(self, text: str, max_length: int = 300) -> List[str]:
        """Split text into segments of approximately max_length words."""
        words = text.split()
        segments = []

        for i in range(0, len(words), max_length):
            segment = ' '.join(words[i:i + max_length])
            segments.append(segment)

        return segments

    async def validate_selected_text_relevance(self, query: str, selected_text: str) -> bool:
        """Validate if the selected text is relevant to the query."""
        # Simple validation: check if query terms appear in selected text
        query_lower = query.lower()
        text_lower = selected_text.lower()

        query_words = set(re.findall(r'\b\w+\b', query_lower))
        text_words = set(re.findall(r'\b\w+\b', text_lower))

        # If at least 30% of query words appear in the selected text, consider it relevant
        if not query_words:
            return True  # If no query words, we can't determine relevance

        overlap = len(query_words.intersection(text_words))
        relevance_score = overlap / len(query_words)

        return relevance_score >= 0.3  # 30% threshold


class SelectedTextChatService:
    """Enhanced service specifically for selected-text QA with validation."""

    def __init__(self):
        self.selected_text_service = SelectedTextService()

    async def process_query_with_validation(self, query: str, selected_text: str) -> List[Dict[str, Any]]:
        """Process query with validation that selected text is relevant."""
        # Validate if selected text is relevant to query
        is_relevant = await self.selected_text_service.validate_selected_text_relevance(query, selected_text)

        if not is_relevant:
            # Return a special response indicating the selected text isn't relevant
            return [{
                'chunk_id': 'no_relevant_text',
                'text': selected_text,
                'metadata': {'source': 'user_selected_text', 'warning': 'selected_text_not_relevant'},
                'similarity_score': 0.0,
                'source': 'Selected Text',
                'token_count': len(selected_text.split())
            }]

        # Process normally if relevant
        return await self.selected_text_service.process_selected_text_query(query, selected_text)

    async def get_context_for_selected_text(self, query: str, selected_text: str) -> List[Dict[str, Any]]:
        """Get context specifically for selected text QA."""
        return await self.selected_text_service.find_relevant_segments(query, selected_text)


# Example usage
async def process_selected_text_query(query: str, selected_text: str) -> List[Dict[str, Any]]:
    """Convenience function to process selected text query."""
    service = SelectedTextChatService()
    return await service.process_query_with_validation(query, selected_text)