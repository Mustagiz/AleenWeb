import os

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Aleen Haute Couture & Atelier CRM — Luxury Design System Studio</title>
  
  <!-- Typography: Distinctive Luxury Serif + High-Precision Geometric Grotesk -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,600&family=Outfit:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,600&display=swap" rel="stylesheet">
  
  <!-- Chart.js for silky dual-spline and donut charts -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    /* ==========================================================================
       DESIGN TOKENS & DYNAMIC THEMES (Zero AI tells, WCAG AAA contrast)
       ========================================================================== */
    :root {
      /* Primary: Haute Emerald (Sabyasachi & Invenza inspiration) */
      --color-primary: #047857;
      --color-primary-dark: #064e3b;
      --color-primary-light: #10b981;
      --color-primary-subtle: #ecfdf5;
      --color-primary-border: #a7f3d0;
      --color-primary-text: #064e3b;
      
      /* Accent: Amber / Zardozi Gold */
      --color-accent: #92400e;
      --color-accent-subtle: #fffbeb;
      --color-accent-border: #fde68a;
      --color-accent-text: #78350f;
      
      /* Secondary: Tailoring Navy */
      --color-secondary: #0369a1;
      --color-secondary-subtle: #f0f9ff;
      --color-secondary-border: #bae6fd;
      --color-secondary-text: #075985;

      /* Surfaces & Canvases */
      --bg-page: #f8fafc;
      --bg-surface: #ffffff;
      --bg-surface-elevated: #ffffff;
      --bg-surface-muted: #f1f5f9;
      --bg-sidebar: #ffffff;

      /* Borders & Hairlines */
      --border-subtle: rgba(15, 23, 42, 0.08);
      --border-strong: rgba(15, 23, 42, 0.16);
      --divider-color: rgba(15, 23, 42, 0.08);

      /* Typography Contrast (Strictly WCAG AA/AAA compliant) */
      --text-main: #0f172a;              /* Slate 900 (16.2:1 contrast on white) */
      --text-muted: #334155;             /* Slate 700 (9.4:1 contrast on white) */
      --text-caption: #475569;           /* Slate 600 (5.8:1 contrast on white, 4.8:1 on muted) */
      --text-inverse: #ffffff;

      /* Corner Radii */
      --radius-card: 16px;
      --radius-button: 9999px;
      --radius-inner: 12px;

      /* Shadows (Neutral elevation, zero-offset glow banned) */
      --shadow-ambient: 0 1px 3px rgba(15, 23, 42, 0.04), 0 8px 24px -4px rgba(15, 23, 42, 0.06);
      --shadow-float: 0 4px 6px -1px rgba(15, 23, 42, 0.05), 0 20px 32px -8px rgba(15, 23, 42, 0.08);
      --shadow-hero: 0 12px 36px -8px rgba(15, 23, 42, 0.25);

      /* Fonts */
      --font-display: "Playfair Display", "Cormorant Garamond", Georgia, serif;
      --font-body: "Outfit", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: ui-monospace, "SF Mono", Menlo, monospace;

      /* Spacing & Density */
      --spacing-card-pad: 22px;
      --spacing-grid-gap: 20px;
      
      /* Motion */
      --ease-haptic: cubic-bezier(0.16, 1, 0.3, 1);
      --duration-haptic: 240ms;
    }

    /* THEME PRESET: ROYAL NAVY & OCHRE */
    [data-theme="navy"] {
      --color-primary: #1e40af;
      --color-primary-dark: #172554;
      --color-primary-light: #3b82f6;
      --color-primary-subtle: #eff6ff;
      --color-primary-border: #bfdbfe;
      --color-primary-text: #1e3a8a;
      --shadow-hero: 0 12px 36px -8px rgba(15, 23, 42, 0.25);
    }

    /* THEME PRESET: BURGUNDY & CHAMPAGNE */
    [data-theme="burgundy"] {
      --color-primary: #831843;
      --color-primary-dark: #500724;
      --color-primary-light: #be185d;
      --color-primary-subtle: #fdf2f8;
      --color-primary-border: #fbcfe8;
      --color-primary-text: #700732;
      --shadow-hero: 0 12px 36px -8px rgba(15, 23, 42, 0.25);
    }

    /* THEME PRESET: PORCELAIN & SLATE */
    [data-theme="slate"] {
      --color-primary: #334155;
      --color-primary-dark: #0f172a;
      --color-primary-light: #64748b;
      --color-primary-subtle: #f8fafc;
      --color-primary-border: #cbd5e1;
      --color-primary-text: #0f172a;
      --shadow-hero: 0 12px 36px -8px rgba(15, 23, 42, 0.25);
    }

    /* THEME PRESET: ATELIER NOIR (OLED Dark Mode) */
    [data-theme="noir"] {
      --bg-page: #090d16;
      --bg-surface: #111827;
      --bg-surface-elevated: #1f2937;
      --bg-surface-muted: #1e293b;
      --bg-sidebar: #0f172a;
      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --text-caption: #94a3b8;
      --border-subtle: rgba(255, 255, 255, 0.1);
      --border-strong: rgba(255, 255, 255, 0.18);
      --divider-color: rgba(255, 255, 255, 0.08);
      --color-primary: #10b981;
      --color-primary-dark: #047857;
      --color-primary-subtle: rgba(16, 185, 129, 0.15);
      --color-primary-border: rgba(16, 185, 129, 0.3);
      --color-primary-text: #6ee7b7;
      --shadow-ambient: 0 2px 8px rgba(0, 0, 0, 0.4), 0 12px 32px rgba(0, 0, 0, 0.5);
      --shadow-hero: 0 16px 40px rgba(0, 0, 0, 0.7);
    }

    /* ==========================================================================
       RESET & TYPOGRAPHY STANDARDS (Strictly >=12px functional text)
       ========================================================================== */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    body {
      font-family: var(--font-body);
      background-color: var(--bg-page);
      color: var(--text-main);
      line-height: 1.5;
      font-size: 14px;
      overflow-x: hidden;
      transition: background-color var(--duration-haptic) var(--ease-haptic), color var(--duration-haptic) var(--ease-haptic);
    }

    button, input, select {
      font-family: inherit;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    .num-tabular {
      font-variant-numeric: tabular-nums;
      letter-spacing: -0.01em;
    }

    /* ==========================================================================
       LAYOUT ARCHITECTURE: MODERN ATELIER WORKSPACE
       ========================================================================== */
    .app-viewport {
      display: flex;
      min-height: 100vh;
      width: 100%;
      position: relative;
    }

    /* FLOATING HARDWARE SIDEBAR */
    .atelier-sidebar {
      width: 272px;
      background-color: var(--bg-sidebar);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      padding: 24px 18px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      z-index: 40;
      transition: all var(--duration-haptic) var(--ease-haptic);
    }

    .brand-cluster {
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 4px 8px 24px 8px;
      border-bottom: 1px solid var(--divider-color);
      margin-bottom: 20px;
    }

    .brand-mark {
      width: 44px;
      height: 44px;
      border-radius: var(--radius-inner);
      background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 700;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
    }

    .brand-meta h1 {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.01em;
      line-height: 1.2;
    }

    .brand-meta p {
      font-size: 12.5px;
      color: var(--text-muted);
      letter-spacing: 0.04em;
      font-weight: 500;
      margin-top: 2px;
    }

    .nav-group-title {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-caption);
      font-weight: 700;
      padding: 12px 12px 6px 12px;
    }

    .nav-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-bottom: 16px;
    }

    .nav-link {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 14px;
      border-radius: var(--radius-inner);
      color: var(--text-muted);
      font-weight: 500;
      font-size: 13.5px;
      transition: all 180ms ease;
      cursor: pointer;
    }

    .nav-link:hover {
      background-color: var(--bg-surface-muted);
      color: var(--text-main);
      transform: translateX(2px);
    }

    .nav-link.active {
      background-color: var(--color-primary-subtle);
      color: var(--color-primary-text);
      font-weight: 600;
      box-shadow: inset 0 0 0 1px var(--color-primary-border);
    }

    .nav-icon {
      width: 20px;
      height: 20px;
      flex-shrink: 0;
      stroke-width: 1.8;
    }

    .nav-pill-badge {
      margin-left: auto;
      font-size: 12px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 9999px;
      background-color: var(--color-primary);
      color: #ffffff;
    }

    /* Counter Status Card in Sidebar Bottom */
    .sidebar-shift-card {
      margin-top: auto;
      padding: 14px;
      border-radius: var(--radius-inner);
      background-color: var(--bg-surface-muted);
      border: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .shift-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .shift-live-indicator {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
      color: var(--color-primary-text);
    }

    .live-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: var(--color-primary);
    }

    /* ==========================================================================
       MAIN CONTENT STAGE
       ========================================================================== */
    .app-main {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
      padding-bottom: 60px;
    }

    .atelier-topbar {
      height: 72px;
      background-color: var(--bg-surface);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 32px;
      position: sticky;
      top: 0;
      z-index: 30;
      backdrop-filter: blur(12px);
    }

    .search-omni-box {
      display: flex;
      align-items: center;
      gap: 10px;
      background-color: var(--bg-surface-muted);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-button);
      padding: 8px 16px;
      width: 380px;
      transition: all 200ms ease;
    }

    .search-omni-box:focus-within {
      background-color: var(--bg-surface);
      border-color: var(--color-primary);
      box-shadow: 0 0 0 3px var(--color-primary-subtle);
    }

    .search-omni-box input {
      border: none;
      background: transparent;
      outline: none;
      color: var(--text-main);
      font-size: 13.5px;
      width: 100%;
    }

    .kbd-shortcut {
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--text-caption);
      background-color: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 1px 6px;
    }

    .topbar-actions {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .btn-island-primary {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
      color: #ffffff;
      padding: 8px 18px;
      border-radius: var(--radius-button);
      border: none;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: var(--shadow-ambient);
      transition: transform 150ms ease, box-shadow 150ms ease;
    }

    .btn-island-primary:hover {
      transform: translateY(-1px);
      box-shadow: var(--shadow-float);
    }

    .btn-trailing-icon-circle {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background-color: rgba(255, 255, 255, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .avatar-couturier {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 4px 10px;
      border-radius: var(--radius-button);
      background-color: var(--bg-surface-muted);
      border: 1px solid var(--border-subtle);
      cursor: pointer;
    }

    .avatar-img {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #0f172a;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 13px;
    }

    /* ==========================================================================
       DASHBOARD STAGE
       ========================================================================== */
    .dashboard-container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 28px 32px;
      display: flex;
      flex-direction: column;
      gap: var(--spacing-grid-gap);
      width: 100%;
    }

    /* Card Primitive (Single-surface clean enclosure, no card-in-card) */
    .atelier-card {
      background-color: var(--bg-surface);
      border-radius: var(--radius-card);
      border: 1px solid var(--border-subtle);
      box-shadow: var(--shadow-ambient);
      padding: var(--spacing-card-pad);
      position: relative;
      transition: background-color var(--duration-haptic) var(--ease-haptic), border-color var(--duration-haptic) var(--ease-haptic);
    }

    /* 1. INVENZA HERO GREETING ISLAND (Deep Pine Velvet) */
    .invenza-hero-island {
      background: linear-gradient(145deg, #022018 0%, #064e3b 60%, #047857 100%);
      color: #ffffff;
      border-radius: var(--radius-card);
      padding: 30px 36px;
      position: relative;
      box-shadow: var(--shadow-hero);
      display: flex;
      flex-direction: column;
      gap: 22px;
      overflow: hidden;
    }

    .invenza-hero-island::after {
      content: "";
      position: absolute;
      top: -60px;
      right: -40px;
      width: 320px;
      height: 320px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
      border-radius: 50%;
      pointer-events: none;
    }

    .hero-top-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
      z-index: 2;
    }

    .hero-salutation-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background-color: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 4px 14px;
      border-radius: 9999px;
      font-size: 12.5px;
      font-weight: 500;
      color: #f0fdf4;
      backdrop-filter: blur(8px);
      margin-bottom: 8px;
    }

    .hero-title {
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.01em;
      color: #ffffff;
      line-height: 1.25;
    }

    .hero-subtitle {
      font-size: 14.5px;
      color: #e2e8f0;
      max-width: 640px;
      margin-top: 4px;
      font-weight: 400;
    }

    .hero-inventory-strip {
      display: flex;
      align-items: center;
      gap: 16px;
      background-color: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: var(--radius-inner);
      padding: 12px 20px;
      backdrop-filter: blur(12px);
    }

    .hero-stat-cell {
      display: flex;
      flex-direction: column;
      padding: 0 14px;
      border-right: 1px solid rgba(255, 255, 255, 0.16);
    }

    .hero-stat-cell:last-child {
      border-right: none;
    }

    .hero-stat-value {
      font-size: 20px;
      font-weight: 700;
      font-family: var(--font-body);
      color: #ffffff;
    }

    .hero-stat-label {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #a7f3d0;
      font-weight: 600;
    }

    .hero-actions-row {
      display: flex;
      align-items: center;
      gap: 12px;
      position: relative;
      z-index: 2;
    }

    .hero-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 18px;
      border-radius: var(--radius-button);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid rgba(255, 255, 255, 0.3);
      background-color: rgba(0, 0, 0, 0.25);
      color: #ffffff;
      backdrop-filter: blur(8px);
      transition: all 180ms ease;
    }

    .hero-btn:hover {
      background-color: rgba(255, 255, 255, 0.2);
      border-color: rgba(255, 255, 255, 0.45);
      transform: translateY(-1px);
    }

    .hero-btn-solid {
      background-color: #ffffff;
      color: #064e3b;
      border-color: #ffffff;
    }

    .hero-btn-solid:hover {
      background-color: #ecfdf5;
      color: #022018;
    }

    /* 2. KPI CARDS: 4-POD METRIC GRID (No nested card hierarchy) */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: var(--spacing-grid-gap);
    }

    .kpi-card {
      background-color: var(--bg-surface);
      border-radius: var(--radius-card);
      border: 1px solid var(--border-subtle);
      padding: 22px;
      box-shadow: var(--shadow-ambient);
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: relative;
      transition: transform 200ms ease, box-shadow 200ms ease;
    }

    .kpi-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-float);
    }

    .kpi-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .kpi-icon-pill {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .kpi-icon-pill.emerald {
      background-color: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }

    .kpi-icon-pill.navy {
      background-color: #f0f9ff;
      color: #075985;
      border: 1px solid #bae6fd;
    }

    .kpi-icon-pill.amber {
      background-color: #fffbeb;
      color: #78350f;
      border: 1px solid #fde68a;
    }

    .kpi-icon-pill.rose {
      background-color: #fff1f2;
      color: #9f1239;
      border: 1px solid #fecdd3;
    }

    .kpi-trend-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12.5px;
      font-weight: 600;
      padding: 3px 9px;
      border-radius: 9999px;
    }

    .trend-up {
      background-color: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }

    .trend-warning {
      background-color: #fffbeb;
      color: #78350f;
      border: 1px solid #fde68a;
    }

    .kpi-label {
      font-size: 13.5px;
      font-weight: 500;
      color: var(--text-muted);
    }

    .kpi-number {
      font-size: 26px;
      font-weight: 700;
      font-family: var(--font-body);
      color: var(--text-main);
      line-height: 1.1;
    }

    .kpi-caption {
      font-size: 12.5px;
      color: var(--text-caption);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* 3. ANALYTICS SPLIT (Dual-Spline Area Chart & Donut) */
    .analytics-split-grid {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: var(--spacing-grid-gap);
    }

    .chart-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
    }

    .chart-header-left h3 {
      font-family: var(--font-display);
      font-size: 19px;
      font-weight: 700;
      color: var(--text-main);
    }

    .chart-header-left p {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .pill-segmented-control {
      display: inline-flex;
      background-color: var(--bg-surface-muted);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-button);
      padding: 3px;
      gap: 2px;
    }

    .segment-tab {
      border: none;
      background: transparent;
      padding: 5px 14px;
      font-size: 12.5px;
      font-weight: 500;
      color: var(--text-muted);
      border-radius: var(--radius-button);
      cursor: pointer;
      transition: all 150ms ease;
    }

    .segment-tab.active {
      background-color: var(--bg-surface);
      color: var(--text-main);
      font-weight: 600;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }

    .chart-canvas-wrapper {
      position: relative;
      height: 290px;
      width: 100%;
    }

    .donut-breakdown-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 18px;
    }

    .donut-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 13.5px;
    }

    .donut-bullet {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    .donut-meta {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* 4. BESPOKE OPERATIONS: FITTINGS PIPELINE & RECENT ORDERS TABLE */
    .section-tab-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--divider-color);
      padding-bottom: 14px;
      margin-bottom: 18px;
    }

    .nav-tabs-cluster {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .surface-tab {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 18px;
      border-radius: var(--radius-button);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      background-color: transparent;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 180ms ease;
    }

    .surface-tab.active {
      background-color: var(--color-primary-subtle);
      color: var(--color-primary-text);
      border-color: var(--color-primary-border);
    }

    /* KANBAN BOARD */
    .kanban-board {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }

    .kanban-col {
      background-color: var(--bg-surface-muted);
      border-radius: var(--radius-inner);
      border: 1px solid var(--border-subtle);
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .kanban-col-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-bottom: 6px;
    }

    .col-title-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .col-status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .col-title {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-main);
    }

    .col-count-pill {
      font-size: 12px;
      font-weight: 600;
      background-color: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      padding: 2px 8px;
      border-radius: 9999px;
      color: var(--text-muted);
    }

    .kanban-card {
      background-color: var(--bg-surface);
      border-radius: 10px;
      border: 1px solid var(--border-subtle);
      padding: 14px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
      display: flex;
      flex-direction: column;
      gap: 8px;
      cursor: grab;
      transition: transform 180ms ease, box-shadow 180ms ease;
    }

    .kanban-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-ambient);
    }

    .kanban-card-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-main);
    }

    .kanban-card-meta {
      font-size: 12.5px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .client-micro-avatar {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: #064e3b;
      color: #ffffff;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* DATA TABLE */
    .table-container {
      width: 100%;
      overflow-x: auto;
    }

    .luxury-data-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }

    .luxury-data-table th {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      font-weight: 700;
      padding: 12px 16px;
      border-bottom: 1px solid var(--divider-color);
      background-color: var(--bg-surface-muted);
    }

    .luxury-data-table td {
      padding: 14px 16px;
      border-bottom: 1px solid var(--divider-color);
      font-size: 13.5px;
      vertical-align: middle;
    }

    .luxury-data-table tr:hover td {
      background-color: var(--bg-surface-muted);
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 12.5px;
      font-weight: 600;
    }

    .status-badge.paid {
      background-color: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
    }

    .status-badge.trial {
      background-color: #fffbeb;
      color: #78350f;
      border: 1px solid #fde68a;
    }

    .status-badge.basting {
      background-color: #f0f9ff;
      color: #075985;
      border: 1px solid #bae6fd;
    }

    .action-icon-btn {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: transparent;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 150ms ease;
    }

    .action-icon-btn:hover {
      background-color: var(--bg-surface-muted);
      color: var(--text-main);
      border-color: var(--text-muted);
    }

    /* ==========================================================================
       FINE-TUNING DRAWER CONTROLS
       ========================================================================== */
    .studio-toggle-trigger {
      position: fixed;
      bottom: 28px;
      right: 28px;
      z-index: 100;
      display: flex;
      align-items: center;
      gap: 10px;
      background: #0f172a;
      color: #ffffff;
      padding: 12px 22px;
      border-radius: 9999px;
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
      cursor: pointer;
      font-size: 13.5px;
      font-weight: 600;
      transition: all 220ms var(--ease-haptic);
    }

    .studio-toggle-trigger:hover {
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
    }

    .studio-drawer {
      position: fixed;
      top: 0;
      right: -420px;
      width: 420px;
      height: 100vh;
      background-color: var(--bg-surface);
      border-left: 1px solid var(--border-strong);
      box-shadow: -10px 0 40px rgba(0, 0, 0, 0.15);
      z-index: 110;
      display: flex;
      flex-direction: column;
      transition: right 360ms var(--ease-haptic);
    }

    .studio-drawer.open {
      right: 0;
    }

    .studio-header {
      padding: 22px 24px;
      border-bottom: 1px solid var(--divider-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background-color: var(--bg-surface-muted);
    }

    .studio-header h2 {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 700;
      color: var(--text-main);
    }

    .studio-close-btn {
      background: transparent;
      border: none;
      cursor: pointer;
      color: var(--text-caption);
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
    }

    .studio-close-btn:hover {
      background-color: rgba(0, 0, 0, 0.05);
      color: var(--text-main);
    }

    .studio-body {
      padding: 24px;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 26px;
    }

    .control-section {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .control-section-title {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 700;
      color: var(--text-caption);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .theme-pill-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }

    .theme-select-card {
      padding: 10px 12px;
      border-radius: var(--radius-inner);
      border: 1px solid var(--border-subtle);
      background-color: var(--bg-surface);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13px;
      font-weight: 600;
      transition: all 180ms ease;
    }

    .theme-select-card.active {
      border-color: var(--color-primary);
      background-color: var(--color-primary-subtle);
      color: var(--color-primary-text);
      box-shadow: 0 0 0 1px var(--color-primary);
    }

    .theme-swatch {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    .slider-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .slider-label-wrap {
      display: flex;
      justify-content: space-between;
      font-size: 13.5px;
      font-weight: 500;
      color: var(--text-main);
    }

    .slider-label-val {
      font-family: var(--font-mono);
      font-size: 12.5px;
      color: var(--text-muted);
    }

    .range-input {
      width: 100%;
      accent-color: var(--color-primary);
      height: 6px;
      background: var(--bg-surface-muted);
      border-radius: 9999px;
      outline: none;
    }

    .custom-select {
      width: 100%;
      padding: 9px 14px;
      border-radius: var(--radius-inner);
      border: 1px solid var(--border-strong);
      background-color: var(--bg-surface);
      color: var(--text-main);
      font-size: 13.5px;
      font-weight: 500;
      outline: none;
    }

    .studio-footer {
      padding: 18px 24px;
      border-top: 1px solid var(--divider-color);
      display: flex;
      flex-direction: column;
      gap: 10px;
      background-color: var(--bg-surface-muted);
    }

    .btn-export-tokens {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 11px;
      border-radius: var(--radius-button);
      background-color: var(--text-main);
      color: var(--bg-surface);
      border: none;
      font-weight: 600;
      font-size: 13.5px;
      cursor: pointer;
      transition: opacity 150ms ease;
    }

    .btn-export-tokens:hover {
      opacity: 0.9;
    }

    @media (max-width: 1080px) {
      .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
      }
      .analytics-split-grid {
        grid-template-columns: 1fr;
      }
      .kanban-board {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    @media (max-width: 768px) {
      .atelier-sidebar {
        display: none;
      }
      .kpi-grid {
        grid-template-columns: 1fr;
      }
      .kanban-board {
        grid-template-columns: 1fr;
      }
      .dashboard-container {
        padding: 16px;
      }
      .invenza-hero-island {
        padding: 20px;
      }
      .hero-inventory-strip {
        flex-direction: column;
        align-items: flex-start;
      }
      .hero-stat-cell {
        border-right: none;
        border-bottom: 1px solid rgba(255, 255, 255, 0.16);
        padding: 6px 0;
        width: 100%;
      }
    }
  </style>
</head>

<body data-theme="invenza">

  <div class="app-viewport">
    
    <!-- 1. FLOATING HARDWARE SIDEBAR -->
    <aside class="atelier-sidebar" id="sidebar">
      <div class="brand-cluster">
        <div class="brand-mark">A</div>
        <div class="brand-meta">
          <h1>Aleen Couture</h1>
          <p>Haute Atelier &bull; Hyderabad</p>
        </div>
      </div>

      <div class="nav-group-title">Core Operations</div>
      <ul class="nav-list">
        <li>
          <a class="nav-link active" onclick="switchMainTab('dashboard')">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="7" height="7" rx="2"></rect>
              <rect x="14" y="3" width="7" height="7" rx="2"></rect>
              <rect x="14" y="14" width="7" height="7" rx="2"></rect>
              <rect x="3" y="14" width="7" height="7" rx="2"></rect>
            </svg>
            <span>Atelier Dashboard</span>
          </a>
        </li>
        <li>
          <a class="nav-link" onclick="switchMainTab('fittings')">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
            <span>Bespoke Fittings</span>
            <span class="nav-pill-badge">8 Today</span>
          </a>
        </li>
        <li>
          <a class="nav-link" onclick="switchMainTab('orders')">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path>
              <path d="M3 6h18"></path>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
            <span>Client Ensembles</span>
          </a>
        </li>
        <li>
          <a class="nav-link" onclick="switchMainTab('pos')">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="2" y="4" width="20" height="16" rx="2"></rect>
              <line x1="2" y1="10" x2="22" y2="10"></line>
            </svg>
            <span>Point of Sale</span>
          </a>
        </li>
      </ul>

      <div class="nav-group-title">Silks & Inventory</div>
      <ul class="nav-list">
        <li>
          <a class="nav-link" href="#silks">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="m7.5 4.27 9 5.15"></path>
              <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"></path>
            </svg>
            <span>Handloom Silks</span>
          </a>
        </li>
        <li>
          <a class="nav-link" href="#karigars">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <span>Karigars & Artisans</span>
          </a>
        </li>
      </ul>

      <div class="sidebar-shift-card">
        <div class="shift-header">
          <span style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--text-caption);">Counter Shift</span>
          <div class="shift-live-indicator">
            <span class="live-dot"></span> Active
          </div>
        </div>
        <div style="font-size: 15px; font-weight: 700; color: var(--text-main);" class="num-tabular">
          ₹1,84,500 <span style="font-size: 12.5px; font-weight: 500; color: var(--text-muted);">in drawer</span>
        </div>
        <div style="font-size: 12.5px; color: var(--text-muted);">
          Register #1 &bull; Jubilee Hills
        </div>
      </div>
    </aside>

    <!-- 2. MAIN STAGE -->
    <main class="app-main">
      <header class="atelier-topbar">
        <div class="search-omni-box">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--text-caption);">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </svg>
          <input type="text" placeholder="Search brides, lehengas, measurements (try 'Ayesha' or 'INV-882')..." />
          <span class="kbd-shortcut">⌘K</span>
        </div>

        <div class="topbar-actions">
          <button class="btn-island-primary" onclick="alert('Launching Rapid POS Counter...')">
            <span>New Sale & Invoice</span>
            <span class="btn-trailing-icon-circle">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </span>
          </button>

          <div class="avatar-couturier" onclick="toggleStudioDrawer()">
            <div class="avatar-img">FM</div>
            <div style="display: flex; flex-direction: column; text-align: left; padding-right: 4px;">
              <span style="font-size: 13px; font-weight: 600; color: var(--text-main);">Fahim Ahmed</span>
              <span style="font-size: 12px; color: var(--text-caption);">Master Couturier</span>
            </div>
          </div>
        </div>
      </header>

      <!-- DASHBOARD WRAPPER -->
      <div class="dashboard-container">
        
        <!-- SECTION 1: INVENZA HERO GREETING ISLAND -->
        <section class="invenza-hero-island" id="heroIsland">
          <div class="hero-top-row">
            <div>
              <div class="hero-salutation-badge">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
                <span>Aleen Jubilee Hills Flagship &bull; Haute Atelier</span>
              </div>
              <h2 class="hero-title">Welcome to the Atelier, Master Tailor Fahim</h2>
              <p class="hero-subtitle">
                18 bespoke bridal fittings scheduled today. 4 master karigar zardozi embroidery ensembles are awaiting final trial verification.
              </p>
            </div>

            <div class="hero-inventory-strip">
              <div class="hero-stat-cell">
                <span class="hero-stat-value num-tabular">1,420</span>
                <span class="hero-stat-label">Catalog Silks</span>
              </div>
              <div class="hero-stat-cell">
                <span class="hero-stat-value num-tabular">28</span>
                <span class="hero-stat-label">In Basting</span>
              </div>
              <div class="hero-stat-cell">
                <span class="hero-stat-value num-tabular">6</span>
                <span class="hero-stat-label">Trials Due</span>
              </div>
              <div class="hero-stat-cell">
                <span class="hero-stat-value num-tabular" style="color: #fde68a;">2</span>
                <span class="hero-stat-label">Rush Orders</span>
              </div>
            </div>
          </div>

          <div class="hero-actions-row">
            <button class="hero-btn hero-btn-solid" onclick="switchMainTab('fittings')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <span>Today's Fitting Roster (8)</span>
            </button>
            <button class="hero-btn" onclick="alert('Opening Custom Measurement Sheet...')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <path d="M12 5v14M5 12h14"></path>
              </svg>
              <span>Record New Bride Measurement</span>
            </button>
            <button class="hero-btn" onclick="alert('Generating Atelier Shift Summary...')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              <span>Export Daily Register</span>
            </button>
          </div>
        </section>

        <!-- SECTION 2: 4-POD METRIC GRID (Clean single-layer card structure) -->
        <section class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-head">
              <div class="kpi-icon-pill emerald">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="1" x2="12" y2="23"></line>
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
              </div>
              <span class="kpi-trend-pill trend-up">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                  <polyline points="17 6 23 6 23 12"></polyline>
                </svg>
                +18.4%
              </span>
            </div>
            <div>
              <span class="kpi-label">Gross Atelier Sales MTD</span>
              <div class="kpi-number num-tabular">₹14,85,400</div>
            </div>
            <div class="kpi-caption">
              <span>vs ₹12,54,000 last month</span>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-head">
              <div class="kpi-icon-pill navy">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path>
                  <path d="M3 6h18"></path>
                </svg>
              </div>
              <span class="kpi-trend-pill trend-up">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <polyline points="23 6 13.5 15.5 8.5 10.5 18"></polyline>
                  <polyline points="17 6 23 6 23 12"></polyline>
                </svg>
                +12.5%
              </span>
            </div>
            <div>
              <span class="kpi-label">Active Bridal Ensembles</span>
              <div class="kpi-number num-tabular">42 Units</div>
            </div>
            <div class="kpi-caption">
              <span>28 in embroidery &bull; 14 in trial</span>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-head">
              <div class="kpi-icon-pill amber">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
              </div>
              <span class="kpi-trend-pill trend-up">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                  <polyline points="17 6 23 6 23 12"></polyline>
                </svg>
                +4.8%
              </span>
            </div>
            <div>
              <span class="kpi-label">Average Ensemble Ticket</span>
              <div class="kpi-number num-tabular">₹35,360</div>
            </div>
            <div class="kpi-caption">
              <span>Haute couture lehengas average</span>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-head">
              <div class="kpi-icon-pill rose">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>
              <span class="kpi-trend-pill trend-warning">
                Action Required
              </span>
            </div>
            <div>
              <span class="kpi-label">Fittings Due in 48 Hours</span>
              <div class="kpi-number num-tabular" style="color: #9f1239;">7 Brides</div>
            </div>
            <div class="kpi-caption">
              <span>3 bridal weddings this weekend</span>
            </div>
          </div>
        </section>

        <!-- SECTION 3: ANALYTICS COMPARISON (Dual-Spline Area Chart & Donut) -->
        <section class="analytics-split-grid">
          <div class="atelier-card">
            <div class="chart-card-header">
              <div class="chart-header-left">
                <h3>Haute Couture vs Prêt-à-Porter Revenue</h3>
                <p>Weekly revenue progression comparison against previous cycle</p>
              </div>
              <div class="pill-segmented-control">
                <button class="segment-tab active" onclick="setChartCycle('7d', this)">7 Days</button>
                <button class="segment-tab" onclick="setChartCycle('30d', this)">30 Days</button>
                <button class="segment-tab" onclick="setChartCycle('90d', this)">Quarterly</button>
              </div>
            </div>

            <div class="chart-canvas-wrapper">
              <canvas id="revenueDualSplineChart"></canvas>
            </div>
          </div>

          <div class="atelier-card">
            <div class="chart-card-header">
              <div class="chart-header-left">
                <h3>Popular Silhouette Share</h3>
                <p>Revenue distribution by ensemble</p>
              </div>
            </div>

            <div style="position: relative; height: 180px; width: 100%;">
              <canvas id="categoryDonutChart"></canvas>
            </div>

            <div class="donut-breakdown-list">
              <div class="donut-item">
                <div class="donut-meta">
                  <span class="donut-bullet" style="background-color: #047857;"></span>
                  <span style="font-weight: 500; color: var(--text-main);">Bridal Lehengas</span>
                </div>
                <span class="num-tabular" style="font-weight: 600; color: var(--text-main);">45% &bull; ₹6.68L</span>
              </div>
              <div class="donut-item">
                <div class="donut-meta">
                  <span class="donut-bullet" style="background-color: #0369a1;"></span>
                  <span style="font-weight: 500; color: var(--text-main);">Zardozi Sherwanis</span>
                </div>
                <span class="num-tabular" style="font-weight: 600; color: var(--text-main);">28% &bull; ₹4.15L</span>
              </div>
              <div class="donut-item">
                <div class="donut-meta">
                  <span class="donut-bullet" style="background-color: #92400e;"></span>
                  <span style="font-weight: 500; color: var(--text-main);">Anarkali Gowns</span>
                </div>
                <span class="num-tabular" style="font-weight: 600; color: var(--text-main);">17% &bull; ₹2.52L</span>
              </div>
              <div class="donut-item">
                <div class="donut-meta">
                  <span class="donut-bullet" style="background-color: #475569;"></span>
                  <span style="font-weight: 500; color: var(--text-main);">Handloom Silks</span>
                </div>
                <span class="num-tabular" style="font-weight: 600; color: var(--text-main);">10% &bull; ₹1.50L</span>
              </div>
            </div>
          </div>
        </section>

        <!-- SECTION 4: BESPOKE OPERATIONS (KANBAN vs DATA GRID) -->
        <section class="atelier-card">
          <div class="section-tab-nav">
            <div class="nav-tabs-cluster">
              <button class="surface-tab active" id="tabKanbanBtn" onclick="toggleSubView('kanban')">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="7" height="18" rx="1"></rect>
                  <rect x="14" y="3" width="7" height="10" rx="1"></rect>
                </svg>
                <span>Bespoke Fitting Kanban (4 Stages)</span>
              </button>
              <button class="surface-tab" id="tabOrdersBtn" onclick="toggleSubView('orders')">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="8" y1="6" x2="21" y2="6"></line>
                  <line x1="8" y1="12" x2="21" y2="12"></line>
                  <line x1="8" y1="18" x2="21" y2="18"></line>
                  <line x1="3" y1="6" x2="3.01" y2="6"></line>
                  <line x1="3" y1="12" x2="3.01" y2="12"></line>
                  <line x1="3" y1="18" x2="3.01" y2="18"></line>
                </svg>
                <span>Client Ensembles Data Table</span>
              </button>
            </div>

            <div>
              <button class="btn-island-primary" style="padding: 6px 14px; font-size: 13px;" onclick="alert('Adding Bespoke Commission...')">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <span>Add Custom Commission</span>
              </button>
            </div>
          </div>

          <!-- VIEW A: KANBAN BOARD -->
          <div id="subViewKanban" class="kanban-board">
            <div class="kanban-col">
              <div class="kanban-col-head">
                <div class="col-title-wrap">
                  <span class="col-status-dot" style="background-color: #475569;"></span>
                  <span class="col-title">Fabric & Dyeing</span>
                </div>
                <span class="col-count-pill">6</span>
              </div>

              <div class="kanban-card">
                <div class="kanban-card-title">Crimson Banarasi Raw Silk</div>
                <div style="font-size: 12.5px; color: var(--text-caption);">Bride: Dr. Ananya Rao &bull; #AL-901</div>
                <div class="kanban-card-meta">
                  <span class="status-badge trial">Dye Vat #2</span>
                  <div class="client-micro-avatar">AR</div>
                </div>
              </div>

              <div class="kanban-card">
                <div class="kanban-card-title">Sage Organza Dupatta</div>
                <div style="font-size: 12.5px; color: var(--text-caption);">Patron: Meera Varma &bull; #AL-908</div>
                <div class="kanban-card-meta">
                  <span class="status-badge trial">Weave Sourcing</span>
                  <div class="client-micro-avatar" style="background:#0369a1;">MV</div>
                </div>
              </div>
            </div>

            <div class="kanban-col">
              <div class="kanban-col-head">
                <div class="col-title-wrap">
                  <span class="col-status-dot" style="background-color: #0369a1;"></span>
                  <span class="col-title">Karigar Zardozi Work</span>
                </div>
                <span class="col-count-pill">12</span>
              </div>

              <div class="kanban-card">
                <div class="kanban-card-title">Imperial Velvet Sherwani</div>
                <div style="font-size: 12.5px; color: var(--text-caption);">Groom: Rohan Kapoor &bull; #AL-884</div>
                <div class="kanban-card-meta">
                  <span class="status-badge basting">Master Ismail</span>
                  <div class="client-micro-avatar" style="background:#1e40af;">RK</div>
                </div>
              </div>

              <div class="kanban-card">
                <div class="kanban-card-title">Dhabka Embroidery Lehenga</div>
                <div style="font-size: 12.5px; color: var(--text-caption);">Bride: Fatima Zehra &bull; #AL-890</div>
                <div class="kanban-card-meta">
                  <span class="status-badge basting">85% Complete</span>
                  <div class="client-micro-avatar" style="background:#92400e;">FZ</div>
                </div>
              </div>
            </div>

            <div class="kanban-col">
              <div class="kanban-col-head">
                <div class="col-title-wrap">
                  <span class="col-status-dot" style="background-color: #92400e;"></span>
                  <span class="col-title">First Trial Fitting</span>
                </div>
                <span class="col-count-pill">8</span>
              </div>

              <div class="kanban-card">
                <div class="kanban-card-title">Rose Dust Bridal Ensemble</div>
                <div style="font-size: 12.5px; color: var(--text-caption);">Bride: Sneha Reddy &bull; #AL-875</div>
                <div class="kanban-card-meta">
                  <span class="status-badge trial">Today 4:30 PM</span>
                  <div class="client-micro-avatar" style="background:#047857;">SR</div>
                </div>
              </div>

              <div class="kanban-card">
                <div class="kanban-card-title">Emerald Silk Anarkali</div>
                <div style="font-size: 12.5px; color: var(--text-caption);">VIP: Smt. Gayatri Devi &bull; #AL-879</div>
                <div class="kanban-card-meta">
                  <span class="status-badge trial">Tomorrow 11 AM</span>
                  <div class="client-micro-avatar" style="background:#065f46;">GD</div>
                </div>
              </div>
            </div>

            <div class="kanban-col">
              <div class="kanban-col-head">
                <div class="col-title-wrap">
                  <span class="col-status-dot" style="background-color: #047857;"></span>
                  <span class="col-title">Final QC & Ready</span>
                </div>
                <span class="col-count-pill">4</span>
              </div>

              <div class="kanban-card">
                <div class="kanban-card-title">Champagne Gold Lehenga</div>
                <div style="font-size: 12.5px; color: var(--text-caption);">Bride: Ayesha Khan &bull; #AL-862</div>
                <div class="kanban-card-meta">
                  <span class="status-badge paid">Box Packed</span>
                  <div class="client-micro-avatar" style="background:#047857;">AK</div>
                </div>
              </div>
            </div>
          </div>

          <!-- VIEW B: DATA TABLE -->
          <div id="subViewOrders" class="table-container" style="display: none;">
            <table class="luxury-data-table">
              <thead>
                <tr>
                  <th>Order Code</th>
                  <th>Patron Name</th>
                  <th>Ensemble Description</th>
                  <th>Master Artisan</th>
                  <th>Scheduled Trial</th>
                  <th>Total Valuation</th>
                  <th>Financial Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="num-tabular" style="font-weight: 600; color: var(--text-main);">#AL-862</td>
                  <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <div class="client-micro-avatar">AK</div>
                      <div>
                        <div style="font-weight: 600; color: var(--text-main);">Ayesha Khan</div>
                        <div style="font-size: 12.5px; color: var(--text-caption);">Bride &bull; Banjara Hills</div>
                      </div>
                    </div>
                  </td>
                  <td>Zardozi Bridal Lehenga in Champagne Gold</td>
                  <td>Master Fahim</td>
                  <td class="num-tabular">Completed (Ready)</td>
                  <td class="num-tabular" style="font-weight: 700; color: var(--text-main);">₹1,85,000</td>
                  <td><span class="status-badge paid">Paid in Full</span></td>
                  <td>
                    <button class="action-icon-btn" title="View Measurement Sheet" onclick="alert('Viewing measurements for Ayesha Khan')">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                    <button class="action-icon-btn" title="Print Invoice" onclick="alert('Printing Tax Invoice #AL-862')">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 6 2 18 2 18 9"></polyline>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                        <rect x="6" y="14" width="12" height="8"></rect>
                      </svg>
                    </button>
                  </td>
                </tr>

                <tr>
                  <td class="num-tabular" style="font-weight: 600; color: var(--text-main);">#AL-875</td>
                  <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <div class="client-micro-avatar" style="background:#0369a1;">SR</div>
                      <div>
                        <div style="font-weight: 600; color: var(--text-main);">Sneha Reddy</div>
                        <div style="font-size: 12.5px; color: var(--text-caption);">Bride &bull; Jubilee Hills</div>
                      </div>
                    </div>
                  </td>
                  <td>Rose Dust Heritage Silk Lehenga</td>
                  <td>Master Ismail</td>
                  <td class="num-tabular">Today &bull; 4:30 PM</td>
                  <td class="num-tabular" style="font-weight: 700; color: var(--text-main);">₹1,40,000</td>
                  <td><span class="status-badge trial">50% Advance</span></td>
                  <td>
                    <button class="action-icon-btn" title="View Measurement Sheet">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                    <button class="action-icon-btn" title="Print Invoice">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 6 2 18 2 18 9"></polyline>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                        <rect x="6" y="14" width="12" height="8"></rect>
                      </svg>
                    </button>
                  </td>
                </tr>

                <tr>
                  <td class="num-tabular" style="font-weight: 600; color: var(--text-main);">#AL-884</td>
                  <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <div class="client-micro-avatar" style="background:#1e40af;">RK</div>
                      <div>
                        <div style="font-weight: 600; color: var(--text-main);">Rohan Kapoor</div>
                        <div style="font-size: 12.5px; color: var(--text-caption);">Groom &bull; Madhapur</div>
                      </div>
                    </div>
                  </td>
                  <td>Imperial Velvet & Zari Sherwani</td>
                  <td>Master Fahim</td>
                  <td class="num-tabular">Nov 04, 2026</td>
                  <td class="num-tabular" style="font-weight: 700; color: var(--text-main);">₹95,000</td>
                  <td><span class="status-badge basting">Work in Progress</span></td>
                  <td>
                    <button class="action-icon-btn" title="View Measurement Sheet">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                    <button class="action-icon-btn" title="Print Invoice">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 6 2 18 2 18 9"></polyline>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                        <rect x="6" y="14" width="12" height="8"></rect>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>

  </div>

  <!-- TRIGGER BUTTON: FINE-TUNE EVERYTHING -->
  <button class="studio-toggle-trigger" onclick="toggleStudioDrawer()">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="3"></circle>
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
    </svg>
    <span>Fine-Tune Everything</span>
  </button>

  <!-- DRAWER PANEL: FULL TOKEN TUNER -->
  <aside class="studio-drawer" id="studioDrawer">
    <div class="studio-header">
      <div>
        <h2>Atelier Fine-Tuning Studio</h2>
        <p style="font-size: 12.5px; color: var(--text-caption);">Live token adjustment & visual calibration</p>
      </div>
      <button class="studio-close-btn" onclick="toggleStudioDrawer()" title="Close drawer">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <div class="studio-body">
      
      <!-- 1. Theme Presets (References 1 to 5) -->
      <div class="control-section">
        <span class="control-section-title">Aesthetic Preset (Inspired by References)</span>
        <div class="theme-pill-grid">
          <div class="theme-select-card active" onclick="applyThemePreset('invenza', this)">
            <span class="theme-swatch" style="background: linear-gradient(135deg, #064e3b, #10b981);"></span>
            <span>Invenza Emerald</span>
          </div>
          <div class="theme-select-card" onclick="applyThemePreset('navy', this)">
            <span class="theme-swatch" style="background: linear-gradient(135deg, #172554, #3b82f6);"></span>
            <span>Royal Navy</span>
          </div>
          <div class="theme-select-card" onclick="applyThemePreset('burgundy', this)">
            <span class="theme-swatch" style="background: linear-gradient(135deg, #500724, #be185d);"></span>
            <span>Haute Burgundy</span>
          </div>
          <div class="theme-select-card" onclick="applyThemePreset('slate', this)">
            <span class="theme-swatch" style="background: linear-gradient(135deg, #0f172a, #64748b);"></span>
            <span>Porcelain & Slate</span>
          </div>
          <div class="theme-select-card" style="grid-column: span 2;" onclick="applyThemePreset('noir', this)">
            <span class="theme-swatch" style="background: linear-gradient(135deg, #090d16, #1f2937); border: 1px solid #475569;"></span>
            <span>Atelier Noir (High-Fashion OLED Dark Mode)</span>
          </div>
        </div>
      </div>

      <!-- 2. Corner Geometry -->
      <div class="control-section">
        <span class="control-section-title">Card Corner Geometry</span>
        <div class="slider-row">
          <div class="slider-label-wrap">
            <span>Card Corner Radius</span>
            <span class="slider-label-val" id="valCardRadius">16px</span>
          </div>
          <input type="range" class="range-input" min="0" max="28" value="16" oninput="updateCardRadius(this.value)">
        </div>
      </div>

      <!-- 3. Shadow Physics & Soft Ambient Diffusion -->
      <div class="control-section">
        <span class="control-section-title">Shadow Physics & Depth</span>
        
        <div class="slider-row">
          <div class="slider-label-wrap">
            <span>Ambient Shadow Softness (Blur)</span>
            <span class="slider-label-val" id="valShadowBlur">24px</span>
          </div>
          <input type="range" class="range-input" min="4" max="48" value="24" oninput="updateShadowBlur(this.value)">
        </div>

        <div class="slider-row">
          <div class="slider-label-wrap">
            <span>Shadow Opacity</span>
            <span class="slider-label-val" id="valShadowOpacity">6%</span>
          </div>
          <input type="range" class="range-input" min="0" max="20" value="6" oninput="updateShadowOpacity(this.value)">
        </div>
      </div>

      <!-- 4. Typography Pairing -->
      <div class="control-section">
        <span class="control-section-title">Editorial Typography Pairing</span>
        <div class="slider-row">
          <label style="font-size: 13.5px; font-weight: 500; color: var(--text-main);">Display Heading Font</label>
          <select class="custom-select" onchange="updateHeadingFont(this.value)">
            <option value="'Playfair Display', Georgia, serif">Playfair Display (Haute Vogue Editorial)</option>
            <option value="'Cormorant Garamond', Georgia, serif">Cormorant Garamond (Royal Heritage)</option>
            <option value="'Outfit', sans-serif">Outfit (Clean Geometric Modern)</option>
            <option value="-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif">Apple SF Pro Display (San Francisco)</option>
          </select>
        </div>
      </div>

      <!-- 5. Ergonomics & Density (POS vs Haute Lounge) -->
      <div class="control-section">
        <span class="control-section-title">Spatial Density & Ergonomics</span>
        <div style="display: flex; gap: 8px;">
          <button class="surface-tab active" style="flex: 1; justify-content: center;" onclick="setDensity('spacious', this)">
            Haute Lounge (Spacious)
          </button>
          <button class="surface-tab" style="flex: 1; justify-content: center;" onclick="setDensity('pos', this)">
            POS Counter (Compact)
          </button>
        </div>
      </div>

      <!-- 6. Component Toggles -->
      <div class="control-section">
        <span class="control-section-title">Surface Components</span>
        <label style="display: flex; align-items: center; justify-content: space-between; font-size: 13.5px; cursor: pointer;">
          <span>Invenza Emerald Greeting Island</span>
          <input type="checkbox" checked onchange="toggleHeroIsland(this.checked)">
        </label>
      </div>

    </div>

    <!-- STUDIO FOOTER: EXPORT TO REACT -->
    <div class="studio-footer">
      <button class="btn-export-tokens" onclick="copyReactTokens()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        <span>Copy Calibrated React Theme Token</span>
      </button>
      <div style="font-size: 12px; color: var(--text-caption); text-align: center;">
        Ready for drop-in into <code>Aleen-react2/src/constants/designSystems.js</code>
      </div>
    </div>
  </aside>

  <!-- JAVASCRIPT CONTROLLERS & CHARTS -->
  <script>
    let revenueChartInstance = null;
    let categoryChartInstance = null;

    function initCharts() {
      const ctxRevenue = document.getElementById('revenueDualSplineChart').getContext('2d');
      
      const gradCurrent = ctxRevenue.createLinearGradient(0, 0, 0, 260);
      gradCurrent.addColorStop(0, 'rgba(4, 120, 87, 0.28)');
      gradCurrent.addColorStop(1, 'rgba(4, 120, 87, 0.0)');

      const gradLast = ctxRevenue.createLinearGradient(0, 0, 0, 260);
      gradLast.addColorStop(0, 'rgba(3, 105, 161, 0.16)');
      gradLast.addColorStop(1, 'rgba(3, 105, 161, 0.0)');

      revenueChartInstance = new Chart(ctxRevenue, {
        type: 'line',
        data: {
          labels: ['Mon 26', 'Tue 27', 'Wed 28', 'Thu 29', 'Fri 30', 'Sat 31', 'Sun 01'],
          datasets: [
            {
              label: 'This Week (Haute Couture)',
              data: [185000, 210000, 165000, 290000, 320000, 485000, 410000],
              borderColor: '#047857',
              backgroundColor: gradCurrent,
              borderWidth: 2.8,
              tension: 0.42,
              fill: true,
              pointBackgroundColor: '#047857',
              pointBorderColor: '#ffffff',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6
            },
            {
              label: 'Last Week (Baseline)',
              data: [140000, 160000, 145000, 210000, 250000, 390000, 330000],
              borderColor: '#94a3b8',
              backgroundColor: gradLast,
              borderWidth: 2,
              borderDash: [5, 5],
              tension: 0.42,
              fill: true,
              pointRadius: 0,
              pointHoverRadius: 5
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top',
              align: 'end',
              labels: {
                boxWidth: 12,
                font: { family: "'Outfit', sans-serif", size: 12.5 },
                color: '#475569'
              }
            },
            tooltip: {
              backgroundColor: '#0f172a',
              titleFont: { family: "'Outfit', sans-serif", size: 13, weight: 'bold' },
              bodyFont: { family: "'Outfit', sans-serif", size: 12.5 },
              padding: 12,
              cornerRadius: 8,
              callbacks: {
                label: function(context) {
                  return context.dataset.label + ': ₹' + Number(context.raw).toLocaleString('en-IN');
                }
              }
            }
          },
          scales: {
            y: {
              grid: { color: 'rgba(15, 23, 42, 0.05)' },
              ticks: {
                color: '#475569',
                font: { family: "'Outfit', sans-serif", size: 12 },
                callback: function(value) { return '₹' + (value / 1000) + 'k'; }
              }
            },
            x: {
              grid: { display: false },
              ticks: {
                color: '#475569',
                font: { family: "'Outfit', sans-serif", size: 12 }
              }
            }
          }
        }
      });

      const ctxDonut = document.getElementById('categoryDonutChart').getContext('2d');
      categoryChartInstance = new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
          labels: ['Bridal Lehengas', 'Zardozi Sherwanis', 'Anarkali Gowns', 'Handloom Silks'],
          datasets: [{
            data: [45, 28, 17, 10],
            backgroundColor: ['#047857', '#0369a1', '#92400e', '#475569'],
            borderWidth: 3,
            borderColor: '#ffffff',
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '72%',
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#0f172a',
              callbacks: {
                label: function(context) {
                  return context.label + ': ' + context.raw + '%';
                }
              }
            }
          }
        }
      });
    }

    function toggleStudioDrawer() {
      const drawer = document.getElementById('studioDrawer');
      drawer.classList.toggle('open');
    }

    function applyThemePreset(themeId, cardElem) {
      document.body.setAttribute('data-theme', themeId);
      document.querySelectorAll('.theme-select-card').forEach(c => c.classList.remove('active'));
      cardElem.classList.add('active');

      if (revenueChartInstance) {
        let primaryHex = '#047857';
        if (themeId === 'navy') primaryHex = '#1e40af';
        if (themeId === 'burgundy') primaryHex = '#831843';
        if (themeId === 'slate') primaryHex = '#334155';
        if (themeId === 'noir') primaryHex = '#10b981';

        revenueChartInstance.data.datasets[0].borderColor = primaryHex;
        revenueChartInstance.data.datasets[0].pointBackgroundColor = primaryHex;
        revenueChartInstance.update();
      }
    }

    function updateCardRadius(val) {
      document.documentElement.style.setProperty('--radius-card', val + 'px');
      document.getElementById('valCardRadius').innerText = val + 'px';
    }

    function updateShadowBlur(val) {
      document.getElementById('valShadowBlur').innerText = val + 'px';
      recalcShadows();
    }

    function updateShadowOpacity(val) {
      document.getElementById('valShadowOpacity').innerText = val + '%';
      recalcShadows();
    }

    function recalcShadows() {
      const blur = document.getElementById('valShadowBlur').innerText.replace('px', '');
      const opacity = parseInt(document.getElementById('valShadowOpacity').innerText.replace('%', '')) / 100;
      const shadowVal = `0 2px 4px rgba(15, 23, 42, ${opacity * 0.6}), 0 ${Math.round(blur/3)}px ${blur}px -4px rgba(15, 23, 42, ${opacity})`;
      document.documentElement.style.setProperty('--shadow-ambient', shadowVal);
    }

    function updateHeadingFont(fontFamily) {
      document.documentElement.style.setProperty('--font-display', fontFamily);
    }

    function setDensity(mode, btn) {
      btn.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      if (mode === 'spacious') {
        document.documentElement.style.setProperty('--spacing-card-pad', '24px');
        document.documentElement.style.setProperty('--spacing-grid-gap', '22px');
      } else {
        document.documentElement.style.setProperty('--spacing-card-pad', '14px');
        document.documentElement.style.setProperty('--spacing-grid-gap', '14px');
      }
    }

    function toggleHeroIsland(show) {
      const hero = document.getElementById('heroIsland');
      hero.style.display = show ? 'flex' : 'none';
    }

    function toggleSubView(view) {
      const kanbanView = document.getElementById('subViewKanban');
      const ordersView = document.getElementById('subViewOrders');
      const tabKanban = document.getElementById('tabKanbanBtn');
      const tabOrders = document.getElementById('tabOrdersBtn');

      if (view === 'kanban') {
        kanbanView.style.display = 'grid';
        ordersView.style.display = 'none';
        tabKanban.classList.add('active');
        tabOrders.classList.remove('active');
      } else {
        kanbanView.style.display = 'none';
        ordersView.style.display = 'block';
        tabKanban.classList.remove('active');
        tabOrders.classList.add('active');
      }
    }

    function switchMainTab(tab) {
      if (tab === 'fittings') {
        toggleSubView('kanban');
      } else if (tab === 'orders') {
        toggleSubView('orders');
      }
    }

    function setChartCycle(cycle, btn) {
      btn.parentElement.querySelectorAll('.segment-tab').forEach(t => t.classList.remove('active'));
      btn.classList.add('active');

      if (cycle === '7d') {
        revenueChartInstance.data.labels = ['Mon 26', 'Tue 27', 'Wed 28', 'Thu 29', 'Fri 30', 'Sat 31', 'Sun 01'];
        revenueChartInstance.data.datasets[0].data = [185000, 210000, 165000, 290000, 320000, 485000, 410000];
        revenueChartInstance.data.datasets[1].data = [140000, 160000, 145000, 210000, 250000, 390000, 330000];
      } else if (cycle === '30d') {
        revenueChartInstance.data.labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
        revenueChartInstance.data.datasets[0].data = [1250000, 1480000, 1620000, 1890000];
        revenueChartInstance.data.datasets[1].data = [1100000, 1250000, 1380000, 1550000];
      } else {
        revenueChartInstance.data.labels = ['Q1 (Spring Bridal)', 'Q2 (Summer Prêt)', 'Q3 (Festive Eid)', 'Q4 (Winter Wedding)'];
        revenueChartInstance.data.datasets[0].data = [3850000, 4200000, 5600000, 7850000];
        revenueChartInstance.data.datasets[1].data = [3100000, 3600000, 4800000, 6400000];
      }
      revenueChartInstance.update();
    }

    function copyReactTokens() {
      const theme = document.body.getAttribute('data-theme') || 'invenza';
      const cardRad = getComputedStyle(document.documentElement).getPropertyValue('--radius-card').trim();
      const pad = getComputedStyle(document.documentElement).getPropertyValue('--spacing-card-pad').trim();

      const tokenJson = {
        themeId: theme,
        shape: {
          borderRadius: parseInt(cardRad) || 16,
          cardRadius: parseInt(cardRad) || 16,
          buttonRadius: 9999
        },
        typography: {
          fontFamily: '"Outfit", -apple-system, BlinkMacSystemFont, sans-serif',
          displayFont: '"Playfair Display", Georgia, serif'
        },
        palette: {
          primary: {
            main: theme === 'navy' ? '#1E40AF' : theme === 'burgundy' ? '#831843' : theme === 'slate' ? '#334155' : '#047857'
          }
        }
      };

      navigator.clipboard.writeText(JSON.stringify(tokenJson, null, 2)).then(() => {
        alert('Copied React Theme Token Object to Clipboard!\\n\\n' + JSON.stringify(tokenJson, null, 2));
      });
    }

    window.addEventListener('DOMContentLoaded', () => {
      initCharts();
    });
  </script>
</body>
</html>
'''

with open('/Users/faeez/faeez.c/aleen-redesign-prototype.html', 'w') as f:
    f.write(html_content)

print("Regenerated cleanly without anti-patterns.")
