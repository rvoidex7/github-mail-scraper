#!/bin/bash
# Quick start script for the GitHub patch scraper

set -e

echo "🚀 GitHub .patch Scraper - Quick Start"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check pip
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is not installed"
    echo ""
    echo "Install pip with one of these commands:"
    echo "  • Arch/Manjaro: sudo pacman -S python-pip"
    echo "  • Debian/Ubuntu: sudo apt install python3-pip"
    echo "  • macOS: curl https://bootstrap.pypa.io/get-pip.py | python3"
    exit 1
fi

echo "✓ pip found: $(python3 -m pip --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install -q -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Run tests
echo "🧪 Running tests..."
python3 -m pytest -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "Try fetching a .patch URL:"
echo "  python3 -m scraper.cli fetch https://github.com/psf/requests/pull/6000.patch"
echo ""
echo "Or see all options:"
echo "  python3 -m scraper.cli --help"
