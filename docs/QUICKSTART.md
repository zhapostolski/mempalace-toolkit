# Quick Start Guide

## Installation

```bash
pip install mempalace
```

## Initialize Your Palace

```bash
# Start the guided setup
mempalace init ~/projects/your-project

# This will:
# 1. Create your palace at ~/.mempalace/palace
# 2. Set up wings for your projects and team members
# 3. Generate your AAAK bootstrap
```

## Mine Your Data

```bash
# Mine project files (code, docs, notes)
mempalace mine ~/projects/your-project/

# Mine conversation exports (Claude, ChatGPT, Slack)
mempalace mine ~/chats/ --mode convos

# Auto-classify into decisions, milestones, problems
mempalace mine ~/chats/ --mode convos --extract general
```

## Search

```bash
# Search everything
mempalace search "why did we switch to GraphQL"

# Search within a specific wing
mempalace search "auth migration" --wing your-project

# Search within a room
mempalace search "database decision" --room auth-migration
```

## Connect to Your AI

### Claude Code (MCP)

```bash
# Add MemPalace as an MCP server
claude mcp add mempalace -- python -m mempalace.mcp_server

# Restart Claude Code
# Now your AI can search your palace automatically
```

### Use the wake-up command

```bash
# Load critical facts into your AI's context
mempalace wake-up > context.txt

# Paste context.txt into your AI's system prompt
```

## Next Steps

- Read the [Full Documentation](README.md)
- Learn about [AAAK compression](README.md#aaak-dialect-experimental)
- Set up [Auto-Save Hooks](README.md#auto-save-hooks)
- Explore the [Knowledge Graph](README.md#knowledge-graph)

---

For help, join our [Discord](https://discord.com/invite/ycTQQCu6kn).
