#!/usr/bin/env python3
"""
Unified Obsidian Vault API
Provides a clean interface for accessing vault functionality
"""

from typing import Dict, List, Optional, Tuple
from vault_loader import ObsidianVaultLoader, VaultFile, Entity
from entity_graph import EntityGraph
from vault_search import VaultIndex, SearchResult
import json


class ObsidianVault:
    """Main API for accessing Obsidian vault"""

    def __init__(self, vault_path: str = '/home/user/obsidian-vault'):
        self.vault_path = vault_path
        self.loader: Optional[ObsidianVaultLoader] = None
        self.graph: Optional[EntityGraph] = None
        self.index: Optional[VaultIndex] = None
        self._loaded = False

    def load(self) -> None:
        """Load and initialize the vault"""
        if self._loaded:
            return

        print(f"Loading Obsidian vault from {self.vault_path}...")

        # Load vault structure
        self.loader = ObsidianVaultLoader(self.vault_path)
        self.loader.load()

        # Build entity graph
        self.graph = EntityGraph(self.loader)
        self.graph.build()

        # Build search index
        self.index = VaultIndex(self.loader)
        self.index.build()

        self._loaded = True
        print("Vault loaded successfully!")

    def is_loaded(self) -> bool:
        """Check if vault is loaded"""
        return self._loaded

    # File and Content Access
    def get_file(self, file_path: str) -> Optional[VaultFile]:
        """Get a file by relative path"""
        self._ensure_loaded()
        return self.loader.files.get(file_path)

    def get_file_by_title(self, title: str) -> Optional[VaultFile]:
        """Get a file by title"""
        self._ensure_loaded()
        for file in self.loader.files.values():
            if file.title == title:
                return file
        return None

    def list_files(self, category: Optional[str] = None) -> List[str]:
        """List all files, optionally filtered by category"""
        self._ensure_loaded()
        if category:
            return self.index.search_by_category(category)
        return sorted(list(self.loader.files.keys()))

    def get_file_content(self, file_path: str) -> Optional[str]:
        """Get the content of a file"""
        file = self.get_file(file_path)
        return file.content if file else None

    # Entity Access
    def get_entity(self, entity_name: str) -> Optional[Entity]:
        """Get an entity by name"""
        self._ensure_loaded()
        return self.loader.entities.get(entity_name)

    def list_entities(self) -> List[str]:
        """List all entities"""
        self._ensure_loaded()
        return sorted(list(self.loader.entities.keys()))

    def get_entity_info(self, entity_name: str) -> Optional[Dict]:
        """Get detailed information about an entity"""
        self._ensure_loaded()
        entity = self.loader.entities.get(entity_name)
        if not entity:
            return None

        # Get network around entity
        network = self.graph.get_entity_network(entity_name, depth=1)

        return {
            'name': entity.name,
            'type': entity.entity_type,
            'file': entity.file_path,
            'description': entity.description,
            'tags': sorted(list(entity.tags)),
            'network': network,
            'mentions_count': len(self.index.entity_mentions.get(entity_name, set()))
        }

    # Search and Discovery
    def search(
        self,
        query: str,
        search_type: str = 'all',
        limit: int = 20
    ) -> List[SearchResult]:
        """Search the vault"""
        self._ensure_loaded()
        return self.index.search(query, search_type=search_type, limit=limit)

    def search_entities(self, query: str) -> List[str]:
        """Search for entities"""
        self._ensure_loaded()
        results = []
        query_lower = query.lower()
        for entity_name in self.loader.entities.keys():
            if query_lower in entity_name.lower():
                results.append(entity_name)
        return sorted(results)

    def find_related_files(self, file_path: str, limit: int = 10) -> List[Tuple[str, float]]:
        """Find files related to a given file"""
        self._ensure_loaded()
        return self.index.search_related(file_path, limit=limit)

    # Relationship Queries
    def get_entity_relationships(self, entity_name: str) -> Optional[Dict]:
        """Get relationships for an entity"""
        self._ensure_loaded()
        if entity_name not in self.loader.entities:
            return None
        return self.graph.get_entity_network(entity_name, depth=2)

    def find_path(self, source: str, target: str) -> Optional[List[str]]:
        """Find shortest path between two entities"""
        self._ensure_loaded()
        return self.graph.find_shortest_path(source, target)

    def find_common_connections(self, entity1: str, entity2: str) -> List[str]:
        """Find entities connected to both entities"""
        self._ensure_loaded()
        common = self.graph.find_common_connections(entity1, entity2)
        return sorted(list(common))

    # Statistics and Metadata
    def get_statistics(self) -> Dict:
        """Get vault statistics"""
        self._ensure_loaded()
        return {
            'total_files': len(self.loader.files),
            'total_entities': len(self.loader.entities),
            'total_tags': len(self.loader.tag_index),
            'total_relationships': len(self.graph.relationships),
            'categories': list(self.index.category_index.keys()),
            'index_stats': self.index.get_statistics()
        }

    def get_vault_summary(self) -> Dict:
        """Get a comprehensive vault summary"""
        self._ensure_loaded()
        return {
            'path': self.vault_path,
            'statistics': self.get_statistics(),
            'categories': {
                cat: len(files)
                for cat, files in self.index.category_index.items()
            },
            'top_entities': list(self.loader.entities.keys())[:10],
            'obsidian_config': self.loader.obsidian_config
        }

    # Categories and Tags
    def get_category_files(self, category: str) -> List[str]:
        """Get all files in a category"""
        self._ensure_loaded()
        return self.index.search_by_category(category)

    def get_files_by_tag(self, tag: str) -> List[str]:
        """Get all files with a specific tag"""
        self._ensure_loaded()
        return sorted(list(self.loader.tag_index.get(tag, set())))

    def list_tags(self) -> Dict[str, int]:
        """List all tags and their frequency"""
        self._ensure_loaded()
        return {
            tag: len(files)
            for tag, files in self.loader.tag_index.items()
        }

    # Export and Serialization
    def export_as_json(self, include_content: bool = False) -> Dict:
        """Export vault data as JSON"""
        self._ensure_loaded()
        return {
            'metadata': {
                'vault_path': self.vault_path,
                'file_count': len(self.loader.files),
                'entity_count': len(self.loader.entities),
            },
            'summary': self.get_vault_summary(),
            'files': self.loader.to_dict() if include_content else {
                'count': len(self.loader.files),
                'categories': list(self.index.category_index.keys())
            }
        }

    def _ensure_loaded(self):
        """Ensure vault is loaded"""
        if not self._loaded:
            self.load()


if __name__ == '__main__':
    import sys

    vault = ObsidianVault('/home/user/obsidian-vault')
    vault.load()

    # Print vault summary
    summary = vault.get_vault_summary()
    print("\nVault Summary:")
    print(json.dumps(summary, indent=2))

    # Example: Search
    print("\n\nExample: Search for 'DARPA'")
    results = vault.search('DARPA', limit=5)
    for result in results:
        print(f"  - {result.title} ({result.match_type}): {result.relevance:.2f}")

    # Example: Entity info
    print("\n\nExample: Get info about 'Junyuan Wang'")
    info = vault.get_entity_info('Junyuan Wang')
    if info:
        print(f"Name: {info['name']}")
        print(f"Type: {info['type']}")
        print(f"Mentions: {info['mentions_count']}")
        print(f"Connected entities: {info['network']['nodes']}")

    # Example: Find path
    print("\n\nExample: Find path between 'Junyuan Wang' and 'DARPA'")
    path = vault.find_path('Junyuan Wang', 'DARPA')
    if path:
        print(f"Path: {' -> '.join(path)}")
    else:
        print("No path found")

    # Example: Related files
    print("\n\nExample: Find files related to 'Entities/People/Junyuan Wang.md'")
    file_path = 'Entities/People/Junyuan Wang.md'
    related = vault.find_related_files(file_path, limit=5)
    for related_path, score in related:
        print(f"  - {related_path}: {score:.2f}")

    print("\n✓ Obsidian Vault API loaded successfully!")
