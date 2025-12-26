"""Chunking service for semantic text splitting."""
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import tiktoken
from .content_parser import DocusaurusContentParser


@dataclass
class Chunk:
    """Represents a semantic chunk of text."""
    id: str
    text: str
    metadata: Dict[str, Any]
    token_count: int
    semantic_boundary: bool = True


class ChunkingService:
    """Service for splitting content into semantic chunks with proper metadata."""

    def __init__(self, min_tokens: int = 500, max_tokens: int = 700):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def chunk_content(self, content_blocks: List[Dict[str, Any]]) -> List[Chunk]:
        """Chunk content blocks into semantic units."""
        all_chunks = []

        for block in content_blocks:
            chunks = self._chunk_single_block(block)
            all_chunks.extend(chunks)

        return all_chunks

    def _chunk_single_block(self, block: Dict[str, Any]) -> List[Chunk]:
        """Chunk a single content block."""
        chunks = []

        # Get the main content
        content = block.get('content', '')
        if not content.strip():
            return chunks

        # Add any code blocks to the content
        code_blocks = block.get('code_blocks', [])
        callouts = block.get('callouts', [])

        # Create a combined text that preserves important elements
        combined_content = self._combine_content_with_elements(content, code_blocks, callouts)

        # Split into chunks
        text_chunks = self._split_by_semantic_boundaries(combined_content)

        # Create chunks with proper metadata
        for i, chunk_text in enumerate(text_chunks):
            chunk_id = f"{block.get('source_file', 'unknown')}_{i}"
            token_count = len(self.tokenizer.encode(chunk_text))

            chunk = Chunk(
                id=chunk_id,
                text=chunk_text,
                metadata={
                    'chapter': block.get('chapter', ''),
                    'section': block.get('section', ''),
                    'source_file': block.get('source_file', ''),
                    'hierarchy_path': block.get('hierarchy_path', ''),
                    'content_type': block.get('type', 'prose'),
                    'original_block_idx': i
                },
                token_count=token_count,
                semantic_boundary=True
            )

            chunks.append(chunk)

        return chunks

    def _combine_content_with_elements(self, content: str, code_blocks: List[Dict], callouts: List[Dict]) -> str:
        """Combine content with code blocks and callouts while preserving structure."""
        combined = content

        # Add code blocks back into the content
        for i, code_block in enumerate(code_blocks):
            code_text = f"\n```{code_block.get('language', 'text')}\n{code_block['content']}\n```\n"
            combined += code_text

        # Add callouts back into the content
        for i, callout in enumerate(callouts):
            callout_text = f"\n:::{callout.get('type', 'note')}\n{callout['content']}\n:::\n"
            combined += callout_text

        return combined

    def _split_by_semantic_boundaries(self, text: str) -> List[str]:
        """Split text by semantic boundaries while respecting token limits."""
        chunks = []

        # Split by paragraphs first (most semantic boundary)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        current_chunk = ""
        current_token_count = 0

        for paragraph in paragraphs:
            paragraph_token_count = len(self.tokenizer.encode(paragraph))

            # If adding this paragraph would exceed max tokens
            if current_token_count + paragraph_token_count > self.max_tokens:
                # If current chunk is already substantial, save it and start new
                if current_token_count >= self.min_tokens:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                    current_token_count = paragraph_token_count
                else:
                    # If current chunk is too small, try to add paragraph anyway
                    if paragraph_token_count <= self.max_tokens:
                        current_chunk += "\n\n" + paragraph
                        current_token_count += paragraph_token_count
                    else:
                        # If paragraph is too long by itself, split it
                        sub_chunks = self._split_long_paragraph(paragraph)
                        chunks.extend(sub_chunks)
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                    current_token_count += paragraph_token_count + 2  # For the \n\n
                else:
                    current_chunk = paragraph
                    current_token_count = paragraph_token_count

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _split_long_paragraph(self, paragraph: str) -> List[str]:
        """Split a paragraph that's too long by itself."""
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)

        current_chunk = ""
        current_token_count = 0

        for sentence in sentences:
            sentence_token_count = len(self.tokenizer.encode(sentence))

            if current_token_count + sentence_token_count > self.max_tokens:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
                current_token_count = sentence_token_count
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                    current_token_count += sentence_token_count + 1  # For the space
                else:
                    current_chunk = sentence
                    current_token_count = sentence_token_count

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def validate_chunks(self, chunks: List[Chunk]) -> List[str]:
        """Validate chunks meet requirements."""
        errors = []

        for chunk in chunks:
            if chunk.token_count < self.min_tokens:
                errors.append(f"Chunk {chunk.id} has {chunk.token_count} tokens, below minimum of {self.min_tokens}")
            if chunk.token_count > self.max_tokens:
                errors.append(f"Chunk {chunk.id} has {chunk.token_count} tokens, above maximum of {self.max_tokens}")

        return errors


def create_chunks_from_directory(directory_path: str) -> List[Chunk]:
    """Create chunks from all content in a directory."""
    parser = DocusaurusContentParser()
    content_blocks = parser.parse_docusaurus_directory(directory_path)

    chunker = ChunkingService()
    chunks = chunker.chunk_content(content_blocks)

    # Validate chunks
    errors = chunker.validate_chunks(chunks)
    if errors:
        print("Chunk validation errors:")
        for error in errors:
            print(f"  - {error}")

    return chunks


if __name__ == "__main__":
    # Example usage
    # chunks = create_chunks_from_directory("path/to/docusaurus/docs")
    pass