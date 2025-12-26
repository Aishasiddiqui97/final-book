#!/usr/bin/env python3
"""Auto re-index script for book updates."""
import asyncio
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to the path so we can import our modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.content_ingestion import ReindexService


async def main():
    parser = argparse.ArgumentParser(description='Re-index textbook content for RAG chatbot')
    parser.add_argument('--source', '-s', required=True, help='Source directory containing textbook markdown files')
    parser.add_argument('--incremental', '-i', action='store_true', help='Perform incremental update (not yet implemented)')
    parser.add_argument('--full', '-f', action='store_true', help='Perform full re-index')

    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"Error: Source directory does not exist: {args.source}")
        return 1

    service = ReindexService()

    if args.incremental:
        print("Performing incremental update (not yet implemented, doing full re-index instead)")
        # For now, incremental does a full re-index since the feature isn't fully implemented
        result = await service.reindex_all(args.source)
    else:
        print("Performing full re-index...")
        result = await service.reindex_all(args.source)

    print(f"Re-index completed: {result}")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)