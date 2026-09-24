"""
Genera revision-productos.html: herramienta de trabajo para revisar las fichas antes de llevarlas
al sitio. No forma parte de la web. Los datos van incrustados en el propio archivo, así que se abre
haciendo doble clic (sin servidor).

Maquetación de la ficha, según lo acordado:
    arriba izquierda -> tabla resumen        arriba derecha -> fotos
    abajo izquierda  -> PDF para descargar

Uso:  python generar_revision.py
"""
import os, json

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'productos.json')
SALIDA = os.path.join(RAIZ, 'revision-productos.html')

CAT_LABELS = {'industrial': 'Industrial', 'interior': 'Interior', 'exterior': 'Exterior',
              'emergencias': 'Emergencias', 'decorativas': 'Decorativas', 'bombillas': 'Bombillas y Accesorios'}

PLANTILLA = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Revisión de fichas técnicas — Apheloria</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;1,400&family=Inter:wght@200;300;400&family=Raleway:ital,wght@0,300;0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
  :root{
    --ink:#1a1612; --ink-rgb:26,22,18; --bg:#FFFFFF;
    --beige:#F2EDE4; --accent:#b0a898; --accent-rgb:176,168,152;
    --accent-soft:#c8bfb0; --accent-text:#857a68; --heading:#6d5f52;
    --placeholder-bg:#e8e0d0; --warn:#a34a3f; --ok:#4a7a5c;
    --ease:cubic-bezier(0.16,1,0.3,1);
  }
  body{background:var(--beige);color:var(--ink);font-family:'Inter',sans-serif;min-height:100vh;}
  header.rv-header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,0.94);
    backdrop-filter:blur(14px);border-bottom:1px solid rgba(var(--ink-rgb),0.08);padding:1.3rem 2.2rem 1rem;}
  .rv-title{font-family:'Cormorant Garamond',serif;font-weight:300;font-size:1.9rem;letter-spacing:0.03em;}
  .rv-title em{font-style:italic;color:var(--accent-text);}
  .rv-sub{font-family:'Raleway',sans-serif;font-size:0.7rem;letter-spacing:0.14em;text-transform:uppercase;
    color:var(--accent-text);margin-top:0.35rem;}
  .rv-controls{display:flex;gap:0.8rem;align-items:center;flex-wrap:wrap;margin-top:1rem;}
  .rv-filters{display:flex;gap:0.35rem;flex-wrap:wrap;}
  .rv-filter-btn{font-family:'Raleway',sans-serif;font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;
    padding:0.5rem 1rem;border-radius:999px;border:1px solid rgba(var(--ink-rgb),0.12);background:#fff;
    color:var(--heading);cursor:pointer;transition:all 0.25s var(--ease);}
  .rv-filter-btn.active{background:var(--ink);color:#fff;border-color:var(--ink);}
  .rv-search{font-family:'Inter',sans-serif;font-size:0.8rem;font-weight:300;padding:0.55rem 1rem;
    border-radius:999px;border:1px solid rgba(var(--ink-rgb),0.14);background:#fff;color:var(--ink);
    outline:none;min-width:230px;margin-left:auto;}
  .rv-count{font-family:'Raleway',sans-serif;font-size:0.7rem;color:var(--accent-text);white-space:nowrap;}
  main.rv-main{padding:1.8rem 2.2rem 4rem;max-width:1800px;margin:0 auto;}
  .rv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1.4rem;}
  .rv-card{background:#fff;cursor:pointer;display:flex;flex-direction:column;position:relative;overflow:hidden;
    transition:transform 0.35s var(--ease),box-shadow 0.35s var(--ease);}
  .rv-card:hover{transform:translateY(-5px);box-shadow:0 20px 40px rgba(var(--ink-rgb),0.14);}
  .rv-card-img-wrap{aspect-ratio:1/1;background:var(--placeholder-bg);overflow:hidden;position:relative;}
  .rv-card-img-wrap img{width:100%;height:100%;object-fit:contain;transition:transform 0.5s;}
  .rv-card:hover .rv-card-img-wrap img{transform:scale(1.04);}
  .rv-badge{position:absolute;top:0.6rem;right:0.6rem;font-family:'Raleway',sans-serif;font-size:0.6rem;
    letter-spacing:0.06em;text-transform:uppercase;font-weight:600;padding:0.3rem 0.55rem;border-radius:999px;
    background:rgba(255,255,255,0.92);color:var(--accent-text);}
  .rv-badge.is-warn{color:#fff;background:var(--warn);}
  .rv-badge.is-caution{color:#fff;background:#b8925a;}
  .rv-refs-badge{position:absolute;top:0.6rem;left:0.6rem;font-family:'Raleway',sans-serif;font-size:0.6rem;
    letter-spacing:0.06em;text-transform:uppercase;font-weight:600;padding:0.3rem 0.55rem;border-radius:999px;
    background:rgba(var(--ink-rgb),0.82);color:#fff;}
  .rv-pend{position:absolute;bottom:0.6rem;left:0.6rem;font-family:'Raleway',sans-serif;font-size:0.58rem;
    letter-spacing:0.08em;text-transform:uppercase;padding:0.25rem 0.5rem;border-radius:999px;
    background:rgba(163,74,63,0.9);color:#fff;}
  .rv-card-body{padding:0.9rem 1rem 1.1rem;display:flex;flex-direction:column;gap:0.3rem;flex:1;}
  .rv-card-eyebrow{font-family:'Raleway',sans-serif;font-size:0.6rem;letter-spacing:0.16em;
    text-transform:uppercase;color:var(--accent-text);}
  .rv-card-name{font-family:'Raleway',sans-serif;font-size:0.9rem;font-weight:600;color:var(--ink);line-height:1.25;}
  .rv-card-meta{font-family:'Inter',sans-serif;font-size:0.66rem;color:var(--accent-text);margin-top:auto;padding-top:0.5rem;}

  /* ── ficha ── */
  .rv-overlay{position:fixed;inset:0;background:var(--bg);z-index:200;display:none;overflow-y:auto;}
  .rv-overlay.visible{display:block;animation:rvIn 0.4s var(--ease);}
  @keyframes rvIn{from{opacity:0;transform:scale(0.98);}to{opacity:1;transform:scale(1);}}
  .rv-back{display:flex;align-items:center;gap:0.6rem;font-family:'Raleway',sans-serif;font-size:0.7rem;
    letter-spacing:0.18em;text-transform:uppercase;color:var(--accent-text);background:rgba(255,255,255,0.96);
    backdrop-filter:blur(8px);border:none;border-bottom:1px solid rgba(var(--ink-rgb),0.07);
    padding:1rem 2.5rem;cursor:pointer;position:sticky;top:0;z-index:5;width:100%;text-align:left;}
  .rv-back:hover{color:var(--ink);}
  .pd-hero{max-width:1800px;margin:0 auto;padding:2.2rem 2.5rem 0;}
  .pd-eyebrow{display:block;font-family:'Raleway',sans-serif;font-size:0.62rem;letter-spacing:0.38em;
    text-transform:uppercase;color:var(--accent-text);font-weight:400;margin-bottom:0.5rem;}
  .pd-title{font-family:'Raleway',sans-serif;font-size:clamp(1.3rem,2vw,2.1rem);font-weight:800;
    color:var(--heading);letter-spacing:-0.005em;line-height:1.15;}
  .pd-refs{font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:300;color:var(--accent-text);
    letter-spacing:0.04em;margin-top:0.5rem;}

  /* tabla arriba izq · fotos arriba dcha · descargas abajo izq */
  .pd-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,42%);
    grid-template-areas:"tabla fotos" "descargas fotos";gap:2.4rem 3rem;align-items:start;
    max-width:1800px;margin:0 auto;padding:1.8rem 2.5rem 3.5rem;}
  .pd-tabla{grid-area:tabla;}
  .pd-fotos{grid-area:fotos;position:sticky;top:1.5rem;display:flex;flex-direction:column;gap:0.9rem;}
  .pd-descargas{grid-area:descargas;}
  .pd-label{font-family:'Raleway',sans-serif;font-size:0.66rem;letter-spacing:0.32em;text-transform:uppercase;
    color:var(--accent-text);font-weight:400;display:block;margin-bottom:0.9rem;}
  table.pd-specs{width:100%;border-collapse:collapse;}
  table.pd-specs tr{border-bottom:1px solid rgba(var(--ink-rgb),0.09);}
  table.pd-specs td{padding:0.75rem 0;vertical-align:top;}
  table.pd-specs td:first-child{font-family:'Raleway',sans-serif;font-size:0.66rem;font-weight:400;
    letter-spacing:0.06em;text-transform:uppercase;color:var(--accent-text);width:44%;padding-right:1rem;}
  table.pd-specs td:last-child{font-family:'Raleway',sans-serif;font-size:0.88rem;font-weight:300;color:var(--ink);}
  table.pd-specs td .multi{color:var(--ink);}
  table.pd-specs td .sep{color:var(--accent-soft);padding:0 0.35rem;}
  .pd-main-wrap{aspect-ratio:1/1;background:var(--placeholder-bg);overflow:hidden;width:min(100%,56vh);margin:0 auto;}
  .pd-main-wrap img{width:100%;height:100%;object-fit:contain;}
  .pd-thumbs{display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center;}
  .pd-thumb{width:64px;height:64px;flex-shrink:0;padding:0;background:var(--placeholder-bg);cursor:pointer;
    border:1px solid rgba(var(--ink-rgb),0.1);opacity:0.62;transition:opacity 0.25s,border-color 0.25s;}
  .pd-thumb img{width:100%;height:100%;object-fit:contain;display:block;}
  .pd-thumb:hover{opacity:0.9;}
  .pd-thumb.active{opacity:1;border-color:var(--accent);}
  .pd-dl{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:0.7rem 0;
    border-bottom:1px solid rgba(var(--ink-rgb),0.08);text-decoration:none;color:inherit;
    transition:padding-left 0.25s var(--ease);}
  .pd-dl:hover{padding-left:0.5rem;}
  .pd-dl-info{display:flex;flex-direction:column;gap:0.15rem;min-width:0;}
  .pd-dl-titulo{font-family:'Raleway',sans-serif;font-size:0.84rem;font-weight:600;color:var(--ink);}
  .pd-dl:hover .pd-dl-titulo{color:var(--accent-text);}
  .pd-dl-ref{font-family:'Inter',sans-serif;font-size:0.66rem;font-weight:300;color:var(--accent-text);}
  .pd-dl-icono{font-family:'Raleway',sans-serif;font-size:0.6rem;letter-spacing:0.16em;text-transform:uppercase;
    color:var(--accent-text);white-space:nowrap;}
  .pd-aviso{font-family:'Raleway',sans-serif;font-size:0.76rem;font-weight:300;color:var(--accent-text);
    line-height:1.7;border-left:2px solid var(--accent-soft);padding-left:1rem;margin-bottom:1.4rem;}
  @media (max-width:900px){
    .rv-header{padding:1.2rem 1.3rem 1rem;} main.rv-main{padding:1.4rem 1.3rem 3rem;}
    .rv-search{min-width:0;width:100%;margin-left:0;}
    .pd-hero{padding:1.8rem 1.5rem 0;}
    .pd-grid{grid-template-columns:1fr;grid-template-areas:"fotos" "tabla" "descargas";gap:1.8rem;
      padding:1.6rem 1.5rem 2.5rem;}
    .pd-fotos{position:static;}
    .pd-main-wrap{aspect-ratio:4/3;width:min(100%,44vh);}
  }
</style>
</head>
<body>

<header class="rv-header">
  <div class="rv-title">Revisión de fichas <em>técnicas</em></div>
  <div class="rv-sub">Apheloria · tabla sacada de los PDF · vista de trabajo, no forma parte del sitio</div>
  <div class="rv-controls">
    <div class="rv-filters" id="rvFilters"></div>
    <span class="rv-count" id="rvCount"></span>
    <input class="rv-search" id="rvSearch" type="text" placeholder="Buscar por nombre o ref…">
  </div>
</header>

<main class="rv-main"><div class="rv-grid" id="rvGrid"></div></main>

<div class="rv-overlay" id="rvOverlay">
  <button type="button" class="rv-back" id="rvBack">← Volver al listado</button>
  <div class="pd-hero">
    <span class="pd-eyebrow" id="pdEyebrow"></span>
    <h2 class="pd-title" id="pdTitle"></h2>
    <div class="pd-refs" id="pdRefs"></div>
  </div>
  <div class="pd-grid">
    <div class="pd-tabla">
      <div id="pdAviso"></div>
      <span class="pd-label">Características técnicas</span>
      <table class="pd-specs"><tbody id="pdSpecs"></tbody></table>
    </div>
    <div class="pd-fotos">
      <div class="pd-main-wrap"><img id="pdMainImg" src="" alt=""></div>
      <div class="pd-thumbs" id="pdThumbs"></div>
    </div>
    <div class="pd-descargas">
      <span class="pd-label" id="pdDescargasLabel">Fichas técnicas en PDF</span>
      <div id="pdDescargas"></div>
    </div>
  </div>
</div>

<script>
const FICHAS = __DATOS__;
const CAT = __CATS__;

const el = (t, c, txt) => { const n = document.createElement(t); if (c) n.className = c; if (txt != null) n.textContent = txt; return n; };
const rutaPdf = p => p.split('/').map(encodeURIComponent).join('/');

function pintarGrid(cat, term){
  const grid = document.getElementById('rvGrid');
  grid.innerHTML = '';
  term = (term || '').trim().toLowerCase();
  let n = 0;
  FICHAS.forEach((f, i) => {
    if (cat !== 'all' && f.categoria !== cat) return;
    if (term && !(f.nombre.toLowerCase().includes(term) || f.refs.join(' ').toLowerCase().includes(term))) return;
    n++;
    const nf = f.imagenes.length;
    const card = el('div', 'rv-card');
    card.innerHTML = `
      <div class="rv-card-img-wrap">
        ${f.imagenes[0] ? `<img src="${f.imagenes[0]}" alt="">` : ''}
        <span class="rv-badge ${nf === 0 ? 'is-warn' : nf === 1 ? 'is-caution' : ''}">${nf} foto${nf === 1 ? '' : 's'}</span>
        ${f.refs.length > 1 ? `<span class="rv-refs-badge">${f.refs.length} códigos</span>` : ''}
        ${f.generada ? '' : '<span class="rv-pend">tabla antigua</span>'}
      </div>
      <div class="rv-card-body">
        <span class="rv-card-eyebrow">${CAT[f.categoria] || f.categoria} · ${f.familia}</span>
        <span class="rv-card-name">${f.nombre}</span>
        <span class="rv-card-meta">${f.specs.length} filas · ${f.descargas.length} PDF</span>
      </div>`;
    card.addEventListener('click', () => abrir(i));
    grid.appendChild(card);
  });
  document.getElementById('rvCount').textContent = n + ' de ' + FICHAS.length + ' fichas';
}

function abrir(i){
  const f = FICHAS[i];
  document.getElementById('pdEyebrow').textContent = (CAT[f.categoria] || f.categoria) + ' · ' + f.familia;
  document.getElementById('pdTitle').textContent = f.nombre;
  document.getElementById('pdRefs').textContent = f.refs.length === 1
    ? 'Ref. ' + f.refs[0]
    : f.refs.length + ' referencias' + (f.refs.length <= 4 ? ': ' + f.refs.join(', ') : ' (abajo, una por PDF)');

  const aviso = document.getElementById('pdAviso');
  aviso.innerHTML = '';
  if (!f.generada) aviso.appendChild(el('p', 'pd-aviso',
    'Esta categoría todavía no se ha rehecho: la tabla es la antigua (sacada de la descripción del Excel), no la del PDF.'));

  const tb = document.getElementById('pdSpecs');
  tb.innerHTML = '';
  f.specs.forEach(s => {
    const tr = el('tr');
    tr.appendChild(el('td', null, s.etiqueta));
    const td = el('td');
    s.valor.split(' | ').forEach((v, k) => {
      if (k) td.appendChild(el('span', 'sep', '|'));
      td.appendChild(el('span', 'multi', v));
    });
    tr.appendChild(td);
    tb.appendChild(tr);
  });

  const main = document.getElementById('pdMainImg');
  main.src = f.imagenes[0] || ''; main.alt = f.nombre;
  const th = document.getElementById('pdThumbs');
  th.innerHTML = '';
  f.imagenes.forEach((src, k) => {
    const b = el('button', 'pd-thumb' + (k === 0 ? ' active' : ''));
    b.type = 'button';
    b.innerHTML = `<img src="${src}" alt="">`;
    b.addEventListener('click', () => {
      main.src = src;
      th.querySelectorAll('.pd-thumb').forEach(t => t.classList.remove('active'));
      b.classList.add('active');
    });
    th.appendChild(b);
  });

  document.getElementById('pdDescargasLabel').textContent =
    f.descargas.length === 1 ? 'Ficha técnica en PDF' : `Fichas técnicas en PDF (${f.descargas.length})`;
  const dl = document.getElementById('pdDescargas');
  dl.innerHTML = '';
  f.descargas.forEach(d => {
    const a = el('a', 'pd-dl');
    a.href = rutaPdf(d.pdf); a.target = '_blank'; a.rel = 'noopener';
    const info = el('div', 'pd-dl-info');
    info.appendChild(el('span', 'pd-dl-titulo', d.titulo));
    info.appendChild(el('span', 'pd-dl-ref', 'Ref. ' + d.ref));
    a.appendChild(info);
    a.appendChild(el('span', 'pd-dl-icono', 'PDF ↓'));
    dl.appendChild(a);
  });

  const ov = document.getElementById('rvOverlay');
  ov.classList.add('visible'); ov.scrollTop = 0;
  document.body.style.overflow = 'hidden';
}

function cerrar(){
  document.getElementById('rvOverlay').classList.remove('visible');
  document.body.style.overflow = '';
}
document.getElementById('rvBack').addEventListener('click', cerrar);
document.addEventListener('keydown', e => { if (e.key === 'Escape') cerrar(); });

const cats = ['all', ...new Set(FICHAS.map(f => f.categoria))];
const wrap = document.getElementById('rvFilters');
let actual = 'all';
cats.forEach(c => {
  const b = el('button', 'rv-filter-btn' + (c === 'all' ? ' active' : ''), c === 'all' ? 'Todas' : (CAT[c] || c));
  b.addEventListener('click', () => {
    actual = c;
    wrap.querySelectorAll('.rv-filter-btn').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    pintarGrid(actual, document.getElementById('rvSearch').value);
  });
  wrap.appendChild(b);
});
document.getElementById('rvSearch').addEventListener('input', e => pintarGrid(actual, e.target.value));
pintarGrid('all', '');
</script>
</body>
</html>
'''

if __name__ == '__main__':
    fichas = json.load(open(DATOS, encoding='utf-8'))
    html = (PLANTILLA.replace('__DATOS__', json.dumps(fichas, ensure_ascii=False))
                     .replace('__CATS__', json.dumps(CAT_LABELS, ensure_ascii=False)))
    open(SALIDA, 'w', encoding='utf-8').write(html)
    print(f"{SALIDA}: {len(fichas)} fichas, {len(html)/1024:.0f} KB")
