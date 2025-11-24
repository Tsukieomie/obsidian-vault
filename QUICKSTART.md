# Quick Start Guide: Supermemory Sync

This guide will help you quickly set up and run the Supermemory sync script.

## Prerequisites

- Python 3.7 or higher
- A Supermemory account and API key

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
# Navigate to your vault directory
cd /path/to/obsidian-vault

# Install required Python packages
pip install --pre supermemory python-dotenv
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Configure Your API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your favorite editor
nano .env
```

Replace `your_api_key_here` with your actual Supermemory API key:
```
SUPERMEMORY_API_KEY=sm_1234567890abcdef
```

**Get your API key**: Visit [Supermemory](https://supermemory.ai/) and sign up or log in.

### Step 3: Run Your First Sync

```bash
# Dry run first (doesn't upload, just shows what would be synced)
python3 supermemory_bulk_sync.py --dry-run

# If everything looks good, run the actual sync
python3 supermemory_bulk_sync.py
```

## What Happens During Sync?

1. **Discovery**: The script finds all `.md` files in your vault
2. **Filtering**: Excludes hidden files and system folders (`.git`, `.obsidian`)
3. **Upload**: Sends new or modified files to Supermemory
4. **Tracking**: Saves sync state to `.supermemory-sync.json`

## Subsequent Syncs

After the first sync, the script only uploads changed or new files:

```bash
python3 supermemory_bulk_sync.py
```

This is much faster since it skips unchanged files.

## Common Commands

```bash
# Normal sync (incremental)
python3 supermemory_bulk_sync.py

# Force re-sync everything
python3 supermemory_bulk_sync.py --force

# Preview what would be synced
python3 supermemory_bulk_sync.py --dry-run

# Sync a specific vault path
python3 supermemory_bulk_sync.py --vault-path /other/vault

# Show help
python3 supermemory_bulk_sync.py --help
```

## Automate It

### Option 1: Run After Git Commits

Create `.git/hooks/post-commit`:
```bash
#!/bin/bash
cd /path/to/vault
python3 supermemory_bulk_sync.py > /dev/null 2>&1 &
```

Make it executable:
```bash
chmod +x .git/hooks/post-commit
```

### Option 2: Cron Job (Every Hour)

```bash
crontab -e
```

Add:
```
0 * * * * cd /path/to/vault && python3 supermemory_bulk_sync.py >> .supermemory-sync.log 2>&1
```

### Option 3: Manual When Needed

Just run the command whenever you want to sync:
```bash
python3 supermemory_bulk_sync.py
```

## Troubleshooting

### "ERROR: SUPERMEMORY_API_KEY environment variable not set"

**Fix**: Make sure you created the `.env` file with your API key.

### "ERROR: supermemory package not installed"

**Fix**: Install it with:
```bash
pip install --pre supermemory
```

### "Connection failed"

**Fix**: 
- Check your internet connection
- Verify your API key is correct in `.env`
- Ensure Supermemory service is accessible

### Script runs but no files upload

Check the output - you might have already synced everything. Try:
```bash
python3 supermemory_bulk_sync.py --force
```

## Understanding the Output

```
[2025-11-24 03:49:00] INFO: ✓ Connected to Supermemory API
[2025-11-24 03:49:00] INFO: Found 46 markdown files
[2025-11-24 03:49:00] INFO: Files to sync: 46
[2025-11-24 03:49:01] INFO: ✓ Uploaded successfully: Investigation Dashboard.md
...
[2025-11-24 03:49:30] INFO: ============================================================
[2025-11-24 03:49:30] INFO: SYNC COMPLETE
[2025-11-24 03:49:30] INFO: Total files in vault: 46
[2025-11-24 03:49:30] INFO: Uploaded: 46
[2025-11-24 03:49:30] INFO: Skipped (unchanged): 0
[2025-11-24 03:49:30] INFO: Errors: 0
[2025-11-24 03:49:30] INFO: ============================================================
```

- **Total files**: All markdown files found
- **Uploaded**: New or modified files sent to Supermemory
- **Skipped**: Unchanged files (not re-uploaded)
- **Errors**: Failed uploads

## Next Steps

Once synced, you can query your notes using the Supermemory API or web interface!

For more details, see [SUPERMEMORY_README.md](SUPERMEMORY_README.md).

---

**Ready to sync?** Just run: `python3 supermemory_bulk_sync.py`
