#!/bin/bash
# install-multi-session.sh
# One-command setup for multi-session MemPalace memory sharing
#
# Usage: ./install-multi-session.sh

set -e

echo "🏰 MemPalace Multi-Session Installer"
echo "===================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install Python 3.9+"
    exit 1
fi

# Check MemPalace
if ! python3 -m pip show mempalace &> /dev/null; then
    echo "📦 Installing MemPalace..."
    python3 -m pip install mempalace
else
    echo "✅ MemPalace already installed"
fi

# Create standard palace directory
PALACE_DIR="$HOME/.mempalace"
if [[ ! -d "$PALACE_DIR/palace" ]]; then
    echo "🛠️  Initializing palace at $PALACE_DIR..."
    mkdir -p "$PALACE_DIR/palace"
    echo "   Run 'mempalace init' to configure your first wing/room structure."
else
    echo "✅ Palace already exists at $PALACE_DIR"
fi

# Run the hook setup script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../hooks/setup_multi_session_hooks.sh" ]]; then
    echo "🔧 Configuring AI session hooks..."
    "$SCRIPT_DIR/../hooks/setup_multi_session_hooks.sh"
    echo "✅ Hooks configured"
else
    echo "⚠️  Hook script not found. Skipping hook configuration."
    echo "   Run 'hooks/setup_multi_session_hooks.sh' manually if needed."
fi

echo ""
echo "===================================="
echo "✅ Installation Complete!"
echo ""
echo "Next steps:"
echo "1. Run 'mempalace init' to set up your initial profile"
echo "2. Start any AI session (Claude, Gemini, etc.)"
echo "3. Search across sessions: mempalace search 'your query'"
echo ""
echo "For support: https://github.com/zhapostolski/mempalace-toolkit"
