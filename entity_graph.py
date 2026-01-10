#!/usr/bin/env python3
"""
Entity Relationship Graph Builder for Obsidian Vault
Builds and analyzes relationships between entities
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import json
from vault_loader import ObsidianVaultLoader, VaultFile, Entity


@dataclass
class Relationship:
    """Represents a relationship between entities"""
    source: str
    target: str
    relation_type: str
    strength: float = 1.0  # 0.0 to 1.0
    evidence: List[str] = field(default_factory=list)  # Files that mention relationship


class EntityGraph:
    """Builds and manages entity relationships"""

    def __init__(self, vault_loader: ObsidianVaultLoader):
        self.loader = vault_loader
        self.relationships: List[Relationship] = []
        self.entity_aliases: Dict[str, Set[str]] = defaultdict(set)
        self.adjacency: Dict[str, Dict[str, Relationship]] = defaultdict(dict)

    def build(self):
        """Build the entity graph from vault content"""
        print("Building entity relationship graph...")

        # Extract entity aliases from frontmatter
        self._extract_aliases()

        # Find relationships based on mentions and links
        self._find_relationships()

        print(f"Found {len(self.relationships)} relationships")

    def _extract_aliases(self):
        """Extract entity aliases from frontmatter"""
        for entity_name, entity in self.loader.entities.items():
            self.entity_aliases[entity_name].add(entity_name)

            # Add aliases from frontmatter
            if 'aliases' in entity.metadata:
                aliases = entity.metadata['aliases']
                if isinstance(aliases, list):
                    for alias in aliases:
                        self.entity_aliases[entity_name].add(alias)
                elif isinstance(aliases, str):
                    self.entity_aliases[entity_name].add(aliases)

    def _find_relationships(self):
        """Find relationships by analyzing vault content"""
        # For each file, find entity mentions and create relationships
        for file_path, vault_file in self.loader.files.items():
            # Check internal links for entity references
            for linked_file in vault_file.internal_links:
                self._process_link(file_path, linked_file, vault_file)

    def _process_link(self, source_file: str, target_ref: str, vault_file: VaultFile):
        """Process a link between two files"""
        # Try to match to entities
        source_entity = self._find_entity_by_file(source_file)
        target_entity = self._find_entity_by_name(target_ref)

        if source_entity and target_entity:
            rel = Relationship(
                source=source_entity.name,
                target=target_entity.name,
                relation_type='mentioned_in',
                evidence=[source_file]
            )
            self._add_relationship(rel)

    def _find_entity_by_file(self, file_path: str) -> Optional[Entity]:
        """Find an entity that corresponds to a file"""
        for entity in self.loader.entities.values():
            if entity.file_path == file_path:
                return entity
        return None

    def _find_entity_by_name(self, name: str) -> Optional[Entity]:
        """Find entity by name or alias"""
        # Direct match
        if name in self.loader.entities:
            return self.loader.entities[name]

        # Try to match by alias
        for entity_name, aliases in self.entity_aliases.items():
            if name in aliases:
                if entity_name in self.loader.entities:
                    return self.loader.entities[entity_name]

        return None

    def _add_relationship(self, rel: Relationship):
        """Add a relationship to the graph"""
        # Check if relationship already exists
        key = (rel.source, rel.target)
        if key in self.adjacency[rel.source]:
            existing = self.adjacency[rel.source][key[1]]
            existing.strength = min(1.0, existing.strength + 0.1)
            existing.evidence.extend(rel.evidence)
        else:
            self.relationships.append(rel)
            self.adjacency[rel.source][rel.target] = rel

    def get_entity_network(self, entity_name: str, depth: int = 2) -> Dict:
        """Get the network around an entity"""
        visited = set()
        network = {
            'entity': entity_name,
            'nodes': set(),
            'edges': []
        }

        def traverse(name: str, current_depth: int):
            if current_depth > depth or name in visited:
                return
            visited.add(name)
            network['nodes'].add(name)

            if name in self.adjacency:
                for target, rel in self.adjacency[name].items():
                    network['edges'].append({
                        'source': rel.source,
                        'target': rel.target,
                        'type': rel.relation_type,
                        'strength': rel.strength
                    })
                    traverse(target, current_depth + 1)

        traverse(entity_name, 0)

        return {
            'entity': entity_name,
            'nodes': sorted(list(network['nodes'])),
            'edges': network['edges']
        }

    def find_shortest_path(self, source: str, target: str) -> Optional[List[str]]:
        """Find shortest path between two entities using BFS"""
        from collections import deque

        if source == target:
            return [source]

        queue = deque([(source, [source])])
        visited = {source}

        while queue:
            current, path = queue.popleft()

            if current in self.adjacency:
                for neighbor in self.adjacency[current]:
                    if neighbor == target:
                        return path + [neighbor]

                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

        return None

    def find_common_connections(self, entity1: str, entity2: str) -> Set[str]:
        """Find entities connected to both entities"""
        connections1 = set(self.adjacency.get(entity1, {}).keys())
        connections2 = set(self.adjacency.get(entity2, {}).keys())
        return connections1 & connections2

    def to_dict(self) -> Dict:
        """Export graph as dictionary"""
        return {
            'relationships': [
                {
                    'source': rel.source,
                    'target': rel.target,
                    'type': rel.relation_type,
                    'strength': rel.strength,
                    'evidence_count': len(rel.evidence)
                }
                for rel in self.relationships
            ],
            'entities': list(self.loader.entities.keys()),
            'statistics': {
                'total_relationships': len(self.relationships),
                'unique_entities': len(self.loader.entities),
            }
        }


if __name__ == '__main__':
    import sys

    vault_path = sys.argv[1] if len(sys.argv) > 1 else '/home/user/obsidian-vault'

    # Load vault and build graph
    loader = ObsidianVaultLoader(vault_path)
    loader.load()

    graph = EntityGraph(loader)
    graph.build()

    # Print sample entity network
    if loader.entities:
        sample_entity = list(loader.entities.keys())[0]
        print(f"\nNetwork around {sample_entity}:")
        network = graph.get_entity_network(sample_entity, depth=2)
        print(json.dumps(network, indent=2, default=str))

    # Save graph data
    with open('entity_graph.json', 'w') as f:
        json.dump(graph.to_dict(), f, indent=2)
    print(f"\nEntity graph saved to entity_graph.json")
