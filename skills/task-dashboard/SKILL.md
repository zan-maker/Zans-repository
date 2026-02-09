# OpenClaw Task Dashboard — Self-Hosted Open-Source Spec

A Trello-style Kanban board that syncs with your OpenClaw agent. No vendor lock-in — runs entirely on your own infrastructure using open-source tools.

---

## Architecture Overview

```
┌─────────────┐     HTTP/REST      ┌──────────────┐     SQL      ┌──────────────┐
│  OpenClaw    │ ──────────────────▶│  API Server   │────────────▶│  Database     │
│  Agent       │   X-API-Key auth   │  (Hono/Express│             │  (SQLite or   │
│              │                    │   on Deno/Node)│             │   Postgres)   │
└─────────────┘                    └──────┬───────┘             └──────────────┘
                                          │                            ▲
                                          │ WebSocket / SSE            │
                                          ▼                            │
                                   ┌──────────────┐     Direct SQL    │
                                   │  Frontend     │──────────────────┘
                                   │  (React/Vue/  │
                                   │   Svelte)     │
                                   └──────────────┘
```

**Recommended Stack (all open-source, all self-hostable):**

| Layer | Options | Notes |
|---|---|---|
| **Database** | SQLite (simplest, single-file) or PostgreSQL (if you need multi-user/realtime) | SQLite is perfect for single-user Mac Mini deployments |
| **API Server** | Hono + Deno (lightweight, TypeScript) or Express + Node.js or FastAPI + Python | Handles OpenClaw webhook/API calls with auth |
| **Frontend** | React + Vite, Vue + Vite, or Svelte | Static build served by the API server or Caddy/Nginx |
| **Realtime** | WebSocket (built into Hono/Express) or Server-Sent Events (SSE) | For live board updates when OpenClaw creates tasks |
| **Hosting** | Your Mac Mini (localhost) or any VPS | Access via Tailscale for remote |

---

## Database Schema

Works identically on SQLite or PostgreSQL. Adjust syntax as needed.

### Table: `tasks`

```sql
CREATE TABLE tasks (
  id            TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),  -- SQLite UUID alternative
  external_id   TEXT UNIQUE,                                           -- OpenClaw runId (nullable)
  source        TEXT NOT NULL DEFAULT 'manual',                        -- 'manual' or 'openclaw'
  title         TEXT NOT NULL,
  description   TEXT,
  status        TEXT NOT NULL DEFAULT 'queue' 
                CHECK (status IN ('queue', 'in_progress', 'waiting', 'done')),
  priority      INTEGER,                                               -- optional
  tags          TEXT,                                                   -- JSON array as text for SQLite
  created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  updated_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  done_at       TEXT                                                   -- set when status = 'done'
);

CREATE INDEX idx_tasks_external_id ON tasks(external_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_done_at ON tasks(done_at);
```

**PostgreSQL variant** (if you prefer Postgres):

```sql
CREATE TABLE tasks (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  external_id   TEXT UNIQUE,
  source        TEXT NOT NULL DEFAULT 'manual',
  title         TEXT NOT NULL,
  description   TEXT,
  status        TEXT NOT NULL DEFAULT 'queue'
                CHECK (status IN ('queue', 'in_progress', 'waiting', 'done')),
  priority      INTEGER,
  tags          TEXT[],
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  done_at       TIMESTAMPTZ
);

-- Postgres trigger for auto-updating updated_at and done_at
CREATE OR REPLACE FUNCTION tasks_update_trigger() RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  IF NEW.status = 'done' AND (OLD.status IS DISTINCT FROM 'done') THEN
    NEW.done_at = now();
  END IF;
  IF NEW.status != 'done' AND OLD.status = 'done' THEN
    NEW.done_at = NULL;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tasks_before_update
  BEFORE UPDATE ON tasks
  FOR EACH ROW EXECUTE FUNCTION tasks_update_trigger();
```

### Done Rules (enforced in API layer for SQLite, or via trigger for Postgres)

- When `status` changes to `'done'` → set `done_at` to current timestamp
- When `status` changes away from `'done'` → clear `done_at` to null
- Every update sets `updated_at` to current timestamp

---

## API Server

A single-file HTTP server that handles OpenClaw task sync and serves the frontend. Pick your runtime.

### Option A: Hono + Deno (Recommended — Lightweight, TypeScript)

```bash
# Install Deno (if not already)
curl -fsSL https://deno.land/install.sh | sh

# Project structure
mkdir openclaw-dashboard && cd openclaw-dashboard
```

**server.ts:**

```typescript
import { Hono } from "https://deno.land/x/hono/mod.ts";
import { cors } from "https://deno.land/x/hono/middleware.ts";
import { DB } from "https://deno.land/x/sqlite/mod.ts";

const app = new Hono();
const db = new DB("./tasks.db");
const API_KEY = Deno.env.get("DASHBOARD_API_KEY") || "change-me-to-a-strong-random-key";
const PORT = parseInt(Deno.env.get("PORT") || "3000");

// Initialize database
db.execute(`
  CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    external_id TEXT UNIQUE,
    source TEXT NOT NULL DEFAULT 'manual',
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'queue'
      CHECK (status IN ('queue','in_progress','waiting','done')),
    priority INTEGER,
    tags TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    done_at TEXT
  );
  CREATE INDEX IF NOT EXISTS idx_tasks_external_id ON tasks(external_id);
  CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
`);

// CORS
app.use("/api/*", cors({
  origin: "*",
  allowMethods: ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
  allowHeaders: ["Content-Type", "X-API-Key"],
}));

// Auth middleware for /api/openclaw/* routes
const authMiddleware = async (c, next) => {
  const key = c.req.header("X-API-Key")?.trim();
  if (!key || key !== API_KEY) {
    return c.json({ error: "unauthorized" }, 401);
  }
  await next();
};

// Helper: apply done_at rules
function applyDoneRules(task, previousStatus) {
  const now = new Date().toISOString();
  task.updated_at = now;
  if (task.status === "done" && previousStatus !== "done") {
    task.done_at = now;
  }
  if (task.status !== "done" && previousStatus === "done") {
    task.done_at = null;
  }
  return task;
}

// ═══════════════════════════════════════════════
// OpenClaw API routes (authenticated)
// ═══════════════════════════════════════════════

// POST /api/openclaw/tasks — Create or upsert from OpenClaw
app.post("/api/openclaw/tasks", authMiddleware, async (c) => {
  try {
    const body = await c.req.json();
    if (!body.title && !body.external_id) {
      return c.json({ error: "title is required" }, 400);
    }

    const now = new Date().toISOString();

    // Upsert by external_id if provided
    if (body.external_id) {
      const existing = db.queryEntries(
        "SELECT * FROM tasks WHERE external_id = ?", [body.external_id]
      );

      if (existing.length > 0) {
        const old = existing[0];
        const status = body.status || old.status;
        const updates = applyDoneRules({ status }, old.status);

        db.query(
          `UPDATE tasks SET title=?, description=?, status=?, updated_at=?, done_at=?, source='openclaw'
           WHERE external_id=?`,
          [body.title || old.title, body.description ?? old.description,
           updates.status ?? status, updates.updated_at, updates.done_at ?? old.done_at,
           body.external_id]
        );

        const result = db.queryEntries(
          "SELECT * FROM tasks WHERE external_id = ?", [body.external_id]
        );
        return c.json(result[0], 200);
      }
    }

    // Create new
    const id = crypto.randomUUID();
    db.query(
      `INSERT INTO tasks (id, external_id, source, title, description, status, created_at, updated_at)
       VALUES (?, ?, 'openclaw', ?, ?, 'queue', ?, ?)`,
      [id, body.external_id || null, body.title, body.description || null, now, now]
    );

    const result = db.queryEntries("SELECT * FROM tasks WHERE id = ?", [id]);
    return c.json(result[0], 200);
  } catch (e) {
    console.error("POST /api/openclaw/tasks error:", e);
    return c.json({ error: "internal error", detail: e.message }, 500);
  }
});

// PATCH /api/openclaw/tasks — Update by external_id
app.patch("/api/openclaw/tasks", authMiddleware, async (c) => {
  try {
    const body = await c.req.json();
    if (!body.external_id) {
      return c.json({ error: "external_id is required" }, 400);
    }

    const existing = db.queryEntries(
      "SELECT * FROM tasks WHERE external_id = ?", [body.external_id]
    );
    if (existing.length === 0) {
      return c.json({ error: "not found" }, 404);
    }

    const old = existing[0];
    const newStatus = body.status || old.status;
    const updates = applyDoneRules({ status: newStatus }, old.status);

    db.query(
      `UPDATE tasks SET
        title = COALESCE(?, title),
        description = COALESCE(?, description),
        status = ?,
        updated_at = ?,
        done_at = ?
       WHERE external_id = ?`,
      [body.title || null, body.description || null,
       newStatus, updates.updated_at, updates.done_at ?? old.done_at,
       body.external_id]
    );

    const result = db.queryEntries(
      "SELECT * FROM tasks WHERE external_id = ?", [body.external_id]
    );
    return c.json(result[0], 200);
  } catch (e) {
    console.error("PATCH /api/openclaw/tasks error:", e);
    return c.json({ error: "internal error", detail: e.message }, 500);
  }
});

// GET /api/openclaw/tasks?external_id=...
app.get("/api/openclaw/tasks", authMiddleware, async (c) => {
  const externalId = c.req.query("external_id");
  if (!externalId) {
    return c.json({ error: "external_id query param required" }, 400);
  }
  const result = db.queryEntries(
    "SELECT * FROM tasks WHERE external_id = ?", [externalId]
  );
  if (result.length === 0) return c.json({ error: "not found" }, 404);
  return c.json(result[0], 200);
});

// DELETE /api/openclaw/tasks?external_id=...
app.delete("/api/openclaw/tasks", authMiddleware, async (c) => {
  const externalId = c.req.query("external_id");
  if (!externalId) {
    return c.json({ error: "external_id query param required" }, 400);
  }
  const existing = db.queryEntries(
    "SELECT * FROM tasks WHERE external_id = ?", [externalId]
  );
  if (existing.length === 0) return c.json({ error: "not found" }, 404);

  db.query("DELETE FROM tasks WHERE external_id = ?", [externalId]);
  return c.json({ ok: true }, 200);
});

// ═══════════════════════════════════════════════
// Frontend API routes (no auth — local access only)
// ═══════════════════════════════════════════════

// GET /api/tasks — List all tasks
app.get("/api/tasks", (c) => {
  const tasks = db.queryEntries("SELECT * FROM tasks ORDER BY created_at DESC");
  return c.json(tasks);
});

// POST /api/tasks — Manual task creation from UI
app.post("/api/tasks", async (c) => {
  const body = await c.req.json();
  if (!body.title) return c.json({ error: "title required" }, 400);

  const id = crypto.randomUUID();
  const now = new Date().toISOString();
  db.query(
    `INSERT INTO tasks (id, source, title, description, status, created_at, updated_at)
     VALUES (?, 'manual', ?, ?, ?, ?, ?)`,
    [id, body.title, body.description || null, body.status || "queue", now, now]
  );
  const result = db.queryEntries("SELECT * FROM tasks WHERE id = ?", [id]);
  return c.json(result[0], 200);
});

// PATCH /api/tasks/:id — Update from UI (drag-and-drop, edit)
app.patch("/api/tasks/:id", async (c) => {
  const id = c.req.param("id");
  const body = await c.req.json();

  const existing = db.queryEntries("SELECT * FROM tasks WHERE id = ?", [id]);
  if (existing.length === 0) return c.json({ error: "not found" }, 404);

  const old = existing[0];
  const newStatus = body.status || old.status;
  const updates = applyDoneRules({ status: newStatus }, old.status);

  db.query(
    `UPDATE tasks SET
      title = COALESCE(?, title),
      description = COALESCE(?, description),
      status = ?,
      updated_at = ?,
      done_at = ?
     WHERE id = ?`,
    [body.title || null, body.description || null,
     newStatus, updates.updated_at, updates.done_at ?? old.done_at, id]
  );

  const result = db.queryEntries("SELECT * FROM tasks WHERE id = ?", [id]);
  return c.json(result[0], 200);
});

// DELETE /api/tasks/:id — Delete from UI
app.delete("/api/tasks/:id", (c) => {
  const id = c.req.param("id");
  db.query("DELETE FROM tasks WHERE id = ?", [id]);
  return c.json({ ok: true }, 200);
});

// ═══════════════════════════════════════════════
// SSE endpoint for realtime updates
// ═══════════════════════════════════════════════

// Simple polling-based SSE (for SQLite — no native pub/sub)
app.get("/api/tasks/stream", (c) => {
  let lastCheck = new Date().toISOString();

  const stream = new ReadableStream({
    start(controller) {
      const interval = setInterval(() => {
        try {
          const updated = db.queryEntries(
            "SELECT * FROM tasks WHERE updated_at > ? ORDER BY updated_at DESC",
            [lastCheck]
          );
          if (updated.length > 0) {
            lastCheck = new Date().toISOString();
            const data = JSON.stringify(updated);
            controller.enqueue(new TextEncoder().encode(`data: ${data}\n\n`));
          }
        } catch (_) {
          clearInterval(interval);
          controller.close();
        }
      }, 1000); // Poll every second
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
    },
  });
});

// Serve static frontend files
app.get("/*", async (c) => {
  // Serve from ./public/ directory
  const path = c.req.path === "/" ? "/index.html" : c.req.path;
  try {
    const file = await Deno.readFile(`./public${path}`);
    const ext = path.split(".").pop();
    const types = { html: "text/html", js: "application/javascript",
                    css: "text/css", json: "application/json", svg: "image/svg+xml" };
    return new Response(file, {
      headers: { "Content-Type": types[ext] || "application/octet-stream" },
    });
  } catch {
    const file = await Deno.readFile("./public/index.html");
    return new Response(file, { headers: { "Content-Type": "text/html" } });
  }
});

console.log(`Dashboard running at http://localhost:${PORT}`);
Deno.serve({ port: PORT }, app.fetch);
```

**Run:**

```bash
export DASHBOARD_API_KEY="your-strong-random-key-here"
deno run --allow-net --allow-read --allow-write --allow-env server.ts
```

### Option B: Express + Node.js

Same logic, swap Hono for Express and `deno-sqlite` for `better-sqlite3`:

```bash
npm init -y
npm install express better-sqlite3 cors
```

Adapt the routes above using Express syntax. The API contract is identical.

### Option C: FastAPI + Python

```bash
pip install fastapi uvicorn aiosqlite
```

Same API contract. Use `aiosqlite` for async SQLite access.

---

## Frontend Spec

Build with React + Vite (recommended), Vue, or Svelte. Compile to static files in `./public/`.

### Visual Design

Target: **Linear x Notion** aesthetic — clean, minimal, premium. Dark/light mode toggle.

- Monospace or inter font for headers
- Subtle card shadows, rounded corners (8px)
- Smooth drag-and-drop animations (use `@dnd-kit/core` for React or `vue-draggable` for Vue)
- Status pills with muted colors (not bright primary colors)

### Columns (Lanes)

| Lane | Filter | Sort |
|---|---|---|
| **Queue** | `status = 'queue'` | `created_at DESC` |
| **In Progress** | `status = 'in_progress'` | `updated_at DESC` |
| **Waiting** | `status = 'waiting'` | `updated_at DESC` |
| **Done Today** | `status = 'done'` AND `done_at` is today (user's local date) | `done_at DESC` |

Each column header shows counter: `Queue (12)`

### Task Card

```
┌─────────────────────────────────┐
│ 🤖  Run weekly report           │  ← robot badge if source == 'openclaw'
│                                 │
│ Generate the Q4 summary...      │  ← description (truncated to 2 lines)
│                                 │
│ 2m ago              In Progress │  ← relative time + status pill
└─────────────────────────────────┘
```

- Show 🤖 badge when `source == 'openclaw'`
- Click card → opens detail drawer for editing title, description, status
- Drag between lanes → optimistic UI update, then PATCH to API

### Add Task

Button at top of each column or global "+" button. Modal or inline form with:
- Title (required)
- Description (optional)
- Status (dropdown, default: Queue)

### Realtime Updates

Connect to `/api/tasks/stream` via EventSource (SSE). When new data arrives, merge into local state. This ensures tasks created by OpenClaw appear on the board within ~1 second without manual refresh.

```javascript
const source = new EventSource("/api/tasks/stream");
source.onmessage = (event) => {
  const updatedTasks = JSON.parse(event.data);
  // Merge into local state
};
```

---

## OpenClaw Integration

### What to Configure in OpenClaw

Give the agent these connection details (store securely in env vars or encrypted memory, never in chat):

```
BASE_URL: http://localhost:3000/api/openclaw/tasks   (or Tailscale IP if remote)
AUTH_HEADER_NAME: X-API-Key
AUTH_HEADER_VALUE: (stored in env var, never in plaintext config)
STATUS_FLOW: queue → in_progress → waiting → in_progress → done
EXTERNAL_ID_RULE: external_id = runId
```

### System Prompt Addition for OpenClaw

Add to MEMORY.md or system prompt:

```
## Task Dashboard Integration

You have access to a task dashboard API. Use it to track your work.

When starting a new task:
  curl -X POST "$DASHBOARD_URL" \
    -H "X-API-Key: $DASHBOARD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"title":"[task name]","external_id":"[runId]"}'

When updating task status:
  curl -X PATCH "$DASHBOARD_URL" \
    -H "X-API-Key: $DASHBOARD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"external_id":"[runId]","status":"in_progress|waiting|done"}'

Status flow: queue → in_progress → waiting → in_progress → done
Always use your runId as external_id for traceability.
Create a task when starting work. Update to 'done' when complete.
```

### Acceptance Tests (cURL)

**Create task from OpenClaw:**
```bash
curl -X POST "http://localhost:3000/api/openclaw/tasks" \
  -H "X-API-Key: $DASHBOARD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Run report","external_id":"run_123"}'
# → 200 with JSON; source='openclaw', status='queue'
```

**Update status to done:**
```bash
curl -X PATCH "http://localhost:3000/api/openclaw/tasks" \
  -H "X-API-Key: $DASHBOARD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"external_id":"run_123","status":"done"}'
# → 200; status='done', done_at set
```

**Get by external_id:**
```bash
curl -G "http://localhost:3000/api/openclaw/tasks" \
  -H "X-API-Key: $DASHBOARD_API_KEY" \
  --data-urlencode "external_id=run_123"
# → 200 with JSON task (or 404)
```

**Delete:**
```bash
curl -X DELETE "http://localhost:3000/api/openclaw/tasks?external_id=run_123" \
  -H "X-API-Key: $DASHBOARD_API_KEY"
# → 200 { ok: true } (or 404)
```

---

## Deployment Options

### Option 1: Mac Mini (Recommended for Your Setup)

```bash
# Run on localhost, access via Tailscale from phone
export DASHBOARD_API_KEY="$(openssl rand -hex 32)"
deno run --allow-all server.ts

# Auto-start on boot (macOS LaunchAgent)
# Create ~/Library/LaunchAgents/com.openclaw.dashboard.plist
```

Access at `http://100.x.y.z:3000` via Tailscale from any device.

### Option 2: Docker (Portable)

```dockerfile
FROM denoland/deno:latest
WORKDIR /app
COPY . .
RUN deno cache server.ts
EXPOSE 3000
CMD ["deno", "run", "--allow-all", "server.ts"]
```

```bash
docker build -t openclaw-dashboard .
docker run -d -p 3000:3000 \
  -e DASHBOARD_API_KEY="your-key" \
  -v ./data:/app/data \
  openclaw-dashboard
```

### Option 3: VPS ($5/month DigitalOcean/Hetzner)

Same as Mac Mini but behind Tailscale or Cloudflare Tunnel. Never expose port 3000 directly.

---

## Security Notes

- **API key auth** on `/api/openclaw/*` routes only. Frontend routes are unauthenticated (local access via Tailscale).
- **Never expose port 3000 to the public internet.** Use Tailscale or SSH tunnel.
- **Store DASHBOARD_API_KEY in an environment variable**, not in code or config files.
- **SQLite database file** contains all task data. Back it up with your OpenClaw memory backups.
- **CORS is permissive** (`*`) because access is controlled at the network level (Tailscale). Tighten if deploying differently.
- The OpenClaw agent should store the API key in an env var (`$DASHBOARD_API_KEY`), not in MEMORY.md or chat history.

---

## Alternative Open-Source Frontend Frameworks

If you don't want to build from scratch, these open-source Kanban boards can be adapted to use the same API:

| Project | Stack | Notes |
|---|---|---|
| [Planka](https://github.com/plankanban/planka) | React + PostgreSQL | Full Trello alternative. Self-hosted. Would need API adapter for OpenClaw. |
| [WeKan](https://github.com/wekan/wekan) | Meteor + MongoDB | Mature, feature-rich. Heavier stack. |
| [Focalboard](https://github.com/mattermost/focalboard) | React + Go + SQLite | Notion-like. By Mattermost. Supports SQLite. |
| [Vikunja](https://github.com/go-vikunja/vikunja) | Vue + Go + SQLite | Lightweight task manager with Kanban view and REST API. |
| [Nullboard](https://github.com/nicoschmdt/nullboard) | Vanilla JS, single HTML file | Zero-dependency. Store in localStorage or JSON file. Simplest possible option. |

For any of these, you'd add a webhook/API bridge that accepts OpenClaw's POST/PATCH calls and translates them to the platform's native API.

---

## Quick-Start Checklist

1. ☐ Install Deno (or Node.js)
2. ☐ Copy `server.ts` to your project directory
3. ☐ Generate API key: `openssl rand -hex 32`
4. ☐ Set `DASHBOARD_API_KEY` env var
5. ☐ Run server: `deno run --allow-all server.ts`
6. ☐ Test with cURL commands above
7. ☐ Build frontend (React/Vue/Svelte) and place in `./public/`
8. ☐ Configure OpenClaw with BASE_URL and API key
9. ☐ Add task dashboard instructions to agent MEMORY.md or system prompt
10. ☐ Access via Tailscale from phone/laptop

---

*This spec replaces Lovable (proprietary frontend builder) with any open-source frontend framework and Supabase (managed Postgres + Edge Functions) with SQLite + a lightweight Deno/Node API server. The API contract is identical — OpenClaw doesn't care what's behind the endpoint.*
