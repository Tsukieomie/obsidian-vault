# Pull Request: GitHub Connector for Claude

## Summary

This PR adds a comprehensive GitHub Connector for Claude that provides intelligent git operations, entity tracking, and automated workflow management for the investigation vault.

**Key Changes:**
- ✅ Smart commit message generation based on file analysis
- ✅ Entity tracking and change reporting
- ✅ TODO item scanning and management
- ✅ Enhanced auto-sync workflow
- ✅ Comprehensive CLI tool with 6 commands

## Changes Made

### New Files (997 lines added, 54 lines removed)

1. **`github-connector.py`** (476 lines) - Core connector implementation
   - Intelligent commit message analyzer
   - Entity change detector
   - TODO scanner
   - Activity reporter
   - Full CLI interface

2. **`github-connector.yml`** (71 lines) - Configuration file
   - Customizable commit analysis rules
   - Entity tracking settings
   - Sync behavior controls
   - Issue tracking configuration

3. **`GITHUB_CONNECTOR.md`** (433 lines) - Complete documentation
   - Feature descriptions
   - Usage examples
   - Configuration guide
   - Troubleshooting section

### Modified Files

4. **`.sync-vault.sh`** - Enhanced auto-sync script
   - Simplified from 73 to 31 lines (-54 lines)
   - Now uses GitHub Connector for intelligent syncing
   - Maintains backward compatibility with logging

## Features

### 🎯 Intelligent Commit Messages

**Before:**
```
Auto-sync: 2025-11-07 13:48:36
```

**After:**
```
Update entity profile: Duke University | Update analysis: DARPA BRAIN Timeline
```

The connector analyzes changed files and generates context-aware messages that reflect what was actually modified.

### 👥 Entity Tracking

Automatically detects and reports changes to:
- Organization profiles (4 tracked)
- People profiles (8 tracked)

Example output:
```
👥 Entity changes:
   - Organization: Duke University
   - Person: Junyuan Wang
```

### ✅ TODO Management

Scans investigation files for TODO items:
- Found: **100 TODO items** across investigation documents
- Sources: `Next Steps.md`, `Investigation Dashboard.md`, `LEGAL_CASE_FRAMEWORK.md`
- Can export to GitHub issues (requires gh CLI)

### 📊 Activity Reports

Comprehensive status reports including:
- Current branch and working directory status
- Recent commit history (configurable count)
- Entity modifications
- TODO item list

### 🔄 Smart Sync Operations

Enhanced sync process:
1. Pull latest changes with automatic retry
2. Analyze file changes by type
3. Generate intelligent commit message
4. Stage and commit changes
5. Push to remote with branch tracking

## Commands

```bash
# Show current status
./github-connector.py status

# Generate activity report
./github-connector.py report

# Smart sync with auto-generated message
./github-connector.py sync

# Sync with custom message
./github-connector.py sync -m "Custom message"

# List all entities
./github-connector.py entities

# Show TODO items
./github-connector.py todos

# Create GitHub issue
./github-connector.py create-issue "Title" "Description"
```

## Test Results

All tests passed successfully:

✅ **Status Command** - Correctly identifies untracked files
✅ **Entities Command** - Lists 4 organizations and 8 people
✅ **Report Command** - Generates comprehensive report
✅ **Sync Command** - Successfully commits and pushes changes
✅ **Enhanced Sync Script** - Auto-sync integration works perfectly

Example test output:
```
🔄 Starting GitHub sync...
📊 Found 3 changes:
   Untracked: 3
💬 Generated message: Add GitHub Connector for Claude
➕ Staging changes...
💾 Creating commit...
⬆️  Pushing to remote...
✅ Successfully pushed to claude/github-connector-011CUtdC2RTxFRm9vEYuH5rg
```

## Integration

### Backward Compatibility

The enhanced `.sync-vault.sh` maintains full compatibility with existing LaunchAgent/cron configurations:
- Same file path
- Same logging behavior
- Same exit codes
- Enhanced with intelligent commit messages

### Configuration

All behavior is customizable via `github-connector.yml`:
- Commit message templates
- Entity tracking directories
- TODO scan sources
- Sync behavior settings

### Dependencies

- Python 3.7+ (vault has Python 3.11) ✅
- Standard library only (no external dependencies required)
- Optional: PyYAML for better config handling
- Optional: GitHub CLI (`gh`) for issue creation

## Benefits for Investigation Workflow

1. **Better Version History**
   - Meaningful commit messages make it easy to track investigation progress
   - Entity changes are clearly documented
   - Analysis updates are properly categorized

2. **Task Management**
   - 100 TODO items automatically discovered and tracked
   - Can create GitHub issues directly from command line
   - Progress tracking across investigation phases

3. **Transparency**
   - Activity reports show exactly what's happening
   - Entity tracking highlights network connections
   - Clear audit trail of all changes

4. **Automation**
   - Replaces manual sync with intelligent automation
   - Reduces commit message fatigue
   - Maintains investigation context automatically

## Documentation

Complete documentation provided in `GITHUB_CONNECTOR.md` including:
- Installation instructions
- Usage examples for all commands
- Configuration guide
- Integration instructions
- Troubleshooting section
- Tips and best practices

## Commits Included

1. `f8938e0` - Add GitHub Connector for Claude (initial implementation)
2. `b8787d2` - Update 2 files (integrate with auto-sync workflow)

## How to Test

After merging, you can test the connector:

```bash
# Generate a report
./github-connector.py report

# List all entities
./github-connector.py entities

# Check current status
./github-connector.py status

# Test sync (dry run without push)
./github-connector.py sync --no-push
```

## Future Enhancements

Potential additions (not in this PR):
- GitHub Actions integration for automated analysis
- PR template generation based on investigation findings
- Issue templates for different investigation types
- Automated evidence linking
- Timeline generation from commit history

## Notes

- All changes are non-breaking
- Original sync script functionality preserved
- Documentation is comprehensive
- Code follows Python best practices
- Ready for immediate use

---

**Branch:** `claude/github-connector-011CUtdC2RTxFRm9vEYuH5rg`
**Target:** `main`
**Total Changes:** +997 lines, -54 lines
**Files Changed:** 5 files
**Status:** ✅ Ready to merge
