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

let saliendo = null;

function verFondo(i) {
  if (i === fondoActual) return;
  const ds = document.querySelectorAll('.hero-dot');
  const previa = fondos[fondoActual];

  // La que se va sigue acercándose mientras se funde. Si se le quitara la animación de
  // golpe volvería a su tamaño original y se vería el tirón por debajo de la nueva.
  if (saliendo) { clearTimeout(saliendo.reloj); saliendo.foto.classList.remove('saliendo'); }
  previa.classList.remove('active');
  previa.classList.add('saliendo');
  saliendo = { foto: previa, reloj: setTimeout(() => previa.classList.remove('saliendo'), 1400) };

  ds[fondoActual].classList.remove('active');
  fondoActual = i;
  const nueva = fondos[i];
  nueva.classList.remove('saliendo');
  nueva.style.animation = 'none';          // el acercamiento empieza de cero
  void nueva.offsetWidth;
  nueva.style.animation = '';
  nueva.classList.add('active');
  ds[i].classList.add('active');
}

// Las diapositivas 2 a 5 traen la ruta en data-foto y se cargan cuando la página ya ha
// terminado, para que no compitan con la primera, que es la que se ve. Van sobradas de
// tiempo: la primera no cambia hasta los 6 s.
function cargarFondosEnDiferido() {
  document.querySelectorAll('.hero-bg-img[data-foto]').forEach(el => {
    el.style.backgroundImage = `var(--velo), url('${el.dataset.foto}')`;
    delete el.dataset.foto;
  });
}
if (document.readyState === 'complete') cargarFondosEnDiferido();
else window.addEventListener('load', cargarFondosEnDiferido);

const sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (fondos.length > 0 && !sinMovimiento) {
  // 6 s: el acercamiento de css/inicio.css dura 9 s, así nunca llega al final ni se para
  setInterval(() => verFondo((fondoActual + 1) % fondos.length), 6000);
}

// ── Botones de bajada ──
const irA = sel => {
  const el = document.querySelector(sel);
  if (el) window.scrollTo({ top: el.offsetTop - parseFloat(getComputedStyle(document.body).paddingTop), behavior: 'smooth' });
};
document.getElementById('scrollHint').addEventListener('click', () => irA('.intro-connector'));
document.getElementById('connectorDown').addEventListener('click', () => irA('.intro-nosotros'));
document.getElementById('btnProductos').addEventListener('click', () => { location.href = 'productos.html'; });
document.getElementById('btnProyectos').addEventListener('click', () => { location.href = 'proyectos.html'; });

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
