# CLAUDE.md — Next.js + SQLite SaaS

> Opinionated project context for Claude Code. Paste into your project root.

## Stack & Versions

- **Runtime:** Node.js 22+ (ESM)
- **Framework:** Next.js 15 (App Router, `src/app/`)
- **Language:** TypeScript (strict mode)
- **Database:** SQLite via `better-sqlite3` (local dev) or Turso (production)
- **ORM:** Drizzle ORM (`drizzle-orm`)
- **Styling:** Tailwind CSS v4
- **Auth:** NextAuth.js v5 (or Lucia)
- **Deployment:** Vercel

## Dev Commands

```bash
pnpm install          # Install deps (use pnpm, not npm/yarn)
pnpm dev              # Start dev server on :3000
pnpm build            # Production build
pnpm lint             # ESLint
pnpm db:generate      # Generate Drizzle migration from schema
pnpm db:migrate       # Run pending migrations
pnpm db:studio        # Open Drizzle Studio (DB GUI)
```

## Folder Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth route group (login, register)
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (dashboard)/       # Protected route group
│   │   ├── layout.tsx     # Dashboard layout with sidebar
│   │   ├── page.tsx       # Dashboard home
│   │   └── settings/
│   ├── api/               # API routes
│   │   └── [...]/route.ts # Each file exports GET, POST, etc.
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Landing page
├── components/
│   ├── ui/                # Shadcn/ui primitives (Button, Input, etc.)
│   └── features/          # Feature-specific components
├── lib/
│   ├── db.ts              # Database connection singleton
│   ├── auth.ts            # Auth configuration
│   └── utils.ts           # Shared utilities (cn, formatDate, etc.)
├── db/
│   ├── schema.ts          # Drizzle schema definitions (single file)
│   ├── migrations/        # Generated SQL migrations
│   └── seed.ts            # Seed script for dev data
└── types/
    └── index.ts           # Shared TypeScript types
```

## Database Rules

1. **All schema changes go in `src/db/schema.ts`**. Never write raw SQL migrations by hand. Run `pnpm db:generate` to create them.
2. **Use Drizzle's query builder**, not raw SQL. This ensures type safety.
3. **Every table has:**
   - `id` (text, primary key, `cuid2`)
   - `createdAt` (integer, Unix timestamp, default `sql`(strftime('%s','now'))`)
   - `updatedAt` (integer, Unix timestamp, updated on every write)
4. **Migrations are one-way.** Never edit a generated migration file. If you need to change it, create a new migration.
5. **Use transactions** for multi-step writes: `db.transaction(async (tx) => { ... })`.
6. **Boolean fields** are stored as integers (0/1) in SQLite. Use `{ type: "integer", mode: "boolean" }` in Drizzle schema.
7. **No ORM-level joins in API routes.** Prefer separate queries and compose in code. Joins are fine for list pages.

## Component Patterns

1. **Server Components by default.** Only add `"use client"` when you need:
   - `useState`, `useEffect`, or other hooks
   - Event handlers (`onClick`, `onChange`)
   - Browser APIs (`localStorage`, `window`)
2. **Data fetching** happens in Server Components or API routes. Never fetch in a client component.
3. **Forms** use Server Actions (`"use server"`), not API routes.
4. **Naming:**
   - Pages: `page.tsx`
   - Layouts: `layout.tsx`
   - Loading states: `loading.tsx`
   - Error boundaries: `error.tsx`
   - Components: PascalCase (e.g., `UserCard.tsx`)
5. **Props:** Define inline types, not separate interfaces.
   ```tsx
   function UserCard({ name, email }: { name: string; email: string }) { ... }
   ```
6. **Styling:** Use Tailwind classes only. No CSS modules, no styled-components. Use `cn()` from `lib/utils` for conditional classes.

## API Route Pattern

```typescript
// src/app/api/users/route.ts
import { NextResponse } from "next/server";
import { db } from "@/lib/db";
import { users } from "@/db/schema";
import { auth } from "@/lib/auth";

export async function GET() {
  const session = await auth();
  if (!session) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  
  const result = await db.select().from(users);
  return NextResponse.json(result);
}

export async function POST(request: Request) {
  const body = await request.json();
  // Validate with zod
  // Insert with db.insert()
  return NextResponse.json({ success: true }, { status: 201 });
}
```

## What We Don't Do (And Why)

- **No Redux/Zustand.** Server state lives in the database. Client state stays minimal. If you need global client state, use React Context.
- **No serverless databases in dev.** SQLite locally, Turso in prod. No Neon, no Supabase. Keeps dev fast.
- **No `/pages` directory.** App Router only. No mixing.
- **No `getServerSideProps` or `getStaticProps`.** Those are Pages Router concepts.
- **No default exports for components.** Use named exports everywhere.
- **No barrel files (`index.ts` re-exports).** Import directly from the file.
- **No `.env.local` commits.** Use `.env.example` with placeholder values.
- **No Prisma.** Drizzle is the ORM. Prisma generates too much code and has slower queries.
- **No `any` type.** If TypeScript can't infer, add a proper type.

## Testing

```bash
pnpm test              # Run tests with Vitest
pnpm test:watch        # Watch mode
pnpm test:e2e          # Playwright E2E tests
```

- **Unit tests** go next to the file: `utils.test.ts` next to `utils.ts`
- **E2E tests** go in `e2e/` at project root
- Use `vitest` for unit, `playwright` for E2E
- Mock the database in unit tests, use real SQLite file in E2E

## Git Conventions

- **Branch naming:** `feat/short-description`, `fix/short-description`
- **Commit messages:** Conventional commits (`feat:`, `fix:`, `chore:`)
- **PRs:** Squash merge into main
