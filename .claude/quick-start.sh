#!/bin/bash

# Quick Start Guide for Cline + Claude Code + Obsidian Vault
# Run this from the vault directory

VAULT="/home/user/obsidian-vault"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Obsidian Vault + Cline + Claude Code Quick Start         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

# Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js $(node --version)"
else
    echo "❌ Node.js not found (required)"
    exit 1
fi

# npm
if command -v npm &> /dev/null; then
    echo "✅ npm $(npm --version)"
else
    echo "❌ npm not found (required)"
    exit 1
fi

# Claude Code
if command -v claude &> /dev/null; then
    echo "✅ Claude Code CLI installed"
else
    echo "⚠️  Claude Code CLI not found (optional, but recommended)"
fi

# VS Code
if command -v code &> /dev/null; then
    echo "✅ VS Code $(code --version | head -1)"
else
    echo "⚠️  VS Code not found (you can install it)"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1️⃣  Install VS Code (if not done):"
echo "   📖 See: .claude/VSCODE_INSTALLATION.md"
echo "   💻 Or: https://code.visualstudio.com"
echo ""
echo "2️⃣  Launch VS Code with vault:"
echo "   📝 $VAULT/.claude/launch-vscode.sh"
echo "   OR: code $VAULT"
echo ""
echo "3️⃣  Install Cline extension (in VS Code):"
echo "   🔍 Press: Ctrl+Shift+X (Cmd+Shift+X on Mac)"
echo "   🔎 Search: Cline"
echo "   📦 Click: Install (by saoudrizwan)"
echo ""
echo "4️⃣  Configure API:"
echo "   ⚙️  Cline Settings → Choose Provider:"
echo "   • Claude: https://console.anthropic.com/keys"
echo "   • Gemini: https://aistudio.google.com (FREE)"
echo "   • OpenRouter: https://openrouter.ai"
echo ""
echo "5️⃣  Start chatting with Cline!"
echo "   💬 Type your task in Cline panel"
echo "   ✅ Approve each step"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🎯 Example Tasks for Cline:"
echo ""
echo "• 'Review all files in Analysis/ and summarize'"
echo "• 'List all people mentioned in the vault'"
echo "• 'Create a timeline from all documents'"
echo "• 'Find all inconsistencies in entity references'"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📚 Documentation:"
echo "  • .claude/VSCODE_INSTALLATION.md  - VS Code setup"
echo "  • .claude/CLINE_vs_CLAUDE_CODE.md - Tool comparison"
echo "  • .claude/MCP_SETUP.md            - Cloud sync options"
echo ""
