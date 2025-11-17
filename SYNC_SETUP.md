# Obsidian Vault Auto-Sync Setup

Your Obsidian vault is now configured for automatic GitHub synchronization!

## Location
**Local Path:** `<your-vault-directory>`
**GitHub URL:** https://github.com/Tsukieomie/obsidian-vault

## Automatic Sync
- Syncs every 5 minutes automatically
- Runs in the background via macOS LaunchAgent
- Pulls remote changes before pushing
- Handles merge conflicts automatically when possible
- Logs all sync activity

## Sync Status
Check sync logs:
```bash
cat <your-vault-directory>/.sync-log.txt
```

## Manual Sync
Force a sync anytime:
```bash
<your-vault-directory>/.sync-vault.sh
```

## Configure Obsidian

### Step 1: Open Obsidian
Launch the Obsidian app on your system

### Step 2: Open Vault
1. Click "Open folder as vault"
2. Navigate to your cloned vault directory
3. Click "Open"

### Step 3: Start Using
Your vault will now:
- Auto-save to GitHub every 5 minutes
- Pull remote changes automatically
- Keep all your devices in sync (if you set up sync on other devices)

## Manage Sync Service

### Check Status
```bash
launchctl list | grep obsidian
```

### Stop Sync
```bash
launchctl unload ~/Library/LaunchAgents/com.obsidian.vault.sync.plist
```

### Start Sync
```bash
launchctl load ~/Library/LaunchAgents/com.obsidian.vault.sync.plist
```

## What Gets Synced
- All markdown notes (.md files)
- All attachments and media
- Obsidian settings (.obsidian folder)
- Canvas files
- Custom plugins and themes

## Troubleshooting

### View Recent Sync Logs
```bash
tail -20 <your-vault-directory>/.sync-log.txt
```

### View Error Logs
```bash
cat <your-vault-directory>/.sync-stderr.log
```

### Manual Conflict Resolution
If conflicts occur:
```bash
cd <your-vault-directory>
git status
# Resolve conflicts manually, then:
git add -A
git commit -m "Resolved conflicts"
git push origin main
```

## Connected via Claude Unified System
This vault is connected to your Claude Unified System with the GitHub connector. You can:
- Ask Claude to search your notes
- Create new notes programmatically
- Analyze your knowledge base
- Generate reports from your vault data

[OK] Auto-sync active and running
