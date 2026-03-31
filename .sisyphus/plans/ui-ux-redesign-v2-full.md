Task continued and completed in 8m 32s.

---

Good — `@hookform/resolvers` is NOT installed. It needs to be added in Wave 0 dependencies. Now I have everything I need. Let me produce the complete, fully-expanded plan.

---

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
| **Forms** | `react-hook-form` + `@hookform/resolvers` + `zod` | Already partially installed. Wire up for settings page and prompt input validation. |
| **Command palette** | `cmdk` from root `package.json` → move to `frontend/package.json` | Already installed. Needs keyboard shortcut (⌘K), navigation actions, theme switching. |
| **Test framework** | Vitest + React Testing Library | Vitest integrates with Vite natively. TDD for all new components. |

---

### Dependency Graph

```
Wave 0  ──────────────────────────────────────────────►  (cleanup, deps, test infra)
   │
   ▼
Wave 1  ──────────────────────────────────────────────►  (design tokens + theme + animations)
   │
   ├──────────┐
   ▼          ▼
Wave 2      Wave 4 (partial — API types/hooks only, no UI)
(ui lib)      │
   │          │
   ├──────────┘
   ▼
Wave 3  ──────────────────────────────────────────────►  (layout + routing + navigation)
   │
   ├──────────┐
   ▼          ▼
Wave 5      Wave 6
(feature     (command
 pages)      palette)
   │          │
   ├──────────┘
   ▼
Wave 7  ──────────────────────────────────────────────►  (animations polish)
   │
   ▼
Wave 8  ──────────────────────────────────────────────►  (accessibility + final)
```

---

### Wave 0 — Cleanup & Foundation
**Complexity: S | Commit: `chore: cleanup dead code and fix dependencies`**

#### 0.1 Delete Dead Files
- **DELETE** `frontend/src/App.css` — 184 lines of unused Vite template CSS, not imported by any live code
- **DELETE** `frontend/src/components/prompt/StreamingOutput.tsx` — unused fake typewriter, never imported
- **DELETE** `frontend/src/components/shared/ThemeToggle.tsx` — uses `next-themes`, never rendered, will be replaced
- **DELETE** `frontend/src/stores/useThemeStore.ts` — dead code, replaced in Wave 1
- **DELETE** `frontend/src/assets/react.svg` — Vite template leftover
- **DELETE** `frontend/src/assets/vite.svg` — Vite template leftover

#### 0.2 Fix Dependencies
- **MODIFY** `frontend/package.json`:
  - **Add** to `dependencies`: `lucide-react@^1.7.0`, `highlight.js@^11.11.1`, `rehype-highlight@^7.0.2`, `remark-gfm@^4.0.1`, `cmdk@^1.1.1`, `@hookform/resolvers@^5.0.0`, `@fontsource-variable/inter`, `@fontsource-variable/jetbrains-mono`, `@tailwindcss/typography@^4.0.0`
  - **Add** to `devDependencies`: `vitest@^3.0.0`, `@testing-library/react@^16.0.0`, `@testing-library/jest-dom@^6.0.0`, `@testing-library/user-event@^14.0.0`, `jsdom@^26.0.0`
  - **Remove** from `dependencies`: `axios` (unused — apiClient uses native fetch), `next-themes` (replaced by Zustand theme store)
  - **Keep** (already installed, will be used): `react-hook-form`, `zod`, `react-router-dom`, `clsx`
- **MODIFY** root `package.json` — Remove all frontend deps that were misplaced here (`lucide-react`, `react-markdown`, `sonner`, `highlight.js`, `remark-gfm`, `rehype-highlight`, `react-syntax-highlighter`, `next-themes`, `cmdk`)

#### 0.3 Setup Test Infrastructure
- **CREATE** `frontend/vitest.config.ts`:
  ```typescript
  import { defineConfig } from 'vitest/config';
  import react from '@vitejs/plugin-react';
  import path from 'path';
  
  export default defineConfig({
    plugins: [react()],
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: ['./src/test/setup.ts'],
      css: true,
    },
    resolve: {
      alias: { '@': path.resolve(__dirname, './src') },
    },
  });
  ```
- **CREATE** `frontend/src/test/setup.ts`:
  ```typescript
  import '@testing-library/jest-dom/vitest';
  ```
- **MODIFY** `frontend/tsconfig.app.json` — Add `"vitest/globals"` to `compilerOptions.types` array alongside `"vite/client"`
- **MODIFY** `frontend/package.json` scripts — Add `"test": "vitest"`, `"test:run": "vitest run"`, `"test:coverage": "vitest run --coverage"`

#### 0.4 Fix Branding
- **MODIFY** `frontend/index.html`:
  - Change `<title>frontend</title>` → `<title>PromptForge — AI Prompt Generator</title>`
  - Keep existing custom `favicon.svg` (purple lightning bolt — already custom)
  - Add FOUC-prevention inline script in `<head>` before `</head>`:
    ```html
    <script>
      try {
        const stored = JSON.parse(localStorage.getItem('prompt-forge-theme') || '{}');
        const theme = stored.state?.theme || 'system';
        const isDark = theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
        document.documentElement.classList.toggle('dark', isDark);
      } catch(e) {}
    </script>
    ```

#### Wave 0 Verification
- **Command:** `cd frontend && npm install && npx tsc -b && npx vite build`
- **Success criteria:** Zero TypeScript errors, build completes, no import errors from deleted files
- **Manual check:** Open `http://localhost:5173`, verify app still renders (GeneratorPage with templates, input, button)

---

### Wave 1 — Design System & Tokens
**Complexity: M | Commit: `feat: design system tokens, theme switching, and font loading`**

All subsequent waves depend on this wave.

#### 1.1 Design Token CSS Architecture
- **REWRITE** `frontend/src/index.css` — Complete replacement with the following structure:

**Section 1 — Imports:**
```css
@import "tailwindcss";
@import "@fontsource-variable/inter";
@import "@fontsource-variable/jetbrains-mono";
@plugin "@tailwindcss/typography";
@custom-variant dark (&:where(.dark, .dark *));
```

**Section 2 — Light theme `:root` semantic variables:**
```css
:root {
  --bg:            oklch(0.985 0.002 260);
  --bg-secondary:  oklch(0.96 0.004 260);
  --fg:            oklch(0.145 0.005 260);
  --fg-muted:      oklch(0.45 0.014 260);
  --surface:       oklch(1.00 0.000 0);
  --surface-hover: oklch(0.97 0.003 260);
  --border:        oklch(0.90 0.006 260);
  --border-hover:  oklch(0.82 0.010 260);
  --ring:          oklch(0.55 0.18 265);
  --muted:         oklch(0.93 0.004 260);
  --accent:        oklch(0.55 0.20 270);
  --accent-hover:  oklch(0.48 0.20 270);
  --accent-fg:     oklch(0.99 0.00 0);
  --success:       oklch(0.55 0.16 145);
  --warning:       oklch(0.70 0.16 75);
  --error:         oklch(0.55 0.20 25);
  --info:          oklch(0.55 0.14 240);
  color-scheme: light;
}
```

**Section 3 — Dark theme `.dark` overrides:**
```css
.dark {
  --bg:            oklch(0.10 0.012 270);
  --bg-secondary:  oklch(0.14 0.014 270);
  --fg:            oklch(0.93 0.005 260);
  --fg-muted:      oklch(0.60 0.014 260);
  --surface:       oklch(0.17 0.015 270);
  --surface-hover: oklch(0.21 0.018 270);
  --border:        oklch(0.26 0.020 270);
  --border-hover:  oklch(0.34 0.024 270);
  --ring:          oklch(0.65 0.20 265);
  --muted:         oklch(0.22 0.015 270);
  --accent:        oklch(0.65 0.22 270);
  --accent-hover:  oklch(0.72 0.22 270);
  --accent-fg:     oklch(0.10 0.00 0);
  --success:       oklch(0.65 0.18 145);
  --warning:       oklch(0.78 0.16 75);
  --error:         oklch(0.65 0.20 25);
  --info:          oklch(0.65 0.16 240);
  color-scheme: dark;
}
```

**Section 4 — `@theme` mapping to Tailwind utilities:**
```css
@theme {
  --color-background: var(--bg);
  --color-background-secondary: var(--bg-secondary);
  --color-foreground: var(--fg);
  --color-foreground-muted: var(--fg-muted);
  --color-surface: var(--surface);
  --color-surface-hover: var(--surface-hover);
  --color-border: var(--border);
  --color-border-hover: var(--border-hover);
  --color-ring: var(--ring);
  --color-muted: var(--muted);
  --color-accent: var(--accent);
  --color-accent-hover: var(--accent-hover);
  --color-accent-foreground: var(--accent-fg);
  --color-success: var(--success);
  --color-warning: var(--warning);
  --color-error: var(--error);
  --color-info: var(--info);
  --font-sans: "Inter Variable", ui-sans-serif, system-ui, -apple-system, sans-serif;
  --font-mono: "JetBrains Mono Variable", ui-monospace, SFMono-Regular, monospace;
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;
  --shadow-xs: 0 1px 2px 0 oklch(0 0 0 / 0.04);
  --shadow-sm: 0 1px 3px 0 oklch(0 0 0 / 0.06), 0 1px 2px -1px oklch(0 0 0 / 0.06);
  --shadow-md: 0 4px 6px -1px oklch(0 0 0 / 0.08), 0 2px 4px -2px oklch(0 0 0 / 0.06);
  --shadow-lg: 0 10px 15px -3px oklch(0 0 0 / 0.08), 0 4px 6px -4px oklch(0 0 0 / 0.06);
  --shadow-xl: 0 20px 25px -5px oklch(0 0 0 / 0.1), 0 8px 10px -6px oklch(0 0 0 / 0.06);
  --shadow-glow: 0 0 24px oklch(0.55 0.20 270 / 0.25);
  --animate-shimmer: shimmer 2s infinite linear;
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-slide-up: slide-up 0.3s ease-out;
  --animate-pulse-glow: pulse-glow 2s infinite ease-in-out;
  @keyframes shimmer {
    from { background-position: -200% 0; }
    to   { background-position: 200% 0; }
  }
  @keyframes fade-in {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
  @keyframes slide-up {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 12px oklch(0.55 0.20 270 / 0.2); }
    50%      { box-shadow: 0 0 24px oklch(0.55 0.20 270 / 0.4); }
  }
}
```

**Section 5 — Base styles and custom utilities:**
```css
body {
  background-color: var(--bg);
  color: var(--fg);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
@utility focus-ring {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}
@utility glass {
  background: oklch(from var(--surface) l c h / 0.7);
  backdrop-filter: blur(16px) saturate(1.2);
  border: 1px solid var(--border);
}
@utility skeleton {
  background: linear-gradient(90deg, var(--muted) 25%, var(--surface-hover) 50%, var(--muted) 75%);
  background-size: 200% 100%;
  animation: shimmer 2s infinite linear;
  border-radius: var(--radius-md);
}
```

#### 1.2 Theme Store
- **CREATE** `frontend/src/stores/useThemeStore.ts` (new file, replaces the deleted one):
  ```typescript
  import { create } from 'zustand';
  import { persist, createJSONStorage } from 'zustand/middleware';

  type ThemeMode = 'light' | 'dark' | 'system';

  interface ThemeState {
    theme: ThemeMode;
    resolvedTheme: 'light' | 'dark';
    setTheme: (theme: ThemeMode) => void;
  }

  function resolveTheme(theme: ThemeMode): 'light' | 'dark' {
    if (theme === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return theme;
  }

  function applyTheme(resolved: 'light' | 'dark') {
    document.documentElement.classList.toggle('dark', resolved === 'dark');
  }

  export const useThemeStore = create<ThemeState>()(
    persist(
      (set) => ({
        theme: 'system',
        resolvedTheme: 'light',
        setTheme: (theme) => {
          const resolved = resolveTheme(theme);
          applyTheme(resolved);
          set({ theme, resolvedTheme: resolved });
        },
      }),
      {
        name: 'prompt-forge-theme',
        storage: createJSONStorage(() => localStorage),
        partialize: (state) => ({ theme: state.theme }),
        onRehydrateStorage: () => (state) => {
          if (state) {
            const resolved = resolveTheme(state.theme);
            applyTheme(resolved);
            state.resolvedTheme = resolved;
          }
        },
      }
    )
  );
  ```

#### 1.3 Theme Initialization Hook
- **CREATE** `frontend/src/hooks/useThemeInit.ts`:
  ```typescript
  import { useEffect } from 'react';
  import { useThemeStore } from '@/stores/useThemeStore';

  export function useThemeInit() {
    const { theme, setTheme } = useThemeStore();

    useEffect(() => {
      // Prevent transition flash on initial load
      document.documentElement.classList.add('no-transition');
      setTheme(theme);
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          document.documentElement.classList.remove('no-transition');
        });
      });
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    // Listen for system preference changes when theme is 'system'
    useEffect(() => {
      if (theme !== 'system') return;
      const mql = window.matchMedia('(prefers-color-scheme: dark)');
      const handler = () => setTheme('system');
      mql.addEventListener('change', handler);
      return () => mql.removeEventListener('change', handler);
    }, [theme, setTheme]);
  }
  ```
  Also add this CSS to `index.css` base section:
  ```css
  html.no-transition, html.no-transition * {
    transition: none !important;
  }
  ```

#### 1.4 Animation Variants Library
- **CREATE** `frontend/src/lib/animations.ts`:
  ```typescript
  import type { Variants, Transition } from 'framer-motion';

  // --- Transition presets ---
  export const springTransition: Transition = {
    type: 'spring', stiffness: 300, damping: 24,
  };
  export const smoothTransition: Transition = {
    duration: 0.2, ease: [0.4, 0, 0.2, 1],
  };
  export const snappyTransition: Transition = {
    duration: 0.15, ease: [0.4, 0, 0.2, 1],
  };

  // --- Variants ---
  export const fadeIn: Variants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: smoothTransition },
    exit: { opacity: 0, transition: snappyTransition },
  };

  export const slideUp: Variants = {
    hidden: { opacity: 0, y: 12 },
    visible: { opacity: 1, y: 0, transition: smoothTransition },
    exit: { opacity: 0, y: -8, transition: snappyTransition },
  };

  export const slideInFromLeft: Variants = {
    hidden: { opacity: 0, x: -16 },
    visible: { opacity: 1, x: 0, transition: smoothTransition },
    exit: { opacity: 0, x: -16, transition: snappyTransition },
  };

  export const slideInFromRight: Variants = {
    hidden: { opacity: 0, x: 16 },
    visible: { opacity: 1, x: 0, transition: smoothTransition },
    exit: { opacity: 0, x: 16, transition: snappyTransition },
  };

  export const scaleIn: Variants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { opacity: 1, scale: 1, transition: springTransition },
    exit: { opacity: 0, scale: 0.95, transition: snappyTransition },
  };

  export const staggerContainer: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.06, delayChildren: 0.1, when: 'beforeChildren' },
    },
    exit: {
      opacity: 0,
      transition: { staggerChildren: 0.03, staggerDirection: -1 },
    },
  };

  export const staggerItem: Variants = {
    hidden: { opacity: 0, y: 16 },
    visible: { opacity: 1, y: 0, transition: springTransition },
    exit: { opacity: 0, y: -8 },
  };

  export const pageTransition: Variants = {
    initial: { opacity: 0, y: 8 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -8 },
  };
  ```

#### Wave 1 Test Plan

**Test file:** `frontend/src/stores/__tests__/useThemeStore.test.ts`
- **Test 1:** `setTheme('dark')` sets `resolvedTheme` to `'dark'` and adds `.dark` class to `document.documentElement`
- **Test 2:** `setTheme('light')` sets `resolvedTheme` to `'light'` and removes `.dark` class from `document.documentElement`
- **Test 3:** `setTheme('system')` resolves based on `matchMedia` result — mock `matchMedia` to return `dark`, verify `.dark` class added
- **Test 4:** Default `theme` is `'system'`

**Test file:** `frontend/src/lib/__tests__/animations.test.ts`
- **Test 1:** All variant objects (`fadeIn`, `slideUp`, `scaleIn`, `staggerContainer`, `staggerItem`, `pageTransition`) export valid objects with `hidden` and `visible` keys
- **Test 2:** `staggerContainer.visible.transition` has `staggerChildren` property
- **Test 3:** `pageTransition` has `initial`, `animate`, and `exit` keys

**Verification:**
- **Command:** `cd frontend && npx vitest run && npx tsc -b && npx vite build`
- **Success criteria:** All tests pass, TypeScript compiles cleanly, build succeeds
- **Manual check:** Open app in browser. Verify: (1) Font is Inter (check in DevTools computed styles), (2) Colors render from CSS variables, (3) Add `.dark` to `<html>` in DevTools — entire UI switches to dark palette

---

### Wave 2 — Component Library
**Complexity: L | Commit: split into 3 sub-commits (see commit strategy)**

All component tasks within Wave 2 are independent and can be built in parallel.

#### 2.1 Button Component

**File:** `frontend/src/components/ui/Button.tsx`

**Props interface:**
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
}
```

**Behavior spec:**
- Renders a `<motion.button>` from Framer Motion
- `variant='primary'`: `bg-accent text-accent-foreground hover:bg-accent-hover`
- `variant='secondary'`: `bg-surface text-foreground border border-border hover:bg-surface-hover`
- `variant='ghost'`: `bg-transparent text-foreground hover:bg-surface-hover`
- `variant='danger'`: `bg-error text-white hover:bg-error/90`
- `variant='outline'`: `bg-transparent border border-border text-foreground hover:border-border-hover`
- `size='sm'`: `px-3 py-1.5 text-sm rounded-md`
- `size='md'`: `px-4 py-2 text-sm rounded-lg`
- `size='lg'`: `px-6 py-3 text-base rounded-lg`
- `loading=true`: renders a 16px spinning SVG before text, sets `aria-busy="true"`, disables button
- `disabled`: sets `opacity-50 cursor-not-allowed`, sets `aria-disabled="true"`
- Framer Motion: `whileTap={{ scale: 0.97 }}` (only when not disabled/loading)
- Focus: `focus-visible:focus-ring` class
- `icon` renders in `iconPosition` (default 'left'), 16px size, with `aria-hidden="true"`
- Uses `clsx` for class composition
- Uses `React.forwardRef` for ref forwarding

**Dependencies within wave:** None

**Test file:** `frontend/src/components/ui/__tests__/Button.test.tsx`
- **Test 1 (renders variants):** Render `<Button variant="primary">Click</Button>`. Assert button has text "Click" and has `bg-accent` class substring
- **Test 2 (loading state):** Render `<Button loading>Submit</Button>`. Assert `aria-busy="true"`, button is disabled, spinner SVG is in DOM
- **Test 3 (click handler):** Render `<Button onClick={mockFn}>Go</Button>`. Fire click event. Assert `mockFn` called once
- **Test 4 (disabled no click):** Render `<Button disabled onClick={mockFn}>Go</Button>`. Fire click event. Assert `mockFn` not called, `aria-disabled="true"` present
- **Test 5 (icon rendering):** Render `<Button icon={<span data-testid="icon" />}>Save</Button>`. Assert `data-testid="icon"` in DOM before button text

---

#### 2.2 Input Component

**File:** `frontend/src/components/ui/Input.tsx`

**Props interface:**
```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  icon?: React.ReactNode;
}
```

**Behavior spec:**
- Renders `<label>` above `<input>` when `label` prop provided
- Label linked to input via `htmlFor` / `id` (auto-generated with `React.useId()`)
- Input styling: `w-full bg-transparent border border-border rounded-lg px-3 py-2 text-sm text-foreground placeholder:text-foreground-muted`
- Focus: `focus:border-ring focus:focus-ring`
- Error state: `border-error` on input, `<p role="alert" class="text-error text-xs mt-1">{error}</p>` below
- `helperText` renders as `<p class="text-foreground-muted text-xs mt-1">{helperText}</p>` below (hidden when error showing)
- `aria-describedby` links to error or helperText element ID
- `aria-invalid="true"` when `error` is truthy
- `icon` renders inside a wrapper `div` with `relative` positioning, icon absolutely positioned left, input gets `pl-9`
- `React.forwardRef` for react-hook-form compatibility

**Dependencies within wave:** None

**Test file:** `frontend/src/components/ui/__tests__/Input.test.tsx`
- **Test 1 (label linkage):** Render `<Input label="Email" />`. Assert `<label>` has `htmlFor` matching input's `id`
- **Test 2 (error display):** Render `<Input error="Required field" />`. Assert text "Required field" in DOM, element has `role="alert"`, input has `aria-invalid="true"`
- **Test 3 (helper text):** Render `<Input helperText="Enter your email" />`. Assert "Enter your email" in DOM. Input has `aria-describedby` pointing to that element
- **Test 4 (icon):** Render `<Input icon={<span data-testid="icon" />} />`. Assert icon is in DOM, input has left padding class
- **Test 5 (typing):** Render `<Input onChange={mockFn} />`. Type "hello" into input. Assert `mockFn` called with event containing "hello"

---

#### 2.3 Textarea Component

**File:** `frontend/src/components/ui/Textarea.tsx`

**Props interface:**
```typescript
interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
  maxLength?: number;
  showCount?: boolean;
  autoResize?: boolean;
}
```

**Behavior spec:**
- Same `label`, `error`, `helperText`, `aria-describedby`, `aria-invalid` patterns as Input
- `showCount=true` with `maxLength`: renders `<span class="text-xs text-foreground-muted">{value.length}/{maxLength}</span>` in bottom-right corner
- When `value.length > maxLength * 0.8`: counter turns `text-warning`
- When `value.length >= maxLength`: counter turns `text-error`
- `autoResize=true`: textarea height adjusts to content via `scrollHeight` on input event. Min 5 rows, max 20 rows
- Base styling: same border/focus pattern as Input, `resize-none` when `autoResize` is true
- `React.forwardRef` for react-hook-form compatibility

**Dependencies within wave:** None

**Test file:** `frontend/src/components/ui/__tests__/Textarea.test.tsx`
- **Test 1 (character count):** Render `<Textarea showCount maxLength={100} />`. Type 50 chars. Assert "50/100" visible
- **Test 2 (warning threshold):** Render `<Textarea showCount maxLength={10} value="12345678" />`. Assert counter has warning-related class
- **Test 3 (error at max):** Render `<Textarea showCount maxLength={10} value="1234567890" />`. Assert counter has error-related class
- **Test 4 (auto resize):** Render `<Textarea autoResize />`. Assert `resize-none` class present
- **Test 5 (error display):** Render `<Textarea error="Too short" />`. Assert "Too short" in DOM, `role="alert"`, `aria-invalid="true"`

---

#### 2.4 Card Component

**File:** `frontend/src/components/ui/Card.tsx`

**Props interface:**
```typescript
interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'glass' | 'elevated' | 'interactive';
}

// Compound components via dot notation:
// Card.Header: React.HTMLAttributes<HTMLDivElement>
// Card.Body: React.HTMLAttributes<HTMLDivElement>
// Card.Footer: React.HTMLAttributes<HTMLDivElement>
```

**Behavior spec:**
- `variant='default'`: `bg-surface border border-border rounded-xl`
- `variant='glass'`: uses `glass` utility class + `rounded-xl`
- `variant='elevated'`: `bg-surface rounded-xl shadow-md`
- `variant='interactive'`: `bg-surface border border-border rounded-xl cursor-pointer hover:border-accent/50 hover:shadow-md transition-all duration-200`
- `Card.Header`: `px-5 py-4 border-b border-border`
- `Card.Body`: `px-5 py-4`
- `Card.Footer`: `px-5 py-4 border-t border-border`
- Implemented as compound components using separate named exports: `Card`, `CardHeader`, `CardBody`, `CardFooter`, plus a namespace export `Card.Header = CardHeader`, etc.

**Dependencies within wave:** None

**Test file:** `frontend/src/components/ui/__tests__/Card.test.tsx`
- **Test 1 (default variant):** Render `<Card>content</Card>`. Assert `bg-surface` class present, "content" in DOM
- **Test 2 (glass variant):** Render `<Card variant="glass">content</Card>`. Assert `glass` class present
- **Test 3 (interactive variant):** Render `<Card variant="interactive" onClick={mockFn}>click me</Card>`. Assert `cursor-pointer` class present. Click. Assert `mockFn` called
- **Test 4 (compound components):** Render `<Card><Card.Header>title</Card.Header><Card.Body>body</Card.Body><Card.Footer>foot</Card.Footer></Card>`. Assert all three text strings in DOM

---

#### 2.5 Badge Component

**File:** `frontend/src/components/ui/Badge.tsx`

**Props interface:**
```typescript
interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info' | 'accent';
  size?: 'sm' | 'md';
  dot?: boolean;
}
```

**Behavior spec:**
- Renders a `<span>` with rounded-full pill styling
- `variant='default'`: `bg-muted text-foreground-muted`
- `variant='success'`: `bg-success/15 text-success`
- `variant='warning'`: `bg-warning/15 text-warning`
- `variant='error'`: `bg-error/15 text-error`
- `variant='info'`: `bg-info/15 text-info`
- `variant='accent'`: `bg-accent/15 text-accent`
- `size='sm'`: `px-2 py-0.5 text-xs`
- `size='md'`: `px-2.5 py-1 text-xs`
- `dot=true`: renders a small 6px circle before text content with the variant's color, `animate-pulse` class if variant is 'success' or 'info'

**Dependencies within wave:** None

**Test file:** `frontend/src/components/ui/__tests__/Badge.test.tsx`
- **Test 1 (renders text):** Render `<Badge>New</Badge>`. Assert "New" in DOM
- **Test 2 (variant classes):** Render `<Badge variant="success">Done</Badge>`. Assert element has success-related class
- **Test 3 (dot indicator):** Render `<Badge dot variant="info">Live</Badge>`. Assert a child element (the dot) exists with width/height styles or appropriate class

---

#### 2.6 Modal Component

**File:** `frontend/src/components/ui/Modal.tsx`

**Props interface:**
```typescript
interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  closeOnOverlayClick?: boolean; // default: true
  closeOnEsc?: boolean; // default: true
  children: React.ReactNode;
}

// Compound components:
// Modal.Body: React.HTMLAttributes<HTMLDivElement>
// Modal.Footer: React.HTMLAttributes<HTMLDivElement>
```

**Behavior spec:**
- Uses a `<div>` overlay + `<div role="dialog">` (not native `<dialog>` — better Framer Motion support)
- Overlay: `fixed inset-0 z-50 bg-black/50 backdrop-blur-sm`
- Content: `fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-lg bg-surface border border-border rounded-2xl shadow-xl`
- `title` renders as `<h2 id="modal-title">` linked via `aria-labelledby` on the dialog div
- `description` renders as `<p id="modal-desc">` linked via `aria-describedby`
- `aria-modal="true"` on dialog div
- Focus trap: on open, focus moves to first focusable element inside. On close, focus returns to previously focused element. Tab cycles within modal content.
- ESC key closes (when `closeOnEsc=true`)
- Overlay click closes (when `closeOnOverlayClick=true`)
- Framer Motion: overlay fades in (`opacity: 0→1`), content uses `scaleIn` variant from animations.ts
- `AnimatePresence` wrapping, keyed on `open`
- `Modal.Body`: `px-6 py-4`
- `Modal.Footer`: `px-6 py-4 border-t border-border flex justify-end gap-3`
- Portal: renders into `document.body` via `createPortal`

**Dependencies within wave:** Depends on `lib/animations.ts` (Wave 1 — already done)

**Test file:** `frontend/src/components/ui/__tests__/Modal.test.tsx`
- **Test 1 (open/close):** Render `<Modal open={true} onClose={mockFn} title="Confirm">body</Modal>`. Assert "Confirm" and "body" in DOM. Re-render with `open={false}`. Assert "Confirm" NOT in DOM
- **Test 2 (ESC closes):** Render open modal. Press `Escape` key. Assert `onClose` called
- **Test 3 (overlay click):** Render open modal. Click overlay element. Assert `onClose` called. Re-render with `closeOnOverlayClick={false}`. Click overlay. Assert `onClose` NOT called again
- **Test 4 (aria attributes):** Render `<Modal open title="Test" description="Desc">…</Modal>`. Assert `role="dialog"`, `aria-modal="true"`, `aria-labelledby` points to element containing "Test", `aria-describedby` points to element containing "Desc"
- **Test 5 (focus management):** Render a button and a modal that opens on button click. Open modal. Assert focus is inside modal. Close modal. Assert focus returns to the button

---

#### 2.7 Select Component

**File:** `frontend/src/components/ui/Select.tsx`

**Props interface:**
```typescript
interface SelectOption {
  value: string;
  label: string;
  icon?: React.ReactNode;
}

interface SelectProps {
  options: SelectOption[];
  value?: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
  error?: string;
  disabled?: boolean;
  searchable?: boolean; // default: false — enables filter input
}
```

**Behavior spec:**
- Renders a trigger `<button>` that displays selected option label (or placeholder)
- On click, opens a floating listbox `<div>` below the trigger
- Listbox: `bg-surface border border-border rounded-lg shadow-lg` with `max-h-60 overflow-y-auto`
- Each option: `<div role="option">` with `px-3 py-2 text-sm hover:bg-surface-hover cursor-pointer`
- Selected option: `bg-accent/10 text-accent`
- `searchable=true`: renders `<input>` at top of listbox, filters options by label (case-insensitive)
- Keyboard: ArrowDown/ArrowUp navigate options, Enter selects, Escape closes, type-ahead focuses matching option
- ARIA: trigger has `role="combobox"`, `aria-expanded`, `aria-haspopup="listbox"`, `aria-activedescendant`. Listbox has `role="listbox"`. Options have `role="option"`, `aria-selected`
- Framer Motion: listbox uses `scaleIn` variant for open/close
- `label` and `error` follow same pattern as Input (label above, error below)
- Closes on outside click (use `useEffect` with document click listener)
- `React.forwardRef` — triggers `onBlur` for react-hook-form
- Disabled state: `opacity-50 cursor-not-allowed`, trigger not clickable

**Dependencies within wave:** None

**Test file:** `frontend/src/components/ui/__tests__/Select.test.tsx`
- **Test 1 (opens and selects):** Render `<Select options={[{value:'a',label:'Apple'},{value:'b',label:'Banana'}]} onChange={mockFn} placeholder="Choose" />`. Click trigger. Assert "Apple" and "Banana" in DOM. Click "Banana". Assert `mockFn` called with `'b'`. Assert listbox closed
- **Test 2 (keyboard navigation):** Render Select with 3 options. Click trigger to open. Press ArrowDown. Assert second option has `aria-selected` focus indicator. Press Enter. Assert `mockFn` called with second option's value
- **Test 3 (search filter):** Render `<Select searchable options={[{value:'a',label:'Apple'},{value:'b',label:'Banana'}]} onChange={mockFn} />`. Open. Type "ban" in search. Assert only "Banana" visible
- **Test 4 (ARIA attributes):** Render Select. Assert trigger has `role="combobox"`, `aria-haspopup="listbox"`, `aria-expanded="false"`. Open. Assert `aria-expanded="true"`. Assert listbox has `role="listbox"`
- **Test 5 (disabled):** Render `<Select disabled ... />`. Click trigger. Assert listbox does NOT open

---

#### 2.8 Tooltip Component

**File:** `frontend/src/components/ui/Tooltip.tsx`

**Props interface:**
```typescript
interface TooltipProps {
  content: React.ReactNode;
  side?: 'top' | 'bottom' | 'left' | 'right'; // default: 'top'
  delayMs?: number; // default: 300
  children: React.ReactElement;
}
```

**Behavior spec:**
- Wrapper component: clones `children` to add event handlers (`onMouseEnter`, `onMouseLeave`, `onFocus`, `onBlur`)
- Shows after `delayMs` on hover/focus, hides instantly on leave/blur
- Tooltip element: `<div role="tooltip">` positioned absolutely relative to child, with `bg-foreground text-background text-xs px-2 py-1 rounded-md shadow-md` (inverted colors for contrast)
- `aria-describedby` linking child to tooltip's ID
- Framer Motion: `fadeIn` variant from animations.ts, `AnimatePresence` keyed on visibility
- Does NOT show when `content` is empty/null

**Dependencies within wave:** Depends on `lib/animations.ts` (Wave 1)

**Test file:** `frontend/src/components/ui/__tests__/Tooltip.test.tsx`
- **Test 1 (shows on hover):** Render `<Tooltip content="Help"><button>Hover me</button></Tooltip>`. Mouse enter on button. Wait 300ms (use `vi.advanceTimersByTime`). Assert "Help" in DOM with `role="tooltip"`
- **Test 2 (hides on leave):** After showing, mouse leave. Assert "Help" NOT in DOM
- **Test 3 (aria linkage):** When tooltip visible, assert button has `aria-describedby` matching tooltip's `id`
- **Test 4 (no content):** Render `<Tooltip content=""><button>test</button></Tooltip>`. Hover. Assert no tooltip appears

---

#### 2.9 Skeleton Component

**File:** `frontend/src/components/ui/Skeleton.tsx`

**Props interface:**
```typescript
interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'text' | 'circle' | 'rect';
  width?: string | number;
  height?: string | number;
  lines?: number; // for 'text' variant, renders multiple lines
}
```

**Behavior spec:**
- `variant='text'` (default): renders `lines` (default 1) `<div>` elements each with `skeleton` utility class, `h-4 rounded`, varied widths (last line 66% width)
- `variant='circle'`: `skeleton rounded-full`, width and height from props (default 40px)
- `variant='rect'`: `skeleton rounded-lg`, width and height from props
- All elements: `aria-hidden="true"`
- Uses `clsx` to merge `className` prop

**Dependencies within wave:** None

**Test file:** `frontend/src/components/ui/__tests__/Skeleton.test.tsx`
- **Test 1 (text lines):** Render `<Skeleton variant="text" lines={3} />`. Assert 3 child divs with `skeleton` class
- **Test 2 (circle):** Render `<Skeleton variant="circle" width={48} height={48} />`. Assert `rounded-full` class, inline style with 48px dimensions
- **Test 3 (aria hidden):** Render `<Skeleton />`. Assert `aria-hidden="true"` on root element

---

#### 2.10 EmptyState Component

**File:** `frontend/src/components/ui/EmptyState.tsx`

**Props interface:**
```typescript
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode; // typically a <Button>
}
```

**Behavior spec:**
- Centered flex column layout: `flex flex-col items-center justify-center py-12 text-center`
- Icon: `text-foreground-muted mb-4`, 48px size, `opacity-60`
- Title: `text-lg font-semibold text-foreground mb-2`
- Description: `text-sm text-foreground-muted max-w-sm mb-6`
- Action: rendered as-is below description
- Framer Motion: `fadeIn` variant on mount

**Dependencies within wave:** Depends on `lib/animations.ts` (Wave 1)

**Test file:** `frontend/src/components/ui/__tests__/EmptyState.test.tsx`
- **Test 1 (renders all):** Render `<EmptyState icon={<span data-testid="ic"/>} title="Nothing here" description="Start creating" action={<button>Create</button>} />`. Assert all 4 elements in DOM
- **Test 2 (optional props):** Render `<EmptyState title="Empty" />`. Assert title in DOM, no description, no action
- **Test 3 (action clickable):** Render with `action={<button onClick={mockFn}>Go</button>}`. Click "Go". Assert `mockFn` called

---

#### 2.11 Refactor CopyButton

**File:** `frontend/src/components/prompt/CopyButton.tsx` (modify existing)

**Changes:**
- Add `<span className="sr-only">{copied ? "Copied to clipboard" : "Copy to clipboard"}</span>` inside button
- Add `aria-live="polite"` on the `sr-only` span so screen readers announce state change
- Add `aria-label="Copy to clipboard"` on the outer button
- Keep existing AnimatePresence icon swap animation (it's well-implemented)
- Replace hardcoded `border border-white/10` with `border border-border hover:bg-surface-hover`
- Add `focus-visible:focus-ring` class

**Dependencies within wave:** None

**Test file:** `frontend/src/components/prompt/__tests__/CopyButton.test.tsx`
- **Test 1 (copies text):** Mock `navigator.clipboard.writeText`. Render `<CopyButton text="hello" />`. Click button. Assert `writeText` called with `"hello"`
- **Test 2 (aria label):** Render `<CopyButton text="x" />`. Assert button has `aria-label="Copy to clipboard"`
- **Test 3 (sr-only changes):** Render `<CopyButton text="x" />`. Assert sr-only text is "Copy to clipboard". Click. Assert sr-only text changes to "Copied to clipboard"

---

#### 2.12 Barrel Export

**File:** `frontend/src/components/ui/index.ts`
```typescript
export { default as Button } from './Button';
export type { ButtonProps } from './Button';
export { default as Input } from './Input';
export { default as Textarea } from './Textarea';
export { Card, CardHeader, CardBody, CardFooter } from './Card';
export { default as Badge } from './Badge';
export { default as Modal } from './Modal';
export { default as Select } from './Select';
export { default as Tooltip } from './Tooltip';
export { default as Skeleton } from './Skeleton';
export { default as EmptyState } from './EmptyState';
```

**Dependencies within wave:** All components must exist first (do this last)

**No test needed** — barrel file is just re-exports.

#### Wave 2 Verification
- **Command:** `cd frontend && npx vitest run src/components/ui && npx vitest run src/components/prompt/__tests__/CopyButton.test.tsx && npx tsc -b && npx vite build`
- **Success criteria:** All 30+ tests pass (3-5 per component × 10 components + CopyButton). Zero TypeScript errors. Build succeeds.
- **Manual check:** Create a temporary test page that renders every component with all variants. Verify in browser: correct styling in both light/dark, keyboard interaction works, hover/focus states visible.

---

### Wave 3 — Layout System & Routing
**Complexity: L | Commit: split into 3 sub-commits**

Depends on: Wave 1 (tokens/theme), Wave 2 (Button, Card, Badge, Tooltip, EmptyState components)

#### 3.1 Router Setup

**File:** `frontend/src/App.tsx` — Complete rewrite

**New content structure:**
```typescript
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/queryClient';
import AppToaster from '@/components/ui/Toaster';
import RootLayout from '@/components/layout/RootLayout';
import AppLayout from '@/components/layout/AppLayout';
import GeneratorPage from '@/features/generator/GeneratorPage';
import HistoryPage from '@/features/history/HistoryPage';
import HistoryDetailPage from '@/features/history/HistoryDetailPage';
import SettingsLayout from '@/features/settings/SettingsLayout';
import ProfileSettings from '@/features/settings/ProfileSettings';
import AppearanceSettings from '@/features/settings/AppearanceSettings';
import NotFoundPage from '@/features/not-found/NotFoundPage';
import ErrorBoundary from '@/components/shared/ErrorBoundary';

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorBoundary />,
    children: [
      {
        element: <AppLayout />,
        children: [
          { index: true, element: <GeneratorPage /> },
          { path: 'history', element: <HistoryPage /> },
          { path: 'history/:id', element: <HistoryDetailPage /> },
          {
            path: 'settings',
            element: <SettingsLayout />,
            children: [
              { index: true, element: <ProfileSettings /> },
              { path: 'appearance', element: <AppearanceSettings /> },
            ],
          },
          { path: '*', element: <NotFoundPage /> },
        ],
      },
    ],
  },
]);

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <AppToaster />
    </QueryClientProvider>
  );
}
```

**File:** `frontend/src/main.tsx` — No changes needed (already renders `<App />`)

**Dependencies within wave:** Needs all layout components and at least stub page components

---

#### 3.2 Root Layout

**File:** `frontend/src/components/layout/RootLayout.tsx` — Complete rewrite

**Behavior spec:**
- Renders `<Outlet />` from react-router (children are nested routes)
- Calls `useThemeInit()` from Wave 1 to initialize theme
- Renders skip-to-content link:
  ```html
  <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[60] focus:rounded-lg focus:bg-accent focus:px-4 focus:py-2 focus:text-accent-foreground">
    Skip to main content
  </a>
  ```
- No other visible UI — just the provider shell

**Dependencies within wave:** Depends on `useThemeInit` (Wave 1)

**Test file:** `frontend/src/components/layout/__tests__/RootLayout.test.tsx`
- **Test 1 (renders outlet):** Render RootLayout inside MemoryRouter with a child route. Assert child content renders
- **Test 2 (skip link):** Render RootLayout. Assert link with text "Skip to main content" exists, has `href="#main-content"`, has `sr-only` class

---

#### 3.3 Animated Outlet

**File:** `frontend/src/components/layout/AnimatedOutlet.tsx`

**Implementation:**
```typescript
import { useRef } from 'react';
import { useLocation, useOutlet } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { pageTransition, smoothTransition } from '@/lib/animations';

export default function AnimatedOutlet() {
  const location = useLocation();
  const outlet = useOutlet();
  const outletRef = useRef(outlet);

  // Preserve outlet during exit animation
  if (outlet) outletRef.current = outlet;

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={location.pathname}
        variants={pageTransition}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={smoothTransition}
      >
        {outlet || outletRef.current}
      </motion.div>
    </AnimatePresence>
  );
}
```

**Dependencies within wave:** Depends on `lib/animations.ts` (Wave 1)

**Test file:** `frontend/src/components/layout/__tests__/AnimatedOutlet.test.tsx`
- **Test 1 (renders current outlet):** Render inside MemoryRouter at route `/`. Assert page content visible
- **Test 2 (key changes on navigate):** Render at `/`, then navigate to `/history`. Assert the motion.div has different `key` prop (verify via data-testid or by checking content changes)

---

#### 3.4 App Layout

**File:** `frontend/src/components/layout/AppLayout.tsx`

**Implementation structure:**
```typescript
export default function AppLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main id="main-content" role="main" className="flex-1 overflow-y-auto px-4 md:px-8">
          <div className="mx-auto max-w-4xl py-6">
            <AnimatedOutlet />
          </div>
        </main>
      </div>
      <CommandPalette />
    </div>
  );
}
```
- Note: `CommandPalette` renders nothing until Wave 6 — use a stub `export default function CommandPalette() { return null; }` until then

**Dependencies within wave:** Depends on Sidebar (3.5), Header (3.7), AnimatedOutlet (3.3)

**Test file:** `frontend/src/components/layout/__tests__/AppLayout.test.tsx`
- **Test 1 (landmark roles):** Render AppLayout inside MemoryRouter. Assert `<main>` with `role="main"` exists. Assert `id="main-content"` present.
- **Test 2 (renders sidebar and header):** Assert sidebar navigation element exists. Assert header element exists.

---

#### 3.5 Sidebar Store

**File:** `frontend/src/stores/useSidebarStore.ts`

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface SidebarState {
  isCollapsed: boolean;
  isMobileOpen: boolean;
  toggleCollapse: () => void;
  setMobileOpen: (open: boolean) => void;
}

export const useSidebarStore = create<SidebarState>()(
  persist(
    (set) => ({
      isCollapsed: false,
      isMobileOpen: false,
      toggleCollapse: () => set((s) => ({ isCollapsed: !s.isCollapsed })),
      setMobileOpen: (isMobileOpen) => set({ isMobileOpen }),
    }),
    {
      name: 'prompt-forge-sidebar',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ isCollapsed: state.isCollapsed }),
    }
  )
);
```

**Test file:** `frontend/src/stores/__tests__/useSidebarStore.test.ts`
- **Test 1 (toggle):** Call `toggleCollapse()`. Assert `isCollapsed` becomes `true`. Call again. Assert `false`.
- **Test 2 (mobile open):** Call `setMobileOpen(true)`. Assert `isMobileOpen` is `true`. Call `setMobileOpen(false)`. Assert `false`.

---

#### 3.6 Sidebar

**File:** `frontend/src/components/layout/Sidebar.tsx` — Complete rewrite

**Behavior spec:**
- **Structure:** `<nav aria-label="Main navigation">` wrapping everything
- **Top section:** Logo area
  - Expanded: Icon + "PromptForge" text, wrapped in `<Link to="/">`
  - Collapsed: Icon only
  - Icon: `Zap` from lucide-react (purple/accent color)
- **Navigation links** using `NavLink` from react-router:
  - `{ to: '/', icon: Sparkles, label: 'Generator' }` — `end: true` for exact match
  - `{ to: '/history', icon: History, label: 'History' }`
  - `{ to: '/settings', icon: Settings, label: 'Settings' }`
  - Active: `bg-accent/10 text-accent` class
  - Inactive: `text-foreground-muted hover:text-foreground hover:bg-surface-hover`
  - Each rendered as `<NavLink className={({isActive}) => ...}>` with icon + label
  - Collapsed: only icon visible, `<Tooltip>` wrapping each link showing label
  - Staggered entrance animation from `staggerContainer`/`staggerItem` variants
- **Recent history section** (visible only when expanded):
  - Heading: `<h3 className="text-xs font-medium text-foreground-muted uppercase tracking-wider px-3 mb-2">Recent</h3>`
  - Lists last 5 history items from `useRecentHistory(userId, 5)` hook (Wave 4)
  - Each item: truncated `userRequest` text (max 40 chars with ellipsis), click navigates to `/history/:id`
  - Loading: 3 skeleton text lines
  - Empty: small text "No history yet"
  - **STUB for now:** Until Wave 4 provides `useRecentHistory`, render static "No history yet" text. The hook integration happens in Wave 5.
- **Bottom section:**
  - Collapse toggle: `<Button variant="ghost" size="sm">` with `PanelLeftClose` / `PanelLeftOpen` icon
  - Theme toggle: `<Button variant="ghost" size="sm">` with `Sun` / `Moon` icon, calls `useThemeStore().setTheme()`
  - Keyboard shortcut hint: `<Badge size="sm">⌘K</Badge>`
- **Responsive:**
  - Desktop (≥768px): persistent sidebar, width `w-64` expanded or `w-16` collapsed, with `motion.nav` `layout` animation
  - Mobile (<768px): overlay drawer from left with backdrop (`fixed inset-0 z-40`), triggered by `isMobileOpen` from store. Backdrop: `bg-black/50 backdrop-blur-sm`. Close on backdrop click or any navigation.
- **Width transitions:** Use `framer-motion` `layout` prop on the nav element. Expanded `width: 256`, collapsed `width: 64`.

**Dependencies within wave:** Depends on `useSidebarStore` (3.5), `useThemeStore` (Wave 1), `Button` + `Badge` + `Tooltip` + `Skeleton` (Wave 2)

**Test file:** `frontend/src/components/layout/__tests__/Sidebar.test.tsx`
- **Test 1 (nav links render):** Render Sidebar in MemoryRouter. Assert "Generator", "History", "Settings" links present
- **Test 2 (active link):** Render at `/history`. Assert "History" link has active class (contains `text-accent`)
- **Test 3 (collapse toggle):** Click collapse button. Assert sidebar narrows (verify class change or store state change)
- **Test 4 (mobile drawer):** Set viewport to mobile width. Call `useSidebarStore.getState().setMobileOpen(true)`. Assert backdrop overlay visible. Click backdrop. Assert `isMobileOpen` becomes `false`
- **Test 5 (theme toggle):** Click theme toggle button (Moon/Sun icon). Assert `useThemeStore` `setTheme` was called

---

#### 3.7 Header

**File:** `frontend/src/components/layout/Header.tsx`

**Props:** None (reads from stores and router)

**Behavior spec:**
- Sticky top bar: `sticky top-0 z-30 flex items-center justify-between h-14 px-4 md:px-8 border-b border-border bg-background/80 backdrop-blur-md`
- **Left side:**
  - Mobile only (`md:hidden`): hamburger button (`Menu` icon) → calls `useSidebarStore().setMobileOpen(true)`
  - `<Breadcrumbs />` component (3.8)
- **Right side:**
  - Command palette trigger: `<button>` showing `<kbd className="text-xs bg-muted rounded px-1.5 py-0.5 font-mono">⌘K</kbd>` + `<span className="text-sm text-foreground-muted ml-2">Search...</span>` — clicking opens command palette (Wire in Wave 6; for now, no-op)
  - User avatar: `<div className="h-8 w-8 rounded-full bg-accent/20 text-accent flex items-center justify-center text-sm font-medium">` showing first letter of `useUserStore().displayName` or "U" default

**Dependencies within wave:** Depends on `Breadcrumbs` (3.8), `useSidebarStore` (3.5), `useUserStore` (existing)

**Test file:** `frontend/src/components/layout/__tests__/Header.test.tsx`
- **Test 1 (renders breadcrumbs):** Render Header inside MemoryRouter at `/settings`. Assert "Settings" text visible in breadcrumbs area
- **Test 2 (mobile menu button):** Render at mobile viewport. Assert button with `Menu` icon (or accessible name) exists. Click it. Assert `useSidebarStore` `setMobileOpen` called with `true`
- **Test 3 (⌘K hint):** Assert "⌘K" text visible in header
- **Test 4 (user avatar):** Set `useUserStore` displayName to "Alice". Assert "A" visible in avatar circle

---

#### 3.8 Breadcrumbs

**File:** `frontend/src/components/layout/Breadcrumbs.tsx`

**Behavior spec:**
- Reads `useLocation().pathname` and splits into segments
- Maps segments to labels: `{ '': 'Generator', 'history': 'History', 'settings': 'Settings', 'appearance': 'Appearance' }`
- Dynamic segments (`:id`): shows "Detail" or the actual ID
- Renders: `<nav aria-label="Breadcrumb"><ol className="flex items-center gap-1.5 text-sm">` with `<li>` elements
- First item (Home/Generator) always shown as link
- Intermediate items: links
- Last item: `<span aria-current="page" className="text-foreground font-medium">`
- Separator: `ChevronRight` icon (lucide-react, 14px, `text-foreground-muted`)
- Single segment (just Generator): show just "Generator" as non-linked text

**Dependencies within wave:** None

**Test file:** `frontend/src/components/layout/__tests__/Breadcrumbs.test.tsx`
- **Test 1 (root path):** Render at `/`. Assert single item "Generator" with `aria-current="page"`
- **Test 2 (history path):** Render at `/history`. Assert "Generator" (link) + separator + "History" (current)
- **Test 3 (nested settings):** Render at `/settings/appearance`. Assert "Generator" + "Settings" (link) + "Appearance" (current)
- **Test 4 (aria label):** Assert `<nav>` has `aria-label="Breadcrumb"`

---

#### 3.9 Error Boundary

**File:** `frontend/src/components/shared/ErrorBoundary.tsx`

**Implementation:** React class component with `componentDidCatch` + `getDerivedStateFromError`

**Behavior spec:**
- State: `{ hasError: boolean, error: Error | null }`
- Fallback UI: renders `EmptyState` component with:
  - `icon`: `AlertTriangle` from lucide-react (48px, `text-error`)
  - `title`: "Something went wrong"
  - `description`: `error.message` or "An unexpected error occurred"
  - `action`: `<Button onClick={resetError} variant="primary">Try Again</Button>`
- `resetError()`: sets `hasError: false`, `error: null`
- Logs `error` and `errorInfo` to `console.error`
- When `hasError` is false: renders `this.props.children`

**Dependencies within wave:** Depends on `EmptyState` (Wave 2), `Button` (Wave 2)

**Test file:** `frontend/src/components/shared/__tests__/ErrorBoundary.test.tsx`
- **Test 1 (catches error):** Render ErrorBoundary wrapping a component that throws. Assert "Something went wrong" visible
- **Test 2 (shows error message):** Throw `new Error("Oops")`. Assert "Oops" visible in description
- **Test 3 (reset):** After error caught, click "Try Again" button. Assert children attempt to re-render (or error clears)
- **Test 4 (no error):** Render ErrorBoundary wrapping `<div>OK</div>`. Assert "OK" visible, no error UI

---

#### 3.10 Not Found Page

**File:** `frontend/src/features/not-found/NotFoundPage.tsx`

**Behavior spec:**
- Renders `EmptyState` with:
  - `icon`: `FileQuestion` from lucide-react
  - `title`: "Page not found"
  - `description`: "The page you're looking for doesn't exist or has been moved."
  - `action`: `<Button variant="primary" onClick={() => navigate('/')}>Back to Generator</Button>` — uses `useNavigate` from react-router

**Dependencies within wave:** Depends on `EmptyState` (Wave 2), `Button` (Wave 2)

**Test file:** `frontend/src/features/not-found/__tests__/NotFoundPage.test.tsx`
- **Test 1 (renders):** Render inside MemoryRouter. Assert "Page not found" text visible
- **Test 2 (navigation):** Click "Back to Generator" button. Assert navigation to `/` (verify via MemoryRouter history)

---

#### 3.11 Command Palette Stub

**File:** `frontend/src/components/shared/CommandPalette.tsx` (stub — full implementation in Wave 6)

```typescript
export default function CommandPalette() {
  return null; // Implemented in Wave 6
}
```

No test needed for stub.

---

#### Wave 3 Verification
- **Command:** `cd frontend && npx vitest run src/components/layout src/stores/__tests__/useSidebarStore.test.ts src/features/not-found src/components/shared/__tests__/ErrorBoundary.test.tsx && npx tsc -b && npx vite build`
- **Success criteria:** All layout/routing tests pass. TypeScript compiles. Build succeeds.
- **Manual check:** Open app in browser. Verify: (1) Sidebar renders with Generator/History/Settings links, (2) Click "History" — URL changes to `/history`, page content changes with animation, (3) Click "Settings" — URL changes, content changes, (4) Sidebar collapse toggle works, (5) On mobile viewport — sidebar hidden, hamburger button shows, tapping opens overlay drawer, (6) Navigate to `/nonexistent` — shows "Page not found", (7) Breadcrumbs update correctly per route.

---

### Wave 4 — API Layer & History Integration
**Complexity: M | Commit: `feat: history API integration, expanded types, query hooks, user store persistence`**

Depends on: Wave 1 (for types), Wave 3 (for routing — history pages need to exist as stubs)

#### 4.1 Expand API Types

**File:** `frontend/src/api/types.ts` — Add to existing file:

```typescript
// Existing (keep):
export interface PromptGenerationRequest { ... }
export interface PromptGenerationResponse { ... }

// New:
export interface HistoryEntry {
  id: string;
  userId: string;
  userRequest: string;
  generatedPrompt: string;
  retrievedContext: string[];
  timestamp: string; // ISO 8601 from backend
}

export interface HistoryResponse {
  history: HistoryEntry[];
  totalCount: number;
}

export interface PaginationParams {
  limit?: number;
  offset?: number;
}
```

**Dependencies within wave:** None

---

#### 4.2 History API Functions

**File:** `frontend/src/api/historyApi.ts`

```typescript
import { fetchApi } from './apiClient';
import type { HistoryResponse, PaginationParams } from './types';

export function fetchHistory(
  userId: string,
  params: PaginationParams = {}
): Promise<HistoryResponse> {
  const { limit = 30, offset = 0 } = params;
  return fetchApi<HistoryResponse>(
    `/api/history/${encodeURIComponent(userId)}?limit=${limit}&offset=${offset}`
  );
}
```

**Dependencies within wave:** Depends on types (4.1)

**Test file:** `frontend/src/api/__tests__/historyApi.test.ts`
- **Test 1 (correct URL):** Mock global `fetch`. Call `fetchHistory('user_123', { limit: 10, offset: 5 })`. Assert `fetch` called with URL ending in `/api/history/user_123?limit=10&offset=5`
- **Test 2 (default params):** Call `fetchHistory('user_123')`. Assert URL has `limit=30&offset=0`
- **Test 3 (snake_case conversion):** Mock fetch returning `{ history: [{ user_id: 'u1', user_request: 'test', generated_prompt: 'out', retrieved_context: [], timestamp: '2025-01-01T00:00:00Z', id: '1' }], total_count: 1 }`. Assert returned object has `userId`, `userRequest`, `generatedPrompt`, `retrievedContext`, `totalCount` (camelCase)
- **Test 4 (error handling):** Mock fetch returning 500 with `{ detail: "Server error" }`. Assert function throws with "Server error"

---

#### 4.3 History Query Hooks

**File:** `frontend/src/hooks/useHistory.ts`

```typescript
import { useQuery } from '@tanstack/react-query';
import { fetchHistory } from '@/api/historyApi';
import type { PaginationParams } from '@/api/types';

export function useHistory(userId: string, params: PaginationParams = {}) {
  return useQuery({
    queryKey: ['history', userId, params],
    queryFn: () => fetchHistory(userId, params),
    enabled: !!userId,
  });
}

export function useRecentHistory(userId: string, limit = 5) {
  return useQuery({
    queryKey: ['history', userId, { limit, offset: 0 }],
    queryFn: () => fetchHistory(userId, { limit, offset: 0 }),
    enabled: !!userId,
    select: (data) => data.history,
  });
}

export function useHistoryEntry(userId: string, entryId: string) {
  return useQuery({
    queryKey: ['history', userId, 'entry', entryId],
    queryFn: () => fetchHistory(userId, { limit: 100, offset: 0 }),
    enabled: !!userId && !!entryId,
    select: (data) => data.history.find((h) => h.id === entryId) ?? null,
  });
}
```

**Dependencies within wave:** Depends on historyApi (4.2), types (4.1)

**Test file:** `frontend/src/hooks/__tests__/useHistory.test.ts`
- **Test 1 (useHistory returns data):** Mock `fetchHistory`. Render hook with `userId='u1'`. Assert `isLoading` initially true, then `data.history` is the mocked array
- **Test 2 (useHistory disabled when no userId):** Render `useHistory('')`. Assert query is NOT executed (fetch not called)
- **Test 3 (useRecentHistory selects):** Mock `fetchHistory` returning `{ history: [{...}, {...}, {...}], totalCount: 3 }`. Render `useRecentHistory('u1', 2)`. Assert returned data is the `history` array directly (not wrapped in `HistoryResponse`)
- **Test 4 (useHistoryEntry selects single):** Mock fetchHistory returning 3 entries. Render `useHistoryEntry('u1', 'entry-2')`. Assert returned data is the single matching entry

---

#### 4.4 Update User Store

**File:** `frontend/src/stores/useUserStore.ts` — Rewrite

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export const SPECIALIZATIONS = [
  'Software Engineer',
  'Data Scientist',
  'Product Manager',
  'Designer',
  'DevOps Engineer',
  'Technical Writer',
  'Researcher',
  'Student',
  'Other',
] as const;

export type Specialization = (typeof SPECIALIZATIONS)[number];

interface UserState {
  userId: string;
  displayName: string;
  specialization: Specialization | '';
  isOnboarded: boolean;
  setUserId: (id: string) => void;
  setDisplayName: (name: string) => void;
  setSpecialization: (s: Specialization) => void;
  completeOnboarding: (data: { userId: string; displayName: string; specialization: Specialization }) => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      userId: '',
      displayName: '',
      specialization: '',
      isOnboarded: false,
      setUserId: (userId) => set({ userId }),
      setDisplayName: (displayName) => set({ displayName }),
      setSpecialization: (specialization) => set({ specialization }),
      completeOnboarding: (data) => set({ ...data, isOnboarded: true }),
    }),
    {
      name: 'prompt-forge-user',
      storage: createJSONStorage(() => localStorage),
    }
  )
);
```

**Dependencies within wave:** None

**Test file:** `frontend/src/stores/__tests__/useUserStore.test.ts`
- **Test 1 (defaults):** Assert initial state has `userId: ''`, `displayName: ''`, `specialization: ''`, `isOnboarded: false`
- **Test 2 (completeOnboarding):** Call `completeOnboarding({ userId: 'u1', displayName: 'Alice', specialization: 'Software Engineer' })`. Assert all fields set, `isOnboarded: true`
- **Test 3 (individual setters):** Call `setUserId('u2')`. Assert `userId === 'u2'`. Other fields unchanged.
- **Test 4 (SPECIALIZATIONS constant):** Assert `SPECIALIZATIONS` contains 'Software Engineer' and has length 9

---

#### 4.5 Update Generate Hook

**File:** `frontend/src/hooks/useGeneratePrompt.ts` — Modify

**Changes:**
- Import `queryClient` from `@/lib/queryClient`
- Add `onSuccess` to mutation options: `queryClient.invalidateQueries({ queryKey: ['history'] })` — this automatically refreshes sidebar history and history page

```typescript
import { useMutation } from '@tanstack/react-query';
import { generatePrompt } from '@/api/promptApi';
import { queryClient } from '@/lib/queryClient';

export function useGeneratePrompt() {
  return useMutation({
    mutationFn: generatePrompt,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['history'] });
    },
  });
}
```

**Dependencies within wave:** None

**Test file:** `frontend/src/hooks/__tests__/useGeneratePrompt.test.ts`
- **Test 1 (invalidates history):** Mock `generatePrompt` to succeed. Mock `queryClient.invalidateQueries`. Call mutation. Assert `invalidateQueries` called with `{ queryKey: ['history'] }`

---

#### Wave 4 Verification
- **Command:** `cd frontend && npx vitest run src/api/__tests__ src/hooks/__tests__ src/stores/__tests__/useUserStore.test.ts && npx tsc -b && npx vite build`
- **Success criteria:** All API/hook/store tests pass. TypeScript compiles. Build succeeds.
- **Manual check:** (Requires running backend) Open app. Open DevTools Network tab. Navigate — verify no `/api/history` calls yet (hooked up in Wave 5). Verify `useUserStore` persists to localStorage under `prompt-forge-user` key.

---

### Wave 5 — Feature Pages
**Complexity: XL | Commit: split into 4 sub-commits (see commit strategy)**

Depends on: Wave 2 (components), Wave 3 (routing), Wave 4 (API/stores)

#### 5.1 Generator Page Redesign

**File:** `frontend/src/features/generator/GeneratorPage.tsx` — Complete rewrite

**Behavior spec:**
- **Hero heading:** `<motion.h1>` with text "What would you like to create?" — `text-3xl font-bold text-foreground`. Uses `slideUp` variant from animations.ts
- **Specialization selector:** `<Select>` component positioned below heading. Options from `SPECIALIZATIONS` constant. Value bound to `useUserStore().specialization`. `onChange` calls `useUserStore().setSpecialization()`. Label: "Specialization". If no specialization set, shows placeholder "Select your specialization..."
- **Template grid:** `<TemplateGrid onSelect={(text) => setRequest(text)} />` (redesigned in 5.2)
- **Input area:** `<Textarea>` component with:
  - `label="Describe your prompt"` 
  - `value={request}` / `onChange` controlled
  - `maxLength={2000}`
  - `showCount={true}`
  - `autoResize={true}`
  - `placeholder="e.g., Create a system prompt for an AI coding assistant that follows best practices..."`
  - `id="prompt-input"` (for skip link and keyboard shortcut targeting)
  - Clear button: When text present, render `<Button variant="ghost" size="sm" icon={<X />} onClick={() => setRequest('')}>` positioned top-right of textarea card
- **Generate button:** `<Button variant="primary" size="lg" loading={mutation.isPending} disabled={!request.trim() || !specialization} onClick={handleGenerate} icon={<Sparkles />} className="w-full mt-4">Generate Prompt</Button>`
- **Output area:**
  - When no data and no loading: `<EmptyState icon={<Wand2 />} title="Your generated prompt will appear here" description="Select a template or describe what you need above" />`
  - When loading: `<GeneratorSkeleton />` (Wave 7 — for now render `<Skeleton variant="rect" height={200} className="mt-6" />`)
  - When data: `<OutputTabs generatedPrompt={mutation.data.generatedPrompt} retrievedContext={mutation.data.retrievedContextUsed} />` (5.3)
  - Wrapper: `<AnimatePresence mode="wait">` keyed on loading/data/empty state
- **Error handling:** `mutation.isError` → `<Card variant="default" className="mt-6 border-error"><Card.Body><p>Generation failed. Please try again.</p><Button onClick={handleGenerate}>Retry</Button></Card.Body></Card>`
- **Toast:** on success → `toast.success("Prompt generated!")`, on error → `toast.error("Generation failed")`

**Dependencies within wave:** Depends on `OutputTabs` (5.3), `TemplateGrid` (5.2). Can be built with stubs initially.

**Test file:** `frontend/src/features/generator/__tests__/GeneratorPage.test.tsx`
- **Test 1 (empty state):** Render page. Assert "Your generated prompt will appear here" visible
- **Test 2 (template fills input):** Render page. Click first template card. Assert textarea value contains the template text
- **Test 3 (disabled when empty):** Render page. Assert generate button is disabled. Type text into textarea. Assert button becomes enabled
- **Test 4 (calls mutation):** Mock `useGeneratePrompt`. Type request, click generate. Assert `mutate` called with `{ userId, specialization, requestDescription }` matching store values and input
- **Test 5 (output renders):** Mock mutation with successful data. Assert output tabs visible with generated prompt text

---

#### 5.2 Template Grid Redesign

**File:** `frontend/src/components/prompt/TemplateGrid.tsx` — Complete rewrite

**Data structure:**
```typescript
interface Template {
  icon: React.ReactNode; // lucide-react icon component
  label: string;
  description: string;
  text: string; // full prompt text inserted into textarea
}

const TEMPLATES: Template[] = [
  { icon: <PenLine />, label: 'Improve Writing', description: 'Enhance clarity of technical docs', text: 'Create a prompt to improve clarity and readability of technical writing...' },
  { icon: <Bug />, label: 'Debug Code', description: 'Systematic debugging approach', text: 'Generate a prompt to debug complex code issues with systematic analysis...' },
  { icon: <FileText />, label: 'Summarize', description: 'Condense long documents', text: 'Create a prompt to summarize long documents while preserving key points...' },
  { icon: <TestTube />, label: 'Write Tests', description: 'Comprehensive test coverage', text: 'Generate a prompt to write comprehensive test cases with edge coverage...' },
  { icon: <BookOpen />, label: 'Documentation', description: 'Generate API docs', text: 'Create a prompt to generate clear and thorough API documentation...' },
  { icon: <RefreshCw />, label: 'Refactor', description: 'Optimize code structure', text: 'Generate a prompt to refactor and optimize code for maintainability...' },
  { icon: <Lightbulb />, label: 'Brainstorm', description: 'Creative problem solving', text: 'Create a prompt to brainstorm creative solutions to complex problems...' },
  { icon: <Target />, label: 'System Prompt', description: 'Design AI assistant behavior', text: 'Generate a system prompt for an AI assistant with specific behavioral guidelines...' },
];
```

**Props interface:**
```typescript
interface TemplateGridProps {
  onSelect: (text: string) => void;
}
```

**Behavior spec:**
- Grid: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 mt-6`
- Each template: `<Card variant="interactive">` with `<Card.Body>` containing icon (24px, `text-accent`), label (`font-medium text-sm`), description (`text-xs text-foreground-muted`)
- On click: calls `onSelect(template.text)`
- Staggered entrance: parent `<motion.div variants={staggerContainer}>`, each card `<motion.div variants={staggerItem}>`
- Hover: handled by Card's interactive variant (`hover:border-accent/50`)

**Dependencies within wave:** Depends on `Card` (Wave 2), `lib/animations` (Wave 1)

**Test file:** `frontend/src/components/prompt/__tests__/TemplateGrid.test.tsx`
- **Test 1 (renders all templates):** Render `<TemplateGrid onSelect={mockFn} />`. Assert 8 template labels visible
- **Test 2 (click calls onSelect):** Click "Debug Code" template. Assert `mockFn` called with string containing "debug"
- **Test 3 (grid layout):** Assert the grid container has appropriate grid class

---

#### 5.3 Output Tabs

**File:** `frontend/src/components/prompt/OutputTabs.tsx`

**Props interface:**
```typescript
interface OutputTabsProps {
  generatedPrompt: string;
  retrievedContext: string[] | null;
}
```

**Behavior spec:**
- **Tab bar:** 3 tabs: "Formatted", "Raw", "Context"
  - Rendered as `<div role="tablist" aria-label="Output format">` with `<button role="tab">` elements
  - Active tab: `aria-selected="true"`, `text-accent border-b-2 border-accent`
  - Inactive tab: `text-foreground-muted hover:text-foreground`
  - Keyboard: ArrowLeft/ArrowRight moves between tabs, Home/End jumps to first/last
  - Animated underline indicator: Framer Motion `<motion.div layoutId="tab-indicator">` positioned under active tab — slides smoothly when switching
- **Tab panels:** `<div role="tabpanel" aria-labelledby={tabId}>` — only active panel rendered
  - **"Formatted" panel:** `<MarkdownRenderer content={generatedPrompt} />` + `<CopyButton text={generatedPrompt} />` in top-right
  - **"Raw" panel:** `<pre className="font-mono text-sm whitespace-pre-wrap bg-background-secondary p-4 rounded-lg overflow-x-auto">{generatedPrompt}</pre>` + `<CopyButton text={generatedPrompt} />`
  - **"Context" panel:** If `retrievedContext` is null or empty: "No context retrieved". Otherwise: numbered list of context strings, each in a `<Card variant="default">` with `<Badge>#{i+1}</Badge>` prefix. `<CopyButton text={retrievedContext.join('\n\n')} />`
- Wrapper: `<Card variant="default" className="mt-6">` with `<Card.Header>` containing tab bar, `<Card.Body>` containing active panel

**Dependencies within wave:** Depends on `Card`, `Badge` (Wave 2), `CopyButton` (Wave 2 refactor), `MarkdownRenderer` (existing)

**Test file:** `frontend/src/components/prompt/__tests__/OutputTabs.test.tsx`
- **Test 1 (default tab):** Render `<OutputTabs generatedPrompt="# Hello" retrievedContext={['ctx1']} />`. Assert "Formatted" tab is selected (`aria-selected="true"`). Assert markdown content rendered
- **Test 2 (tab switching):** Click "Raw" tab. Assert raw text visible in `<pre>` element. Assert "Formatted" panel not visible.
- **Test 3 (keyboard nav):** Focus first tab. Press ArrowRight. Assert second tab gains focus and `aria-selected="true"`. Press ArrowRight again. Assert third tab focused.
- **Test 4 (context panel):** Click "Context" tab. Assert "ctx1" text visible
- **Test 5 (empty context):** Render with `retrievedContext={null}`. Switch to Context tab. Assert "No context retrieved" visible
- **Test 6 (ARIA):** Assert `role="tablist"` present. Each tab has `role="tab"`. Each panel has `role="tabpanel"` with `aria-labelledby` matching its tab's ID

---

#### 5.4 History Page

**File:** `frontend/src/features/history/HistoryPage.tsx`

**Behavior spec:**
- **Header area:**
  - Title: `<h1 className="text-2xl font-bold">Prompt History</h1>`
  - Search: `<Input icon={<Search />} placeholder="Search your prompts..." value={search} onChange={setSearch} />` — positioned right of title on desktop, below on mobile
- **Loading state:** When `useHistory` returns `isLoading`: render 5 `<HistoryCardSkeleton />` instances (Wave 7 — stub as `<Skeleton variant="rect" height={100} />` until then) wrapped in `<motion.div variants={staggerContainer}>`
- **Error state:** `<Card variant="default" className="border-error"><Card.Body>Failed to load history. <Button onClick={refetch}>Retry</Button></Card.Body></Card>`
- **Empty state:** `<EmptyState icon={<History />} title="No prompts generated yet" description="Start by creating your first prompt" action={<Button variant="primary" onClick={() => navigate('/')}>Create a Prompt</Button>} />`
- **Data state:**
  - Client-side search filter: `data.history.filter(h => h.userRequest.toLowerCase().includes(search.toLowerCase()))`
  - Staggered list: `<motion.div variants={staggerContainer}>` wrapping entries
  - Each entry rendered as: `<motion.div variants={staggerItem}><Card variant="interactive" onClick={() => navigate(\`/history/${entry.id}\`)}>`:
    - `<Card.Body className="flex flex-col gap-2">`
    - Row 1: `<p className="text-sm font-medium line-clamp-2">{entry.userRequest}</p>`
    - Row 2: `<p className="text-xs text-foreground-muted line-clamp-1">{entry.generatedPrompt}</p>`
    - Row 3: `<div className="flex items-center gap-2"><Badge size="sm">{relativeTime(entry.timestamp)}</Badge></div>`
  - `relativeTime` helper: format timestamp as "2 hours ago", "Yesterday", "Mar 15" etc. (implement as simple utility function in `lib/utils.ts`)
- **Pagination:** After list, if `data.totalCount > displayed count`: `<Button variant="secondary" onClick={loadMore} loading={isFetchingNextPage}>Load more</Button>`. Increment `offset` state by `limit` (30).

**Dependencies within wave:** Depends on `Input`, `Card`, `Badge`, `EmptyState`, `Button`, `Skeleton` (Wave 2), `useHistory` (Wave 4), `staggerContainer`/`staggerItem` (Wave 1)

**Test file:** `frontend/src/features/history/__tests__/HistoryPage.test.tsx`
- **Test 1 (loading state):** Mock `useHistory` returning `isLoading: true`. Assert skeleton elements visible (at least 3)
- **Test 2 (data renders):** Mock `useHistory` returning 3 entries. Assert 3 cards visible with user request text
- **Test 3 (empty state):** Mock `useHistory` returning empty array. Assert "No prompts generated yet" visible
- **Test 4 (search filters):** Mock `useHistory` with entries ["apple prompt", "banana prompt"]. Type "banana" in search input. Assert only "banana prompt" card visible
- **Test 5 (click navigates):** Mock `useHistory` with 1 entry (id: "abc"). Click card. Assert navigation to `/history/abc`

---

#### 5.5 History Detail Page

**File:** `frontend/src/features/history/HistoryDetailPage.tsx`

**Behavior spec:**
- Reads `id` from `useParams()` and `userId` from `useUserStore()`
- Calls `useHistoryEntry(userId, id)`
- **Loading:** Full-page skeleton (2 skeleton rects)
- **Not found:** `<EmptyState icon={<FileQuestion />} title="Prompt not found" action={<Button onClick={() => navigate('/history')}>Back to History</Button>} />`
- **Data layout:**
  - **Back button:** `<Button variant="ghost" icon={<ArrowLeft />} onClick={() => navigate('/history')}>Back to History</Button>`
  - **Metadata row:** `<Badge>{relativeTime(entry.timestamp)}</Badge>`
  - **"Your Request" section:** `<Card><Card.Header><h2>Your Request</h2></Card.Header><Card.Body><p>{entry.userRequest}</p></Card.Body></Card>`
  - **"Generated Prompt" section:** `<OutputTabs generatedPrompt={entry.generatedPrompt} retrievedContext={entry.retrievedContext} />`
  - **Action row:** `<Button variant="secondary" icon={<RefreshCw />} onClick={() => { navigate('/'); setRequest(entry.userRequest); }}>Re-generate</Button>` — navigates to generator with request pre-filled (via URL search param `?request=...` or a temporary zustand store)

**Dependencies within wave:** Depends on `OutputTabs` (5.3), `Card`, `Badge`, `Button`, `EmptyState` (Wave 2), `useHistoryEntry` (Wave 4)

**Test file:** `frontend/src/features/history/__tests__/HistoryDetailPage.test.tsx`
- **Test 1 (loading):** Mock `useHistoryEntry` returning `isLoading: true`. Assert skeleton visible
- **Test 2 (renders entry):** Mock entry with `userRequest: "test request"`, `generatedPrompt: "test output"`. Assert both visible
- **Test 3 (not found):** Mock `useHistoryEntry` returning `data: null`. Assert "Prompt not found" visible
- **Test 4 (back navigation):** Click "Back to History" button. Assert navigation to `/history`

---

#### 5.6 Settings Layout

**File:** `frontend/src/features/settings/SettingsLayout.tsx`

**Behavior spec:**
- Left sidebar nav (desktop) / top tabs (mobile):
  - "Profile" → `/settings` (index route, `end: true`)
  - "Appearance" → `/settings/appearance`
  - Uses `NavLink` with active class: `bg-accent/10 text-accent rounded-lg`
  - Inactive: `text-foreground-muted hover:text-foreground hover:bg-surface-hover rounded-lg`
  - Each nav item: `px-3 py-2 text-sm`
- Right content: `<Outlet />`
- Layout: `<div className="flex flex-col md:flex-row gap-8">` with nav `<aside className="w-full md:w-48">` and content `<div className="flex-1">`

**Dependencies within wave:** None (just uses react-router)

**Test file:** `frontend/src/features/settings/__tests__/SettingsLayout.test.tsx`
- **Test 1 (nav links):** Render at `/settings`. Assert "Profile" and "Appearance" links visible
- **Test 2 (active state):** Render at `/settings/appearance`. Assert "Appearance" link has active class
- **Test 3 (outlet renders):** Render at `/settings` with child route. Assert child content visible

---

#### 5.7 Profile Settings

**File:** `frontend/src/features/settings/ProfileSettings.tsx`

**Zod schema:**
```typescript
import { z } from 'zod';
const profileSchema = z.object({
  displayName: z.string().min(2, 'Name must be at least 2 characters').max(50, 'Name too long'),
  userId: z.string().min(1, 'User ID is required').regex(/^[a-zA-Z0-9_]+$/, 'Only letters, numbers, and underscores'),
  specialization: z.string().min(1, 'Please select a specialization'),
});
type ProfileFormData = z.infer<typeof profileSchema>;
```

**Behavior spec:**
- Title: `<h2 className="text-xl font-semibold mb-6">Profile Settings</h2>`
- Form using `useForm<ProfileFormData>({ resolver: zodResolver(profileSchema), defaultValues: { displayName: store.displayName, userId: store.userId, specialization: store.specialization } })`
- Fields:
  - `displayName`: `<Input label="Display Name" {...register('displayName')} error={errors.displayName?.message} />`
  - `userId`: `<Input label="User ID" {...register('userId')} helperText="Used to identify your prompts and history" error={errors.userId?.message} />`
  - `specialization`: `<Select label="Specialization" options={SPECIALIZATIONS.map(s => ({value:s, label:s}))} value={watch('specialization')} onChange={(v) => setValue('specialization', v)} error={errors.specialization?.message} />`
- Submit: `<Button variant="primary" type="submit" loading={false}>Save Changes</Button>`
- On valid submit: calls `useUserStore` setters for each field, shows `toast.success("Settings saved!")`
- Form resets `isDirty` after save

**Dependencies within wave:** Depends on `Input`, `Select`, `Button` (Wave 2), `useUserStore` (Wave 4), `@hookform/resolvers` (Wave 0 deps)

**Test file:** `frontend/src/features/settings/__tests__/ProfileSettings.test.tsx`
- **Test 1 (renders form):** Render ProfileSettings. Assert "Display Name", "User ID", "Specialization" labels visible
- **Test 2 (validation errors):** Submit with empty fields. Assert error messages: "Name must be at least 2 characters", "User ID is required", "Please select a specialization"
- **Test 3 (invalid userId):** Enter "user@123" in userId. Submit. Assert error "Only letters, numbers, and underscores"
- **Test 4 (successful save):** Fill valid data. Submit. Assert `useUserStore` updated with new values. Assert success toast
- **Test 5 (loads defaults from store):** Set store to `{ displayName: 'Alice', userId: 'alice_1', specialization: 'Designer' }`. Render. Assert fields pre-filled

---

#### 5.8 Appearance Settings

**File:** `frontend/src/features/settings/AppearanceSettings.tsx`

**Behavior spec:**
- Title: `<h2 className="text-xl font-semibold mb-6">Appearance</h2>`
- Theme selector: 3 `<Card variant="interactive">` elements in a `grid grid-cols-3 gap-4` layout
  - Each card: icon (`Sun` / `Moon` / `Monitor`), label ("Light" / "Dark" / "System"), small preview area (6px tall gradient strip — light colors for Light card, dark colors for Dark card, split for System)
  - Active card: `border-accent ring-2 ring-accent/30` + checkmark icon in corner
  - Click: calls `useThemeStore().setTheme(mode)`
- Reads `theme` from `useThemeStore()` to determine which card is active

**Dependencies within wave:** Depends on `Card` (Wave 2), `useThemeStore` (Wave 1)

**Test file:** `frontend/src/features/settings/__tests__/AppearanceSettings.test.tsx`
- **Test 1 (renders 3 cards):** Assert "Light", "Dark", "System" text visible
- **Test 2 (active indicator):** Set theme store to `'dark'`. Render. Assert "Dark" card has accent border / checkmark
- **Test 3 (click changes theme):** Click "Light" card. Assert `useThemeStore().setTheme` called with `'light'`
- **Test 4 (system card):** Click "System" card. Assert `setTheme` called with `'system'`

---

#### 5.9 Onboarding Modal

**File:** `frontend/src/features/onboarding/OnboardingModal.tsx`

**Behavior spec:**
- Shows when `useUserStore().isOnboarded === false`
- Uses `<Modal>` component from Wave 2 with `open={!isOnboarded}`, `closeOnOverlayClick={false}`, `closeOnEsc={false}` (must complete onboarding)
- **Step 1 — "Welcome to PromptForge":**
  - Heading: "Welcome to PromptForge 👋"
  - Description: "Set up your profile to get started"
  - Fields: `displayName` (`<Input>`) and `userId` (`<Input>`)
  - Validation: same zod rules as ProfileSettings (displayName min 2, userId alphanumeric)
  - Button: `<Button variant="primary">Continue</Button>` — validates step 1, proceeds to step 2
- **Step 2 — "Select your specialization":**
  - Heading: "What's your specialization?"
  - Grid of `SPECIALIZATIONS` as clickable cards (3-column grid)
  - Each card: specialization name, checkmark on selected
  - Button: `<Button variant="primary" disabled={!selectedSpecialization}>Get Started</Button>`
- On complete: calls `useUserStore().completeOnboarding({ userId, displayName, specialization })`
- Step transition: Framer Motion `AnimatePresence mode="wait"` with `slideInFromRight` for forward, `slideInFromLeft` for back. Back button on step 2.
- Uses `react-hook-form` for step 1 validation

**Dependencies within wave:** Depends on `Modal`, `Input`, `Button`, `Card` (Wave 2), `useUserStore` (Wave 4), animations (Wave 1)

**Test file:** `frontend/src/features/onboarding/__tests__/OnboardingModal.test.tsx`
- **Test 1 (shows when not onboarded):** Set `isOnboarded: false` in store. Render. Assert "Welcome to PromptForge" visible
- **Test 2 (hidden when onboarded):** Set `isOnboarded: true`. Render. Assert modal NOT visible
- **Test 3 (step 1 validation):** Click Continue with empty fields. Assert error messages visible
- **Test 4 (step navigation):** Fill valid step 1 data. Click Continue. Assert step 2 visible ("What's your specialization?")
- **Test 5 (completes onboarding):** Complete both steps. Assert `completeOnboarding` called with correct data. Assert modal closes.

---

#### 5.10 Relative Time Utility

**File:** `frontend/src/lib/utils.ts`

```typescript
export function relativeTime(isoString: string): string {
  const date = new Date(isoString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

export function cn(...classes: (string | undefined | null | false)[]): string {
  return clsx(...classes);
}
```

**Test file:** `frontend/src/lib/__tests__/utils.test.ts`
- **Test 1:** `relativeTime(new Date().toISOString())` → "Just now"
- **Test 2:** `relativeTime(new Date(Date.now() - 3600000).toISOString())` → "1h ago"
- **Test 3:** `relativeTime(new Date(Date.now() - 86400000 * 3).toISOString())` → "3d ago"

---

#### Wave 5 Verification
- **Command:** `cd frontend && npx vitest run src/features src/components/prompt/__tests__/TemplateGrid.test.tsx src/components/prompt/__tests__/OutputTabs.test.tsx src/lib/__tests__/utils.test.ts && npx tsc -b && npx vite build`
- **Success criteria:** All ~30 feature page tests pass. TypeScript compiles. Build succeeds.
- **Manual check (requires backend running):** (1) Fresh visit shows onboarding modal, fill in details, select specialization, click Get Started → modal closes, Generator page shows. (2) Type prompt, click Generate → output renders in formatted/raw/context tabs. (3) Navigate to History → see generated prompt in list. Click it → detail page. (4) Settings → Profile pre-filled with onboarding data, Appearance lets you toggle theme. (5) All pages accessible via sidebar navigation.

---

### Wave 6 — Command Palette
**Complexity: M | Commit: `feat: command palette with navigation, actions, and theme switching`**

Depends on: Wave 3 (routing), Wave 1 (theme store)

#### 6.1 Command Palette Component

**File:** `frontend/src/components/shared/CommandPalette.tsx` — Replace stub from Wave 3

**Behavior spec:**
- Uses `Command` from `cmdk` package
- **Keyboard shortcut:** `useEffect` with `keydown` listener for `⌘K` / `Ctrl+K` → toggles `open` state
- **Dialog structure:**
  - Overlay: `fixed inset-0 z-50 bg-black/50 backdrop-blur-sm` with fade animation
  - Content: `fixed top-[20%] left-1/2 -translate-x-1/2 z-50 w-full max-w-xl rounded-xl border border-border bg-surface shadow-2xl overflow-hidden`
  - `<Command.Input>`: `w-full border-b border-border bg-transparent px-4 py-3 text-base text-foreground placeholder:text-foreground-muted outline-none`
  - `<Command.List>`: `max-h-80 overflow-y-auto p-2`
  - `<Command.Empty>`: `py-6 text-center text-sm text-foreground-muted` with "No results found."
- **Command Groups:**

  **"Navigation" group:**
  | Item | Icon | Action |
  |------|------|--------|
  | Generator | `Sparkles` | `navigate('/')` |
  | History | `History` | `navigate('/history')` |
  | Settings | `Settings` | `navigate('/settings')` |
  | Appearance | `Palette` | `navigate('/settings/appearance')` |

  **"Actions" group:**
  | Item | Icon | Action |
  |------|------|--------|
  | New Prompt | `Plus` | `navigate('/')` + focus prompt input |
  | Search History | `Search` | `navigate('/history')` + focus search input |

  **"Theme" group:**
  | Item | Icon | Action |
  |------|------|--------|
  | Light Mode | `Sun` | `setTheme('light')` |
  | Dark Mode | `Moon` | `setTheme('dark')` |
  | System Theme | `Monitor` | `setTheme('system')` |

- Each `<Command.Item>`: `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-foreground cursor-pointer`, selected state: `data-[selected=true]:bg-accent/10 data-[selected=true]:text-accent`
- **Footer hint bar:** `<div className="border-t border-border px-4 py-2 text-xs text-foreground-muted flex gap-4">` with: `↑↓ Navigate`, `↵ Select`, `esc Close`
- On select: action executes, dialog closes, search resets
- Uses `useNavigate()` from react-router

**Dependencies within wave:** None beyond Wave 3 routing and Wave 1 theme

**CSS additions** to `frontend/src/index.css` (add at bottom):
```css
[cmdk-list] {
  height: var(--cmdk-list-height);
  max-height: 320px;
  transition: height 100ms ease;
  overflow-y: auto;
}
[cmdk-group-heading] {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--fg-muted);
  padding: 0.5rem 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

**Test file:** `frontend/src/components/shared/__tests__/CommandPalette.test.tsx`
- **Test 1 (⌘K opens):** Render CommandPalette inside MemoryRouter. Dispatch `keydown` event with `key='k'` and `metaKey=true`. Assert "No results found." placeholder or input visible
- **Test 2 (⌘K closes):** Open palette. Dispatch ⌘K again. Assert palette closed
- **Test 3 (navigation action):** Open palette. Type "history". Assert "History" item visible. Select it (simulate Enter or click). Assert `navigate` called with `/history`. Assert palette closed
- **Test 4 (theme action):** Open palette. Type "dark". Assert "Dark Mode" item visible. Select it. Assert `setTheme` called with `'dark'`. Assert palette closed
- **Test 5 (ESC closes):** Open palette. Press Escape. Assert palette closed

---

#### 6.2 Keyboard Shortcuts Hook

**File:** `frontend/src/hooks/useKeyboardShortcuts.ts`

**Implementation:**
```typescript
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useThemeStore } from '@/stores/useThemeStore';

export function useKeyboardShortcuts() {
  const navigate = useNavigate();
  const setTheme = useThemeStore((s) => s.setTheme);
  const theme = useThemeStore((s) => s.theme);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      // Don't fire in input/textarea unless with meta key
      const target = e.target as HTMLElement;
      const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable;
      
      if (e.key === '/' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        document.getElementById('prompt-input')?.focus();
      }
      
      if (e.key === 'Enter' && (e.metaKey || e.ctrlKey) && isInput) {
        // ⌘Enter to submit — handled by individual forms, not here
        return;
      }
      
      if (e.key === 't' && e.metaKey && e.shiftKey) {
        e.preventDefault();
        setTheme(theme === 'dark' ? 'light' : theme === 'light' ? 'dark' : 'light');
      }
    };

    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [navigate, setTheme, theme]);
}
```

- Call `useKeyboardShortcuts()` inside `AppLayout` component

**Dependencies within wave:** Depends on theme store (Wave 1), routing (Wave 3)

**Test file:** `frontend/src/hooks/__tests__/useKeyboardShortcuts.test.ts`
- **Test 1 (⌘/ focuses input):** Create element with `id="prompt-input"`. Mock its `focus()`. Render hook. Dispatch ⌘/. Assert `focus()` called
- **Test 2 (⌘Shift+T toggles theme):** Set theme to 'light'. Render hook. Dispatch ⌘Shift+T. Assert `setTheme` called with 'dark'

---

#### 6.3 Wire Command Palette into AppLayout

**File:** `frontend/src/components/layout/AppLayout.tsx` — Modify

**Changes:**
- Replace `<CommandPalette />` stub import with real implementation
- Add `useKeyboardShortcuts()` call

**No additional test needed** — covered by CommandPalette and AppLayout existing tests.

#### Wave 6 Verification
- **Command:** `cd frontend && npx vitest run src/components/shared/__tests__/CommandPalette.test.tsx src/hooks/__tests__/useKeyboardShortcuts.test.ts && npx tsc -b && npx vite build`
- **Success criteria:** All 7 command palette/keyboard tests pass. TypeScript compiles. Build succeeds.
- **Manual check:** (1) Press ⌘K → palette opens. (2) Type "gen" → "Generator" appears. Press Enter → navigates to `/`. (3) Type "dark" → "Dark Mode" appears. Select → theme switches. (4) Press Escape → palette closes. (5) Press ⌘Shift+T → theme toggles. (6) Press ⌘/ → prompt input focuses.

---

### Wave 7 — Animations & Micro-interactions Polish
**Complexity: M | Commit: `feat: skeleton loading, micro-interactions, scroll reveals, reduced motion`**

Depends on: Wave 5 (all pages exist to apply animations to)

#### 7.1 Generator Skeleton

**File:** `frontend/src/components/prompt/GeneratorSkeleton.tsx`

**Behavior spec:**
- Renders a skeleton preview matching the generator output area layout:
  - 3 skeleton tabs in a row (each `<Skeleton variant="rect" width={80} height={32} />`)
  - Below: `<Skeleton variant="rect" height={200} className="w-full" />`
- Framer Motion: `fadeIn` variant on mount
- `aria-hidden="true"`, parent gets `aria-busy="true"` and `aria-label="Loading generated output"`

**Dependencies:** Depends on `Skeleton` (Wave 2)

**Test file:** `frontend/src/components/prompt/__tests__/GeneratorSkeleton.test.tsx`
- **Test 1 (renders):** Assert multiple skeleton elements present (`skeleton` class)
- **Test 2 (aria hidden):** Assert root has `aria-hidden="true"`

---

#### 7.2 History Card Skeleton

**File:** `frontend/src/features/history/HistoryCardSkeleton.tsx`

**Behavior spec:**
- Renders a skeleton matching a history card:
  - `<Card>` containing:
    - `<Skeleton variant="text" width="75%" />` (request title)
    - `<Skeleton variant="text" width="100%" />` (prompt preview)
    - `<Skeleton variant="text" width="40%" />` (timestamp badge)
- `aria-hidden="true"`

**Dependencies:** Depends on `Card`, `Skeleton` (Wave 2)

**Test file:** `frontend/src/features/history/__tests__/HistoryCardSkeleton.test.tsx`
- **Test 1 (renders):** Assert 3 skeleton text elements inside a card
- **Test 2 (aria hidden):** Assert `aria-hidden="true"`

---

#### 7.3 Generate Button Enhancement

**File:** `frontend/src/features/generator/GeneratorPage.tsx` — Modify generate button area

**Changes to generate button behavior:**
- **Loading state:** Button already shows spinner from Wave 5. Add: subtle animated gradient sweep across button background during loading. CSS: `bg-gradient-to-r from-accent via-accent-hover to-accent bg-[length:200%_100%] animate-shimmer`
- **Success animation:** After `mutation.isSuccess`, briefly (600ms) apply `ring-2 ring-success/50` class to button, then remove. Use `useState` + `useEffect` + `setTimeout`
- **Error animation:** After `mutation.isError`, apply Framer Motion `animate={{ x: [-4, 4, -4, 4, 0] }}` (shake) for 400ms. Apply `ring-2 ring-error/50` class for 600ms

**Dependencies:** None new

**Test file:** `frontend/src/features/generator/__tests__/GenerateButtonEffects.test.tsx`
- **Test 1 (success ring):** Mock mutation as success. Assert success ring class appears momentarily (use `vi.advanceTimersByTime`)
- **Test 2 (error shake):** Mock mutation as error. Assert motion animation props applied

---

#### 7.4 Sidebar Micro-interactions

**File:** `frontend/src/components/layout/Sidebar.tsx` — Modify existing

**Changes:**
- Nav item active indicator: Add `<motion.div layoutId="nav-indicator" className="absolute left-0 w-1 h-6 rounded-r bg-accent" />` inside active nav link. Because of `layoutId`, it slides between nav items when active route changes.
- Collapse/expand: The `<nav>` element uses `<motion.nav layout>` with `style={{ width: isCollapsed ? 64 : 256 }}` and `transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}`
- Nav items: entrance uses `staggerContainer`/`staggerItem` on first mount only

**Dependencies:** None new

**Test file:** No new test file — covered by existing Sidebar tests from Wave 3. Add:
- **Test 6 (active indicator):** Render at `/history`. Assert an element with testid "nav-indicator" exists inside History link area

---

#### 7.5 Toast Enhancement

**File:** `frontend/src/components/ui/Toaster.tsx` — Modify

**Changes:**
```typescript
import { Toaster } from 'sonner';

export default function AppToaster() {
  return (
    <Toaster
      richColors
      position="top-right"
      closeButton
      toastOptions={{
        className: 'bg-surface border border-border text-foreground',
        style: {
          background: 'var(--surface)',
          borderColor: 'var(--border)',
          color: 'var(--fg)',
        },
      }}
    />
  );
}
```

**Dependencies:** None new

**Test:** No dedicated test — toaster is a configuration component. Verified through manual checking that toasts match design system colors.

---

#### 7.6 Scroll Reveal Hook

**File:** `frontend/src/hooks/useScrollReveal.ts`

**Implementation:**
```typescript
import { useRef, useState, useEffect } from 'react';

interface UseScrollRevealOptions {
  threshold?: number; // default 0.1
  triggerOnce?: boolean; // default true
}

export function useScrollReveal<T extends HTMLElement = HTMLDivElement>(
  options: UseScrollRevealOptions = {}
) {
  const { threshold = 0.1, triggerOnce = true } = options;
  const ref = useRef<T>(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          if (triggerOnce) observer.unobserve(el);
        } else if (!triggerOnce) {
          setInView(false);
        }
      },
      { threshold }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold, triggerOnce]);

  return { ref, inView };
}
```

**Dependencies:** None

**Test file:** `frontend/src/hooks/__tests__/useScrollReveal.test.ts`
- **Test 1 (initially false):** Render hook. Assert `inView` is `false`
- **Test 2 (becomes true):** Mock `IntersectionObserver` to fire callback with `isIntersecting: true`. Assert `inView` becomes `true`
- **Test 3 (triggerOnce):** After becoming true, simulate element leaving viewport (`isIntersecting: false`). Assert `inView` stays `true` (not reset)

---

#### 7.7 Reduced Motion Hook

**File:** `frontend/src/hooks/useReducedMotion.ts`

**Implementation:**
```typescript
import { useState, useEffect } from 'react';

export function useReducedMotion(): boolean {
  const [reducedMotion, setReducedMotion] = useState(
    () => window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );

  useEffect(() => {
    const mql = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handler = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mql.addEventListener('change', handler);
    return () => mql.removeEventListener('change', handler);
  }, []);

  return reducedMotion;
}
```

**Usage pattern:** Components that use Framer Motion can conditionally set `transition={{ duration: reducedMotion ? 0 : 0.2 }}`. The `AnimatedOutlet` can skip exit animations. This is opt-in per component.

**Dependencies:** None

**Test file:** `frontend/src/hooks/__tests__/useReducedMotion.test.ts`
- **Test 1 (default false):** Mock `matchMedia` to return `matches: false`. Assert hook returns `false`
- **Test 2 (returns true):** Mock `matchMedia` to return `matches: true`. Assert hook returns `true`
- **Test 3 (responds to change):** Mock `matchMedia`, fire change event with `matches: true`. Assert hook updates to `true`

---

#### Wave 7 Verification
- **Command:** `cd frontend && npx vitest run src/components/prompt/__tests__/GeneratorSkeleton.test.tsx src/features/history/__tests__/HistoryCardSkeleton.test.tsx src/features/generator/__tests__/GenerateButtonEffects.test.tsx src/hooks/__tests__/useScrollReveal.test.ts src/hooks/__tests__/useReducedMotion.test.ts && npx tsc -b && npx vite build`
- **Success criteria:** All ~12 tests pass. TypeScript compiles. Build succeeds.
- **Manual check:** (1) Generator: click Generate with valid input — button shows gradient sweep during loading, green ring flash on success. (2) History page: loading shows skeleton cards with shimmer. (3) Sidebar: active nav indicator slides when switching routes. (4) Sidebar collapse/expand is smoothly animated. (5) System Settings → enable reduced motion in OS → verify animations are instant/disabled.

---

### Wave 8 — Accessibility Hardening & Final Polish
**Complexity: M | Commit: `feat: accessibility hardening, ARIA live regions, focus management, final CSS audit`**

Depends on: All previous waves

#### 8.1 Focus Management on Route Change

**File:** `frontend/src/components/layout/AnimatedOutlet.tsx` — Modify

**Changes:**
- After page transition `animate` completes, find the `<h1>` in the new page and call `.focus()` with `{ preventScroll: true }`
- Use Framer Motion's `onAnimationComplete` callback on the `<motion.div>`
- Add `tabIndex={-1}` to all page `<h1>` elements (so they're focusable but not in tab order)

**Test file:** `frontend/src/components/layout/__tests__/AnimatedOutlet.test.tsx` — Add test:
- **Test 3 (focus on h1 after transition):** Navigate to a page with `<h1 tabIndex={-1}>Title</h1>`. After animation, assert `document.activeElement` is the h1 (or verify `.focus()` was called)

---

#### 8.2 Focus Management on Generate Complete

**File:** `frontend/src/features/generator/GeneratorPage.tsx` — Modify

**Changes:**
- After `mutation.isSuccess`, move focus to the output area: `outputRef.current?.focus()` where `outputRef` is attached to the output container `<div tabIndex={-1} ref={outputRef}>`
- After template selection, move focus to textarea: `document.getElementById('prompt-input')?.focus()`

**Test file:** `frontend/src/features/generator/__tests__/GeneratorPage.test.tsx` — Add test:
- **Test (focus on output after generate):** Mock successful mutation. Assert focus moves to output region element

---

#### 8.3 ARIA Live Regions

**File:** `frontend/src/features/generator/GeneratorPage.tsx` — Modify

**Changes:**
- Add `aria-live="polite"` on the output container `<div>` that wraps the `OutputTabs`
- Add a visually hidden status element: `<div className="sr-only" role="status">{mutation.isPending ? "Generating prompt..." : mutation.isSuccess ? "Prompt generated successfully" : ""}</div>`
- Add `<div role="alert" className="sr-only">{mutation.isError ? "Prompt generation failed. Please try again." : ""}</div>`

---

#### 8.4 Keyboard Navigation Audit

**Files to modify:** All interactive components from Waves 2-6

**Implementation:** Add `onKeyDown` handlers to TemplateGrid for arrow navigation (role="listbox", role="option", roving tabIndex)

**Test file:** `frontend/src/components/prompt/__tests__/TemplateGrid.test.tsx` — Add tests:
- **Test (arrow key navigation):** Render grid. Focus first card. Press ArrowRight. Assert second card focused. Press Enter. Assert `onSelect` called
- **Test (ARIA attributes):** Assert grid has `role="listbox"`, cards have `role="option"`

---

#### 8.5 Screen Reader Labels Audit

Scan all components — add missing `aria-label` to icon-only buttons, `aria-hidden="true"` to decorative icons, ensure all form inputs have labels.

Install `@axe-core/react` as dev dependency for automated a11y violation reporting in dev console.

---

#### 8.6 Markdown Renderer Accessibility

**File:** `frontend/src/components/prompt/MarkdownRenderer.tsx` — Modify

**Changes:** Fix prose theming to `prose dark:prose-invert`, add `lang` attribute to code blocks.

**Test file:** `frontend/src/components/prompt/__tests__/MarkdownRenderer.test.tsx`
- **Test 1:** Render `<MarkdownRenderer content="# Hello" />`. Assert `<h1>` with "Hello" in DOM
- **Test 2:** Assert root element has `prose` class
- **Test 3:** Render with fenced code block. Assert `<code>` has `lang` attribute

---

#### 8.7 Final CSS Audit

Grep for hardcoded colors (`#`, `rgb(`, `white/`, `black/`) — replace all with design tokens. Verify dark/light mode completeness.

---

#### Wave 8 Verification
- **Command:** `cd frontend && npx vitest run && npx tsc -b && npx vite build`
- **Success criteria:** ALL tests pass (full suite, ~80+ tests). Zero TypeScript errors. Build succeeds.
- **Manual check:**
  1. Open app — check DevTools console for axe-core violations. Fix critical/serious.
  2. Navigate entire app with ONLY keyboard. Every element reachable. Focus visible.
  3. Toggle light/dark mode — all text readable, borders visible, no broken styles.
  4. Enable OS reduced motion — animations instant/disabled.
  5. VoiceOver test — navigation makes sense, form labels read, live regions announce status.

---

### Complete File Manifest

| Wave | Action | File Path |
|------|--------|-----------|
| 0 | DELETE | `frontend/src/App.css` |
| 0 | DELETE | `frontend/src/components/prompt/StreamingOutput.tsx` |
| 0 | DELETE | `frontend/src/components/shared/ThemeToggle.tsx` |
| 0 | DELETE | `frontend/src/stores/useThemeStore.ts` |
| 0 | DELETE | `frontend/src/assets/react.svg` |
| 0 | DELETE | `frontend/src/assets/vite.svg` |
| 0 | MODIFY | `frontend/package.json` |
| 0 | MODIFY | `root/package.json` |
| 0 | CREATE | `frontend/vitest.config.ts` |
| 0 | CREATE | `frontend/src/test/setup.ts` |
| 0 | MODIFY | `frontend/tsconfig.app.json` |
| 0 | MODIFY | `frontend/index.html` |
| 1 | REWRITE | `frontend/src/index.css` |
| 1 | CREATE | `frontend/src/stores/useThemeStore.ts` |
| 1 | CREATE | `frontend/src/hooks/useThemeInit.ts` |
| 1 | CREATE | `frontend/src/lib/animations.ts` |
| 2 | CREATE | 10 UI components + barrel export in `frontend/src/components/ui/` |
| 2 | MODIFY | `frontend/src/components/prompt/CopyButton.tsx` |
| 2 | CREATE | 11 test files in `frontend/src/components/ui/__tests__/` |
| 3 | REWRITE | `frontend/src/App.tsx` |
| 3 | REWRITE | `frontend/src/components/layout/RootLayout.tsx` |
| 3 | CREATE | AppLayout, AnimatedOutlet, Sidebar, Header, Breadcrumbs, ErrorBoundary, CommandPalette (stub), NotFoundPage |
| 3 | CREATE | `frontend/src/stores/useSidebarStore.ts` |
| 4 | MODIFY | `frontend/src/api/types.ts` |
| 4 | CREATE | `frontend/src/api/historyApi.ts` |
| 4 | CREATE | `frontend/src/hooks/useHistory.ts` |
| 4 | MODIFY | `frontend/src/stores/useUserStore.ts`, `frontend/src/hooks/useGeneratePrompt.ts` |
| 5 | REWRITE | GeneratorPage, TemplateGrid, PromptInputCard |
| 5 | CREATE | OutputTabs, HistoryPage, HistoryDetailPage, SettingsLayout, ProfileSettings, AppearanceSettings, OnboardingModal, utils.ts |
| 6 | REWRITE | CommandPalette (full implementation) |
| 6 | CREATE | `frontend/src/hooks/useKeyboardShortcuts.ts` |
| 7 | CREATE | GeneratorSkeleton, HistoryCardSkeleton, useScrollReveal, useReducedMotion |
| 7 | MODIFY | GeneratorPage (button effects), Sidebar (micro-interactions), Toaster |
| 8 | MODIFY | AnimatedOutlet, GeneratorPage, TemplateGrid, MarkdownRenderer, main.tsx |

**Total: ~100 files (creates + modifies + deletes + tests)**
**Estimated: ~80+ test cases across all waves**
**Estimated builder time: ~5.5 hours across 8 sequential waves**