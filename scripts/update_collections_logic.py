import os

script_path = os.path.join(os.path.dirname(__file__), "rebuild_collections_page.py")
with open(script_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the URL check and filtering logic
old_block_start = '  // Check URL category query\n  const urlParams = new URLSearchParams(window.location.search);'
old_block_end = '  // Boot\n  updateTabButtons();\n  filterAndSortGarments(true);'

pos1 = text.find(old_block_start)
pos2 = text.find(old_block_end)

if pos1 == -1 or pos2 == -1:
    print(f"Failed to find markers: pos1={pos1}, pos2={pos2}")
    exit(1)

new_block = '''  // Check URL query parameters (category & filter=new)
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
'''

new_text = text[:pos1] + new_block + '\n' + text[pos2:]

with open(script_path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("Updated rebuild_collections_page.py successfully!")

