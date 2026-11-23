/* Apheloria — Estudios Lumínicos: pestañas del caso real y aparición al desplazarse. */

// ── Visor del caso real: una pestaña por documento del estudio ──
// Las vistas ocultas llevan el atributo hidden (display:none), así sus imágenes
// con loading="lazy" no se descargan hasta que se abren.
(function visor() {
  const tabs = [...document.querySelectorAll('.est-visor-tabs [role="tab"]')];
  if (!tabs.length) return;

  function abrir(tab, foco) {
    tabs.forEach(t => {
      const activa = t === tab;
      t.setAttribute('aria-selected', String(activa));
      t.tabIndex = activa ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !activa;
    });
    if (foco) tab.focus();
  }

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => abrir(tab));
    // flechas para moverse entre pestañas, como en cualquier tablist
    tab.addEventListener('keydown', e => {
      const rtl = document.documentElement.dir === 'rtl';
      const paso = { ArrowRight: rtl ? -1 : 1, ArrowLeft: rtl ? 1 : -1 }[e.key];
      if (paso) abrir(tabs[(i + paso + tabs.length) % tabs.length], true);
      else if (e.key === 'Home') abrir(tabs[0], true);
      else if (e.key === 'End') abrir(tabs[tabs.length - 1], true);
      else return;
      e.preventDefault();
    });
  });
})();

// ── Aparición suave de los bloques al entrar en pantalla ──
(function aparecer() {
  if (!('IntersectionObserver' in window)) return;
  document.body.classList.add('est-animado');
  const observador = new IntersectionObserver(entradas => {
    entradas.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('visible');
      observador.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(el => observador.observe(el));
})();
