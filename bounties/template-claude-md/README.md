# CLAUDE.md Template: Next.js + SQLite SaaS

An opinionated, production-ready `CLAUDE.md` for a SaaS project built with Next.js 15 App Router and SQLite (better-sqlite3 or Turso).

## Usage

1. Start a new Next.js + SQLite project
2. Copy `CLAUDE.md` to the project root
3. Open in Claude Code
4. Claude understands your project context without asking clarifying questions

## What's Included

Every section has a reason:

| Section | Why It Exists |
|---------|---------------|
| Stack & Versions | Prevents Claude from suggesting wrong APIs (React 18 vs 19, etc.) |
| Dev Commands | So Claude can run correct commands without guessing |
| Folder Structure | So Claude creates files in the right place |
| Database Rules | SQLite has quirks (booleans as integers, no real joins). This prevents bugs. |
| Component Patterns | App Router has specific patterns. This avoids Pages Router confusion. |
| API Route Pattern | Shows the exact pattern to follow |
| What We Don't Do | Prevents Claude from suggesting Redux, Prisma, Pages Router, etc. |
| Testing | Standardizes test tooling |
| Git Conventions | Consistent branch/commit naming |

## Design Decisions

- **Drizzle over Prisma:** Faster queries, less generated code, better TypeScript inference
- **better-sqlite3 over Turso for dev:** Zero latency, no network, instant feedback
- **Server Components by default:** App Router best practice, avoids hydration issues
- **Named exports only:** Prevents confusion with default vs named imports
- **No barrel files:** Better tree-shaking, clearer imports, easier to trace
- **Tailwind only:** No CSS-in-JS runtime overhead, consistent styling
- **SQLite booleans as integers:** SQLite has no native boolean type, this is the convention

## Verification

Tested by:
1. Creating a fresh `pnpm create next-app` project
2. Installing better-sqlite3 + drizzle-orm
3. Pasting this CLAUDE.md
4. Asking Claude Code to "create a users table and a registration page"
5. Claude correctly used Drizzle schema, App Router, Server Actions, and SQLite conventions
