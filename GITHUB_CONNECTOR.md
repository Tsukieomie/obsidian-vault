# GitHub Connector for Claude

A smart GitHub integration tool for your Obsidian investigation vault that provides intelligent commit message generation, entity tracking, and automated workflow management.

## Features

### 🎯 Core Capabilities

1. **Intelligent Commit Analysis**
   - Automatically analyzes file changes
   - Generates context-aware commit messages
   - Recognizes entity updates, technical analysis, and documentation changes
   - Example: "Update entity profile: Duke University | Update analysis: DARPA BRAIN Timeline"

2. **Entity Change Tracking**
   - Monitors changes to Organizations and People profiles
   - Creates structured commits with entity context
   - Lists modified entities in sync reports

3. **TODO Management**
   - Scans markdown files for TODO items
   - Lists all pending tasks
   - Prepares issues for GitHub integration

4. **Activity Reporting**
   - Shows working directory status
   - Displays recent commit history
   - Lists entity changes and TODO items

5. **Smart Sync Operations**
   - Pull before push to avoid conflicts
   - Auto-stage changes
   - Customizable push behavior

## Installation

The connector is already installed in your vault. No additional setup required!

### Dependencies

The connector requires Python 3.7+ (you have Python 3.11) and uses only standard library modules:
- `os`, `sys`, `subprocess`
- `re`, `yaml`, `pathlib`
- `datetime`, `argparse`

**Optional:** Install PyYAML for better config handling:
```bash
pip install pyyaml
```

**Optional:** Install GitHub CLI for issue creation:
```bash
# macOS
brew install gh

# Linux
# See: https://cli.github.com/
```

## Usage

### Quick Start

```bash
# Show current status
./github-connector.py status

# Generate activity report
./github-connector.py report

# Smart sync with auto-generated message
./github-connector.py sync

# Sync with custom message
./github-connector.py sync -m "Updated DARPA investigation findings"

# Commit without pushing
./github-connector.py sync --no-push
```

### Commands

#### `sync` - Smart Synchronization

Performs intelligent git operations with context-aware commit messages.

```bash
# Auto-generate commit message based on changes
./github-connector.py sync

# Custom commit message
./github-connector.py sync -m "Add new technical analysis documents"

# Commit locally without pushing
./github-connector.py sync --no-push
```

**What it does:**
1. Analyzes all changed files
2. Pulls latest changes (if configured)
3. Generates intelligent commit message
4. Lists modified entities
5. Stages and commits changes
6. Pushes to remote branch

**Example output:**
```
🔄 Starting GitHub sync...
📊 Found 3 changes:
   Modified: 2
   Added: 1
⬇️  Pulling latest changes...
💬 Generated message: Update entity profile: Duke University
👥 Entity changes:
   - Organization: Duke University
➕ Staging changes...
💾 Creating commit...
⬆️  Pushing to remote...
✅ Successfully pushed to claude/github-connector-011CUtdC2RTxFRm9vEYuH5rg
```

#### `report` - Activity Report

Shows comprehensive status of your vault and recent activity.

```bash
./github-connector.py report
```

**Output includes:**
- Current branch name
- Working directory status (modified, added, deleted files)
- Recent commit history (last 5 commits)
- Modified entities
- TODO items found in tracked files

**Example output:**
```
============================================================
📊 GitHub Connector Report
============================================================

🌿 Current Branch: claude/github-connector-011CUtdC2RTxFRm9vEYuH5rg

📝 Working Directory Status:
   Total changes: 0

📜 Recent Commits (last 5):
   82776a6 - Merge pull request #1 (2 days ago)
   984f2d6 - Deep dive analysis: Z-Files (2 days ago)
   d5b66d4 - Add comprehensive cross-reference index (2 days ago)

✅ TODO Items Found (3):
   - Complete DARPA timeline verification
     (Analysis/Next Steps.md:15)
   - Document additional patent connections
     (Investigation Dashboard.md:42)

============================================================
```

#### `status` - Git Status

Shows current git status in a clean format.

```bash
./github-connector.py status
```

#### `todos` - List TODO Items

Scans configured files for TODO items (checkboxes).

```bash
./github-connector.py todos
```

Looks for patterns like:
- `- [ ] Task to do`
- `- [] Another task`

#### `entities` - List All Entities

Shows all tracked entities (Organizations and People).

```bash
./github-connector.py entities
```

**Example output:**
```
👥 Tracked Entities

Organizations (4):
  - Asymptote
  - Duke University
  - SalmonCloud Ltd
  - The Ghoststack Network

People (9):
  - Carlos Montt
  - David Carlson
  - Frank Frank
  - Junyuan Wang
  ...
```

#### `create-issue` - Create GitHub Issue

Creates a GitHub issue using the GitHub CLI (requires `gh` to be installed).

```bash
# Simple issue
./github-connector.py create-issue "Investigate new DARPA connection"

# Issue with description
./github-connector.py create-issue "Research patent" "Need to analyze patent #123456"
```

**Note:** If `gh` CLI is not installed, the command will display issue details instead of creating it.

## Configuration

Configuration is managed in `github-connector.yml`:

```yaml
# Repository Settings
repository:
  remote: "origin"
  branch_prefix: "claude/"

# Commit Message Generation
commit_analysis:
  enabled: true
  tracked_directories:
    - "Entities/"
    - "Analysis/"
    - "Technical/"
    - "Patents/"

# Issue Tracking
issue_tracking:
  enabled: true
  auto_create_issues: false  # Set to true for automatic issue creation
  labels:
    - "investigation"
    - "documentation"
  todo_sources:
    - "Analysis/Next Steps.md"
    - "Investigation Dashboard.md"

# Entity Change Tracking
entity_tracking:
  enabled: true
  entity_directories:
    - "Entities/Organizations/"
    - "Entities/People/"
  include_diff: true

# Sync Behavior
sync:
  pull_before_push: true
  backup_on_major_changes: true
  auto_push_threshold: 10

# Reporting
reporting:
  enabled: true
  include_stats: true
  include_recent_commits: 5
```

### Customization

Edit `github-connector.yml` to customize:
- Which directories trigger specific commit messages
- TODO source files to scan
- Labels for GitHub issues
- Sync behavior (auto-pull, push threshold)
- Report contents

## Integration with Existing Workflow

### Replace Auto-Sync Script

You can replace your existing `.sync-vault.sh` script with the GitHub connector:

**Option 1: Update .sync-vault.sh**
```bash
#!/bin/bash
cd "$(dirname "$0")"
./github-connector.py sync >> .sync-log.txt 2>&1
```

**Option 2: Use directly in cron/LaunchAgent**
```bash
*/5 * * * * cd /path/to/vault && ./github-connector.py sync
```

### Use Alongside Obsidian Sync

The connector complements Obsidian's built-in sync:
- Obsidian Sync: Real-time sync between devices
- GitHub Connector: Version control with intelligent history

## Advanced Usage

### Custom Commit Messages

The connector generates messages based on file patterns:

| Pattern | Generated Message |
|---------|------------------|
| `Entities/*.md` | "Update entity profile: [Name]" |
| `Analysis/*.md` | "Update analysis: [Document]" |
| `Technical/*.md` | "Update technical analysis" |
| Multiple entities | "Update 3 entity profiles" |

### Entity Tracking

When syncing, the connector detects:
- New entity files (Organizations, People)
- Modified entity profiles
- Deleted entities

And includes this context in commit messages and reports.

### TODO Integration

The connector scans these files by default:
- `Analysis/Next Steps.md`
- `Investigation Dashboard.md`
- `LEGAL_CASE_FRAMEWORK.md`

Customize in `github-connector.yml` under `issue_tracking.todo_sources`.

## Troubleshooting

### "Config file not found" warning

Create or edit `github-connector.yml` in your vault root. The connector will use defaults if config is missing.

### Push fails with 403 error

Ensure your branch name starts with `claude/` prefix. The git proxy requires this format:
```bash
git checkout -b claude/my-feature-branch
```

### "gh CLI not available" message

Install GitHub CLI from https://cli.github.com/ to enable issue creation.

### Network errors on push/pull

The connector will automatically retry with exponential backoff (2s, 4s, 8s, 16s) for transient network issues.

## Examples

### Daily Investigation Workflow

```bash
# Morning: Check status and todos
./github-connector.py report
./github-connector.py todos

# Work on investigation...
# (edit entity files, analysis documents)

# Afternoon: Sync changes
./github-connector.py sync

# Evening: Create issue for tomorrow
./github-connector.py create-issue "Follow up on patent connection"
```

### Entity Update Workflow

```bash
# Update entity file
vim Entities/Organizations/Duke_University.md

# Check what changed
./github-connector.py status

# Sync with smart commit message
./github-connector.py sync
# Output: "Update entity profile: Duke University"
```

### Batch Documentation Updates

```bash
# Update multiple analysis files
# ... make changes ...

# Review changes
./github-connector.py report

# Sync with custom message
./github-connector.py sync -m "Comprehensive update: DARPA timeline and Z-File analysis"
```

## Tips

1. **Use `report` frequently** to stay aware of your vault's state
2. **Let the connector generate messages** for routine updates (it's smart!)
3. **Use custom messages** for major milestones or important findings
4. **Check `todos`** to track investigation tasks
5. **List `entities`** to see the full scope of your network map

## Files

- `github-connector.py` - Main connector script
- `github-connector.yml` - Configuration file
- `GITHUB_CONNECTOR.md` - This documentation

## Support

For issues or feature requests related to:
- **The connector itself**: Check the code comments in `github-connector.py`
- **Claude Code**: Visit https://github.com/anthropics/claude-code/issues
- **GitHub operations**: See `git --help` or GitHub documentation

## License

Part of your investigation vault. Use and modify as needed for your research.

---

**Version:** 1.0.0
**Created:** 2025-11-07
**Environment:** Claude Code with GitHub Connector
