#!/usr/bin/env python3
"""
Claude Code pre-tool-use hook that blocks destructive bash commands.

Installation:
  1. Copy to ~/.claude/hooks/pre-tool-use-block-destructive.py
  2. chmod +x ~/.claude/hooks/pre-tool-use-block-destructive.py
  3. Add to ~/.claude/settings.json under hooks.pre-tool-use

Blocks: rm -rf, DROP TABLE, TRUNCATE, DELETE FROM without WHERE,
        git push --force, git clean -fdx, dd to disk, fork bombs, chmod/chown on /
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

BLOCKED_LOG = os.path.expanduser("~/.claude/hooks/blocked.log")
PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

# Dangerous patterns - each is a (regex, reason) tuple
DANGEROUS_PATTERNS = [
    # rm -rf variants
    (r'\brm\s+.*-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\s+/(?:\s|$)', "rm -rf on root directory"),
    (r'\brm\s+.*-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\s+/(?:\s|$)', "rm -rf on root directory"),
    (r'\brm\s+-rf\s+~(?:\s|$)', "rm -rf on home directory"),
    (r'\brm\s+-rf\s+\*(?:\s|$)', "rm -rf * in current directory"),
    (r'\brm\s+-rf\s+\.(?:\s|$)', "rm -rf . current directory"),
    (r'\brm\s+--no-preserve-root', "rm with --no-preserve-root"),
    
    # SQL destruction
    (r'\bDROP\s+TABLE\b', "DROP TABLE destroys data"),
    (r'\bDROP\s+DATABASE\b', "DROP DATABASE destroys data"),
    (r'\bTRUNCATE\s+TABLE\b', "TRUNCATE empties a table"),
    (r'\bTRUNCATE\s+\w+', "TRUNCATE empties a table"),
    (r'\bDELETE\s+FROM\s+\w+\s*;', "DELETE FROM without WHERE clause"),
    (r'\bDELETE\s+FROM\s+\w+\s*$', "DELETE FROM without WHERE clause"),
    
    # Git force push
    (r'\bgit\s+push\s+.*--force', "git push --force overwrites remote history"),
    (r'\bgit\s+push\s+-f\b', "git push -f overwrites remote history"),
    (r'\bgit\s+push\s+\+\w+', "git push with + forces overwrite"),
    
    # Git clean
    (r'\bgit\s+clean\s+.*-[a-zA-Z]*f[a-zA-Z]*d[a-zA-Z]*x', "git clean -fdx removes all untracked files"),
    
    # Disk destruction
    (r'\bdd\s+.*of=/dev/[sh]d', "dd writing directly to disk device"),
    
    # Fork bomb
    (r':\(\)\{\s*:\|:&\s*\};:', "Fork bomb detected"),
    (r'\(\)\{\s*\(\)\|&\s*\};\s*\(\)', "Fork bomb variant"),
    
    # Permission destruction
    (r'\bchmod\s+-R\s+777\s+/', "chmod 777 on root destroys permissions"),
    (r'\bchown\s+-R\s+\S+\s+/', "chown -R on root changes all ownership"),
    
    # Package manager uninstall all
    (r'\bapt(?:-get)?\s+remove\s+.*\*', "apt remove with wildcard"),
    (r'\byum\s+remove\s+.*\*', "yum remove with wildcard"),
    (r'\bpip\s+uninstall\s+-y\s+\*', "pip uninstall all packages"),
]


def log_blocked(command: str, reason: str):
    """Log a blocked command attempt."""
    os.makedirs(os.path.dirname(BLOCKED_LOG), exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(BLOCKED_LOG, "a") as f:
        f.write(f"{timestamp} | BLOCKED | {reason} | {command} | {PROJECT_DIR}\n")


def check_command(command: str) -> tuple[bool, str]:
    """Check if a command is dangerous. Returns (is_dangerous, reason)."""
    # Normalize whitespace
    normalized = " ".join(command.split())
    
    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True, reason
    
    return False, ""


def main():
    try:
        # Read the tool use input from stdin
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # Can't parse input, allow through
        sys.exit(0)
    
    # Extract the command from the Bash tool input
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)
    
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")
    
    if not command:
        sys.exit(0)
    
    is_dangerous, reason = check_command(command)
    
    if is_dangerous:
        log_blocked(command, reason)
        
        # Return blocked response
        response = {
            "decision": "block",
            "reason": f"Blocked destructive command: {reason}. The command '{command}' was prevented from executing to protect your system. If you really need to run this, please confirm with the user first."
        }
        print(json.dumps(response))
        sys.exit(0)
    
    # Allow through - no output needed
    sys.exit(0)


if __name__ == "__main__":
    main()
