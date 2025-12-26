# Research: RAG Chatbot for Docusaurus Textbook

## Decision: Chunking Strategy for Semantic Boundaries
**Rationale**: Using semantic boundaries instead of fixed token counts preserves context and maintains document hierarchy as required by the specification
**Alternatives considered**: Fixed 500-700 token chunks without regard for document structure; sentence-level chunking

## Decision: Embedding Model Selection
**Rationale**: OpenAI embedding model (likely text-embedding-ada-002) provides good balance of quality and cost for the textbook content
**Alternatives considered**: Other OpenAI models, open-source alternatives like Sentence Transformers

## Decision: Qdrant Cloud Free Tier Usage
**Rationale**: Free tier provides sufficient capacity for textbook content while meeting the specification requirements
**Alternatives considered**: Other vector databases (Pinecone, Weaviate), self-hosted Qdrant

## Decision: FastAPI Framework Choice
**Rationale**: FastAPI provides excellent performance, automatic API documentation, and good integration with Python ML/AI libraries
**Alternatives considered**: Flask, Django, Node.js frameworks

## Decision: React Component Architecture
**Rationale**: React component embedded in Docusaurus pages provides best integration with existing textbook infrastructure
**Alternatives considered**: Standalone web application, iframe embedding, vanilla JavaScript component

## Decision: Code Block Handling
**Rationale**: Code-aware chunking preserves complete code blocks within chunks to maintain functionality when retrieved
**Alternatives considered**: Treating code as regular text, separate code indexing

## Decision: Selected-Text Implementation
**Rationale**: Client-side text selection with server-side restriction provides real-time user experience without excessive pre-processing
**Alternatives considered**: Pre-computing embeddings for all possible selections, dynamic server-side selection processing