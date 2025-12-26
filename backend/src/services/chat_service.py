"""Chat service for handling conversations with context injection."""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from .retrieval_service import RetrievalService, SelectedTextService
from .prompt_service import PromptService, CitationService
from ..models.session_models import ChatSession, ChatMessage, ChatMode


class ChatService:
    """Service for handling chat conversations with context injection."""

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.selected_text_service = SelectedTextService()
        self.prompt_service = PromptService()
        self.citation_service = CitationService()

    async def process_query(self, query: str, session_id: str = None, mode: str = "full_book",
                           selected_text: Optional[str] = None) -> Dict[str, Any]:
        """Process a user query and return a response with citations."""
        # Create a new session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())

        # Retrieve relevant context based on mode
        if mode == "selected_text" and selected_text:
            context_chunks = await self.selected_text_service.process_selected_text_query(
                query, selected_text
            )
        else:
            context_chunks = await self.retrieval_service.retrieve_relevant_chunks(
                query, selected_text=selected_text
            )

        # Generate response using RAG
        response_data = await self.prompt_service.generate_response(
            query, context_chunks, mode, selected_text
        )

        # Format the response
        result = {
            "session_id": session_id,
            "response": response_data["response"],
            "citations": response_data["citations"],
            "sources": response_data["sources"],
            "query": query,
            "mode": mode
        }

        return result

    async def create_session(self, mode: ChatMode = ChatMode.FULL_BOOK,
                           selected_text: Optional[str] = None) -> ChatSession:
        """Create a new chat session."""
        session_id = str(uuid.uuid4())
        now = datetime.now()

        session = ChatSession(
            session_id=session_id,
            created_at=now,
            updated_at=now,
            mode=mode,
            selected_text=selected_text
        )

        return session

    async def get_conversation_history(self, session_id: str) -> List[ChatMessage]:
        """Get conversation history for a session (placeholder - in real implementation would use DB)."""
        # In a real implementation, this would fetch from a database
        # For now, we return an empty list
        return []

    async def validate_response_quality(self, response: str, context_chunks: List[Dict[str, Any]]) -> bool:
        """Validate that the response is grounded in the provided context (basic check)."""
        # This is a basic check - in a more sophisticated system, you'd use more advanced validation
        response_lower = response.lower()

        # Check if key terms from context appear in response
        context_text = " ".join([chunk.get('text', '')[:200] for chunk in context_chunks[:3]]).lower()

        # Simple overlap check - if there's no overlap, it might be hallucinated
        context_words = set(context_text.split()[:50])  # First 50 words
        response_words = set(response_lower.split()[:100])  # First 100 words

        overlap = context_words.intersection(response_words)

        # If less than 10% of response words overlap with context, flag for review
        if len(overlap) == 0:
            return False

        return True


class SelectedTextChatService:
    """Service specifically for handling selected-text-only chat functionality."""

    def __init__(self):
        self.chat_service = ChatService()

    async def process_selected_text_query(self, query: str, selected_text: str, session_id: str = None) -> Dict[str, Any]:
        """Process a query specifically against selected text."""
        return await self.chat_service.process_query(
            query,
            session_id=session_id,
            mode="selected_text",
            selected_text=selected_text
        )


# Example usage function
async def handle_chat_query(query: str, mode: str = "full_book", selected_text: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to handle a chat query."""
    service = ChatService()
    return await service.process_query(query, mode=mode, selected_text=selected_text)


if __name__ == "__main__":
    # Example usage
    # import asyncio
    # result = asyncio.run(handle_chat_query("What is Physical AI?", mode="full_book"))
    # print(result)
    pass