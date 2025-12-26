"""RAG prompt service with zero hallucination enforcement."""
import asyncio
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from ..config import OPENAI_API_KEY
from .citation_service import CitationService


class PromptService:
    """Service for generating RAG prompts with zero hallucination enforcement."""

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Check if using OpenRouter by looking at the key format
        if OPENAI_API_KEY.startswith("sk-or-"):
            # Using OpenRouter - need to select an appropriate model
            self.client = AsyncOpenAI(
                api_key=OPENAI_API_KEY,
                base_url="https://openrouter.ai/api/v1"
            )
            # Using a model available on OpenRouter that's good for instruction following
            self.model = "openai/gpt-4-turbo"  # OpenRouter format for GPT-4 Turbo
        else:
            # Using OpenAI
            self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            self.model = "gpt-4-turbo"  # Using GPT-4 Turbo for better instruction following

        self.citation_service = CitationService()

    async def generate_response(self, query: str, context_chunks: List[Dict[str, Any]],
                              mode: str = "full_book", selected_text: Optional[str] = None) -> Dict[str, Any]:
        """Generate a response based on the query and context, enforcing zero hallucination."""

        # Format the context for the prompt
        formatted_context = self._format_context(context_chunks, mode)

        # Create the system message enforcing zero hallucination
        system_message = self._create_system_message(mode)

        # Create the user message with query and context
        user_message = self._create_user_message(query, formatted_context, selected_text, mode)

        # Call the OpenAI API
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,  # Low temperature for more consistent, fact-based responses
                max_tokens=1000,
                timeout=30
            )

            # Extract the response
            content = response.choices[0].message.content

            # Extract citations from context using the citation service
            citations = self.citation_service.create_citations(context_chunks)
            formatted_citations = self.citation_service.format_citations(citations)
            unique_sources = self.citation_service.get_unique_sources(citations)

            return {
                "response": content,
                "citations": formatted_citations,
                "sources": unique_sources
            }

        except Exception as e:
            # Handle the case where no relevant context was found
            if "No relevant context found" in str(e) or len(context_chunks) == 0:
                if mode == "selected_text":
                    return {
                        "response": "Not found in selected text",
                        "citations": [],
                        "sources": []
                    }
                else:
                    return {
                        "response": "Not found in this book",
                        "citations": [],
                        "sources": []
                    }
            else:
                raise e

    def _create_system_message(self, mode: str) -> str:
        """Create the system message that enforces zero hallucination."""
        if mode == "selected_text":
            return """
            You are an AI assistant for a textbook. You must answer ONLY based on the provided selected text context.
            Do not use any external knowledge or make up information.
            If the answer cannot be found in the provided selected text, respond with "Not found in selected text".
            Always provide citations in the format [Chapter > Section] when possible.
            """
        else:
            return """
            You are an AI assistant for a textbook. You must answer ONLY based on the provided textbook content context.
            Do not use any external knowledge or make up information.
            If the answer cannot be found in the provided context, respond with "Not found in this book".
            Always provide citations in the format [Chapter > Section] when possible.
            """

    def _create_user_message(self, query: str, formatted_context: str,
                           selected_text: Optional[str], mode: str) -> str:
        """Create the user message with query and context."""
        if mode == "selected_text" and selected_text:
            return f"""
            Using only the following selected text, answer the question:

            SELECTED TEXT:
            {selected_text}

            QUESTION:
            {query}

            Remember: Answer only based on the provided text. If the answer is not in the text, say "Not found in selected text".
            """
        else:
            return f"""
            Using only the following textbook context, answer the question:

            CONTEXT:
            {formatted_context}

            QUESTION:
            {query}

            Remember: Answer only based on the provided context. If the answer is not in the context, say "Not found in this book".
            """

    def _format_context(self, context_chunks: List[Dict[str, Any]], mode: str) -> str:
        """Format the context chunks for the prompt."""
        if not context_chunks:
            return "No relevant context found."

        formatted_parts = []
        for i, chunk in enumerate(context_chunks):
            text = chunk.get('text', '')[:500]  # Limit text length to avoid token issues
            source = chunk.get('source', 'Unknown source')
            formatted_parts.append(f"[Source {i+1}: {source}]\n{text}\n")

        return "\n".join(formatted_parts)

    def _extract_citations(self, context_chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Extract citations from context chunks."""
        citations = []
        for chunk in context_chunks:
            metadata = chunk.get('metadata', {})
            source = metadata.get('hierarchy_path', chunk.get('source', 'Unknown'))

            # Extract chapter and section from hierarchy path
            parts = source.split(' > ')
            chapter = parts[0] if parts else 'Unknown Chapter'
            section = parts[1] if len(parts) > 1 else 'Unknown Section'
            subsection = parts[2] if len(parts) > 2 else None

            citation = {
                "chapter": chapter,
                "section": section,
                "subsection": subsection,
                "source": source,
                "text_preview": chunk.get('text', '')[:100] + "..."
            }

            citations.append(citation)

        return citations


# Example usage
async def generate_rag_response(query: str, context_chunks: List[Dict[str, Any]],
                              mode: str = "full_book", selected_text: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to generate RAG response."""
    service = PromptService()
    return await service.generate_response(query, context_chunks, mode, selected_text)


if __name__ == "__main__":
    # Example usage
    # import asyncio
    # context = [{"text": "Physical AI is the integration of artificial intelligence with physical systems...", "source": "Module 1 > Introduction"}]
    # result = asyncio.run(generate_rag_response("What is Physical AI?", context))
    # print(result)
    pass