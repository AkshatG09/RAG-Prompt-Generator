# React Frontend Implementation Plan — RAG Prompt Generator

## 1. Codebase Analysis Summary

### What This Application Does

This is an **LLM Prompt Generator** — a FastAPI backend that uses Retrieval-Augmented Generation (RAG) to automatically produce optimized LLM prompts. A user provides their professional specialization and a description of what they need, and the system:

1. **Embeds** the user's request via OpenRouter (`nvidia/llama-nemotron-embed-vl-1b-v2:free`)
2. **Retrieves** relevant prompt engineering guidelines from ChromaDB (semantic similarity search, top 3 chunks)
3. **Fetches** the user's last 5 past interactions from MongoDB for conversational context
4. **Generates** a tailored prompt by sending system message (guidelines) + user message (specialization + request + history) to `qwen/qwen3.5-9b` via OpenRouter/LangChain
5. **Persists** the interaction to MongoDB (`rag_prompts_db.conversations`)
6. **Returns** the generated prompt + the retrieved RAG context

### Existing API Surface

| Method | Path | Request Body | Response Body |
|--------|------|-------------|---------------|
| `GET` | `/health` | — | `{ "status": "ok" }` |
| `POST` | `/api/generate` | `PromptRequest` | `PromptResponse` |

**Pydantic Models:**

```python
class PromptRequest(BaseModel):
    user_id: str             # "user_123"
    specialization: str      # "Software Engineer"
    request_description: str # "Generate a prompt to improve technical writing clarity"

class PromptResponse(BaseModel):
    generated_prompt: str                     # The LLM-generated prompt
    retrieved_context_used: list[str] | None  # RAG context chunks (debug)
```

### Current Project Structure

```
RAG-Prompt-Generator/
├── app/
│   ├── main.py          # FastAPI app, lifespan, 2 endpoints
│   ├── services.py      # RAG orchestration, embeddings, LLM calls, MongoDB CRUD
│   ├── models.py        # Pydantic request/response schemas
│   ├── database.py      # MongoDB (motor) + ChromaDB connections
│   └── monitoring.py    # LangChain callback handlers (custom + Langfuse)
├── scripts/
│   ├── ingest.py        # Document ingestion pipeline (txt → chunks → ChromaDB)
│   └── text_file_processing.py
├── source_documents/    # Raw + processed knowledge base documents
├── requirements.txt
├── .env                 # OPENROUTER_API_KEY, MONGO_URI
└── README.md
```

### Backend Tech Stack (DO NOT MODIFY core logic)
- **FastAPI** on uvicorn (port 8000)
- **ChromaDB** — local persistent vector store (`./chroma_db`)
- **MongoDB** — async via motor (`rag_prompts_db` database)
- **OpenRouter** — embeddings + LLM generation
- **LangChain** — ChatOpenAI wrapper + monitoring callbacks

---

## 2. Architecture Overview

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    React Frontend (Vite)                       │
│                                                                │
│  ┌─────────────┐  ┌───────────────┐  ┌──────────────────┐    │
│  │  Generator   │  │   History     │  │    Settings       │    │
│  │  Page        │  │   Page        │  │    Page           │    │
│  └──────┬───────┘  └──────┬────────┘  └──────┬───────────┘    │
│         │                  │                   │                │
│  ┌──────┴──────────────────┴───────────────────┴──────────┐   │
│  │              TanStack Query (Server State)              │   │
│  │        +     Zustand (Client State / Preferences)       │   │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         │                                      │
│  ┌──────────────────────┴──────────────────────────────────┐   │
│  │                   API Client Layer                       │   │
│  │           (fetch wrapper + type-safe calls)              │   │
│  └──────────────────────┬──────────────────────────────────┘   │
└─────────────────────────┼──────────────────────────────────────┘
                          │  HTTP (localhost:5173 → proxy → :8000)
┌─────────────────────────┼──────────────────────────────────────┐
│                    FastAPI Backend                              │
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ /health  │  │ /api/    │  │ /api/    │  │ /api/history │  │
│  │          │  │ generate │  │ history/ │  │ /{id}/delete │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │
│                       │                                        │
│  ┌────────────────────┴────────────────────────────────────┐  │
│  │  services.py (RAG pipeline, embeddings, LLM, MongoDB)   │  │
│  └────────────┬──────────────────────┬─────────────────────┘  │
│               │                      │                         │
│  ┌────────────┴─────┐  ┌────────────┴─────────────────────┐  │
│  │   ChromaDB        │  │   MongoDB (motor async)          │  │
│  │   (Vector Store)  │  │   (Conversation History)         │  │
│  └───────────────────┘  └──────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Tech Stack (Frontend — NEW)

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Build | Vite | 6.x | Dev server, bundling, proxy |
| Framework | React | 19.x | UI library |
| Language | TypeScript | 5.x | Type safety |
| Styling | Tailwind CSS | 4.x | Utility-first CSS |
| Components | shadcn/ui | latest | Accessible component primitives |
| Server State | TanStack Query | 5.x | API caching, mutations, loading states |
| Client State | Zustand | 5.x | User preferences, UI state |
| Routing | React Router | 7.x | Client-side navigation |
| Animations | Framer Motion | 12.x | Page transitions, micro-interactions |
| Markdown | react-markdown + rehype | latest | Render LLM output |
| Icons | Lucide React | latest | Consistent icon set |
| Notifications | Sonner | latest | Toast notifications |
| Forms | React Hook Form + Zod | latest | Validated form handling |

---

## 3. Complete File Tree

```
frontend/
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
├── tailwind.config.ts
├── postcss.config.js
├── components.json                          # shadcn/ui config
├── .env.development                         # VITE_API_BASE_URL=http://localhost:8000
├── .env.production                          # VITE_API_BASE_URL=/api
│
├── public/
│   └── favicon.svg
│
└── src/
    ├── main.tsx                             # React entry point
    ├── App.tsx                              # Root component (providers + router)
    ├── index.css                            # Tailwind directives + global styles
    ├── vite-env.d.ts                        # Vite type declarations
    │
    ├── api/
    │   ├── apiClient.ts                     # Base fetch wrapper with error handling
    │   ├── promptApi.ts                     # generate(), getHistory(), deleteHistory()
    │   └── types.ts                         # TypeScript types mirroring Pydantic models
    │
    ├── hooks/
    │   ├── useGeneratePrompt.ts             # TanStack mutation for POST /api/generate
    │   ├── usePromptHistory.ts              # TanStack query for GET /api/history/:userId
    │   ├── useDeleteHistory.ts              # TanStack mutation for DELETE endpoint
    │   ├── useHealthCheck.ts                # TanStack query for GET /health
    │   └── useCopyToClipboard.ts            # Clipboard utility hook
    │
    ├── stores/
    │   ├── useUserStore.ts                  # userId, defaultSpecialization, preferences
    │   └── useThemeStore.ts                 # theme mode (light/dark/system), accent color
    │
    ├── components/
    │   ├── ui/                              # shadcn/ui primitives (auto-generated)
    │   │   ├── button.tsx
    │   │   ├── input.tsx
    │   │   ├── textarea.tsx
    │   │   ├── select.tsx
    │   │   ├── card.tsx
    │   │   ├── badge.tsx
    │   │   ├── dialog.tsx
    │   │   ├── dropdown-menu.tsx
    │   │   ├── command.tsx                  # Command palette (cmdk)
    │   │   ├── tooltip.tsx
    │   │   ├── skeleton.tsx
    │   │   ├── separator.tsx
    │   │   ├── scroll-area.tsx
    │   │   ├── collapsible.tsx
    │   │   ├── sheet.tsx                    # Mobile sidebar drawer
    │   │   └── sonner.tsx                   # Toast provider
    │   │
    │   ├── layout/
    │   │   ├── RootLayout.tsx               # App shell: sidebar + main content area
    │   │   ├── AppSidebar.tsx               # Collapsible sidebar (history + nav)
    │   │   ├── TopBar.tsx                   # Header: logo, theme toggle, settings
    │   │   └── MobileNav.tsx                # Bottom sheet / hamburger for mobile
    │   │
    │   ├── shared/
    │   │   ├── ThemeToggle.tsx              # Light/dark/system switcher
    │   │   ├── Logo.tsx                     # App logo + wordmark
    │   │   ├── EmptyState.tsx               # Illustrated empty state component
    │   │   ├── ErrorBoundary.tsx            # React error boundary with fallback UI
    │   │   ├── LoadingSpinner.tsx           # Animated loading indicator
    │   │   └── GradientMeshBackground.tsx   # Ambient gradient mesh for empty states
    │   │
    │   └── prompt/
    │       ├── SpecializationSelector.tsx   # Combobox/command palette for specializations
    │       ├── RequestDescriptionInput.tsx  # Auto-resize textarea with char count
    │       ├── GenerateButton.tsx           # Submit button with loading/disabled states
    │       ├── PromptOutputCard.tsx         # Generated prompt display + copy + actions
    │       ├── MarkdownRenderer.tsx         # react-markdown wrapper with syntax highlight
    │       ├── RetrievedContextPanel.tsx    # Collapsible RAG context viewer
    │       ├── PromptSkeleton.tsx           # Content-shaped skeleton for loading
    │       ├── StreamingTextAnimation.tsx   # Typewriter effect for prompt reveal
    │       ├── CopyButton.tsx              # Copy-to-clipboard with checkmark feedback
    │       ├── PromptFeedbackBar.tsx        # Thumbs up/down + category tags
    │       └── TemplateCard.tsx             # Quick-start prompt template card
    │
    ├── features/
    │   ├── generator/
    │   │   └── GeneratorPage.tsx            # Main prompt generation page
    │   │
    │   ├── history/
    │   │   ├── HistoryPage.tsx              # Full conversation history view
    │   │   ├── HistoryList.tsx              # Scrollable list of past prompts
    │   │   ├── HistorySearchBar.tsx         # Search/filter past conversations
    │   │   ├── HistoryCard.tsx              # Individual history entry card
    │   │   └── HistoryEmptyState.tsx        # Empty state for no history
    │   │
    │   └── settings/
    │       ├── SettingsPage.tsx             # User preferences page
    │       ├── ProfileSection.tsx           # User ID + default specialization
    │       ├── AppearanceSection.tsx        # Theme, font size, density
    │       └── DataSection.tsx              # Export/clear history
    │
    ├── router/
    │   └── index.tsx                        # React Router route definitions
    │
    ├── lib/
    │   ├── constants.ts                     # API URLs, specialization list, defaults
    │   ├── utils.ts                         # cn() helper, date formatters, truncate
    │   └── queryClient.ts                   # TanStack Query client configuration
    │
    └── test/
        ├── setup.ts                         # Vitest setup
        ├── api/
        │   └── promptApi.test.ts
        ├── hooks/
        │   ├── useGeneratePrompt.test.ts
        │   └── usePromptHistory.test.ts
        ├── components/
        │   ├── SpecializationSelector.test.tsx
        │   ├── PromptOutputCard.test.tsx
        │   └── MarkdownRenderer.test.tsx
        └── features/
            └── GeneratorPage.test.tsx
```

---

## 4. Complete Naming Reference

### A. TypeScript Types & Interfaces (`api/types.ts`)

```typescript
// ──────────────────────────────────────────────
// Request / Response Types (mirror Pydantic exactly)
// ──────────────────────────────────────────────

/** Request body for POST /api/generate */
export interface PromptGenerationRequest {
  userId: string;            // maps to user_id (camelCase in TS)
  specialization: string;
  requestDescription: string; // maps to request_description
}

/** Response body from POST /api/generate */
export interface PromptGenerationResponse {
  generatedPrompt: string;              // maps to generated_prompt
  retrievedContextUsed: string[] | null; // maps to retrieved_context_used
}

/** Single history entry from GET /api/history/:userId */
export interface PromptHistoryEntry {
  id: string;                  // MongoDB _id as string
  userId: string;
  userRequest: string;         // maps to user_request
  generatedPrompt: string;
  retrievedContext: string[];
  timestamp: string;           // ISO 8601 datetime
}

/** Response body from GET /api/history/:userId */
export interface PromptHistoryResponse {
  history: PromptHistoryEntry[];
  totalCount: number;
}

/** Health check response */
export interface HealthCheckResponse {
  status: "ok" | "error";
}

// ──────────────────────────────────────────────
// API Error Type
// ──────────────────────────────────────────────

export interface ApiErrorResponse {
  detail: string;
}

export class ApiClientError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public detail: string
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

// ──────────────────────────────────────────────
// UI / Client-Side Types
// ──────────────────────────────────────────────

export type ThemeMode = "light" | "dark" | "system";

export interface UserPreferences {
  userId: string;
  defaultSpecialization: string;
  themeMode: ThemeMode;
}

export interface PromptTemplate {
  id: string;
  label: string;
  specialization: string;
  requestDescription: string;
  icon: string;     // Lucide icon name
}
```

### B. API Client Functions (`api/apiClient.ts` + `api/promptApi.ts`)

```typescript
// apiClient.ts
const API_BASE_URL: string;                    // from env
async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T>;

// promptApi.ts
async function generatePrompt(request: PromptGenerationRequest): Promise<PromptGenerationResponse>;
async function getPromptHistory(userId: string, limit?: number, offset?: number): Promise<PromptHistoryResponse>;
async function deleteHistoryEntry(userId: string, entryId: string): Promise<void>;
async function checkHealth(): Promise<HealthCheckResponse>;
```

### C. React Hooks

| Hook Name | File | Purpose | Returns |
|-----------|------|---------|---------|
| `useGeneratePrompt` | `hooks/useGeneratePrompt.ts` | TanStack mutation wrapping `generatePrompt()` | `{ mutate, mutateAsync, isPending, isError, error, data, reset }` |
| `usePromptHistory` | `hooks/usePromptHistory.ts` | TanStack query wrapping `getPromptHistory()` | `{ data, isLoading, isError, error, refetch }` |
| `useDeleteHistory` | `hooks/useDeleteHistory.ts` | TanStack mutation wrapping `deleteHistoryEntry()` | `{ mutate, isPending }` |
| `useHealthCheck` | `hooks/useHealthCheck.ts` | TanStack query wrapping `checkHealth()` | `{ data, isError }` |
| `useCopyToClipboard` | `hooks/useCopyToClipboard.ts` | Clipboard API with feedback state | `{ copy, isCopied }` |

### D. Zustand Stores

```typescript
// stores/useUserStore.ts
interface UserState {
  userId: string;
  defaultSpecialization: string;
  setUserId: (id: string) => void;
  setDefaultSpecialization: (spec: string) => void;
}
export const useUserStore: UseBoundStore<StoreApi<UserState>>;

// stores/useThemeStore.ts
interface ThemeState {
  themeMode: ThemeMode;
  setThemeMode: (mode: ThemeMode) => void;
  resolvedTheme: "light" | "dark"; // computed from themeMode + system pref
}
export const useThemeStore: UseBoundStore<StoreApi<ThemeState>>;
```

### E. Component Names (PascalCase)

**Layout:** `RootLayout`, `AppSidebar`, `TopBar`, `MobileNav`
**Shared:** `ThemeToggle`, `Logo`, `EmptyState`, `ErrorBoundary`, `LoadingSpinner`, `GradientMeshBackground`
**Prompt:** `SpecializationSelector`, `RequestDescriptionInput`, `GenerateButton`, `PromptOutputCard`, `MarkdownRenderer`, `RetrievedContextPanel`, `PromptSkeleton`, `StreamingTextAnimation`, `CopyButton`, `PromptFeedbackBar`, `TemplateCard`
**History:** `HistoryPage`, `HistoryList`, `HistorySearchBar`, `HistoryCard`, `HistoryEmptyState`
**Settings:** `SettingsPage`, `ProfileSection`, `AppearanceSection`, `DataSection`
**Pages:** `GeneratorPage`, `HistoryPage`, `SettingsPage`

### F. Constants (`lib/constants.ts`)

```typescript
export const API_BASE_URL: string;
export const DEFAULT_USER_ID = "default_user";
export const MAX_REQUEST_LENGTH = 2000;
export const HISTORY_PAGE_SIZE = 20;
export const PROMPT_TEMPLATES: PromptTemplate[];

export const SPECIALIZATIONS = [
  "Software Engineer",
  "Data Scientist",
  "Product Manager",
  "Technical Writer",
  "UX Designer",
  "DevOps Engineer",
  "Legal Professional",
  "Medical Professional",
  "Marketing Specialist",
  "Educator",
  "Researcher",
  "Business Analyst",
  "Creative Writer",
  "Financial Analyst",
  "Customer Support",
] as const;

export type Specialization = (typeof SPECIALIZATIONS)[number];
```

---

## 5. API Documentation (OpenAPI-Compatible)

### Existing Endpoints

#### `GET /health`
```yaml
summary: Health Check
description: Returns API health status
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            status:
              type: string
              enum: [ok]
```

#### `POST /api/generate`
```yaml
summary: Generate Optimized LLM Prompt
description: |
  Accepts a user's specialization and request description,
  retrieves relevant prompt engineering guidelines via RAG,
  incorporates conversation history, and generates a tailored prompt.
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        required: [user_id, specialization, request_description]
        properties:
          user_id:
            type: string
            description: Unique identifier for tracking conversation history
            example: "user_123"
          specialization:
            type: string
            description: User's professional domain
            example: "Software Engineer"
          request_description:
            type: string
            description: What the user wants the LLM prompt to accomplish
            example: "Generate a prompt to improve technical writing clarity"
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            generated_prompt:
              type: string
              description: The final AI-generated prompt
            retrieved_context_used:
              type: array
              items:
                type: string
              nullable: true
              description: RAG context chunks used in generation
  500:
    content:
      application/json:
        schema:
          type: object
          properties:
            detail:
              type: string
              example: "Failed to generate prompt."
```

### New Endpoints (to be added)

#### `GET /api/history/{user_id}`
```yaml
summary: Get User Prompt History
description: Retrieves paginated conversation history for a user
parameters:
  - name: user_id
    in: path
    required: true
    schema:
      type: string
  - name: limit
    in: query
    schema:
      type: integer
      default: 20
  - name: offset
    in: query
    schema:
      type: integer
      default: 0
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            history:
              type: array
              items:
                $ref: '#/components/schemas/PromptHistoryEntry'
            total_count:
              type: integer
```

#### `DELETE /api/history/{user_id}/{entry_id}`
```yaml
summary: Delete History Entry
description: Removes a specific conversation from user's history
parameters:
  - name: user_id
    in: path
    required: true
    schema:
      type: string
  - name: entry_id
    in: path
    required: true
    schema:
      type: string
responses:
  204:
    description: Successfully deleted
  404:
    content:
      application/json:
        schema:
          type: object
          properties:
            detail:
              type: string
              example: "History entry not found"
```

### Snake Case ↔ CamelCase Conversion Strategy

The backend uses `snake_case` (Python convention), the frontend uses `camelCase` (TypeScript convention). Conversion happens in the API client layer:

```typescript
// api/apiClient.ts
function snakeToCamel(obj: Record<string, unknown>): Record<string, unknown>;
function camelToSnake(obj: Record<string, unknown>): Record<string, unknown>;

// Applied automatically in fetchApi():
// - Outgoing requests: camelToSnake(body)
// - Incoming responses: snakeToCamel(response)
```

---

## 6. Backend Modifications Required

### 6A. CORS Middleware (app/main.py)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:4173",   # Vite preview
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6B. New Pydantic Models (app/models.py)

```python
class PromptHistoryEntry(BaseModel):
    id: str = Field(..., description="MongoDB document ID")
    user_id: str
    user_request: str
    generated_prompt: str
    retrieved_context: list[str]
    timestamp: datetime

class PromptHistoryResponse(BaseModel):
    history: list[PromptHistoryEntry]
    total_count: int
```

### 6C. New Service Functions (app/services.py)

```python
async def get_paginated_history(user_id: str, limit: int = 20, offset: int = 0) -> dict:
    """Fetches paginated conversation history for a user."""
    ...

async def delete_history_entry(user_id: str, entry_id: str) -> bool:
    """Deletes a specific conversation entry."""
    ...
```

### 6D. New Endpoints (app/main.py)

```python
@app.get("/api/history/{user_id}", response_model=PromptHistoryResponse)
async def get_history(user_id: str, limit: int = 20, offset: int = 0):
    ...

@app.delete("/api/history/{user_id}/{entry_id}", status_code=204)
async def delete_history(user_id: str, entry_id: str):
    ...
```

### 6E. Production Static File Serving (Optional)

```python
# For production: serve built React app from FastAPI
from fastapi.staticfiles import StaticFiles

# Mount AFTER API routes
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
```

---

## 7. Design System Specification

### Color Palette

```css
/* CSS Custom Properties (via Tailwind CSS v4) */

/* Light Mode */
--color-background: oklch(1 0 0);              /* white */
--color-surface: oklch(0.985 0.002 247);       /* zinc-50 */
--color-surface-elevated: oklch(1 0 0 / 0.8);  /* glass effect */
--color-border: oklch(0.92 0.004 264 / 0.6);   /* zinc-200/60 */
--color-text-primary: oklch(0.21 0.006 285);    /* zinc-900 */
--color-text-secondary: oklch(0.55 0.014 258);  /* zinc-500 */
--color-accent: oklch(0.65 0.2 275);            /* indigo-500 */
--color-accent-subtle: oklch(0.65 0.2 275 / 0.1);

/* Dark Mode */
--color-background: oklch(0.145 0.005 286);     /* zinc-950 */
--color-surface: oklch(0.21 0.006 285 / 0.8);   /* zinc-900/80 */
--color-surface-elevated: oklch(0.27 0.006 286 / 0.6);
--color-border: oklch(0.27 0.006 286 / 0.4);    /* zinc-800/40 */
--color-text-primary: oklch(0.985 0.002 247);    /* zinc-50 */
--color-text-secondary: oklch(0.63 0.015 261);   /* zinc-400 */
```

### Typography

```css
--font-sans: "Inter", "Geist Sans", system-ui, sans-serif;
--font-mono: "JetBrains Mono", "Geist Mono", monospace;
--text-body: 0.875rem / 1.5;      /* 14px */
--text-heading-lg: 1.5rem / 1.3;  /* 24px */
--text-heading-md: 1.125rem / 1.4; /* 18px */
--tracking-tight: -0.02em;
```

### Glass Morphism

```css
.glass-panel {
  background: var(--color-surface-elevated);
  backdrop-filter: blur(12px);
  border: 1px solid var(--color-border);
  border-radius: 1rem;
  box-shadow: 0 1px 3px oklch(0 0 0 / 0.04);
}
```

### Gradient Accent

```css
.gradient-accent {
  background: linear-gradient(
    135deg,
    oklch(0.7 0.18 280) 0%,      /* violet */
    oklch(0.65 0.2 250) 50%,      /* indigo */
    oklch(0.7 0.15 220) 100%      /* blue */
  );
}
```

### Animation Tokens

```css
--duration-fast: 150ms;
--duration-normal: 250ms;
--duration-slow: 500ms;
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
```

### Skeleton Loading Pattern

```tsx
// Content-shaped skeletons with staggered wave effect
<div className="space-y-3">
  <Skeleton className="h-6 w-3/4" />
  <Skeleton className="h-4 w-full [animation-delay:100ms]" />
  <Skeleton className="h-4 w-[95%] [animation-delay:200ms]" />
  <Skeleton className="h-4 w-[88%] [animation-delay:300ms]" />
  <Skeleton className="h-20 w-full rounded-lg [animation-delay:400ms]" />
</div>
```

### Typewriter / Streaming Text Effect

```tsx
// StreamingTextAnimation.tsx — Framer Motion character-by-character reveal
// Uses framer-motion's staggerChildren + individual letter variants
// Renders markdown progressively with react-markdown
// Falls back to instant render on completion
```

---

## 8. Phased Implementation Order

### Phase 1: Foundation (Backend + Frontend Scaffolding)
**Estimated effort: 1-2 hours**

| Step | Description | Files |
|------|-------------|-------|
| 1.1 | Add CORS middleware to FastAPI | `app/main.py` |
| 1.2 | Add history endpoints + models to backend | `app/main.py`, `app/models.py`, `app/services.py` |
| 1.3 | Initialize Vite + React + TypeScript project | `frontend/` scaffold |
| 1.4 | Install all dependencies | `frontend/package.json` |
| 1.5 | Configure Tailwind CSS v4 + shadcn/ui | `tailwind.config.ts`, `components.json`, `src/index.css` |
| 1.6 | Configure Vite proxy to FastAPI | `vite.config.ts` |
| 1.7 | Set up React Router with layout routes | `src/router/index.tsx`, `src/App.tsx` |

**Success Criteria:**
- `npm run dev` starts without errors
- Vite proxy forwards `/api/*` to FastAPI
- Empty pages render at `/`, `/history`, `/settings`
- Backend `/api/history/{user_id}` returns data from MongoDB

### Phase 2: API Layer + State Management
**Estimated effort: 1-2 hours**

| Step | Description | Files |
|------|-------------|-------|
| 2.1 | Create TypeScript types | `src/api/types.ts` |
| 2.2 | Build API client with snake↔camel conversion | `src/api/apiClient.ts` |
| 2.3 | Build prompt API functions | `src/api/promptApi.ts` |
| 2.4 | Set up TanStack Query client | `src/lib/queryClient.ts` |
| 2.5 | Create all custom hooks | `src/hooks/*.ts` |
| 2.6 | Create Zustand stores | `src/stores/*.ts` |
| 2.7 | Create constants file | `src/lib/constants.ts` |

**Success Criteria:**
- `useGeneratePrompt` successfully calls `/api/generate` and returns typed data
- `usePromptHistory` successfully fetches and caches history
- Zustand stores persist to `localStorage`

### Phase 3: Layout + Design System
**Estimated effort: 2-3 hours**

| Step | Description | Files |
|------|-------------|-------|
| 3.1 | Install shadcn/ui components | `src/components/ui/*.tsx` |
| 3.2 | Build RootLayout (sidebar + main + topbar) | `src/components/layout/RootLayout.tsx` |
| 3.3 | Build AppSidebar (collapsible, mobile drawer) | `src/components/layout/AppSidebar.tsx` |
| 3.4 | Build TopBar (logo, theme, nav) | `src/components/layout/TopBar.tsx` |
| 3.5 | Build MobileNav | `src/components/layout/MobileNav.tsx` |
| 3.6 | Build ThemeToggle with system detection | `src/components/shared/ThemeToggle.tsx` |
| 3.7 | Build shared components | `src/components/shared/*.tsx` |
| 3.8 | Set up dark/light mode CSS | `src/index.css` |

**Success Criteria:**
- App renders with sidebar, topbar, main content area
- Theme toggle switches between light/dark/system
- Sidebar collapses on desktop, becomes drawer on mobile
- Glass morphism and gradient accents visible

### Phase 4: Generator Page (Core Feature)
**Estimated effort: 3-4 hours**

| Step | Description | Files |
|------|-------------|-------|
| 4.1 | Build SpecializationSelector (command palette) | `src/components/prompt/SpecializationSelector.tsx` |
| 4.2 | Build RequestDescriptionInput (auto-resize) | `src/components/prompt/RequestDescriptionInput.tsx` |
| 4.3 | Build GenerateButton (loading states) | `src/components/prompt/GenerateButton.tsx` |
| 4.4 | Build MarkdownRenderer | `src/components/prompt/MarkdownRenderer.tsx` |
| 4.5 | Build StreamingTextAnimation | `src/components/prompt/StreamingTextAnimation.tsx` |
| 4.6 | Build CopyButton | `src/components/prompt/CopyButton.tsx` |
| 4.7 | Build PromptOutputCard | `src/components/prompt/PromptOutputCard.tsx` |
| 4.8 | Build RetrievedContextPanel (collapsible) | `src/components/prompt/RetrievedContextPanel.tsx` |
| 4.9 | Build PromptSkeleton | `src/components/prompt/PromptSkeleton.tsx` |
| 4.10 | Build TemplateCard + template gallery | `src/components/prompt/TemplateCard.tsx` |
| 4.11 | Build PromptFeedbackBar | `src/components/prompt/PromptFeedbackBar.tsx` |
| 4.12 | Assemble GeneratorPage | `src/features/generator/GeneratorPage.tsx` |

**Success Criteria:**
- User can select specialization via searchable command palette
- User can type request description with live character count
- Clicking "Generate" shows skeleton → typewriter animation → final prompt
- Copy button works with visual feedback (check icon for 2s)
- Retrieved context shows in collapsible panel
- Template cards pre-fill the form
- Toast notification on error

### Phase 5: History Page
**Estimated effort: 1-2 hours**

| Step | Description | Files |
|------|-------------|-------|
| 5.1 | Build HistorySearchBar | `src/features/history/HistorySearchBar.tsx` |
| 5.2 | Build HistoryCard | `src/features/history/HistoryCard.tsx` |
| 5.3 | Build HistoryList (with infinite scroll) | `src/features/history/HistoryList.tsx` |
| 5.4 | Build HistoryEmptyState | `src/features/history/HistoryEmptyState.tsx` |
| 5.5 | Assemble HistoryPage | `src/features/history/HistoryPage.tsx` |

**Success Criteria:**
- History page loads and displays past conversations
- Search filters conversations by request text
- Each card shows request, generated prompt (truncated), timestamp
- Click card expands to show full prompt + context
- Delete button removes entry with optimistic update
- Empty state shows when no history exists

### Phase 6: Settings Page
**Estimated effort: 1 hour**

| Step | Description | Files |
|------|-------------|-------|
| 6.1 | Build ProfileSection | `src/features/settings/ProfileSection.tsx` |
| 6.2 | Build AppearanceSection | `src/features/settings/AppearanceSection.tsx` |
| 6.3 | Build DataSection | `src/features/settings/DataSection.tsx` |
| 6.4 | Assemble SettingsPage | `src/features/settings/SettingsPage.tsx` |

**Success Criteria:**
- User can set/change user ID
- User can set default specialization
- Theme toggle works
- "Export history" downloads JSON
- "Clear history" deletes all with confirmation dialog

### Phase 7: Polish + Accessibility
**Estimated effort: 1-2 hours**

| Step | Description |
|------|-------------|
| 7.1 | Add Framer Motion page transitions |
| 7.2 | Add `aria-live="polite"` + `role="log"` to streaming output |
| 7.3 | Keyboard navigation: Tab order, Escape handlers, Enter to submit |
| 7.4 | Focus management: don't steal focus after generation completes |
| 7.5 | Color contrast audit (WCAG 2.1 AA) |
| 7.6 | Responsive QA: test at 320px, 768px, 1024px, 1440px |
| 7.7 | Error boundary + offline detection |
| 7.8 | `<meta>` tags, favicon, document title |

### Phase 8: Testing + Production Build
**Estimated effort: 1-2 hours**

| Step | Description |
|------|-------------|
| 8.1 | Write unit tests for API client (mock fetch) |
| 8.2 | Write unit tests for hooks (TanStack Query testing) |
| 8.3 | Write component tests for key components |
| 8.4 | Write integration test for GeneratorPage |
| 8.5 | Run `npm run build` — verify zero errors |
| 8.6 | Test production build with `npm run preview` |
| 8.7 | Optional: configure FastAPI static mount for production |

---

## 9. Development Workflow

### Vite Configuration (`vite.config.ts`)

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/health": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
```

### Package Scripts (`package.json`)

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "test": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

### Concurrent Development (from project root)

```bash
# Terminal 1: FastAPI backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: React frontend
cd frontend && npm run dev
```

---

## 10. Risk Considerations

| Risk | Mitigation |
|------|-----------|
| OpenRouter rate limits during demo | Show cached/mock response while explaining |
| ChromaDB cold start (no documents ingested) | Frontend gracefully handles empty RAG context |
| MongoDB connection failure | Health check on mount, error boundary with retry |
| Long LLM generation time (5-15s) | Skeleton + progress indicator, no timeout in frontend |
| snake_case/camelCase mismatch | Automated conversion in API client layer |
| Mobile keyboard obscuring input | `visualViewport` API to adjust layout |
| Large prompt output (10k+ chars) | Virtualized rendering or truncate + "show more" |
| Accessibility with streaming text | Debounced `aria-live` announcements every 3s |
| Theme flash on page load | Inline script in `index.html` to set class before render |
| Browser clipboard API restrictions | Fallback to `document.execCommand("copy")` |
