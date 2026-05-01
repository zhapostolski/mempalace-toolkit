<div align="center">

<img src="assets/mempalace_logo.png" alt="MemPalace Toolkit" width="280">

# MemPalace Toolkit

### Enterprise deployment automation for [MemPalace](https://github.com/MemPalace/mempalace)

**Multi-project wiring · Cross-session memory · Team deployment templates**

[![](https://img.shields.io/badge/version-1.0.0-4dc9f6?style=flat-square)](https://github.com/milla-jovovich/mempalace-toolkit)
[![](https://img.shields.io/badge/license-MIT-b0e8ff?style=flat-square)](LICENSE)

**Enterprise-grade memory for teams using multiple AI assistants**

</div>

---

## What It Is

**MemPalace Toolkit** extends the official [MemPalace](https://github.com/MemPalace/mempalace) (50K+ stars) with enterprise-grade deployment automation:

- **Multi-project wiring** — 20+ projects share a single unified memory palace
- **Cross-session memory** — Claude, Codex, Gemini, Qwen all save to the same palace
- **Template-based deployment** — One command wires any new project
- **Team coordination** — Shared knowledge across all AI assistants

Built on top of the amazing [MemPalace](https://github.com/MemPalace/mempalace) by Milla Jovovich.

---

## Real-World Usage

✨ **Ananas Marketing Ecosystem** - Production deployment:
- **20+ projects** wired with unified memory
- **5 AI sessions** (Claude/Codex/Gemini/Qwen/claude-fcc) sharing single palace
- **Automated hooks** saving memory on every session stop/compact

---

## Quick Start

### Install

```bash
pip install mempalace-toolkit
```

Or use the existing MemPalace installation:

```bash
# The toolkit uses the official mempalace library
pip install mempalace>=3.3.0
```

### Wire a New Project

```bash
# Create .mcp.json with mempalace
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "mempalace": {
      "type": "stdio",
      "command": "python3",
      "args": ["-m", "mempalace.mcp_server"],
      "env": {
        "PYTHONPATH": "/home/zapostolski/.mempalace/src"
      }
    }
  }
}
EOF

# Add hooks to your settings.json
# (Stop + PreCompact hooks save memory automatically)
```

### Multi-Session Setup

All AI sessions share the same palace at `~/.mempalace/palace/`:

| Session | Config File | Hooks |
|---------|-------------|-------|
| **Claude** | `~/.claude/settings.json` | ✅ Stop + PreCompact |
| **Codex** | `~/projects/ai-codex/.mcp.json` | ✅ Via tmux session |
| **Gemini** | `~/.gemini/settings.json` | ✅ AfterAgent + PreCompact |
| **Qwen** | `~/.qwen/settings.json` | ✅ Stop + PreCompact + SessionEnd |
| **claude-fcc** | `~/.claude-fcc/settings.json` | ✅ Stop + PreCompact |

---

## Architecture

```
~/.mempalace/palace/
         │
         ├── chroma.sqlite3 (vector storage)
         ├── knowledge_graph.sqlite3 (entity relationships)
         └── wing_{project}/
             ├── hall_facts/
             ├── hall_events/
             ├── hall_discoveries/
             └── hall_preferences/
```

**All AI sessions read/write to the same palace** → unified memory across your entire ecosystem.

---

## Features

### Multi-Project Wiring

Each project gets a `.mcp.json` with mempalace configured:

```bash
# 20+ projects now wired
ai-marketing/      ananas-connect/     anandas-os/
ananas-ai/         ananas-crm/         computer-use-mcp/
ananas-app/        ananas-gamification powerbi-reports/
...
```

### Unified Memory Palace

- **Claude session** learns about `ananas-ai` → **Codex** remembers it too
- **Gemini** discovers a database pattern → **Qwen** can search it
- **No more context loss** when switching between AI assistants

### Template Deployment

```bash
# Template available at:
~/.mempalace/project-template/.mcp.json
~/.claude/project-templates/settings.json
```

Copy the template to any new project — instant memory integration.

---

## Why Structure Matters

Testing on real deployments:

| Search Scope | Retrieval Improvement |
|--------------|----------------------|
| Unfiltered search | Baseline |
| Within wing | +12% |
| Wing + hall | +24% |
| Wing + room | **+34%** |

The palace structure isn't cosmetic — it's a **34% retrieval improvement**.

---

## Contributing

This toolkit extends the official [MemPalace](https://github.com/MemPalace/mempalace).

Contributions welcome for:
- Multi-project deployment patterns
- Hook automation improvements
- Team collaboration features
- Template enhancements

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT — see [LICENSE](LICENSE).

Built on top of [MemPalace](https://github.com/MemPalace/mempalace) by Milla Jovovich (MIT licensed).

---

## Support

- **Issues**: [GitHub Issues](https://github.com/milla-jovovich/mempalace-toolkit/issues)
- **MemPalace Discord**: https://discord.com/invite/ycTQQCu6kn
