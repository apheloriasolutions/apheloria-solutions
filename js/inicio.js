/* Apheloria — portada: slideshow del hero, revelado al bajar y efecto cortina. */

// Dispara las animaciones de entrada del hero (antes dependían de .slide.active)
requestAnimationFrame(() => document.body.classList.add('lista'));

// ── Slideshow del hero ──
const fondos = document.querySelectorAll('.hero-bg-img');
const puntos = document.getElementById('heroDots');
let fondoActual = 0;

fondos.forEach((_, i) => {
  const d = document.createElement('button');
  d.type = 'button';
  d.className = 'hero-dot' + (i === 0 ? ' active' : '');
  d.setAttribute('aria-label', 'Ver imagen ' + (i + 1));
  d.addEventListener('click', () => verFondo(i));
  puntos.appendChild(d);
});

function verFondo(i) {
  const ds = document.querySelectorAll('.hero-dot');
  fondos[fondoActual].classList.remove('active');
  ds[fondoActual].classList.remove('active');
  fondoActual = i;
  fondos[fondoActual].classList.add('active');
  ds[fondoActual].classList.add('active');
}

const sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (fondos.length > 0 && !sinMovimiento) {
  setInterval(() => verFondo((fondoActual + 1) % fondos.length), 4000);
}

// ── Botones de bajada ──
const irA = sel => {
  const el = document.querySelector(sel);
  if (el) window.scrollTo({ top: el.offsetTop - parseFloat(getComputedStyle(document.body).paddingTop), behavior: 'smooth' });
};
document.getElementById('scrollHint').addEventListener('click', () => irA('.intro-connector'));
document.getElementById('connectorDown').addEventListener('click', () => irA('.intro-nosotros'));
document.getElementById('btnProductos').addEventListener('click', () => { location.href = 'productos.html'; });

// ── Revelado al entrar en pantalla ──
const observador = new IntersectionObserver(entradas => {
  entradas.forEach(e => { if (e.isIntersecting) e.target.classList.add('in-view'); });
}, { threshold: 0.25 });
document.querySelectorAll('.scroll-reveal').forEach(el => observador.observe(el));

// ── Cortina: los fondos se quedan quietos mientras la sección sube ──
// Cada fondo compensa el scroll con la posición de su propia sección, así que
// sigue funcionando aunque las secciones no midan exactamente una pantalla.
const cortinas = [
  ['.hero-bg', '.intro-hero'],
  ['.connector-bg', '.intro-connector'],
  ['#nosotrosBg', '.intro-nosotros'],
].map(([fondo, seccion]) => [document.querySelector(fondo), document.querySelector(seccion)])
 .filter(([f, s]) => f && s);

function moverCortinas() {
  const y = window.scrollY + parseFloat(getComputedStyle(document.body).paddingTop);
  cortinas.forEach(([fondo, seccion]) => {
    fondo.style.transform = 'translateY(' + (y - seccion.offsetTop) + 'px)';
  });
}
window.addEventListener('scroll', moverCortinas, { passive: true });
window.addEventListener('resize', moverCortinas);
moverCortinas();
