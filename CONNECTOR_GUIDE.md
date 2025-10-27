# Obsidian-Claude Connector Guide

Complete guide for using the Obsidian-Claude connector to programmatically interact with your vault.

## Overview

The Obsidian-Claude connector provides a Python API for:
- Reading and writing notes
- Searching across your vault
- Extracting metadata (tags, links, backlinks)
- Analyzing vault statistics
- Creating notes from templates

## Installation

### Requirements
- Python 3.7 or higher
- Git (for sync functionality)

### Setup
```bash
# Navigate to your vault
cd ~/Documents/Obsidian/obsidian-vault

# No additional packages required! The connector uses only Python stdlib
# Optional: Install enhanced features
pip install anthropic python-frontmatter watchdog rich
```

## Quick Start

### Basic Usage

```python
from obsidian_connector import ObsidianConnector

# Initialize connector (uses current directory by default)
connector = ObsidianConnector()

# Or specify vault path
connector = ObsidianConnector('/path/to/vault')

# List all notes
notes = connector.list_notes()
print(f"Found {len(notes)} notes")

# Read a specific note
note = connector.read_note('Welcome.md')
print(f"Title: {note.title}")
print(f"Tags: {note.tags}")
print(f"Links: {note.links}")
print(f"Content: {note.content[:100]}...")

# Create a new note
connector.write_note(
    'Ideas/New Idea.md',
    '# New Idea\n\nThis is a new note!\n\n#ideas #draft'
)

# Search for content
results = connector.search_notes('DARPA')
for result in results:
    print(f"{result['path']}: {result['match_count']} matches")

# Find notes by tag
tagged_notes = connector.search_by_tag('investigation')
print(f"Found {len(tagged_notes)} notes with #investigation")

# Get vault statistics
stats = connector.get_vault_stats()
print(f"Total notes: {stats['total_notes']}")
print(f"Total words: {stats['total_words']}")
```

## API Reference

### ObsidianConnector Class

#### `__init__(vault_path: str = None)`
Initialize the connector with the path to your vault.

**Parameters:**
- `vault_path`: Path to vault (defaults to current directory)

#### `list_notes(pattern: str = "**/*.md") -> List[str]`
List all markdown notes in the vault.

**Parameters:**
- `pattern`: Glob pattern to filter notes

**Returns:** List of relative paths to notes

**Example:**
```python
# All notes
all_notes = connector.list_notes()

# Notes in specific folder
entity_notes = connector.list_notes('Entities/**/*.md')

# Notes matching pattern
people = connector.list_notes('Entities/People/*.md')
```

#### `read_note(note_path: str) -> Note`
Read a specific note with all metadata.

**Parameters:**
- `note_path`: Relative path to the note

**Returns:** Note object with:
- `path`: Relative path
- `title`: Note title (from filename)
- `content`: Full content
- `tags`: Extracted tags
- `links`: Internal links
- `created`: Creation timestamp
- `modified`: Last modification timestamp
- `word_count`: Number of words

**Example:**
```python
note = connector.read_note('Analysis/Threat Assessment.md')
print(f"Title: {note.title}")
print(f"Tags: {', '.join(note.tags)}")
print(f"Links to: {', '.join(note.links)}")
print(f"Words: {note.word_count}")
```

#### `write_note(note_path: str, content: str, create_dirs: bool = True) -> str`
Write or update a note.

**Parameters:**
- `note_path`: Where to save the note
- `content`: Note content
- `create_dirs`: Create parent directories if needed

**Returns:** Absolute path to the created note

**Example:**
```python
# Create a new note
connector.write_note(
    'Projects/New Project.md',
    '''# New Project

## Overview
Project description here

## Tasks
- [ ] Task 1
- [ ] Task 2

#project #active
'''
)

# Update existing note
note = connector.read_note('Timeline.md')
updated_content = note.content + '\n\n## New Entry\n- Added today'
connector.write_note('Timeline.md', updated_content)
```

#### `search_notes(query: str, case_sensitive: bool = False) -> List[Dict]`
Search for notes containing a query string.

**Parameters:**
- `query`: Search query
- `case_sensitive`: Case-sensitive search

**Returns:** List of dictionaries with:
- `path`: Note path
- `title`: Note title
- `matches`: List of matching lines with line numbers
- `match_count`: Number of matches

**Example:**
```python
# Search for keyword
results = connector.search_notes('DARPA BRAIN')

for result in results:
    print(f"\n{result['path']} ({result['match_count']} matches)")
    for match in result['matches'][:3]:  # Show first 3
        print(f"  Line {match['line_number']}: {match['line']}")
```

#### `search_by_tag(tag: str) -> List[Note]`
Find all notes with a specific tag.

**Parameters:**
- `tag`: Tag to search for (with or without #)

**Returns:** List of Note objects

**Example:**
```python
# Find all investigation notes
investigations = connector.search_by_tag('investigation')

for note in investigations:
    print(f"- {note.title} ({note.word_count} words)")
```

#### `get_backlinks(note_title: str) -> List[Note]`
Find all notes that link to a specific note.

**Parameters:**
- `note_title`: Title of note to find backlinks for

**Returns:** List of Note objects that link to the specified note

**Example:**
```python
# Find what links to a person
backlinks = connector.get_backlinks('Brandon Han')

print(f"Notes linking to Brandon Han:")
for note in backlinks:
    print(f"  - {note.title}")
```

#### `get_all_tags() -> Dict[str, int]`
Get all tags used in the vault with frequency.

**Returns:** Dictionary mapping tag name to count

**Example:**
```python
tags = connector.get_all_tags()

print("Most used tags:")
for tag, count in list(tags.items())[:10]:
    print(f"  #{tag}: {count} notes")
```

#### `get_vault_stats() -> Dict`
Get statistics about the vault.

**Returns:** Dictionary with:
- `total_notes`: Number of notes
- `total_words`: Total word count
- `unique_tags`: Number of unique tags
- `unique_links`: Number of unique links
- `vault_path`: Path to vault

**Example:**
```python
stats = connector.get_vault_stats()
print(f"Vault Statistics:")
print(f"  Notes: {stats['total_notes']}")
print(f"  Words: {stats['total_words']}")
print(f"  Tags: {stats['unique_tags']}")
print(f"  Links: {stats['unique_links']}")
```

#### `create_note_from_template(note_path: str, template_path: str, variables: Dict[str, str] = None) -> str`
Create a new note from a template.

**Parameters:**
- `note_path`: Where to create the note
- `template_path`: Path to template
- `variables`: Variables to replace ({{variable}} format)

**Returns:** Path to created note

**Example:**
```python
# Create a template
connector.write_note(
    'Templates/Person.md',
    '''# {{name}}

## Overview
{{description}}

## Links
- Organization: [[{{organization}}]]

Created: {{date}}

#person #entity
'''
)

# Use the template
connector.create_note_from_template(
    'Entities/People/New Person.md',
    'Templates/Person.md',
    variables={
        'name': 'New Person',
        'description': 'Person description',
        'organization': 'Company Name'
    }
)
```

## Integration with Claude

### Using the Connector with Claude API

```python
import os
from anthropic import Anthropic
from obsidian_connector import ObsidianConnector

# Initialize
connector = ObsidianConnector()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Read context from vault
note = connector.read_note('INVESTIGATION_SUMMARY.md')

# Ask Claude about your notes
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Analyze this investigation summary and provide insights:\n\n{note.content}"
    }]
)

# Save Claude's response as a new note
connector.write_note(
    'Analysis/Claude Analysis.md',
    f"# Claude Analysis\n\n{message.content[0].text}\n\n#analysis #claude"
)
```

## Advanced Usage

### Batch Operations

```python
# Update multiple notes
for note_path in connector.list_notes('Entities/People/*.md'):
    note = connector.read_note(note_path)

    # Add a tag if not present
    if 'reviewed' not in note.tags:
        content = note.content + '\n\n#reviewed'
        connector.write_note(note_path, content)
```

### Building a Knowledge Graph

```python
# Build a graph of connections
graph = {}

for note_path in connector.list_notes():
    note = connector.read_note(note_path)
    graph[note.title] = {
        'tags': note.tags,
        'links': note.links,
        'backlinks': [n.title for n in connector.get_backlinks(note.title)]
    }

# Find most connected notes
sorted_notes = sorted(
    graph.items(),
    key=lambda x: len(x[1]['links']) + len(x[1]['backlinks']),
    reverse=True
)

print("Most connected notes:")
for title, data in sorted_notes[:10]:
    connections = len(data['links']) + len(data['backlinks'])
    print(f"  {title}: {connections} connections")
```

### Daily Note Automation

```python
from datetime import datetime

# Create daily note
today = datetime.now().strftime('%Y-%m-%d')
connector.write_note(
    f'{today}.md',
    f'''# Daily Note - {today}

## Summary


## Tasks
- [ ]

## Notes


#daily
'''
)
```

## Configuration

Edit `connector_config.json` to customize:

```json
{
  "vault": {
    "path": "/home/user/obsidian-vault",
    "name": "obsidian-vault"
  },
  "search": {
    "case_sensitive": false,
    "max_results": 100,
    "exclude_patterns": [".git/*", ".obsidian/*"]
  },
  "claude": {
    "integration_enabled": true,
    "model": "claude-3-5-sonnet-20241022"
  }
}
```

## CLI Tool

Use the provided CLI tool for quick operations:

```bash
# Get vault stats
python vault_cli.py stats

# Search notes
python vault_cli.py search "DARPA"

# List notes
python vault_cli.py list

# Read a note
python vault_cli.py read "Welcome.md"

# Find notes by tag
python vault_cli.py tags investigation

# Get backlinks
python vault_cli.py backlinks "Brandon Han"
```

## Sync with Git

The connector works seamlessly with the auto-sync setup:

```bash
# Make changes via connector
python -c "
from obsidian_connector import ObsidianConnector
c = ObsidianConnector()
c.write_note('test.md', '# Test\nContent')
"

# Sync will happen automatically every 5 minutes
# Or trigger manually
./.sync-vault.sh
```

## Best Practices

1. **Always use relative paths** from the vault root
2. **Include file extensions** (.md) when creating notes
3. **Use tags** for better organization and searchability
4. **Create templates** for repetitive note structures
5. **Check for existing notes** before creating new ones
6. **Use backlinks** to build connections between notes
7. **Let auto-sync handle git operations** - don't commit manually

## Troubleshooting

### Note not found
Ensure you're using the correct relative path from vault root:
```python
# Wrong
connector.read_note('/home/user/obsidian-vault/Welcome.md')

# Correct
connector.read_note('Welcome.md')
```

### Encoding errors
The connector uses UTF-8 encoding. If you have special characters, ensure files are UTF-8 encoded.

### Search returns no results
Check case sensitivity and verify the content exists:
```python
# Case insensitive (default)
results = connector.search_notes('darpa')

# Case sensitive
results = connector.search_notes('DARPA', case_sensitive=True)
```

## Support

For issues or questions:
- Check this guide
- Review the code comments in `obsidian_connector.py`
- Test with the CLI tool: `python vault_cli.py`

## License

MIT License - Free to use and modify
