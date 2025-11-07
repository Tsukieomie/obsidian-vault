# Google Drive Integration for Obsidian Vault

Access your Obsidian investigation vault from any Claude session via Google Drive.

## Overview

This integration allows you to:
1. **Store** your vault manifest on Google Drive
2. **Access** the vault from any Claude session
3. **Sync** and work with your investigation from anywhere
4. **Maintain** a single source of truth for your vault connection

## How It Works

```
┌─────────────────┐
│  Google Drive   │  ← Upload manifest file
│                 │
│  obsidian-vault │
│  -manifest.json │
└────────┬────────┘
         │
         │ Search & Download
         ↓
┌─────────────────┐
│  Claude Session │  ← "Search Google Drive for manifest"
│                 │
│  Execute:       │
│  connect script │
└────────┬────────┘
         │
         │ Clone/Sync
         ↓
┌─────────────────┐
│  Local Vault    │  ← Work with GitHub Connector
│                 │
│  Full access to │
│  investigation  │
└─────────────────┘
```

## Setup

### Step 1: Upload Manifest to Google Drive

1. **Locate the manifest file** in your vault:
   ```
   obsidian-vault-manifest.json
   ```

2. **Upload to Google Drive**:
   - Open Google Drive (drive.google.com)
   - Upload `obsidian-vault-manifest.json` to your root folder or any location
   - Ensure Google Drive desktop app is synced (recommended)

3. **Verify upload**:
   - Check that file appears in Google Drive web interface
   - If using desktop app, verify it's synced locally

### Step 2: Install Google Drive Desktop (Recommended)

For easiest access:

**macOS:**
```bash
brew install --cask google-drive
```

**Windows:**
Download from: https://www.google.com/drive/download/

**Linux:**
Use rclone or similar tools

### Step 3: Test Connection

```bash
# Search for manifest
./google-drive-connector.py search

# Should output:
# ✅ Found manifest: /path/to/Google Drive/obsidian-vault-manifest.json
```

## Usage

### Quick Start Workflow

**From a new Claude session:**

1. **Ask Claude to search Google Drive:**
   ```
   "Search my Google Drive for obsidian-vault-manifest.json"
   ```

2. **Claude will find and read the manifest**

3. **Connect to vault:**
   ```bash
   ./google-drive-connector.py connect
   ```

4. **Navigate to vault:**
   ```bash
   cd obsidian-vault
   ```

5. **Use GitHub Connector:**
   ```bash
   ./github-connector.py report
   ./github-connector.py sync
   ```

### Commands

#### `search` - Find Manifest

Searches common Google Drive locations for the manifest file.

```bash
./google-drive-connector.py search
```

**Output:**
```
🔍 Searching for vault manifest in Google Drive...
✅ Found manifest: /Users/you/Google Drive/obsidian-vault-manifest.json
```

#### `connect` - Connect to Vault

Connects to the vault by cloning the repository.

```bash
# Auto-search for manifest
./google-drive-connector.py connect

# Specify manifest location
./google-drive-connector.py connect --manifest /path/to/manifest.json

# Specify target directory
./google-drive-connector.py connect --target ~/my-vaults/
```

**What it does:**
1. Finds or uses provided manifest
2. Reads repository information
3. Clones the vault repository
4. Saves connection for future use

**Output:**
```
🚀 Connecting to Obsidian vault via Google Drive...

🔍 Searching for vault manifest in Google Drive...
✅ Found manifest: /Users/you/Google Drive/obsidian-vault-manifest.json
📖 Reading manifest: /Users/you/Google Drive/obsidian-vault-manifest.json
✅ Loaded manifest for: Obsidian Investigation Vault
📦 Cloning vault from: https://github.com/Tsukieomie/obsidian-vault.git
   Target: /current/path/obsidian-vault
✅ Vault cloned successfully!

✅ Connected successfully!

📂 Vault location: /current/path/obsidian-vault

💡 Next steps:
   cd /current/path/obsidian-vault
   ./github-connector.py report
```

#### `sync` - Sync Connected Vault

Syncs the vault using the GitHub Connector.

```bash
./google-drive-connector.py sync
```

**Requirements:** Must run `connect` first.

#### `status` - Show Connection Status

Displays connection status and vault information.

```bash
./google-drive-connector.py status
```

**Output:**
```
============================================================
📊 Google Drive Connector Status
============================================================

✅ Connected
   Manifest: /Users/you/Google Drive/obsidian-vault-manifest.json
   Vault: /path/to/obsidian-vault
   Connected: 2025-11-07T14:30:00

📂 Vault Status:
   Path: /path/to/obsidian-vault
   Exists: ✅
   GitHub Connector: ✅

Changes: 0

🔍 Google Drive Access:
   Manifest found: ✅
   Location: /Users/you/Google Drive/obsidian-vault-manifest.json

============================================================
```

#### `open` - Open Vault Directory

Changes to the vault directory and shows status.

```bash
./google-drive-connector.py open
```

## Workflows

### Workflow 1: First Time Setup

```bash
# 1. Upload manifest to Google Drive
# (done via web interface)

# 2. Search for manifest
./google-drive-connector.py search

# 3. Connect to vault
./google-drive-connector.py connect

# 4. Navigate to vault
cd obsidian-vault

# 5. Start working
./github-connector.py report
```

### Workflow 2: Daily Use with Claude

```
You: "Search my Google Drive for the obsidian vault manifest"

Claude: *searches and finds manifest*
        "I found your vault manifest. Let me connect to it."
        *runs google-drive-connector.py connect*

You: "Show me the current investigation status"

Claude: *runs github-connector.py report*
        *displays entities, todos, recent commits*

You: "Update the Duke University entity profile"

Claude: *makes changes*
        *runs github-connector.py sync*
        "Updated entity profile and committed with message:
        'Update entity profile: Duke University'"
```

### Workflow 3: Working from Multiple Machines

**Machine A:**
```bash
# Make changes
vim Entities/Organizations/Duke_University.md

# Sync with intelligent commit
./github-connector.py sync
```

**Machine B (later):**
```bash
# Connect via Google Drive
./google-drive-connector.py connect

# Sync latest changes
./google-drive-connector.py sync

# Continue working
./github-connector.py report
```

### Workflow 4: Claude-Initiated Investigation

```
You: "Connect to my investigation vault and review recent findings"

Claude:
1. Searches Google Drive for manifest
2. Runs: ./google-drive-connector.py connect
3. Runs: ./github-connector.py report
4. Analyzes recent commits and entity changes
5. Provides investigation summary

You: "Add a new technical analysis document"

Claude:
1. Creates document in Technical/ folder
2. Runs: ./github-connector.py sync
3. Commits with message: "Update technical analysis (1 file)"
```

## Manifest File Structure

The `obsidian-vault-manifest.json` contains:

```json
{
  "vault_name": "Obsidian Investigation Vault",
  "vault_id": "unique-identifier",

  "repository": {
    "platform": "github",
    "owner": "username",
    "name": "repo-name",
    "url": "https://github.com/username/repo-name",
    "git_url": "https://github.com/username/repo-name.git"
  },

  "tools": {
    "github_connector": {
      "installed": true,
      "commands": ["sync", "report", "status", ...]
    }
  },

  "metadata": {
    "total_files": 46,
    "active_todos": 100,
    "tracked_entities": 12
  }
}
```

### Customizing the Manifest

You can edit the manifest to:
- Update repository information
- Change default branch
- Add custom metadata
- Include investigation notes

**After editing:**
1. Save changes
2. Upload to Google Drive (replaces old version)
3. Reconnect: `./google-drive-connector.py connect`

## Integration with Claude

### Recommended Claude Prompts

**To access vault:**
```
"Search my Google Drive for obsidian-vault-manifest.json and connect to my investigation vault"
```

**To sync and work:**
```
"Connect to my obsidian vault via Google Drive and show me the current status"
```

**To make changes:**
```
"Access my investigation vault and update the entity profile for [Entity Name]"
```

### Claude Will Automatically:

1. **Search Google Drive** using WebFetch or file system access
2. **Read the manifest** to understand vault structure
3. **Execute commands** to clone/sync the vault
4. **Use GitHub Connector** for intelligent operations
5. **Report results** with context-aware summaries

## Troubleshooting

### Manifest Not Found

**Problem:** `❌ Manifest not found in common Google Drive locations`

**Solutions:**

1. **Check Google Drive sync status**:
   - Ensure Google Drive desktop app is running
   - Verify file is synced (has checkmark icon)

2. **Specify manifest location manually**:
   ```bash
   ./google-drive-connector.py connect --manifest /path/to/manifest.json
   ```

3. **Search manually**:
   ```bash
   find ~ -name "obsidian-vault-manifest.json" 2>/dev/null
   ```

4. **Check common locations**:
   - `~/Google Drive/`
   - `~/GoogleDrive/`
   - `~/Library/CloudStorage/GoogleDrive-*/`

### Google Drive Not Installed

**Problem:** No Google Drive desktop app

**Solutions:**

1. **Install Google Drive**:
   - macOS: `brew install --cask google-drive`
   - Windows: Download from Google
   - Linux: Use rclone

2. **Alternative: Manual download**:
   - Download manifest from Google Drive web interface
   - Place in current directory
   - Run: `./google-drive-connector.py connect --manifest ./obsidian-vault-manifest.json`

### Vault Already Exists

**Problem:** `⚠️  Directory already exists: obsidian-vault`

**Solution:**

```bash
# Navigate to existing vault
cd obsidian-vault

# Sync instead
./github-connector.py sync
```

Or specify different target:
```bash
./google-drive-connector.py connect --target ~/vaults/new-location/
```

### Permission Denied

**Problem:** Cannot clone repository

**Solutions:**

1. **Check GitHub authentication**:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"
   ```

2. **Use SSH instead of HTTPS** (edit manifest):
   ```json
   "git_url": "git@github.com:username/repo-name.git"
   ```

3. **Check repository access**: Ensure you have read access to the repository

### Claude Can't Access Google Drive

**Problem:** Claude session doesn't have Google Drive access

**Solutions:**

1. **Download manifest manually**:
   - Go to Google Drive web interface
   - Download `obsidian-vault-manifest.json`
   - Upload to Claude chat (drag & drop)
   - Save it: `cat > obsidian-vault-manifest.json`
   - Connect: `./google-drive-connector.py connect`

2. **Share file link**:
   - Right-click manifest in Google Drive
   - Get shareable link
   - Ask Claude to fetch via link

## Advanced Usage

### Multiple Vaults

Manage multiple investigation vaults:

```bash
# Create separate manifests
obsidian-vault-manifest.json
project-alpha-manifest.json
research-beta-manifest.json

# Connect to specific vault
./google-drive-connector.py connect --manifest project-alpha-manifest.json --target ~/project-alpha/
```

### Custom Sync Scripts

Create automated sync workflow:

```bash
#!/bin/bash
# daily-sync.sh

# Connect to vault via Google Drive
./google-drive-connector.py connect

# Sync changes
cd obsidian-vault
./github-connector.py sync

# Generate report
./github-connector.py report
```

Run daily via cron:
```bash
0 9 * * * /path/to/daily-sync.sh
```

### Team Collaboration

Share vault with team:

1. **Create team manifest** with shared repository access
2. **Upload to shared Google Drive** folder
3. **Team members connect**:
   ```bash
   ./google-drive-connector.py connect --manifest /path/to/shared/manifest.json
   ```
4. **Everyone syncs** using the same GitHub Connector

## Configuration

Connection settings stored in:
```
~/.config/obsidian-vault-connector/connection.json
```

**Contents:**
```json
{
  "manifest_path": "/path/to/manifest.json",
  "vault_path": "/path/to/vault",
  "connected_at": "2025-11-07T14:30:00"
}
```

### Resetting Connection

```bash
# Remove saved connection
rm ~/.config/obsidian-vault-connector/connection.json

# Reconnect
./google-drive-connector.py connect
```

## Security Considerations

### Manifest File Security

The manifest contains:
- ✅ Repository URLs (public information)
- ✅ Vault structure (safe to share)
- ❌ No credentials or tokens
- ❌ No sensitive data

**Safe to store on Google Drive**

### Credentials

Git credentials managed separately:
- Use SSH keys for authentication
- Or GitHub personal access tokens
- Never store credentials in manifest

### Private Repositories

For private repositories:
1. Set up SSH keys: `ssh-keygen -t ed25519`
2. Add to GitHub: Settings → SSH Keys
3. Use SSH URL in manifest: `git@github.com:user/repo.git`

## Tips & Best Practices

### 1. Keep Manifest Updated

After major vault changes:
```bash
# Update manifest
vim obsidian-vault-manifest.json

# Upload to Google Drive
# (or use Drive desktop sync)
```

### 2. Use Descriptive Vault IDs

```json
"vault_id": "investigation-2024-darpa-brain"
```

### 3. Add Investigation Notes to Manifest

```json
"metadata": {
  "investigation_focus": [
    "Current objective",
    "Key entities",
    "Next steps"
  ]
}
```

### 4. Regular Syncs

```bash
# Daily workflow
./google-drive-connector.py sync
./github-connector.py report
```

### 5. Backup Manifest

Keep local backup:
```bash
cp obsidian-vault-manifest.json ~/backups/
```

## Integration Examples

### Example 1: Morning Investigation Routine

```bash
# Claude prompt:
"Good morning! Connect to my investigation vault via Google Drive
and give me a status update on recent changes and pending TODOs"

# Claude executes:
./google-drive-connector.py connect
./github-connector.py report
./github-connector.py todos

# Claude responds with:
- Recent commits summary
- Entity changes
- TODO list
- Suggested next steps
```

### Example 2: Quick Entity Update

```bash
# You to Claude:
"Update Duke University entity profile with new DARPA connection information"

# Claude:
1. Connects to vault
2. Opens entity file
3. Adds information
4. Syncs with intelligent commit message
5. Confirms update
```

### Example 3: Investigation Report

```bash
# You to Claude:
"Generate an investigation progress report from my vault"

# Claude:
1. Connects via Google Drive
2. Analyzes all entity files
3. Reviews analysis documents
4. Checks TODO progress
5. Generates comprehensive report
6. Saves as new document
7. Syncs changes
```

## Files

- `google-drive-connector.py` - Main connector script
- `obsidian-vault-manifest.json` - Vault manifest file
- `GOOGLE_DRIVE_INTEGRATION.md` - This documentation
- `github-connector.py` - Git operations (used by connector)

## Related Documentation

- [GitHub Connector Documentation](GITHUB_CONNECTOR.md)
- [Investigation Dashboard](Investigation%20Dashboard.md)
- [Entity Network Map](ENTITY_NETWORK_MAP.md)

## Support

For issues:
- **Google Drive Connector**: Check this documentation
- **GitHub Connector**: See `GITHUB_CONNECTOR.md`
- **Claude Code**: Visit https://github.com/anthropics/claude-code/issues

---

**Version:** 1.0.0
**Created:** 2025-11-07
**Integration:** Google Drive + GitHub + Claude
