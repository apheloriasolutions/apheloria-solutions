# Apheloria Solutions — Landing Page

## Sobre la empresa
Especialistas en iluminación técnica y material eléctrico.
Más de 20 años de experiencia. No es e-commerce, es un escaparate.

## Stack
Sitio estático de un solo archivo (`index.html`, CSS y JS inline). Sin framework ni build.
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
- Scroll guiado por secciones con transición suave (slides con rutas #inicio…#contacto)
- Referencias: Agolar (agolar.eu), template Vanila de Framer

## Secciones
- Inicio ✅ (hero con slideshow + conector + Nosotros, scroll continuo)
- Proyectos ✅ (grid único con filtros por data-category)
- Productos ✅ (grid único con filtros + 48 paneles de detalle con fichas PDF)
- Catálogo ✅ (el PDF del catálogo general está pendiente; botón deshabilitado)
- Contacto ✅ (formulario vía mailto; **email/teléfono son placeholders — poner los reales**)

## Convenciones del código
- Los paneles de detalle se abren con `data-open="id-del-panel"` y se cierran con
  `data-close="id"` / `data-close-all` (delegación de eventos en `document`).
- Filtros: las cards llevan `data-category`; el filtrado oculta con el atributo `hidden`.
- Cards no disponibles: clase `is-soon` (badge "Próximamente" + imagen desaturada).
- Altura del nav en `--nav-h`; usar siempre esa variable, no valores sueltos.
- Paneles ocultos con `display:none` (no `opacity:0`) para no descargar sus imágenes.

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
- Email y teléfono reales en Contacto (buscar `TODO` en index.html) y en el JS
  (`CONTACT_EMAIL`). Valorar un servicio de formularios (Formspree o similar).
- PDF del catálogo general para activar el botón de descarga.
- Al desplegar: configurar headers de seguridad en el hosting y `og:image` con URL absoluta.
