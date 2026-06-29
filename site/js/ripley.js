/* Occult Image DB — George Ripley & The Alchemical Work */
const RIPLEY = { items: [], works: {}, ripleyIds: [] };

async function boot() {
  const cat = await fetch("../data/catalog.json").then(r => r.json());
  RIPLEY.items = cat.items || [];
  RIPLEY.works = Object.fromEntries((cat.works || []).map(w => [w.key, w]));

  // gather all Ripley Scroll images
  RIPLEY.ripleyIds = RIPLEY.items
    .filter(i => i.work_key === "ripley_scrolls" && i.tier !== "page_scan")
    .sort((a, b) => (a.seq || 0) - (b.seq || 0))
    .map(i => i.id);

  renderScrollGallery();
}

function renderScrollGallery() {
  const gallery = document.getElementById("scroll-gallery");
  if (!gallery || !RIPLEY.ripleyIds.length) return;

  const cards = RIPLEY.ripleyIds.map(id => {
    const it = RIPLEY.items.find(i => i.id === id);
    if (!it) return "";
    return `<a class="scroll-card" href="item.html?id=${encodeURIComponent(id)}">
      <img loading="lazy" src="${it.thumb}" alt="${(it.title || "").replace(/"/g, "&quot;")}">
      <span class="scroll-label">${(it.title || "").slice(0, 60)}</span>
    </a>`;
  }).join("");

  gallery.innerHTML = cards;
}

boot();
