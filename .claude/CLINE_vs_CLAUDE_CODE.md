# Cline vs Claude Code: Setup & Comparison

This guide explains both tools and how to use them together for your Obsidian vault project.

## Quick Comparison

### Claude Code (What You're Using Now)
- **Interface**: CLI (command line)
- **Installation**: `brew install claude` or similar
- **Access**: Terminal-based, full control
- **Best for**: Autonomous task completion, batch operations
- **MCP Support**: Full support for all MCP servers
- **Cost**: Pay-per-API-use

### Cline (VS Code Extension)
- **Interface**: VS Code sidebar (graphical)
- **Installation**: VS Code Marketplace extension
- **Access**: Click icon in VS Code
- **Best for**: Interactive coding, visual feedback
- **MCP Support**: Growing support
- **Cost**: Free with API key (any provider)

## When to Use Each

### Use Claude Code When:
- Running batch operations
- Working in terminal/SSH environments
- Need to coordinate multiple tools
- Performing complex multi-step refactoring
- Working with MCP servers extensively
- Running scripts and automation

### Use Cline When:
- Want visual feedback in IDE
- Prefer interactive step-by-step workflow
- Need to review changes before approval
- Working on UI/display code
- Testing in real-time in editor
- Less technical users

## Installation & Setup

### Option 1: Cline (VS Code Extension) - Recommended for Visual Work

#### Step 1: Install VS Code
```bash
# macOS (if not installed)
brew install visual-studio-code

# Ubuntu/Linux
sudo apt install code

# Or download from https://code.visualstudio.com
```

#### Step 2: Install Cline Extension
1. Open VS Code
2. Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)
3. Search for "Cline"
4. Click Install (by saoudrizwan)

#### Step 3: Configure API
1. Click Cline icon in left sidebar (should appear after install)
2. Click "Settings" (gear icon)
3. Choose provider:
   - **Anthropic** (Claude): https://console.anthropic.com/keys
   - **Google Gemini** (Free): https://aistudio.google.com
   - **OpenRouter**: https://openrouter.ai
4. Add your API key

#### Step 4: Open Folder
1. File → Open Folder → `/home/user/obsidian-vault`
2. Cline will index your vault
3. Start asking questions in Cline chat

### Option 2: Continue with Claude Code (CLI) - What You Have

You already have this set up! Use it with:
```bash
cd /home/user/obsidian-vault
claude
# or
claude /ide  # to connect to VS Code
```

## Example Workflows

### Scenario 1: Review Investigation Files
**Best with Cline** (visual, interactive):
1. Open vault in VS Code
2. Click Cline icon
3. Ask: "Review all Analysis files and summarize findings"
4. Cline shows files in sidebar, you approve each action
5. Changes appear in editor in real-time

**With Claude Code** (autonomous, fast):
```bash
claude "Review all Analysis files in /home/user/obsidian-vault/Analysis and create summary"
```

### Scenario 2: Refactor Investigation Structure
**Best with Cline**:
1. Open Cline chat
2. Ask: "Reorganize Entities folder by connection strength"
3. Review each file change in editor before approving
4. See diffs side-by-side

**With Claude Code**:
```bash
claude "Reorganize Entities/ folder: high confidence (95%+), medium (50-95%), low (<50%)"
```

### Scenario 3: Update Documentation
**Best with Cline**:
1. Click on file in sidebar
2. Say "Update this Analysis file with new findings"
3. See edits appear in editor
4. Save when ready

**With Claude Code**:
```bash
claude /edit Analysis/Z_FILE_DEEP_ANALYSIS.md
# Provides edits that you apply
```

## Using Both Tools Together

### Recommended Workflow

1. **Planning Phase**: Use Claude Code (CLI)
   ```bash
   claude "Analyze vault structure and create task plan"
   ```

2. **Implementation Phase**: Use Cline (VS Code)
   - Open in VS Code
   - Use Cline for interactive changes
   - See diffs before committing

3. **Review Phase**: Use Claude Code (CLI)
   ```bash
   claude "Review all changes and verify completeness"
   ```

4. **Commit Phase**: Either tool
   ```bash
   # CLI version
   claude "Commit changes with message: [your message]"

   # Or manual
   git add .
   git commit -m "..."
   git push
   ```

## File Structure

```
/home/user/obsidian-vault/
├── .claude/
│   ├── settings.json          # Claude Code MCP servers
│   ├── settings.local.json    # Credentials (not committed)
│   ├── MCP_SETUP.md           # MCP guide
│   └── CLINE_vs_CLAUDE_CODE.md ← You are here
├── .cline-config.json         # Cline configuration (optional)
├── .gitignore                 # Protects sensitive files
└── [investigation files...]
```

## Configuration

### Cline Custom Instructions

Set up Cline-specific rules in `.cline-config.json`:
- Ignore patterns (`.obsidian/`, `node_modules/`)
- Custom instructions for your vault
- Workspace folder definitions
- Environment settings

### Claude Code MCP Servers

Set up in `.claude/settings.json`:
- Filesystem access
- Git operations
- Fetch external content
- Custom MCP servers

## Security Considerations

### Protect Your Data
1. **API Keys**:
   - Store in `.claude/settings.local.json` (not committed)
   - Use `.env` for additional keys
   - Never commit credentials

2. **Git Security**:
   - `.gitignore` protects sensitive files
   - Always review changes before push
   - Use branch protection on main

3. **File Access**:
   - Both tools can read/write files
   - Review AI suggestions before applying
   - Maintain commit history for auditability

## Troubleshooting

### Cline Connection Issues
- Verify VS Code is updated to latest version
- Check API provider credentials
- Restart VS Code after install
- Check extension output: View → Output → Cline

### Claude Code Issues
- Run `claude --version` to verify installation
- Test with `claude /help`
- Check MCP servers: `claude /mcp`

### Sync Between Tools
- Both use same Git repository
- Both access same file system
- Commits from either are visible in both
- Keep VS Code open while using CLI to avoid conflicts

## API Cost Comparison

### Using Claude (Anthropic)
- Input: $3 per million tokens
- Output: $15 per million tokens
- Typical investigation review: $0.10-$1.00

### Using Google Gemini (Free)
- 50 free calls/day (Cline only)
- Good for testing
- Rate limited after free tier

### Using OpenRouter
- Multiple models available
- Pricing varies by model
- Often cheaper than direct providers

## Next Steps

### Quick Start
1. Install Cline in VS Code
2. Open your vault folder
3. Test with a simple task: "List all markdown files"
4. Compare with Claude Code CLI

### Full Integration
1. Keep both tools installed
2. Use Claude Code for big tasks
3. Use Cline for interactive work
4. Both sync via Git

### Optimization
1. Customize `.cline-config.json` for your workflow
2. Set custom MCP servers in `.claude/settings.json`
3. Create reusable prompts for common tasks
4. Build automated workflows with Git hooks

---

## Resources

- **Cline Documentation**: https://docs.cline.bot
- **Cline GitHub**: https://github.com/cline/cline
- **Cline VS Code Marketplace**: https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev
- **Claude Code Docs**: https://code.claude.com/docs
- **Claude API Pricing**: https://www.anthropic.com/pricing/claude

## Summary

| Task | Use Cline | Use Claude Code |
|------|-----------|-----------------|
| Visual code editing | ✅ | ❌ |
| Batch automation | ❌ | ✅ |
| MCP servers | ⚠️ Growing | ✅ Full |
| Terminal workflows | ❌ | ✅ |
| Interactive feedback | ✅ | ⚠️ CLI only |
| Cost-effective | ✅ Free tier | Pay-per-use |
| Large refactoring | ⚠️ Slower | ✅ Faster |
| Git integration | ✅ | ✅ |
| Learning curve | Beginner-friendly | Developer-focused |

**Best setup**: Use both! Cline for interactive work, Claude Code for automation.
