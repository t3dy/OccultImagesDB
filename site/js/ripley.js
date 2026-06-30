/* Occult Image DB — George Ripley & The Alchemical Work */
const RIPLEY = { items: [], works: {}, ripleyItems: [] };

const esc_r = s => (s || "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

async function boot() {
  let cat;
  try {
    cat = await fetch("../data/catalog.json").then(r => r.json());
  } catch(e) {
    const g = document.getElementById("scroll-gallery");
    if (g) g.innerHTML = '<p style="color:var(--ink-dim);text-align:center;padding:40px 0">Catalog not built yet.</p>';
    return;
  }
  RIPLEY.items = cat.items || [];
  RIPLEY.works = Object.fromEntries((cat.works || []).map(w => [w.key, w]));

  // gather all Ripley Scroll images that are curated illustrations, sorted by seq
  RIPLEY.ripleyItems = RIPLEY.items
    .filter(i => i.work_key === "ripley_scrolls" && i.tier !== "page_scan")
    .sort((a, b) => (a.seq || 999) - (b.seq || 999));

  renderScrollGallery();
}

function renderScrollGallery() {
  const gallery = document.getElementById("scroll-gallery");
  if (!gallery) return;

  if (!RIPLEY.ripleyItems.length) {
    gallery.innerHTML = '<p style="color:var(--ink-dim);text-align:center;padding:40px 0">No Ripley Scroll images found in catalog.</p>';
    return;
  }

  // Update count badge
  const countEl = document.getElementById("scroll-count");
  if (countEl) countEl.textContent = `${RIPLEY.ripleyItems.length} images`;

  gallery.innerHTML = RIPLEY.ripleyItems.map(it => {
    const id   = it.id;
    const title = (it.title || id).replace(/"/g, "&quot;");
    // Use thumb for gallery display; fall back to card if thumb missing
    const src  = it.thumb || it.card || `images/thumbs/${encodeURIComponent(id)}.jpg`;
    const card = it.card  || `images/cards/${encodeURIComponent(id)}.jpg`;
    const shortTitle = (it.title || "").replace(/Ripley Scroll \([^)]+\) — /i, "").replace(/The Ripley Scroll — /i, "");
    return `<a class="scroll-card" href="item.html?id=${encodeURIComponent(id)}">
      <img loading="lazy" src="${esc_r(src)}"
           onerror="this.src='${esc_r(card)}';this.onerror=null"
           alt="${esc_r(title)}">
      <span class="scroll-label">${esc_r(shortTitle || title)}</span>
    </a>`;
  }).join("");
}

boot();
