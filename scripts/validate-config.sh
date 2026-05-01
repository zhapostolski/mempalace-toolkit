#!/bin/bash
# validate-config.sh
# Validate that all AI sessions are properly configured

echo "🔍 MemPalace Configuration Validator"
echo "===================================="
echo ""

errors=0
warnings=0

# Check palace exists
if [[ -d "$HOME/.mempalace/palace" ]]; then
    echo "✅ Palace directory exists"
else
    echo "⚠️  Palace not found at ~/.mempalace/palace"
    ((warnings++))
fi

# Check hooks
check_hooks() {
    local config_file="$1"
    local session_name="$2"
    
    if [[ ! -f "$config_file" ]]; then
        echo "ℹ️  $session_name config not found ($config_file)"
        return
    fi
    
    if grep -q "mempal_save_hook" "$config_file" 2>/dev/null; then
        echo "✅ $session_name: Hooks configured"
    else
        echo "⚠️  $session_name: Hooks not configured"
        ((warnings++))
    fi
}

check_hooks "$HOME/.claude/settings.json" "Claude Code"
check_hooks "$HOME/.gemini/settings.json" "Gemini CLI"
check_hooks "$HOME/.qwen/settings.json" "Qwen"

# Check MCP servers
echo ""
echo "MCP Server Check:"
echo "-----------------"

for proj in ~/projects/*/.mcp.json; do
    if [[ -f "$proj" ]] && grep -q "mempalace" "$proj"; then
        project_name=$(basename $(dirname "$proj"))
        echo "✅ $project_name: MemPalace MCP configured"
    fi
done

echo ""
echo "===================================="
echo "Summary: $errors errors, $warnings warnings"

if [[ $warnings -gt 0 ]]; then
    echo ""
    echo "Run './install-multi-session.sh' to auto-fix missing configurations"
fi
