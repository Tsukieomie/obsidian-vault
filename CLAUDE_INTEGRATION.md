# Claude API Integration Guide

Complete guide for integrating Claude AI with your Obsidian vault using the connector.

## Overview

The Claude integration enables AI-powered features for your vault:
- **Intelligent Analysis**: Have Claude analyze notes and extract insights
- **Smart Search**: Search with AI-powered result interpretation
- **Note Generation**: Create new notes on any topic
- **Tag Suggestions**: Get intelligent tag recommendations
- **Connection Discovery**: Find related notes automatically
- **Entity Extraction**: Extract people, organizations, and topics
- **Batch Analysis**: Analyze multiple notes by tag or topic

## Setup

### 1. Install Requirements

```bash
# Install the Anthropic Python SDK
pip install anthropic

# Or install all optional dependencies
pip install -r requirements.txt
```

### 2. Get Your API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy your key (starts with `sk-ant-...`)

### 3. Set Environment Variable

```bash
# Linux/Mac
export ANTHROPIC_API_KEY='your-key-here'

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY='your-key-here'

# Windows (CMD)
set ANTHROPIC_API_KEY=your-key-here

# Add to your shell profile for persistence
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
# or ~/.zshrc, etc.
```

## Quick Start

### Basic Usage

```python
from claude_integration import ClaudeObsidianIntegration

# Initialize
integration = ClaudeObsidianIntegration()

# Analyze a note
analysis = integration.analyze_note('Welcome.md')
print(analysis)

# Smart search
results = integration.smart_search('DARPA research')
print(results)

# Generate a new note
content = integration.generate_note(
    'Overview of neurotechnology',
    include_tags=['research', 'technology'],
    save=True
)
```

## API Reference

### ClaudeObsidianIntegration Class

#### `__init__(vault_path=None, api_key=None)`

Initialize the integration.

**Parameters:**
- `vault_path`: Path to vault (default: current directory)
- `api_key`: API key (default: from ANTHROPIC_API_KEY env var)

**Example:**
```python
# Use defaults
integration = ClaudeObsidianIntegration()

# Specify vault path
integration = ClaudeObsidianIntegration('/path/to/vault')

# Provide API key directly
integration = ClaudeObsidianIntegration(api_key='sk-ant-...')
```

---

#### `ask_about_note(note_path, question, max_tokens=1024)`

Ask Claude a question about a specific note.

**Parameters:**
- `note_path`: Path to the note
- `question`: Question to ask
- `max_tokens`: Maximum tokens in response

**Returns:** Claude's answer as string

**Example:**
```python
answer = integration.ask_about_note(
    'Analysis/Threat Assessment.md',
    'What are the main security concerns mentioned?'
)
print(answer)
```

---

#### `analyze_note(note_path, save_analysis=True)`

Have Claude analyze a note comprehensively.

**Parameters:**
- `note_path`: Path to the note
- `save_analysis`: Whether to save analysis as new note

**Returns:** Analysis text

**Saves to:** `Analysis/Claude - {note_title}.md`

**Example:**
```python
# Analyze and save
analysis = integration.analyze_note('INVESTIGATION_SUMMARY.md')

# Analyze without saving
analysis = integration.analyze_note(
    'Timeline.md',
    save_analysis=False
)
```

---

#### `summarize_notes(note_paths, save_summary=True)`

Generate a summary of multiple related notes.

**Parameters:**
- `note_paths`: List of note paths
- `save_summary`: Whether to save summary

**Returns:** Summary text

**Saves to:** `Analysis/Summary - {timestamp}.md`

**Example:**
```python
# Summarize related notes
notes_to_summarize = [
    'Entities/People/Brandon Han.md',
    'Entities/People/Jerry Han.md',
    'Entities/Organizations/Asymptote Network LLC.md'
]

summary = integration.summarize_notes(notes_to_summarize)
print(summary)
```

---

#### `smart_search(query, max_results=5)`

Intelligent search with AI-powered result interpretation.

**Parameters:**
- `query`: Search query
- `max_results`: Number of results to analyze

**Returns:** Intelligent summary of search results

**Example:**
```python
# Traditional search would just return matching notes
# Smart search provides context and insights

result = integration.smart_search('DARPA BRAIN Initiative')
print(result)

# Output includes:
# - Summary of what the notes are about
# - How they relate to the query
# - Key insights across notes
# - Suggested next steps
```

---

#### `generate_note(topic, include_tags=None, link_to=None, save=True)`

Generate a new note on any topic using Claude.

**Parameters:**
- `topic`: Topic for the note
- `include_tags`: List of tags to include
- `link_to`: List of note paths to reference for context
- `save`: Whether to save the note

**Returns:** Generated note content

**Saves to:** `AI Generated/{topic}.md`

**Example:**
```python
# Simple generation
content = integration.generate_note('Neural interface basics')

# With tags and context
content = integration.generate_note(
    topic='Analysis of current threats',
    include_tags=['security', 'analysis', 'urgent'],
    link_to=['Entities/DARPA.md', 'Technical/AS53616 Network Analysis.md'],
    save=True
)
```

---

#### `extract_entities(note_path)`

Extract entities (people, organizations, locations, etc.) from a note.

**Parameters:**
- `note_path`: Path to the note

**Returns:** Dictionary with entity categories

**Example:**
```python
entities = integration.extract_entities('INVESTIGATION_SUMMARY.md')

print(f"People: {entities['people']}")
print(f"Organizations: {entities['organizations']}")
print(f"Locations: {entities['locations']}")
print(f"Topics: {entities['topics']}")
print(f"Dates: {entities['dates']}")

# Output:
# People: ['Brandon Han', 'Jerry Han', 'Carlos Montt']
# Organizations: ['DARPA', 'Duke University', 'Asymptote Network LLC']
# Locations: ['Oklahoma', 'North Carolina']
# Topics: ['neural interfaces', 'BRAIN Initiative', 'network security']
# Dates: ['2013', '2024-10-27']
```

---

#### `suggest_tags(note_path, max_tags=5)`

Get intelligent tag suggestions based on note content.

**Parameters:**
- `note_path`: Path to the note
- `max_tags`: Maximum number of tags to suggest

**Returns:** List of suggested tag names

**Example:**
```python
suggestions = integration.suggest_tags('Welcome.md', max_tags=5)
print(f"Suggested tags: {', '.join([f'#{tag}' for tag in suggestions])}")

# Claude considers:
# - Note content and themes
# - Existing tags in the vault
# - Common tagging patterns
```

---

#### `find_connections(note_path)`

Find potential connections between a note and others in the vault.

**Parameters:**
- `note_path`: Path to the note

**Returns:** List of dictionaries with title and reason

**Example:**
```python
connections = integration.find_connections('Entities/People/Brandon Han.md')

for conn in connections:
    print(f"Connect to: {conn['title']}")
    print(f"Reason: {conn['reason']}\n")

# Output:
# Connect to: Asymptote Network LLC
# Reason: Brandon Han is associated with this organization
#
# Connect to: Technical Analysis
# Reason: Technical details relate to Brandon Han's activities
```

---

#### `batch_analyze_by_tag(tag, save_report=True)`

Analyze all notes with a specific tag and generate insights.

**Parameters:**
- `tag`: Tag to filter by (without #)
- `save_report`: Whether to save the report

**Returns:** Analysis report text

**Saves to:** `Analysis/Tag Analysis - {tag}.md`

**Example:**
```python
# Analyze all investigation notes
report = integration.batch_analyze_by_tag('investigation')

# Report includes:
# - Overview of what notes cover
# - Common themes and patterns
# - Key insights
# - Gaps or areas to explore
# - Suggested next actions
```

## Example Scripts

The `examples/` directory contains ready-to-use scripts:

### 1. Analyze Vault
```bash
python examples/analyze_vault.py
```
Analyzes your entire vault by top tags and generates reports.

### 2. Smart Search
```bash
python examples/smart_search.py "DARPA BRAIN"
```
Search with AI-powered interpretation of results.

### 3. Generate Notes
```bash
python examples/generate_notes.py "Neural interface technology"
```
Generate new notes on any topic.

### 4. Suggest Tags
```bash
python examples/suggest_tags.py
```
Get tag suggestions for notes that need them.

### 5. Find Connections
```bash
python examples/find_connections.py "Entities/People/Brandon Han.md"
```
Discover connections between notes.

## Use Cases

### 1. Research Assistant

```python
# Ask Claude about your research
answer = integration.ask_about_note(
    'Analysis/DARPA_BRAIN_Patents_Research.md',
    'What are the key patents mentioned and what do they cover?'
)

# Generate follow-up notes
integration.generate_note(
    'Deep dive into DARPA BRAIN patents',
    link_to=['Analysis/DARPA_BRAIN_Patents_Research.md']
)
```

### 2. Knowledge Base Maintenance

```python
# Find notes needing tags
connector = integration.connector
for path in connector.list_notes():
    note = connector.read_note(path)
    if len(note.tags) < 2:
        suggestions = integration.suggest_tags(path)
        print(f"{note.title}: {suggestions}")
```

### 3. Investigation Support

```python
# Analyze all evidence
evidence_notes = connector.search_by_tag('evidence')
evidence_paths = [note.path for note in evidence_notes]
summary = integration.summarize_notes(evidence_paths)

# Find connections between entities
connections = integration.find_connections('Entities/People/Brandon Han.md')
```

### 4. Content Generation

```python
# Generate multiple related notes
topics = [
    'Overview of neural interfaces',
    'DARPA BRAIN Initiative timeline',
    'Key players in neurotechnology'
]

for topic in topics:
    integration.generate_note(
        topic,
        include_tags=['research', 'generated'],
        save=True
    )
```

### 5. Daily Workflow

```python
from datetime import datetime

# Morning: Analyze yesterday's notes
yesterday_notes = []  # Get notes from yesterday
if yesterday_notes:
    summary = integration.summarize_notes(yesterday_notes)
    # Review summary and plan today

# During day: Quick searches
results = integration.smart_search('current investigation status')

# Evening: Generate daily summary
integration.generate_note(
    f"Daily Summary - {datetime.now().strftime('%Y-%m-%d')}",
    include_tags=['daily', 'summary']
)
```

## Advanced Integration

### Custom Workflows

```python
class CustomWorkflow:
    def __init__(self):
        self.integration = ClaudeObsidianIntegration()

    def weekly_review(self):
        """Generate a weekly review of all activity"""
        connector = self.integration.connector

        # Get all notes modified this week
        recent_notes = []  # Filter by modification date

        # Summarize the week
        summary = self.integration.summarize_notes(recent_notes)

        # Generate action items
        action_items = self.integration.ask_about_note(
            summary,
            "What are the key action items for next week?"
        )

        return summary, action_items
```

### API Response Streaming

```python
# For long responses, you can stream the output
from anthropic import Anthropic

client = Anthropic()

with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=[{"role": "user", "content": "Analyze this..."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Error Handling

```python
try:
    analysis = integration.analyze_note('nonexistent.md')
except FileNotFoundError:
    print("Note not found")
except Exception as e:
    print(f"Error: {e}")
```

## Best Practices

### 1. API Usage

- **Cache results**: Don't re-analyze the same content repeatedly
- **Batch operations**: Process multiple notes when possible
- **Use appropriate max_tokens**: Start small, increase if needed
- **Handle rate limits**: Add delays between requests if needed

### 2. Note Generation

- **Review AI content**: Always review generated notes before finalizing
- **Provide context**: Link to related notes for better generation
- **Use specific prompts**: More specific topics yield better results
- **Tag appropriately**: Always tag AI-generated content

### 3. Search and Analysis

- **Start specific**: Specific queries yield better results
- **Use smart search**: Let Claude interpret ambiguous queries
- **Combine methods**: Use traditional + AI search together
- **Save reports**: Keep analysis reports for reference

### 4. Cost Management

- **Monitor usage**: Track API calls and token usage
- **Optimize prompts**: Shorter prompts = lower costs
- **Use caching**: Cache repeated queries
- **Batch when possible**: Process multiple items in one call

## Configuration

Edit `connector_config.json` for Claude settings:

```json
{
  "claude": {
    "integration_enabled": true,
    "model": "claude-3-5-sonnet-20241022",
    "api_key_env": "ANTHROPIC_API_KEY",
    "max_tokens_default": 1024,
    "temperature": 1.0
  }
}
```

## Troubleshooting

### API Key Issues

```
Error: API key required
```
**Solution**: Set `ANTHROPIC_API_KEY` environment variable

### Import Errors

```
ImportError: anthropic package not installed
```
**Solution**: `pip install anthropic`

### Rate Limits

```
Error: 429 Too Many Requests
```
**Solution**: Add delays between requests, reduce frequency

### Token Limits

```
Error: Maximum context length exceeded
```
**Solution**: Reduce input size, summarize content first, or use smaller notes

### Connection Errors

```
Error: Connection timeout
```
**Solution**: Check internet connection, retry with exponential backoff

## Security Considerations

### API Key Safety

- ✅ Store in environment variables
- ✅ Never commit to git
- ✅ Use `.env` files with `.gitignore`
- ❌ Don't hardcode in scripts
- ❌ Don't share in public repos

### Data Privacy

- Notes are sent to Anthropic's API
- Consider data sensitivity before using AI features
- Review Anthropic's privacy policy
- Use on-device models for sensitive data (when available)

### Access Control

- API key grants full access to your Claude account
- Rotate keys periodically
- Use separate keys for different projects
- Monitor usage in Anthropic console

## Model Selection

### Available Models

```python
# Sonnet (default) - Best balance of speed and quality
integration = ClaudeObsidianIntegration()
integration.model = "claude-3-5-sonnet-20241022"

# Opus - Highest quality, slower, more expensive
integration.model = "claude-3-opus-20240229"

# Haiku - Fastest, cheapest, good for simple tasks
integration.model = "claude-3-haiku-20240307"
```

### When to Use Each

- **Sonnet**: General purpose, recommended default
- **Opus**: Complex analysis, important decisions
- **Haiku**: Tag suggestions, simple searches, batch operations

## Pricing

Current pricing (as of 2024):
- **Claude 3.5 Sonnet**: $3/$15 per million tokens (input/output)
- **Claude 3 Opus**: $15/$75 per million tokens
- **Claude 3 Haiku**: $0.25/$1.25 per million tokens

Estimate: Analyzing a 1000-word note with Sonnet costs ~$0.01

## Support

For issues:
1. Check this guide
2. Review example scripts in `examples/`
3. Check Anthropic documentation: https://docs.anthropic.com/
4. Verify API key is set correctly
5. Test with simple examples first

## Additional Resources

- **Anthropic Documentation**: https://docs.anthropic.com/
- **Claude API Console**: https://console.anthropic.com/
- **Connector Guide**: CONNECTOR_GUIDE.md
- **Example Scripts**: examples/ directory

## License

MIT License - Free to use and modify

---

**Built with Claude** for intelligent knowledge management
