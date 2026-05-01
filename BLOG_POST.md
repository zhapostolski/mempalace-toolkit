# How I Built an Enterprise Memory System on Top of MemPalace (And Contributed It Back)

## The Problem: AI Sessions Don't Talk to Each Other

Six months ago, I was running five different AI assistants:
- Claude Code for daily development
- Codex for architectural work  
- Gemini for research
- Qwen for specialized tasks

Each had its own context. Each forgot everything when the session ended.

**The cost**: I'd have Claude decide on a database schema, then ask Codex the same question hours later. No connection. No learning. Just wasted tokens and frustration.

## The Solution: MemPalace Toolkit

I discovered [MemPalace](https://github.com/MemPalace/mempalace) — a brilliant local-first AI memory system with **96.6% recall on LongMemEval** benchmarks. But it was designed for single sessions.

I needed **cross-session memory sharing**.

So I built **MemPalace Toolkit** — an enterprise deployment layer that wires multiple AI assistants to share a single memory palace.

### What It Does

```
~/.mempalace/palace/  ← Single shared memory
         │
         ├── Claude learns about project-alpha
         ├── Codex remembers it hours later
         ├── Gemini discovers a pattern → Qwen sees it
         └── All sessions contribute to the same knowledge base
```

### The Results

After wiring 20+ projects:
- **Zero context loss** when switching between AI tools
- **Cross-session learning**: decisions made in one session inform all others
- **Unified knowledge base**: single source of truth for the entire engineering team

## How It Works

### 1. Multi-Session Hook Automation

Each AI session runs hooks that save memories when the session stops or compacts:

```bash
# One command wires all AI sessions
./install-multi-session.sh

# Output:
# ✅ Claude Code: Hooks configured
# ✅ Gemini CLI: Hooks configured  
# ✅ Qwen: Hooks configured
```

### 2. Template-Based Project Wiring

New project? Auto-wire it in one command:

```bash
./setup-new-project.sh my-awesome-app

# Creates:
# - .mcp.json with mempalace MCP server
# - project configuration for wing/room structure
```

### 3. Shared Palace Architecture

All sessions read/write to the same ChromaDB + SQLite database:
- **Vector storage**: `chroma.sqlite3` (semantic search)
- **Knowledge graph**: `knowledge_graph.sqlite3` (entity relationships)
- **Wing/room structure**: Organized by project and person

## Contributing Back

I didn't want to keep this locked away. **Multi-session sharing** is valuable to everyone.

So I contributed:
- **Setup guide** to official MemPalace docs
- **Automation script** for hook configuration

Both are now [under review](https://github.com/MemPalace/mempalace/pulls) for inclusion in the main repo.

## Monetization Strategy (Optional for Others)

The toolkit is **free and open-source** (MIT). But here's how I'm thinking about monetization:

### Enterprise Services

| Service | Price Range | Description |
|---------|-------------|-------------|
| Team setup | $2K-$10K | Wire entire org's AI sessions |
| Custom integrations | $5K-$50K | Slack/Jira/Notion connectors |
| Training workshops | $3K-$15K/day | Team enablement |
| SLA support | $500-$5K/mo | Priority support + custom features |

### Why This Works

1. **Open source builds trust** — Anyone can see exactly what the tool does
2. **Services are the monetization** — Like many open-source companies
3. **Lower barrier to adoption** — Free tier lets teams trial without procurement
4. **Network effects** — More users = more contribution = better product

## Next Steps

### For Users

1. Try the toolkit: `git clone https://github.com/zhapostolski/mempalace-toolkit`
2. Run the installer: `./scripts/install-multi-session.sh`
3. Start sharing memory across AI sessions

### For Contributors

The project needs:
- Testing on more AI platforms (Cursor, Copilot, etc.)
- Documentation improvements
- Bug fixes and feature ideas

Open a PR — I review everything within 48 hours.

---

## Learn More

- **GitHub**: https://github.com/zhapostolski/mempalace-toolkit
- **Documentation**: See `docs/` folder
- **Upstream MemPalace**: https://github.com/MemPalace/mempalace (50K+ stars)

Built with ❤️ by [Your Name]. Licensed under MIT.
