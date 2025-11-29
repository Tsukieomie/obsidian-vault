#!/bin/bash

# Complete Cline setup script
# This installs and configures everything needed for Cline in your vault

set -e

VAULT_PATH="/home/user/obsidian-vault"
CLINE_CONFIG="$VAULT_PATH/.cline-config.json"

echo "🔧 Complete Cline Setup"
echo "══════════════════════════════════════"
echo ""

# Step 1: Check Node.js
echo "Step 1: Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install it:"
    echo "   https://nodejs.org"
    exit 1
fi
NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION"

# Step 2: Check VS Code
echo ""
echo "Step 2: Checking VS Code installation..."
if ! command -v code &> /dev/null; then
    echo "⚠️  VS Code not found. This is optional but recommended."
    echo ""
    read -p "Would you like to see VS Code installation instructions? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cat << 'EOF'

📥 VS Code Installation:

macOS:
  brew install visual-studio-code

Ubuntu/Debian:
  sudo apt update && sudo apt install code

Fedora:
  sudo dnf install code

Snap (any Linux):
  snap install code --classic

Windows:
  Download from https://code.visualstudio.com

After installation, run this script again.
EOF
        exit 1
    fi
else
    CODE_VERSION=$(code --version | head -1)
    echo "✅ VS Code $CODE_VERSION"
fi

# Step 3: Verify configuration files
echo ""
echo "Step 3: Checking configuration files..."

if [ -f "$CLINE_CONFIG" ]; then
    echo "✅ Cline config exists: $CLINE_CONFIG"
else
    echo "⚠️  Cline config not found"
fi

if [ -f "$VAULT_PATH/.claude/settings.json" ]; then
    echo "✅ Claude Code settings exists"
else
    echo "⚠️  Claude Code settings not found"
fi

if [ -f "$VAULT_PATH/.gitignore" ]; then
    echo "✅ .gitignore configured"
else
    echo "⚠️  .gitignore not found"
fi

# Step 4: Install Cline VS Code extension (if VS Code is available)
if command -v code &> /dev/null; then
    echo ""
    echo "Step 4: Installing Cline VS Code extension..."
    code --install-extension saoudrizwan.claude-dev --force 2>&1 || {
        echo "⚠️  Could not auto-install Cline extension"
        echo "   You'll need to install it manually:"
        echo "   1. Press Ctrl+Shift+X (Cmd+Shift+X on Mac)"
        echo "   2. Search 'Cline'"
        echo "   3. Click Install"
    }
    echo "✅ Extension installation attempted"
fi

# Step 5: Instructions for API key
echo ""
echo "Step 5: API Key Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Choose your API provider:"
echo ""
echo "Option A: Claude (Recommended)"
echo "  1. Go to: https://console.anthropic.com/keys"
echo "  2. Create API key"
echo "  3. In Cline settings, paste key"
echo ""
echo "Option B: Google Gemini (Free tier)"
echo "  1. Go to: https://aistudio.google.com"
echo "  2. Get API key"
echo "  3. In Cline settings, paste key"
echo ""
echo "Option C: OpenRouter (Multi-model)"
echo "  1. Go to: https://openrouter.ai"
echo "  2. Create account and API key"
echo "  3. In Cline settings, paste key"
echo ""

# Step 6: Summary
echo ""
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━"
echo ""

if command -v code &> /dev/null; then
    echo "To launch VS Code with your vault:"
    echo "  $VAULT_PATH/.claude/launch-vscode.sh"
    echo ""
    echo "Or from terminal:"
    echo "  code $VAULT_PATH"
else
    echo "VS Code is not installed yet."
    echo "Once installed, use:"
    echo "  code $VAULT_PATH"
fi

echo ""
echo "Then configure Cline:"
echo "  1. Click Cline icon in sidebar"
echo "  2. Settings → Add API key"
echo "  3. Start chatting with Cline!"
echo ""
