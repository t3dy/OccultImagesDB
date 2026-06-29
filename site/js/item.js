/* Occult Image DB — item detail */
const ERA_LABEL = { antiquity: "Antiquity", medieval: "Medieval", renaissance: "Renaissance", early_modern: "Early modern", modern: "Modern" };
const cap = s => (s || "").replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
const esc = s => (s || "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function inlineFmt(s) {
  let h = esc(s).replace(/\[PLACEHOLDER:([^\]]*)\]/g, '<span class="ph-inline">[needs:$1]</span>');
  return h.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>").replace(/\*([^*]+)\*/g, "<em>$1</em>");
}
function renderSummary(text) {
  // lightweight: ## heading (rest of block becomes a paragraph), blank-line paragraphs,
  // **bold**, *italic*, and [PLACEHOLDER: ...] highlighting.
  const blocks = (text || "").trim().split(/\n\s*\n/);
  return blocks.map(b => {
    b = b.trim();
    if (b.startsWith("## ")) {
      const nl = b.indexOf("\n");
      const head = nl === -1 ? b.slice(3) : b.slice(3, nl);
      const rest = nl === -1 ? "" : b.slice(nl + 1).trim();
      let out = `<h2>${esc(head.trim())}</h2>`;
      if (rest) out += `<p>${inlineFmt(rest).replace(/\n/g, "<br>")}</p>`;
      return out;
    }
    return `<p>${inlineFmt(b).replace(/\n/g, "<br>")}</p>`;
  }).join("");
}

function renderScholApparatus(it, items) {
  let html = "";
  if (Array.isArray(it.key_concepts) && it.key_concepts.length) {
    html += `<div class="schol-block"><h3>Key concepts</h3><div class="taglist">` +
      it.key_concepts.map(k => `<a href="gallery.html?q=${encodeURIComponent(k)}">${esc(k)}</a>`).join("") + `</div></div>`;
  }
  if (Array.isArray(it.related_emblems) && it.related_emblems.length) {
    const links = it.related_emblems.map(n => {
      const rid = `atalanta_fugiens__emblem-${String(n).padStart(2, "0")}`;
      const r = items.find(x => x.id === rid);
      return r ? `<a href="item.html?id=${rid}">${esc(r.title.replace(/^Atalanta Fugiens — /, ""))}</a>` : null;
    }).filter(Boolean);
    if (links.length) html += `<div class="schol-block"><h3>Related emblems</h3><div class="taglist">${links.join("")}</div></div>`;
  }
  if (Array.isArray(it.citations) && it.citations.length) {
    html += `<div class="schol-block"><h3>Sources &amp; further reading</h3><ul class="cites">` +
      it.citations.map(c => c.url
        ? `<li><a href="${esc(c.url)}" target="_blank" rel="noopener">${inlineFmt(c.text)} ↗</a></li>`
        : `<li>${inlineFmt(c.text)}</li>`).join("") + `</ul></div>`;
  }
  return html ? `<div class="schol-apparatus">${html}</div>` : "";
}

async function boot() {
  const id = new URLSearchParams(location.search).get("id");
  const data = await (await fetch("../data/catalog.json")).json();
  const items = data.items || [];
  const it = items.find(x => x.id === id);
  const root = document.getElementById("item");
  if (!it) { root.innerHTML = "<p>Image not found.</p>"; return; }
  document.title = `${it.title} — Occult Image DB`;
  const work = (data.works || []).find(w => w.key === it.work_key) || {};

  const isPh = it.summary_status === "placeholder";
  const phNote = isPh ? `<div class="placeholder-note"><strong>Scholarly summary needed.</strong>
     This image is catalogued with verified provenance, but its full iconographic essay has not yet been
     authored. Source material and a draft can be added in <code>data/overrides.json</code>.</div>` : "";

  // creator-entity key, if this work maps to a known creator profile
  const creatorKey = (data.creators_index || {})[it.work_key];
  const facts = [
    ["Source work", `<a href="entity.html?type=work&key=${encodeURIComponent(it.work_key)}">${esc(it.work)}</a>`],
    ["Creator", creatorKey ? `<a href="entity.html?type=creator&key=${creatorKey}">${esc(it.creator)}</a>` : esc(it.creator)],
    ["Date", esc(it.date)],
    ["Place", esc(it.place)],
    ["Era", `<a href="entity.html?type=era&key=${it.era}">${ERA_LABEL[it.era] || cap(it.era)}</a>`],
    ["Tradition", `<a href="entity.html?type=tradition&key=${it.tradition}">${cap(it.tradition)}</a>`],
    ["Medium", it.medium ? `<a href="gallery.html?medium=${encodeURIComponent(it.medium)}">${cap(it.medium)}</a>` : ""],
    ["Language", esc(it.language)],
    ["Repository", esc(it.repository)],
    ["Shelfmark", esc(it.shelfmark)],
    ["Rights", esc(it.rights)],
  ].filter(r => r[1] && !/^\[PLACEHOLDER/.test(r[1]));

  const tags = (it.motifs || []).map(m =>
    `<a href="gallery.html?motif=${encodeURIComponent(m)}">${cap(m)}</a>`).join("");
  const figures = (it.figures || []).map(f =>
    `<a href="gallery.html?figure=${encodeURIComponent(f)}">${esc(f)}</a>`).join("");

  const prov = it.provenance_url && !/PLACEHOLDER/.test(it.provenance_url)
    ? `<a class="btn" href="${esc(it.provenance_url)}" target="_blank" rel="noopener">View source ↗</a>` : "";

  root.innerHTML = `
  <div class="item-wrap">
    <div class="viewer">
      <img src="${it.card}" alt="${esc(it.title)}">
      <div class="actions">
        <a class="btn primary" href="${it.card}" download>↓ Download image</a>
        ${prov}
      </div>
    </div>
    <div class="item-body">
      <h1>${esc(it.title)}</h1>
      <p class="work-line">${esc(it.creator)} · <em>${esc(it.work)}</em>${it.date ? " · " + esc(it.date) : ""}</p>
      <div class="taglist">${tags}</div>
      ${figures ? `<p class="figures-line"><span class="figures-label">Depicted:</span> <span class="taglist inline">${figures}</span></p>` : ""}
      <table class="facts">${facts.map(r => `<tr><th>${r[0]}</th><td>${r[1]}</td></tr>`).join("")}</table>
      ${phNote}
      <div class="summary">${renderSummary(it.summary)}</div>
      ${renderScholApparatus(it, items)}
    </div>
  </div>
  <div class="related" id="related"></div>`;

  // related: same work, nearby
  const sib = items.filter(x => x.work_key === it.work_key && x.id !== it.id)
    .sort((a, b) => Math.abs((a.seq || 0) - (it.seq || 0)) - Math.abs((b.seq || 0) - (it.seq || 0)))
    .slice(0, 6);
  if (sib.length) {
    document.getElementById("related").innerHTML =
      `<h2>More from ${esc(it.work)}</h2><div class="strip">` +
      sib.map(s => `<a class="card" href="item.html?id=${encodeURIComponent(s.id)}">
        <img loading="lazy" src="${s.thumb}" alt="${esc(s.title)}">
        <div class="meta"><p class="t" style="font-size:14px">${esc(s.title)}</p></div></a>`).join("") +
      `</div>`;
  }
}
boot();
