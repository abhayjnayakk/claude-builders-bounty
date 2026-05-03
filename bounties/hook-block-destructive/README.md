# Pre-tool-use Hook: Block Destructive Bash Commands

A Claude Code hook that intercepts and blocks dangerous bash commands before execution.

## Installation

```bash
mkdir -p ~/.claude/hooks
cp pre-tool-use-block-destructive.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/pre-tool-use-block-destructive.py
```

Then add to your `~/.claude/settings.json` or project's `.claude/settings.json`:

```json
{
  "hooks": {
    "pre-tool-use": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/pre-tool-use-block-destructive.py"
          }
        ]
      }
    ]
  }
}
```

## What It Blocks

| Pattern | Why |
|---------|-----|
| `rm -rf /` | Destroys entire filesystem |
| `rm -rf ~` | Destroys home directory |
| `rm -rf *` | Destroys current directory |
| `rm -rf .` | Destroys current directory |
| `DROP TABLE` | Destroys database table |
| `DROP DATABASE` | Destroys entire database |
| `TRUNCATE TABLE` | Empties a table |
| `DELETE FROM` without WHERE | Deletes all rows |
| `git push --force` | Overwrites remote history |
| `git push -f` | Same as above |
| `git clean -fdx` | Removes all untracked files |
| `dd if=... of=/dev/sda` | Overwrites disk |
| `:(){ :\|:& };:` | Fork bomb |
| `chmod -R 777 /` | Destroys all permissions |
| `chown -R ... /` | Changes all file ownership |

## How It Works

1. Claude Code calls the hook before executing any `Bash` tool use
2. The hook reads the proposed command from stdin (JSON format)
3. It checks the command against dangerous patterns
4. If blocked, it returns a JSON response telling Claude why the command was rejected
5. If safe, it returns silently (allows execution)
6. Every blocked attempt is logged to `~/.claude/hooks/blocked.log`

## Log Format

```
2026-05-04T03:30:00Z | BLOCKED | rm -rf / | /home/user/project
2026-05-04T03:30:05Z | BLOCKED | DROP TABLE users | /home/user/db-project
```
