# MCP Server Setup & Cloud Sync Guide

This document explains the MCP (Model Context Protocol) server configuration and how to sync files with Google Drive and your phone.

## Configured MCP Servers

### 1. **Filesystem Server**
- **Purpose**: Local file operations (read, write, manage files)
- **Access Paths**:
  - `/home/user/obsidian-vault` (vault root)
  - `/home/user/Documents`
  - `/home/user/Downloads`
- **Usage**: Claude Code can directly manipulate project files

### 2. **Git Server**
- **Purpose**: Repository operations and version control
- **Repository**: `/home/user/obsidian-vault`
- **Usage**: Commit, push, fetch, and manage Git operations

### 3. **Fetch Server**
- **Purpose**: Web content retrieval and HTML-to-Markdown conversion
- **Usage**: Fetch documentation and web resources

### 4. **Zapier Server** (Optional - Requires Setup)
- **Purpose**: Connect to 8,000+ apps including Google Drive, Dropbox, OneDrive
- **Usage**: Automated syncing and workflow integration

## Setting Up Google Drive Sync

### Option 1: Obsidian Sync (Recommended for Phone)

Obsidian has built-in mobile sync that works across devices:

1. **Install Obsidian on your phone** (iOS or Android)
2. **Enable Obsidian Sync**:
   - Desktop: Settings → Sync → Sign in
   - Mobile: Settings → Sync → Sign in
3. **Automatic sync** happens in real-time across all devices

**Pros**:
- Simple, built-in solution
- Real-time sync
- Offline support

**Cons**:
- Requires Obsidian subscription (~$96/year)

### Option 2: Google Drive Direct Sync

Store vault directly in Google Drive:

1. **Move vault to Google Drive**:
   ```bash
   mv /home/user/obsidian-vault ~/Google\ Drive/obsidian-vault
   ```

2. **Symlink for easy access**:
   ```bash
   ln -s ~/Google\ Drive/obsidian-vault /home/user/obsidian-vault
   ```

3. **Update Claude Code**:
   ```bash
   # Update settings.json paths to point to symlink
   ```

4. **On phone**:
   - Install Google Drive app
   - Install Obsidian
   - Open vault directly from Google Drive folder

**Pros**:
- Free (Google Drive)
- Cross-platform
- Simple setup

**Cons**:
- Slower sync
- Requires Google Drive app on phone
- Potential sync conflicts

### Option 3: Zapier Automation

Use Zapier to sync with Google Drive automatically:

1. **Get Zapier API Key**:
   - Go to https://zapier.com/app/dashboard
   - Get your API key

2. **Add to `.claude/settings.local.json`**:
   ```json
   {
     "mcpServers": {
       "zapier": {
         "command": "npx",
         "args": ["@modelcontextprotocol/server-zapier"],
         "env": {
           "ZAPIER_API_KEY": "YOUR_KEY_HERE"
         }
       }
     }
   }
   ```

3. **Create Zapier workflow**:
   - Trigger: File changes in obsidian-vault
   - Action: Upload/sync to Google Drive
   - Action: Notify phone

**Pros**:
- Flexible automation
- Can integrate with multiple cloud services
- Customizable workflows

**Cons**:
- Requires Zapier account
- More setup required

## Access Methods

### Desktop (VS Code)
```bash
cd /home/user/obsidian-vault
claude /ide
```
- Install VS Code extension
- Click Spark icon in sidebar
- Full Claude Code integration in editor

### Phone (Obsidian Mobile)

**Using Obsidian Sync** (Recommended):
1. Open Obsidian app
2. Settings → Sync → Sign in
3. Auto-syncs with desktop

**Using Google Drive**:
1. Download Google Drive app
2. Download Obsidian app
3. Navigate to vault folder in Google Drive
4. Tap "Open with" → Obsidian

### Browser (Web Access)
Several options for web-based access:

- **Obsidian Publish** (paid): Publish specific vault as website
- **Google Drive**: Access files directly through Google Drive web
- **Github Pages**: Automatically publish vault docs (if enabled)

## File Syncing Best Practices

### Before Syncing
- Ensure no uncommitted changes: `git status`
- Backup important files
- Close vault in other devices before syncing

### Sync Workflow
```bash
# 1. Commit current work
git add .
git commit -m "Auto-sync: $(date)"

# 2. Sync to remote (your branch)
git push -u origin claude/review-conversations-01RDuVdi9qiwNpmpyfS1nH1r

# 3. Files automatically available across devices
```

### Conflict Resolution
If sync conflicts occur:
1. Keep both versions: Rename one with timestamp
2. Use VS Code's merge tool
3. Manually review and keep desired version

## Current Setup Status

- ✅ `.claude/settings.json` configured with:
  - Filesystem server (local files)
  - Git server (version control)
  - Fetch server (web content)

- ⏳ `.claude/settings.local.json` waiting for:
  - Zapier API key (optional)
  - Google Drive credentials (if using direct sync)

## Next Steps

1. **For Phone Access**:
   - Choose sync method above (Obsidian Sync recommended)
   - Install Obsidian on phone
   - Configure sync settings

2. **For Google Drive Access**:
   - Option A: Use Obsidian Sync (paid, easiest)
   - Option B: Move vault to Google Drive folder (free)
   - Option C: Set up Zapier automation (flexible)

3. **Verify MCP Servers**:
   ```bash
   claude /mcp
   ```

4. **Connect to VS Code**:
   ```bash
   claude /ide
   ```

## Environment Variables

If using sensitive credentials (Google API, Zapier, etc.):
1. Add to `.claude/settings.local.json` (NOT committed)
2. Add `.claude/settings.local.json` to `.gitignore` (already done)
3. Keep credentials safe and never commit

## Troubleshooting

### MCP Servers Not Connecting
```bash
# Verify configuration
claude /mcp

# Check logs
claude /help
```

### Phone Sync Not Working
- Verify WiFi connection
- Restart Obsidian on both devices
- Check Obsidian Sync status
- Ensure vault folder permissions allow syncing

### Google Drive Access Issues
- Verify folder path is correct
- Check Google Drive API credentials
- Ensure symlink is properly created

---

For more details on MCP servers, see the Claude Code documentation:
https://code.claude.com/docs/en/mcp
