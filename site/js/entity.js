/* Occult Image DB — entity profile (creator / work / tradition / motif / era / topic / region / collection) */
/* relies on common.js (ESC, CAP, ERA_LABEL, REGIONS, regionKeyOf, imageMatches, renderMasonry) */
const esc = ESC, cap = CAP;

// catalog motif strings that count as a given motif-entity
const MOTIF_MATCH = {
  "ouroboros": ["ouroboros"],
  "green-lion": ["green lion", "lion"],
  "coniunctio": ["coniunctio", "king and queen", "king", "queen", "marriage", "union", "two figures"],
  "rebis": ["hermaphrodite", "rebis", "androgyne"],
  "furnace": ["furnace", "vessel", "alembic", "apparatus", "still", "laboratory"],
  "dragon": ["dragon", "serpent"],
};

let DB = { entities: null, items: [], works: [], topics: [], collections: [], eraCats: [] };

// parse a category key "<era>__<catkey>" → {era, cat object} from era_categories.json
function findCategory(key) {
  const i = (key || "").indexOf("__");
  if (i < 0) return null;
  const era = key.slice(0, i), ck = key.slice(i + 2);
  const eb = DB.eraCats.find(e => e.era === era);
  const cat = eb && eb.categories.find(c => c.key === ck);
  return cat ? { era, cat, siblings: eb.categories } : null;
}
function catMatches(it, m) {
  return (m.media && m.media.includes(it.medium)) ||
    (m.traditions && m.traditions.includes(it.tradition)) ||
    (m.work_keys && m.work_keys.includes(it.work_key)) ||
    (m.motif_terms && (it.motifs || []).some(x => m.motif_terms.map(t => t.toLowerCase()).includes(x.toLowerCase())));
}

function linkFor(type, key, label) {
  return `<a href="entity.html?type=${type}&key=${encodeURIComponent(key)}">${esc(label)}</a>`;
}
// resolve [[type:key]] wiki-links + inline formatting in one string
function inlineResolve(text) {
  const ent = DB.entities;
  return esc(text).replace(/\[\[(creator|work|tradition|motif|era):([a-z0-9_\-]+)\]\]/g, (m, type, key) => {
    let label = key.replace(/[-_]/g, " ");
    if (type === "work") { const w = DB.works.find(w => w.key === key); if (w) label = w.title; return linkFor("work", key, label); }
    if (type === "creator") { const c = (ent.creators || []).find(c => c.key === key); if (c) label = c.name; return linkFor("creator", key, label); }
    if (type === "tradition") { const t = (ent.traditions || []).find(t => t.key === key); if (t) label = t.name; return linkFor("tradition", key, label); }
    if (type === "motif") { const o = (ent.motifs || []).find(o => o.key === key); if (o) label = o.name; return linkFor("motif", key, cap(label)); }
    if (type === "era") return linkFor("era", key, ERA_LABEL[key] || cap(key));
    return cap(label);
  }).replace(/\[PLACEHOLDER:([^\]]*)\]/g, '<span class="ph-inline">[needs:$1]</span>')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}
// block-aware: ## heading lines become <h2>, blank-line-separated blocks become <p>
function resolveLinks(text) {
  return (text || "").trim().split(/\n\s*\n/).map(b => {
    b = b.trim();
    if (b.startsWith("## ")) {
      const nl = b.indexOf("\n");
      const head = nl === -1 ? b.slice(3) : b.slice(3, nl);
      const rest = nl === -1 ? "" : b.slice(nl + 1).trim();
      return `<h2>${inlineResolve(head)}</h2>` + (rest ? `<p>${inlineResolve(rest).replace(/\n/g, "<br>")}</p>` : "");
    }
    return `<p>${inlineResolve(b).replace(/\n/g, "<br>")}</p>`;
  }).join("");
}

function itemsFor(type, key) {
  const it = DB.items;
  if (type === "work") return it.filter(x => x.work_key === key);
  if (type === "tradition") return it.filter(x => x.tradition === key);
  if (type === "era") return it.filter(x => x.era === key);
  if (type === "creator") {
    const c = (DB.entities.creators || []).find(c => c.key === key);
    const wk = c ? c.works : [];
    return it.filter(x => wk.includes(x.work_key));
  }
  if (type === "motif") {
    const o = (DB.entities.motifs || []).find(o => o.key === key);
    const match = ((o && o.match) || MOTIF_MATCH[key] || [key, (o ? o.name.toLowerCase() : key)]).map(s => s.toLowerCase());
    return it.filter(x => (x.motifs || []).some(m => match.includes(m.toLowerCase())));
  }
  if (type === "region") return it.filter(x => regionKeyOf(x) === key);
  if (type === "topic") { const t = DB.topics.find(t => t.key === key); return t ? it.filter(x => imageMatches(x, t.match)) : []; }
  if (type === "collection") { const c = DB.collections.find(c => c.key === key); return c ? it.filter(x => imageMatches(x, c.match)) : []; }
  if (type === "category") {
    const f = findCategory(key); if (!f) return [];
    return it.filter(x => x.era === f.era && catMatches(x, f.cat.match));
  }
  return [];
}

function cardEl(it) {
  return `<a class="card" href="item.html?id=${encodeURIComponent(it.id)}">
    <span class="badge">${it.short_id}</span>
    <img decoding="async" src="${it.thumb}" alt="${esc(it.title)}">
    <div class="meta"><p class="t" style="font-size:15px">${esc(it.title)}</p>
    <p class="sub">${esc(it.creator)} · ${esc(it.date)}</p></div></a>`;
}

function header(type, key) {
  const ent = DB.entities;
  if (type === "creator") {
    const c = (ent.creators || []).find(c => c.key === key);
    if (!c) return null;
    const works = (c.works || []).map(wk => { const w = DB.works.find(w => w.key === wk); return w ? linkFor("work", wk, w.title) : null; }).filter(Boolean);
    return { kicker: c.role || "Figure", title: c.name, sub: c.dates || "",
      summary: c.summary, links: c.links,
      related: works.length ? `<div class="rel-block"><h3>Works</h3>${works.join(" · ")}</div>` : "" };
  }
  if (type === "tradition") {
    const t = (ent.traditions || []).find(t => t.key === key);
    if (!t) return null;
    const creators = (ent.creators || []).filter(c => (c.works || []).some(wk => { const w = DB.works.find(w => w.key === wk); return w && w.tradition === key; }));
    const rel = creators.length ? `<div class="rel-block"><h3>Figures</h3>${creators.map(c => linkFor("creator", c.key, c.name)).join(" · ")}</div>` : "";
    return { kicker: "Tradition", title: t.name, sub: t.blurb, summary: t.summary, links: t.links, related: rel };
  }
  if (type === "motif") {
    const o = (ent.motifs || []).find(o => o.key === key);
    if (!o) return null;
    const see = (o.see_also || []).map(s => { const m = (ent.motifs || []).find(m => m.key === s); return m ? linkFor("motif", s, m.name) : cap(s); });
    const rel = see.length ? `<div class="rel-block"><h3>See also</h3>${see.join(" · ")}</div>` : "";
    return { kicker: "Motif", title: o.name, sub: o.blurb, summary: o.summary, links: o.links, related: rel };
  }
  if (type === "work") {
    const w = DB.works.find(w => w.key === key);
    if (!w) return null;
    const c = (ent.creators || []).find(c => (c.works || []).includes(key));
    const rel = `<div class="rel-block"><h3>Relations</h3>
      ${c ? "Creator: " + linkFor("creator", c.key, c.name) + " · " : ""}
      Tradition: ${linkFor("tradition", w.tradition, cap(w.tradition))} ·
      Era: ${linkFor("era", w.era, ERA_LABEL[w.era] || cap(w.era))}</div>`;
    const links = w.provenance_url && !w.provenance_url.includes("PLACEHOLDER") ? [{ label: "Source / digitisation", url: w.provenance_url }] : [];
    return { kicker: "Source work", title: w.title, sub: `${w.creator} · ${w.date} · ${w.place}`, summary: w.blurb + "\n\n*" + w.rights + "*", links, related: rel };
  }
  if (type === "era") {
    return { kicker: "Era", title: ERA_LABEL[key] || cap(key), sub: "", summary: ERA_BLURB[key] || "", links: [], related: "" };
  }
  if (type === "region") {
    const r = REGIONS.find(r => r.key === key); if (!r) return null;
    return { kicker: "Region", title: r.name, sub: "", summary: "Images made in this region of the esoteric world.", links: [], related: "" };
  }
  if (type === "category") {
    const f = findCategory(key); if (!f) return null;
    const sibs = f.siblings.filter(c => c.key !== f.cat.key)
      .map(c => linkFor("category", f.era + "__" + c.key, c.label)).join(" · ");
    const rel = `<div class="rel-block"><h3>More in ${ERA_LABEL[f.era] || cap(f.era)}</h3>${sibs}</div>`;
    return { kicker: `${ERA_LABEL[f.era] || cap(f.era)} · Gallery`, title: f.cat.label, sub: f.cat.blurb,
      summary: "", links: [], related: rel };
  }
  if (type === "topic") {
    const t = DB.topics.find(t => t.key === key); if (!t) return null;
    let rel = "";
    if (t.subthemes && t.subthemes.length) rel += `<div class="rel-block"><h3>Sub-themes</h3>${t.subthemes.map(cap).join(" · ")}</div>`;
    const figs = (t.figures || []).map(fk => { const c = (ent.creators || []).find(c => c.key === fk); return c ? linkFor("creator", fk, c.name) : null; }).filter(Boolean);
    if (figs.length) rel += `<div class="rel-block"><h3>Figures</h3>${figs.join(" · ")}</div>`;
    let summary = t.summary;
    if (t.status === "coming_soon") summary += "\n\n[PLACEHOLDER: " + (t.needs || "images for this topic are still being sourced — see SOURCINGIMAGES.md") + "]";
    return { kicker: t.status === "coming_soon" ? "Topic · coming soon" : "Topic", title: t.name, sub: t.blurb, summary, links: t.links, related: rel };
  }
  if (type === "collection") {
    const c = DB.collections.find(c => c.key === key); if (!c) return null;
    const figs = (c.figures || []).map(fk => { const cr = (ent.creators || []).find(x => x.key === fk); return cr ? linkFor("creator", fk, cr.name) : null; }).filter(Boolean);
    const rel = figs.length ? `<div class="rel-block"><h3>Figures</h3>${figs.join(" · ")}</div>` : "";
    let summary = c.framing;
    if (c.status === "coming_soon") summary += "\n\n[PLACEHOLDER: " + (c.needs || "this curated collection is on the roadmap; images to be sourced") + "]";
    return { kicker: c.status === "coming_soon" ? "Curated collection · coming soon" : "Curated collection", title: c.title, sub: "", summary, links: [], related: rel };
  }
  return null;
}
const ERA_BLURB = {
  antiquity: "Late-antique and Hellenistic origins of the tradition — the first ouroboros, the apparatus of Zosimos and Kleopatra. [PLACEHOLDER: images not yet sourced — see SOURCINGIMAGES.md].",
  medieval: "The Latin-medieval alchemical manuscripts — the earliest stratum of the printed-image tradition's ancestry (Aurora Consurgens, the pseudo-Lullian corpus).",
  renaissance: "The 15th–16th-century flowering: the rediscovery of Hermes, the great illuminated manuscripts and the first printed emblem sequences.",
  early_modern: "The 17th-century Baroque of alchemy — Maier, Mylius, Stolcius, Fludd — when the engraved emblem reached its height.",
  modern: "Victorian and modern occult-revival imagery. [PLACEHOLDER: not yet in corpus]."
};

async function boot() {
  const p = new URLSearchParams(location.search);
  const type = p.get("type"), key = p.get("key");
  const [entities, catalog, topics, collections, eraCats] = await Promise.all([
    fetch("../data/entities.json").then(r => r.json()),
    fetch("../data/catalog.json").then(r => r.json()),
    fetch("../data/topics.json").then(r => r.json()).catch(() => ({ topics: [] })),
    fetch("../data/collections.json").then(r => r.json()).catch(() => ({ collections: [] })),
    fetch("../data/era_categories.json").then(r => r.json()).catch(() => ({ eras: [] })),
  ]);
  DB.entities = entities; DB.items = (catalog.items || []).filter(i => i.tier !== "page_scan"); DB.works = catalog.works || [];
  DB.topics = topics.topics || []; DB.collections = collections.collections || []; DB.eraCats = eraCats.eras || [];
  const h = header(type, key);
  const root = document.getElementById("entity");
  if (!h) { root.innerHTML = "<p>Unknown theme. <a href='browse.html'>See all themes →</a></p>"; return; }
  document.title = `${h.title} — Occult Image DB`;
  const imgs = itemsFor(type, key);
  const linksHtml = (h.links || []).length
    ? `<div class="learn-more"><h3>Learn more</h3><ul>${h.links.map(l => `<li><a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)} ↗</a></li>`).join("")}</ul></div>` : "";
  root.innerHTML = `
    <div class="entity-head">
      <p class="kicker">${esc(h.kicker)}</p>
      <h1>${esc(h.title)}</h1>
      ${h.sub ? `<p class="entity-sub">${esc(h.sub)}</p>` : ""}
      <div class="entity-summary">${resolveLinks(h.summary)}</div>
      <div class="entity-rels">${h.related}${linksHtml}</div>
    </div>
    <div class="entity-images">
      <h2>${imgs.length} image${imgs.length === 1 ? "" : "s"} in the archive
        ${galleryLink(type, key, imgs.length)}</h2>
      <div class="masonry" id="entimgs"></div>
    </div>`;
  renderMasonry(document.getElementById("entimgs"), imgs.slice(0, 120));
}
function galleryLink(type, key, n) {
  if (!n) return "";
  const facet = { work: "work", tradition: "tradition", era: "era" }[type];
  if (facet) return `<a class="seeall" href="gallery.html?${facet}=${encodeURIComponent(key)}">open in faceted gallery →</a>`;
  if (type === "motif") return `<a class="seeall" href="gallery.html?motif=${encodeURIComponent((MOTIF_MATCH[key] || [key])[0])}">open in gallery →</a>`;
  if (type === "category") {
    const f = findCategory(key); if (!f) return "";
    const m = f.cat.match;
    const p = m.media ? `medium=${encodeURIComponent(m.media[0])}` : m.traditions ? `tradition=${encodeURIComponent(m.traditions[0])}`
      : m.work_keys ? `work=${encodeURIComponent(m.work_keys[0])}` : "";
    return p ? `<a class="seeall" href="gallery.html?era=${f.era}&${p}">open in faceted gallery →</a>` : "";
  }
  return "";
}
boot();
