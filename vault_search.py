#!/usr/bin/env python3
"""
Vault Search and Indexing System
Provides efficient search and retrieval of vault content
"""

from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict
import json
import re
from vault_loader import ObsidianVaultLoader, VaultFile


@dataclass
class SearchResult:
    """Represents a search result"""
    file_path: str
    title: str
    match_type: str  # 'title', 'tag', 'content', 'link'
    relevance: float  # 0.0 to 1.0
    matched_text: str = ""


class VaultIndex:
    """Full-text index and search engine for vault"""

    def __init__(self, loader: ObsidianVaultLoader):
        self.loader = loader
        self.word_index: Dict[str, Set[str]] = defaultdict(set)  # word -> files
        self.phrase_index: Dict[str, Set[str]] = defaultdict(set)  # phrase -> files
        self.entity_mentions: Dict[str, Set[str]] = defaultdict(set)  # entity -> files
        self.category_index: Dict[str, Set[str]] = defaultdict(set)  # category -> files

    def build(self):
        """Build all indices"""
        print("Building vault search index...")

        for file_path, vault_file in self.loader.files.items():
            # Index by category
            if vault_file.category:
                self.category_index[vault_file.category].add(file_path)

            # Index words and phrases
            self._index_content(file_path, vault_file)

            # Index entity mentions
            self._index_entity_mentions(file_path, vault_file)

        print(f"Index built: {len(self.word_index)} unique words")

    def _index_content(self, file_path: str, vault_file: VaultFile):
        """Index the content of a file"""
        # Index title
        for word in self._tokenize(vault_file.title):
            self.word_index[word].add(file_path)

        # Index body content
        for word in self._tokenize(vault_file.content):
            self.word_index[word].add(file_path)

    def _index_entity_mentions(self, file_path: str, vault_file: VaultFile):
        """Index entity mentions in a file"""
        for entity_name in self.loader.entities.keys():
            # Check if entity name is mentioned
            if self._is_mentioned(entity_name, vault_file.content):
                self.entity_mentions[entity_name].add(file_path)

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Convert to lowercase and split on word boundaries
        words = re.findall(r'\b[a-z0-9_-]+\b', text.lower())
        return [w for w in words if len(w) > 2]  # Filter short words

    def _is_mentioned(self, entity_name: str, text: str) -> bool:
        """Check if an entity is mentioned in text (case-insensitive)"""
        return entity_name.lower() in text.lower()

    def search(
        self,
        query: str,
        search_type: str = 'all',
        limit: int = 20
    ) -> List[SearchResult]:
        """
        Search the vault
        search_type: 'all', 'title', 'content', 'tags', 'entities'
        """
        results: Dict[str, SearchResult] = {}

        if search_type in ['all', 'title']:
            self._search_titles(query, results)

        if search_type in ['all', 'tags']:
            self._search_tags(query, results)

        if search_type in ['all', 'entities']:
            self._search_entities(query, results)

        if search_type in ['all', 'content']:
            self._search_content(query, results)

        # Sort by relevance
        sorted_results = sorted(
            results.values(),
            key=lambda r: r.relevance,
            reverse=True
        )

        return sorted_results[:limit]

    def _search_titles(self, query: str, results: Dict[str, SearchResult]):
        """Search in file titles"""
        query_lower = query.lower()
        for file_path, vault_file in self.loader.files.items():
            if query_lower in vault_file.title.lower():
                relevance = 0.9 if query_lower == vault_file.title.lower() else 0.7
                results[file_path] = SearchResult(
                    file_path=file_path,
                    title=vault_file.title,
                    match_type='title',
                    relevance=relevance,
                    matched_text=vault_file.title
                )

    def _search_tags(self, query: str, results: Dict[str, SearchResult]):
        """Search by tags"""
        query_lower = query.lower().lstrip('#')
        for file_path, vault_file in self.loader.files.items():
            for tag in vault_file.tags:
                if query_lower in tag.lower():
                    if file_path not in results or results[file_path].relevance < 0.6:
                        results[file_path] = SearchResult(
                            file_path=file_path,
                            title=vault_file.title,
                            match_type='tag',
                            relevance=0.6,
                            matched_text=tag
                        )

    def _search_entities(self, query: str, results: Dict[str, SearchResult]):
        """Search for entity mentions"""
        query_lower = query.lower()
        for entity_name in self.loader.entities.keys():
            if query_lower in entity_name.lower():
                for file_path in self.entity_mentions.get(entity_name, set()):
                    if file_path not in results or results[file_path].relevance < 0.5:
                        vault_file = self.loader.files[file_path]
                        results[file_path] = SearchResult(
                            file_path=file_path,
                            title=vault_file.title,
                            match_type='entity',
                            relevance=0.5,
                            matched_text=entity_name
                        )

    def _search_content(self, query: str, results: Dict[str, SearchResult]):
        """Full-text search in content"""
        query_lower = query.lower()
        for file_path, vault_file in self.loader.files.items():
            if query_lower in vault_file.content.lower():
                if file_path not in results or results[file_path].relevance < 0.3:
                    # Find context around match
                    idx = vault_file.content.lower().find(query_lower)
                    start = max(0, idx - 50)
                    end = min(len(vault_file.content), idx + 50)
                    context = vault_file.content[start:end]

                    results[file_path] = SearchResult(
                        file_path=file_path,
                        title=vault_file.title,
                        match_type='content',
                        relevance=0.3,
                        matched_text=f"...{context}..."
                    )

    def search_by_category(self, category: str) -> List[str]:
        """Get all files in a category"""
        return sorted(list(self.category_index.get(category, set())))

    def search_related(self, file_path: str, limit: int = 10) -> List[Tuple[str, float]]:
        """Find files related to a given file"""
        if file_path not in self.loader.files:
            return []

        vault_file = self.loader.files[file_path]
        related: Dict[str, float] = {}

        # Score based on shared tags
        for tag in vault_file.tags:
            for related_file in self.loader.tag_index.get(tag, set()):
                if related_file != file_path:
                    related[related_file] = related.get(related_file, 0) + 0.5

        # Score based on shared links
        for linked_file in vault_file.internal_links:
            # Try to find file with this name
            for file_path_candidate, candidate_file in self.loader.files.items():
                if linked_file in candidate_file.title:
                    related[file_path_candidate] = related.get(file_path_candidate, 0) + 0.3

        # Sort by relevance
        sorted_related = sorted(
            related.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_related[:limit]

    def get_statistics(self) -> Dict:
        """Get index statistics"""
        return {
            'total_files': len(self.loader.files),
            'total_entities': len(self.loader.entities),
            'unique_words_indexed': len(self.word_index),
            'unique_phrases_indexed': len(self.phrase_index),
            'categories': dict(
                (cat, len(files))
                for cat, files in self.category_index.items()
            ),
            'entity_mentions': {
                entity: len(files)
                for entity, files in self.entity_mentions.items()
            }
        }

    def to_dict(self) -> Dict:
        """Export index as dictionary"""
        return {
            'statistics': self.get_statistics(),
            'categories': {k: sorted(list(v)) for k, v in self.category_index.items()}
        }


if __name__ == '__main__':
    import sys

    vault_path = sys.argv[1] if len(sys.argv) > 1 else '/home/user/obsidian-vault'

    # Load vault and build index
    loader = ObsidianVaultLoader(vault_path)
    loader.load()

    index = VaultIndex(loader)
    index.build()

    # Run sample searches
    print("\nSample searches:")
    for query in ['DARPA', 'investigation', '#network']:
        results = index.search(query, limit=5)
        print(f"\nSearch for '{query}':")
        for result in results:
            print(f"  - {result.title} ({result.match_type}): {result.relevance:.2f}")

    # Print statistics
    stats = index.get_statistics()
    print(f"\nIndex statistics:")
    print(f"  Total files: {stats['total_files']}")
    print(f"  Total entities: {stats['total_entities']}")
    print(f"  Unique words: {stats['unique_words_indexed']}")

    # Save index data
    with open('vault_index.json', 'w') as f:
        json.dump(index.to_dict(), f, indent=2)
    print(f"\nVault index saved to vault_index.json")
