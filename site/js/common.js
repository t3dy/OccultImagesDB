/* Occult Image DB — shared helpers: constants, matching, regions, masonry, lightbox */
const ESC = s => (s || "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const CAP = s => (s || "").replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
const ERA_LABEL = { antiquity: "Antiquity", medieval: "Medieval", renaissance: "Renaissance", early_modern: "Early modern", modern: "Modern" };
const ERA_ORDER = { antiquity: 0, medieval: 1, renaissance: 2, early_modern: 3, modern: 4 };

// macro-regions (match against an image's free-text region field)
const REGIONS = [
  { key: "mediterranean", name: "Mediterranean & Near East", terms: ["mediterranean", "egypt", "byzant", "africa", "greece", "arab", "near east"] },
  { key: "italy", name: "Italy", terms: ["venice", "italy", "italian", "florence", "rome"] },
  { key: "central_europe", name: "German Lands & Central Europe", terms: ["german", "hre", "bohemia", "frankfurt", "oppenheim", "hamburg", "hanau", "basel", "silesia", "switzerland", "austria"] },
  { key: "north_sea", name: "England & the Low Countries", terms: ["england", "english", "london", "dutch", "amsterdam", "low countries", "netherlands"] },
  { key: "latin_west", name: "The Latin West & Beyond", terms: ["latin west", "europe", "france", "spain", "various"] },
];
function regionKeyOf(img) {
  const r = (img.region || img.place || "").toLowerCase();
  for (const reg of REGIONS) if (reg.terms.some(t => r.includes(t))) return reg.key;
  return "latin_west";
}

// match an image against a {work_keys, traditions, motif_terms, ids} query (OR across present clauses)
function imageMatches(img, m) {
  if (!m) return false;
  if (m.ids && m.ids.includes(img.id)) return true;
  if (m.work_keys && m.work_keys.includes(img.work_key)) return true;
  if (m.traditions && m.traditions.includes(img.tradition)) return true;
  if (m.motif_terms && m.motif_terms.length) {
    const mot = (img.motifs || []).map(x => x.toLowerCase());
    if (m.motif_terms.some(t => mot.includes(t.toLowerCase()))) return true;
  }
  return false;
}

/* ---------- brief card description (lede of the summary, markdown-stripped) ---------- */
function briefDesc(img, max = 150) {
  let s = img.summary || "";
  s = s.split(/\n\s*##/)[0];                       // text before the first ## section = the lede
  s = s.replace(/\[\[[^\]|]*\|([^\]]+)\]\]/g, "$1") // [[x|Label]] -> Label
       .replace(/\[\[([^\]]+)\]\]/g, "$1")          // [[x]] -> x
       .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")      // [text](url) -> text
       .replace(/[*_`#>]/g, "")                       // strip md emphasis/markers
       .replace(/\s+/g, " ").trim();
  if (!s) s = [img.creator, img.work].filter(Boolean).join(" · ");
  if (s.length > max) {
    s = s.slice(0, max);
    s = s.slice(0, Math.max(s.lastIndexOf(" "), 60)).replace(/[\s,;:.]+$/, "") + "…";
  }
  return s;
}

/* ---------- image-forward masonry ---------- */
function masonryCard(img) {
  const a = document.createElement("a");
  a.className = "mcard";
  a.href = `item.html?id=${encodeURIComponent(img.id)}`;
  a.dataset.id = img.id;
  const title = (img.title || "").replace(/[*`]/g, "");
  a.innerHTML = `<span class="mcard-img"><img decoding="async" src="${img.thumb}" alt="${ESC(title)}">
    <span class="mcard-zoom" title="Zoom">⤢</span></span>
    <span class="mcard-cap"><b>${ESC(title)}</b><i>${ESC(img.creator || "")}${img.date ? " · " + ESC(img.date) : ""}</i><em>${ESC(briefDesc(img))}</em></span>`;
  return a;
}
// render images into container; clicking the zoom badge opens the lightbox, clicking card navigates
function renderMasonry(container, images, opts = {}) {
  container.innerHTML = "";
  const frag = document.createDocumentFragment();
  images.forEach((img, i) => {
    const card = masonryCard(img);
    card.querySelector(".mcard-zoom").addEventListener("click", e => {
      e.preventDefault(); e.stopPropagation(); Lightbox.open(images, i);
    });
    frag.appendChild(card);
  });
  container.appendChild(frag);
  return images.length;
}

/* ---------- lightbox with zoom / pan ---------- */
const Lightbox = (() => {
  let el, imgEl, capEl, list = [], idx = 0, scale = 1, tx = 0, ty = 0, drag = null;
  function build() {
    el = document.createElement("div");
    el.className = "lbx"; el.hidden = true;
    el.innerHTML = `
      <button class="lbx-close" aria-label="Close">×</button>
      <button class="lbx-nav lbx-prev" aria-label="Previous">‹</button>
      <button class="lbx-nav lbx-next" aria-label="Next">›</button>
      <div class="lbx-stage"><img alt=""></div>
      <div class="lbx-bar">
        <div class="lbx-cap"></div>
        <div class="lbx-tools">
          <button data-z="out">−</button><button data-z="reset">⟳</button><button data-z="in">+</button>
          <a class="lbx-open" href="#">Open full record →</a>
        </div>
      </div>`;
    document.body.appendChild(el);
    imgEl = el.querySelector("img");
    capEl = el.querySelector(".lbx-cap");
    el.querySelector(".lbx-close").onclick = close;
    el.querySelector(".lbx-prev").onclick = () => step(-1);
    el.querySelector(".lbx-next").onclick = () => step(1);
    el.querySelector('[data-z=in]').onclick = () => zoom(1.4);
    el.querySelector('[data-z=out]').onclick = () => zoom(1 / 1.4);
    el.querySelector('[data-z=reset]').onclick = reset;
    el.addEventListener("click", e => { if (e.target === el) close(); });
    const stage = el.querySelector(".lbx-stage");
    stage.addEventListener("wheel", e => { e.preventDefault(); zoom(e.deltaY < 0 ? 1.15 : 1 / 1.15); }, { passive: false });
    imgEl.addEventListener("dblclick", () => scale > 1 ? reset() : zoom(2.2));
    imgEl.addEventListener("pointerdown", e => { if (scale <= 1) return; drag = { x: e.clientX - tx, y: e.clientY - ty }; imgEl.setPointerCapture(e.pointerId); });
    imgEl.addEventListener("pointermove", e => { if (!drag) return; tx = e.clientX - drag.x; ty = e.clientY - drag.y; apply(); });
    imgEl.addEventListener("pointerup", e => { drag = null; });
    document.addEventListener("keydown", e => {
      if (el.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") step(-1);
      else if (e.key === "ArrowRight") step(1);
      else if (e.key === "+" || e.key === "=") zoom(1.4);
      else if (e.key === "-") zoom(1 / 1.4);
    });
  }
  function apply() { imgEl.style.transform = `translate(${tx}px,${ty}px) scale(${scale})`; imgEl.style.cursor = scale > 1 ? "grab" : "default"; }
  function reset() { scale = 1; tx = 0; ty = 0; apply(); }
  function zoom(f) { scale = Math.min(8, Math.max(1, scale * f)); if (scale === 1) { tx = 0; ty = 0; } apply(); }
  function show() {
    const it = list[idx];
    imgEl.src = it.card || it.thumb;
    capEl.innerHTML = `<b>${ESC(it.title)}</b><span>${ESC(it.creator || "")}${it.date ? " · " + ESC(it.date) : ""}</span>`;
    el.querySelector(".lbx-open").href = `item.html?id=${encodeURIComponent(it.id)}`;
    reset();
  }
  function step(d) { idx = (idx + d + list.length) % list.length; show(); }
  function open(images, i) { if (!el) build(); list = images; idx = i || 0; el.hidden = false; document.body.style.overflow = "hidden"; show(); }
  function close() { el.hidden = true; document.body.style.overflow = ""; }
  return { open };
})();
