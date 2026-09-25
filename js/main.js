/* Apheloria — JS del sitio.
   Extraído de index.html sin cambios de comportamiento; se reparte por páginas en la parte 2. */

// ── Navegación entre slides ──
const slides = document.querySelectorAll('.slide');
const ROUTES = ['inicio', 'proyectos', 'productos', 'catalogo', 'contacto'];
let current = 0;

function updateNav(idx) {
  document.querySelectorAll('nav a[data-slide]').forEach(a =>
    a.classList.toggle('active', parseInt(a.dataset.slide, 10) === idx));
}

function goTo(index, updateHash = true) {
  closeMenu();
  if (index < 0 || index >= slides.length) return;
  if (index === current) {
    // Ya estás en esta sección: si hay una ficha de producto abierta, ciérrala
    // y vuelve a la vista general en vez de no hacer nada.
    closeAllPanels();
    if (updateHash) history.replaceState(null, '', '#' + ROUTES[index]);
    return;
  }
  closeAllPanels();
  if (index === 0) slides[0].scrollTop = 0;
  const out = slides[current];
  const next = slides[index];
  out.classList.remove('active');
  out.classList.add('exiting');
  setTimeout(() => out.classList.remove('exiting'), 1450); // debe superar --dur-slide (1.25s)
  current = index;
  requestAnimationFrame(() => {
    next.classList.add('active');
    updateNav(current);
  });
  if (updateHash) history.replaceState(null, '', '#' + ROUTES[index]);
}

// Actualiza el hash con la subsección activa, ej. #productos/industrial
function setSubRoute(routeName, filter) {
  const hash = filter === 'all' ? routeName : routeName + '/' + filter;
  history.replaceState(null, '', '#' + hash);
}

document.querySelectorAll('nav a[data-slide]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const idx = parseInt(a.dataset.slide, 10);
    if (idx === 0 && current === 0) { slides[0].scrollTo({ top: 0, behavior: 'smooth' }); closeMenu(); return; }
    goTo(idx);
  });
});
document.getElementById('nav-logo').addEventListener('click', () => {
  if (current === 0) { slides[0].scrollTo({ top: 0, behavior: 'smooth' }); return; }
  goTo(0);
});

// Rutas #hash: enlazables y con soporte de carga directa.
// Formato: #seccion  ó  #seccion/filtro (ej. #productos/industrial)
function applyHash(hash) {
  const [routeName, filterName] = hash.split('/');
  const idx = ROUTES.indexOf(routeName);
  if (idx < 0) return;
  goTo(idx, false);
  if (filterName) {
    const wrap = routeName === 'productos' ? '.products-filters' : '.projects-filters';
    const btn = document.querySelector(wrap + ' .filter-btn[data-filter="' + filterName + '"]');
    if (btn) btn.click();
  }
}
window.addEventListener('hashchange', () => applyHash(location.hash.slice(1)));
if (location.hash.slice(1)) applyHash(location.hash.slice(1));

// ── Menú móvil ──
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
navToggle.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
});
function closeMenu() {
  navLinks.classList.remove('open');
  navToggle.setAttribute('aria-expanded', 'false');
}

// ── Slideshow del hero ──
const bgImgs = document.querySelectorAll('.hero-bg-img');
const dotsEl = document.getElementById('heroDots');
let bgCurrent = 0;
bgImgs.forEach((_, i) => {
  const d = document.createElement('div');
  d.className = 'hero-dot' + (i === 0 ? ' active' : '');
  d.addEventListener('click', () => setBg(i));
  dotsEl.appendChild(d);
});
function setBg(i) {
  const dots = document.querySelectorAll('.hero-dot');
  bgImgs[bgCurrent].classList.remove('active');
  dots[bgCurrent].classList.remove('active');
  bgCurrent = i;
  bgImgs[bgCurrent].classList.add('active');
  dots[bgCurrent].classList.add('active');
}
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (bgImgs.length > 0 && !prefersReducedMotion) setInterval(() => setBg((bgCurrent + 1) % bgImgs.length), 4000);

// ── Filtros (un único grid, se ocultan cards por categoría) ──
function bindFilters(wrapSel, gridSel, cardSel, countId, routeName) {
  const btns = document.querySelectorAll(wrapSel + ' .filter-btn');
  const grid = document.querySelector(gridSel);
  btns.forEach(btn => btn.addEventListener('click', () => {
    btns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.filter;
    let n = 0;
    document.querySelectorAll(gridSel + ' ' + cardSel).forEach(c => {
      const show = f === 'all' || c.dataset.category === f;
      c.hidden = !show;
      if (show) n++;
    });
    document.getElementById(countId).textContent = '( ' + n + ' )';
    setSubRoute(routeName, f);
    // Reinicia la animación de aparición de la rejilla (se perdía al filtrar sobre un único grid)
    grid.classList.remove('active');
    void grid.offsetWidth;
    grid.classList.add('active');
  }));
}
bindFilters('.projects-filters', '#grid-all', '.project-card', 'projCount', 'proyectos');
bindFilters('.products-filters', '#prod-grid-all', '.product-card', 'prodCount', 'productos');

// Dropdown "Productos": se abre al pasar el ratón y se cierra con un pequeño
// margen de tiempo (no al instante), para poder cruzar hasta él en diagonal
// y pulsar p.ej. "Industrial" sin que se cierre por el camino.
document.querySelectorAll('.nav-item').forEach(item => {
  let closeTimer = null;
  item.addEventListener('mouseenter', () => {
    clearTimeout(closeTimer);
    item.classList.add('dropdown-open');
  });
  item.addEventListener('mouseleave', () => {
    closeTimer = setTimeout(() => item.classList.remove('dropdown-open'), 350);
  });
});

// Dropdown del nav: ir a Productos con el filtro aplicado
document.querySelectorAll('.nav-dropdown .dropdown-link').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    closeAllPanels();
    const item = link.closest('.nav-item');
    if (item) item.classList.remove('dropdown-open');
    goTo(2);
    const btn = document.querySelector('.products-filters .filter-btn[data-filter="' + link.dataset.filter + '"]');
    if (btn) btn.click();
  });
});

// ── Paneles de detalle: delegación de eventos ──
function openPanel(id) {
  const p = document.getElementById(id);
  if (p) { p.classList.add('visible'); p.scrollTop = 0; }
}
function closePanel(id) {
  const p = document.getElementById(id);
  if (p) p.classList.remove('visible');
}
function closeAllPanels() {
  document.querySelectorAll('.product-detail-view.visible').forEach(v => v.classList.remove('visible'));
}

document.addEventListener('click', e => {
  const closeAll = e.target.closest('[data-close-all]');
  if (closeAll) { closeAllPanels(); return; }
  const closer = e.target.closest('[data-close]');
  if (closer) { closePanel(closer.dataset.close); return; }
  const opener = e.target.closest('[data-open]');
  if (opener) openPanel(opener.dataset.open);
});

// Teclado: Enter/Espacio abre cards, Escape cierra panel o menú
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    const open = document.querySelectorAll('.product-detail-view.visible');
    if (open.length) open[open.length - 1].classList.remove('visible');
    else closeMenu();
    return;
  }
  if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('[data-open][role="button"]')) {
    e.preventDefault();
    openPanel(e.target.dataset.open);
  }
});

// ── Scroll con rueda: interno en grids, bloqueado en el resto ──
window.addEventListener('wheel', e => {
  if (current === 1 || current === 2) {
    if (document.querySelector('.product-detail-view.visible')) return;
    const grid = document.querySelector(current === 1 ? '.projects-grid.active' : '.products-grid.active');
    if (grid) {
      const atBottom = grid.scrollHeight - grid.scrollTop <= grid.clientHeight + 5;
      const atTop = grid.scrollTop === 0;
      if ((e.deltaY > 0 && !atBottom) || (e.deltaY < 0 && !atTop)) return;
    }
    e.preventDefault();
    return;
  }
  if (current === 3 || current === 4) {
    // en pantallas pequeñas estos slides tienen scroll interno propio
    if (e.target.closest('.slide-inner')) return;
    e.preventDefault();
  }
}, { passive: false });

// ── Intro: CTAs de scroll y animaciones al entrar en viewport ──
const introSlide = slides[0];
document.getElementById('scrollHint').addEventListener('click', () => {
  introSlide.scrollTo({ top: document.querySelector('.intro-connector').offsetTop, behavior: 'smooth' });
});
document.getElementById('connectorDown').addEventListener('click', () => {
  introSlide.scrollTo({ top: document.querySelector('.intro-nosotros').offsetTop, behavior: 'smooth' });
});
document.getElementById('btnProductos').addEventListener('click', () => goTo(2));

const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('in-view');
  });
}, { root: introSlide, threshold: 0.25 });
document.querySelectorAll('.scroll-reveal').forEach(el => revealObserver.observe(el));

// Cortina: los fondos quedan fijos mientras las secciones suben
const heroBgEl = document.querySelector('.hero-bg');
const connectorBgEl = document.querySelector('.connector-bg');
const nosotrosBgEl = document.getElementById('nosotrosBg');
introSlide.addEventListener('scroll', () => {
  const s = introSlide.scrollTop;
  const vh = introSlide.clientHeight;
  if (heroBgEl) heroBgEl.style.transform = 'translateY(' + s + 'px)';
  if (connectorBgEl) connectorBgEl.style.transform = 'translateY(' + (s - vh) + 'px)';
  if (nosotrosBgEl) nosotrosBgEl.style.transform = 'translateY(' + (s - 2 * vh) + 'px)';
}, { passive: true });

// ── Formulario de contacto: envío real vía Web3Forms (sin salir de la página) ──
const contactForm = document.getElementById('contactForm');
const contactFeedback = document.getElementById('conFeedback');
const contactSendBtn = contactForm ? contactForm.querySelector('.con-send') : null;

function showContactFeedback(message, ok) {
  contactFeedback.textContent = message;
  contactFeedback.classList.remove('is-ok', 'is-error');
  contactFeedback.classList.add(ok ? 'is-ok' : 'is-error');
  contactFeedback.hidden = false;
  requestAnimationFrame(() => contactFeedback.classList.add('visible'));
}

if (contactForm) {
  contactForm.addEventListener('submit', async e => {
    e.preventDefault();
    // Honeypot: si un bot ha rellenado este campo oculto, no enviamos nada
    if (contactForm.botcheck && contactForm.botcheck.checked) return;

    contactSendBtn.disabled = true;
    const originalLabel = contactSendBtn.textContent;
    contactSendBtn.textContent = 'Enviando…';

    try {
      const res = await fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { 'Accept': 'application/json' }
      });
      const data = await res.json();
      if (data.success) {
        showContactFeedback('Mensaje enviado. Te responderemos lo antes posible.', true);
        contactForm.reset();
      } else {
        showContactFeedback('No se ha podido enviar. Escríbenos a info@apheloria.es.', false);
      }
    } catch (err) {
      showContactFeedback('No se ha podido enviar. Escríbenos a info@apheloria.es.', false);
    } finally {
      contactSendBtn.disabled = false;
      contactSendBtn.textContent = originalLabel;
    }
  });
}

updateNav(0);
