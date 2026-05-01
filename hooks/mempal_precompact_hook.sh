#!/bin/bash
# MEMPALACE PRE-COMPACT HOOK — Emergency save before compaction

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMPALACE_SRC="$(dirname "$SCRIPT_DIR")"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}$MEMPALACE_SRC"

STATE_DIR="$HOME/.mempalace/hook_state"
mkdir -p "$STATE_DIR"

# Optional: set to the directory you want auto-ingested before compaction.
MEMPAL_DIR=""

# Read JSON input from stdin
INPUT=$(cat)

SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id','unknown'))" 2>/dev/null || echo "unknown")

# Detect harness
HARNESS="claude-code"
PARENT_CMD=$(ps -p $PPID -o comm= 2>/dev/null | tr -d ' ' || echo "")
case "$PARENT_CMD" in
    codex|Codex) HARNESS="codex" ;;
    opencode|Opencode) HARNESS="opencode" ;;
    claude|Claude|claude-sonnet*|claude-code) HARNESS="claude-code" ;;
    gemini|Gemini|gemini-cli) HARNESS="gemini" ;;
esac

echo "[$(date '+%H:%M:%S')] PRE-COMPACT triggered for session $SESSION_ID (harness: $HARNESS)" >> "$STATE_DIR/hook.log"

# Select behavior.
MODE="${MEMPAL_PRECOMPACT_MODE:-}"
if [ -z "$MODE" ]; then
    if [[ "$HARNESS" == "claude-code" ]] || [[ "$HARNESS" == "gemini" ]]; then
        MODE="proceed"
    else
        MODE="block_once"
    fi
fi

# Optional: run mempalace ingest
if [ -n "$MEMPAL_DIR" ] && [ -d "$MEMPAL_DIR" ]; then
    python3 -m mempalace mine "$MEMPAL_DIR" >> "$STATE_DIR/hook.log" 2>&1 || true
fi

# If configured to never block, allow compaction to proceed.
if [ "$MODE" = "proceed" ]; then
    echo "[$(date '+%H:%M:%S')] Session $SESSION_ID: MODE=proceed - allowing compaction" >> "$STATE_DIR/hook.log"
    echo '{"decision": "allow"}'
    exit 0
fi

NOTIFIED_FILE="$STATE_DIR/${SESSION_ID}.notified"

if [ -f "$NOTIFIED_FILE" ]; then
    echo "[$(date '+%H:%M:%S')] Session $SESSION_ID already notified - allowing compaction" >> "$STATE_DIR/hook.log"
    echo '{"decision": "allow"}'
    exit 0
fi

# If configured to always block
if [ "$MODE" = "block" ]; then
    echo "[$(date '+%H:%M:%S')] Session $SESSION_ID: MODE=block — blocking" >> "$STATE_DIR/hook.log"
    echo '{"decision": "block", "reason": "COMPACTION IMMINENT. Save your session context to MemPalace before proceeding."}'
    exit 0
fi

# First time for this session — mark and block
touch "$NOTIFIED_FILE"
echo "[$(date '+%H:%M:%S')] Session $SESSION_ID: blocking to prompt save" >> "$STATE_DIR/hook.log"
echo '{"decision": "block", "reason": "COMPACTION IMMINENT. Save your session context to MemPalace before proceeding."}'
