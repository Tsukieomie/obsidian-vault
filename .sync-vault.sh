#!/bin/bash

# Obsidian Vault Auto-Sync Script
# Automatically syncs vault changes with GitHub

VAULT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$VAULT_DIR/.sync-log.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$VAULT_DIR" || exit 1

# Check if we have changes
if [[ -z $(git status -s) ]]; then
    log "[SYNC] No changes to sync"
    exit 0
fi

log "[SYNC] Uncommitted changes detected - proceeding with sync..."

# Pull latest changes first
log "[PULL] Fetching remote changes..."
git fetch origin main

# Check for conflicts
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
    log "[INFO] Already up to date with remote"
elif [ $LOCAL = $BASE ]; then
    log "[PULL] Remote has changes, pulling..."
    git pull origin main
elif [ $REMOTE = $BASE ]; then
    log "[INFO] Local has changes, will push"
else
    log "[WARN] Diverged! Attempting merge..."
    git pull origin main
    if [ $? -ne 0 ]; then
        log "[FAIL] Merge conflict! Manual intervention required"
        exit 1
    fi
fi

# Add all changes
log "[ADD] Staging changes..."
git add -A

# Check if there are staged changes
if [[ -z $(git diff --cached --name-only) ]]; then
    log "[SYNC] No staged changes after pull"
    exit 0
fi

# Commit with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
log "[COMMIT] Creating commit..."
git commit -m "Auto-sync: $TIMESTAMP

[OK] Vault synced automatically" > /dev/null 2>&1

# Push to GitHub
log "[PUSH] Pushing to GitHub..."
if git push origin main; then
    log "[OK] Sync complete"
else
    log "[FAIL] Push failed"
    exit 1
fi
