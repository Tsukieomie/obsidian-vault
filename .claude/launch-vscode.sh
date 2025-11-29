#!/bin/bash

# Launch VS Code with Obsidian vault
# This script opens VS Code with the vault folder and configures it for Cline

VAULT_PATH="/home/user/obsidian-vault"

echo "🚀 Launching VS Code with Obsidian Vault..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if code command is available
if ! command -v code &> /dev/null; then
    echo "❌ VS Code not found. Please install it:"
    echo ""
    echo "   macOS:   brew install visual-studio-code"
    echo "   Ubuntu:  sudo apt install code"
    echo "   Fedora:  sudo dnf install code"
    echo "   Snap:    snap install code --classic"
    echo "   Manual:  https://code.visualstudio.com/download"
    echo ""
    echo "After installing, run this script again."
    exit 1
fi

# Check if Cline extension is installed
echo "Checking for Cline extension..."
CODE_VERSION=$(code --version | head -1)
echo "✅ VS Code $CODE_VERSION found"

# Open VS Code with the vault
echo "Opening vault folder: $VAULT_PATH"
code "$VAULT_PATH"

echo ""
echo "🎯 VS Code is launching!"
echo ""
echo "Next steps:"
echo "  1. If Cline extension is not installed:"
echo "     - Press Ctrl+Shift+X (Cmd+Shift+X on Mac)"
echo "     - Search for 'Cline'"
echo "     - Click Install (by saoudrizwan)"
echo ""
echo "  2. Configure Cline API:"
echo "     - Click Cline icon in sidebar"
echo "     - Click Settings (gear icon)"
echo "     - Choose API provider (Claude, Gemini, etc.)"
echo "     - Add your API key"
echo ""
echo "  3. Start using Cline:"
echo "     - Click Cline icon"
echo "     - Type your task in the chat"
echo "     - Approve each step"
echo ""
