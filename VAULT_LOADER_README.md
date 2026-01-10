# Obsidian Vault Loader

A comprehensive Python system for loading, parsing, and analyzing Obsidian vaults programmatically.

## Overview

This vault loader provides a complete API for:
- **Loading** Obsidian vault structure and content
- **Parsing** markdown files with frontmatter and metadata
- **Indexing** files, entities, and relationships
- **Searching** across vault content
- **Analyzing** entity relationships and networks

## Components

### 1. `vault_loader.py` - Core Loader
The main loader module that:
- Scans the vault directory structure
- Parses markdown files with YAML frontmatter
- Extracts tags, links, and metadata
- Organizes files by category
- Identifies and catalogs entities

**Usage:**
```python
from vault_loader import ObsidianVaultLoader

loader = ObsidianVaultLoader('/path/to/vault')
vault_data = loader.load()

# Access files and entities
for path, file in loader.files.items():
    print(f"{file.title}: {file.category}")

for name, entity in loader.entities.items():
    print(f"{name} ({entity.entity_type})")
```

### 2. `entity_graph.py` - Relationship Graph
Builds and analyzes relationships between entities:
- Extracts entity mentions from files
- Builds relationship graphs
- Finds shortest paths between entities
- Identifies common connections

**Usage:**
```python
from entity_graph import EntityGraph

graph = EntityGraph(loader)
graph.build()

# Get entity network
network = graph.get_entity_network('Junyuan Wang', depth=2)

# Find path between entities
path = graph.find_shortest_path('Entity A', 'Entity B')

# Find common connections
common = graph.find_common_connections('Entity A', 'Entity B')
```

### 3. `vault_search.py` - Search and Indexing
Full-text search and content indexing:
- Tokenizes and indexes all content
- Supports multiple search types (title, tags, entities, content)
- Relevance ranking
- Category browsing
- Related file discovery

**Usage:**
```python
from vault_search import VaultIndex

index = VaultIndex(loader)
index.build()

# Search vault
results = index.search('DARPA', limit=10)
for result in results:
    print(f"{result.title} ({result.match_type}): {result.relevance}")

# Get files by category
files = index.search_by_category('Analysis')

# Find related files
related = index.search_related('file_path.md')
```

### 4. `vault_api.py` - Unified API
High-level API combining all components:
- Simple, intuitive interface
- Lazy loading
- Comprehensive queries
- Data export

**Usage:**
```python
from vault_api import ObsidianVault

vault = ObsidianVault('/path/to/vault')
vault.load()

# Search
results = vault.search('investigation')

# Get entity info
info = vault.get_entity_info('Junyuan Wang')

# List files by category
files = vault.list_files(category='Analysis')

# Find relationships
relationships = vault.get_entity_relationships('Junyuan Wang')

# Get statistics
stats = vault.get_statistics()
```

## Features

### File Operations
- `get_file(path)` - Get file by relative path
- `get_file_by_title(title)` - Get file by title
- `list_files(category)` - List files, optionally by category
- `get_file_content(path)` - Get raw content

### Entity Operations
- `get_entity(name)` - Get entity by name
- `list_entities()` - List all entities
- `get_entity_info(name)` - Get comprehensive entity information
- `search_entities(query)` - Search for entities

### Search & Discovery
- `search(query, type, limit)` - Full-text search
- `find_related_files(path, limit)` - Find related files
- `get_files_by_tag(tag)` - Get files by tag
- `list_tags()` - Get all tags with frequency

### Relationship Analysis
- `get_entity_relationships(name)` - Get entity network
- `find_path(source, target)` - Find shortest path
- `find_common_connections(entity1, entity2)` - Find common connections

### Statistics
- `get_statistics()` - Comprehensive statistics
- `get_vault_summary()` - Full vault summary
- `export_as_json()` - Export as JSON

## Data Structures

### VaultFile
```python
@dataclass
class VaultFile:
    path: str
    relative_path: str
    title: str
    content: str
    frontmatter: Dict
    tags: Set[str]
    internal_links: Set[str]
    external_links: Set[str]
    category: Optional[str]
```

### Entity
```python
@dataclass
class Entity:
    name: str
    entity_type: str
    file_path: str
    description: str
    relationships: Dict[str, List[str]]
    tags: Set[str]
    metadata: Dict
```

### SearchResult
```python
@dataclass
class SearchResult:
    file_path: str
    title: str
    match_type: str  # 'title', 'tag', 'content', 'entity'
    relevance: float
    matched_text: str
```

## Vault Statistics (Current)

- **Total Files:** 46
- **Total Entities:** 21
- **Total Tags:** 72
- **Total Relationships:** 36
- **Unique Indexed Words:** 4,425
- **Categories:** Entities, Analysis, Patents, Technical

### Top Entities by Mentions
1. DARPA (21 mentions)
2. Google (21 mentions)
3. Asymptote Network LLC (21 mentions)
4. NSF (20 mentions)
5. Apple (19 mentions)

## Example Usage

```python
from vault_api import ObsidianVault

# Initialize and load vault
vault = ObsidianVault()
vault.load()

# Print summary
print(vault.get_vault_summary())

# Search for related documents
results = vault.search('technology transfer')
for result in results:
    print(f"- {result.title}")

# Analyze entity networks
entity_info = vault.get_entity_info('Junyuan Wang')
print(f"Connected to: {entity_info['network']['nodes']}")

# Find relationships
path = vault.find_path('Asymptote Network LLC', 'DARPA')
if path:
    print(f"Connection: {' → '.join(path)}")

# Get files by category
analysis_docs = vault.list_files(category='Analysis')
for doc in analysis_docs:
    print(f"- {doc}")
```

## Running Examples

```bash
# Load and analyze vault
python3 vault_api.py

# Generate vault data
python3 vault_loader.py

# Generate entity graph
python3 entity_graph.py

# Generate search index
python3 vault_search.py
```

## Output Files

When run individually, the loaders generate JSON files:
- `vault_data.json` - Complete vault structure and content
- `entity_graph.json` - Entity relationship graph
- `vault_index.json` - Search index and statistics

## Command-Line Interface

A comprehensive CLI tool (`vault_cli.py`) provides easy access to all vault functionality:

```bash
# View vault information
./vault_cli.py info

# Search vault
./vault_cli.py search "DARPA"
./vault_cli.py search "technology transfer" --type content --limit 10

# List entities
./vault_cli.py entities
./vault_cli.py entities "Wang"

# Get entity details
./vault_cli.py entity "Junyuan Wang"

# Analyze relationships
./vault_cli.py graph --name "Junyuan Wang"
./vault_cli.py graph --source "Junyuan Wang" --target "DARPA"
./vault_cli.py graph --common "Entity1,Entity2"

# Browse files
./vault_cli.py files
./vault_cli.py files --category Analysis

# Work with tags
./vault_cli.py tags
./vault_cli.py tags --tag investigation

# Find related files
./vault_cli.py related "Junyuan Wang.md"

# Export data
./vault_cli.py export --format json --output vault.json
./vault_cli.py export --format csv --output vault.csv

# Generate report
./vault_cli.py report
./vault_cli.py report --output analysis.txt
```

## Usage Examples

See `vault_examples.py` for 10 comprehensive examples of using the API programmatically:

```python
from vault_api import ObsidianVault

vault = ObsidianVault()
vault.load()

# Search
results = vault.search('investigation')

# Get entity info
info = vault.get_entity_info('Junyuan Wang')

# Find relationships
path = vault.find_path('Junyuan Wang', 'DARPA')
common = vault.find_common_connections('Entity A', 'Entity B')

# Browse by category
analysis_files = vault.list_files(category='Analysis')

# Get statistics
stats = vault.get_statistics()
```

## Requirements

- Python 3.7+
- PyYAML (for frontmatter parsing)

## Notes

- The vault loader is designed for efficient batch processing
- Internal wiki-style links (`[[...]]`) are extracted and indexed
- Entity relationships are discovered through content mentions
- Search uses TF-like scoring for relevance ranking
- Categories are determined by directory structure
