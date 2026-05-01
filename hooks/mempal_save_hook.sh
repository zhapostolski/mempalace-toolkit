#!/bin/bash
# MEMPALACE SAVE HOOK — Auto-detect harness (claude-code, codex, opencode, claude)
#
# Add to Claude Code settings.json (hooks.Stop) or use directly.
# For Codex, add to .codex/hooks.json with "type": "command".

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMPALACE_SRC="$(dirname "$SCRIPT_DIR")"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$MEMPALACE_SRC"

INPUT=$(cat)

HARNESS="claude-code"
PARENT_CMD=$(ps -p $PPID -o comm= 2>/dev/null | tr -d ' ' || echo "")

case "$PARENT_CMD" in
    codex|Codex)
        HARNESS="codex"
        ;;
    opencode|Opencode)
        HARNESS="opencode"
        ;;
    claude|Claude|claude-sonnet*|claude-code)
        HARNESS="claude-code"
        ;;
    gemini|Gemini|gemini-cli)
        HARNESS="gemini"
        ;;
    qwen|Qwen|qwen-code)
        HARNESS="qwen"
        ;;
    droid|Droid|dask|deepseek)
        HARNESS="deepseek"
        ;;
    *)
        # Check for indicators in the input
        if echo "$INPUT" | grep -q "claude-code"; then
            HARNESS="claude-code"
        elif echo "$INPUT" | grep -q "gemini-cli"; then
            HARNESS="gemini"
        elif echo "$INPUT" | grep -q "qwen-code"; then
            HARNESS="qwen"
        elif echo "$INPUT" | grep -q '"transcript_path".*codex"'; then
            HARNESS="codex"
        fi
        ;;
esac

printf '%s' "$INPUT" | python3 -m mempalace hook run --hook stop --harness "$HARNESS"
