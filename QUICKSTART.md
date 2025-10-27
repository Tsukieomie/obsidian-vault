# Quick Start Guide

Get up and running with the Obsidian-Claude connector in 5 minutes.

## Step 1: Verify Setup (30 seconds)

```bash
# Check Python version (need 3.7+)
python3 --version

# Test basic connector
python3 vault_cli.py stats
```

You should see your vault statistics. If this works, the basic connector is ready!

## Step 2: Try Basic Features (2 minutes)

```bash
# List all your notes
python3 vault_cli.py list

# Search for something
python3 vault_cli.py search "investigation"

# Show all tags
python3 vault_cli.py alltags

# Read a specific note
python3 vault_cli.py read "Welcome.md"
```

## Step 3: Use Python API (1 minute)

Create a test script `test.py`:

```python
from obsidian_connector import ObsidianConnector

# Initialize
connector = ObsidianConnector()

# Get stats
stats = connector.get_vault_stats()
print(f"Your vault has {stats['total_notes']} notes!")

# Search
results = connector.search_notes('DARPA')
print(f"Found {len(results)} notes mentioning DARPA")

# Read a note
notes = connector.list_notes()
if notes:
    note = connector.read_note(notes[0])
    print(f"\nFirst note: {note.title}")
    print(f"Tags: {note.tags}")
```

Run it:
```bash
python3 test.py
```

## Step 4: Add Claude AI (Optional - 1 minute)

If you want AI-powered features:

1. **Install anthropic:**
   ```bash
   pip install anthropic
   ```

2. **Get API key:**
   - Go to https://console.anthropic.com/
   - Create account / log in
   - Generate API key

3. **Set environment variable:**
   ```bash
   export ANTHROPIC_API_KEY='your-key-here'
   ```

4. **Test it:**
   ```python
   from claude_integration import ClaudeObsidianIntegration

   integration = ClaudeObsidianIntegration()

   # Smart search
   result = integration.smart_search('investigation')
   print(result)
   ```

## Common Tasks

### Create a New Note

```python
from obsidian_connector import ObsidianConnector

connector = ObsidianConnector()
connector.write_note(
    'Ideas/Test Note.md',
    '# Test Note\n\nThis is a test!\n\n#test'
)
```

### Search by Tag

```python
connector = ObsidianConnector()
notes = connector.search_by_tag('investigation')

for note in notes:
    print(f"- {note.title} ({note.word_count} words)")
```

### Find Backlinks

```python
connector = ObsidianConnector()
backlinks = connector.get_backlinks('Brandon Han')

print(f"Notes linking to Brandon Han:")
for note in backlinks:
    print(f"  - {note.title}")
```

### Analyze with Claude (requires API key)

```python
from claude_integration import ClaudeObsidianIntegration

integration = ClaudeObsidianIntegration()

# Analyze a note
analysis = integration.analyze_note('INVESTIGATION_SUMMARY.md')
print(analysis)
```

## What's Next?

### Learn More
- **CONNECTOR_README.md** - Overview and architecture
- **CONNECTOR_GUIDE.md** - Complete API reference
- **CLAUDE_INTEGRATION.md** - AI features guide
- **examples/** - Ready-to-use scripts

### Try Examples
```bash
# Run the full example suite
python3 example_usage.py

# Try Claude integration examples
python3 examples/smart_search.py "your query"
python3 examples/generate_notes.py "your topic"
```

### Build Something

Common project ideas:
1. **Daily note generator** - Automatic daily notes
2. **Tag manager** - Bulk tag operations
3. **Link checker** - Find broken links
4. **Export tool** - Export to other formats
5. **Research assistant** - AI-powered analysis
6. **Knowledge graph** - Visualize connections

### Automate Workflows

Add to your shell aliases:

```bash
# Search vault from anywhere
alias vsearch='python3 /path/to/vault/vault_cli.py search'

# Quick stats
alias vstats='python3 /path/to/vault/vault_cli.py stats'

# AI search
alias vsmart='python3 /path/to/vault/examples/smart_search.py'
```

## Troubleshooting

### "Module not found"
```bash
# Make sure you're in the vault directory
cd /home/user/obsidian-vault

# Or add to path
export PYTHONPATH="/home/user/obsidian-vault:$PYTHONPATH"
```

### "Permission denied"
```bash
# Make scripts executable
chmod +x vault_cli.py example_usage.py
chmod +x examples/*.py
```

### "API key error"
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# Set it
export ANTHROPIC_API_KEY='your-key-here'

# Make permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc
```

## Support

- Read the guides in the main directory
- Check example scripts in `examples/`
- Review code comments in source files
- Test with simple examples first

## Quick Reference

### CLI Commands
```bash
vault_cli.py stats                    # Vault statistics
vault_cli.py list [pattern]           # List notes
vault_cli.py read <path>              # Read note
vault_cli.py search <query>           # Search
vault_cli.py tags <tag>               # Find by tag
vault_cli.py alltags                  # Show all tags
vault_cli.py backlinks <title>        # Find backlinks
```

### Python API
```python
from obsidian_connector import ObsidianConnector

c = ObsidianConnector()
c.list_notes()                        # List all notes
c.read_note(path)                     # Read note
c.write_note(path, content)           # Write note
c.search_notes(query)                 # Search
c.search_by_tag(tag)                  # By tag
c.get_backlinks(title)                # Backlinks
c.get_all_tags()                      # All tags
c.get_vault_stats()                   # Statistics
```

### Claude Integration
```python
from claude_integration import ClaudeObsidianIntegration

i = ClaudeObsidianIntegration()
i.ask_about_note(path, question)      # Ask questions
i.analyze_note(path)                  # Analyze
i.smart_search(query)                 # Smart search
i.generate_note(topic)                # Generate
i.suggest_tags(path)                  # Suggest tags
i.find_connections(path)              # Find connections
```

---

**Ready to go!** Start with `vault_cli.py stats` and explore from there.
