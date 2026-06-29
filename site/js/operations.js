/* Occult Image DB — The Twelve Processes of the Great Work (Ripley's gates) */
const OP = { items: [], byId: {}, works: {}, ops: [], meta: {}, sort: "chrono", group: "image", medium: "" };
const ERA_LABEL = { antiquity: "Antiquity", medieval: "Medieval", renaissance: "Renaissance", early_modern: "Early modern", modern: "Modern" };
const ERA_ORDER = { antiquity: 0, medieval: 1, renaissance: 2, early_modern: 3, modern: 4 };
const STAGE_COLOR = { nigredo: "#1c1a1a", "nigredo→albedo": "#5a5550", albedo: "#e9e4d8", citrinitas: "#d8b53f", rubedo: "#9c2b22" };
const CAP = s => (s || "").replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
const ESC = s => (s || "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

async function boot() {
  let cat, opd;
  try {
    [cat, opd] = await Promise.all([
      fetch("../data/catalog.json").then(r => r.json()),
      fetch("../data/operations.json").then(r => r.json()),
    ]);
  } catch (e) {
    document.getElementById("loading").textContent = "Could not load the archive — run scripts/build_operations.py";
    return;
  }
  OP.items = (cat.items || []);
  OP.byId = Object.fromEntries(OP.items.map(i => [i.id, i]));
  OP.works = Object.fromEntries((cat.works || []).map(w => [w.key, w]));
  OP.ops = opd.operations || [];
  OP.meta = opd;
  window.addEventListener("hashchange", route);
  route();
}

function route() {
  const p = new URLSearchParams(location.search);
  const hash = location.hash.replace(/^#/, "");
  const key = hash || p.get("op");
  const op = OP.ops.find(o => o.key === key);
  if (op) renderGate(op); else renderOverview();
  window.scrollTo(0, 0);
}

/* ---------- overview: the twelve gates ---------- */
function renderOverview() {
  const cards = OP.ops.map(o => {
    const cov = OP.byId[o.cover];
    const dot = `<span class="stage-dot" style="background:${STAGE_COLOR[o.stage] || "#888"}" title="${ESC(o.stage)}"></span>`;
    return `<a class="op-card" href="#${o.key}">
      <span class="op-cover">${cov ? `<img loading="lazy" src="${cov.thumb}" alt="${ESC(o.name)}">` : `<span class="cat-noimg">☿</span>`}
        <span class="op-num">${o.n}</span></span>
      <span class="op-meta">
        <b>${ESC(o.name)}</b><span class="op-latin">${ESC(o.latin)} ${dot}</span>
        <i class="op-tag">${ESC(o.tagline)}</i>
        <span class="op-count">${o.count} image${o.count === 1 ? "" : "s"} · ${o.n_sources} sources</span>
      </span></a>`;
  }).join("");
  document.getElementById("opmain").innerHTML = `
    <div class="op-head">
      <p class="op-kicker">A curated rabbit hole</p>
      <h1>${ESC(OP.meta.title || "The Twelve Processes")}</h1>
      <p class="op-intro">${ESC(OP.meta.intro || "")}</p>
    </div>
    <div class="op-grid">${cards}</div>
    <p class="op-foot-note">Each gate gathers whole illustrations <em>from across the archive</em> that depict the
      same operation — so you can set Splendor Solis beside the Rosarium, Maier, and a dozen other hands all
      picturing the one moment of the Work.</p>`;
}

/* ---------- one gate: cross-source images for a single operation ---------- */
function gateImages(op) {
  let imgs = op.image_ids.map(id => OP.byId[id]).filter(Boolean);
  if (OP.medium) imgs = imgs.filter(i => i.medium === OP.medium);
  if (OP.sort === "source") imgs = imgs.slice().sort((a, b) =>
    (a._work || a.work_key).localeCompare(b._work || b.work_key) || (a.seq || 0) - (b.seq || 0));
  else imgs = imgs.slice().sort((a, b) =>
    (ERA_ORDER[a.era] ?? 9) - (ERA_ORDER[b.era] ?? 9) || (a.date || "").localeCompare(b.date || ""));
  return imgs;
}

function renderGate(op) {
  const idx = OP.ops.findIndex(o => o.key === op.key);
  const prev = OP.ops[idx - 1], next = OP.ops[idx + 1];
  const imgs = gateImages(op);
  // medium filter options from the FULL (unfiltered) set
  const allMedia = {};
  op.image_ids.map(id => OP.byId[id]).filter(Boolean).forEach(i => { if (i.medium) allMedia[i.medium] = (allMedia[i.medium] || 0) + 1; });
  const mediaChips = Object.entries(allMedia).sort((a, b) => b[1] - a[1]).map(([m, n]) =>
    `<button class="mchip${OP.medium === m ? " on" : ""}" data-m="${m}">${CAP(m)} <span class="n">${n}</span></button>`).join("");

  let body;
  if (OP.group === "source") {
    const groups = bySource(imgs);
    body = groups.map(g => sourceCard(g)).join("");
  } else {
    body = imgs.map(cardEl).join("");
  }

  document.getElementById("opmain").innerHTML = `
    <div class="op-bar">
      <a class="op-back" href="#">← All twelve gates</a>
      <span class="op-step">Gate ${op.n} of 12</span>
    </div>
    <div class="gate-head">
      <div class="gate-num" style="--stage:${STAGE_COLOR[op.stage] || "#888"}">${op.n}</div>
      <div class="gate-words">
        <h1>${ESC(op.name)} <span class="gate-latin">${ESC(op.latin)}</span></h1>
        <p class="gate-tag">${ESC(op.tagline)}</p>
        <p class="gate-blurb">${ESC(op.blurb)}</p>
        <p class="gate-stage"><span class="stage-dot" style="background:${STAGE_COLOR[op.stage] || "#888"}"></span>
          stage: <b>${ESC(op.stage)}</b> &nbsp;·&nbsp; ${op.count} images from ${op.n_sources} sources</p>
      </div>
    </div>
    <div class="gate-controls">
      <div class="seg" id="grp">
        <button data-g="image"${OP.group === "image" ? ' class="on"' : ""}>Individual images</button>
        <button data-g="source"${OP.group === "source" ? ' class="on"' : ""}>By source work</button>
      </div>
      <select id="opsort">
        <option value="chrono"${OP.sort === "chrono" ? " selected" : ""}>Sort: chronological</option>
        <option value="source"${OP.sort === "source" ? " selected" : ""}>Sort: by source work</option>
      </select>
      <div class="mchips">${OP.medium ? `<button class="mchip on" data-m="">All media ✕</button>` : ""}${mediaChips}</div>
    </div>
    <div class="grid">${body || '<p class="empty">No images for this filter.</p>'}</div>
    <div class="gate-nav">
      ${prev ? `<a href="#${prev.key}">← ${prev.n}. ${ESC(prev.name)}</a>` : "<span></span>"}
      ${next ? `<a href="#${next.key}">${next.n}. ${ESC(next.name)} →</a>` : "<span></span>"}
    </div>`;

  document.getElementById("opsort").onchange = e => { OP.sort = e.target.value; renderGate(op); };
  document.querySelectorAll("#grp button").forEach(b => b.onclick = () => { OP.group = b.dataset.g; renderGate(op); });
  document.querySelectorAll(".mchip").forEach(b => b.onclick = () => { OP.medium = b.dataset.m; renderGate(op); });
}

function bySource(imgs) {
  const m = new Map();
  for (const it of imgs) { if (!m.has(it.work_key)) m.set(it.work_key, []); m.get(it.work_key).push(it); }
  return [...m.entries()].map(([wk, list]) => {
    const w = OP.works[wk] || {};
    return { work_key: wk, title: w.title || list[0]._work || wk, cover: list[0],
      count: list.length, creator: w.creator || list[0].creator, date: w.date || list[0].date, era: list[0].era };
  }).sort((a, b) => (ERA_ORDER[a.era] ?? 9) - (ERA_ORDER[b.era] ?? 9) || b.count - a.count);
}

function sourceCard(g) {
  return `<a class="card book-card" href="gallery.html?work=${encodeURIComponent(g.work_key)}">
    <span class="badge">${g.count} here</span><span class="book-spine">📖</span>
    <img decoding="async" src="${g.cover.thumb}" alt="${ESC(g.title)}">
    <div class="meta"><p class="t">${ESC(g.title)}</p>
    <p class="sub">${ESC(g.creator || "")}${g.date ? " · " + g.date : ""}</p></div></a>`;
}

function cardEl(it) {
  const work = (OP.works[it.work_key] || {}).title || it.work || "";
  return `<a class="card" href="item.html?id=${encodeURIComponent(it.id)}">
    <span class="badge">${ESC(work).slice(0, 26)}</span>
    <img decoding="async" loading="lazy" src="${it.thumb}" alt="${ESC(it.title)}">
    <div class="meta"><p class="t">${ESC(it.title)}</p>
    <p class="sub">${ESC(it.creator)} · ${ESC(it.date)}</p></div></a>`;
}

// attach work titles to items for sort/labels
fetch("../data/catalog.json").then(r => r.json()).then(c => {
  const wt = Object.fromEntries((c.works || []).map(w => [w.key, w.title]));
  OP.items.forEach(i => i._work = wt[i.work_key] || i.work);
});
boot();
