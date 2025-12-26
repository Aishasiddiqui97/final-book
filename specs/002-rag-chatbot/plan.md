# Implementation Plan: RAG Chatbot for Docusaurus Textbook

**Branch**: `002-rag-chatbot` | **Date**: 2025-12-26 | **Spec**: [link to specs/002-rag-chatbot/spec.md]
**Input**: Feature specification from `/specs/002-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Retrieval-Augmented Generation (RAG) chatbot for the Physical AI & Humanoid Robotics textbook. The system will ingest Docusaurus markdown content, create embeddings using OpenAI models, store in Qdrant vector database, and provide a React-based chat interface with zero hallucination policy and proper citation requirements.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript for frontend
**Primary Dependencies**: FastAPI, OpenAI SDK, Qdrant, React, Docusaurus
**Storage**: Qdrant Cloud (vector database), embedded in Docusaurus site
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web server for backend, browser for frontend
**Project Type**: Web application
**Performance Goals**: <3 second response time, 95% accuracy in content retrieval
**Constraints**: <500ms p95 for UI interactions, privacy-first (no user data retention), academic integrity (zero hallucination)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The implementation must comply with the RAG Chatbot Principles in the constitution:
- Zero Hallucination Rule: System must answer ONLY from book chapters, labs, and code blocks
- Citation Requirement: Every answer must include citations (Chapter → Section → URL)
- Dual Mode Functionality: Support full-book and selected-text answering
- Performance Standards: Fast enough for in-page usage
- Privacy-First Approach: No training on user data

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── config/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

book/
└── src/
    └── components/
        └── RagChatbot/
```

**Structure Decision**: Web application structure with separate backend (FastAPI) and frontend (React component embedded in Docusaurus)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Implementation Phases

### Phase 1: Book Content Ingestion
**Goal**: Extract and parse Docusaurus markdown content from textbook chapters
**Output Artifact**: Content ingestion service that processes Markdown files, preserves structure (headings, code blocks, callouts)
**Acceptance Criteria**: System can parse all existing textbook chapters, maintain document hierarchy, extract text, code blocks, and other elements

### Phase 2: Chunking & Embeddings
**Goal**: Split content into semantic chunks (500-700 tokens) and generate OpenAI embeddings
**Output Artifact**: Chunking service with semantic boundary detection and embedding generation
**Acceptance Criteria**: Content chunks maintain context, stay within token limits, preserve document hierarchy, generate valid embeddings

### Phase 3: Qdrant Indexing
**Goal**: Store embeddings in Qdrant Cloud vector database with metadata
**Output Artifact**: Vector database with indexed textbook content and metadata for retrieval
**Acceptance Criteria**: All textbook content indexed in Qdrant, metadata includes chapter/section references for citations

### Phase 4: RAG Agent Prompt Design
**Goal**: Create prompt templates that enforce zero hallucination and citation requirements
**Output Artifact**: Prompt engineering for OpenAI agent with proper context injection and response formatting
**Acceptance Criteria**: Agent responds only from retrieved context, includes proper citations, refuses to answer from external knowledge

### Phase 5: Selected-Text QA Pipeline
**Goal**: Implement pipeline for answering questions from user-selected text only
**Output Artifact**: Text selection service and restricted retrieval mechanism
**Acceptance Criteria**: System can answer questions based only on selected text, provides appropriate responses when content is insufficient

### Phase 6: FastAPI Backend
**Goal**: Create API endpoints for chat functionality, retrieval, and citation generation
**Output Artifact**: FastAPI application with endpoints for question answering, retrieval, and chat session management
**Acceptance Criteria**: API provides chat interface, handles both full-book and selected-text modes, returns properly cited responses

### Phase 7: Docusaurus UI Embedding
**Goal**: Create React component for chat interface embedded in Docusaurus pages
**Output Artifact**: Docusaurus-compatible React component with floating chat interface
**Acceptance Criteria**: Component integrates seamlessly with Docusaurus, provides good UX, supports both answering modes

### Phase 8: Testing & Validation
**Goal**: Validate accuracy, performance, and compliance with constitutional requirements
**Output Artifact**: Test suite covering functionality, accuracy, and constitutional compliance
**Acceptance Criteria**: Tests verify zero hallucination, proper citations, performance requirements, and privacy compliance

### Phase 9: Deployment
**Goal**: Deploy backend and integrate frontend into Docusaurus site
**Output Artifact**: Deployed RAG chatbot accessible within textbook
**Acceptance Criteria**: System is live and accessible, meets performance requirements, maintains all constitutional principles