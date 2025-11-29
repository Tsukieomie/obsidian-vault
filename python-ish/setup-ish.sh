#!/bin/sh
# Setup script for Python on iSH
# This script installs Python 3 and essential packages for iSH (Alpine Linux)

echo "================================"
echo "  Python Setup for iSH"
echo "================================"
echo ""

# Update package index
echo "📦 Updating package index..."
apk update

# Install Python 3 and pip
echo "🐍 Installing Python 3..."
apk add python3 py3-pip

# Install development tools
echo "🔧 Installing development tools..."
apk add python3-dev build-base

# Install useful system packages
echo "📚 Installing useful packages..."
apk add git nano vim curl wget

# Upgrade pip
echo "⬆️  Upgrading pip..."
python3 -m pip install --upgrade pip

# Install Python packages from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "📥 Installing Python packages from requirements.txt..."
    python3 -m pip install -r requirements.txt
else
    echo "⚠️  No requirements.txt found, installing basic packages..."
    python3 -m pip install requests numpy pandas matplotlib
fi

# Create a symlink for python command (optional)
echo "🔗 Creating python symlink..."
if ! command -v python &> /dev/null; then
    ln -sf /usr/bin/python3 /usr/bin/python
fi

# Verify installation
echo ""
echo "✅ Installation complete!"
echo ""
echo "Installed versions:"
python3 --version
pip3 --version

echo ""
echo "================================"
echo "  Setup Complete!"
echo "================================"
echo ""
echo "You can now run Python scripts with:"
echo "  python3 script.py"
echo "  or"
echo "  ./run.py (if the script has shebang)"
echo ""
