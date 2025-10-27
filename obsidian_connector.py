#!/usr/bin/env python3
"""
Obsidian-Claude Connector

A comprehensive connector that allows programmatic access to an Obsidian vault.
Provides methods for reading, writing, searching, and analyzing markdown notes.

Author: Claude
License: MIT
"""

import os
import re
import json
import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import fnmatch


@dataclass
class Note:
    """Represents an Obsidian note with metadata"""
    path: str
    title: str
    content: str
    tags: List[str]
    links: List[str]
    created: Optional[str] = None
    modified: Optional[str] = None
    word_count: int = 0

    def to_dict(self) -> dict:
        """Convert note to dictionary"""
        return asdict(self)


class ObsidianConnector:
    """
    Main connector class for interacting with an Obsidian vault.
    """

    def __init__(self, vault_path: str = None):
        """
        Initialize the Obsidian connector.

        Args:
            vault_path: Path to the Obsidian vault. If None, uses current directory.
        """
        self.vault_path = Path(vault_path) if vault_path else Path.cwd()

        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {self.vault_path}")

        # Exclude patterns for common non-note files
        self.exclude_patterns = [
            '.git/*', '.obsidian/*', '.sync-*', '*.canvas', '*.base',
            '__pycache__/*', '*.pyc', 'node_modules/*'
        ]

    def _should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded based on patterns"""
        relative_path = path.relative_to(self.vault_path)
        relative_str = str(relative_path)

        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(relative_str, pattern):
                return True
        return False

    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from markdown content (both #tag and YAML frontmatter)"""
        tags = set()

        # Extract hashtags
        hashtag_pattern = r'#([a-zA-Z0-9_/-]+)'
        hashtags = re.findall(hashtag_pattern, content)
        tags.update(hashtags)

        # Extract YAML frontmatter tags
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            # Look for tags: [tag1, tag2] or tags: tag1, tag2
            tag_match = re.search(r'tags:\s*\[([^\]]+)\]', yaml_content)
            if tag_match:
                yaml_tags = [t.strip().strip('"\'') for t in tag_match.group(1).split(',')]
                tags.update(yaml_tags)
            else:
                tag_match = re.search(r'tags:\s*(.+)', yaml_content)
                if tag_match:
                    yaml_tags = [t.strip().strip('"\'') for t in tag_match.group(1).split(',')]
                    tags.update(yaml_tags)

        return sorted(list(tags))

    def _extract_links(self, content: str) -> List[str]:
        """Extract internal links from markdown content"""
        # Obsidian internal links: [[Link]] or [[Link|Alias]]
        link_pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        links = re.findall(link_pattern, content)
        return sorted(list(set(links)))

    def _get_file_stats(self, path: Path) -> Tuple[Optional[str], Optional[str]]:
        """Get file creation and modification times"""
        stats = path.stat()
        created = datetime.datetime.fromtimestamp(stats.st_ctime).isoformat()
        modified = datetime.datetime.fromtimestamp(stats.st_mtime).isoformat()
        return created, modified

    def _parse_note(self, path: Path) -> Note:
        """Parse a markdown file into a Note object"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get title from filename (without .md extension)
        title = path.stem

        # Extract metadata
        tags = self._extract_tags(content)
        links = self._extract_links(content)
        created, modified = self._get_file_stats(path)
        word_count = len(content.split())

        # Get relative path from vault root
        relative_path = str(path.relative_to(self.vault_path))

        return Note(
            path=relative_path,
            title=title,
            content=content,
            tags=tags,
            links=links,
            created=created,
            modified=modified,
            word_count=word_count
        )

    def list_notes(self, pattern: str = "**/*.md") -> List[str]:
        """
        List all markdown notes in the vault.

        Args:
            pattern: Glob pattern to filter notes (default: all .md files)

        Returns:
            List of relative paths to notes
        """
        notes = []
        for path in self.vault_path.glob(pattern):
            if path.is_file() and not self._should_exclude(path):
                relative_path = str(path.relative_to(self.vault_path))
                notes.append(relative_path)
        return sorted(notes)

    def read_note(self, note_path: str) -> Note:
        """
        Read a specific note from the vault.

        Args:
            note_path: Relative path to the note from vault root

        Returns:
            Note object with content and metadata
        """
        full_path = self.vault_path / note_path

        if not full_path.exists():
            raise FileNotFoundError(f"Note not found: {note_path}")

        if not full_path.suffix == '.md':
            raise ValueError(f"Not a markdown file: {note_path}")

        return self._parse_note(full_path)

    def write_note(self, note_path: str, content: str, create_dirs: bool = True) -> str:
        """
        Write or update a note in the vault.

        Args:
            note_path: Relative path where to save the note
            content: Content of the note
            create_dirs: Whether to create parent directories if they don't exist

        Returns:
            Absolute path to the created/updated note
        """
        full_path = self.vault_path / note_path

        # Ensure .md extension
        if not full_path.suffix == '.md':
            full_path = full_path.with_suffix('.md')

        # Create parent directories if needed
        if create_dirs:
            full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the note
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(full_path)

    def search_notes(self, query: str, case_sensitive: bool = False) -> List[Dict]:
        """
        Search for notes containing the query string.

        Args:
            query: Search query
            case_sensitive: Whether to perform case-sensitive search

        Returns:
            List of dictionaries with note path and matching lines
        """
        results = []

        if not case_sensitive:
            query = query.lower()

        for note_path in self.list_notes():
            try:
                note = self.read_note(note_path)
                content = note.content if case_sensitive else note.content.lower()

                if query in content:
                    # Find matching lines
                    lines = note.content.split('\n')
                    matches = []

                    for i, line in enumerate(lines, 1):
                        check_line = line if case_sensitive else line.lower()
                        if query in check_line:
                            matches.append({
                                'line_number': i,
                                'line': line.strip()
                            })

                    results.append({
                        'path': note_path,
                        'title': note.title,
                        'matches': matches,
                        'match_count': len(matches)
                    })
            except Exception as e:
                print(f"Error searching {note_path}: {e}")
                continue

        return results

    def search_by_tag(self, tag: str) -> List[Note]:
        """
        Find all notes with a specific tag.

        Args:
            tag: Tag to search for (without # prefix)

        Returns:
            List of Note objects
        """
        # Remove # if provided
        tag = tag.lstrip('#')
        notes_with_tag = []

        for note_path in self.list_notes():
            try:
                note = self.read_note(note_path)
                if tag in note.tags:
                    notes_with_tag.append(note)
            except Exception as e:
                print(f"Error reading {note_path}: {e}")
                continue

        return notes_with_tag

    def get_backlinks(self, note_title: str) -> List[Note]:
        """
        Find all notes that link to a specific note.

        Args:
            note_title: Title of the note to find backlinks for

        Returns:
            List of Note objects that link to the specified note
        """
        backlinks = []

        for note_path in self.list_notes():
            try:
                note = self.read_note(note_path)
                if note_title in note.links:
                    backlinks.append(note)
            except Exception as e:
                print(f"Error reading {note_path}: {e}")
                continue

        return backlinks

    def get_all_tags(self) -> Dict[str, int]:
        """
        Get all tags used in the vault with their frequency.

        Returns:
            Dictionary mapping tag names to count of notes using them
        """
        tag_counts = {}

        for note_path in self.list_notes():
            try:
                note = self.read_note(note_path)
                for tag in note.tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
            except Exception as e:
                print(f"Error reading {note_path}: {e}")
                continue

        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True))

    def get_vault_stats(self) -> Dict:
        """
        Get statistics about the vault.

        Returns:
            Dictionary with vault statistics
        """
        notes = self.list_notes()
        total_notes = len(notes)
        total_words = 0
        total_tags = set()
        total_links = set()

        for note_path in notes:
            try:
                note = self.read_note(note_path)
                total_words += note.word_count
                total_tags.update(note.tags)
                total_links.update(note.links)
            except Exception:
                continue

        return {
            'total_notes': total_notes,
            'total_words': total_words,
            'unique_tags': len(total_tags),
            'unique_links': len(total_links),
            'vault_path': str(self.vault_path)
        }

    def create_note_from_template(self, note_path: str, template_path: str,
                                  variables: Dict[str, str] = None) -> str:
        """
        Create a new note from a template.

        Args:
            note_path: Path where to create the new note
            template_path: Path to the template note
            variables: Dictionary of variables to replace in template ({{variable}})

        Returns:
            Path to the created note
        """
        template_note = self.read_note(template_path)
        content = template_note.content

        # Replace variables
        if variables:
            for key, value in variables.items():
                content = content.replace(f'{{{{{key}}}}}', value)

        # Add creation date
        content = content.replace('{{date}}', datetime.datetime.now().strftime('%Y-%m-%d'))
        content = content.replace('{{datetime}}', datetime.datetime.now().isoformat())

        return self.write_note(note_path, content)


def main():
    """Example usage of the connector"""
    # Initialize connector
    connector = ObsidianConnector()

    # Get vault statistics
    print("Vault Statistics:")
    print(json.dumps(connector.get_vault_stats(), indent=2))

    # List all notes
    print("\nAll Notes:")
    for note in connector.list_notes()[:10]:  # Show first 10
        print(f"  - {note}")

    # Get all tags
    print("\nTop Tags:")
    tags = connector.get_all_tags()
    for tag, count in list(tags.items())[:10]:
        print(f"  #{tag}: {count} notes")


if __name__ == '__main__':
    main()
