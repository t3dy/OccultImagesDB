/* Occult Image DB — Explore homepage tab controller */
const EX = { items: [], works: [], entities: null, topics: [], collections: [], eraCats: [], tab: "rooms", q: "" };
const yearOf = d => { const m = (d || "").match(/-?\d{3,4}/); return m ? +m[0] : 9999; };
const view = () => document.getElementById("view");

async function boot() {
  const [catalog, entities, topics, collections, eraCats] = await Promise.all([
    fetch("../data/catalog.json").then(r => r.json()),
    fetch("../data/entities.json").then(r => r.json()),
    fetch("../data/topics.json").then(r => r.json()).catch(() => ({ topics: [] })),
    fetch("../data/collections.json").then(r => r.json()).catch(() => ({ collections: [] })),
    fetch("../data/era_categories.json").then(r => r.json()).catch(() => ({ eras: [] })),
  ]);
  EX.items = catalog.items || []; EX.works = catalog.works || [];
  EX.entities = entities; EX.topics = topics.topics || []; EX.collections = collections.collections || [];
  EX.eraCats = eraCats.eras || [];
  const p = new URLSearchParams(location.search);
  if (p.get("tab")) EX.tab = p.get("tab");
  if (p.get("q")) EX.q = p.get("q").toLowerCase().trim();
  wire();
  if (EX.q) document.getElementById("q").value = EX.q;
  render();
}

function wire() {
  document.querySelectorAll("#tabbar button").forEach(b => {
    b.classList.toggle("on", b.dataset.tab === EX.tab);
    b.onclick = () => { EX.tab = b.dataset.tab; EX.q = ""; document.getElementById("q").value = "";
      document.querySelectorAll("#tabbar button").forEach(x => x.classList.toggle("on", x === b)); render(); };
  });
  const q = document.getElementById("q");
  q.oninput = () => { EX.q = q.value.toLowerCase().trim(); render(); };
}

function catCard({ href, thumb, title, sub, count, badge, soon }) {
  const cover = thumb
    ? `<img decoding="async" src="${thumb}" alt="${ESC(title)}">`
    : `<div class="cat-noimg">☿</div>`;
  return `<a class="cat-card${soon ? " soon" : ""}" href="${href}">
    <div class="cat-cover">${cover}${badge ? `<span class="cat-badge">${badge}</span>` : ""}</div>
    <div class="cat-meta"><p class="cat-title">${ESC(title)}</p>
      ${sub ? `<p class="cat-sub">${ESC(sub)}</p>` : ""}
      ${count != null ? `<span class="cat-count">${count} image${count === 1 ? "" : "s"}</span>` : ""}</div>
  </a>`;
}
const coverThumb = imgs => imgs.length ? imgs[0].thumb : null;

function render() {
  if (EX.q) return renderSearch();
  ({ rooms: tabRooms, timeline: tabTimeline, eras: tabEras, regions: tabRegions, topics: tabTopics, media: tabMedia,
     figures: tabFigures, collections: tabCollections, gallery: tabGallery }[EX.tab] || tabRooms)();
}

function renderSearch() {
  const q = EX.q;
  const res = EX.items.filter(it =>
    `${it.title} ${it.creator} ${it._workTitle || ""} ${(it.motifs || []).join(" ")} ${it.summary || ""}`.toLowerCase().includes(q));
  view().innerHTML = `<div class="view-head"><h2>${res.length} result${res.length === 1 ? "" : "s"} for “${ESC(q)}”</h2></div><div class="masonry" id="m"></div>`;
  renderMasonry(document.getElementById("m"), res);
}

function tabRooms() {
  const byId = Object.fromEntries(EX.items.map(i => [i.id, i]));
  const rows = EX.eraCats.map(eb => {
    const cards = eb.categories.map(c => {
      const cov = c.cover && byId[c.cover];
      const thumb = (cov && cov.thumb) || (EX.items.find(i => i.era === eb.era) || {}).thumb;
      const href = `entity.html?type=category&key=${encodeURIComponent(eb.era + "__" + c.key)}`;
      return `<a class="gal-card" href="${href}">
        <span class="gal-cover">${thumb ? `<img loading="lazy" src="${thumb}" alt="${ESC(c.label)}">` : `<span class="cat-noimg">☿</span>`}</span>
        <span class="gal-meta"><b>${ESC(c.label)}</b><i>${c.count} image${c.count === 1 ? "" : "s"}</i></span></a>`;
    }).join("");
    const eraN = EX.items.filter(i => i.era === eb.era).length;
    return `<section class="era-room">
      <div class="era-room-head"><h3><a href="entity.html?type=era&key=${eb.era}">${ERA_LABEL[eb.era] || CAP(eb.era)}</a></h3>
        <a class="era-room-all" href="entity.html?type=era&key=${eb.era}">all ${eraN} →</a></div>
      <div class="gal-row">${cards}</div></section>`;
  }).join("");
  view().innerHTML = `<div class="view-head"><h2>The archive, room by room</h2>
    <p class="view-sub">Each era opens onto its characteristic galleries — sculpture and gems in antiquity,
      the great manuscripts of the Middle Ages, the engraved emblem of the Baroque. Pick a room to enter.</p></div>
    ${rows}`;
}

function tabTimeline() {
  const imgs = EX.items.slice().sort((a, b) =>
    (ERA_ORDER[a.era] - ERA_ORDER[b.era]) || (yearOf(a.date) - yearOf(b.date)) || a.work.localeCompare(b.work));
  const eras = [...new Set(imgs.map(i => i.era))].sort((a, b) => ERA_ORDER[a] - ERA_ORDER[b]);
  view().innerHTML = `<div class="view-head"><h2>The whole tradition, in order</h2>
    <p class="view-sub">${imgs.length} images from the first ouroboros to the Baroque emblem. Click ⤢ to zoom.</p></div>` +
    eras.map(e => `<section class="tl-band"><h3 class="band-h">${ERA_LABEL[e] || CAP(e)}
      <span>${imgs.filter(i => i.era === e).length}</span></h3><div class="masonry" data-era="${e}"></div></section>`).join("");
  eras.forEach(e => renderMasonry(view().querySelector(`.masonry[data-era="${e}"]`), imgs.filter(i => i.era === e)));
}

function tabEras() {
  const eras = [...new Set(EX.items.map(i => i.era))].sort((a, b) => ERA_ORDER[a] - ERA_ORDER[b]);
  grid("Browse by era", "From late antiquity to the early-modern Baroque.",
    eras.map(e => { const im = EX.items.filter(i => i.era === e);
      return catCard({ href: `entity.html?type=era&key=${e}`, thumb: coverThumb(im), title: ERA_LABEL[e] || CAP(e), count: im.length }); }));
}

function tabRegions() {
  const cards = REGIONS.map(r => { const im = EX.items.filter(i => regionKeyOf(i) === r.key);
    return im.length ? catCard({ href: `entity.html?type=region&key=${r.key}`, thumb: coverThumb(im), title: r.name, count: im.length }) : "";
  }).filter(Boolean);
  grid("Browse by region", "Where the images were made — from Hellenistic Egypt to Jacobean England.", cards);
}

function tabTopics() {
  const cards = EX.topics.map(t => {
    const im = EX.items.filter(i => imageMatches(i, t.match));
    return catCard({ href: `entity.html?type=topic&key=${t.key}`, thumb: coverThumb(im), title: t.name,
      sub: t.blurb, count: t.status === "live" ? im.length : null,
      badge: t.status === "coming_soon" ? "coming soon" : null, soon: t.status === "coming_soon" });
  });
  grid("Browse by topic", "The domains of esoteric historiography — drawn from the project's research databases.", cards);
}

function tabMedia() {
  const counts = {};
  EX.items.forEach(i => { if (i.medium) counts[i.medium] = (counts[i.medium] || 0) + 1; });
  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  grid("Browse by medium", "The material form of the image — manuscript, woodcut, engraving, painting, gem, object …",
    sorted.map(([md]) => { const im = EX.items.filter(i => i.medium === md);
      return catCard({ href: `gallery.html?medium=${encodeURIComponent(md)}`, thumb: coverThumb(im), title: CAP(md), count: im.length }); }));
}

function tabFigures() {
  const cards = (EX.entities.creators || []).map(c => {
    const im = EX.items.filter(i => (c.works || []).includes(i.work_key));
    return catCard({ href: `entity.html?type=creator&key=${c.key}`, thumb: coverThumb(im), title: c.name,
      sub: c.dates, count: im.length });
  });
  grid("Browse by figure", "The makers, magi, and adepts behind the images.", cards);
}

function tabCollections() {
  const cards = EX.collections.map(c => {
    const im = EX.items.filter(i => imageMatches(i, c.match));
    const cov = c.cover && EX.items.find(i => i.id === c.cover);
    return catCard({ href: `entity.html?type=collection&key=${c.key}`, thumb: (cov && cov.thumb) || coverThumb(im),
      title: c.title, count: c.status === "live" ? im.length : null,
      badge: c.status === "coming_soon" ? "coming soon" : "curated", soon: c.status === "coming_soon" });
  });
  grid("Curated collections", "Hand-built thematic journeys through the archive.", cards, "cards-wide");
}

function tabGallery() {
  view().innerHTML = `<div class="view-head"><h2>All ${EX.items.length} images
    <a class="view-link" href="gallery.html">advanced filters →</a></h2>
    <p class="view-sub">Image-forward. Use the search above, or open the faceted gallery for era/tradition/motif filters.</p></div>
    <div class="masonry" id="m"></div>`;
  renderMasonry(document.getElementById("m"), EX.items);
}

function grid(title, sub, cards, cls = "") {
  view().innerHTML = `<div class="view-head"><h2>${title}</h2><p class="view-sub">${sub}</p></div>
    <div class="cat-grid ${cls}">${cards.join("")}</div>`;
}

// attach work titles for search
fetch("../data/catalog.json"); // noop warm
boot();
