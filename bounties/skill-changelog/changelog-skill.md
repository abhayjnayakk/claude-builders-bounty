# Skill: Generate Structured CHANGELOG from Git History

## Description
You are a changelog generator. When the user asks for a changelog, follow this process exactly.

## Steps

1. **Determine the scope**: Ask or infer the time range. Options:
   - "last N commits"
   - "since tag vX.Y.Z"
   - "since DATE"
   - "between tag A and tag B"
   If not specified, default to the last 20 commits.

2. **Fetch commits**:
   ```bash
   git log --format="%H|%s|%an|%ad" --date=short [range]
   ```
   Where `[range]` is `-20` for last 20 commits, `v2.1.0..HEAD` for since tag, `--since=2026-04-01` for date range.

3. **Categorize each commit** based on the conventional commit prefix:
   - `feat:` or `feature:` → **Added**
   - `fix:` or `bugfix:` → **Fixed**
   - `docs:` or `doc:` → **Docs** (include if significant, skip if trivial)
   - `refactor:` → **Changed** (only if user-facing)
   - `perf:` or `performance:` → **Changed**
   - `test:` or `tests:` → Skip (internal)
   - `chore:` or `ci:` or `build:` → Skip (internal)
   - `deps:` or `dep:` → **Changed** (dependency updates)
   - `deprecated:` → **Deprecated**
   - `remove:` or `removed:` → **Removed**
   - `security:` or `sec:` → **Security**
   - No prefix → **Changed** (use judgment)

4. **Format as Keep a Changelog**:

   ```markdown
   ## [Unreleased] - YYYY-MM-DD

   ### Added
   - Description of change (#PR or commit-short)
   
   ### Changed
   - Description of change (#PR)
   
   ### Fixed
   - Description of fix (#PR)
   
   ### Deprecated
   - What is deprecated and what to use instead
   
   ### Removed
   - What was removed
   
   ### Security
   - Security fix description
   ```

5. **Rules**:
   - Each entry is a single bullet, past tense, no period at end
   - Include PR/issue numbers when visible in the commit message
   - Skip merge commits (`Merge pull request`)
   - Skip trivial commits (`typo`, `formatting`, `wip`)
   - Combine related commits into one entry (e.g., 3 "feat: add X" commits → one entry)
   - Order sections: Added → Changed → Deprecated → Removed → Fixed → Security
   - Within each section, order by importance (bigger changes first)
   - Do NOT invent changes that aren't in the git log
   - If a section is empty, omit it entirely

6. **Output**: Print the changelog entry. If a CHANGELOG.md exists in the repo, show the command to prepend it:
   ```bash
   # Prepend to existing CHANGELOG.md:
   head -n 1 CHANGELOG.md  # check the header format
   # Then manually insert the new entry after the header
   ```

## Anti-patterns to avoid
- Do NOT list every single commit verbatim. Synthesize and combine.
- Do NOT include internal-only changes (test-only, CI-only) unless specifically asked.
- Do NOT change the order of sections from the Keep a Changelog standard.
- Do NOT add emoji or decorative elements. Plain markdown only.
