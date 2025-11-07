#!/bin/bash

# Obsidian Vault Auto-Sync Script (Enhanced with GitHub Connector)
# Automatically syncs vault changes with GitHub using intelligent commit messages

VAULT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$VAULT_DIR/.sync-log.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$VAULT_DIR" || exit 1

# Use the new GitHub Connector for intelligent syncing
log "[SYNC] Starting GitHub Connector sync..."

# Run the connector with output to log
python3 "$VAULT_DIR/github-connector.py" sync 2>&1 | while IFS= read -r line; do
    log "$line"
done

# Check exit status
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    log "[OK] Sync complete (powered by GitHub Connector)"
    exit 0
else
    log "[FAIL] Sync failed"
    exit 1
fi
