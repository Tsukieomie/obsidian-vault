# Supermemory Integration for Obsidian Vault

This repository includes a Python script to sync your Obsidian vault with Supermemory, enabling AI-powered search and querying of your notes.

## What is Supermemory?

Supermemory is an AI-powered memory API that allows you to store, search, and query information using natural language. By syncing your Obsidian vault with Supermemory, you can:

- Search your notes using natural language queries
- Get AI-powered answers from your knowledge base
- Access your notes through the Supermemory API
- Build custom applications on top of your Obsidian vault

## Setup

### 1. Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Note: Supermemory may require the --pre flag if in pre-release
pip install --pre supermemory
```

### 2. Get Your Supermemory API Key

1. Visit [Supermemory](https://supermemory.ai/)
2. Sign up or log in to your account
3. Navigate to your API settings
4. Copy your API key

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use your preferred editor
```

Edit the `.env` file:
```
SUPERMEMORY_API_KEY=your_actual_api_key_here
```

**Important**: Never commit your `.env` file to version control. It's already excluded in `.gitignore`.

## Usage

### Basic Sync

Sync all markdown files in the current vault:

```bash
python3 supermemory_bulk_sync.py
```

### Sync Specific Vault

If you're not in the vault directory:

```bash
python3 supermemory_bulk_sync.py --vault-path /path/to/your/vault
```

### Force Full Re-sync

Re-upload all files, ignoring the sync cache:

```bash
python3 supermemory_bulk_sync.py --force
```

### Dry Run

See what would be synced without actually uploading:

```bash
python3 supermemory_bulk_sync.py --dry-run
```

### Command Line Options

```
Options:
  --vault-path PATH    Path to Obsidian vault (default: current directory)
  --sync-log FILE      Sync state file (default: .supermemory-sync.json)
  --force              Force sync all files, ignoring cache
  --dry-run            Show what would be synced without uploading
  -h, --help           Show help message
```

## How It Works

### Sync Process

1. **Discovery**: Scans your vault for all markdown files (`.md`)
2. **Filtering**: Excludes hidden files and system directories (`.git`, `.obsidian`, etc.)
3. **Change Detection**: Compares file hashes to detect changes since last sync
4. **Upload**: Uploads new or modified files to Supermemory
5. **State Tracking**: Saves sync state to `.supermemory-sync.json`

### What Gets Synced

- ✅ All markdown files (`.md`)
- ✅ File metadata (path, name, sync date)
- ✅ Full file content

### What Gets Excluded

- ❌ Hidden files (starting with `.`)
- ❌ System directories (`.git`, `.obsidian`, `.trash`)
- ❌ Empty files
- ❌ Non-markdown files

### Sync State

The script maintains a `.supermemory-sync.json` file that tracks:
- Which files have been synced
- File hashes to detect changes
- Sync statistics and timestamps

This allows incremental syncs - only new or modified files are uploaded on subsequent runs.

## Examples

### First-Time Sync

```bash
$ python3 supermemory_bulk_sync.py
[2025-11-24 03:49:00] INFO: Vault path: /home/user/obsidian-vault
[2025-11-24 03:49:00] INFO: ✓ Connected to Supermemory API
[2025-11-24 03:49:00] INFO: Starting sync of vault: /home/user/obsidian-vault
[2025-11-24 03:49:01] INFO: Found 46 markdown files
[2025-11-24 03:49:01] INFO: Files to sync: 46
[2025-11-24 03:49:01] INFO: Progress: 1/46
[2025-11-24 03:49:02] INFO: ✓ Uploaded successfully: Investigation Dashboard.md
...
[2025-11-24 03:49:30] INFO: ============================================================
[2025-11-24 03:49:30] INFO: SYNC COMPLETE
[2025-11-24 03:49:30] INFO: ============================================================
[2025-11-24 03:49:30] INFO: Total files in vault: 46
[2025-11-24 03:49:30] INFO: Uploaded: 46
[2025-11-24 03:49:30] INFO: Skipped (unchanged): 0
[2025-11-24 03:49:30] INFO: Errors: 0
[2025-11-24 03:49:30] INFO: Total synced lifetime: 46
[2025-11-24 03:49:30] INFO: ============================================================
```

### Incremental Sync

```bash
$ python3 supermemory_bulk_sync.py
[2025-11-24 04:00:00] INFO: Vault path: /home/user/obsidian-vault
[2025-11-24 04:00:00] INFO: ✓ Connected to Supermemory API
[2025-11-24 04:00:00] INFO: Starting sync of vault: /home/user/obsidian-vault
[2025-11-24 04:00:01] INFO: Found 46 markdown files
[2025-11-24 04:00:01] INFO: Files to sync: 2
[2025-11-24 04:00:01] INFO: Progress: 1/2
[2025-11-24 04:00:02] INFO: ✓ Uploaded successfully: Investigation Dashboard.md
[2025-11-24 04:00:02] INFO: Progress: 2/2
[2025-11-24 04:00:03] INFO: ✓ Uploaded successfully: Timeline.md
[2025-11-24 04:00:03] INFO: ============================================================
[2025-11-24 04:00:03] INFO: SYNC COMPLETE
[2025-11-24 04:00:03] INFO: ============================================================
[2025-11-24 04:00:03] INFO: Total files in vault: 46
[2025-11-24 04:00:03] INFO: Uploaded: 2
[2025-11-24 04:00:03] INFO: Skipped (unchanged): 44
[2025-11-24 04:00:03] INFO: Errors: 0
[2025-11-24 04:00:03] INFO: Total synced lifetime: 46
[2025-11-24 04:00:03] INFO: ============================================================
```

## Automation

### Cron Job (Linux/Mac)

Add to your crontab to sync every hour:

```bash
crontab -e
```

Add this line:
```
0 * * * * cd /path/to/vault && /path/to/venv/bin/python3 supermemory_bulk_sync.py >> .supermemory-sync.log 2>&1
```

### Scheduled Task (Windows)

Use Windows Task Scheduler to run the script periodically.

### Integration with Git Hooks

Add to `.git/hooks/post-commit`:

```bash
#!/bin/bash
python3 supermemory_bulk_sync.py
```

## Troubleshooting

### API Key Not Found

```
ERROR: SUPERMEMORY_API_KEY environment variable not set
```

**Solution**: Ensure you've created a `.env` file with your API key, or set the environment variable:
```bash
export SUPERMEMORY_API_KEY='your-api-key-here'
```

### Connection Failed

```
✗ Failed to connect to Supermemory
```

**Solution**: 
- Check your internet connection
- Verify your API key is correct
- Ensure Supermemory service is available

### Import Error

```
ERROR: supermemory package not installed
```

**Solution**: Install the package:
```bash
pip install --pre supermemory
```

### Permission Denied

Ensure the script is executable:
```bash
chmod +x supermemory_bulk_sync.py
```

## Advanced Usage

### Custom Sync Log Location

```bash
python3 supermemory_bulk_sync.py --sync-log /custom/path/sync-state.json
```

### Environment Variables

You can set these in your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
export SUPERMEMORY_API_KEY='your-api-key'
export OBSIDIAN_VAULT_PATH='/path/to/vault'
```

## Security Notes

- **Never commit your `.env` file** - it contains your API key
- The `.supermemory-sync.json` file can be committed (contains no secrets)
- Your API key grants access to your Supermemory account - keep it secure
- Use environment variables or `.env` files, not hardcoded keys

## Querying Your Synced Notes

Once synced, you can query your notes using the Supermemory API or SDK:

```python
from supermemory import Supermemory
import os

client = Supermemory(api_key=os.getenv("SUPERMEMORY_API_KEY"))

# Search your notes
results = client.search.execute(q="network infrastructure analysis")

for result in results.results:
    print(f"Found: {result.content}")
```

## Contributing

If you find issues or have improvements:
1. Test your changes thoroughly
2. Update documentation as needed
3. Submit a pull request with a clear description

## Resources

- [Supermemory Documentation](https://supermemory.mintlify.dev/)
- [Supermemory Python SDK](https://supermemory.mintlify.dev/docs/memory-api/sdks/python)
- [Obsidian Documentation](https://help.obsidian.md/)

## License

This script is provided as-is for use with your Obsidian vault and Supermemory account.

---

**Need Help?** Check the [troubleshooting section](#troubleshooting) or open an issue in the repository.
