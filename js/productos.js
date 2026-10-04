/* Apheloria — Productos: dos plantillas para todo el catálogo.
 *
 *   1. Pantalla de navegación: cabecera + rejilla de tarjetas (secciones o productos).
 *   2. Ficha de producto: fotos, tabla de características, descripción y descargas.
 *
 * Cada nivel tiene su propia dirección, así que el botón atrás sube uno y se puede
 * compartir cualquier pantalla:
 *     productos.html#industriales
 *     productos.html#industriales/campanas
 *     productos.html#industriales/campanas/campanas-cam
 *     productos.html#industriales/campanas/campanas-cam/campana-grandes-alturas-para-suspender-mod-cam
 *
 * Los datos salen de js/catalogo-web.js, que genera scripts/catalogo/construir_web.py.
 */

const CAT = window.CATALOGO;
const lienzo = document.getElementById('catalogo');

const esc = t => String(t ?? '').replace(/[&<>"']/g, c =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const url = ruta => encodeURI(ruta);

// Las fotos de las fichas son pequeñas: se dejan crecer como mucho al doble
// de su tamaño real para que no se note la pérdida de calidad.
const medida = foto => `max-width:min(100%, ${(foto.px?.[0] || 400) * 2}px)`;

// ── Dónde estamos ──
function resolver(ruta) {
  const partes = ruta.split('/').filter(Boolean);
  const cadena = [{ nombre: 'Productos', ruta: '' }];
  let nodo = CAT, hasta = [];

  for (let i = 0; i < partes.length; i++) {
    const hijo = nodo.hijos.find(h => h.slug === partes[i]);
    if (hijo) {
      hasta.push(hijo.slug);
      nodo = hijo;
      cadena.push({ nombre: hijo.nombre, ruta: hasta.join('/'), salta: seSalta(hijo) });
      continue;
    }
    const producto = nodo.productos.find(p => p.slug === partes[i]);
    if (producto && i === partes.length - 1) {
      return { nodo, producto, cadena };
    }
    return null;                                   // la dirección no existe
  }
  return { nodo, producto: null, cadena };
}

// ── Piezas comunes ──
function miga(cadena, actual) {
  const trozos = cadena.map(c => `<a href="#${esc(c.ruta)}">${esc(c.nombre)}</a>`);
  trozos.push(`<span class="cat-ruta-actual">${esc(actual)}</span>`);
  return `<nav class="cat-ruta" aria-label="Ruta de navegación">
    ${trozos.join('<span class="cat-ruta-sep">/</span>')}</nav>`;
}

function tarjeta(enlace, foto, nombre, meta) {
  const img = foto
    ? `<img src="${url(foto.ruta)}" alt="${esc(nombre)}" style="${medida(foto)}" loading="lazy">`
    : '';
  return `<a class="cat-card" href="#${esc(enlace)}">
    <div class="cat-card-foto${foto ? '' : ' cat-card-foto--vacia'}">${img}</div>
    <div class="cat-card-cuerpo">
      <span class="cat-card-nombre">${esc(nombre)}</span>
      ${meta ? `<span class="cat-card-meta">${esc(meta)}</span>` : ''}
    </div></a>`;
}

// Una pantalla con una sola tarjeta no aporta nada y es un clic de más, así que se salta.
// Pasa en dos casos: la sección no tiene productos propios y solo lleva a otra sección,
// o lo único que hay dentro es un producto suelto.
const seSalta = n => !n.productos.length && n.hijos.length === 1;

function rutaDirecta(nodo, ruta) {
  let n = nodo, r = ruta;
  while (seSalta(n)) {
    n = n.hijos[0];
    r += '/' + n.slug;
  }
  if (!n.hijos.length && n.productos.length === 1) {
    r += '/' + n.productos[0].slug;
  }
  return r;
}


// ── Plantilla 1: pantalla de navegación ──
function pintarNavegacion(nodo, cadena, ruta) {
  const padres = cadena.slice(0, -1).filter(c => !c.salta).map(c => c.nombre).join(' · ');
  const foto = nodo.hero;
  const cabecera = `<header class="cat-hero${foto ? '' : ' cat-hero--sin-foto'}">
      ${foto ? `<div class="cat-hero-foto"><img src="${url(foto.ruta)}" alt="${esc(nodo.nombre)}"></div>` : ''}
      <div>
        ${padres ? `<span class="cat-hero-eyebrow">${esc(padres)}</span>` : ''}
        <h1 class="cat-hero-titulo">${esc(nodo.nombre)}</h1>
        ${nodo.texto ? `<p class="cat-hero-texto">${esc(nodo.texto)}</p>` : ''}
      </div>
    </header>`;

  const bloques = [];
  if (nodo.hijos.length) {
    const n = nodo.hijos.length;
    bloques.push(`<span class="cat-apartado">${n} ${n === 1 ? 'sección' : 'secciones'}</span>
      <div class="cat-grid">` + nodo.hijos.map(h => tarjeta(
        rutaDirecta(h, ruta ? ruta + '/' + h.slug : h.slug), h.portada, h.nombre,
        `${h.cuenta} ${h.cuenta === 1 ? 'producto' : 'productos'}`)).join('') + '</div>');
  }
  if (nodo.productos.length) {
    const n = nodo.productos.length;
    bloques.push(`<span class="cat-apartado">${n} ${n === 1 ? 'producto' : 'productos'}</span>
      <div class="cat-grid">` + nodo.productos.map(p => tarjeta(
        ruta ? ruta + '/' + p.slug : p.slug, p.fotos.luminaria, p.nombre, p.resumen)).join('') + '</div>');
  }

  const actual = cadena[cadena.length - 1].nombre;
  const previas = cadena.slice(0, -1).filter(c => !c.salta);
  return (previas.length ? miga(previas, actual) : '') + cabecera + bloques.join('');
}

// ── Plantilla 2: ficha de producto ──
const NOMBRE_FOTO = { luminaria: 'Producto', medidas: 'Medidas', ambiente: 'Ambiente', angulo: 'Curva fotométrica' };

function pintarFicha(producto, cadena) {
  const fotos = Object.entries(producto.fotos).filter(([, f]) => f);
  const principal = producto.fotos.luminaria || (fotos[0] || [])[1];

  const galeria = `<div class="ficha-galeria">
      <figure class="ficha-foto" id="fichaFoto">
        ${principal ? `<img src="${url(principal.ruta)}" alt="${esc(producto.nombre)}" style="${medida(principal)}">` : ''}
      </figure>
      ${fotos.length > 1 ? `<div class="ficha-miniaturas">` + fotos.map(([tipo, f], i) => `
        <button type="button" class="ficha-mini${f === principal ? ' activa' : ''}"
                data-foto="${url(f.ruta)}" data-ancho="${f.px?.[0] || 400}"
                title="${esc(NOMBRE_FOTO[tipo] || tipo)}" aria-label="${esc(NOMBRE_FOTO[tipo] || tipo)}">
          <img src="${url(f.ruta)}" alt="${esc(NOMBRE_FOTO[tipo] || tipo)}" loading="lazy"></button>`).join('')
        + `</div><span class="ficha-mini-pie">Pulsa una miniatura para verla en grande</span>` : ''}
    </div>`;

  const tabla = producto.tabla.length ? `<table class="ficha-tabla">
      <tbody>${producto.tabla.map(([et, v]) =>
        `<tr><th scope="row">${esc(et)}</th><td>${esc(v)}</td></tr>`).join('')}</tbody></table>
      ${producto.notas.length ? `<ul class="ficha-notas">`
        + producto.notas.map(n => `<li>${esc(n)}</li>`).join('') + '</ul>' : ''}`
    : '<p class="cat-vacio" style="padding:0">Esta ficha no trae tabla de características.</p>';

  const descripcion = producto.descripcion.length ? `<div class="ficha-pie">
      <span class="ficha-rotulo">Descripción</span>
      <div class="ficha-desc">${producto.descripcion.map(d => `<p>${esc(d)}</p>`).join('')}</div>
    </div>` : '';

  const descargas = producto.fichas.length ? `<div class="ficha-pie">
      <span class="ficha-rotulo">Fichas técnicas</span>
      <div class="ficha-descargas">${producto.fichas.map(f => `
        <a class="ficha-descarga" href="${url(f.pdf)}" target="_blank" rel="noopener">
          Ficha técnica${f.etiqueta ? ' ' + esc(f.etiqueta) : ''}
          <span class="ficha-descarga-flecha" aria-hidden="true">↗</span></a>`).join('')}</div>
    </div>` : '';

  return miga(cadena.filter(c => !c.salta), producto.nombre) + `
    <header class="ficha-cabecera">
      <h1 class="ficha-titulo">${esc(producto.nombre)}</h1>
      <span class="ficha-refs">Ref. ${producto.codigos.map(esc).join(' · ')}</span>
    </header>
    <div class="ficha-cuerpo">${galeria}<div>${tabla}</div></div>
    ${descripcion}${descargas}`;
}

// ── Pintado y direcciones ──
function pintar() {
  const ruta = decodeURIComponent(location.hash.slice(1));
  const sitio = resolver(ruta);
  if (!sitio) {
    lienzo.innerHTML = `<p class="cat-vacio">Esa dirección ya no existe.
      <a href="#">Volver a Productos</a>.</p>`;
    return;
  }
  lienzo.innerHTML = sitio.producto
    ? pintarFicha(sitio.producto, sitio.cadena)
    : pintarNavegacion(sitio.nodo, sitio.cadena, ruta);
  document.title = (sitio.producto ? sitio.producto.nombre
                                   : sitio.cadena[sitio.cadena.length - 1].nombre)
                   + ' — Apheloria Solutions';
}

// Cambiar la foto grande desde las miniaturas
lienzo.addEventListener('click', e => {
  const mini = e.target.closest('.ficha-mini');
  if (!mini) return;
  const foto = document.querySelector('#fichaFoto img');
  if (!foto) return;
  foto.src = mini.dataset.foto;
  foto.style.maxWidth = `min(100%, ${mini.dataset.ancho * 2}px)`;
  lienzo.querySelectorAll('.ficha-mini').forEach(m => m.classList.toggle('activa', m === mini));
});

window.addEventListener('hashchange', () => { pintar(); window.scrollTo({ top: 0 }); });
pintar();
