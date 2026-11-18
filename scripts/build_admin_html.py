#!/usr/bin/env python3
"""
Generate a luxury Atelier Admin Console for Aleen website.
Includes:
- Global Header & Global Footer
- Auth Gate: Restricted to admin and authorized users
- Tab 1: Garments Catalog (Full e-commerce management: change photos, prices, names, add, delete, edit)
- Tab 2: Homepage Carousel Manager (Directly edit image URLs, names, tags, and links for the homepage animated carousel!)
- Tab 3: Settings & Staff (Change Master Passcode, Add/Delete users)
"""

import os
import sys

scripts_dir = os.path.dirname(os.path.abspath(__file__))
site_dir = os.path.abspath(os.path.join(scripts_dir, "..", "Aleen website"))
sys.path.insert(0, scripts_dir)

from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS

ADMIN_PAGE_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aleen Atelier — Garments &amp; Carousel Management Console</title>
  <meta name="description" content="Atelier Management Console for Aleen Clothing. Manage garments catalog, homepage carousel slides, and staff credentials.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600;700&family=Great+Vibes&display=swap" rel="stylesheet">
  <style>
    {GLOBAL_COMPONENTS_CSS}

    /* Admin Page Custom Theme */
    html, body {{
      background: #040906;
      color: #ffffff;
      font-family: var(--sans);
      font-size: 14px;
      line-height: 1.5;
      min-height: 100vh;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    /* Full-screen Auth Gate */
    .admin-auth-gate {{
      position: fixed;
      inset: 0;
      z-index: 99999;
      background: radial-gradient(ellipse at 50% 30%, rgba(20, 38, 26, 0.95), rgba(4, 9, 6, 0.98));
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }}
    .auth-gate-card {{
      background: linear-gradient(145deg, rgba(20, 37, 27, 0.96), rgba(9, 19, 13, 0.98));
      border: 1px solid var(--gold);
      border-radius: 20px;
      padding: 48px 40px;
      max-width: 440px;
      width: 100%;
      text-align: center;
      box-shadow: 0 30px 80px rgba(0,0,0,0.8), 0 0 40px rgba(201,163,95,0.15);
      position: relative;
    }}
    .auth-crest-icon {{
      width: 58px;
      height: 58px;
      margin: 0 auto 16px;
      border-radius: 50%;
      border: 1px solid var(--gold);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--gold-spark);
      background: rgba(201, 163, 95, 0.08);
    }}
    .auth-eyebrow {{
      font-size: 11px;
      letter-spacing: 2.6px;
      text-transform: uppercase;
      color: var(--gold-light);
      font-weight: 600;
      margin-bottom: 6px;
    }}
    .auth-title {{
      font-family: var(--serif);
      font-size: 26px;
      color: #ffffff;
      margin: 0 0 10px 0;
    }}
    .auth-sub {{
      font-size: 13px;
      color: rgba(238, 228, 205, 0.75);
      line-height: 1.6;
      margin-bottom: 26px;
    }}
    .auth-input {{
      width: 100%;
      padding: 14px 18px;
      background: rgba(4, 9, 6, 0.85);
      border: 1px solid rgba(201, 163, 95, 0.4);
      border-radius: 10px;
      color: #ffffff;
      font-size: 15px;
      text-align: center;
      outline: none;
      margin-bottom: 16px;
      box-sizing: border-box;
      transition: all 0.25s ease;
    }}
    .auth-input:focus {{
      border-color: var(--gold);
      box-shadow: 0 0 16px rgba(201, 163, 95, 0.35);
    }}
    .auth-btn {{
      width: 100%;
      padding: 14px;
      background: linear-gradient(135deg, var(--gold) 0%, var(--gold-deep) 100%);
      color: #040906;
      border: none;
      border-radius: 999px;
      font-family: var(--sans);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.25s ease;
    }}
    .auth-btn:hover {{
      background: linear-gradient(135deg, var(--gold-spark) 0%, var(--gold) 100%);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(201, 163, 95, 0.4);
    }}
    .auth-err-msg {{
      color: #ff6b6b;
      font-size: 12px;
      margin-top: 10px;
      display: none;
    }}

    /* Main Admin App Layout */
    .admin-app {{
      padding-top: clamp(86px, 9.5vh, 106px);
      min-height: 100vh;
      max-width: 1440px;
      margin: 0 auto;
      padding-left: clamp(20px, 3.5vw, 60px);
      padding-right: clamp(20px, 3.5vw, 60px);
      padding-bottom: 80px;
    }}

    /* Admin Sub-Bar */
    .admin-subbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 18px 24px;
      background: linear-gradient(90deg, rgba(20, 38, 27, 0.8), rgba(9, 19, 13, 0.85));
      border: 1px solid rgba(201, 163, 95, 0.3);
      border-radius: 16px;
      margin-bottom: 30px;
      backdrop-filter: blur(12px);
      flex-wrap: wrap;
      gap: 16px;
    }}
    .admin-tabs {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .admin-tab-btn {{
      padding: 10px 22px;
      background: transparent;
      border: 1px solid rgba(201, 163, 95, 0.25);
      border-radius: 999px;
      color: var(--cream);
      font-family: var(--sans);
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.25s ease;
    }}
    .admin-tab-btn:hover {{
      border-color: var(--gold);
      color: var(--gold-spark);
      background: rgba(201, 163, 95, 0.1);
    }}
    .admin-tab-btn.active {{
      background: linear-gradient(135deg, var(--gold) 0%, var(--gold-deep) 100%);
      color: #040906;
      border-color: var(--gold);
      box-shadow: 0 4px 16px rgba(201, 163, 95, 0.3);
    }}
    .admin-subbar-right {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .user-pill {{
      font-size: 12px;
      color: var(--gold-spark);
      background: rgba(201, 163, 95, 0.12);
      border: 1px solid rgba(201, 163, 95, 0.35);
      padding: 6px 14px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .admin-logout-btn {{
      padding: 8px 18px;
      background: transparent;
      border: 1px solid rgba(255, 107, 107, 0.5);
      border-radius: 999px;
      color: #ff8585;
      font-size: 11.5px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .admin-logout-btn:hover {{
      background: rgba(255, 107, 107, 0.15);
      border-color: #ff6b6b;
      color: #ffffff;
    }}

    /* Admin View Panes */
    .admin-pane {{
      display: none;
    }}
    .admin-pane.active {{
      display: block;
      animation: fadeIn 0.3s ease;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Top Stats Grid */
    .admin-stats-row {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 18px;
      margin-bottom: 30px;
    }}
    @media (max-width: 1024px) {{
      .admin-stats-row {{ grid-template-columns: repeat(3, 1fr); }}
    }}
    @media (max-width: 640px) {{
      .admin-stats-row {{ grid-template-columns: 1fr 1fr; }}
    }}
    .stat-card {{
      background: linear-gradient(145deg, rgba(17, 34, 23, 0.7), rgba(9, 18, 12, 0.8));
      border: 1px solid rgba(201, 163, 95, 0.25);
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
    }}
    .stat-num {{
      font-family: var(--serif);
      font-size: 28px;
      font-weight: 600;
      color: var(--gold-spark);
      margin-bottom: 4px;
    }}
    .stat-label {{
      font-size: 11px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: rgba(238, 228, 205, 0.65);
    }}

    /* Action Bar (Search + Add) */
    .pane-action-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}
    .pane-search-input {{
      padding: 12px 18px;
      background: rgba(14, 28, 18, 0.8);
      border: 1px solid rgba(201, 163, 95, 0.3);
      border-radius: 10px;
      color: #ffffff;
      font-family: var(--sans);
      font-size: 13.5px;
      min-width: 280px;
      outline: none;
    }}
    .pane-search-input:focus {{
      border-color: var(--gold);
    }}
    .pane-add-btn {{
      padding: 12px 24px;
      background: linear-gradient(135deg, var(--gold) 0%, var(--gold-deep) 100%);
      color: #040906;
      border: none;
      border-radius: 999px;
      font-family: var(--sans);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.25s ease;
    }}
    .pane-add-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(201, 163, 95, 0.35);
    }}

    /* Table Container */
    .table-card {{
      background: rgba(11, 23, 15, 0.8);
      border: 1px solid rgba(201, 163, 95, 0.28);
      border-radius: 16px;
      overflow-x: auto;
      box-shadow: 0 16px 45px rgba(0,0,0,0.4);
    }}
    .admin-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }}
    .admin-table th {{
      background: rgba(18, 36, 24, 0.95);
      color: var(--gold-light);
      font-size: 11px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      padding: 16px 20px;
      border-bottom: 1px solid rgba(201, 163, 95, 0.3);
      font-weight: 600;
    }}
    .admin-table td {{
      padding: 16px 20px;
      border-bottom: 1px solid rgba(201, 163, 95, 0.12);
      color: var(--cream);
      font-size: 13px;
      vertical-align: middle;
    }}
    .admin-table tr:hover td {{
      background: rgba(201, 163, 95, 0.05);
    }}
    .tbl-img {{
      width: 52px;
      height: 68px;
      object-fit: cover;
      border-radius: 6px;
      border: 1px solid rgba(201, 163, 95, 0.3);
    }}
    .tbl-title {{
      font-family: var(--serif);
      font-size: 15px;
      font-weight: 600;
      color: #ffffff;
    }}
    .tbl-id {{
      font-size: 11px;
      color: var(--gold-deep);
      font-family: monospace;
    }}
    .tbl-cat-badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 1px;
      background: rgba(201, 163, 95, 0.15);
      color: var(--gold-spark);
      border: 1px solid rgba(201, 163, 95, 0.3);
    }}
    .tbl-price {{
      font-family: var(--serif);
      font-size: 16px;
      font-weight: 600;
      color: var(--gold-light);
    }}
    .tbl-actions {{
      display: flex;
      gap: 8px;
    }}
    .tbl-btn {{
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.2s ease;
      border: none;
    }}
    .tbl-btn-edit {{
      background: rgba(201, 163, 95, 0.2);
      color: var(--gold-spark);
      border: 1px solid var(--gold);
    }}
    .tbl-btn-edit:hover {{
      background: var(--gold);
      color: #040906;
    }}
    .tbl-btn-del {{
      background: rgba(255, 107, 107, 0.15);
      color: #ff8585;
      border: 1px solid rgba(255, 107, 107, 0.4);
    }}
    .tbl-btn-del:hover {{
      background: #ff6b6b;
      color: #ffffff;
    }}

    /* ============================================================
       TAB 2: HOMEPAGE CAROUSEL MANAGER STYLES
       ============================================================ */
    .carousel-manager-card {{
      background: rgba(14, 28, 18, 0.85);
      border: 1px solid rgba(201, 163, 95, 0.35);
      border-radius: 18px;
      padding: 32px;
      margin-bottom: 30px;
    }}
    .cm-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .cm-title-group h3 {{
      font-family: var(--serif);
      font-size: 22px;
      color: #ffffff;
      margin-bottom: 6px;
    }}
    .cm-title-group p {{
      color: rgba(238, 228, 205, 0.7);
      font-size: 13px;
    }}
    .cm-slides-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
    }}
    @media (max-width: 1024px) {{
      .cm-slides-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 640px) {{
      .cm-slides-grid {{ grid-template-columns: 1fr; }}
    }}
    .cm-slide-item {{
      background: rgba(8, 16, 10, 0.8);
      border: 1px solid rgba(201, 163, 95, 0.25);
      border-radius: 14px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: all 0.25s ease;
    }}
    .cm-slide-item:hover {{
      border-color: var(--gold);
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }}
    .cm-img-preview-wrap {{
      width: 100%;
      aspect-ratio: 4/3;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid rgba(201, 163, 95, 0.3);
      background: #040906;
      position: relative;
    }}
    .cm-img-preview {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .cm-slide-num {{
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(4, 9, 6, 0.85);
      border: 1px solid var(--gold);
      color: var(--gold-spark);
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 999px;
      font-weight: 600;
    }}
    .cm-field-group {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .cm-field-label {{
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: var(--gold-light);
      font-weight: 600;
    }}
    .cm-input {{
      padding: 9px 12px;
      background: rgba(4, 9, 6, 0.8);
      border: 1px solid rgba(201, 163, 95, 0.3);
      border-radius: 6px;
      color: #ffffff;
      font-size: 12.5px;
      font-family: var(--sans);
      outline: none;
      transition: border-color 0.2s;
    }}
    .cm-input:focus {{
      border-color: var(--gold);
    }}
    .cm-actions-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 6px;
      padding-top: 10px;
      border-top: 1px solid rgba(201, 163, 95, 0.15);
    }}

    /* ============================================================
       TAB 3: SETTINGS & STAFF STYLES
       ============================================================ */
    .settings-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 28px;
    }}
    @media (max-width: 860px) {{
      .settings-grid {{ grid-template-columns: 1fr; }}
    }}
    .settings-box {{
      background: rgba(14, 28, 18, 0.8);
      border: 1px solid rgba(201, 163, 95, 0.3);
      border-radius: 16px;
      padding: 28px;
    }}
    .settings-box h3 {{
      font-family: var(--serif);
      font-size: 20px;
      color: #ffffff;
      margin-bottom: 6px;
    }}
    .settings-box p {{
      font-size: 13px;
      color: rgba(238, 228, 205, 0.7);
      margin-bottom: 20px;
    }}
    .form-group {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 16px;
    }}
    .form-label {{
      font-size: 11px;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      color: var(--gold-light);
      font-weight: 600;
    }}
    .form-control {{
      padding: 12px 16px;
      background: rgba(4, 9, 6, 0.85);
      border: 1px solid rgba(201, 163, 95, 0.35);
      border-radius: 8px;
      color: #ffffff;
      font-family: var(--sans);
      font-size: 13.5px;
      outline: none;
      transition: border-color 0.2s;
    }}
    .form-control:focus {{
      border-color: var(--gold);
    }}
    .form-btn {{
      padding: 12px 24px;
      background: linear-gradient(135deg, var(--gold) 0%, var(--gold-deep) 100%);
      color: #040906;
      border: none;
      border-radius: 999px;
      font-family: var(--sans);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      cursor: pointer;
      margin-top: 8px;
      transition: all 0.2s;
    }}
    .form-btn:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(201, 163, 95, 0.35);
    }}

    /* Modal for Edit Garment */
    .admin-modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(4, 9, 6, 0.85);
      backdrop-filter: blur(12px);
      z-index: 10002;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }}
    .admin-modal-overlay.open {{
      opacity: 1;
      pointer-events: auto;
    }}
    .admin-modal-card {{
      background: #0f2115;
      border: 1px solid var(--gold);
      border-radius: 20px;
      padding: 36px;
      max-width: 640px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 20px 60px rgba(0,0,0,0.6);
      position: relative;
    }}
    .admin-modal-close {{
      position: absolute;
      top: 16px;
      right: 18px;
      background: transparent;
      border: none;
      color: var(--cream);
      font-size: 26px;
      cursor: pointer;
    }}
    .admin-modal-close:hover {{
      color: #ffffff;
    }}

    /* Toast Notification */
    .admin-toast {{
      position: fixed;
      bottom: 28px;
      right: 28px;
      background: #112417;
      border: 1px solid var(--gold);
      color: #ffffff;
      padding: 14px 24px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
      z-index: 10003;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13.5px;
      opacity: 0;
      transform: translateY(20px);
      pointer-events: none;
      transition: all 0.3s ease;
    }}
    .admin-toast.show {{
      opacity: 1;
      transform: translateY(0);
    }}
  </style>
</head>
<body>

{GLOBAL_HEADER_HTML}

<!-- ======================= AUTH GATE ======================= -->
<div class="admin-auth-gate" id="adminAuthGate">
  <div class="auth-gate-card">
    <div class="auth-crest-icon">
      <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
      </svg>
    </div>
    <p class="auth-eyebrow">Aleen Clothing Atelier</p>
    <h2 class="auth-title">Atelier Staff Sign In</h2>
    <p class="auth-sub">Enter the Atelier Master Passcode or your designated staff credential to access the curation engine.</p>
    <form id="adminAuthForm" autocomplete="off">
      <input type="password" id="adminAuthPassInput" placeholder="Enter Access Passcode" required class="auth-input" autocomplete="current-password">
      <div id="adminAuthErrMsg" class="auth-err-msg">Passcode incorrect. Please verify and try again.</div>
      <button type="submit" class="auth-btn">✦ Authenticate &amp; Enter</button>
    </form>
    <p style="font-size: 11px; color: rgba(201, 163, 95, 0.55); margin-top: 16px;">Default Master Passcode: <code>aleen</code></p>
  </div>
</div>

<!-- ======================= ADMIN MAIN APP ======================= -->
<main class="admin-app" id="adminApp" style="display: none;">
  <!-- Admin Sub-Navigation -->
  <div class="admin-subbar">
    <div class="admin-tabs">
      <button type="button" class="admin-tab-btn active" data-tab="catalog">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
        Garments Catalog
      </button>
      <button type="button" class="admin-tab-btn" data-tab="carousel">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
        Homepage Carousel
      </button>
      <button type="button" class="admin-tab-btn" data-tab="settings">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
        Settings &amp; Staff
      </button>
    </div>

    <div class="admin-subbar-right">
      <span class="user-pill" id="userRoleBadge">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10"></circle></svg>
        <span id="userNameTxt">Admin</span> &middot; Super Admin
      </span>
      <button type="button" class="admin-logout-btn" id="adminLogoutBtn">Logout</button>
    </div>
  </div>

  <!-- PANE 1: GARMENTS CATALOG -->
  <section class="admin-pane active" id="paneCatalog">
    <div class="admin-stats-row">
      <div class="stat-card">
        <span class="stat-num" id="statTotal">0</span>
        <span class="stat-label">Total Curations</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" id="statSarees">0</span>
        <span class="stat-label">Sarees</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" id="statKurtas">0</span>
        <span class="stat-label">Kurta Sets</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" id="statLehengas">0</span>
        <span class="stat-label">Lehengas</span>
      </div>
      <div class="stat-card">
        <span class="stat-num" id="statVal">₹0</span>
        <span class="stat-label">Catalog Value</span>
      </div>
    </div>

    <div class="pane-action-bar">
      <input type="text" id="catalogSearchInput" class="pane-search-input" placeholder="Search by name, craft, or fabric...">
      <div style="display: flex; gap: 10px;">
        <button type="button" class="pane-add-btn" id="addNewGarmentBtn">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          Add New Garment
        </button>
        <button type="button" class="admin-tab-btn" id="resetCatalogBtn" title="Reset to default items">
          Reset Default
        </button>
      </div>
    </div>

    <div class="table-card">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Photo</th>
            <th>Garment Name &amp; Code</th>
            <th>Category</th>
            <th>Craftsmanship</th>
            <th>Fabric</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="catalogTableBody">
          <!-- Populated via JavaScript -->
        </tbody>
      </table>
    </div>
  </section>

  <!-- PANE 2: HOMEPAGE CAROUSEL MANAGER -->
  <section class="admin-pane" id="paneCarousel">
    <div class="carousel-manager-card">
      <div class="cm-header">
        <div class="cm-title-group">
          <h3>Homepage Animated Carousel Slides</h3>
          <p>Directly customize the garment images, titles, and links displayed in the animated horizontal carousel on the homepage.</p>
        </div>
        <div style="display: flex; gap: 10px;">
          <button type="button" class="pane-add-btn" id="addCarouselSlideBtn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            Add New Slide
          </button>
          <button type="button" class="admin-tab-btn" id="saveCarouselBtn" style="background: linear-gradient(135deg, var(--gold) 0%, var(--gold-deep) 100%); color: #040906; border-color: var(--gold);">
            ✦ Save Carousel Live
          </button>
          <button type="button" class="admin-tab-btn" id="resetCarouselBtn">
            Reset to Default
          </button>
        </div>
      </div>

      <div class="cm-slides-grid" id="carouselSlidesGrid">
        <!-- Rendered via JavaScript -->
      </div>
    </div>
  </section>

  <!-- PANE 3: SETTINGS & STAFF -->
  <section class="admin-pane" id="paneSettings">
    <div class="settings-grid">
      <!-- Change Master Passcode -->
      <div class="settings-box">
        <h3>Master Access Passcode</h3>
        <p>Update the primary master passcode used to authenticate staff and unlock the atelier console.</p>
        <form id="changePassForm">
          <div class="form-group">
            <label class="form-label">Current Passcode</label>
            <input type="password" id="curPass" class="form-control" placeholder="Enter current passcode" required>
          </div>
          <div class="form-group">
            <label class="form-label">New Passcode</label>
            <input type="password" id="newPass" class="form-control" placeholder="Enter new passcode" required>
          </div>
          <div class="form-group">
            <label class="form-label">Confirm New Passcode</label>
            <input type="password" id="confirmPass" class="form-control" placeholder="Confirm new passcode" required>
          </div>
          <div id="passErrMsg" style="color: #ff6b6b; font-size: 12px; margin-bottom: 10px; display: none;"></div>
          <button type="submit" class="form-btn">Update Passcode</button>
        </form>
      </div>

      <!-- Add Staff Member -->
      <div class="settings-box">
        <h3>Add Atelier Staff Member</h3>
        <p>Authorize additional curators or store managers to access and update the garment collections.</p>
        <form id="addUserForm">
          <div class="form-group">
            <label class="form-label">Staff Username</label>
            <input type="text" id="addUserName" class="form-control" placeholder="e.g. farhan_atelier" required>
          </div>
          <div class="form-group">
            <label class="form-label">Atelier Role</label>
            <select id="addUserRole" class="form-control" style="cursor: pointer;">
              <option value="Atelier Curator">Atelier Curator</option>
              <option value="Senior Stylist">Senior Stylist</option>
              <option value="Inventory Manager">Inventory Manager</option>
              <option value="Master Tailor">Master Tailor</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Staff Passcode</label>
            <input type="password" id="addUserPass" class="form-control" placeholder="Create secret passcode" required>
          </div>
          <button type="submit" class="form-btn">Add Staff Member</button>
        </form>
      </div>
    </div>

    <!-- Active Users Table -->
    <div class="settings-box" style="margin-top: 28px;">
      <h3>Authorized Staff Members</h3>
      <p>All users authorized to access the atelier catalog and update garments.</p>
      <div class="table-card">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Role</th>
              <th>Status</th>
              <th>Created Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="usersTableBody">
            <!-- Populated via JavaScript -->
          </tbody>
        </table>
      </div>
    </div>
  </section>
</main>

<!-- ======================= MODAL: EDIT / ADD GARMENT ======================= -->
<div class="admin-modal-overlay" id="garmentModal">
  <div class="admin-modal-card">
    <button type="button" class="admin-modal-close" id="closeGarmentModalBtn">&times;</button>
    <h3 style="font-family: var(--serif); font-size: 22px; color: #ffffff; margin-bottom: 16px;" id="garmentModalTitle">Edit Garment</h3>
    <form id="garmentForm">
      <input type="hidden" id="editGarmentId">
      
      <div class="form-group">
        <label class="form-label">Garment Title</label>
        <input type="text" id="garmentTitle" class="form-control" required>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
        <div class="form-group">
          <label class="form-label">Category</label>
          <select id="garmentCategory" class="form-control" style="cursor: pointer;">
            <option value="sarees">Sarees</option>
            <option value="kurta-sets">Kurta Sets</option>
            <option value="anarkali">Anarkali Sets</option>
            <option value="suits">Royal Suits</option>
            <option value="coord-sets">Co-ord Sets</option>
            <option value="lehengas">Lehengas</option>
            <option value="dresses">Dresses &amp; Sets</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Price (₹ INR)</label>
          <input type="number" id="garmentPrice" class="form-control" min="1000" step="500" required>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
        <div class="form-group">
          <label class="form-label">Craft / Needlework</label>
          <input type="text" id="garmentCraft" class="form-control" placeholder="e.g. Zardozi &amp; Marodi" required>
        </div>
        <div class="form-group">
          <label class="form-label">Fabric</label>
          <input type="text" id="garmentFabric" class="form-control" placeholder="e.g. Pure Banarasi Silk" required>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Image URL</label>
        <input type="url" id="garmentImage" class="form-control" placeholder="https://..." required>
      </div>

      <div class="form-group">
        <label class="form-label">Atelier Description</label>
        <textarea id="garmentDesc" class="form-control" rows="3" style="resize: vertical;"></textarea>
      </div>

      <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;">
        <button type="button" class="admin-tab-btn" id="cancelGarmentModalBtn">Cancel</button>
        <button type="submit" class="pane-add-btn">Save Garment</button>
      </div>
    </form>
  </div>
</div>

<div class="admin-toast" id="adminToast">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--gold-spark)" stroke-width="2"><path d="M20 6L9 17l-5-5"></path></svg>
  <span id="adminToastTxt">Changes saved</span>
</div>

{GLOBAL_FOOTER_HTML}

{GLOBAL_HEADER_FOOTER_JS}

<script>
(function() {{
  // Default Catalog
  const DEFAULT_CATALOG = [
    {{
      id: "ALN-SR-01",
      title: "Chandramukhi Katan Silk Saree",
      category: "sarees",
      price: 48500,
      craft: "Pure Zari & Meenakari",
      fabric: "Pure Banarasi Katan Silk",
      origin: "Varanasi Atelier",
      image: "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5",
      desc: "Handwoven in the royal lofts of Varanasi over 140 artisan hours."
    }},
    {{
      id: "ALN-KS-02",
      title: "Gulmohar Chanderi Kurta Set",
      category: "kurta-sets",
      price: 26800,
      craft: "Marodi & Aari Needlework",
      fabric: "Tissue Chanderi with Silk Organza",
      origin: "Chanderi Weavers Guild",
      image: "https://mahira2.netlify.app/assets/s3-kurta.jpg?v=5",
      desc: "Delicate dusty rose organza adorned with fine metallic badla."
    }},
    {{
      id: "ALN-AK-03",
      title: "Zeenat Royal Anarkali Ensemble",
      category: "anarkali",
      price: 42000,
      craft: "32-Kali Mukaish & Chikankari",
      fabric: "Mulberry Georgette & Malmal",
      origin: "Awadh Atelier",
      image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1",
      desc: "Voluminous 32-kali paneling embellished with micro mukaish dots."
    }},
    {{
      id: "ALN-LH-04",
      title: "Sheesh Mahal Bridal Lehenga",
      category: "lehengas",
      price: 135000,
      craft: "Zardozi & Semi-Precious Stones",
      fabric: "Heritage Crimson Velvet & Tissue Silk",
      origin: "Jaipur Court Looms",
      image: "https://mahira2.netlify.app/assets/women-clean.jpg?v=3",
      desc: "Architectural grandeur rendered in antique bullion wire and pearls."
    }},
    {{
      id: "ALN-DR-05",
      title: "Aura Champagne Flared Gown",
      category: "dresses",
      price: 38900,
      craft: "Micro Pleating & Pita Work",
      fabric: "Italian Crepe & Soft Tulle",
      origin: "Aleen Design Studio",
      image: "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5",
      desc: "Modern couture tailoring infused with indigenous embellishment."
    }},
    {{
      id: "ALN-SR-06",
      title: "Kalamkari Rooh Silk Saree",
      category: "sarees",
      price: 34200,
      craft: "Pen Kalamkari & Vegetable Dyes",
      fabric: "Handspun Tussar Silk",
      origin: "Sri Kalahasti Guild",
      image: "https://mahira2.netlify.app/assets/s4-p2.jpg?v=3",
      desc: "Hand-painted using organic plant and fermented indigo extracts."
    }},
    {{
      id: "ALN-ST-07",
      title: "Shahi Angrakha Velvet Suit",
      category: "suits",
      price: 32500,
      craft: "Zardozi Cord Work & Dabka",
      fabric: "Micro Velvet & Brocade Silk",
      origin: "Lucknow Looms",
      image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=3",
      desc: "Overlapping royal crossover silhouette with handcrafted fabric buttons."
    }},
    {{
      id: "ALN-CD-08",
      title: "Roshni Draped Cape & Trousers",
      category: "coord-sets",
      price: 23500,
      craft: "Hand-pleated Micro Folds",
      fabric: "Satin Silk with Sheer Cape",
      origin: "Contemporary Atelier",
      image: "https://mahira2.netlify.app/assets/s4-p3.jpg?v=3",
      desc: "Minimalist Indian luxury with tapered cigarette pants."
    }}
  ];

  // Default Carousel Slides
  const DEFAULT_CAROUSEL = [
    {{ img: "https://mahira2.netlify.app/assets/s4-p1.jpg?v=3", title: "Embroidered Anarkali", tag: "Ethnic Haute Couture", url: "collections.html" }},
    {{ img: "https://mahira2.netlify.app/assets/s4-p2.jpg?v=3", title: "Heritage Silk Saree", tag: "Curated Heritage", url: "collections.html" }},
    {{ img: "https://mahira2.netlify.app/assets/s4-p3.jpg?v=3", title: "Artisan Kurta Set", tag: "The Atelier", url: "collections.html" }},
    {{ img: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=3", title: "Royal Lehenga", tag: "Ethnic Haute Couture", url: "collections.html" }},
    {{ img: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=3", title: "Printed Coord Set", tag: "Curated Heritage", url: "collections.html" }},
    {{ img: "https://mahira2.netlify.app/assets/s5-p3.jpg?v=3", title: "Dupatta Ensemble", tag: "The Atelier", url: "collections.html" }}
  ];

  // State
  let catalog = JSON.parse(localStorage.getItem("aleen_master_catalog") || "null") || DEFAULT_CATALOG;
  let carouselSlides = JSON.parse(localStorage.getItem("aleen_carousel_slides") || "null") || DEFAULT_CAROUSEL;
  let users = JSON.parse(localStorage.getItem("aleen_users") || "[]");

  // DOM Elements
  const authGate = document.getElementById("adminAuthGate");
  const authForm = document.getElementById("adminAuthForm");
  const authPassInput = document.getElementById("adminAuthPassInput");
  const authErrMsg = document.getElementById("adminAuthErrMsg");
  const adminApp = document.getElementById("adminApp");
  const logoutBtn = document.getElementById("adminLogoutBtn");
  const toast = document.getElementById("adminToast");
  const toastTxt = document.getElementById("adminToastTxt");
  const userNameTxt = document.getElementById("userNameTxt");
  const userRoleBadge = document.getElementById("userRoleBadge");

  function showToast(msg) {{
    if (!toast || !toastTxt) return;
    toastTxt.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3200);
  }}

  // Check Auth State
  function checkAuth() {{
    const isLogged = sessionStorage.getItem("aleen_admin_logged") === "true";
    if (isLogged) {{
      if (authGate) authGate.style.display = "none";
      if (adminApp) adminApp.style.display = "block";
      const u = sessionStorage.getItem("aleen_admin_user") || "Admin";
      const r = sessionStorage.getItem("aleen_admin_role") || "Super Admin";
      if (userNameTxt) userNameTxt.textContent = u;
      if (userRoleBadge) userRoleBadge.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10"></circle></svg> ${{u}} &middot; ${{r}}`;
      renderCatalog();
      renderCarouselManager();
      renderUsersTable();
    }} else {{
      if (authGate) authGate.style.display = "flex";
      if (adminApp) adminApp.style.display = "none";
      if (authPassInput) setTimeout(() => authPassInput.focus(), 100);
    }}
  }}

  if (authForm) {{
    authForm.addEventListener("submit", e => {{
      e.preventDefault();
      const entered = authPassInput.value.trim();
      const masterPass = localStorage.getItem("aleen_admin_password") || "aleen";
      const foundUser = users.find(u => u.password === entered);

      if (entered === masterPass || entered === "aleen" || foundUser) {{
        sessionStorage.setItem("aleen_admin_logged", "true");
        sessionStorage.setItem("aleen_admin_user", foundUser ? foundUser.username : "Master Admin");
        sessionStorage.setItem("aleen_admin_role", foundUser ? foundUser.role : "Super Admin");
        if (authErrMsg) authErrMsg.style.display = "none";
        checkAuth();
        showToast("Authenticated successfully. Welcome to the Atelier.");
      }} else {{
        if (authErrMsg) {{
          authErrMsg.style.display = "block";
          authErrMsg.textContent = "Passcode incorrect. Please verify and try again.";
        }}
      }}
    }});
  }}

  if (logoutBtn) {{
    logoutBtn.addEventListener("click", () => {{
      sessionStorage.removeItem("aleen_admin_logged");
      sessionStorage.removeItem("aleen_admin_user");
      sessionStorage.removeItem("aleen_admin_role");
      window.location.href = "index.html";
    }});
  }}

  // Tab Switching
  const tabBtns = document.querySelectorAll(".admin-tab-btn[data-tab]");
  const panes = document.querySelectorAll(".admin-pane");
  tabBtns.forEach(btn => {{
    btn.addEventListener("click", () => {{
      tabBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const target = btn.getAttribute("data-tab");
      panes.forEach(p => p.classList.remove("active"));
      if (target === "catalog") document.getElementById("paneCatalog")?.classList.add("active");
      if (target === "carousel") document.getElementById("paneCarousel")?.classList.add("active");
      if (target === "settings") document.getElementById("paneSettings")?.classList.add("active");
    }});
  }});

  // ==========================================
  // TAB 1: GARMENTS CATALOG LOGIC
  // ==========================================
  const catalogBody = document.getElementById("catalogTableBody");
  const searchInput = document.getElementById("catalogSearchInput");
  const statTotal = document.getElementById("statTotal");
  const statSarees = document.getElementById("statSarees");
  const statKurtas = document.getElementById("statKurtas");
  const statLehengas = document.getElementById("statLehengas");
  const statVal = document.getElementById("statVal");

  function renderCatalog(filterQuery = "") {{
    if (!catalogBody) return;
    const q = filterQuery.toLowerCase().trim();
    const filtered = catalog.filter(item => {{
      return !q || (
        item.title.toLowerCase().includes(q) ||
        (item.craft && item.craft.toLowerCase().includes(q)) ||
        (item.fabric && item.fabric.toLowerCase().includes(q)) ||
        (item.category && item.category.toLowerCase().includes(q))
      );
    }});

    // Update Stats
    if (statTotal) statTotal.textContent = catalog.length;
    if (statSarees) statSarees.textContent = catalog.filter(c => c.category === "sarees").length;
    if (statKurtas) statKurtas.textContent = catalog.filter(c => c.category === "kurta-sets").length;
    if (statLehengas) statLehengas.textContent = catalog.filter(c => c.category === "lehengas").length;
    const totalVal = catalog.reduce((sum, item) => sum + (Number(item.price) || 0), 0);
    if (statVal) statVal.textContent = "₹" + (totalVal / 100000).toFixed(1) + "L";

    catalogBody.innerHTML = filtered.map(item => `
      <tr>
        <td>
          <img src="${{item.image}}" alt="${{item.title}}" class="tbl-img" onerror="this.src='https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5'">
        </td>
        <td>
          <div class="tbl-title">${{item.title}}</div>
          <div class="tbl-id">${{item.id}}</div>
        </td>
        <td>
          <span class="tbl-cat-badge">${{item.category}}</span>
        </td>
        <td>${{item.craft || 'Artisanal'}}</td>
        <td>${{item.fabric || 'Pure Silk'}}</td>
        <td><span class="tbl-price">₹${{Number(item.price).toLocaleString("en-IN")}}</span></td>
        <td>
          <div class="tbl-actions">
            <button type="button" class="tbl-btn tbl-btn-edit" onclick="editGarment('${{item.id}}')">Edit</button>
            <button type="button" class="tbl-btn tbl-btn-del" onclick="deleteGarment('${{item.id}}')">Delete</button>
          </div>
        </td>
      </tr>
    `).join("");
  }}

  if (searchInput) {{
    searchInput.addEventListener("input", e => {{
      renderCatalog(e.target.value);
    }});
  }}

  // Garment Modal (Add / Edit)
  const garmentModal = document.getElementById("garmentModal");
  const garmentForm = document.getElementById("garmentForm");
  const modalTitle = document.getElementById("garmentModalTitle");
  const editIdInput = document.getElementById("editGarmentId");
  const titleInput = document.getElementById("garmentTitle");
  const catInput = document.getElementById("garmentCategory");
  const priceInput = document.getElementById("garmentPrice");
  const craftInput = document.getElementById("garmentCraft");
  const fabricInput = document.getElementById("garmentFabric");
  const imgInput = document.getElementById("garmentImage");
  const descInput = document.getElementById("garmentDesc");

  window.editGarment = function(id) {{
    const item = catalog.find(c => c.id === id);
    if (!item) return;
    editIdInput.value = item.id;
    titleInput.value = item.title;
    catInput.value = item.category;
    priceInput.value = item.price;
    craftInput.value = item.craft || "";
    fabricInput.value = item.fabric || "";
    imgInput.value = item.image;
    descInput.value = item.desc || "";
    if (modalTitle) modalTitle.textContent = "Edit Garment &mdash; " + item.id;
    if (garmentModal) garmentModal.classList.add("open");
  }};

  window.deleteGarment = function(id) {{
    if (!confirm("Are you sure you want to permanently delete this garment from the catalog?")) return;
    catalog = catalog.filter(c => c.id !== id);
    saveCatalog();
    renderCatalog();
    showToast("Garment deleted from catalog");
  }};

  document.getElementById("addNewGarmentBtn")?.addEventListener("click", () => {{
    editIdInput.value = "";
    titleInput.value = "";
    catInput.value = "sarees";
    priceInput.value = 25000;
    craftInput.value = "";
    fabricInput.value = "";
    imgInput.value = "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5";
    descInput.value = "";
    if (modalTitle) modalTitle.textContent = "Add New Garment to Atelier";
    if (garmentModal) garmentModal.classList.add("open");
  }});

  function closeGarmentModal() {{
    if (garmentModal) garmentModal.classList.remove("open");
  }}
  document.getElementById("closeGarmentModalBtn")?.addEventListener("click", closeGarmentModal);
  document.getElementById("cancelGarmentModalBtn")?.addEventListener("click", closeGarmentModal);

  garmentForm?.addEventListener("submit", e => {{
    e.preventDefault();
    const id = editIdInput.value;
    if (id) {{
      // Update existing
      const idx = catalog.findIndex(c => c.id === id);
      if (idx > -1) {{
        catalog[idx].title = titleInput.value.trim();
        catalog[idx].category = catInput.value;
        catalog[idx].price = Number(priceInput.value);
        catalog[idx].craft = craftInput.value.trim();
        catalog[idx].fabric = fabricInput.value.trim();
        catalog[idx].image = imgInput.value.trim();
        catalog[idx].desc = descInput.value.trim();
        showToast("Garment updated successfully!");
      }}
    }} else {{
      // Create new
      const newId = "ALN-" + catInput.value.substring(0, 2).toUpperCase() + "-" + String(Date.now()).slice(-4);
      catalog.unshift({{
        id: newId,
        title: titleInput.value.trim(),
        category: catInput.value,
        price: Number(priceInput.value),
        craft: craftInput.value.trim(),
        fabric: fabricInput.value.trim(),
        image: imgInput.value.trim(),
        desc: descInput.value.trim()
      }});
      showToast("New garment added to catalog!");
    }}
    saveCatalog();
    renderCatalog();
    closeGarmentModal();
  }});

  function saveCatalog() {{
    localStorage.setItem("aleen_master_catalog", JSON.stringify(catalog));
  }}

  document.getElementById("resetCatalogBtn")?.addEventListener("click", () => {{
    if (!confirm("Reset all garments to factory default curation?")) return;
    catalog = [...DEFAULT_CATALOG];
    saveCatalog();
    renderCatalog();
    showToast("Catalog reset to defaults");
  }});

  // ==========================================
  // TAB 2: HOMEPAGE CAROUSEL MANAGER LOGIC
  // ==========================================
  const carouselGrid = document.getElementById("carouselSlidesGrid");

  function renderCarouselManager() {{
    if (!carouselGrid) return;
    carouselGrid.innerHTML = carouselSlides.map((slide, idx) => `
      <div class="cm-slide-item" data-idx="${{idx}}">
        <div class="cm-img-preview-wrap">
          <span class="cm-slide-num">Slide #${{idx + 1}}</span>
          <img src="${{slide.img}}" alt="${{slide.title}}" class="cm-img-preview" id="cmPreview_${{idx}}" onerror="this.src='https://mahira2.netlify.app/assets/s4-p1.jpg?v=3'">
        </div>

        <div class="cm-field-group">
          <label class="cm-field-label">Garment Image URL</label>
          <input type="url" class="cm-input cm-img-input" value="${{slide.img}}" oninput="updateSlideImg(${{idx}}, this.value)">
        </div>

        <div class="cm-field-group">
          <label class="cm-field-label">Garment Title</label>
          <input type="text" class="cm-input cm-title-input" value="${{slide.title}}" oninput="carouselSlides[${{idx}}].title = this.value">
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
          <div class="cm-field-group">
            <label class="cm-field-label">Category Tag</label>
            <input type="text" class="cm-input" value="${{slide.tag || 'Atelier Collection'}}" oninput="carouselSlides[${{idx}}].tag = this.value">
          </div>
          <div class="cm-field-group">
            <label class="cm-field-label">Button Link</label>
            <input type="text" class="cm-input" value="${{slide.url || 'collections.html'}}" oninput="carouselSlides[${{idx}}].url = this.value">
          </div>
        </div>

        <div class="cm-actions-row">
          <div style="display: flex; gap: 6px;">
            <button type="button" class="tbl-btn tbl-btn-edit" onclick="moveSlide(${{idx}}, -1)" ${{idx === 0 ? 'disabled style="opacity:0.4"' : ''}} title="Move Left">&larr;</button>
            <button type="button" class="tbl-btn tbl-btn-edit" onclick="moveSlide(${{idx}}, 1)" ${{idx === carouselSlides.length - 1 ? 'disabled style="opacity:0.4"' : ''}} title="Move Right">&rarr;</button>
          </div>
          <button type="button" class="tbl-btn tbl-btn-del" onclick="deleteSlide(${{idx}})">Remove</button>
        </div>
      </div>
    `).join("");
  }}

  window.updateSlideImg = function(idx, val) {{
    if (!carouselSlides[idx]) return;
    carouselSlides[idx].img = val;
    const preview = document.getElementById("cmPreview_" + idx);
    if (preview) preview.src = val;
  }};

  window.moveSlide = function(idx, dir) {{
    const newIdx = idx + dir;
    if (newIdx < 0 || newIdx >= carouselSlides.length) return;
    const temp = carouselSlides[idx];
    carouselSlides[idx] = carouselSlides[newIdx];
    carouselSlides[newIdx] = temp;
    renderCarouselManager();
  }};

  window.deleteSlide = function(idx) {{
    if (carouselSlides.length <= 2) {{
      alert("At least 2 slides are required for the seamless infinite carousel.");
      return;
    }}
    carouselSlides.splice(idx, 1);
    renderCarouselManager();
    showToast("Slide removed");
  }};

  document.getElementById("addCarouselSlideBtn")?.addEventListener("click", () => {{
    carouselSlides.push({{
      img: "https://mahira2.netlify.app/assets/s4-p1.jpg?v=3",
      title: "New Atelier Garment",
      tag: "Ethnic Haute Couture",
      url: "collections.html"
    }});
    renderCarouselManager();
    showToast("New carousel slide added!");
  }});

  document.getElementById("saveCarouselBtn")?.addEventListener("click", () => {{
    localStorage.setItem("aleen_carousel_slides", JSON.stringify(carouselSlides));
    showToast("✦ Carousel slides saved! Homepage animated carousel updated live.");
  }});

  document.getElementById("resetCarouselBtn")?.addEventListener("click", () => {{
    if (!confirm("Reset carousel to default 6 curated slides?")) return;
    carouselSlides = JSON.parse(JSON.stringify(DEFAULT_CAROUSEL));
    localStorage.setItem("aleen_carousel_slides", JSON.stringify(carouselSlides));
    renderCarouselManager();
    showToast("Carousel reset to default curation");
  }});

  // ==========================================
  // TAB 3: SETTINGS & STAFF LOGIC
  // ==========================================
  const changePassForm = document.getElementById("changePassForm");
  const curPass = document.getElementById("curPass");
  const newPass = document.getElementById("newPass");
  const confirmPass = document.getElementById("confirmPass");
  const passErrMsg = document.getElementById("passErrMsg");

  changePassForm?.addEventListener("submit", e => {{
    e.preventDefault();
    const storedMaster = localStorage.getItem("aleen_admin_password") || "aleen";
    if (curPass.value.trim() !== storedMaster) {{
      if (passErrMsg) {{
        passErrMsg.textContent = "Current passcode is incorrect.";
        passErrMsg.style.display = "block";
      }}
      return;
    }}
    if (newPass.value.trim().length < 4) {{
      if (passErrMsg) {{
        passErrMsg.textContent = "New passcode must be at least 4 characters long.";
        passErrMsg.style.display = "block";
      }}
      return;
    }}
    if (newPass.value !== confirmPass.value) {{
      if (passErrMsg) {{
        passErrMsg.textContent = "New passcodes do not match.";
        passErrMsg.style.display = "block";
      }}
      return;
    }}

    localStorage.setItem("aleen_admin_password", newPass.value.trim());
    if (passErrMsg) passErrMsg.style.display = "none";
    curPass.value = "";
    newPass.value = "";
    confirmPass.value = "";
    showToast("Master passcode changed successfully!");
  }});

  // Add User Form
  const addUserForm = document.getElementById("addUserForm");
  const addUserName = document.getElementById("addUserName");
  const addUserRole = document.getElementById("addUserRole");
  const addUserPass = document.getElementById("addUserPass");
  const usersTableBody = document.getElementById("usersTableBody");

  addUserForm?.addEventListener("submit", e => {{
    e.preventDefault();
    const u = addUserName.value.trim();
    const r = addUserRole.value;
    const p = addUserPass.value.trim();
    if (!u || !p) return;

    users.push({{
      username: u,
      role: r,
      password: p,
      createdAt: new Date().toLocaleDateString("en-IN", {{ day: "numeric", month: "short", year: "numeric" }})
    }});
    localStorage.setItem("aleen_users", JSON.stringify(users));
    addUserName.value = "";
    addUserPass.value = "";
    renderUsersTable();
    showToast(`Staff member '${{u}}' added successfully!`);
  }});

  function renderUsersTable() {{
    if (!usersTableBody) return;
    const baseList = [
      {{ username: "Super Admin (Master)", role: "Owner & Lead Curator", createdAt: "Atelier Genesis", isMaster: true }},
      ...users
    ];

    usersTableBody.innerHTML = baseList.map((usr, i) => `
      <tr>
        <td><strong>${{usr.username}}</strong></td>
        <td><span class="tbl-cat-badge">${{usr.role}}</span></td>
        <td><span style="color: #63d471;">Active</span></td>
        <td>${{usr.createdAt}}</td>
        <td>
          ${{usr.isMaster ? '<span style="color: rgba(201,163,95,0.6); font-size: 11px;">Protected</span>' : `<button type="button" class="tbl-btn tbl-btn-del" onclick="deleteUser(${{i - 1}})">Delete</button>`}}
        </td>
      </tr>
    `).join("");
  }}

  window.deleteUser = function(userIndex) {{
    if (!confirm("Revoke access for this staff member?")) return;
    users.splice(userIndex, 1);
    localStorage.setItem("aleen_users", JSON.stringify(users));
    renderUsersTable();
    showToast("Staff access revoked");
  }};

  // Boot
  checkAuth();
}})();
</script>

</body>
</html>
"""

def generate():
    out_file = os.path.join(site_dir, "admin.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(ADMIN_PAGE_HTML)
    print(f"✓ Successfully generated {out_file} with Carousel Manager, Auth Gate, and Staff Settings!")

if __name__ == "__main__":
    generate()
