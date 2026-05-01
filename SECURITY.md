# Security Policy

## Local-First by Design

MemPalace Toolkit is a **local-first deployment automation** tool. All data stays on your machine:

- No network requests by default
- No cloud syncing unless you configure it
- No API calls without explicit environment variables
- SQLite/ChromaDB databases live in `~/.mempalace/palace/`

## Reporting Vulnerabilities

For security issues related to the **hook automation scripts** or **configuration**:

1. Open a [private security advisory](https://github.com/zhapostolski/mempalace-toolkit/security/advisories)
2. Or email: (add your email if you want)

For issues with the **core MemPalace library** (not the toolkit), report upstream at https://github.com/MemPalace/mempalace/security

## Best Practices

### Protect Your Palace

Your memory palace contains conversations, decisions, and potentially sensitive project data:

```bash
# Backup regularly
tar -czf mempalace-backup-$(date +%Y%m%d).tar.gz ~/.mempalace/palace/

# Encrypt sensitive palaces
gpg -c ~/.mempalace/palace/chromadb.sqlite3
```

### Environment Variables

Never commit `.env` files with credentials:

```bash
# Good
SUPABASE_URL="${SUPABASE_URL}"

# Bad (don't hardcode)
SUPABASE_URL="https://abc123.supabase.co"
```

### Hook Security

The automation script (`setup_multi_session_hooks.sh`) only:
- Reads existing config files
- Appends hook configurations
- Does NOT modify system files
- Does NOT download external code

Review the script before running:
```bash
cat hooks/setup_multi_session_hooks.sh
```

## Audit Log

- `~/.mempalace/hook_state/hook.log` — Auto-save history
- `~/.mempalace/palace/knowledge_graph.sqlite3` — Entity relationships

Review these periodically for any unexpected memory writes.

---

**Last updated**: 2026-05-01
