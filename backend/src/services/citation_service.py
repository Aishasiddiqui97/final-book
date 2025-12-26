"""Service for handling citations and academic integrity."""
from typing import List, Dict, Any
from ..models.session_models import Citation


class CitationService:
    """Service for creating, formatting, and validating citations."""

    def __init__(self):
        pass

    def create_citations(self, context_chunks: List[Dict[str, Any]]) -> List[Citation]:
        """Create Citation objects from context chunks."""
        citations = []
        for i, chunk in enumerate(context_chunks):
            metadata = chunk.get('metadata', {})
            source = metadata.get('hierarchy_path', chunk.get('source', 'Unknown source'))

            # Extract chapter and section from hierarchy path
            parts = source.split(' > ')
            chapter = parts[0] if parts else 'Unknown Chapter'
            section = parts[1] if len(parts) > 1 else 'Unknown Section'
            subsection = parts[2] if len(parts) > 2 else None

            citation = Citation(
                citation_id=f"cit_{chunk.get('chunk_id', f'chunk_{i}')}",
                chapter=chapter,
                section=section,
                subsection=subsection,
                url=metadata.get('url', ''),
                text_preview=chunk.get('text', '')[:100] + "..." if len(chunk.get('text', '')) > 100 else chunk.get('text', ''),
                relevance_score=chunk.get('similarity_score', 0.0),
                metadata=metadata
            )

            citations.append(citation)

        return citations

    def format_citations(self, citations: List[Citation]) -> List[Dict[str, str]]:
        """Format citations in the required format [Chapter > Section]."""
        formatted = []
        for citation in citations:
            formatted_citation = {
                "chapter": citation.chapter,
                "section": citation.section,
                "subsection": citation.subsection,
                "url": citation.url,
                "text_preview": citation.text_preview,
                "relevance_score": citation.relevance_score
            }

            formatted.append(formatted_citation)

        return formatted

    def deduplicate_citations(self, citations: List[Citation]) -> List[Citation]:
        """Remove duplicate citations based on source information."""
        seen_sources = set()
        unique_citations = []

        for citation in citations:
            source_key = f"{citation.chapter}|{citation.section}|{citation.subsection}"
            if source_key not in seen_sources:
                seen_sources.add(source_key)
                unique_citations.append(citation)

        return unique_citations

    def validate_citation_integrity(self, citations: List[Citation], context_chunks: List[Dict[str, Any]]) -> bool:
        """Validate that citations correspond to actual context chunks."""
        if len(citations) > len(context_chunks):
            return False

        # Check that each citation has a corresponding chunk
        for citation in citations:
            found = False
            for chunk in context_chunks:
                if citation.citation_id == f"cit_{chunk.get('chunk_id', 'unknown')}":
                    found = True
                    break
            if not found:
                return False

        return True

    def format_citation_display(self, citations: List[Citation]) -> str:
        """Format citations for display in the response."""
        if not citations:
            return ""

        formatted_parts = []
        for citation in citations:
            if citation.subsection:
                formatted_parts.append(f"[{citation.chapter} > {citation.section} > {citation.subsection}]")
            else:
                formatted_parts.append(f"[{citation.chapter} > {citation.section}]")

        return " ".join(formatted_parts)

    def get_unique_sources(self, citations: List[Citation]) -> List[str]:
        """Get a list of unique source identifiers."""
        sources = set()
        for citation in citations:
            if citation.subsection:
                sources.add(f"{citation.chapter} > {citation.section} > {citation.subsection}")
            else:
                sources.add(f"{citation.chapter} > {citation.section}")

        return list(sources)


class AcademicIntegrityService:
    """Service for ensuring academic integrity in responses."""

    def __init__(self):
        self.citation_service = CitationService()

    def validate_response_academic_integrity(self, response: str, citations: List[Citation],
                                           context_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate that the response maintains academic integrity."""
        validation_result = {
            "has_proper_citations": len(citations) > 0,
            "citations_match_context": self.citation_service.validate_citation_integrity(citations, context_chunks),
            "no_external_knowledge": self._check_for_external_knowledge(response, context_chunks),
            "citation_format_correct": self._validate_citation_format(response),
            "overall_integrity_score": 0.0
        }

        # Calculate overall integrity score
        score = 0
        if validation_result["has_proper_citations"]:
            score += 25
        if validation_result["citations_match_context"]:
            score += 25
        if validation_result["no_external_knowledge"]:
            score += 25
        if validation_result["citation_format_correct"]:
            score += 25

        validation_result["overall_integrity_score"] = score

        return validation_result

    def _check_for_external_knowledge(self, response: str, context_chunks: List[Dict[str, Any]]) -> bool:
        """Check if response contains information not in context chunks."""
        # This is a simplified check - in a more sophisticated implementation,
        # we'd use semantic similarity or other techniques
        response_lower = response.lower()

        # Combine all context text
        context_text = " ".join([chunk.get('text', '').lower() for chunk in context_chunks])

        # Check if response content is supported by context
        # This is a basic keyword overlap check
        response_words = set(response_lower.split()[:50])  # First 50 words
        context_words = set(context_text.split()[:200])   # First 200 words

        overlap = len(response_words.intersection(context_words))
        overlap_ratio = overlap / len(response_words) if response_words else 1.0

        # If less than 50% of response words appear in context, flag as potential external knowledge
        return overlap_ratio >= 0.5

    def _validate_citation_format(self, response: str) -> bool:
        """Validate that citations in response follow the required format."""
        import re

        # Look for citations in the format [Chapter > Section] or [Chapter > Section > Subsection]
        citation_pattern = r'\[([^\]]*?) > ([^\]]*?)(?: > ([^\]]*?))?\]'
        citations_found = re.findall(citation_pattern, response)

        # If citations are found in the response, format is likely correct
        # This is a basic check - in practice, you'd want more sophisticated validation
        return len(citations_found) > 0


# Example usage
def create_formatted_citations(context_chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Convenience function to create formatted citations."""
    service = CitationService()
    citations = service.create_citations(context_chunks)
    return service.format_citations(citations)