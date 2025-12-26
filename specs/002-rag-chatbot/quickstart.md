# Quickstart: RAG Chatbot for Docusaurus Textbook

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docusaurus project setup
- OpenAI API key
- Qdrant Cloud account (Free Tier)

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install fastapi uvicorn openai qdrant-client python-dotenv
```

### 2. Configuration

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=textbook_content
```

### 3. Content Ingestion

Run the content ingestion script to process textbook markdown files:

```bash
# Navigate to the backend directory
cd backend

# Run the ingestion script
python -m src.services.content_ingestion
```

This will:
- Parse all markdown files in the textbook
- Chunk content with semantic boundaries (500-700 tokens)
- Generate OpenAI embeddings
- Store in Qdrant vector database

### 4. Start the Backend Server

```bash
# Start the FastAPI server
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 5. Integrate Frontend Component

Add the RAG chatbot component to your Docusaurus pages:

```jsx
// In your Docusaurus layout or specific pages
import RagChatbot from '@site/src/components/RagChatbot';

// Add to your layout
<RagChatbot />
```

### 6. API Endpoints

The backend provides the following endpoints:

- `POST /api/chat` - Main chat endpoint
- `POST /api/retrieve` - Retrieve relevant content
- `GET /api/health` - Health check

Example request:
```json
{
  "query": "What is the main principle of Physical AI?",
  "mode": "full_book",  // or "selected_text"
  "selected_text": "Optional selected text for selected-text mode"
}
```

### 7. Development

To run in development mode with hot reloading:

```bash
# Backend
cd backend
uvicorn src.api.main:app --reload

# Frontend (if developing the React component separately)
cd frontend
npm start
```

## Testing

Run the backend tests:
```bash
cd backend
pytest
```

## Deployment

1. Set up environment variables in your deployment environment
2. Build the Docusaurus site with the embedded component
3. Deploy the FastAPI backend to your preferred hosting platform
4. Update the frontend to point to your deployed backend URL