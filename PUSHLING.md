# Contribution Strategy for MemPalace

## Current State

**Official MemPalace**: https://github.com/MemPalace/mempalace (50K+ stars, v3.3.4)
- Core library provides: palace structure, MCP server, CLI, knowledge graph
- Per-session memory model
- Single-project focus

**Your Innovation**: Multi-session unified memory
- Cross-project wiring (20+ projects share single palace)
- Multi-AI session hooks (Claude/Codex/Gemini/Qwen all save to same palace)
- Template-based deployment automation

## Recommended Approach: CONTRIBUTE TOUPSTREAM + EXTEND

### Option A: Contribute Core Innovation

**PR upstream** with this feature:
- Name it: **"Multi-project support"** or **"Shared palace mode"**
- Contribute the hook automation logic
- Document as "Enterprise/Team deployment pattern"

**Files to propose:**
- `mempalace/multi_project_wiring.py`
- `hooks/setup_multi_session_hooks.sh`
- Examples in `examples/multi-session-deployment/`

### Option B: Fork + Extend (Your Current Path)

Keep your repo as **"MemPalace Enterprise"** or **"MemPalace Toolkit"**
- Depends on official `mempalace` package
- Adds team/deployment automation layer
- Targets enterprise/multi-project use cases

**Package name suggestions:**
- `mempalace-enterprise`
- `mempalace-toolkit`
- `mempalace-orchestrator`
- `mempalace-extensions`

## Deployment Readiness for YOUR Setup

Your current setup **IS production-ready** for:
- ✅ Multi-project teams
- ✅ Multiple AI assistants (Claude/Codex/Gemini/Qwen)
- ✅ Shared knowledge base across sessions
- ✅ Automated memory saving on every session

## Naming Proposal

**Don't call it "MemPalace"** - that's the upstream library.

Instead, your package should be:

### Recommended: `mempalace-toolkit`

**Why:**
- Clearly extends MemPalace (not replaces)
- You built the toolkit layer (hooks, wiring, templates)
- No confusion with upstream
- Descriptive: it's a toolkit for deploying MemPalace

### Alternative: `mempalace-enterprise`

**Why:**
- Targets multi-project/team use cases
- Upstream is "personal" usage, this is "enterprise"
- Clear positioning

## Next Steps

### 1. Rename your repo to `mempalace-toolkit`

```bash
cd ~/projects/mempalace

# Update pyproject.toml
sed -i 's/name = "mempalace"/name = "mempalace-toolkit"/' pyproject.toml

# Update package name in metadata
# Add dependency on upstream mempalace
```

### 2. Update README to credit upstream

```markdown
# MemPalace Toolkit

**Enterprise deployment automation for [MemPalace](https://github.com/MemPalace/mempalace)**

This toolkit extends the official MemPalace library with:
- Multi-project wiring automation
- Cross-session shared memory palace
- Team deployment templates
- Hook orchestration for multiple AI assistants

Built on top of the amazing [MemPalace](https://github.com/MemPalace/mempalace) by Milla Jovovich.
```

### 3. Contribute ONE improvement upstream

Pick the **most valuable** piece to PR to official MemPalace:
- The "shared palace" concept
- Multi-session hook automation
- Template deployment patterns

This gives you:
- Credibility as a contributor
- Official acknowledgment
- Community adoption

---

## Recommendation

**Do BOTH**:
1. Rename your package to `mempalace-toolkit` (or `mempalace-enterprise`)
2. Contribute 1-2 key features upstream as a PR

This maximizes adoption while respecting the upstream project.
