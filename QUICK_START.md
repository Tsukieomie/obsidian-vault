# Obsidian Vault Loader - Quick Start Guide

## Installation

```bash
pip3 install pyyaml
```

## Quick Commands

### Get Vault Information
```bash
python3 vault_cli.py info
```

### Search the Vault
```bash
python3 vault_cli.py search "DARPA"
python3 vault_cli.py search "investigation" --type content --limit 10
```

### Explore Entities
```bash
python3 vault_cli.py entities                    # List all
python3 vault_cli.py entities "Wang"             # Search
python3 vault_cli.py entity "Junyuan Wang"       # Details
```

### Analyze Relationships
```bash
python3 vault_cli.py graph --name "Junyuan Wang"
python3 vault_cli.py graph --source "A" --target "B"
python3 vault_cli.py graph --common "A,B"
```

### Browse Files
```bash
python3 vault_cli.py files                       # All files
python3 vault_cli.py files --category Analysis   # By category
python3 vault_cli.py related "file.md"           # Related files
```

### Work with Tags
```bash
python3 vault_cli.py tags                        # All tags
python3 vault_cli.py tags --tag investigation    # Files by tag
```

### Export Data
```bash
python3 vault_cli.py export --format json --output vault.json
python3 vault_cli.py export --format csv --output vault.csv
```

### Generate Reports
```bash
python3 vault_cli.py report
python3 vault_cli.py report --output analysis.txt
python3 vault_insights.py
python3 vault_insights.py --save insights.json
```

## Usage as a Python Library

```python
from vault_api import ObsidianVault

# Initialize
vault = ObsidianVault()
vault.load()

# Search
results = vault.search('investigation', limit=5)
for result in results:
    print(f"{result.title}: {result.relevance}")

# Get entity info
info = vault.get_entity_info('Junyuan Wang')
print(f"Connections: {info['network']['nodes']}")

# Find relationships
path = vault.find_path('Entity A', 'Entity B')
common = vault.find_common_connections('Entity A', 'Entity B')

# Get files
files = vault.list_files()
file = vault.get_file('path/to/file.md')

# Get statistics
stats = vault.get_statistics()
print(f"Files: {stats['total_files']}")
print(f"Entities: {stats['total_entities']}")
```

## File Structure

```
vault_loader.py       - Core parsing engine
vault_api.py          - Main API interface
vault_cli.py          - Command-line tool
vault_search.py       - Search and indexing
entity_graph.py       - Relationship analysis
vault_insights.py     - Analytics generator
vault_examples.py     - Usage examples
VAULT_LOADER_README.md        - Detailed documentation
IMPLEMENTATION_SUMMARY.md     - Project overview
QUICK_START.md               - This file
```

## Current Vault Stats

- 47 Files
- 21 Entities
- 72 Tags
- 36 Relationships
- 4,524 Indexed Words

## Common Workflows

### Find everything about an entity
```bash
python3 vault_cli.py entity "Junyuan Wang"
python3 vault_cli.py graph --name "Junyuan Wang"
python3 vault_cli.py search "Junyuan Wang" --limit 10
```

### Find connections between two people
```bash
python3 vault_cli.py graph --source "Junyuan Wang" --target "Brandon Han"
python3 vault_cli.py graph --common "Junyuan Wang,Brandon Han"
```

### Explore a topic
```bash
python3 vault_cli.py search "technology transfer"
python3 vault_cli.py tags --tag investigation
python3 vault_cli.py files --category Analysis
```

### Get comprehensive analysis
```bash
python3 vault_cli.py info
python3 vault_insights.py
python3 vault_cli.py report --output report.txt
```

### Export for external analysis
```bash
python3 vault_cli.py export --format json --output data.json
python3 vault_cli.py export --format csv --output data.csv
```

## Help

```bash
python3 vault_cli.py --help
python3 vault_cli.py search --help
python3 vault_cli.py entity --help
python3 vault_cli.py graph --help
```

## Performance

- First load: ~2-5 seconds (including indexing)
- Search: <100ms typical
- Entity lookup: <10ms typical
- Graph operations: <50ms typical

## Features

✅ Full-text search with relevance ranking
✅ Entity discovery and relationship analysis
✅ Tag-based browsing and filtering
✅ Related file finding
✅ Shortest path discovery
✅ Common connection detection
✅ Category organization
✅ Data export (JSON, CSV)
✅ Report generation
✅ Statistical analysis
✅ CLI interface
✅ Python API

## For More Information

- See `VAULT_LOADER_README.md` for detailed API documentation
- See `IMPLEMENTATION_SUMMARY.md` for architecture overview
- See `vault_examples.py` for code examples
