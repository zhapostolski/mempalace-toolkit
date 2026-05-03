# MemPalace File Formats and Best Practices

## Drawer File Format

All drawer files in MemPalace should use **Markdown (`.md`)** extension.

### Why `.md`?

1. **AI Agent Optimization**: All major AI coding agents (Claude, Codex, Gemini, Qwen) parse and understand Markdown significantly better than plain text
2. **Consistency**: All existing mempalace entries use `.md` (see `hooks/` directory for examples)
3. **Better Search**: Pattern matching and grep operations work more effectively with `.md` files
4. **Readability**: Markdown provides better structure for humans to read and edit

### Example Drawer File Structure

```markdown
# DRAWER: Subpath Routing Implementation Complete

**Date**: 2026-05-03 14:36 UTC  
**Status**: ✅ VERIFIED WORKING

## Summary

Brief overview of what was accomplished.

## Technical Details

Detailed implementation notes, code snippets, configuration examples.

## Verification

Test results, verification steps, and evidence that it works.

## Next Steps

Follow-up actions or known limitations.
```

### File Naming Convention

- Use descriptive names with dates: `YYYY-MM-DD_topic_description.md`
- Include unique identifier if needed to avoid collisions: `topic_description_abc123.md`
- Example patterns:
  - `SESSION_2026-05-03_subpath_routing_complete.md`
  - `subpath_routing_complete_74f47a56.md`
  - `FEATURE_oauth_integration_design.md`

## Wing Configuration

### Cross-Project, Cross-Agent Usage

MemPalace is designed to work as a **unified, shared memory** across all projects and AI agents from a single instance at `~/.mempalace/`.

### Adding New Wings

To add a new wing for your project:

1. Create wing directory: `mkdir -p ~/.mempalace/palace/<wing-name>`
2. Add wing configuration to `~/.mempalace/palace/mempalace.yaml`:
   ```yaml
   wing: <wing-name>
   rooms:
     - name: infrastructure
       description: AWS, networking, infrastructure
     - name: database
       description: Database schemas, migrations
     - name: general
       description: General notes
   ```
3. Create room directories: `mkdir -p ~/.mempalace/palace/<wing-name>/<room-name>`
4. Add drawer files to rooms

### Example: ananas-os Wing

```yaml
# ~/.mempalace/palace/mempalace.yaml
wing: ananas-os
rooms:
  - name: infrastructure
    description: AWS EC2, RDS, networking
  - name: database
    description: Database schema, migrations
  - name: deployment
    description: Deployment status, EC2 setup
  - name: decisions
    description: Key architectural decisions
  - name: agents
    description: AI agents, MCP tools
  - name: general
    description: General notes
```

## Troubleshooting

### "Transaction within a transaction" Error

**Symptom**: MCP tools return error "cannot start a transaction within a transaction"

**Cause**: A previous mempalace MCP server process (PID) has an uncommitted database transaction, blocking new connections.

**Solution**:
```bash
# 1. Find the hanging process
ps aux | grep mempalace.mcp_server

# 2. Kill the process (replace PID with actual number)
kill <PID>

# 3. Restart the MCP server (automatic in most cases)
# New process will start on next MCP tool call
```

**Prevention**: This typically happens when:
- Multiple Claude Code sessions are running simultaneously
- The session was terminated abnormally (Ctrl+C, kill -9)
- The system crashed or ran out of memory

### Wing Not Found

**Symptom**: MCP tools can't find the expected wing directory

**Solution**:
```bash
# Create the wing directory
mkdir -p ~/.mempalace/palace/<wing-name>

# Ensure mempalace.yaml is configured
cat > ~/.mempalace/palace/mempalace.yaml << EOF
wing: <wing-name>
rooms:
  - name: general
    description: General notes
EOF
```

### Database Lock Issues

**Symptom**: Unable to read/write to knowledge graph

**Solution**:
```bash
# Check for active processes
lsof ~/.mempalace/knowledge_graph.sqlite3

# If a process is holding the lock, kill it
kill <PID>

# Remove WAL/SHM files (Safe if no active connections)
rm -f ~/.mempalace/knowledge_graph.sqlite3-wal
rm -f ~/.mempalace/knowledge_graph.sqlite3-shm
```

## Best Practices

### For Users

1. **Use `.md` files** - Your drawer files should always have `.md` extension
2. **Organize by wing/room** - Use the MemPalace structure (wings → rooms → drawers)
3. **Name descriptively** - Include dates and topics in filenames
4. **One topic per drawer** - Keep memories atomic and focused
5. **Run `mempalace mine`** - After manual edits, run `mempalace mine <dir>` to update vector index

### For Developers

1. **Follow existing patterns** - Look at `hooks/*.md` for examples
2. **No code changes needed** - The system works with any markdown files
3. **Test cross-agent** - Verify your changes work with multiple AI tools
4. **Document edge cases** - Add troubleshooting sections for known issues

## Related Documentation

- [README.md](../README.md) - Main project overview
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- [hooks/README.md](../hooks/README.md) - Auto-save hook configuration
- [CHANGELOG.md](../CHANGELOG.md) - Version history
