"""Markdown parser for Docusaurus chapters."""
import re
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import markdown
from markdown import Extension
from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree


class DocusaurusContentParser:
    """Parser for Docusaurus markdown content with special handling for callouts, code blocks, etc."""

    def __init__(self):
        self.content_blocks = []
        self.current_chapter = ""
        self.current_section = ""
        self.current_subsection = ""

    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a single Docusaurus markdown file into structured content blocks."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter if present
        frontmatter, content = self._extract_frontmatter(content)

        # Extract chapter/section info from filename or frontmatter
        self._extract_hierarchy_info(file_path, frontmatter)

        # Parse content into blocks
        blocks = self._parse_content_to_blocks(content, file_path)

        return blocks

    def _extract_frontmatter(self, content: str) -> tuple:
        """Extract YAML frontmatter from content."""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[1].strip(), parts[2].strip()
        return "", content

    def _extract_hierarchy_info(self, file_path: str, frontmatter: str):
        """Extract chapter and section info from file path or frontmatter."""
        path_parts = Path(file_path).parts
        # Extract chapter and section from path structure
        # e.g., docs/module-1-ros/introduction-to-physical-ai.md
        for part in path_parts:
            if 'module' in part.lower():
                self.current_chapter = part.replace('-', ' ').title()
            elif 'chapter' in part.lower():
                self.current_section = part.replace('-', ' ').title()

        # If no chapter found, use directory name
        if not self.current_chapter:
            self.current_chapter = Path(file_path).parent.name.replace('-', ' ').title()

        # Use filename as section
        self.current_section = Path(file_path).stem.replace('-', ' ').title()

    def _parse_content_to_blocks(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Parse content into structured blocks."""
        blocks = []

        # Split content into sections based on headers
        lines = content.split('\n')
        current_block = {
            'type': 'prose',
            'content': '',
            'headers': [],
            'code_blocks': [],
            'callouts': []
        }

        i = 0
        while i < len(lines):
            line = lines[i]

            # Check for headers
            if line.startswith('#'):
                # Save previous block if it has content
                if current_block['content'].strip():
                    blocks.append(self._create_content_block(current_block, file_path))

                # Extract header information
                header_level = len(line) - len(line.lstrip('#'))
                header_text = line.lstrip('#').strip()

                current_block = {
                    'type': 'prose',
                    'content': f"{header_text}\n",
                    'headers': [(header_level, header_text)],
                    'code_blocks': [],
                    'callouts': [],
                    'section': header_text
                }

            # Check for code blocks
            elif line.startswith('```'):
                code_block, i = self._extract_code_block(lines, i)
                current_block['code_blocks'].append(code_block)

            # Check for callouts/admonitions
            elif line.startswith(':::'):
                callout, i = self._extract_callout(lines, i)
                current_block['callouts'].append(callout)

            else:
                current_block['content'] += line + '\n'

            i += 1

        # Add the last block
        if current_block['content'].strip():
            blocks.append(self._create_content_block(current_block, file_path))

        return blocks

    def _extract_code_block(self, lines: List[str], start_idx: int) -> tuple:
        """Extract a code block from lines starting at start_idx."""
        lang = lines[start_idx].strip('`').strip() or 'text'
        code_lines = []
        i = start_idx + 1

        while i < len(lines) and not lines[i].startswith('```'):
            code_lines.append(lines[i])
            i += 1

        code_block = {
            'language': lang,
            'content': '\n'.join(code_lines),
            'type': 'code'
        }

        return code_block, i  # Return the new index

    def _extract_callout(self, lines: List[str], start_idx: int) -> tuple:
        """Extract a Docusaurus callout/admonition."""
        callout_type = lines[start_idx].strip(':')
        callout_lines = []
        i = start_idx + 1

        while i < len(lines) and not lines[i].startswith(':::'):
            callout_lines.append(lines[i])
            i += 1

        callout = {
            'type': callout_type,
            'content': '\n'.join(callout_lines),
            'content_type': 'callout'
        }

        return callout, i  # Return the new index

    def _create_content_block(self, block_data: Dict[str, Any], file_path: str) -> Dict[str, Any]:
        """Create a standardized content block."""
        return {
            'chapter': self.current_chapter,
            'section': block_data.get('section', self.current_section),
            'content': block_data['content'].strip(),
            'type': block_data['type'],
            'code_blocks': block_data['code_blocks'],
            'callouts': block_data['callouts'],
            'source_file': file_path,
            'hierarchy_path': f"{self.current_chapter} > {block_data.get('section', self.current_section)}",
            'headers': block_data.get('headers', [])
        }


def parse_docusaurus_directory(directory_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
    """Parse all markdown files in a Docusaurus directory."""
    parser = DocusaurusContentParser()
    all_blocks = []

    pattern = "**/*.md" if recursive else "*.md"

    for md_file in Path(directory_path).glob(pattern):
        try:
            blocks = parser.parse_file(str(md_file))
            all_blocks.extend(blocks)
        except Exception as e:
            print(f"Error parsing {md_file}: {str(e)}")
            continue

    return all_blocks


if __name__ == "__main__":
    # Example usage
    # blocks = parse_docusaurus_directory("path/to/docusaurus/docs")
    pass