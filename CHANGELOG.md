# Changelog

All notable changes to MemPalace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Project-wide Mempalace wiring across all Ananas Marketing projects
- Template infrastructure for new project setup
- Centralized memory palace shared across all AI sessions

### Changed
- Breaking: ChromaDB pinned to `>=0.5.0,<0.7`

## [3.0.11] - 2026-04-14

### Fixed
- Pinned ChromaDB version to resolve compatibility issues
- Fixed shell injection vulnerability in hooks (#110)

## [3.0.10] - 2026-04-10

### Added
- Knowledge graph with temporal entity-relationship triples
- AAAK dialect for context compression (experimental)
- Specialist agents with individual wings and diaries

### Changed
- MCP server now teaches AAAK automatically on connect

## [3.0.0] - 2026-04-08

### Added
- Initial release with palace structure (wings, rooms, halls, tunnels)
- 19 MCP tools for palace navigation and management
- Auto-save hooks for Claude Code
- LongMemEval benchmark with 96.6% R@5 score
- Local SQLite-based knowledge graph

### Changed
- Complete rewrite from previous versions
- Switched from flat storage to hierarchical palace model
- Native support for conversation mining (Claude, ChatGPT exports)

---

## [2.x.x] - Legacy (pre-2026)

Previous versions used a different architecture. See the v2 branch for legacy code.

[Unreleased]: https://github.com/milla-jovovich/mempalace/compare/v3.0.11...HEAD
[3.0.11]: https://github.com/milla-jovovich/mempalace/compare/v3.0.10...v3.0.11
[3.0.10]: https://github.com/milla-jovovich/mempalace/compare/v3.0.0...v3.0.10
[3.0.0]: https://github.com/milla-jovovich/mempalace/releases/tag/v3.0.0
