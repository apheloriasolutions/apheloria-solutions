# Auditoría web — Apheloria Solutions

**Fecha:** 2026-07-13 · **Alcance:** [index.html](index.html) (2.985 líneas, ~268 KB) + assets del repositorio
**Stack:** sitio estático de un solo archivo HTML (CSS y JS inline). Sin framework, sin build, sin dependencias npm. Navegación tipo SPA por "slides" con transiciones.

---

## Resumen ejecutivo

La base visual es sólida y coherente con la referencia (Agolar/Vanila), y los 177 enlaces a fichas técnicas PDF resuelven correctamente. Sin embargo, el sitio **no está en estado publicable**: las secciones Catálogo y Contacto están vacías (pantalla en blanco), los nombres de producto en las vistas de detalle son invisibles (texto crema sobre fondo crema), las 307 imágenes son placeholders de picsum.photos (mientras 64 fotos reales de producto están sin usar en `images/`), y no existe ni una sola media query ni gesto táctil: en móvil el sitio es inutilizable. SEO y accesibilidad están a cero (sin meta description, sin ARIA, sin alt, tipografías de 7 px). La mayoría de arreglos son de bajo esfuerzo porque el CSS necesario ya existe.

---

## Tabla de hallazgos

| # | Área | Severidad | Descripción | Ubicación |
|---|------|-----------|-------------|-----------|
| 1 | Funcional | **Crítico** | Los slides Catálogo y Contacto no tienen contenido (`<div class="slide-inner"></div>` vacío). El menú lleva a una pantalla en blanco y, como el handler `wheel` hace `preventDefault()` en los índices 3 y 4, el usuario queda "atrapado" sin scroll. Todo el CSS del formulario y del catálogo existe (`.cat-*`, `.con-*`) pero el markup fue borrado. Bug ya documentado en [.agent.md](.agent.md). | [index.html:2528-2535](index.html#L2528-L2535), CSS huérfano en [index.html:643-726](index.html#L643-L726) |
| 2 | Visual/Funcional | **Crítico** | Nombres de producto invisibles en las 48 vistas de detalle: `.product-card-name` tiene `color: #F2EDE4` (pensado para overlay sobre foto) pero en las vistas de detalle va dentro de `.product-card-body` —clase usada 115 veces en el HTML y **sin ninguna regla CSS**— sobre fondo `#F2EDE4`. Texto crema sobre fondo crema. | [index.html:465-469](index.html#L465-L469) vs. p. ej. [index.html:2477](index.html#L2477) |
| 3 | Contenido/Performance | **Crítico** | 307 imágenes son placeholders de `picsum.photos` (aleatorias, dependencia externa que no debe llegar a producción), mientras la carpeta [images/](images/) contiene 64 fotos reales de producto que **no se referencian ni una vez**. Además, ~231 de esos placeholders están en vistas de detalle ocultas con `opacity: 0` (no `display: none`), así que **todas se descargan al cargar la página** (~240 peticiones de imágenes 1400×900). | Todo el documento; vistas de detalle [index.html:1376-2525](index.html#L1376-L2525) |
| 4 | Responsive/Móvil | **Crítico** | Cero media queries en todo el CSS. Sin menú hamburguesa (los 5 enlaces del nav a 0.65rem se desbordan), paneles de ancho fijo (`.cat-panel` 440px, `.con-right` 420px), grids de 3-4 columnas sin colapso. El handler `touchend` calcula el desplazamiento y **no hace nada con él**: en móvil no hay forma de navegar entre slides salvo el menú. `100vh` con `overflow: hidden` agrava el problema en iOS Safari (usar `100dvh`). | CSS completo; [index.html:2664-2670](index.html#L2664-L2670) |
| 5 | Accesibilidad | **Crítico** | Cero atributos ARIA, `tabindex`, `role` o handlers de teclado en todo el documento. Los enlaces del nav son `<a>` **sin `href`** (no focusables ni operables con teclado). El dropdown de Productos solo abre con `:hover` (inaccesible por teclado y por táctil). Toda imagen es `background-image`: no existe ningún texto alternativo. Spans clicables anidados dentro de `<button>` (interactivos anidados, inválido). | [index.html:736-752](index.html#L736-L752), [index.html:57](index.html#L57), breadcrumbs p. ej. [index.html:2464](index.html#L2464) |
| 6 | Accesibilidad | **Importante** | Tipografías ilegibles: abundan tamaños de 0.44–0.58rem (**7–9 px**) con letter-spacing de hasta 0.45em (`.project-num`, `.con-ilbl`, `.cat-sub`, metas de cards). El acento `#b0a898` sobre fondo `#F2EDE4` ronda un contraste ~1.6:1 (WCAG AA exige 4.5:1) y se usa para textos informativos, no solo decorativos. | p. ej. [index.html:384-389](index.html#L384-L389), [index.html:724](index.html#L724) |
| 7 | SEO | **Importante** | El `<head>` solo tiene `title` y `viewport`: sin meta description, sin Open Graph/Twitter Card, sin favicon, sin canonical, sin robots.txt ni sitemap. Al ser una SPA de slides sin hash-routing, Proyectos/Productos/Contacto no tienen URL propia ni son enlazables/indexables por sección. Las imágenes de fondo CSS no se indexan en Google Imágenes. | [index.html:1-7](index.html#L1-L7) |
| 8 | Marca/Diseño | **Importante** | Incumple la guía de marca del propio repo (CLAUDE.md): el fondo global es `#ffffff` en vez de `#F2EDE4`; los títulos usan Montserrat y Raleway cuando la guía especifica Cormorant Garamond (que solo se usa en el logo del nav); se cargan **4 familias** de Google Fonts (Cormorant, Inter, Montserrat, Raleway con 6+ variantes) cuando la guía define 2. La "sidebar derecha con logo" que la guía marca como hecha ya no existe en el markup. | [index.html:7](index.html#L7), [index.html:10](index.html#L10), [index.html:126](index.html#L126) |
| 9 | Layout | **Importante** | Desajuste nav/contenido: el `<nav>` mide `height: 70px` pero `.page-layout` está anclado a `top: 56px` con `height: calc(100vh - 56px)` → 14 px de contenido quedan permanentemente tapados bajo la barra. | [index.html:16](index.html#L16) vs. [index.html:72-73](index.html#L72-L73) |
| 10 | Código muerto | **Importante** | CSS sin markup que lo use: `.sidebar*` (63 líneas), `.projects-list*`/`.project-row*`/`.proj-hover-img` (layout de lista abandonado), todo `.cat-*` y `.con-*` (ver hallazgo 1). JS muerto: listener `touchend` sin efecto. Comentario `<!-- SLIDE 3: CATÁLOGO -->` duplicado. | [index.html:359-412](index.html#L359-L412), [index.html:563-593](index.html#L563-L593), [index.html:2526-2527](index.html#L2526-L2527) |
| 11 | Mantenibilidad | **Importante** | Duplicación estructural: cada proyecto está copiado dos veces en el DOM (una en `grid-all` y otra en su grid de filtro) en vez de filtrar con `data-category`; los bloques CSS `.projects-*` y `.products-*` son idénticos byte a byte; ~250 líneas de JS son bindings repetitivos uno-a-uno (`btnBackFromX`/`data-detail`) que una delegación de eventos con data-attributes reduciría a ~20 líneas. | [index.html:830-866](index.html#L830-L866), [index.html:244-305](index.html#L244-L305), [index.html:2713-2979](index.html#L2713-L2979) |
| 12 | Despliegue | **Importante** | Rutas de PDF con espacios, acentos, `º` y `ª` sin codificar (`href="1 INDUSTRIALES/…/00FALI30… 150º X 70º….pdf"`). En local funcionan (177/177 verificados), pero al subir a un hosting el encoding del servidor o un CDN pueden romperlas. Archivos que no deberían publicarse dentro del webroot: `index.html.zip`, `.DS_Store` (varios), `FAROLAS.rar`, `SALAS BLANCAS.rar`. | hrefs por todo el documento; raíz del repo |
| 13 | Performance | Menor | Google Fonts render-blocking sin `preconnect` a `fonts.gstatic.com`; `logo.png` pesa 117 KB (cabría en <10 KB como WebP/SVG); sin `loading="lazy"` posible porque no hay `<img>`. | [index.html:7](index.html#L7), [logo.png](logo.png) |
| 14 | Robustez JS | Menor | `updateNav()` mapea slides por índice posicional del nav (frágil si se añade un enlace); `goTo()` usa un `setTimeout(1450)` mágico acoplado a la duración CSS (1.3s); duplicar la duración en dos sitios invita a desincronización. | [index.html:2619-2643](index.html#L2619-L2643) |
| 15 | UX | Menor | Botón "Descargar catálogo" con `cursor: not-allowed` y opacidad 0.5 sin explicación; tarjetas "Próximamente" mezcladas con productos reales sin distinción visual; filtro "Nuevos Productos" muestra un único placeholder genérico. | [index.html:687](index.html#L687), [index.html:1306](index.html#L1306) |

---

## Recomendaciones de diseño

1. **Restaurar Catálogo y Contacto reutilizando el CSS existente.** El markup se puede reconstruir directamente contra las clases huérfanas: `.con-left` con el formulario (`.con-form`, `.con-row`, `.con-inp`, `.con-send`) y `.con-right` con los datos de contacto (`.con-list`, `.con-item`); `.cat-visual` con los libros (`.cat-books`) y `.cat-panel` con stats y CTA. Coste bajo, desbloquea las dos secciones del menú.
2. **Unificar la tipografía según la guía de marca.** Elegir: o se actualiza CLAUDE.md para oficializar Montserrat/Raleway, o se sustituyen los títulos por Cormorant Garamond 200-300 como dicta la guía. En cualquier caso, eliminar de la URL de Google Fonts las familias/pesos no usados (hoy se cargan 4 familias y ~15 variantes; el sitio funciona con 2 familias y 5-6 variantes).
3. **Sistema de escala tipográfica mínima de 11 px.** Sustituir los tamaños 0.44–0.58rem por un mínimo de 0.6875rem (11px) para metadatos y 0.75rem para labels interactivos, compensando con `letter-spacing` menor. Los textos en `#b0a898` que transmiten información (contadores, metas, breadcrumbs) deben pasar a `#6d5f52` o más oscuro para cumplir contraste 4.5:1; reservar `#b0a898` para decoración.
4. **Responsive por breakpoints.** Mínimo tres: `<640px` (nav hamburguesa, grids a 1 columna, paneles fijos a `width: 100%`, hero `clamp` ya lo soporta), `640-1024px` (grids a 2 columnas, dropdown convertido en acordeón táctil), `>1024px` (actual). Añadir swipe real en `touchend` (el esqueleto ya está escrito) y sustituir `100vh` por `100dvh`.
5. **Distinguir contenido futuro.** Tarjetas "Próximamente" con estilo propio (imagen desaturada + badge), y el botón de catálogo deshabilitado con un texto tipo "Disponible próximamente" en lugar de solo `cursor: not-allowed`.
6. **Recuperar la sidebar de marca o retirarla de la guía.** CLAUDE.md la da por hecha; el CSS existe pero el elemento no. Decidir y alinear código y documentación.

## Recomendaciones de funcionamiento / técnicas

1. **Sustituir picsum.photos por las fotos reales de `images/`.** Ya existen 64 fotos con nomenclatura que mapea a las referencias (`EST__`, `PROY__`, `CAMP__`, `FAR__`, `SB__`). Renombrarlas a slugs sin espacios (`est-00paes17w6k60.png`), comprimirlas a WebP (~100-200 KB máx.) y referenciarlas. Ningún placeholder debe llegar a producción.
2. **Diferir la carga de las vistas de detalle.** Cambiar el ocultamiento de `.product-detail-view` de `opacity: 0` a `display: none` (o añadir `content-visibility: hidden`), y aplicar la clase de visibilidad con la animación al abrir. Esto elimina ~231 descargas de imagen en el load inicial; con ello el LCP pasa de depender de 240 peticiones a ~4.
3. **Refactor del JS de paneles a delegación de eventos.** Un único listener en `document` que lea `data-open-panel` / `data-close-panel` sustituye ~250 líneas de bindings; los botones "back" ya llevan la información en el id. Elimina además el riesgo de `null.addEventListener` si se borra un panel del HTML.
4. **Deduplicar los grids de proyectos/productos.** Una sola lista de cards con `data-category`, y filtros que togglen `hidden` — elimina el doble DOM y el contador se calcula solo. Fusionar los bloques CSS `.projects-*`/`.products-*` en clases compartidas.
5. **SEO técnico básico.** Añadir: `<meta name="description">` (150-160 caracteres con "iluminación técnica y material eléctrico"), Open Graph (`og:title`, `og:description`, `og:image` con una foto real), favicon (derivado de logo.png), `robots.txt` y hash-routing (`#proyectos`, `#productos`, `#contacto`) sincronizado con `goTo()` para que las secciones sean enlazables y el botón atrás funcione.
6. **Higiene de despliegue.** Sacar del webroot `index.html.zip`, `.DS_Store`, `FAROLAS.rar` y `SALAS BLANCAS.rar`; renombrar las carpetas de PDFs a rutas sin espacios/acentos (o servirlas vía slugs), o como mínimo codificar los hrefs con `encodeURI`. Añadir headers de seguridad en el hosting (`X-Content-Type-Options`, `Referrer-Policy`, CSP básica) — al ser estático es solo configuración.
7. **Corregir el desajuste 70px/56px** unificando en una custom property (`--nav-h: 70px`) usada por `nav` y `.page-layout`.
8. **Fuentes:** añadir `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` y recortar la URL de Google Fonts a las variantes en uso; valorar `font-display: swap` (ya incluido vía `display=swap`, mantener).

## Quick wins (alto impacto, <1 h cada uno)

| Quick win | Impacto | Esfuerzo |
|---|---|---|
| Añadir CSS para `.product-card-body` y color legible a `.product-card-name` dentro de vistas de detalle | Arregla 48 vistas con nombres invisibles (hallazgo 2) | ~10 min |
| Restaurar el markup de Contacto (el CSS `.con-*` está completo) | Recupera la sección de mayor valor de negocio del sitio | ~30-45 min |
| Cambiar `.product-detail-view` oculto a `display: none` | Elimina ~231 descargas de imagen en el load inicial | ~15 min |
| `meta description` + favicon + Open Graph | SEO/compartibilidad inmediata | ~15 min |
| Unificar `--nav-h` (70px vs 56px) | Elimina los 14 px de contenido tapado en todas las secciones | ~5 min |
| Borrar `index.html.zip`, `.DS_Store`, `*.rar` del webroot | Higiene y peso del despliegue | ~5 min |
| `preconnect` a fonts.gstatic.com y quitar familias no usadas | Mejora FCP/LCP sin tocar diseño | ~10 min |
| Dar `href` real (`#seccion`) a los enlaces del nav | Primer paso de accesibilidad por teclado + URLs enlazables | ~20 min |

**Sugerencia de orden:** hallazgos 1-2 (bloqueantes visibles) → quick wins → imágenes reales (hallazgo 3) → responsive/móvil (hallazgo 4) → accesibilidad y SEO (5-7) → refactors de mantenibilidad (10-11).
