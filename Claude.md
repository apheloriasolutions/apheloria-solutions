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

## Migración de fichas técnicas (en curso, sep-2026)

Proyecto en 4 fases para que "Productos" deje de depender de leer el PDF a mano: extraer datos
estructurados + fotos reales de las ~285 fichas técnicas actuales. **El HTML no se ha tocado
todavía** — todo vive en archivos de datos aparte, a la espera de una fase final de integración.

- **Fase 1 (auditoría)** → `docs/migracion-fichas/audit-productos.json` (ya corregido el `tch[`
  del inicio, es JSON válido) + `audit-resumen.md`. Inventario de los 285
  `product-card`/`product-variant-item` de hoy: PDF, imagen actual, duplicados.
- **Fase 2 (cruce + specs)** → `data/productos.json` (187 refs) + `matching-resumen.md`. Cruza
  esos 285 productos contra el Excel maestro `CÓDIGOS GENERALES.xlsx` (28 hojas, sin columnas de
  specs reales — todo es texto libre tipo `"REF - descripción con potencia/lúmenes/IP/CCT..."`,
  parseado con reglas). Dos tipos de entrada:
  - `"tipo": "producto"` — ficha suelta: `ref`, `nombre`, `categoria`, `subfamilia`, `panel_id`,
    `pdf_path`, `specs` (lista ordenada de `{etiqueta, valor}`), `imagenes`.
  - `"tipo": "grupo"` — cuando 2+ refs son el mismo producto con distinta potencia/CCT/acabado
    (encaja con el bloque HTML `product-variant-groups` que ya existe): `specs_resumen` (mismo
    formato pero `valores` es una lista) + `variantes` (cada una con su propio `pdf_path` y
    `imagenes` — 1 ficha-resumen, N PDFs individuales descargables). 29 grupos así detectados.
- **Fase 3 (fotos)** → `images/productos/<ref>/01.jpg, 02.jpg…` + `imagenes-resumen.md`.
  Extraídas directamente del objeto de imagen incrustado en el PDF con PyMuPDF (nunca captura de
  pantalla), aplicando la máscara de transparencia del PDF (si no, sale fondo negro en vez de
  blanco) y descartando logos/curvas fotométricas/planos técnicos de la galería de fotos. Se
  añade además, cuando existe, la imagen de cotas/medidas como última imagen de la carpeta —
  detectarla fue el punto más laborioso: ni el aspecto de la imagen ni su posición en la página
  bastan por sí solos, hizo falta contar "manchas con forma de dígito" (componentes conexas del
  tamaño de un carácter, vía `scipy.ndimage`) para diferenciarla de un icono sin cotas o de una
  foto de producto colada por error. 173/187 refs tienen esta imagen; limitaciones conocidas
  (una foto real de línea; una tumba fotométrica cuando no hay plano en el PDF) en
  `imagenes-resumen.md` sección 5.
- **Fase 4 (integración en HTML)** — **empezada 2026-09-24**: construida y validada la plantilla
  de ficha de producto individual (sustituye al PDF). Es **un único panel compartido**
  `#product-single` (`.product-detail-view.product-detail-view--sub`, insertado justo antes del
  cierre del slide Productos en `index.html`), NO 280 páginas estáticas — se repinta por JS según
  la ref recibida: `openProductDetail(ref)` (expuesta en `window` para pruebas) hace `fetch` a
  `data/productos.json` (una sola vez, cacheado en `productosDataPromise`), busca la ref con
  `findProductoByRef` (soporta tanto `tipo:"producto"` como una `variante` dentro de un `tipo:
  "grupo"`), pinta breadcrumb (`.pdb-crumb`/`data-close-all`, mismo patrón que el resto de paneles
  `--sub`), galería (foto principal + miniaturas clicables desde `imagenes`, `object-fit: contain`
  sobre fondo `--placeholder-bg` para no recortar fotos con proporciones raras), tabla de specs en
  su orden desde `specs`, y un botón que enlaza al PDF original (`pdf_path`, con cada segmento de
  ruta pasado por `encodeURIComponent` — los nombres de carpeta tienen espacios/tildes/º). Para una
  variante de grupo, el título añade automáticamente lo que varía respecto al resto (p. ej.
  "Downlight ZEN — 7W · 2700K · CRI90 · 70° · 160 mA") y se muestra una nota con el nº de variantes
  de la familia. **Las 280 tarjetas actuales todavía NO están enlazadas a esta vista** (eso es la
  fase 5) — solo existe la plantilla, probada con Playwright+Chromium (`openProductDetail('ref')`
  vía consola/`page.evaluate`, sin servidor de test permanente) en escritorio y móvil sobre 5 refs
  de categorías distintas. Hallazgos de esa prueba, ambos de **contenido** (fase 3), no de la
  plantilla: `OPANABAX344KD` tiene una curva fotométrica colada como su imagen 02 (debería haberse
  descartado); y en varias refs la foto 01 (elegida como "principal") es una foto de ambiente/
  aplicación en vez de un primer plano limpio del producto — la plantilla los muestra tal cual
  vienen de `data/productos.json`, sin filtrar de más. Pendiente decidir si se revisa la selección
  de fase 3 antes de la fase 5. Plan completo del resultado final en
  `~/Desktop/Apheloria - Plan Productos (estructura y fases).md`.

**Resuelto 2026-09-21**: "Punto 8" (texto suelto del Excel sin clasificar: `UGR19`, `"No fliker"`,
`"monocolor"`, `"difusor opal"`...) — se decidió guardarlo como specs propios, con su propia
etiqueta (no como nota de texto libre ni descartado). Se añadieron 88 specs nuevos sobre 70 de las
187 referencias (Difusor, Uso recomendado, Deslumbramiento (UGR), Tipo de color, Parpadeo, Chip
LED, Mantenimiento, Régimen de funcionamiento, Ajuste del ángulo, Tecnología, Vida útil (LED); más
`Regulación / control: DALI2` donde faltaba). Detalle completo en `matching-resumen.md` sección 8,
incluye también 3 errores de parseo corregidos de paso (potencias con coma decimal mal leídas en
`OPANABAX344KD` y `0PHEIPAS41W...KD`; un `Voltaje` duplicado/erróneo en `00CAPGL488W30`).

**Replanteamiento 2026-09-24 — la tabla sale del PDF, no del Excel.** El Excel maestro NO tiene la
tabla de características: solo el código, una descripción de una línea y referencias de proveedor
(estas **nunca se publican**). Por eso las fichas salían con 4 filas en vez de las ~20 del PDF. Ahora:

- `scripts/fichas/extraer_tabla.py` lee la tabla del PDF **por coordenadas**: las bandas beige
  alternas de la columna izquierda marcan la rejilla exacta de filas (incluidas las más altas, con
  etiqueta de varias líneas), y dentro de cada fila es etiqueta lo que empieza en el margen
  izquierdo. `extract_tables()` y el texto plano no sirven (la tabla no tiene líneas). Si una ficha
  no sigue la plantilla o está escaneada, se lista aparte: **nunca se inventan datos**.
- `scripts/fichas/leer_excel.py` solo aporta qué códigos son el mismo producto, los mA y las
  opciones múltiples.
- `scripts/fichas/construir_productos.py` genera **una ficha por producto real, no por código**:
  los códigos que son el mismo producto con distinta potencia/K/mA/acabado (p. ej. los 21 del ZEN)
  se fusionan en una sola tabla y los valores que cambian van separados por `" | "`
  (`7W | 12W | 20W...`, `2700K | 3000K | 4000K`, `160 mA | 350 mA...`). Debajo quedan todos sus PDF
  para descargar, cada uno etiquetado con lo que lo distingue ("20W · 3000K · 350 mA").
- `scripts/fichas/generar_json.py` escribe `data/productos.json` con una estructura única
  (`id, nombre, categoria, familia, refs[], specs[], imagenes[], descargas[], generada`) + el
  informe `docs/migracion-fichas/fichas-generadas.md`. **105 fichas generadas** (industrial e
  interior, 192 refs); exterior y emergencias siguen con la tabla antigua (`generada: false`).
- `scripts/fichas/generar_revision.py` regenera `revision-productos.html` (herramienta de trabajo,
  no forma parte del sitio): tabla arriba izquierda, fotos arriba derecha, PDF abajo izquierda.
- Las erratas de los PDF (`2 ños`, lúmenes en `lm/W`, potencias sin número...) **no se corrigen**:
  se anotan en `docs/migracion-fichas/erratas-pdf.md` para que las arregle el proveedor.
- Ojo al ampliar a más categorías: hay códigos publicados que solo están en hojas de familia
  (SALAS BLANCAS, PANELES, PROYECTORES, TIRAS LED...) y no en las hojas "TODO"; la categoría de
  esos se recupera de `audit-productos.json`.

**Pendientes antes de la fase 4** (detalle en `matching-resumen.md` e `imagenes-resumen.md`):
- 92 productos publicados sin match en el Excel + 4 sin referencia asignable (las "Fuentes de
  alimentación") — necesitan specs a mano. Incluye tanto refs "normales" no encontradas como el
  caso `00PLAF22CCTIP` de abajo. **2026-09-21**: se generó
  `~/Desktop/Apheloria - Códigos sin match en Excel.xlsx` con el detalle fila por fila (categoría,
  subfamilia, nombre, ref, ruta PDF) para que Samanta reasigne códigos y renombre PDFs; hay un
  borrador de correo en Gmail explicándolo, todavía sin enviar (pendiente poner su email real y
  adjuntar el Excel).
- Categorías **bombillas** y **decorativas**: 0% de match con el Excel, sin specs ni fotos reales
  en `data/productos.json` todavía (ya incluidas en el Excel de arriba).
- El código `00PLAF22CCTIP` aparece en dos PDFs distintos del repo (exterior: plafón 22W —
  correcto, coincide con el Excel maestro; interior: lineal de aluminio 30W — el archivo PDF está
  mal nombrado, copiado del plafón). **No es una corrupción de datos**: en `data/productos.json`
  solo existe la entrada del plafón (correcta); el lineal simplemente no tiene código real
  asignado en ningún sitio y quedó fuera del cruce — está incluido como caso especial en el Excel
  de Samanta de arriba, a la espera de que le asignen un código propio.

## Pendientes (requieren decisión o material del cliente)
- Sustituir los ~209 placeholders restantes de picsum.photos (hero, portadas de categoría,
  fotos de proyectos) por fotografías reales — no deben llegar a producción.
- Email y teléfono reales en Contacto (buscar `TODO` en index.html) y en el JS
  (`CONTACT_EMAIL`). Valorar un servicio de formularios (Formspree o similar).
- PDF del catálogo general para activar el botón de descarga.
- Al desplegar: configurar headers de seguridad en el hosting y `og:image` con URL absoluta.
