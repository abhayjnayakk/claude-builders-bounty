# CHANGELOG Generator Skill

A Claude Code skill that generates a structured CHANGELOG from git history.

## Installation

Copy `changelog-skill.md` to your `.claude/skills/` directory or paste into your `CLAUDE.md`.

## Usage

```
claude "generate a changelog for the last 10 commits"
claude "generate a changelog since v2.1.0"
claude "generate a changelog for the last 30 days"
```

## What It Does

1. Runs `git log` with structured format
2. Categorizes commits by type (feat, fix, docs, refactor, etc.)
3. Groups into Keep a Changelog sections: Added, Changed, Fixed, Deprecated, Removed, Security
4. Outputs a clean Markdown CHANGELOG entry

## Example Output

```markdown
## [Unreleased] - 2026-05-04

### Added
- User authentication with OAuth2 support (#142)
- Export dashboard data as CSV (#138)

### Fixed
- Memory leak in WebSocket connection handler (#145)
- Incorrect timezone handling in scheduling module (#139)

### Changed
- Upgraded database driver to v3.2.0 (#144)
- Improved error messages for API validation (#141)

### Deprecated
- `utils.old_formatter()` - use `utils.format()` instead (#140)
```

## Skill Prompt

See `changelog-skill.md` for the full skill definition that teaches Claude Code how to generate changelogs following this format.
