/* Apheloria — común a todas las páginas: menú, desplegable y enlaces antiguos. */

// ── Enlaces antiguos: cuando la web era un solo archivo con #inicio…#contacto ──
// index.html#productos/industrial  ->  productos.html#industrial
(function redirigirEnlacesAntiguos() {
  const hash = location.hash.slice(1);
  if (!hash) return;
  const [seccion, filtro] = hash.split('/');
  const paginas = { proyectos: 'proyectos.html', productos: 'productos.html',
                    catalogo: 'catalogo.html', contacto: 'contacto.html' };
  if (seccion === 'inicio') {
    history.replaceState(null, '', location.pathname);
    return;
  }
  const destino = paginas[seccion];
  if (destino && !location.pathname.endsWith(destino)) {
    location.replace(destino + (filtro ? '#' + filtro : ''));
  }
})();

// ── Apartado activo en el menú ──
(function marcarApartado() {
  const actual = document.body.dataset.pagina;
  document.querySelectorAll('nav [data-pagina]').forEach(a =>
    a.classList.toggle('active', a.dataset.pagina === actual));
})();

// ── Menú móvil ──
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const abierto = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(abierto));
  });
}
function cerrarMenu() {
  if (!navLinks) return;
  navLinks.classList.remove('open');
  navToggle.setAttribute('aria-expanded', 'false');
}

// ── Desplegable "Productos": se cierra con un poco de margen para poder
//    cruzar en diagonal hasta él sin que se cierre por el camino ──
document.querySelectorAll('.nav-item').forEach(item => {
  let temporizador = null;
  item.addEventListener('mouseenter', () => {
    clearTimeout(temporizador);
    item.classList.add('dropdown-open');
  });
  item.addEventListener('mouseleave', () => {
    temporizador = setTimeout(() => item.classList.remove('dropdown-open'), 350);
  });
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') cerrarMenu();
});
