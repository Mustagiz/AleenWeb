# Premium Interactive Dashboard & Motion Design System
**Codified Reference: Executive Health / Atelier Intelligence UI Pattern**

This design system pattern is extracted and codified from the reference video (`AQMPvRHg5-a9t5jEZccLWO1y_ZTuV4U48bfQYmbNgqqYI90T-RCvfGH7z_qxnLwfJCivhrSrXaksw_B96Tmt4smQZKCGzDWzHQ6RaNAYAVIWJQ.mp4`). It serves as our core memory and aesthetic blueprint for all UI/UX designs, layouts, motions, and interactive workflows.

---

## 1. Aesthetic Foundations & Spatial Harmony

### 1.1 Canvas & Surface Hierarchy
- **Canvas Ground**: Warm, soft neutral background (`#F7F8FA` or `#F4F6F9`) in Light mode; deep obsidian (`#0A0D14`) in Dark mode. Avoid pure white backgrounds—the subtle off-white background allows white card surfaces to stand out with soft tactile elevation.
- **Card Surfaces**: Pure `#FFFFFF` in Light mode; `#121620` / `#181E2C` in Dark mode.
- **Card Geometry**:
  - Outer containers / cards: `border-radius: 20px - 24px`.
  - Inner widgets, slots, and list rows: `border-radius: 12px - 14px`.
  - Pills, status chips, and badges: `border-radius: 9999px` (capsule).
- **Hairline Definition**:
  - `border: 1px solid rgba(0, 0, 0, 0.045)` (Light) or `1px solid rgba(255, 255, 255, 0.08)` (Dark).
- **Ambient Diffusion**:
  - `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 6px 20px rgba(0, 0, 0, 0.035)`.

### 1.2 Color & Status Architecture
- **Text Palette**:
  - Headers: Deep obsidian `#0F172A` (weight 700 / 800).
  - Body & Labels: `#334155` (weight 500 / 600).
  - Subtle Metadata: Muted slate `#64748B`.
- **Semantic Status Signals**:
  - **Success / Resolved**: Emerald `#059669` (text/icon), `#10B981` (main), Tint `#ECFDF5`, Border `#A7F3D0`.
  - **Warning / Waiting / Delay**: Amber `#D97706` (text/icon), `#F59E0B` (main), Tint `#FFFBEB`, Border `#FDE68A`.
  - **Conflict / Overdue / Urgent**: Coral Red `#DC2626` (text/icon), `#EF4444` (main), Tint `#FEF2F2`, Border `#FCA5A5`.
  - **Active / Info**: Cyan `#0D9488` or Cobalt `#0284C7`, Tint `#F0FDFA`.
  - **AI Magic Accent**: Violet/Indigo gradient `linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)`.

---

## 2. Component Design & Layout Blueprint

### 2.1 Top Control & Context Navigation
- **Location / Campus Selector**: Soft pill button with subtle border (`Alty Clinic Main campus ∨`).
- **Date Selector**: Clean pill with calendar icon (`Tue, Oct 27, 2026 ∨`).
- **Utility Actions**:
  - Circular icon buttons with soft hover halos (Bell with active red badge dot, Help circle).
  - **"Ask AI" Capsule**: Glowing violet/indigo gradient button with white text and sparkle icon.
  - Theme Mode Toggle: Sun/Moon dual-icon sliding capsule.
  - User Avatar: Circular thumbnail with high-contrast border.

### 2.2 Executive Greeting & Segmented View Filter
- **Greeting**: Warm, personal greeting (`Good morning, Rachel`, weight 800).
- **Live Pulse Summary**: One crisp sentence answering *what requires action today* (`48 visits across 4 departments, 17 completed so far. 4 items need attention.`).
- **Timeframe Segmented Filter**: Floating dock `[ Today | Week | Month ]`. The active option is an elevated white pill inside a neutral soft-gray container.
- **Action Button**: Secondary bordered action button (`Export report` with download icon).

### 2.3 KPI Metric Cards with Dot-Matrix Telemetry
- **Top Row**: Pastel icon badge (with 20% tint background) + title + right-aligned micro-trend pill (`↗ +8%` in green, `↘ -3 min` in teal).
- **Hero Metric**: Large, bold numerical metric (weight 800, tabular numerals).
- **Bottom Telemetry Visualizer**: Multi-row **Dot-Matrix Grid** (e.g., 4 rows × 25 dots) where columns light up with status-colored dots representing real-time volume or latency across time buckets.

### 2.4 "Needs Attention" Actionable Problem Cards
- **Subheading**: `Highest risk first` in clean sentence-case caption.
- **List Item Layout**:
  - Left: Pastel icon badge inside rounded squircle (flask, calendar warning, note, hourglass).
  - Center: High-contrast title (`7 lab results awaiting review`), subtext with time/context (`Oldest 26 h, 2 departments`).
  - Right: High-visibility status chip with dot indicator (`● Overdue`, `● Conflict`, `● Unsigned`, `● Delay`) + subtle chevron `>`.
- **Interaction Contract**: Clicking any alert row opens a contextual side-sheet or in-place resolution workflow!

### 2.5 Diagnostic Side-Sheet (Flyout Drawer)
When a user clicks on an actionable issue (e.g. a scheduling conflict):
1. A smooth drawer slides in from the right edge with a backdrop blur overlay.
2. **Header**: Entity avatar, title, and current risk delta in bold red (e.g., `22 min behind`).
3. **Timeline Breakdown**: Chronological slot sequence showing normal slots, conflicts highlighted in soft red cards with `Overlap` pills, and open slots with dashed teal borders.
4. **Causal Diagnostics**:
   - `Why it happened`: Soft purple link icon badge + plain-language explanation of root cause.
   - `If nothing changes`: Amber warning badge + concrete risk statement (e.g., `One of them waits 50 minutes...`).
5. **Recommended Resolution**: A highlighted card (`Best fit` teal chip) showing the optimal action (e.g., `Move Layla Haddad to 11:30 AM`).

### 2.6 Multi-Step Resolution Modal with Staged Channels
- **Stepper Capsule**: `1. Choose fix` (checked) → `2. Tell Patient` (active blue pill) → `3. Confirm`.
- **Before / After Comparison**: Side-by-side cards:
  - `NOW` panel: Conflict highlighted with soft red background.
  - `AFTER` panel: Resolved schedule with soft green highlight.
- **Channel Selector**: Segmented tab control `[ Text message | Phone call | Portal message ]`.
- **Draft Box**: Pre-composed, editable templated message box with patient phone number and template badge.

### 2.7 Optimistic Feedback & Floating Toast
- When the action is confirmed:
  1. The resolution sheet/modal closes smoothly.
  2. The item in the "Needs attention" list optimistically morphs from red/conflict to a green checkmark with `Resolved` status pill!
  3. A luxury floating toast capsule appears at the bottom right (`#0F172A` dark background with subtle border, green check icon, descriptive message, and an instant **Undo** action button).
  4. The "Live activity" stream automatically prepends the completed event at the top with a smooth vertical slide transition.

---

## 3. Motion & Animation Standards

- **Transitions**: Natural spring or cubic bezier curves:
  ```css
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  ```
- **Button Micro-Interactions**:
  - Hover: `transform: translateY(-1px)`, subtle elevation increase.
  - Active: `transform: scale(0.98)`.
  - Focus: Crisp `outline: 2px solid [Color]`, `outline-offset: 2px`.
- **Drawer Slide-Over**:
  - `transform: translateX(0)` with `opacity: 1` on open; `transform: translateX(100%)` on close.
  - Backdrop: `rgba(15, 23, 42, 0.25)` with `backdrop-filter: blur(4px)`.
- **Reduced Motion**: Always honor `prefers-reduced-motion: reduce` by replacing spatial slides with pure opacity fades.
