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

log "[SYNC] Starting sync..."

# Pull latest changes first
log "[PULL] Fetching remote changes..."
if ! git fetch origin main; then
    log "[FAIL] Failed to fetch from remote repository. Check your network connection and repository access."
    exit 1
fi

# Check for conflicts
if ! LOCAL=$(git rev-parse @ 2>&1); then
    log "[FAIL] Failed to get local commit hash. Repository may be corrupted: $LOCAL"
    exit 1
fi

if ! REMOTE=$(git rev-parse @{u} 2>&1); then
    log "[FAIL] Failed to get remote tracking branch. Ensure branch is tracking origin/main: $REMOTE"
    exit 1
fi

if ! BASE=$(git merge-base @ @{u} 2>&1); then
    log "[FAIL] Failed to find common ancestor with remote. Repository may have diverged significantly: $BASE"
    exit 1
fi

if [ $LOCAL = $REMOTE ]; then
    log "[INFO] Already up to date with remote"
elif [ $LOCAL = $BASE ]; then
    log "[PULL] Remote has changes, pulling..."
    if ! git pull origin main; then
        log "[FAIL] Failed to pull remote changes. Check for merge conflicts or network issues."
        exit 1
    fi
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
if ! git add -A; then
    log "[FAIL] Failed to stage changes. Check file permissions and repository integrity."
    exit 1
fi

# Check if there are staged changes
if [[ -z $(git diff --cached --name-only) ]]; then
    log "[SYNC] No staged changes after pull"
    exit 0
fi

# Commit with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
log "[COMMIT] Creating commit..."
if ! git commit -m "Auto-sync: $TIMESTAMP

[OK] Vault synced automatically" > /dev/null 2>&1; then
    log "[FAIL] Failed to create commit. Check git configuration (user.name, user.email) and repository state."
    exit 1
fi

# Push to GitHub
log "[PUSH] Pushing to GitHub..."
if git push origin main; then
    log "[OK] Sync complete"
else
    log "[FAIL] Push failed"
    exit 1
fi
