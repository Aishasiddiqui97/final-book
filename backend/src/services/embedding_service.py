"""Embedding service for generating vector representations."""
import asyncio
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from .chunking_service import Chunk
from ..config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL


class EmbeddingService:
    """Service for generating embeddings using OpenAI API or OpenRouter."""

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Check if using OpenRouter by looking at the key format
        if OPENAI_API_KEY.startswith("sk-or-"):
            # Using OpenRouter
            self.client = AsyncOpenAI(
                api_key=OPENAI_API_KEY,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            # Using OpenAI
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

        self.model = OPENAI_EMBEDDING_MODEL

    async def generate_embeddings(self, chunks: List[Chunk]) -> List[List[float]]:
        """Generate embeddings for a list of chunks."""
        if not chunks:
            return []

        # Prepare texts for embedding
        texts = [chunk.text for chunk in chunks]

        # Call OpenAI API to generate embeddings
        try:
            response = await self.client.embeddings.create(
                input=texts,
                model=self.model
            )

            # Extract embeddings from response
            embeddings = []
            for i, embedding_obj in enumerate(response.data):
                chunk_embedding = embedding_obj.embedding
                chunks[i].metadata['embedding_id'] = embedding_obj.index
                embeddings.append(chunk_embedding)

            return embeddings

        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            raise

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate a single embedding for a text."""
        try:
            response = await self.client.embeddings.create(
                input=[text],
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating single embedding: {str(e)}")
            raise

    def get_embedding_dimensions(self) -> int:
        """Get the expected dimensions for embeddings."""
        # Different models have different dimensions
        # text-embedding-ada-002 has 1536 dimensions
        if self.model == "text-embedding-ada-002":
            return 1536
        elif self.model == "text-embedding-3-small":
            return 1536  # Default to 1536, but can be 512 with dimensions=512
        elif self.model == "text-embedding-3-large":
            return 3072
        else:
            return 1536  # Default assumption


class BatchEmbeddingService:
    """Service for batch processing embeddings efficiently."""

    def __init__(self, max_batch_size: int = 20):
        self.embedding_service = EmbeddingService()
        self.max_batch_size = max_batch_size

    async def generate_embeddings_batch(self, chunks: List[Chunk]) -> List[List[float]]:
        """Generate embeddings in batches to respect API limits."""
        all_embeddings = []

        # Process in batches
        for i in range(0, len(chunks), self.max_batch_size):
            batch_chunks = chunks[i:i + self.max_batch_size]
            batch_embeddings = await self.embedding_service.generate_embeddings(batch_chunks)
            all_embeddings.extend(batch_embeddings)

            # Add a small delay to respect rate limits
            await asyncio.sleep(0.1)

        return all_embeddings

    async def process_chunks_with_embeddings(self, chunks: List[Chunk]) -> List[Dict[str, Any]]:
        """Process chunks and return them with embeddings."""
        embeddings = await self.generate_embeddings_batch(chunks)

        result = []
        for chunk, embedding in zip(chunks, embeddings):
            chunk_dict = {
                'chunk_id': chunk.id,
                'text': chunk.text,
                'embedding': embedding,
                'metadata': chunk.metadata,
                'token_count': chunk.token_count
            }
            result.append(chunk_dict)

        return result


# Example usage function
async def create_embeddings_for_directory(directory_path: str) -> List[Dict[str, Any]]:
    """Create embeddings for all content in a directory."""
    from .chunking_service import create_chunks_from_directory

    chunks = create_chunks_from_directory(directory_path)
    batch_service = BatchEmbeddingService()

    return await batch_service.process_chunks_with_embeddings(chunks)


if __name__ == "__main__":
    # Example usage
    # chunks = create_chunks_from_directory("path/to/docusaurus/docs")
    # embeddings = await create_embeddings_for_directory("path/to/docusaurus/docs")
    pass