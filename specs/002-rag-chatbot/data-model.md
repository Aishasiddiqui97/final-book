# Data Model: RAG Chatbot for Docusaurus Textbook

## Entities

### TextbookContent
- **Description**: Represents the source content from Docusaurus textbook
- **Fields**:
  - content_id: Unique identifier for the content chunk
  - chapter: Chapter title/identifier
  - section: Section title/identifier
  - subsection: Subsection title/identifier (optional)
  - content_text: The actual text content
  - content_type: Type of content (prose, code, callout, heading)
  - source_file: Original markdown file path
  - hierarchy_path: Full hierarchy path (Chapter > Section > Subsection)
  - embedding_vector: Vector representation of the content
  - token_count: Number of tokens in the chunk

### EmbeddingChunk
- **Description**: Represents a semantically coherent chunk of textbook content
- **Fields**:
  - chunk_id: Unique identifier for the chunk
  - content_id: Reference to the original content
  - text: The chunked text (500-700 tokens)
  - embedding: Vector embedding of the text
  - metadata: Additional metadata including source references
  - semantic_boundary: Flag indicating if this chunk respects semantic boundaries

### ChatSession
- **Description**: Represents a conversation session between user and chatbot
- **Fields**:
  - session_id: Unique identifier for the session
  - created_at: Timestamp of session creation
  - updated_at: Timestamp of last activity
  - mode: Answering mode (full-book or selected-text)
  - selected_text: Text selected by user (for selected-text mode)
  - user_id: Anonymous identifier for the session (no personal data)

### ChatMessage
- **Description**: Represents a single message in the conversation
- **Fields**:
  - message_id: Unique identifier for the message
  - session_id: Reference to the chat session
  - role: Message role (user or assistant)
  - content: The message content
  - timestamp: When the message was created
  - citations: List of source citations for assistant responses
  - query_type: Type of query (general or selected-text)

### RetrievalResult
- **Description**: Represents the results of a vector search operation
- **Fields**:
  - result_id: Unique identifier for the result
  - query: The original query text
  - retrieved_chunks: List of relevant content chunks
  - similarity_scores: Scores for each retrieved chunk
  - metadata: Additional information about the retrieval process
  - search_type: Type of search (semantic, keyword, or hybrid)

### Citation
- **Description**: Represents a reference to a specific part of the textbook
- **Fields**:
  - citation_id: Unique identifier for the citation
  - chapter: Chapter reference
  - section: Section reference
  - subsection: Subsection reference (optional)
  - url: URL to the specific section in the textbook
  - text_preview: Short preview of the cited text
  - relevance_score: How relevant this citation is to the query