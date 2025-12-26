"""Startup script for the RAG Chatbot backend server."""
import uvicorn
import argparse
import os
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description='Start the RAG Chatbot API server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload (development)')
    parser.add_argument('--workers', type=int, default=1, help='Number of worker processes')

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Verify required environment variables
    required_vars = ['OPENAI_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment")
        return 1

    print(f"Starting RAG Chatbot API server on {args.host}:{args.port}")
    print(f"Auto-reload: {'enabled' if args.reload else 'disabled'}")
    print(f"Workers: {args.workers}")

    # Start the server
    uvicorn.run(
        "src.api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers if not args.reload else 1,  # Can't use multiple workers with reload
        log_level="info"
    )

    return 0


if __name__ == "__main__":
    exit(main())