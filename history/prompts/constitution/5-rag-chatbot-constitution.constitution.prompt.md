---
id: 5
title: RAG Chatbot Constitution
stage: constitution
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Aisha.A.Siddiqui
command: /sp.constitution
labels: ["constitution", "rag", "chatbot", "textbook", "physical-ai", "humanoid-robotics"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

You are building an integrated Retrieval-Augmented Generation (RAG) chatbot for an already-published Docusaurus textbook titled "Physical AI & Humanoid Robotics".

Core principles:
- The chatbot must answer ONLY from the book chapters, labs, and code blocks
- Zero hallucination: if information is not in the book, say "Not found in this book"
- Every answer must include citations (Chapter → Section → URL)
- Support two modes:
  1) Full-book question answering
  2) Selected-text–only answering (user-highlighted content)
- Fast enough for in-page usage
- Designed for engineering students and researchers
- Privacy-first: no training on user data

## Response snapshot

Updated the project constitution to include RAG chatbot principles for the Physical AI & Humanoid Robotics textbook, adding five new principles: Zero Hallucination Rule, Citation Requirement, Dual Mode Functionality, Performance Standards, and Privacy-First Approach.

## Outcome

- ✅ Impact: Constitution updated with RAG chatbot principles while preserving existing educational principles
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Use updated constitution for RAG chatbot development
- 🧠 Reflection: Balance between existing educational mission and new chatbot functionality achieved

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not applicable
- Prompt variant (if applicable): not applicable
- Next experiment (smallest change to try): none needed