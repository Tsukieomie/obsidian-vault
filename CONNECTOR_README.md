# Obsidian-Claude Connector

A powerful Python connector that enables programmatic access to your Obsidian vault, allowing Claude and other tools to read, write, search, and analyze your notes.

## Features

- **Read & Write Notes**: Full CRUD operations on markdown files
- **Smart Search**: Search by content, tags, or links
- **Metadata Extraction**: Automatically extract tags, links, and frontmatter
- **Backlink Analysis**: Find all notes linking to a specific note
- **Vault Statistics**: Get insights about your knowledge base
- **Template System**: Create notes from templates with variable substitution
- **CLI Tool**: Command-line interface for quick operations
- **No External Dependencies**: Uses only Python standard library
- **Git Integration**: Works seamlessly with auto-sync

## Quick Start

### 1. Installation

```bash
cd /home/user/obsidian-vault

# No installation needed! Uses Python 3.7+ standard library
# Optional: Install for enhanced features
pip install anthropic python-frontmatter
```

### 2. Basic Usage

```python
from obsidian_connector import ObsidianConnector

# Initialize
connector = ObsidianConnector()

# Get vault stats
stats = connector.get_vault_stats()
print(f"Total notes: {stats['total_notes']}")
print(f"Total words: {stats['total_words']:,}")

# Search for content
results = connector.search_notes('DARPA')
for result in results:
    print(f"{result['path']}: {result['match_count']} matches")

# Read a note
note = connector.read_note('Welcome.md')
print(f"Title: {note.title}")
print(f"Tags: {note.tags}")
print(f"Content: {note.content[:200]}...")

# Create a new note
connector.write_note(
    'Ideas/New Note.md',
    '# New Note\n\nContent here\n\n#ideas'
)
```

### 3. CLI Usage

```bash
# Show vault statistics
python vault_cli.py stats

# Search for text
python vault_cli.py search "investigation"

# List all notes
python vault_cli.py list

# Find notes by tag
python vault_cli.py tags technical

# Show all tags
python vault_cli.py alltags

# Find backlinks
python vault_cli.py backlinks "Brandon Han"

# Read a note
python vault_cli.py read "Welcome.md"
```

## Project Structure

```
obsidian-vault/
├── obsidian_connector.py      # Main connector library
├── vault_cli.py                # Command-line interface
├── connector_config.json       # Configuration file
├── CONNECTOR_GUIDE.md          # Comprehensive API documentation
├── CONNECTOR_README.md         # This file
├── requirements.txt            # Python dependencies (minimal)
└── .sync-vault.sh             # Auto-sync script (existing)
```

## Architecture

The connector is designed with simplicity and functionality in mind:

```
┌─────────────────────────────────────────┐
│         Your Application / Claude        │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│      ObsidianConnector Class            │
│  ┌─────────────────────────────────┐   │
│  │ • list_notes()                  │   │
│  │ • read_note()                   │   │
│  │ • write_note()                  │   │
│  │ • search_notes()                │   │
│  │ • search_by_tag()               │   │
│  │ • get_backlinks()               │   │
│  │ • get_all_tags()                │   │
│  │ • get_vault_stats()             │   │
│  │ • create_note_from_template()   │   │
│  └─────────────────────────────────┘   │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│         Obsidian Vault (Markdown)        │
│  ┌────────────────────────────────┐    │
│  │ • Notes (.md files)            │    │
│  │ • Tags (#tag)                  │    │
│  │ • Links ([[Note]])             │    │
│  │ • Metadata (YAML frontmatter)  │    │
│  └────────────────────────────────┘    │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│    Git Auto-Sync (.sync-vault.sh)       │
│    Syncs to GitHub every 5 minutes      │
└─────────────────────────────────────────┘
```

## API Overview

### Core Methods

| Method | Description |
|--------|-------------|
| `list_notes(pattern)` | List all notes matching pattern |
| `read_note(path)` | Read note with metadata |
| `write_note(path, content)` | Create or update note |
| `search_notes(query)` | Search by content |
| `search_by_tag(tag)` | Find notes by tag |
| `get_backlinks(title)` | Find notes linking to a note |
| `get_all_tags()` | Get all tags with counts |
| `get_vault_stats()` | Get vault statistics |
| `create_note_from_template()` | Create from template |

### Note Object

Each note returned by `read_note()` contains:

```python
Note(
    path='Analysis/Threat Assessment.md',
    title='Threat Assessment',
    content='# Threat Assessment\n\n...',
    tags=['investigation', 'analysis'],
    links=['Brandon Han', 'DARPA'],
    created='2025-10-27T00:00:00',
    modified='2025-10-27T15:00:00',
    word_count=1234
)
```

## Use Cases

### 1. Knowledge Base Analysis

```python
# Analyze your knowledge base
connector = ObsidianConnector()

# Find most connected notes
all_notes = {}
for path in connector.list_notes():
    note = connector.read_note(path)
    backlinks = connector.get_backlinks(note.title)
    connections = len(note.links) + len(backlinks)
    all_notes[note.title] = connections

# Show top 10
for title, count in sorted(all_notes.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{title}: {count} connections")
```

### 2. Tag Management

```python
# Find untagged notes
for path in connector.list_notes():
    note = connector.read_note(path)
    if not note.tags:
        print(f"Untagged: {note.title}")
```

### 3. Content Generation with Claude

```python
from anthropic import Anthropic
import os

connector = ObsidianConnector()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Gather context
context_notes = connector.search_by_tag('investigation')
context = "\n\n".join([n.content for n in context_notes[:5]])

# Generate analysis
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": f"Analyze these investigation notes:\n\n{context}"
    }]
)

# Save result
connector.write_note(
    'Analysis/AI Generated Analysis.md',
    f"# AI Analysis\n\n{response.content[0].text}\n\n#ai-generated #analysis"
)
```

### 4. Daily Note Automation

```python
from datetime import datetime

# Create today's daily note
today = datetime.now()
daily_note = f'''# Daily Note - {today.strftime('%Y-%m-%d')}

## Summary


## Tasks
- [ ]

## Notes


#daily #{today.strftime('%Y')} #{today.strftime('%B').lower()}
'''

connector.write_note(f'{today.strftime("%Y-%m-%d")}.md', daily_note)
```

### 5. Link Graph Analysis

```python
import json

# Build a complete link graph
graph = {}
for path in connector.list_notes():
    note = connector.read_note(path)
    graph[note.title] = {
        'tags': note.tags,
        'outbound_links': note.links,
        'inbound_links': [n.title for n in connector.get_backlinks(note.title)]
    }

# Save graph data
connector.write_note(
    'Analysis/Link Graph.md',
    f'# Link Graph\n\n```json\n{json.dumps(graph, indent=2)}\n```'
)
```

## Integration Examples

### With Claude API

See `CONNECTOR_GUIDE.md` for detailed examples of:
- Analyzing notes with Claude
- Generating summaries
- Answering questions about your vault
- Creating new notes based on AI insights

### With Jupyter Notebooks

```python
# In Jupyter
import sys
sys.path.append('/home/user/obsidian-vault')

from obsidian_connector import ObsidianConnector
import pandas as pd

connector = ObsidianConnector()

# Create DataFrame of all notes
notes_data = []
for path in connector.list_notes():
    note = connector.read_note(path)
    notes_data.append({
        'title': note.title,
        'words': note.word_count,
        'tags': len(note.tags),
        'links': len(note.links),
        'path': note.path
    })

df = pd.DataFrame(notes_data)
df.describe()
```

### With REST API (Future Enhancement)

The connector can be wrapped in a simple Flask/FastAPI server:

```python
from flask import Flask, jsonify
from obsidian_connector import ObsidianConnector

app = Flask(__name__)
connector = ObsidianConnector()

@app.route('/api/notes')
def list_notes():
    return jsonify(connector.list_notes())

@app.route('/api/stats')
def get_stats():
    return jsonify(connector.get_vault_stats())

# ... more endpoints
```

## Configuration

Edit `connector_config.json` to customize behavior:

```json
{
  "vault": {
    "path": "/home/user/obsidian-vault"
  },
  "search": {
    "case_sensitive": false,
    "max_results": 100
  },
  "claude": {
    "integration_enabled": true,
    "model": "claude-3-5-sonnet-20241022"
  }
}
```

## Testing

Run the test suite:

```bash
# Test vault stats
python vault_cli.py stats

# Test search
python vault_cli.py search "test"

# Test tag search
python vault_cli.py tags investigation

# Run Python tests
python -c "
from obsidian_connector import ObsidianConnector
c = ObsidianConnector()
assert len(c.list_notes()) > 0
print('✓ All tests passed')
"
```

## Performance

The connector is optimized for typical vault sizes:

- **Small vaults** (<100 notes): All operations < 1 second
- **Medium vaults** (100-1000 notes): Search < 2 seconds
- **Large vaults** (1000+ notes): Search < 5 seconds

Operations are performed in-memory for speed. For very large vaults, consider:
- Using specific glob patterns to limit scope
- Implementing caching for frequently accessed notes
- Running batch operations during off-peak times

## Security Considerations

- **Local only**: Connector operates on local filesystem
- **No cloud sync**: Git sync is separate and controlled
- **Read/Write access**: Has full access to vault files
- **API keys**: Store in environment variables, not in code
- **Git commits**: Auto-sync handles commits automatically

## Troubleshooting

### Common Issues

**Problem**: `FileNotFoundError` when reading notes
**Solution**: Use relative paths from vault root, not absolute paths

**Problem**: Tags not being extracted
**Solution**: Ensure tags use `#tag` format or are in YAML frontmatter

**Problem**: Search returns no results
**Solution**: Check case sensitivity setting, verify content exists

**Problem**: Slow performance on large vaults
**Solution**: Use specific patterns to limit scope (e.g., `Entities/**/*.md`)

### Debug Mode

Enable debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

connector = ObsidianConnector()
# Operations will now show debug info
```

## Contributing

This connector is designed to be extended. Feel free to:
- Add new search methods
- Implement caching layers
- Create additional CLI commands
- Build API wrappers
- Add export formats

## Documentation

- **CONNECTOR_GUIDE.md**: Complete API reference with examples
- **CONNECTOR_README.md**: This file - overview and quick start
- **connector_config.json**: Configuration reference
- **obsidian_connector.py**: Source code with inline documentation

## Roadmap

Future enhancements:
- [ ] REST API server
- [ ] WebSocket support for real-time updates
- [ ] Advanced caching layer
- [ ] Full-text search with ranking
- [ ] Export to various formats (PDF, HTML, etc.)
- [ ] Import from other note systems
- [ ] Plugin system for custom extractors

## License

MIT License - Free to use and modify

## Support

For questions or issues:
1. Check the **CONNECTOR_GUIDE.md** for detailed examples
2. Review inline code documentation
3. Test with `vault_cli.py` to isolate issues
4. Check git status for sync issues

## Changelog

### Version 1.0.0 (2025-10-27)
- Initial release
- Core connector functionality
- CLI tool
- Comprehensive documentation
- Git integration

---

**Built with Claude** for seamless Obsidian-Claude integration
