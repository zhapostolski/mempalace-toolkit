"""
Hook logic for MemPalace — Python implementation of session-start, stop, and precompact hooks.

Reads JSON from stdin, outputs JSON to stdout.
Supported hooks: session-start, stop, precompact
Supported harnesses: claude-code, codex (extensible to cursor, gemini, etc.)
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SAVE_INTERVAL = 10
STATE_DIR = Path.home() / ".mempalace" / "hook_state"

STOP_BLOCK_REASON = (
    "AUTO-SAVE checkpoint. Save only the new meaningful items since the last "
    "checkpoint: decisions, findings, milestones, blockers, architecture "
    "changes, code or data contracts, and actionable next steps. Skip "
    "duplicates, chatter, and repeated status text. Continue conversation "
    "after saving."
)

PRECOMPACT_BLOCK_REASON = (
    "COMPACTION IMMINENT. Save ALL topics, decisions, quotes, code, and "
    "important context from this session to your memory system. Be thorough "
    "\u2014 after compaction, detailed context will be lost. Organize into "
    "appropriate categories. Use verbatim quotes where possible. Save "
    "everything, then allow compaction to proceed."
)


def _sanitize_session_id(session_id: str) -> str:
    """Only allow alnum, dash, underscore to prevent path traversal."""
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "", session_id)
    return sanitized or "unknown"


def _normalize_text(text: str) -> str:
    """Normalize transcript text for lightweight heuristics."""
    return re.sub(r"\s+", " ", text).strip()


def _extract_text(content) -> str:
    """Flatten transcript content blocks into plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        blocks = []
        for block in content:
            if isinstance(block, dict):
                text = block.get("text", "")
                if isinstance(text, str):
                    blocks.append(text)
        return " ".join(blocks)
    return ""


def _iter_real_messages(transcript_path: str):
    """Yield normalized user/assistant messages, excluding command chatter."""
    path = Path(transcript_path).expanduser()
    if not path.is_file():
        return
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    msg = entry.get("message", {})
                except (json.JSONDecodeError, AttributeError):
                    continue
                if not isinstance(msg, dict):
                    continue
                role = msg.get("role")
                if role not in {"user", "assistant"}:
                    continue
                text = _normalize_text(_extract_text(msg.get("content", "")))
                if not text or "<command-message>" in text:
                    continue
                yield role, text
    except OSError:
        return


def _iter_real_messages_any(transcript_path: str):
    """Yield user/assistant messages from ANY transcript format.
    
    Tries multiple schemas in order:
    1. Claude Code JSONL: {"message": {"role": ..., "content": ...}}
    2. Qwen JSONL: {"message": {"role": ..., "parts": [{"text": ...}]}}
    3. JSON files (Gemini, Claude sessions): via normalize.py
    4. normalize.py fallback for any format
    """
    path = Path(transcript_path).expanduser()
    if not path.is_file():
        return

    ext = path.suffix.lower()

    # Try Qwen JSONL schema: {"message": {"role": "...", "parts": [{"text": "..."}]}}
    if ext == ".jsonl":
        try:
            found = False
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                    except (json.JSONDecodeError, AttributeError):
                        continue
                    msg = entry.get("message", {})
                    if not isinstance(msg, dict):
                        continue
                    role = msg.get("role")
                    if role not in {"user", "assistant"}:
                        continue
                    parts = msg.get("parts", [])
                    text = ""
                    if isinstance(parts, list):
                        text = " ".join(p.get("text", "") for p in parts if isinstance(p, dict))
                    if text and "<command-message>" not in text:
                        found = True
                        yield role, _normalize_text(text)
            if found:
                return
        except OSError:
            pass

    # Try standard JSONL schema (Claude Code, Codex)
    for role, text in _iter_real_messages(transcript_path):
        yield role, text

    # For JSON files (Gemini, Claude session files), use normalize.py
    if ext == ".json":
        try:
            from mempalace.normalize import normalize
            transcript = normalize(str(path))
            if transcript and "> " in transcript:
                lines = transcript.split("\n")
                i = 0
                while i < len(lines):
                    if lines[i].startswith("> "):
                        yield "user", lines[i][2:].strip()
                        i += 1
                        if i < len(lines) and lines[i].strip() and not lines[i].startswith("> "):
                            yield "assistant", lines[i].strip()
                            i += 1
                    else:
                        i += 1
                return
        except Exception:
            pass

    # Final fallback: normalize.py for any format
    try:
        from mempalace.normalize import normalize
        transcript = normalize(str(path))
        if transcript and "> " in transcript:
            lines = transcript.split("\n")
            i = 0
            while i < len(lines):
                if lines[i].startswith("> "):
                    yield "user", lines[i][2:].strip()
                    i += 1
                    if i < len(lines) and lines[i].strip() and not lines[i].startswith("> "):
                        yield "assistant", lines[i].strip()
                        i += 1
                else:
                    i += 1
    except Exception:
        pass


def _count_human_messages(transcript_path: str) -> int:
    """Count human messages in any transcript format, skipping command chatter."""
    count = 0
    for role, _text in _iter_real_messages_any(transcript_path) or []:
        if role == "user":
            count += 1
    return count


def _log(message: str):
    """Append to hook state log file."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        log_path = STATE_DIR / "hook.log"
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(log_path, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    except OSError:
        pass


def _output(data: dict):
    """Print JSON to stdout with consistent formatting (pretty-printed)."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _maybe_auto_ingest():
    """If MEMPAL_DIR is set and exists, run mempalace mine in background."""
    mempal_dir = os.environ.get("MEMPAL_DIR", "")
    if mempal_dir and os.path.isdir(mempal_dir):
        try:
            log_path = STATE_DIR / "hook.log"
            with open(log_path, "a") as log_f:
                subprocess.Popen(
                    [sys.executable, "-m", "mempalace", "mine", mempal_dir],
                    stdout=log_f,
                    stderr=log_f,
                )
        except OSError:
            pass


def _maybe_sync_obsidian():
    """Mirror recent memory changes into the Obsidian vault when available."""
    sync_script = Path.home() / "obsidian-vault" / "sync.py"
    if not sync_script.is_file():
        return
    try:
        log_path = STATE_DIR / "hook.log"
        with open(log_path, "a") as log_f:
            subprocess.Popen(
                [sys.executable, str(sync_script), "--quick"],
                stdout=log_f,
                stderr=log_f,
            )
    except OSError:
        pass


SUPPORTED_HARNESSES = {"claude-code", "claude", "codex", "opencode", "gemini", "qwen", "deepseek"}
SIGNAL_KEYWORDS = (
    "decision",
    "plan",
    "fix",
    "build",
    "implement",
    "found",
    "finding",
    "audit",
    "error",
    "blocker",
    "risk",
    "deploy",
    "architecture",
    "infra",
    "database",
    "metric",
    "source",
    "query",
    "report",
    "powerbi",
    "portal",
    "aws",
    "rds",
    "ecs",
    "mcp",
    "api",
    "route",
    "component",
    "dataset",
    "dax",
    "migration",
    "verify",
    "passed",
    "failed",
)
ARTIFACT_HINT_RE = re.compile(
    r"`[^`]+`|/[\w./-]+|\b[\w.-]+\.(?:ts|tsx|js|jsx|py|sh|md|sql|json|ya?ml|tf)\b|https?://",
    re.IGNORECASE,
)
TRIVIAL_MESSAGE_RE = re.compile(
    r"^(?:"
    r"continue|resume|go on|keep going|proceed|"
    r"ok(?:ay)?|k|yes|yep|no|nah|"
    r"thanks|thank you|good|sounds good|do it|go ahead|"
    r"continue please|switch and continue|"
    r"codex resume --last"
    r")(?:[.!? ]+)?$",
    re.IGNORECASE,
)


def _collect_unsaved_messages(transcript_path: str, last_save: int) -> list[str]:
    """Collect the message slice after the last checkpointed user message."""
    messages: list[str] = []
    user_count = 0
    for role, text in _iter_real_messages_any(transcript_path) or []:
        if role == "user":
            user_count += 1
            if user_count <= last_save:
                continue
        elif user_count <= last_save:
            continue
        messages.append(text)
    return messages


def _looks_trivial(text: str) -> bool:
    """Treat short acknowledgements as low signal."""
    normalized = _normalize_text(text).lower()
    if not normalized:
        return True
    if TRIVIAL_MESSAGE_RE.fullmatch(normalized):
        return True
    return len(normalized) < 8


def _has_meaningful_updates(messages: list[str]) -> bool:
    """Avoid blocking on chatter-only windows."""
    substantive: list[str] = []
    keyword_hits = 0
    artifact_hits = 0

    for text in messages:
        if _looks_trivial(text):
            continue
        lower = text.lower()
        has_keyword = any(keyword in lower for keyword in SIGNAL_KEYWORDS)
        artifact_count = len(list(ARTIFACT_HINT_RE.finditer(text)))
        if has_keyword:
            keyword_hits += 1
        artifact_hits += artifact_count
        if len(text) >= 30 or has_keyword or artifact_count:
            substantive.append(text)

    if not substantive:
        return False

    char_count = sum(len(text) for text in substantive)
    if keyword_hits >= 2:
        return True
    if artifact_hits >= 2:
        return True
    if len(substantive) >= 4 and char_count >= 300:
        return True
    if len(substantive) >= 2 and char_count >= 500:
        return True
    return False


def _parse_harness_input(data: dict, harness: str) -> dict:
    """Parse stdin JSON according to the harness type."""
    if harness not in SUPPORTED_HARNESSES:
        print(f"Unknown harness: {harness}", file=sys.stderr)
        sys.exit(1)
    return {
        "session_id": _sanitize_session_id(str(data.get("session_id", "unknown"))),
        "stop_hook_active": data.get("stop_hook_active", False),
        "transcript_path": str(data.get("transcript_path", "")),
    }


def hook_stop(data: dict, harness: str):
    """Stop hook: block every N messages for auto-save."""
    parsed = _parse_harness_input(data, harness)
    session_id = parsed["session_id"]
    stop_hook_active = parsed["stop_hook_active"]
    transcript_path = parsed["transcript_path"]

    # If already in a save cycle, let through (infinite-loop prevention)
    if str(stop_hook_active).lower() in ("true", "1", "yes"):
        _output({})
        return

    # Count human messages
    exchange_count = _count_human_messages(transcript_path)

    # Track last save point
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    last_save_file = STATE_DIR / f"{session_id}_last_save"
    last_save = 0
    if last_save_file.is_file():
        try:
            last_save = int(last_save_file.read_text().strip())
        except (ValueError, OSError):
            last_save = 0

    since_last = exchange_count - last_save

    _log(f"Session {session_id}: {exchange_count} exchanges, {since_last} since last save")

    if since_last >= SAVE_INTERVAL and exchange_count > 0:
        unsaved_messages = _collect_unsaved_messages(transcript_path, last_save)
        if not _has_meaningful_updates(unsaved_messages):
            _log(f"SKIPPING SAVE at exchange {exchange_count}: low-signal window")
            _output({})
            return

        # Update last save point
        try:
            last_save_file.write_text(str(exchange_count))
        except OSError:
            pass

        _log(f"TRIGGERING SAVE at exchange {exchange_count}")

        # Optional: auto-ingest if MEMPAL_DIR is set
        _maybe_auto_ingest()
        _maybe_sync_obsidian()

        _output({"decision": "block", "reason": STOP_BLOCK_REASON})
    else:
        _output({})


def hook_session_start(data: dict, harness: str):
    """Session start hook: initialize session tracking state."""
    parsed = _parse_harness_input(data, harness)
    session_id = parsed["session_id"]

    _log(f"SESSION START for session {session_id}")

    # Initialize session state directory
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    # Pass through — no blocking on session start
    _output({})


def hook_precompact(data: dict, harness: str):
    """Precompact hook: always block with comprehensive save instruction."""
    parsed = _parse_harness_input(data, harness)
    session_id = parsed["session_id"]

    _log(f"PRE-COMPACT triggered for session {session_id}")

    # Optional: auto-ingest synchronously before compaction (so memories land first)
    mempal_dir = os.environ.get("MEMPAL_DIR", "")
    if mempal_dir and os.path.isdir(mempal_dir):
        try:
            log_path = STATE_DIR / "hook.log"
            with open(log_path, "a") as log_f:
                subprocess.run(
                    [sys.executable, "-m", "mempalace", "mine", mempal_dir],
                    stdout=log_f,
                    stderr=log_f,
                    timeout=60,
                )
        except OSError:
            pass

    # Always block -- compaction = save everything
    _output({"decision": "block", "reason": PRECOMPACT_BLOCK_REASON})


def run_hook(hook_name: str, harness: str):
    """Main entry point: read stdin JSON, dispatch to hook handler."""
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        _log("WARNING: Failed to parse stdin JSON, proceeding with empty data")
        data = {}

    hooks = {
        "session-start": hook_session_start,
        "stop": hook_stop,
        "precompact": hook_precompact,
    }

    handler = hooks.get(hook_name)
    if handler is None:
        print(f"Unknown hook: {hook_name}", file=sys.stderr)
        sys.exit(1)

    handler(data, harness)
