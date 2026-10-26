# Apheloria Solutions — Landing Page

## Sobre la empresa
Especialistas en iluminación técnica y material eléctrico.
Más de 20 años de experiencia. No es e-commerce, es un escaparate.

## Stack
Sitio estático sin framework ni build: **una página HTML por apartado** (`index.html` = Inicio,
`proyectos.html`, `productos.html`, `catalogo.html`, `contacto.html`, más las tres legales).
El CSS y el JS viven en archivos compartidos:
- `css/estilos.css` (paleta, tipografía, nav, pie, botones) + uno por apartado:
  `inicio.css`, `listados.css` (Proyectos y Productos), `catalogo.css`, `contacto.css`, `legal.css`.
- `js/main.js` (menú, desplegable, apartado activo, redirección de enlaces antiguos) +
  `inicio.js`, `listados.js`, `contacto.js`.

Las fichas técnicas son PDFs en las carpetas `1 INDUSTRIALES/` … `5 DECORATIVAS/` y
`BOMBILLAS Y ACCESORIOS/`; las fotos de producto están en `images/` (el nombre incluye
el código de referencia, p. ej. `EST__00PAES17W6K60 - ….png`).

## Paleta de colores
- Fondo: #F2EDE4 (beige) — *nota: el hero y el nav usan blanco/oscuro; decidir si se unifica*
- Texto: #1a1612 (marrón oscuro)
- Acento decorativo: #b0a898 / #c8bfb0
- Acento para texto informativo (contraste AA): var(--accent-text) #857a68

## Tipografía
- Guía original: títulos Cormorant Garamond 200-300, texto Inter 300-400
- Estado actual del código: títulos en Montserrat 100-200 y Raleway; Cormorant solo en el
  logo del nav. **Decisión pendiente: unificar hacia la guía o oficializar Montserrat/Raleway.**

## Estilo
- Minimalista y elegante
- Scroll normal de página. El nav y el pie son barras fijas; `body` les reserva sitio con
  `padding-top: var(--nav-h)` y `padding-bottom: var(--footer-h)`.
- Referencias: Agolar (agolar.eu), template Vanila de Framer

## Secciones (una página cada una)
- Inicio ✅ (hero con slideshow + conector + Nosotros, uno detrás de otro)
- Proyectos ✅ (grid único con filtros por data-category)
- Productos ✅ (grid único con filtros + 48 paneles de detalle con fichas PDF)
- Catálogo ✅ (el PDF se descarga de catalogo/catalogo-apheloria.pdf; lo genera
  scripts/catalogo/construir_catalogo_completo.py)
- Contacto ✅ (formulario vía Web3Forms; email y teléfono reales confirmados: info@apheloria.es y 645 085 743)

## Convenciones del código
- Los paneles de detalle se abren con `data-open="id-del-panel"` y se cierran con
  `data-close="id"` / `data-close-all` (delegación de eventos en `document`).
- **Cada nivel tiene su dirección** y el botón atrás sube uno:
  `productos.html#industrial/campanas/cam` = filtro / familia / gama. Lo gestiona
  `js/listados.js`, que guarda el filtro y una pila de paneles, escribe la URL con
  `pushState` y la relee en `popstate`/`hashchange`. El id del panel sale del trozo de
  URL quitándole el prefijo `detail-` o `proj-`.
- Solo se muestra el último panel de la pila; el listado se oculta con `.listado[hidden]`.
- Filtros: las cards llevan `data-category`; el filtrado oculta con el atributo `hidden`.
- Cards no disponibles: clase `is-soon` (badge "Próximamente" + imagen desaturada).
- Altura del nav en `--nav-h` y del pie en `--footer-h`; usar siempre esas variables.
- Paneles ocultos con `display:none` (no `opacity:0`) para no descargar sus imágenes.
- Nada debe tener scroll propio salvo el menú móvil: los listados usan el scroll de la
  página. Si hiciera falta uno, darle barra fina (`scrollbar-width`/`scrollbar-color` y
  `::-webkit-scrollbar` con **width y height**): en Windows las barras ocupan sitio real
  y salen con el aspecto del sistema, en macOS se superponen y no se notan.

## Reglas
- Nunca usar negro puro, siempre #1a1612
- Sin bordes visibles entre secciones
- Imágenes siempre con hover effect
- Texto mínimo 0.6rem; el beige #b0a898 solo para decoración, nunca para texto informativo

## Productos: estructura y estado (sep-2026)
- La estructura de Productos sigue el Excel maestro CÓDIGOS GENERALES.xlsx:
  - Categoría = hoja "... TODO" (INDUSTRIAL TODO, INTERIORES TODO, EXTERIORES TODO, EMERGENCIA TODO).
  - Familia = títulos de la columna C de esa hoja (p. ej. CAMPANAS, ESTANCAS, PANELES, PROYECTORES, PANTALLAS SALAS BLANCAS, FAROLAS).
  - Gama = títulos de la columna Q dentro de cada familia (p. ej. ALFA, CAM, SOL). Las familias sin gamas llevan directamente a sus productos.
- Solo se publica lo que tiene ficha técnica en PDF. Lo que está en el Excel sin PDF (p. ej. la gama UFO, OOCAMU200W4KD) no se muestra.
- Las referencias de proveedor del Excel (LEDME, LEDSHOME, DELUXE, CELUX, OPPLE, GARMALUX...) nunca se publican, y el Excel no se sube a git.
- El nivel de ficha (lo que aparece al entrar en una gama) se queda de momento como está: enlaces a los PDF. Ahí irán en el futuro la tabla de características y las fotos. No se toca hasta que se pida.
- El trabajo de la migración anterior (scripts de extracción de tabla y fotos, informes, fotos extraídas) está archivado en ~/Downloads/Apheloria - archivo fases/ por si se reutiliza.
- **Pendiente con Samanta**: 92 productos publicados sin match en el Excel + 4 sin referencia; el detalle está en `~/Desktop/Apheloria - Códigos sin match en Excel.xlsx` y hay un borrador de correo en Gmail sin enviar (falta su email real y adjuntar el Excel).

## Pendientes (requieren decisión o material del cliente)
- Sustituir los ~209 placeholders restantes de picsum.photos (hero, portadas de categoría,
  fotos de proyectos) por fotografías reales — no deben llegar a producción.
- La portada del catálogo en PDF lleva otros datos (comercial@apheloria.es y
  +34 607 591 975); confirmar si es a propósito o si debe usar los de Contacto.
- Al desplegar: configurar headers de seguridad en el hosting y `og:image` con URL absoluta.
