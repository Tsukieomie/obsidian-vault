#!/bin/bash

# Obsidian Vault Auto-Sync Script
# Automatically syncs vault changes with GitHub

VAULT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$VAULT_DIR/.sync-log.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Retry function for network operations
# Usage: retry_network_command "command description" command args...
retry_network_command() {
    local description="$1"
    shift
    local max_attempts=4
    local attempt=1
    local delay=1

    while [ $attempt -le $max_attempts ]; do
        if [ $attempt -gt 1 ]; then
            log "[RETRY] Attempt $attempt/$max_attempts for $description after ${delay}s delay..."
            sleep $delay
            delay=$((delay * 2))
        fi

        if "$@"; then
            return 0
        fi

        attempt=$((attempt + 1))
    done

    return 1
}

cd "$VAULT_DIR" || exit 1

# Prerequisite validation
if ! command -v git &> /dev/null; then
    echo "[FAIL] Git is not installed. Please install git and try again."
    exit 1
fi

if ! git rev-parse --git-dir &> /dev/null; then
    echo "[FAIL] Not a git repository. Please initialize git in this directory."
    exit 1
fi

if ! git config user.name &> /dev/null; then
    echo "[FAIL] Git user.name not configured. Run: git config user.name \"Your Name\""
    exit 1
fi

if ! git config user.email &> /dev/null; then
    echo "[FAIL] Git user.email not configured. Run: git config user.email \"your@email.com\""
    exit 1
fi

# Validate log file can be written
if ! touch "$LOG_FILE" 2>/dev/null; then
    echo "[FAIL] Cannot write to log file: $LOG_FILE. Check directory permissions."
    exit 1
fi

# Check if we have changes
if [[ -z $(git status -s) ]]; then
    log "[SYNC] No changes to sync"
    exit 0
fi

log "[SYNC] Starting sync..."

# Pull latest changes first
log "[PULL] Fetching remote changes..."
if ! retry_network_command "git fetch" git fetch origin main; then
    log "[FAIL] Failed to fetch from remote repository after 4 attempts. Check your network connection and repository access."
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
    if ! git pull origin main; then
        log "[FAIL] Merge conflict! Manual intervention required. Resolve conflicts and commit manually."
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
if retry_network_command "git push" git push origin main; then
    log "[OK] Sync complete"
else
    log "[FAIL] Push failed after 4 attempts. Check network connection, repository permissions, and authentication (SSH keys/tokens)."
    exit 1
fi
