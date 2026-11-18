import os
import json
from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Aleen website"))

with open(os.path.join(os.path.dirname(__file__), "master_garments.json"), "r") as f:
    master_garments_raw = f.read()

COLLECTIONS_PAGE_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aleen Clothing — The Haute Garments Gallery</title>
  <meta name="description" content="Explore handcrafted Sarees, Kurta Sets, Lehengas, Dresses & Unstitched Silks by Aleen Clothing. Tradition meets tomorrow.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600;700&family=Great+Vibes&display=swap" rel="stylesheet">
  <style>
    {GLOBAL_COMPONENTS_CSS}

    /* Collections Page specific aesthetic matching Picture 3 */
    html, body {{
      background-color: #f3ebdd;
      background-image: url('assets/collection-bg.png');
      background-repeat: no-repeat;
      background-position: top left;
      background-size: cover;
      background-attachment: fixed;
      color: #17261b;
      font-family: var(--sans);
      font-size: 16px;
      line-height: 1.6;
      overflow-x: hidden;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Announcement Bar */
    .atelier-announcement {{
      background: linear-gradient(90deg, #112217, #1c3826, #112217);
      border-bottom: 1px solid rgba(201, 163, 95, 0.35);
      padding: 9px 20px;
      text-align: center;
      font-size: 11px;
      letter-spacing: 2.2px;
      text-transform: uppercase;
      color: var(--gold-spark);
      font-weight: 500;
      position: relative;
      z-index: 1001;
      margin-top: clamp(76px, 8.4vh, 92px);
    }}

    /* Gallery Hero Section */
    .catalog-hero {{
      padding: 60px clamp(24px, 5vw, 80px) 40px;
      text-align: center;
      position: relative;
    }}
    .catalog-hero-inner {{
      max-width: 980px;
      margin: 0 auto;
    }}
    .catalog-kicker {{
      font-family: var(--sans);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 4px;
      text-transform: uppercase;
      color: #8a6420;
      margin-bottom: 12px;
      display: inline-block;
    }}
    .catalog-title {{
      font-family: var(--serif);
      font-size: clamp(38px, 5vw, 64px);
      font-weight: 400;
      color: #112417;
      line-height: 1.15;
      margin-bottom: 14px;
      letter-spacing: -0.5px;
    }}
    .catalog-tagline {{
      font-family: var(--serif-i);
      font-size: clamp(18px, 2vw, 24px);
      color: #554121;
      max-width: 720px;
      margin: 0 auto 34px;
      line-height: 1.45;
    }}

    /* Controls Container: filter pills + search */
    .catalog-controls-card {{
      background: rgba(255, 255, 255, 0.72);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(184, 154, 98, 0.45);
      border-radius: 20px;
      padding: 24px 28px;
      box-shadow: 0 12px 36px rgba(23, 38, 27, 0.08);
      margin-bottom: 30px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    .filter-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
    }}
    .filter-tab {{
      background: rgba(255, 255, 255, 0.8);
      border: 1px solid rgba(184, 154, 98, 0.4);
      color: #17261b;
      padding: 9px 20px;
      border-radius: 999px;
      font-family: var(--sans);
      font-size: 11.5px;
      font-weight: 600;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.25s ease;
    }}
    .filter-tab:hover {{
      background: #17261b;
      color: var(--gold-light);
      border-color: #17261b;
    }}
    .filter-tab.active {{
      background: #17261b;
      color: #f7efdc;
      border-color: #c9a35f;
      box-shadow: 0 6px 18px rgba(23, 38, 27, 0.25);
    }}

    .catalog-search-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      border-top: 1px solid rgba(184, 154, 98, 0.25);
      padding-top: 18px;
    }}
    .search-box {{
      position: relative;
      flex: 1;
      min-width: 260px;
      max-width: 440px;
    }}
    .search-box svg {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: #7a6e5a;
    }}
    .search-input {{
      width: 100%;
      background: rgba(255, 255, 255, 0.95);
      border: 1px solid rgba(184, 154, 98, 0.45);
      border-radius: 999px;
      padding: 10px 18px 10px 42px;
      font-family: var(--sans);
      font-size: 13px;
      color: #17261b;
      outline: none;
      transition: border-color 0.25s ease;
    }}
    .search-input:focus {{
      border-color: #8a6420;
    }}
    .search-input::placeholder {{
      color: #7a6e5a;
    }}

    .sort-box select {{
      background: rgba(255, 255, 255, 0.95);
      border: 1px solid rgba(184, 154, 98, 0.45);
      border-radius: 999px;
      padding: 10px 24px;
      font-family: var(--sans);
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 1px;
      color: #17261b;
      outline: none;
      cursor: pointer;
    }}

    /* Main Grid Section */
    .catalog-section {{
      max-width: 1380px;
      margin: 0 auto;
      padding: 10px clamp(24px, 4vw, 60px) 100px;
    }}
    .catalog-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 13px;
      color: #554121;
      font-weight: 500;
      margin-bottom: 28px;
      padding: 0 4px;
    }}
    .catalog-count-badge {{
      color: #112417;
      font-weight: 700;
    }}

    /* Garments Grid */
    .garments-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
      gap: 36px 28px;
    }}

    /* Garment Card: Deep Emerald Arch */
    .garment-card {{
      background: linear-gradient(180deg, #132418 0%, #09120c 100%);
      border: 1px solid rgba(201, 163, 95, 0.45);
      border-radius: 200px 200px 18px 18px;
      padding: 12px 12px 22px;
      position: relative;
      display: flex;
      flex-direction: column;
      transition: all 0.35s var(--ease);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.28);
    }}
    .garment-card:hover {{
      transform: translateY(-8px);
      border-color: var(--gold-spark);
      box-shadow: 0 24px 50px rgba(0, 0, 0, 0.45), 0 0 20px rgba(201, 163, 95, 0.25);
    }}

    .card-media {{
      position: relative;
      width: 100%;
      height: 380px;
      border-radius: 190px 190px 12px 12px;
      overflow: hidden;
      background: #040906;
    }}
    .card-media img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.6s var(--ease);
    }}
    .garment-card:hover .card-media img {{
      transform: scale(1.06);
    }}

    .card-wish-btn {{
      position: absolute;
      top: 16px;
      right: 16px;
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: rgba(4, 9, 6, 0.7);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(201, 163, 95, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--cream);
      cursor: pointer;
      z-index: 3;
      transition: all 0.25s ease;
    }}
    .card-wish-btn:hover, .card-wish-btn.liked {{
      background: var(--gold);
      color: #241A0C;
      border-color: var(--gold-spark);
    }}

    .quick-examine-btn {{
      position: absolute;
      bottom: 14px;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      opacity: 0;
      background: rgba(4, 9, 6, 0.85);
      border: 1px solid var(--gold);
      color: var(--gold-spark);
      padding: 9px 22px;
      border-radius: 999px;
      font-family: var(--sans);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      z-index: 3;
      transition: all 0.3s ease;
      white-space: nowrap;
    }}
    .garment-card:hover .quick-examine-btn {{
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }}
    .quick-examine-btn:hover {{
      background: var(--gold);
      color: #241A0C;
    }}

    .card-info {{
      padding: 18px 10px 0;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}
    .card-craft-type {{
      font-family: var(--sans);
      font-size: 10.5px;
      font-weight: 600;
      letter-spacing: 2.2px;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 6px;
    }}
    .card-title {{
      font-family: var(--serif);
      font-size: 21px;
      font-weight: 500;
      color: var(--cream-hi);
      line-height: 1.25;
      margin-bottom: 6px;
    }}
    .card-fabric {{
      font-size: 12.5px;
      color: rgba(239, 228, 200, 0.72);
      margin-bottom: 16px;
      line-height: 1.4;
    }}
    .card-bottom-row {{
      margin-top: auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid rgba(201, 163, 95, 0.2);
      padding-top: 12px;
    }}
    .card-price-group {{
      display: flex;
      flex-direction: column;
    }}
    .card-price-label {{
      font-size: 9.5px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: rgba(201, 163, 95, 0.8);
    }}
    .card-price {{
      font-family: var(--serif);
      font-size: 19px;
      font-weight: 600;
      color: var(--gold-spark);
    }}
    .card-add-btn {{
      background: transparent;
      border: 1px solid rgba(201, 163, 95, 0.6);
      border-radius: 999px;
      padding: 8px 18px;
      font-family: var(--sans);
      font-size: 10.5px;
      font-weight: 600;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #ffffff;
      cursor: pointer;
      transition: all 0.25s ease;
    }}
    .card-add-btn:hover {{
      background: var(--gold);
      color: #241A0C;
      border-color: var(--gold);
    }}

    /* Quick Examine Modal */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(4, 9, 6, 0.85);
      backdrop-filter: blur(12px);
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }}
    .modal-overlay.open {{
      opacity: 1;
      pointer-events: auto;
    }}
    .modal-card {{
      background: linear-gradient(135deg, #112318 0%, #07100a 100%);
      border: 1px solid rgba(201, 163, 95, 0.5);
      border-radius: 24px;
      max-width: 900px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.8);
      position: relative;
      display: grid;
      grid-template-columns: 1fr 1fr;
    }}
    .modal-close-btn {{
      position: absolute;
      top: 16px;
      right: 18px;
      background: none;
      border: none;
      color: var(--cream);
      font-size: 26px;
      cursor: pointer;
      z-index: 5;
    }}
    .modal-img-frame {{
      height: 100%;
      min-height: 440px;
      background: #040906;
    }}
    .modal-img-frame img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .modal-detail-col {{
      padding: 40px 32px;
      display: flex;
      flex-direction: column;
      color: #fff;
    }}
    .modal-kicker {{
      font-size: 11px;
      letter-spacing: 2px;
      color: var(--gold);
      text-transform: uppercase;
      font-weight: 600;
      margin-bottom: 8px;
    }}
    .modal-title {{
      font-family: var(--serif);
      font-size: 28px;
      color: var(--cream-hi);
      line-height: 1.2;
      margin-bottom: 12px;
    }}
    .modal-price {{
      font-family: var(--serif);
      font-size: 24px;
      color: var(--gold-spark);
      margin-bottom: 16px;
    }}
    .modal-desc {{
      font-size: 14px;
      line-height: 1.7;
      color: rgba(239, 228, 200, 0.85);
      margin-bottom: 24px;
    }}
    .spec-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      background: rgba(4, 9, 6, 0.5);
      border: 1px solid rgba(201, 163, 95, 0.25);
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 24px;
    }}
    .spec-lbl {{
      font-size: 10px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: var(--gold);
      display: block;
    }}
    .spec-val {{
      font-size: 13px;
      color: var(--cream);
      font-weight: 500;
    }}
    .size-picker-title {{
      font-size: 11px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: var(--cream);
      margin-bottom: 10px;
      display: block;
    }}
    .size-chips {{
      display: flex;
      gap: 8px;
      margin-bottom: 24px;
    }}
    .size-chip {{
      padding: 6px 14px;
      border: 1px solid rgba(201, 163, 95, 0.4);
      background: rgba(4, 9, 6, 0.4);
      border-radius: 6px;
      color: var(--cream);
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .size-chip.active, .size-chip:hover {{
      background: var(--gold);
      color: #241A0C;
      border-color: var(--gold-spark);
    }}
    .modal-action-row {{
      display: flex;
      gap: 12px;
      margin-top: auto;
    }}
    .modal-add-bag {{
      flex: 1;
      padding: 13px 20px;
      background: var(--gold);
      color: #241A0C;
      border: 1px solid var(--gold-light);
      border-radius: 999px;
      font-family: var(--sans);
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.25s ease;
    }}
    .modal-add-bag:hover {{
      background: var(--gold-spark);
      transform: translateY(-2px);
    }}
    .modal-bespoke {{
      padding: 13px 20px;
      background: transparent;
      color: var(--gold-light);
      border: 1px solid rgba(201, 163, 95, 0.6);
      border-radius: 999px;
      font-family: var(--sans);
      font-size: 11.5px;
      font-weight: 600;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.25s ease;
    }}
    .modal-bespoke:hover {{
      background: rgba(201, 163, 95, 0.15);
      border-color: var(--gold);
    }}

    /* Toast */
    .toast-popup {{
      position: fixed;
      bottom: 28px;
      right: 28px;
      background: #112417;
      border: 1px solid var(--gold);
      color: #ffffff;
      padding: 14px 24px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
      z-index: 10001;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13.5px;
      opacity: 0;
      transform: translateY(20px);
      pointer-events: none;
      transition: all 0.3s ease;
    }}
    .toast-popup.show {{
      opacity: 1;
      transform: translateY(0);
    }}

    @media (max-width: 768px) {{
      .modal-card {{
        grid-template-columns: 1fr;
      }}
      .modal-img-frame {{
        min-height: 280px;
        height: 280px;
      }}
      .modal-detail-col {{
        padding: 24px 20px;
      }}
    }}
  </style>
</head>
<body>

{GLOBAL_HEADER_HTML}

<div class="atelier-announcement">
  ✦ Handcrafted Banarasi Silks, Zardozi Embroideries &amp; Tailored Drapes &middot; Worldwide Express Concierge
</div>

<header class="catalog-hero">
  <div class="catalog-hero-inner">
    <span class="catalog-kicker">Atelier Curation</span>
    <h1 class="catalog-title">The Grand Garments Gallery</h1>
    <p class="catalog-tagline">"From timeless banarasi weaves to hand-cut modern drapes &mdash; explore our complete atelier portfolio."</p>

    <!-- Controls -->
    <div class="catalog-controls-card">
      <div class="filter-tabs" id="filterTabs">
        <button class="filter-tab active" data-category="all">All Garments</button>
        <button class="filter-tab" data-category="sarees">Sarees</button>
        <button class="filter-tab" data-category="kurta-sets">Kurta Sets</button>
        <button class="filter-tab" data-category="lehengas">Lehengas</button>
        <button class="filter-tab" data-category="dresses">Dresses &amp; Sets</button>
        <button class="filter-tab" data-category="dupattas">Dupattas</button>
        <button class="filter-tab" data-category="unstitched">Unstitched Fabrics</button>
      </div>

      <div class="catalog-search-row">
        <div class="search-box">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="searchInput" class="search-input" placeholder="Search silk sarees, anarkali, zardozi..." autocomplete="off">
        </div>

        <div class="sort-box">
          <select id="sortSelect" aria-label="Sort garments">
            <option value="featured">Featured Curations</option>
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
            <option value="name-asc">Name: A to Z</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</header>

<main class="catalog-section">
  <div class="catalog-meta">
    <span id="activeFilterLabel">Displaying all curated creations</span>
    <span>Showing <span class="catalog-count-badge" id="visibleCount">12</span> garments</span>
  </div>

  <div class="garments-grid" id="garmentsGrid">
    <!-- Garments Injected via JavaScript -->
  </div>

  <!-- See More Pagination Button -->
  <div class="see-more-wrap" id="seeMoreWrap" style="display: none;">
    <button type="button" class="see-more-btn" id="seeMoreBtn">
      <span>See More Garments</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
    </button>
  </div>
</main>

<!-- Quick Examine Modal -->
<div class="modal-overlay" id="quickModal" role="dialog" aria-modal="true">
  <div class="modal-card">
    <button class="modal-close-btn" id="modalCloseBtn" aria-label="Close modal">&times;</button>
    <div class="modal-img-frame">
      <img id="modalImg" src="" alt="Garment presentation">
    </div>
    <div class="modal-detail-col">
      <span class="modal-kicker" id="modalCraft">Handcrafted Masterpiece</span>
      <h2 class="modal-title" id="modalTitle">Noor-e-Kashmir Silk Saree</h2>
      <div class="modal-price" id="modalPrice">₹48,500</div>
      <p class="modal-desc" id="modalDesc">Detailed description of this bespoke piece will appear here.</p>

      <div class="spec-grid">
        <div class="spec-item">
          <span class="spec-lbl">Fabric</span>
          <span class="spec-val" id="modalFabric">Pure Silk</span>
        </div>
        <div class="spec-item">
          <span class="spec-lbl">Weave / Craft</span>
          <span class="spec-val" id="modalWeave">Kalamkari &amp; Zardozi</span>
        </div>
        <div class="spec-item">
          <span class="spec-lbl">Origin</span>
          <span class="spec-val" id="modalOrigin">Varanasi Looms</span>
        </div>
        <div class="spec-item">
          <span class="spec-lbl">Atelier Delivery</span>
          <span class="spec-val">Express Insured Dispatch</span>
        </div>
      </div>

      <span class="size-picker-title">Select Sizing</span>
      <div class="size-chips" id="modalSizePicker">
        <button type="button" class="size-chip active">Custom Bespoke</button>
        <button type="button" class="size-chip">Standard S</button>
        <button type="button" class="size-chip">Standard M</button>
        <button type="button" class="size-chip">Standard L</button>
      </div>

      <div class="modal-action-row">
        <button class="modal-add-bag" id="modalAddBagBtn">Add to Atelier Bag</button>
        <button class="modal-bespoke" id="modalBespokeBtn">Consult Tailor</button>
      </div>
    </div>
  </div>
</div>

<div class="toast-popup" id="toastMsg">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--gold-spark)" stroke-width="2"><path d="M20 6L9 17l-5-5"></path></svg>
  <span id="toastText">Item saved to bag</span>
</div>

{GLOBAL_FOOTER_HTML}
{GLOBAL_HEADER_FOOTER_JS}

<script>
(function() {{
  // Master Garments Data
  const DEFAULT_GARMENTS = {master_garments_raw};

  // State
  let GARMENTS = [...DEFAULT_GARMENTS];
  const savedCatalog = localStorage.getItem("aleen_master_catalog");
  if (savedCatalog) {{
    try {{
      const parsed = JSON.parse(savedCatalog);
      if (Array.isArray(parsed) && parsed.length > 0) {{
        GARMENTS = parsed;
      }}
    }} catch(e) {{
      console.warn("Using default garments:", e);
    }}
  }}

  let currentCategory = "all";
  let searchQuery = "";
  let sortOrder = "featured";
  let visibleLimit = 8;
  const PAGE_SIZE = 8;
  let currentFilteredList = [];
  let wishlist = JSON.parse(localStorage.getItem("aleen_wishlist") || "[]");
  let bag = JSON.parse(localStorage.getItem("aleen_bag") || "[]");
  let activeModalItem = null;

  // Check URL query parameters (category & filter=new)
  const urlParams = new URLSearchParams(window.location.search);
  const catParam = urlParams.get("category");
  const filterParam = urlParams.get("filter");
  let isNewArrivalsOnly = (filterParam === "new");

  if (catParam) {{
    currentCategory = catParam.toLowerCase();
  }}

  // DOM Elements
  const gridEl = document.getElementById("garmentsGrid");
  const countEl = document.getElementById("visibleCount");
  const filterTabsEl = document.getElementById("filterTabs");
  const searchInput = document.getElementById("searchInput");
  const sortSelect = document.getElementById("sortSelect");
  const toastEl = document.getElementById("toastMsg");
  const toastText = document.getElementById("toastText");
  const seeMoreWrap = document.getElementById("seeMoreWrap");
  const seeMoreBtn = document.getElementById("seeMoreBtn");

  // Modal Elements
  const modalEl = document.getElementById("quickModal");
  const modalCloseBtn = document.getElementById("modalCloseBtn");
  const modalImg = document.getElementById("modalImg");
  const modalCraft = document.getElementById("modalCraft");
  const modalTitle = document.getElementById("modalTitle");
  const modalPrice = document.getElementById("modalPrice");
  const modalDesc = document.getElementById("modalDesc");
  const modalFabric = document.getElementById("modalFabric");
  const modalWeave = document.getElementById("modalWeave");
  const modalOrigin = document.getElementById("modalOrigin");
  const modalAddBagBtn = document.getElementById("modalAddBagBtn");
  const modalBespokeBtn = document.getElementById("modalBespokeBtn");
  const modalSizePicker = document.getElementById("modalSizePicker");

  function showToast(msg) {{
    if (!toastEl || !toastText) return;
    toastText.textContent = msg;
    toastEl.classList.add("show");
    setTimeout(() => {{
      toastEl.classList.remove("show");
    }}, 3200);
  }}

  function formatPrice(num) {{
    return "₹" + Number(num).toLocaleString("en-IN");
  }}

  function filterAndSortGarments(resetPage = false) {{
    if (resetPage) {{
      visibleLimit = PAGE_SIZE;
    }}

    let filtered = GARMENTS.filter(item => {{
      const matchesCat = currentCategory === "all" || item.category === currentCategory;
      const q = searchQuery.toLowerCase().trim();
      const matchesSearch = !q || (
        (item.title && item.title.toLowerCase().includes(q)) ||
        (item.craft && item.craft.toLowerCase().includes(q)) ||
        (item.fabric && item.fabric.toLowerCase().includes(q)) ||
        (item.origin && item.origin.toLowerCase().includes(q))
      );
      const matchesNew = !isNewArrivalsOnly || (item.badge && item.badge.toLowerCase().includes("new")) || item.badge === "Heritage Edition" || item.badge === "Bestseller";
      return matchesCat && matchesSearch && matchesNew;
    }});

    if (sortOrder === "price-asc") {{
      filtered.sort((a, b) => a.price - b.price);
    }} else if (sortOrder === "price-desc") {{
      filtered.sort((a, b) => b.price - a.price);
    }} else if (sortOrder === "name-asc") {{
      filtered.sort((a, b) => a.title.localeCompare(b.title));
    }}

    currentFilteredList = filtered;
    renderGarments(filtered);
  }}

  function renderGarments(items) {{
    if (!gridEl) return;
    gridEl.innerHTML = "";

    if (items.length === 0) {{
      if (countEl) countEl.textContent = "0";
      if (seeMoreWrap) seeMoreWrap.style.display = "none";
      gridEl.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
          <p style="font-family: var(--serif-i); font-size: 24px; color: #554121; margin-bottom: 12px;">No atelier garments matched your filter.</p>
          <button class="filter-tab active" onclick="resetFilters()">Reset All Filters</button>
        </div>
      `;
      return;
    }}

    const toShow = items.slice(0, visibleLimit);
    if (countEl) countEl.textContent = `${{toShow.length}} of ${{items.length}}`;

    toShow.forEach(item => {{
      const isLiked = wishlist.includes(item.id);
      const card = document.createElement("article");
      card.className = "garment-card";
      card.innerHTML = `
        <div class="card-media">
          <button class="card-wish-btn ${{isLiked ? 'liked' : ''}}" data-id="${{item.id}}" aria-label="Save to Wishlist">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="${{isLiked ? 'currentColor' : 'none'}}" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
          </button>
          <img src="${{item.image}}" alt="${{item.title}}" loading="lazy" />
          <button class="quick-examine-btn" data-id="${{item.id}}">
            <span>Examine Craft</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
          </button>
          ${{item.badge ? `<span class="card-badge">${{item.badge}}</span>` : ''}}
        </div>
        <div class="card-info">
          <span class="card-origin">${{item.craft || 'Artisanal Needlework'}}</span>
          <h3 class="card-title">${{item.title}}</h3>
          <p class="card-price">${{formatPrice(item.price)}}</p>
          <div class="card-foot">
            <span class="card-cat-badge">${{item.categoryLabel || item.category}}</span>
            <button class="card-add-btn" data-id="${{item.id}}">Acquire</button>
          </div>
        </div>
      `;
      gridEl.appendChild(card);
    }});

    // Update See More Button
    if (seeMoreWrap && seeMoreBtn) {{
      if (visibleLimit < items.length) {{
        const remaining = items.length - visibleLimit;
        seeMoreWrap.style.display = "block";
        seeMoreBtn.innerHTML = `<span>See More Garments (${{remaining}} remaining)</span> <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12l7 7 7-7"/></svg>`;
      }} else {{
        seeMoreWrap.style.display = "none";
      }}
    }}
  }}

  if (seeMoreBtn) {{
    seeMoreBtn.addEventListener("click", () => {{
      visibleLimit += PAGE_SIZE;
      renderGarments(currentFilteredList);
    }});
  }}

  window.resetFilters = function() {{
    currentCategory = "all";
    searchQuery = "";
    sortOrder = "featured";
    isNewArrivalsOnly = false;
    if (searchInput) searchInput.value = "";
    if (sortSelect) sortSelect.value = "featured";
    updateTabButtons();
    filterAndSortGarments(true);
  }};

  function updateTabButtons() {{
    if (!filterTabsEl) return;
    const tabs = filterTabsEl.querySelectorAll(".filter-tab");
    tabs.forEach(tab => {{
      if (tab.getAttribute("data-category") === currentCategory) {{
        tab.classList.add("active");
      }} else {{
        tab.classList.remove("active");
      }}
    }});
  }}

  // Modal Logic
  function openModal(id) {{
    const item = GARMENTS.find(g => g.id === id);
    if (!item || !modalEl) return;
    activeModalItem = item;

    if (modalImg) {{
      modalImg.src = item.image;
      modalImg.alt = item.title;
    }}
    if (modalCraft) modalCraft.textContent = item.craft || "Handcrafted Masterpiece";
    if (modalTitle) modalTitle.textContent = item.title;
    if (modalPrice) modalPrice.textContent = formatPrice(item.price);
    if (modalDesc) modalDesc.textContent = item.desc || "Bespoke creation by Aleen master artisans.";
    if (modalFabric) modalFabric.textContent = item.fabric || "Pure Silk";
    if (modalWeave) modalWeave.textContent = item.craft || "Artisan Weave";
    if (modalOrigin) modalOrigin.textContent = item.origin || "Aleen Looms";

    modalEl.classList.add("open");
    document.body.style.overflow = "hidden";
  }}

  function closeModal() {{
    if (!modalEl) return;
    modalEl.classList.remove("open");
    document.body.style.overflow = "";
    activeModalItem = null;
  }}

  if (filterTabsEl) {{
    filterTabsEl.addEventListener("click", e => {{
      const btn = e.target.closest(".filter-tab");
      if (!btn) return;
      currentCategory = btn.getAttribute("data-category");
      isNewArrivalsOnly = false;
      updateTabButtons();
      filterAndSortGarments(true);
    }});
  }}

  if (searchInput) {{
    searchInput.addEventListener("input", e => {{
      searchQuery = e.target.value;
      filterAndSortGarments(true);
    }});
  }}

  if (sortSelect) {{
    sortSelect.addEventListener("change", e => {{
      sortOrder = e.target.value;
      filterAndSortGarments(true);
    }});
  }}

  if (gridEl) {{
    gridEl.addEventListener("click", e => {{
      const wishBtn = e.target.closest(".card-wish-btn");
      if (wishBtn) {{
        e.stopPropagation();
        const id = wishBtn.getAttribute("data-id");
        toggleWishlist(id, wishBtn);
        return;
      }}

      const examineBtn = e.target.closest(".quick-examine-btn");
      if (examineBtn) {{
        e.stopPropagation();
        const id = examineBtn.getAttribute("data-id");
        openModal(id);
        return;
      }}

      const addBtn = e.target.closest(".card-add-btn");
      if (addBtn) {{
        e.stopPropagation();
        const id = addBtn.getAttribute("data-id");
        addToBag(id);
        return;
      }}

      const card = e.target.closest(".garment-card");
      if (card) {{
        const id = card.querySelector(".quick-examine-btn")?.getAttribute("data-id");
        if (id) openModal(id);
      }}
    }});
  }}

  function toggleWishlist(id, btnEl) {{
    const idx = wishlist.indexOf(id);
    if (idx > -1) {{
      wishlist.splice(idx, 1);
      if (btnEl) btnEl.classList.remove("liked");
      showToast("Garment removed from private wishlist");
    }} else {{
      wishlist.push(id);
      if (btnEl) btnEl.classList.add("liked");
      showToast("Garment saved to your private wishlist");
    }}
    localStorage.setItem("aleen_wishlist", JSON.stringify(wishlist));
  }}

  function addToBag(id, size = "Standard Boutique Sizing") {{
    const item = GARMENTS.find(g => g.id === id);
    if (!item) return;

    const existing = bag.find(b => b.id === id && b.size === size);
    if (existing) {{
      existing.qty = (existing.qty || 1) + 1;
    }} else {{
      bag.push({{
        id: item.id,
        title: item.title,
        price: item.price,
        image: item.image,
        size: size,
        qty: 1
      }});
    }}
    localStorage.setItem("aleen_bag", JSON.stringify(bag));
    showToast(`${{item.title}} added to Atelier Bag`);
  }}

  if (modalSizePicker) {{
    modalSizePicker.addEventListener("click", e => {{
      const chip = e.target.closest(".size-chip");
      if (!chip) return;
      modalSizePicker.querySelectorAll(".size-chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
    }});
  }}

  if (modalAddBagBtn) {{
    modalAddBagBtn.addEventListener("click", () => {{
      if (!activeModalItem) return;
      const selectedSize = modalSizePicker?.querySelector(".size-chip.active")?.textContent || "Standard";
      addToBag(activeModalItem.id, selectedSize);
      closeModal();
    }});
  }}

  if (modalBespokeBtn) {{
    modalBespokeBtn.addEventListener("click", () => {{
      if (!activeModalItem) return;
      showToast(`Master tailor consultation initiated for ${{activeModalItem.title}}`);
      closeModal();
    }});
  }}

  if (modalCloseBtn) modalCloseBtn.addEventListener("click", closeModal);
  if (modalEl) {{
    modalEl.addEventListener("click", e => {{
      if (e.target === modalEl) closeModal();
    }});
  }}

  document.addEventListener("keydown", e => {{
    if (e.key === "Escape" && modalEl?.classList.contains("open")) {{
      closeModal();
    }}
  }});

  // Boot
  updateTabButtons();
  filterAndSortGarments(true);
}})();
</script>

</body>
</html>
"""

dest = os.path.join(SITE_DIR, "collections.html")
with open(dest, "w", encoding="utf-8") as f:
    f.write(COLLECTIONS_PAGE_HTML)

print("✦ Rebuilt collections.html with Picture 3 background, fixed JS, and global header/footer!")

