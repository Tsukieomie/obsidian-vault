# VS Code & Cline Installation Guide

This guide covers installing VS Code and Cline in your environment.

## Quick Setup

### Fastest Way: Run Setup Script
```bash
cd /home/user/obsidian-vault
./.claude/setup-cline.sh
```

This automatically:
- ✅ Checks Node.js (already installed)
- ✅ Checks VS Code installation
- ✅ Installs Cline extension
- ✅ Guides you through API setup

---

## Installation by Operating System

### macOS

#### Option 1: Homebrew (Recommended)
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install VS Code
brew install visual-studio-code

# Launch with vault
code /home/user/obsidian-vault
```

#### Option 2: Direct Download
1. Visit https://code.visualstudio.com/download
2. Click macOS (Intel or Apple Silicon)
3. Drag VS Code to Applications folder
4. Run: `code /home/user/obsidian-vault`

---

### Linux (Ubuntu/Debian)

#### Option 1: apt
```bash
# Add Microsoft repository
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null

# Install
sudo apt update
sudo apt install code
```

#### Option 2: Snap
```bash
snap install code --classic
```

#### Option 3: .deb File
1. Download from https://code.visualstudio.com/download
2. Run: `sudo dpkg -i code_latest_amd64.deb`

---

### Linux (Fedora/RHEL)

```bash
# Add repository
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

# Install
sudo dnf install code
```

---

### Windows

1. Visit https://code.visualstudio.com/download
2. Click Windows (Stable)
3. Run the installer
4. Make sure "Add to PATH" is checked
5. In PowerShell: `code C:\Users\YourUser\obsidian-vault`

---

### Docker (If Everything Else Fails)

Run VS Code in a Docker container:

```bash
docker run -it --rm \
  -v /home/user/obsidian-vault:/workspace \
  -p 8000:8000 \
  -e DISPLAY=$DISPLAY \
  codercom/code-server:latest \
  code /workspace
```

Access at: http://localhost:8000

---

## Post-Installation: Cline Setup

After installing VS Code:

### Step 1: Install Cline Extension

**Method A: Marketplace (Easiest)**
1. Open VS Code
2. Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)
3. Search: `Cline`
4. Click Install (by saoudrizwan)

**Method B: Command Line**
```bash
code --install-extension saoudrizwan.claude-dev
```

**Method C: Manual Installation**
1. Download: https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev
2. Click "Install"
3. VS Code opens and installs

### Step 2: Configure API Provider

#### Option A: Claude (Recommended)

1. Get API key:
   - Go to: https://console.anthropic.com/keys
   - Click "Create Key"
   - Copy your key

2. Configure in Cline:
   - Click Cline icon in sidebar
   - Click Settings (gear icon)
   - Select "Anthropic" from provider dropdown
   - Paste API key
   - Click Save

#### Option B: Google Gemini (Free Tier)

1. Get API key:
   - Go to: https://aistudio.google.com
   - Click "Get API Key"
   - Copy key

2. Configure in Cline:
   - Click Cline icon → Settings
   - Select "Google Gemini"
   - Paste API key
   - Click Save

#### Option C: OpenRouter (Multi-Model)

1. Get API key:
   - Go to: https://openrouter.ai
   - Sign up / login
   - Get API key from https://openrouter.ai/keys

2. Configure in Cline:
   - Click Cline icon → Settings
   - Select "OpenRouter"
   - Paste API key
   - Click Save

### Step 3: Open Your Vault

```bash
# From terminal
code /home/user/obsidian-vault
```

Or use the launch script:
```bash
/home/user/obsidian-vault/.claude/launch-vscode.sh
```

### Step 4: Start Using Cline

1. Click **Cline icon** in left sidebar (should show a sparkle/star)
2. You'll see the **Cline chat panel**
3. Type your first task:
   ```
   Review the vault structure and explain what you find
   ```
4. Click **Send**
5. Review Cline's suggested actions
6. Click ✅ to approve each step

---

## VS Code Settings for Obsidian Vault

The project includes:
- `.cline-config.json` - Cline-specific settings
- `.claude/settings.json` - Claude Code MCP server settings
- `.gitignore` - Protects sensitive files

These are automatically loaded by VS Code.

---

## Troubleshooting

### "Command 'code' not found"

**Solution 1: Add to PATH**
```bash
# Get VS Code installation path
which code

# If empty, VS Code might not be in PATH
# macOS: /usr/local/bin/code or /opt/homebrew/bin/code
# Linux: /usr/bin/code

# Add symlink (Linux):
sudo ln -s /usr/bin/code /usr/local/bin/code
```

**Solution 2: Reinstall**
```bash
# macOS
brew uninstall visual-studio-code
brew install visual-studio-code

# Ubuntu
sudo apt remove code
sudo apt install code
```

### Cline Extension Not Showing

1. Restart VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"
2. Check extension installed: `Ctrl+Shift+X` → Search "Cline"
3. Check status in Activity Bar (left sidebar)

### API Key Not Working

1. Verify key is correct (no extra spaces)
2. Check API provider is active:
   - Claude: https://console.anthropic.com/keys
   - Gemini: https://aistudio.google.com
   - OpenRouter: https://openrouter.ai
3. Restart VS Code after changing API key

### Performance Issues

If VS Code is slow:

```json
// Add to .vscode/settings.json
{
  "files.exclude": {
    ".git": true,
    ".obsidian": true,
    "node_modules": true
  },
  "search.exclude": {
    ".git": true,
    ".obsidian": true
  }
}
```

### Network/Proxy Issues

If you're behind a proxy:

```json
// Settings → Edit Settings (JSON)
{
  "http.proxy": "http://proxy.company.com:8080",
  "http.proxyStrictSSL": false
}
```

---

## Launch Scripts

### Quick Launch

```bash
# Make executable if needed
chmod +x /home/user/obsidian-vault/.claude/launch-vscode.sh

# Launch with vault
/home/user/obsidian-vault/.claude/launch-vscode.sh
```

### From Anywhere

Add to your shell profile (`~/.bash_profile`, `~/.zshrc`, etc.):

```bash
alias vault-code='code /home/user/obsidian-vault'
```

Then:
```bash
vault-code
```

---

## Using VS Code Remote (SSH/WSL)

### SSH

```bash
# Remote development
code --remote ssh://user@hostname/home/user/obsidian-vault
```

### WSL (Windows)

```bash
code --remote wsl+ubuntu-20.04:/home/user/obsidian-vault
```

---

## Integrating with Claude Code CLI

You can use both simultaneously:

```bash
# Terminal 1: VS Code with Cline
code /home/user/obsidian-vault

# Terminal 2: Claude Code CLI
cd /home/user/obsidian-vault
claude

# Or connect them:
claude /ide
```

Both access the same files via Git and sync automatically.

---

## VS Code Extensions to Consider

### Recommended for Obsidian Vault:
- **Obsidian Markdown Preview** - Preview markdown like Obsidian
- **GitHub Copilot** - Extra AI assistance
- **GitLens** - Powerful Git integration
- **Markdown All in One** - Better markdown support
- **Pylance** (if using Python) - Python language support

Install from Extensions (Ctrl+Shift+X).

---

## Next Steps

1. ✅ Install VS Code (if not already done)
2. ✅ Install Cline extension
3. ✅ Add API key (Claude, Gemini, or OpenRouter)
4. ✅ Open vault: `code /home/user/obsidian-vault`
5. ✅ Start with simple task: "List all files in this vault"
6. ✅ Explore and build confidence

---

## Getting Help

- **Cline Issues**: https://github.com/cline/cline/issues
- **VS Code Help**: https://code.visualstudio.com/docs
- **Cline Docs**: https://docs.cline.bot
- **API Provider Support**:
  - Claude: https://support.anthropic.com
  - Google: https://support.google.com/aistudio
  - OpenRouter: https://openrouter.ai/docs

---

## Summary

```bash
# Quick Start Checklist

# 1. Install VS Code
brew install visual-studio-code  # macOS
sudo apt install code            # Ubuntu
# or visit https://code.visualstudio.com

# 2. Open vault
code /home/user/obsidian-vault

# 3. Install Cline
# Ctrl+Shift+X → Search "Cline" → Install

# 4. Add API Key
# Cline Settings → Choose Provider → Paste Key

# 5. Start using!
# Type task in Cline chat panel
```

You're ready to go! 🚀
