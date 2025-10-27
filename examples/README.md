# Claude Integration Examples

Example scripts demonstrating the Obsidian-Claude integration.

## Setup

Before running these examples:

1. **Install requirements:**
   ```bash
   pip install anthropic
   ```

2. **Set your API key:**
   ```bash
   export ANTHROPIC_API_KEY='your-key-here'
   ```

3. **Get an API key:** https://console.anthropic.com/

## Examples

### 1. analyze_vault.py
Analyze your entire vault by popular tags and generate insight reports.

```bash
python examples/analyze_vault.py
```

**What it does:**
- Identifies top tags in your vault
- Analyzes all notes for each tag
- Generates comprehensive reports
- Saves reports to Analysis/ folder

**Output:**
- `Analysis/Tag Analysis - {tag}.md` for each tag

---

### 2. smart_search.py
Search with AI-powered interpretation of results.

```bash
python examples/smart_search.py "DARPA BRAIN"
```

**What it does:**
- Performs traditional text search
- Sends top results to Claude
- Gets intelligent summary and insights
- Suggests related topics

**Good for:**
- Understanding complex topics
- Finding connections between notes
- Getting quick summaries
- Exploring your vault intelligently

---

### 3. generate_notes.py
Generate new notes on any topic using Claude.

```bash
python examples/generate_notes.py "Neural interface technology overview"
```

**What it does:**
- Asks Claude to create a note on the topic
- Formats for Obsidian (markdown, tags, structure)
- Saves to AI Generated/ folder
- Automatically tags as #ai-generated

**Good for:**
- Quick drafts on new topics
- Research starting points
- Expanding your knowledge base
- Generating structured content

---

### 4. suggest_tags.py
Get intelligent tag suggestions for notes.

```bash
python examples/suggest_tags.py
```

**What it does:**
- Finds notes with few or no tags
- Analyzes content and suggests relevant tags
- Considers existing vault tags
- Optionally adds tags to notes

**Good for:**
- Organizing untagged notes
- Maintaining consistent tagging
- Discovering tag opportunities
- Improving searchability

---

### 5. find_connections.py
Discover connections between notes.

```bash
python examples/find_connections.py "Entities/People/Brandon Han.md"
```

**What it does:**
- Analyzes a specific note
- Compares with other vault notes
- Suggests meaningful connections
- Optionally adds links

**Good for:**
- Building knowledge graphs
- Finding related research
- Connecting ideas
- Discovering patterns

---

## Usage Tips

### Run Multiple Examples

```bash
# Analyze vault first
python examples/analyze_vault.py

# Then search specific topics
python examples/smart_search.py "investigation status"

# Generate follow-up notes
python examples/generate_notes.py "Next steps in investigation"
```

### Customize Scripts

All scripts are designed to be modified. Key areas:

1. **Change models:**
   ```python
   integration.model = "claude-3-haiku-20240307"  # Faster, cheaper
   ```

2. **Adjust parameters:**
   ```python
   max_tokens=2048  # Longer responses
   max_results=10   # More search results
   ```

3. **Filter notes:**
   ```python
   # Only analyze recent notes
   notes = [n for n in notes if recent(n)]
   ```

### Chain Operations

```bash
# 1. Find connections
python examples/find_connections.py "Analysis/Threat Assessment.md"

# 2. Search related topics
python examples/smart_search.py "security threats"

# 3. Generate summary
python examples/generate_notes.py "Security threat analysis summary"
```

## Cost Estimates

Using Claude 3.5 Sonnet (default):

| Operation | Typical Cost |
|-----------|-------------|
| Analyze one note (1000 words) | ~$0.01 |
| Smart search (5 results) | ~$0.02 |
| Generate note (500 words) | ~$0.02 |
| Suggest tags (one note) | ~$0.005 |
| Find connections | ~$0.01 |
| Analyze vault by tag (10 notes) | ~$0.10 |

**Tips for cost control:**
- Use Haiku model for simple tasks
- Limit max_results in searches
- Process fewer notes per batch
- Cache results when possible

## Troubleshooting

### API Key Not Set

```
❌ Error: Set ANTHROPIC_API_KEY environment variable
```

**Solution:**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### anthropic Package Missing

```
ImportError: anthropic package not installed
```

**Solution:**
```bash
pip install anthropic
```

### Import Errors

```
ModuleNotFoundError: No module named 'claude_integration'
```

**Solution:** Run from vault root:
```bash
cd /home/user/obsidian-vault
python examples/analyze_vault.py
```

### Rate Limits

```
Error: 429 Too Many Requests
```

**Solution:** Add delays between requests or reduce batch size

## Creating Custom Scripts

Use these as templates:

```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_integration import ClaudeObsidianIntegration

def main():
    integration = ClaudeObsidianIntegration()

    # Your custom logic here
    # - Use integration.connector for vault access
    # - Use integration methods for AI features

if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    main()
```

## Best Practices

1. **Start small:** Test with one note before batch operations
2. **Review output:** Always review AI-generated content
3. **Save results:** Keep analysis reports for reference
4. **Monitor costs:** Track API usage in Anthropic console
5. **Use appropriate models:** Haiku for simple tasks, Sonnet for complex
6. **Handle errors:** Add try/except for production use
7. **Rate limit:** Add delays in loops

## Additional Examples

See the main integration module for more methods:
- `ask_about_note()` - Ask questions
- `extract_entities()` - Extract people, orgs, etc.
- `summarize_notes()` - Multi-note summaries
- `batch_analyze_by_tag()` - Tag-based analysis

Read `CLAUDE_INTEGRATION.md` for complete documentation.

## Contributing

Feel free to:
- Modify these examples
- Create new example scripts
- Share improvements
- Report issues

## License

MIT License - Free to use and modify
