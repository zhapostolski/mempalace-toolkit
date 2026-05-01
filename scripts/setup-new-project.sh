#!/bin/bash
# setup-new-project.sh
# Auto-wire a new project with MemPalace memory
#
# Usage: ./setup-new-project.sh [project-name]
# Example: ./setup-new-project.sh my-awesome-app

set -e

PROJECT_NAME="${1:-$(basename $(pwd))}"
PROJECT_DIR="${2:-.}"

echo "🏰 Wiring project: $PROJECT_NAME"
echo "===================================="
echo ""

# Create .mcp.json
cat > "$PROJECT_DIR/.mcp.json" << MCP_EOF
{
  "mcpServers": {
    "mempalace": {
      "type": "stdio",
      "command": "python3",
      "args": ["-m", "mempalace.mcp_server"],
      "env": {
        "PYTHONPATH": "${MEMPALACE_PYTHONPATH:-/path/to/.mempalace/src}"
      }
    }
  }
}
MCP_EOF

echo "✅ Created .mcp.json with mempalace server"

# Create .mempalace/project.config if it doesn't exist
if [[ ! -f "$PROJECT_DIR/.mempalace/project.config" ]]; then
    mkdir -p "$PROJECT_DIR/.mempalace"
    cat > "$PROJECT_DIR/.mempalace/project.config" << CONFIG_EOF
{
  "project": "$PROJECT_NAME",
  "wing": "wing_$PROJECT_NAME",
  "created": "$(date -Iseconds)"
}
CONFIG_EOF
    echo "✅ Created project configuration"
else
    echo "ℹ️  Project config already exists"
fi

echo ""
echo "===================================="
echo "✅ $PROJECT_NAME is now wired for MemPalace!"
echo ""
echo "To mine this project:"
echo "  mempalace mine $PROJECT_DIR --wing wing_$PROJECT_NAME"
echo ""
echo "To search memory:"
echo "  mempalace search 'your query' --wing wing_$PROJECT_NAME"
