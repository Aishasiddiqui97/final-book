"""Test script to verify Qdrant configuration works properly."""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing Qdrant configuration...")

# Check if environment variables are loaded
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

print(f"Qdrant URL loaded: {'Yes' if qdrant_url else 'No'}")
print(f"Qdrant API Key loaded: {'Yes' if qdrant_api_key else 'No'}")
print(f"Collection name: {collection_name}")

# Test importing and initializing Qdrant configuration
try:
    from src.config.vector_db import vector_db_config
    print("[OK] VectorDB config imported successfully")

    # Try to get the client
    client = vector_db_config.get_client()
    print(f"[OK] Qdrant client created: {type(client).__name__}")

    # Try to get collection info (this will test the connection)
    try:
        collection_info = client.get_collection(collection_name)
        print(f"[OK] Connected to collection '{collection_name}' successfully")
        print(f"[OK] Collection vectors count: {collection_info.points_count}")
    except Exception as e:
        print(f"[INFO] Collection '{collection_name}' doesn't exist yet (will be created): {e}")

except Exception as e:
    print(f"[ERROR] Error with Qdrant configuration: {e}")

print("\nQdrant configuration test completed!")