/* Occult Image DB — gallery */
const state = {
  items: [], works: [], filtered: [],
  facets: { era: new Set(), tradition: new Set(), medium: new Set(), work: new Set(), figures: new Set(), motif: new Set() },
  q: "", sort: "chrono", showScans: false, rendered: 0, PAGE: 60,
};
const ERA_LABEL = { antiquity: "Antiquity", medieval: "Medieval", renaissance: "Renaissance", early_modern: "Early modern", modern: "Modern" };
const ERA_ORDER = { antiquity: 0, medieval: 1, renaissance: 2, early_modern: 3, modern: 4 };
const cap = s => (s || "").replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());

async function boot() {
  let data;
  try {
    data = await (await fetch("../data/catalog.json")).json();
  } catch (e) {
    document.getElementById("heroStats").textContent = "Catalog not built yet — run scripts/build_catalog.py";
    return;
  }
  state.items = data.items || [];
  state.works = data.works || [];
  const workTitle = Object.fromEntries(state.works.map(w => [w.key, w.title]));
  state.items.forEach(it => { it._work = workTitle[it.work_key] || it.work; });
  // deep links from item pages: ?work=key  ?motif=x  ?era=x  ?tradition=x  ?medium=x  ?figure=Name  ?q=text
  const p = new URLSearchParams(location.search);
  for (const f of ["work", "motif", "era", "tradition", "medium"]) {
    const v = p.get(f); if (v && state.facets[f]) state.facets[f].add(v);
  }
  if (p.get("figure")) state.facets.figures.add(p.get("figure"));
  if (p.get("q")) { state.q = p.get("q").toLowerCase(); }
  if (p.get("scan")) state.showScans = true;
  buildFacets();
  wire();
  apply();
  const illos = state.items.filter(i => i.tier === "illustration").length;
  document.getElementById("heroStats").textContent =
    `${state.items.length.toLocaleString()} catalogued images · ${state.works.length} source works · ${illos.toLocaleString()} curated illustrations`;
}

function facetCounts(facet, accessorList) {
  const m = new Map();
  for (const it of pool()) {
    const vals = accessorList(it);
    for (const v of vals) if (v) m.set(v, (m.get(v) || 0) + 1);
  }
  return m;
}
function pool() { return state.showScans ? state.items : state.items.filter(i => i.tier === "illustration"); }

function buildFacets() {
  renderChips("era", facetCounts("era", i => [i.era]), v => ERA_LABEL[v] || cap(v),
    (a, b) => (ERA_ORDER[a[0]] ?? 9) - (ERA_ORDER[b[0]] ?? 9));
  renderChips("tradition", facetCounts("tradition", i => [i.tradition]), cap, byCountDesc);
  renderChips("medium", facetCounts("medium", i => [i.medium]), cap, byCountDesc);
  renderChips("work", facetCounts("work", i => [i.work_key]),
    k => (state.works.find(w => w.key === k) || {}).title || k, byCountDesc);
  renderChips("figures", facetCounts("figures", i => i.figures || []), s => s, byCountDesc);
  renderChips("motif", facetCounts("motif", i => i.motifs || []), cap, byCountDesc);
}
const byCountDesc = (a, b) => b[1] - a[1];

function renderChips(facet, countMap, labelFn, sortFn) {
  const box = document.querySelector(`.chips[data-facet="${facet}"]`);
  const entries = [...countMap.entries()].sort(sortFn);
  box.innerHTML = "";
  for (const [val, n] of entries) {
    const el = document.createElement("button");
    el.className = "chip" + (state.facets[facet].has(val) ? " on" : "");
    el.innerHTML = `${labelFn(val)} <span class="n">${n}</span>`;
    el.onclick = () => {
      state.facets[facet].has(val) ? state.facets[facet].delete(val) : state.facets[facet].add(val);
      buildFacets(); apply();
    };
    box.appendChild(el);
  }
}

function wire() {
  const q = document.getElementById("q");
  q.value = state.q; document.getElementById("showScans").checked = state.showScans;
  q.oninput = () => { state.q = q.value.toLowerCase().trim(); apply(); };
  document.getElementById("sort").onchange = e => { state.sort = e.target.value; apply(); };
  document.getElementById("showScans").onchange = e => { state.showScans = e.target.checked; buildFacets(); apply(); };
  document.getElementById("clearFilters").onclick = clearAll;
  document.getElementById("resetEmpty").onclick = clearAll;
  const io = new IntersectionObserver(es => { if (es[0].isIntersecting) renderMore(); }, { rootMargin: "600px" });
  io.observe(document.getElementById("sentinel"));
}
function clearAll() {
  for (const k in state.facets) state.facets[k].clear();
  state.q = ""; document.getElementById("q").value = "";
  buildFacets(); apply();
}

function matches(it) {
  for (const facet of ["era", "tradition", "medium", "work", "figures", "motif"]) {
    const sel = state.facets[facet]; if (!sel.size) continue;
    if (facet === "work") { if (!sel.has(it.work_key)) return false; }
    else if (facet === "motif") { if (![...sel].every(m => (it.motifs || []).includes(m))) return false; }
    else if (facet === "figures") { if (![...sel].every(f => (it.figures || []).includes(f))) return false; }
    else if (!sel.has(it[facet])) return false;
  }
  if (state.q) {
    const hay = `${it.title} ${it._work} ${it.creator} ${it.tradition} ${(it.motifs || []).join(" ")} ${it.summary || ""}`.toLowerCase();
    if (!hay.includes(state.q)) return false;
  }
  return true;
}

function apply() {
  let r = pool().filter(matches);
  if (state.sort === "title") r.sort((a, b) => a.title.localeCompare(b.title));
  else if (state.sort === "work") r.sort((a, b) => a._work.localeCompare(b._work) || (a.seq || 0) - (b.seq || 0));
  else r.sort((a, b) => (ERA_ORDER[a.era] ?? 9) - (ERA_ORDER[b.era] ?? 9) || a._work.localeCompare(b._work) || (a.seq || 0) - (b.seq || 0));
  state.filtered = r;
  document.getElementById("count").innerHTML = `<b>${r.length.toLocaleString()}</b> image${r.length === 1 ? "" : "s"}`;
  const grid = document.getElementById("grid");
  grid.innerHTML = ""; state.rendered = 0;
  document.getElementById("empty").hidden = r.length > 0;
  renderMore();
}

function renderMore() {
  const grid = document.getElementById("grid");
  const next = state.filtered.slice(state.rendered, state.rendered + state.PAGE);
  const frag = document.createDocumentFragment();
  for (const it of next) frag.appendChild(cardEl(it));
  grid.appendChild(frag);
  state.rendered += next.length;
}

function cardEl(it) {
  const a = document.createElement("a");
  a.className = "card";
  a.href = `item.html?id=${encodeURIComponent(it.id)}`;
  const badge = `<span class="badge">${it.short_id} · ${ERA_LABEL[it.era] || cap(it.era)}</span>`;
  const ph = it.summary_status === "placeholder" ? `<span class="ph" title="scholarly summary needed">needs text</span>` : "";
  a.innerHTML = `${badge}${ph}
    <img decoding="async" src="${it.thumb}" alt="${it.title.replace(/"/g, "&quot;")}">
    <div class="meta"><p class="t">${it.title}</p>
    <p class="sub">${it.creator} · ${it.date}</p></div>`;
  return a;
}

boot();
