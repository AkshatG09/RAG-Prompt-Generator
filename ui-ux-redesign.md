## Implementation Plan: RAG Prompt Generator — Professional UI/UX Transformation

### Summary

Transform the RAG-Prompt-Generator frontend from a single-page prototype with hardcoded data into a professional, multi-page application with a complete design system (Tailwind v4 `@theme` tokens + OKLCH colors + dark/light themes), React Router navigation with animated page transitions, real API integration (history endpoint), a cmdk command palette, a reusable component library, and full accessibility support. The plan is structured in 8 execution waves — each wave is atomic (can be committed independently), and tasks within a wave can run in parallel.

---

### Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Theme system** | Zustand `persist` + `.dark` class toggle on `<html>` | Remove `next-themes` dependency; Zustand already used for state. `:root`/`.dark` CSS variables provide the actual theming. Inline `<script>` in `<head>` prevents FOUC. |
| **Routing** | `createBrowserRouter` with nested layout routes | React Router v7 already installed. Layout routes allow persistent sidebar + animated outlets. |
| **Color system** | OKLCH color space | Perceptually uniform lightness steps. Tailwind v4 native support. |
| **Token architecture** | 3-layer: Base → Semantic → Component tokens via `@theme` + `:root`/`.dark` | Semantic tokens in `:root`/`.dark` for theme switching; mapped to Tailwind utilities via `@theme`. Prevents style drift. |
| **Animation** | Framer Motion shared variants + Tailwind `@keyframes` for CSS animations | Framer Motion for orchestrated React animations (page transitions, staggered lists, layout). Tailwind `@keyframes` for CSS-only effects (shimmer, pulse). |
| **Forms** | `react-hook-form` + `zod` | Already installed but unused. Wire up for settings page and prompt input validation. |
| **Command palette** | `cmdk` from root `package.json` → move to `frontend/package.json` | Already installed. Needs keyboard shortcut (⌘K), navigation actions, theme switching. |
| **Test framework** | Vitest + React Testing Library | Vitest integrates with Vite natively. TDD for all new components. |

---

### Wave 0 — Cleanup & Foundation (Prereqs for everything)
**Complexity: S | Commit: `chore: cleanup dead code and fix dependencies`**

This wave removes technical debt and establishes a clean baseline before any new work begins.

#### 0.1 Delete Dead Files
- **DELETE** `frontend/src/App.css` — 184 lines of unused Vite template CSS
- **DELETE** `frontend/src/components/prompt/StreamingOutput.tsx` — unused fake typewriter
- **DELETE** `frontend/src/components/shared/ThemeToggle.tsx` — uses `next-themes`, never rendered, will be replaced
- **DELETE** `frontend/src/stores/useThemeStore.ts` — dead code, conflicts with next-themes, will be replaced
- **DELETE** `frontend/src/assets/react.svg` — Vite template leftover
- **DELETE** `frontend/src/assets/vite.svg` — Vite template leftover

#### 0.2 Fix Dependencies
- **MODIFY** `frontend/package.json` — Add missing dependencies that are incorrectly in root:
  - Move from root: `lucide-react`, `highlight.js`, `rehype-highlight`, `remark-gfm`, `cmdk`, `next-themes` (to be removed after migration)
  - Add new: `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `@testing-library/user-event`, `jsdom`, `@fontsource-variable/inter`, `@fontsource-variable/jetbrains-mono`
  - Keep (already installed, now will be used): `react-hook-form`, `zod`, `react-router-dom`, `clsx`
  - Remove unused: `axios`, `next-themes` (after ThemeToggle replacement)
- **MODIFY** root `package.json` — Remove all frontend dependencies (lucide-react, react-markdown, etc.) — this file is an orphaned artifact

#### 0.3 Setup Test Infrastructure
- **CREATE** `frontend/vitest.config.ts` — Vitest config with jsdom, path aliases matching tsconfig
- **CREATE** `frontend/src/test/setup.ts` — Test setup with `@testing-library/jest-dom` matchers
- **MODIFY** `frontend/tsconfig.app.json` — Add `vitest/globals` types
- **MODIFY** `frontend/package.json` — Add `"test": "vitest"`, `"test:run": "vitest run"` scripts

#### 0.4 Fix Branding
- **MODIFY** `frontend/index.html`:
  - Change `<title>` from `"frontend"` to `"PromptForge — AI Prompt Generator"`
  - Keep existing `favicon.svg` (it's a nice purple lightning bolt, already custom)
  - Add preconnect for font loading
  - Add inline theme script in `<head>` to prevent FOUC

**Tests for Wave 0:** None (cleanup wave). Verify build passes: `tsc -b && vite build`.

---

### Wave 1 — Design System & Tokens (Foundation for ALL UI)
**Complexity: M | Commit: `feat: design system tokens, theme switching, and font loading`**

All subsequent waves depend on this. This establishes the complete visual language.

#### 1.1 Design Token CSS Architecture
- **REWRITE** `frontend/src/index.css` — Complete replacement with OKLCH light/dark themes, Tailwind @theme tokens, base layer styles, utility classes (focus-ring, glass, skeleton)

#### 1.2 Theme Store (Replace old Zustand + next-themes)
- **CREATE** `frontend/src/stores/useThemeStore.ts` (new version):
  - Uses Zustand `persist` middleware
  - Toggles `.dark` class on `document.documentElement`
  - Listens for system preference changes

#### 1.3 Theme Initialization Hook
- **CREATE** `frontend/src/hooks/useThemeInit.ts`

#### 1.4 Animation Variants Library
- **CREATE** `frontend/src/lib/animations.ts` — Shared Framer Motion variants and transition presets

**Tests for Wave 1:**
- `useThemeStore.test.ts` — Theme persistence, system preference resolution, `.dark` class toggle
- `animations.test.ts` — Variant objects have correct keys
- Visual: manually verify light/dark toggle works, font loading, token classes generate

---

### Wave 2 — Component Library (Reusable Primitives)
**Complexity: L | Commit: `feat: reusable UI component library`**

#### Components to Create (all independent/parallel):
- 2.1 Button — variants, sizes, loading, icon, a11y
- 2.2 Input & Textarea — label, error, helperText, character count, form integration
- 2.3 Card — compound component (Header, Body, Footer), variants
- 2.4 Badge — variants, sizes, dot indicator
- 2.5 Modal/Dialog — native dialog, focus trapping, animations
- 2.6 Select/Dropdown — custom select, keyboard nav, search
- 2.7 Tooltip — position, delay, ARIA
- 2.8 Skeleton — variants (text, circle, rect, card), shimmer
- 2.9 EmptyState — icon, title, description, action
- 2.10 CopyButton refactor — use new Button, add ARIA
- 2.11 Barrel export file

---

### Wave 3 — Layout System & Routing
**Complexity: L | Commit: `feat: multi-page routing, responsive layout, navigation`**

Depends on: Wave 1 (tokens), Wave 2 (components)

- 3.1 Router Setup — createBrowserRouter with nested layout routes
- 3.2 Root Layout rewrite — providers shell
- 3.3 App Layout — sidebar + main with AnimatedOutlet
- 3.4 Sidebar rewrite — real navigation, real history, collapse/expand, mobile drawer
- 3.5 AnimatedOutlet — route transitions with AnimatePresence
- 3.6 Header Bar — breadcrumbs, theme toggle, command palette hint
- 3.7 Breadcrumbs — auto-generated from location
- 3.8 Error Boundary
- 3.9 Not Found Page

---

### Wave 4 — API Layer & History Integration
**Complexity: M | Commit: `feat: history API integration, API types, query hooks`**

Depends on: Wave 1, Wave 3

- 4.1 Expand API Types
- 4.2 History API Functions
- 4.3 History Query Hooks (useHistory, useHistoryEntry, useRecentHistory)
- 4.4 Update User Store (persistence, profile fields, specializations)
- 4.5 Update Generate Hook (invalidate history on success)

---

### Wave 5 — Feature Pages (Generator, History, Settings)
**Complexity: XL | Commit: multiple commits per feature**

Depends on: Wave 2, Wave 3, Wave 4

- 5.1 Generator Page Redesign — hero, specialization selector, templates, rich output with tabs
- 5.2 Template Grid Redesign — 8 templates, icons, categories, 3-col responsive
- 5.3 Output Tabs Component — Formatted/Raw/Context tabs
- 5.4 History Page — search, filters, pagination, skeletons, empty state
- 5.5 History Detail Page — request/prompt/context sections, actions
- 5.6 Settings Layout + Profile — react-hook-form + zod
- 5.7 Appearance Settings — theme radio cards with previews
- 5.8 Onboarding Modal — first-visit multi-step form

---

### Wave 6 — Command Palette
**Complexity: M | Commit: `feat: command palette with navigation, actions, and theme switching`**

- 6.1 CommandPalette with cmdk — ⌘K, navigation, actions, theme, recent history
- 6.2 Keyboard Shortcuts Registry — global shortcuts

---

### Wave 7 — Animations & Micro-interactions Polish
**Complexity: M | Commit: `feat: advanced animations, loading states, micro-interactions`**

- 7.1 Page Transitions Enhancement — direction-aware
- 7.2 Loading States — GeneratorSkeleton, HistoryCardSkeleton
- 7.3 Generate Button Enhancement — success/error animations
- 7.4 Sidebar Micro-interactions
- 7.5 Toast Enhancements
- 7.6 Scroll-Triggered Reveals
- 7.7 Reduced Motion Support

---

### Wave 8 — Accessibility Hardening & Final Polish
**Complexity: M | Commit: `feat: accessibility hardening, ARIA, keyboard nav, final polish`**

- 8.1 Focus Management on route changes
- 8.2 Skip Links
- 8.3 ARIA Live Regions
- 8.4 Keyboard Navigation Audit
- 8.5 Screen Reader Testing Labels
- 8.6 Markdown Renderer Accessibility
- 8.7 Final CSS Cleanup

---

### Dependency Graph

```
Wave 0  ──────────────────────────────────────────────►  (cleanup)
   │
   ▼
Wave 1  ──────────────────────────────────────────────►  (design tokens + theme)
   │
   ├──────────┐
   ▼          ▼
Wave 2      Wave 4 (partial — API types/hooks only)
(components)  │
   │          │
   ├──────────┘
   ▼
Wave 3  ──────────────────────────────────────────────►  (layout + routing)
   │
   ├──────────┐
   ▼          ▼
Wave 5      Wave 6
(pages)     (command palette)
   │          │
   ├──────────┘
   ▼
Wave 7  ──────────────────────────────────────────────►  (animations polish)
   │
   ▼
Wave 8  ──────────────────────────────────────────────►  (accessibility + final)
```

### Estimated Total: ~77 files, ~5.5 hours builder time across 8 waves.
