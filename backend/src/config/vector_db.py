"""Vector database configuration and setup for Qdrant."""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional
from . import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME


class VectorDBConfig:
    """Configuration and setup for Qdrant vector database."""

    def __init__(self):
        if not QDRANT_URL:
            raise ValueError("QDRANT_URL environment variable is required")

        if not QDRANT_API_KEY:
            raise ValueError("QDRANT_API_KEY environment variable is required")

        # Initialize Qdrant client
        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )

        self.collection_name = QDRANT_COLLECTION_NAME

    def create_collection(self):
        """Create the collection with appropriate vector configuration."""
        # Get embedding dimensions from our model
        # For text-embedding-ada-002, it's 1536 dimensions
        embedding_size = 1536

        # Check if collection already exists
        try:
            self.client.get_collection(self.collection_name)
            print(f"Collection {self.collection_name} already exists")
            return
        except:
            pass  # Collection doesn't exist, so we'll create it

        # Create the collection
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=embedding_size,
                distance=models.Distance.COSINE  # Cosine distance for semantic similarity
            )
        )

        print(f"Created collection {self.collection_name} with {embedding_size} dimensions")

    def setup_payload_schema(self):
        """Set up payload schema for the collection."""
        # In Qdrant, we don't need to explicitly define a schema
        # but we can set up field indices for better performance
        pass

    def get_client(self) -> QdrantClient:
        """Get the configured Qdrant client."""
        return self.client

    def get_collection_name(self) -> str:
        """Get the configured collection name."""
        return self.collection_name

    def reset_collection(self):
        """Reset the collection (useful for development)."""
        try:
            self.client.delete_collection(self.collection_name)
            print(f"Deleted collection {self.collection_name}")
        except:
            pass  # Collection may not exist yet

        self.create_collection()


# Lazy initialization to avoid issues at module load time
_vector_db_config = None


def get_vector_db_config() -> VectorDBConfig:
    """Get the configured VectorDBConfig instance (lazy initialization)."""
    global _vector_db_config
    if _vector_db_config is None:
        _vector_db_config = VectorDBConfig()
    return _vector_db_config


def get_vector_db_client() -> QdrantClient:
    """Get the configured Qdrant client."""
    return get_vector_db_config().get_client()


def get_collection_name() -> str:
    """Get the configured collection name."""
    return get_vector_db_config().get_collection_name()


# Backward compatibility - this will be initialized lazily when first accessed
class _LazyVectorDBConfig:
    """Lazy accessor for vector_db_config for backward compatibility."""
    def __getattr__(self, name):
        return getattr(get_vector_db_config(), name)

vector_db_config = _LazyVectorDBConfig()


if __name__ == "__main__":
    # Initialize and setup the vector database
    config = VectorDBConfig()
    config.create_collection()
    print("Vector database setup complete")