"""Test script to verify OpenRouter configuration works properly."""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing OpenRouter configuration...")

# Check if environment variables are loaded
api_key = os.getenv("OPENAI_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

print(f"API Key loaded: {'Yes' if api_key else 'No'}")
print(f"Qdrant URL loaded: {'Yes' if qdrant_url else 'No'}")
print(f"Qdrant API Key loaded: {'Yes' if qdrant_api_key else 'No'}")

# Check if using OpenRouter
if api_key and api_key.startswith("sk-or-"):
    print("Using OpenRouter API key format")
else:
    print("Using standard OpenAI API key format")

# Test importing and initializing services
try:
    from src.services.embedding_service import EmbeddingService
    print("[OK] EmbeddingService imported successfully")

    embedding_service = EmbeddingService()
    print("[OK] EmbeddingService initialized successfully")

    # Check the client configuration
    if hasattr(embedding_service, 'client'):
        print(f"[OK] Embedding client configured: {type(embedding_service.client).__name__}")

        # Check if base_url is set for OpenRouter
        if hasattr(embedding_service.client, '_client') and hasattr(embedding_service.client._client, 'base_url'):
            base_url = str(embedding_service.client._client.base_url)
            if 'openrouter' in base_url.lower():
                print("[OK] OpenRouter base URL configured for embeddings")
            else:
                print(f"[OK] Base URL configured: {base_url}")

except Exception as e:
    print(f"[ERROR] Error with EmbeddingService: {e}")

try:
    from src.services.prompt_service import PromptService
    print("[OK] PromptService imported successfully")

    prompt_service = PromptService()
    print("[OK] PromptService initialized successfully")

    # Check the client configuration
    if hasattr(prompt_service, 'client'):
        print(f"[OK] Prompt client configured: {type(prompt_service.client).__name__}")

        # Check if base_url is set for OpenRouter
        if hasattr(prompt_service.client, '_client') and hasattr(prompt_service.client._client, 'base_url'):
            base_url = str(prompt_service.client._client.base_url)
            if 'openrouter' in base_url.lower():
                print("[OK] OpenRouter base URL configured for prompts")
            else:
                print(f"[OK] Base URL configured: {base_url}")

        print(f"[OK] Model configured: {prompt_service.model}")

except Exception as e:
    print(f"[ERROR] Error with PromptService: {e}")

print("\nConfiguration test completed!")
print("\nTo run the backend server:")
print("1. Activate virtual environment: source venv/bin/activate (Windows: venv\\Scripts\\activate)")
print("2. Start backend: python start_server.py")
print("3. Start Docusaurus: cd book && npm start")
print("4. Reindex content: python -m scripts.reindex --source ../book/docs")