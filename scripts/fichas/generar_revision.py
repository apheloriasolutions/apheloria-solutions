"""
Genera revision-productos.html: herramienta de trabajo para revisar las fichas antes de llevarlas
al sitio. No forma parte de la web. Los datos van incrustados en el propio archivo, así que se abre
haciendo doble clic (sin servidor).

Navegación en tres niveles, como la sección Productos del sitio:
    1. secciones de la columna C del Excel (Campanas, Estancas, Paneles, Proyectores...)
    2. gamas dentro de cada sección (ALFA, CAM, SOL...); las fichas sin gama van sueltas
    3. la ficha

Maquetación de la ficha, según lo acordado:
    arriba izquierda -> fotos (la luminaria primero)   arriba derecha -> tabla resumen
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
  .rv-crumbs{display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;padding:0.9rem 2.2rem 0;
    max-width:1800px;margin:0 auto;font-family:'Raleway',sans-serif;font-size:0.68rem;
    letter-spacing:0.16em;text-transform:uppercase;color:var(--accent-text);}
  .rv-crumb{background:none;border:none;padding:0;font:inherit;color:inherit;letter-spacing:inherit;
    cursor:pointer;text-decoration:none;}
  .rv-crumb:hover{color:var(--ink);text-decoration:underline;text-underline-offset:0.25em;}
  .rv-crumb-sep{color:var(--accent-soft);}
  .rv-crumb-actual{color:var(--ink);}
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
  .pd-grid{display:grid;grid-template-columns:minmax(0,42%) minmax(0,1fr);
    grid-template-areas:"fotos tabla" "descargas tabla";gap:2.4rem 3rem;align-items:start;
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
    .rv-crumbs{padding:0.8rem 1.3rem;}
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

<nav class="rv-crumbs" id="rvCrumbs"></nav>
<main class="rv-main"><div class="rv-grid" id="rvGrid"></div></main>

<div class="rv-overlay" id="rvOverlay">
  <button type="button" class="rv-back" id="rvBack">← Volver al listado</button>
  <div class="pd-hero">
    <span class="pd-eyebrow" id="pdEyebrow"></span>
    <h2 class="pd-title" id="pdTitle"></h2>
    <div class="pd-refs" id="pdRefs"></div>
  </div>
  <div class="pd-grid">
    <div class="pd-fotos">
      <div class="pd-main-wrap"><img id="pdMainImg" src="" alt=""></div>
      <div class="pd-thumbs" id="pdThumbs"></div>
    </div>
    <div class="pd-tabla">
      <div id="pdAviso"></div>
      <span class="pd-label">Características técnicas</span>
      <table class="pd-specs"><tbody id="pdSpecs"></tbody></table>
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
const claveSec = f => f.categoria + '||' + f.seccion;

let catActual = 'all', termino = '', sel = { seccion: null, gama: null };

const visibles = () => FICHAS.filter(f => catActual === 'all' || f.categoria === catActual);
const deSeccion = k => FICHAS.filter(f => claveSec(f) === k);
const deGama = (k, g) => deSeccion(k).filter(f => (f.gama || '\u0000' + f.id) === g);
const portada = fs => { const f = fs.find(x => x.imagenes.length); return f ? f.imagenes[0] : ''; };

// ── migas ──
function migas(partes){
  const c = document.getElementById('rvCrumbs');
  c.innerHTML = '';
  partes.forEach((p, i) => {
    if (i) c.appendChild(el('span', 'rv-crumb-sep', '/'));
    if (p.accion){
      const b = el('button', 'rv-crumb', p.t);
      b.type = 'button';
      b.addEventListener('click', p.accion);
      c.appendChild(b);
    } else {
      c.appendChild(el('span', 'rv-crumb-actual', p.t));
    }
  });
}

// ── tarjetas ──
function tarjeta({ img, eyebrow, nombre, meta, badge, badgeClase, esquina, pendiente, onClick }){
  const card = el('div', 'rv-card');
  card.innerHTML = `
    <div class="rv-card-img-wrap">
      ${img ? `<img src="${img}" alt="">` : ''}
      ${badge ? `<span class="rv-badge ${badgeClase || ''}">${badge}</span>` : ''}
      ${esquina ? `<span class="rv-refs-badge">${esquina}</span>` : ''}
      ${pendiente ? '<span class="rv-pend">tabla antigua</span>' : ''}
    </div>
    <div class="rv-card-body">
      <span class="rv-card-eyebrow">${eyebrow}</span>
      <span class="rv-card-name">${nombre}</span>
      <span class="rv-card-meta">${meta}</span>
    </div>`;
  card.addEventListener('click', onClick);
  return card;
}

function pintarSecciones(){
  const grid = document.getElementById('rvGrid');
  const claves = [];
  visibles().forEach(f => { if (!claves.includes(claveSec(f))) claves.push(claveSec(f)); });
  claves.sort((a, b) => a.localeCompare(b, 'es'));
  claves.forEach(k => {
    const fs = deSeccion(k).filter(f => catActual === 'all' || f.categoria === catActual);
    const gamas = new Set(fs.map(f => f.gama).filter(Boolean));
    grid.appendChild(tarjeta({
      img: portada(fs),
      eyebrow: CAT[fs[0].categoria] || fs[0].categoria,
      nombre: fs[0].seccion,
      meta: fs.length + ' ficha' + (fs.length === 1 ? '' : 's') +
            (gamas.size ? ' \u00b7 ' + gamas.size + ' gama' + (gamas.size === 1 ? '' : 's') : ''),
      esquina: fs.some(f => !f.generada) ? null : null,
      pendiente: fs.every(f => !f.generada),
      onClick: () => { sel = { seccion: k, gama: null }; pintar(); }
    }));
  });
  document.getElementById('rvCount').textContent = claves.length + ' secciones';
  migas([{ t: 'Todas las secciones' }]);
}

function pintarGamas(){
  const grid = document.getElementById('rvGrid');
  const fs = deSeccion(sel.seccion);
  const grupos = [];
  fs.forEach(f => {
    const g = f.gama || '\u0000' + f.id;                 // sin gama: la ficha va suelta
    if (!grupos.some(x => x.g === g)) grupos.push({ g, gama: f.gama });
  });
  grupos.sort((a, b) => (a.gama ? 0 : 1) - (b.gama ? 0 : 1) || String(a.g).localeCompare(String(b.g), 'es'));
  grupos.forEach(({ g, gama }) => {
    const sub = deGama(sel.seccion, g);
    grid.appendChild(tarjeta({
      img: portada(sub),
      eyebrow: gama ? 'Gama' : sub[0].familia,
      nombre: gama || sub[0].nombre,
      meta: gama ? sub.length + ' ficha' + (sub.length === 1 ? '' : 's')
                 : sub[0].specs.length + ' filas \u00b7 ' + sub[0].descargas.length + ' PDF',
      badge: gama ? null : sub[0].imagenes.length + ' fotos',
      badgeClase: gama ? '' : (sub[0].imagenes.length <= 1 ? 'is-caution' : ''),
      esquina: sub[0].refs.length > 1 && !gama ? sub[0].refs.length + ' códigos' : null,
      pendiente: sub.every(f => !f.generada),
      onClick: () => {
        if (!gama && sub.length === 1) return abrirFicha(sub[0]);
        sel.gama = g;
        if (deGama(sel.seccion, g).length === 1) return abrirFicha(sub[0]);
        pintar();
      }
    }));
  });
  document.getElementById('rvCount').textContent = fs.length + ' fichas';
  migas([
    { t: 'Todas las secciones', accion: () => { sel = { seccion: null, gama: null }; pintar(); } },
    { t: fs[0].seccion }
  ]);
}

function pintarFichas(lista, contexto){
  const grid = document.getElementById('rvGrid');
  lista.forEach(f => grid.appendChild(tarjeta({
    img: f.imagenes[0],
    eyebrow: (CAT[f.categoria] || f.categoria) + ' \u00b7 ' + f.seccion,
    nombre: f.nombre,
    meta: f.specs.length + ' filas \u00b7 ' + f.descargas.length + ' PDF',
    badge: f.imagenes.length + ' foto' + (f.imagenes.length === 1 ? '' : 's'),
    badgeClase: f.imagenes.length === 0 ? 'is-warn' : f.imagenes.length === 1 ? 'is-caution' : '',
    esquina: f.refs.length > 1 ? f.refs.length + ' códigos' : null,
    pendiente: !f.generada,
    onClick: () => abrirFicha(f)
  })));
  document.getElementById('rvCount').textContent = lista.length + ' ficha' + (lista.length === 1 ? '' : 's');
  migas(contexto || [{ t: 'Resultados' }]);
}

function pintar(){
  document.getElementById('rvGrid').innerHTML = '';
  const term = termino.trim().toLowerCase();
  if (term){
    const lista = visibles().filter(f => f.nombre.toLowerCase().includes(term) ||
                                         f.refs.join(' ').toLowerCase().includes(term));
    return pintarFichas(lista, [{ t: 'Buscando: ' + term }]);
  }
  if (!sel.seccion) return pintarSecciones();
  if (!sel.gama)    return pintarGamas();
  const sub = deGama(sel.seccion, sel.gama);
  pintarFichas(sub, [
    { t: 'Todas las secciones', accion: () => { sel = { seccion: null, gama: null }; pintar(); } },
    { t: sub[0].seccion, accion: () => { sel.gama = null; pintar(); } },
    { t: sub[0].gama || sub[0].nombre }
  ]);
}

// ── ficha ──
function abrirFicha(f){
  document.getElementById('pdEyebrow').textContent =
    (CAT[f.categoria] || f.categoria) + ' \u00b7 ' + f.seccion + (f.gama ? ' \u00b7 ' + f.gama : '');
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
    f.descargas.length === 1 ? 'Ficha técnica en PDF' : 'Fichas técnicas en PDF (' + f.descargas.length + ')';
  const dl = document.getElementById('pdDescargas');
  dl.innerHTML = '';
  f.descargas.forEach(d => {
    const a = el('a', 'pd-dl');
    a.href = rutaPdf(d.pdf); a.target = '_blank'; a.rel = 'noopener';
    const info = el('div', 'pd-dl-info');
    info.appendChild(el('span', 'pd-dl-titulo', d.titulo));
    info.appendChild(el('span', 'pd-dl-ref', 'Ref. ' + d.ref));
    a.appendChild(info);
    a.appendChild(el('span', 'pd-dl-icono', 'PDF \u2193'));
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

// ── filtros de categoría y buscador ──
const cats = ['all', ...new Set(FICHAS.map(f => f.categoria))];
const wrap = document.getElementById('rvFilters');
cats.forEach(c => {
  const b = el('button', 'rv-filter-btn' + (c === 'all' ? ' active' : ''), c === 'all' ? 'Todas' : (CAT[c] || c));
  b.addEventListener('click', () => {
    catActual = c; sel = { seccion: null, gama: null };
    wrap.querySelectorAll('.rv-filter-btn').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    pintar();
  });
  wrap.appendChild(b);
});
document.getElementById('rvSearch').addEventListener('input', e => { termino = e.target.value; pintar(); });
pintar();
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
