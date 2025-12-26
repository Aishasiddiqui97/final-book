"""Hybrid retrieval service for semantic + keyword search."""
import asyncio
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import PointStruct, ScoredPoint
from .embedding_service import EmbeddingService
from ..config.vector_db import get_vector_db_client, get_collection_name


class RetrievalService:
    """Service for retrieving relevant content using hybrid search."""

    def __init__(self):
        self.vector_client = get_vector_db_client()
        self.collection_name = get_collection_name()
        self.embedding_service = EmbeddingService()

    async def retrieve_relevant_chunks(self, query: str, top_k: int = 5, selected_text: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks based on query using semantic search."""
        if selected_text:
            # If selected text is provided, search within that text only
            return await self._retrieve_from_selected_text(query, selected_text, top_k)
        else:
            # Perform semantic search in the vector database
            return await self._semantic_search(query, top_k)

    async def _semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search using vector embeddings."""
        # Generate embedding for the query
        query_embedding = await self.embedding_service.generate_embedding(query)

        # Search in Qdrant
        search_results = self.vector_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Format results
        results = []
        for result in search_results:
            formatted_result = {
                'chunk_id': result.payload.get('chunk_id', ''),
                'text': result.payload.get('text', ''),
                'metadata': result.payload.get('metadata', {}),
                'similarity_score': result.score,
                'source': result.payload.get('metadata', {}).get('hierarchy_path', ''),
                'token_count': result.payload.get('token_count', 0)
            }
            results.append(formatted_result)

        return results

    async def _retrieve_from_selected_text(self, query: str, selected_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant chunks from selected text only."""
        # For now, we'll create a simple keyword-based search within the selected text
        # In a more sophisticated implementation, we could chunk the selected text
        # and perform semantic search within it

        # Simple approach: return the selected text as a single chunk if it's relevant
        # In practice, you'd want to chunk the selected text and then search within those chunks
        return [{
            'chunk_id': 'selected_text_chunk',
            'text': selected_text,
            'metadata': {'source': 'user_selected_text'},
            'similarity_score': 1.0,  # Perfect match since user selected it
            'source': 'Selected Text',
            'token_count': len(selected_text.split())
        }]

    async def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform hybrid search combining semantic and keyword approaches."""
        # For now, we'll focus on semantic search
        # In a more advanced implementation, we could combine:
        # 1. Semantic search using embeddings
        # 2. Keyword search using full-text search
        # 3. Re-rank the combined results

        semantic_results = await self._semantic_search(query, top_k)

        # For hybrid approach, we could also do keyword-based search
        # and combine the results, but for now we'll return semantic results
        return semantic_results

    async def get_content_by_ids(self, chunk_ids: List[str]) -> List[Dict[str, Any]]:
        """Retrieve content by specific chunk IDs."""
        results = self.vector_client.retrieve(
            collection_name=self.collection_name,
            ids=chunk_ids,
            with_payload=True
        )

        formatted_results = []
        for result in results:
            formatted_result = {
                'chunk_id': result.payload.get('chunk_id', ''),
                'text': result.payload.get('text', ''),
                'metadata': result.payload.get('metadata', {}),
                'source': result.payload.get('metadata', {}).get('hierarchy_path', ''),
                'token_count': result.payload.get('token_count', 0)
            }
            formatted_results.append(formatted_result)

        return formatted_results


class SelectedTextService:
    """Service specifically for handling selected-text-only QA."""

    def __init__(self):
        self.embedding_service = EmbeddingService()

    async def process_selected_text_query(self, query: str, selected_text: str) -> List[Dict[str, Any]]:
        """Process a query against selected text only."""
        # This would involve:
        # 1. Potentially chunking the selected text if it's very long
        # 2. Performing semantic search within the selected text
        # 3. Returning relevant portions

        # For now, we'll return the selected text as context if it's relevant to the query
        # In practice, you'd want to chunk and search within the selected text
        return [{
            'chunk_id': 'selected_text_context',
            'text': selected_text,
            'metadata': {'source': 'user_selected_text'},
            'similarity_score': 0.8,  # Assuming some relevance
            'source': 'Selected Text',
            'token_count': len(selected_text.split())
        }]


# Example usage
async def retrieve_content(query: str, selected_text: Optional[str] = None) -> List[Dict[str, Any]]:
    """Convenience function to retrieve content."""
    service = RetrievalService()
    return await service.retrieve_relevant_chunks(query, top_k=5, selected_text=selected_text)


if __name__ == "__main__":
    # Example usage
    # import asyncio
    # results = asyncio.run(retrieve_content("What is Physical AI?"))
    # print(results)
    pass