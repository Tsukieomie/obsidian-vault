#!/usr/bin/env python3
"""
Obsidian Vault Loader - Load and parse Obsidian vault structure and content
"""

import os
import json
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict
import yaml


@dataclass
class VaultFile:
    """Represents a markdown file in the vault"""
    path: str
    relative_path: str
    title: str
    content: str
    frontmatter: Dict = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    internal_links: Set[str] = field(default_factory=set)
    external_links: Set[str] = field(default_factory=set)
    category: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary, converting sets to lists"""
        data = asdict(self)
        data['tags'] = sorted(list(self.tags))
        data['internal_links'] = sorted(list(self.internal_links))
        data['external_links'] = sorted(list(self.external_links))
        return data


@dataclass
class Entity:
    """Represents an entity (person, organization, etc.)"""
    name: str
    entity_type: str
    file_path: str
    description: str = ""
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    metadata: Dict = field(default_factory=dict)


class ObsidianVaultLoader:
    """Loads and parses an Obsidian vault"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.files: Dict[str, VaultFile] = {}
        self.entities: Dict[str, Entity] = {}
        self.link_graph: Dict[str, Set[str]] = defaultdict(set)
        self.tag_index: Dict[str, Set[str]] = defaultdict(set)
        self.obsidian_config = {}

    def load(self) -> Dict:
        """Load the entire vault"""
        print(f"Loading Obsidian vault from {self.vault_path}")

        # Load Obsidian configuration
        self._load_obsidian_config()

        # Scan and load all markdown files
        self._load_markdown_files()

        # Extract entities from specific directories
        self._extract_entities()

        # Build link graph and indices
        self._build_indices()

        print(f"Loaded {len(self.files)} files, {len(self.entities)} entities")
        return self.to_dict()

    def _load_obsidian_config(self):
        """Load Obsidian configuration files"""
        obsidian_dir = self.vault_path / '.obsidian'
        if obsidian_dir.exists():
            config_file = obsidian_dir / 'app.json'
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        self.obsidian_config = json.load(f)
                    print(f"Loaded Obsidian configuration")
                except Exception as e:
                    print(f"Warning: Could not load Obsidian config: {e}")

    def _load_markdown_files(self):
        """Recursively load all markdown files from the vault"""
        for md_file in self.vault_path.rglob('*.md'):
            # Skip hidden directories and certain paths
            if '/.obsidian/' in str(md_file) or '/.git/' in str(md_file):
                continue

            try:
                self._load_file(md_file)
            except Exception as e:
                print(f"Warning: Could not load {md_file}: {e}")

    def _load_file(self, file_path: Path):
        """Load and parse a single markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter
        frontmatter, body = self._parse_frontmatter(content)

        # Extract metadata
        title = frontmatter.get('title', file_path.stem)
        relative_path = str(file_path.relative_to(self.vault_path))

        # Extract tags and links
        tags = self._extract_tags(body)
        internal_links = self._extract_internal_links(body)
        external_links = self._extract_external_links(body)

        # Determine category from directory
        category = self._determine_category(relative_path)

        vault_file = VaultFile(
            path=str(file_path),
            relative_path=relative_path,
            title=title,
            content=body,
            frontmatter=frontmatter,
            tags=tags,
            internal_links=internal_links,
            external_links=external_links,
            category=category
        )

        self.files[relative_path] = vault_file

    def _parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse YAML frontmatter from markdown content"""
        if not content.startswith('---'):
            return {}, content

        lines = content.split('\n', 1)
        if len(lines) < 2:
            return {}, content

        rest = lines[1]
        parts = rest.split('---', 1)

        if len(parts) < 2:
            return {}, content

        try:
            frontmatter = yaml.safe_load(parts[0])
            body = parts[1].lstrip('\n')
            return frontmatter or {}, body
        except yaml.YAMLError:
            return {}, content

    def _extract_tags(self, content: str) -> Set[str]:
        """Extract all tags from markdown content"""
        tags = set()
        # Match #tag pattern (not in code blocks)
        for match in re.finditer(r'(?:^|\s)#([a-zA-Z0-9_-]+)', content):
            tags.add(match.group(1))
        return tags

    def _extract_internal_links(self, content: str) -> Set[str]:
        """Extract internal wiki-style links [[...]]"""
        links = set()
        for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
            link = match.group(1)
            # Handle aliases like [[file|alias]]
            if '|' in link:
                link = link.split('|')[0]
            links.add(link)
        return links

    def _extract_external_links(self, content: str) -> Set[str]:
        """Extract external URLs"""
        links = set()
        for match in re.finditer(r'https?://[^\s\)\]\}]+', content):
            links.add(match.group(0))
        return links

    def _determine_category(self, relative_path: str) -> Optional[str]:
        """Determine the category based on directory structure"""
        parts = relative_path.split('/')
        if len(parts) > 1:
            return parts[0]
        return None

    def _extract_entities(self):
        """Extract entities from Entities directory and other designated areas"""
        entities_dir = self.vault_path / 'Entities'

        if entities_dir.exists():
            # Process People directory
            people_dir = entities_dir / 'People'
            if people_dir.exists():
                self._process_entity_directory(people_dir, 'Person')

            # Process Organizations directory
            org_dir = entities_dir / 'Organizations'
            if org_dir.exists():
                self._process_entity_directory(org_dir, 'Organization')

            # Process individual entity files
            for file in entities_dir.glob('*.md'):
                self._process_entity_file(file)

    def _process_entity_directory(self, dir_path: Path, entity_type: str):
        """Process all entities in a directory"""
        for file in dir_path.glob('*.md'):
            self._process_entity_file(file, entity_type)

    def _process_entity_file(self, file_path: Path, entity_type: Optional[str] = None):
        """Process a single entity file"""
        relative_path = str(file_path.relative_to(self.vault_path))

        if relative_path not in self.files:
            return

        vault_file = self.files[relative_path]

        # Determine entity type
        if entity_type is None:
            entity_type = vault_file.frontmatter.get('type', 'Entity')

        entity = Entity(
            name=vault_file.title,
            entity_type=entity_type,
            file_path=relative_path,
            description=vault_file.content[:500],  # First 500 chars
            tags=vault_file.tags.copy(),
            metadata=vault_file.frontmatter.copy()
        )

        self.entities[vault_file.title] = entity

    def _build_indices(self):
        """Build link graph and tag indices"""
        for relative_path, file in self.files.items():
            # Build link graph
            self.link_graph[relative_path] = file.internal_links.copy()

            # Build tag index
            for tag in file.tags:
                self.tag_index[tag].add(relative_path)

    def to_dict(self) -> Dict:
        """Export vault data as dictionary"""
        return {
            'vault_path': str(self.vault_path),
            'file_count': len(self.files),
            'entity_count': len(self.entities),
            'files': {k: v.to_dict() for k, v in self.files.items()},
            'entities': {
                k: {
                    'name': v.name,
                    'type': v.entity_type,
                    'file_path': v.file_path,
                    'description': v.description,
                    'tags': sorted(list(v.tags)),
                }
                for k, v in self.entities.items()
            },
            'tag_index': {k: sorted(list(v)) for k, v in self.tag_index.items()},
            'obsidian_config': self.obsidian_config,
        }

    def search_files(self, query: str) -> List[str]:
        """Search for files containing query text"""
        results = []
        query_lower = query.lower()

        for relative_path, file in self.files.items():
            if query_lower in file.title.lower() or query_lower in file.content.lower():
                results.append(relative_path)

        return results

    def get_entity_relationships(self, entity_name: str) -> Dict:
        """Get all relationships for an entity"""
        if entity_name not in self.entities:
            return {}

        entity = self.entities[entity_name]
        relationships = {}

        # Find files that link to this entity
        linked_from = set()
        for relative_path, links in self.link_graph.items():
            if entity_name in links or entity.file_path in links:
                linked_from.add(relative_path)

        return {
            'entity': entity_name,
            'type': entity.entity_type,
            'file': entity.file_path,
            'linked_from': sorted(list(linked_from)),
            'links_to': sorted(list(entity.relationships.get('links_to', []))),
        }


if __name__ == '__main__':
    import sys

    vault_path = sys.argv[1] if len(sys.argv) > 1 else '/home/user/obsidian-vault'

    loader = ObsidianVaultLoader(vault_path)
    vault_data = loader.load()

    # Print summary
    print(f"\nVault Summary:")
    print(f"  Files: {vault_data['file_count']}")
    print(f"  Entities: {vault_data['entity_count']}")
    print(f"  Tags: {len(vault_data['tag_index'])}")

    # Save to JSON for inspection
    with open('vault_data.json', 'w') as f:
        json.dump(vault_data, f, indent=2)
    print(f"\nVault data saved to vault_data.json")
