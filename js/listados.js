/* Apheloria — Proyectos y Productos: filtros y paneles de detalle con dirección propia.
 *
 * La dirección refleja dónde estás, y el botón atrás sube un nivel cada vez:
 *     productos.html#industrial                  filtro
 *     productos.html#industrial/campanas         familia
 *     productos.html#industrial/campanas/cam     gama
 * Se puede abrir o compartir cualquiera de ellas directamente.
 */

const listado = document.querySelector('.listado');
const paneles = [...document.querySelectorAll('.product-detail-view')];
const botonesFiltro = [...document.querySelectorAll('.products-filters .filter-btn, .projects-filters .filter-btn')];
const rejilla = document.querySelector('.products-grid, .projects-grid');
const contadorId = document.querySelector('.products-count, .projects-count')?.id
                || (document.getElementById('prodCount') ? 'prodCount' : 'projCount');

const PREFIJOS = ['detail-', 'proj-'];
const aSlug = id => PREFIJOS.reduce((s, p) => (s.startsWith(p) ? s.slice(p.length) : s), id);
const aId = slug => paneles.find(p => aSlug(p.id) === slug)?.id || null;

// Estado actual: filtro + pila de paneles abiertos
let filtro = 'all';
let pila = [];

// ── Pintado ──
function aplicarFiltro(f) {
  let n = 0;
  document.querySelectorAll('.products-grid .product-card, .projects-grid .project-card').forEach(c => {
    const ver = f === 'all' || c.dataset.category === f;
    c.hidden = !ver;
    if (ver) n++;
  });
  botonesFiltro.forEach(b => b.classList.toggle('active', b.dataset.filter === f));
  const contador = document.getElementById(contadorId);
  if (contador) contador.textContent = '( ' + n + ' )';
  if (rejilla) {                       // reinicia la animación de aparición
    rejilla.style.animation = 'none';
    void rejilla.offsetWidth;
    rejilla.style.animation = '';
  }
}

function pintar() {
  aplicarFiltro(filtro);
  const arriba = pila[pila.length - 1] || null;     // solo se ve el último nivel
  paneles.forEach(p => p.classList.toggle('visible', p.id === arriba));
  if (listado) listado.hidden = pila.length > 0;
  document.body.classList.toggle('con-panel', pila.length > 0);
}

// ── Dirección ──
function aTexto() {
  const partes = [];
  if (filtro !== 'all') partes.push(filtro);
  pila.forEach(id => partes.push(aSlug(id)));
  return partes.join('/');
}

function desdeTexto(hash) {
  const partes = (hash || '').split('/').filter(Boolean);
  filtro = partes.length && botonesFiltro.some(b => b.dataset.filter === partes[0]) ? partes[0] : 'all';
  const desde = (partes.length && filtro !== 'all') || partes[0] === 'all' ? 1 : 0;
  pila = partes.slice(desde).map(aId).filter(Boolean);
}

function ir(nuevoFiltro, nuevaPila, apilar = true) {
  filtro = nuevoFiltro;
  pila = nuevaPila;
  const destino = aTexto();
  const url = location.pathname + (destino ? '#' + destino : '');
  if (apilar) history.pushState(null, '', url);
  else history.replaceState(null, '', url);
  pintar();
  window.scrollTo({ top: 0, behavior: 'auto' });
}

// Sube un nivel, igual que la miga de pan. No usamos history.back() porque al
// entrar por un enlace directo no hay historial propio al que volver.
const subirNivel = () => ir(filtro, pila.slice(0, -1));

// ── Interacción ──
botonesFiltro.forEach(b => b.addEventListener('click', () => ir(b.dataset.filter, [])));

document.addEventListener('click', e => {
  const cerrarTodo = e.target.closest('[data-close-all]');
  if (cerrarTodo) { ir(filtro, []); return; }

  const cerrar = e.target.closest('[data-close]');
  if (cerrar) {                                    // la miga de pan sube un nivel
    const i = pila.indexOf(cerrar.dataset.close);
    ir(filtro, i >= 0 ? pila.slice(0, i) : pila.slice(0, -1));
    return;
  }

  const abrir = e.target.closest('[data-open]');
  if (abrir && document.getElementById(abrir.dataset.open)) {
    ir(filtro, [...pila, abrir.dataset.open]);
  }
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && pila.length) { subirNivel(); return; }
  if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('[data-open][role="button"]')) {
    e.preventDefault();
    ir(filtro, [...pila, e.target.dataset.open]);
  }
});

// popstate: botón atrás/adelante. hashchange: enlaces del menú dentro de la misma página
// (p. ej. el desplegable de Productos apuntando a productos.html#interior).
function sincronizarConLaUrl() {
  desdeTexto(location.hash.slice(1));
  pintar();
}
window.addEventListener('popstate', sincronizarConLaUrl);
window.addEventListener('hashchange', sincronizarConLaUrl);

// ── Arranque: respeta la dirección con la que se ha entrado ──
desdeTexto(location.hash.slice(1));
pintar();
