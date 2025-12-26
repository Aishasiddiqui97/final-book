"""Content ingestion service for the RAG chatbot."""
import os
from typing import List, Dict, Any
from pathlib import Path
import logging
from .content_parser import parse_docusaurus_directory
from .chunking_service import ChunkingService, create_chunks_from_directory
from .embedding_service import BatchEmbeddingService
from ..config.vector_db import get_vector_db_client, get_collection_name
from qdrant_client.http import models


class ContentIngestionService:
    """Service for ingesting content from Docusaurus into vector database."""

    def __init__(self):
        self.chunker = ChunkingService()
        self.embedder = BatchEmbeddingService()
        self.vector_client = get_vector_db_client()
        self.collection_name = get_collection_name()
        self.logger = logging.getLogger(__name__)

    async def ingest_directory(self, directory_path: str, reindex: bool = False) -> Dict[str, Any]:
        """Ingest all content from a directory into the vector database."""
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory does not exist: {directory_path}")

        # Parse content from directory
        self.logger.info(f"Parsing content from {directory_path}")
        content_blocks = parse_docusaurus_directory(directory_path)

        # Create chunks
        self.logger.info(f"Creating chunks from {len(content_blocks)} content blocks")
        chunks = self.chunker.chunk_content(content_blocks)

        # Generate embeddings
        self.logger.info(f"Generating embeddings for {len(chunks)} chunks")
        chunk_embeddings = await self.embedder.process_chunks_with_embeddings(chunks)

        # Index in vector database
        self.logger.info(f"Indexing {len(chunk_embeddings)} embeddings in vector database")
        indexed_count = await self._index_embeddings(chunk_embeddings, reindex)

        return {
            "success": True,
            "processed_files": len(content_blocks),
            "created_chunks": len(chunks),
            "indexed_embeddings": indexed_count,
            "timestamp": "2025-12-26"
        }

    async def _index_embeddings(self, chunk_embeddings: List[Dict[str, Any]], reindex: bool = False) -> int:
        """Index embeddings in the vector database."""
        if reindex:
            # Clear existing collection
            self.vector_client.delete_collection(self.collection_name)
            from ..config.vector_db import get_vector_db_config
            get_vector_db_config().create_collection()

        # Prepare points for Qdrant
        points = []
        for i, chunk_data in enumerate(chunk_embeddings):
            point = models.PointStruct(
                id=i,
                vector=chunk_data['embedding'],
                payload={
                    "chunk_id": chunk_data['chunk_id'],
                    "text": chunk_data['text'],
                    "metadata": chunk_data['metadata'],
                    "token_count": chunk_data['token_count']
                }
            )
            points.append(point)

        # Upload to Qdrant
        self.vector_client.upload_points(
            collection_name=self.collection_name,
            points=points
        )

        return len(points)

    async def update_content(self, file_path: str) -> Dict[str, Any]:
        """Update a single file in the vector database."""
        # This would involve:
        # 1. Parsing the specific file
        # 2. Chunking it
        # 3. Generating embeddings
        # 4. Upserting to Qdrant
        # For now, this is a placeholder
        pass

    async def delete_content(self, content_ids: List[str]) -> Dict[str, Any]:
        """Delete specific content from the vector database."""
        # Delete by filtering on payload
        # This is a simplified version - in practice you'd want more sophisticated deletion
        pass


class ReindexService:
    """Service for reindexing content when the textbook is updated."""

    def __init__(self):
        self.ingestion_service = ContentIngestionService()

    async def reindex_all(self, source_directory: str) -> Dict[str, Any]:
        """Reindex all content from scratch."""
        return await self.ingestion_service.ingest_directory(source_directory, reindex=True)

    async def incremental_update(self, source_directory: str, changed_files: List[str]) -> Dict[str, Any]:
        """Perform incremental update based on changed files."""
        # For now, we'll do a full reindex
        # In a production system, you'd want to implement proper incremental updates
        return await self.ingestion_service.ingest_directory(source_directory, reindex=True)


# Example usage function
async def ingest_textbook_content(textbook_path: str) -> Dict[str, Any]:
    """Convenience function to ingest textbook content."""
    service = ContentIngestionService()
    return await service.ingest_directory(textbook_path)


if __name__ == "__main__":
    # Example usage
    # import asyncio
    # result = asyncio.run(ingest_textbook_content("path/to/textbook/docs"))
    # print(result)
    pass