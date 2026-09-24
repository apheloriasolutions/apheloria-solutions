# Auditoría del apartado "Productos" — index.html

Fecha: 2026-09-03. Solo lectura, no se ha modificado ningún archivo del sitio.
Fuente de datos completa: [`audit-productos.json`](./audit-productos.json) (285 objetos).

## 1. Cifras generales

| Métrica | Valor |
|---|---|
| Productos con ficha PDF enlazada (`product-card` + `product-variant-item`) | **285** |
| Paneles `.product-detail-view` de producto (excluye proyectos) | 63 (55 con productos propios, 8 son "hubs" de familia sin ficha directa) |
| PDFs en disco (`1 INDUSTRIALES…5 DECORATIVAS`, `BOMBILLAS Y ACCESORIOS`) | 287 |
| Enlaces rotos (href de ficha que no existe en disco) | **0** |
| PDFs huérfanos (existen en disco, ningún `product-card` los enlaza) | **2** |
| Con imagen real en `/images` | **63** (22%) |
| Con placeholder `picsum.photos` | **222** (78%) |

El recuento cuadra exactamente: 285 enlazados + 2 huérfanos = 287 PDFs en disco. No hay ninguna ficha referenciada en el HTML que falte físicamente.

### Reparto por categoría (`data-category`)

| categoría | productos | con imagen real | tarjetas de nivel superior en la grid |
|---|---|---|---|
| industrial | 105 | 63 (60%) | 6 |
| interior | 138 | 0 | 6 |
| exterior | 16 | 0 | 5 |
| emergencias | 19 | 0 | 11 |
| decorativas | 6 | 0 | 2 |
| bombillas | 1 | 0 | 1 |

**Dato relevante:** las 63 fotos reales que existen están *todas* dentro de Industrial (concretamente en Campanas, Estancas, Farolas y Salas Blancas). El resto de categorías — Interior con 138 productos incluido — siguen al 100% en `picsum.photos`. Si el criterio para sustituir placeholders es "por lotes", Industrial es el único lote terminado.

## 2. PDFs huérfanos (en disco, sin tarjeta que los enlace)

- `2 INTERIORES/DOWNLIGHTS EMPOTRADOS/00DNEX12W40K.pdf`
- `2 INTERIORES/PROYECTORES (Interiores)/Proyector LED 27W mod. CLIP 27-30-40K 2700lm CRI95 apertura 20º-50º.pdf`

Ambos en Interiores. Puede ser una ficha retirada intencionadamente o simplemente olvidada al montar el panel — habría que confirmarlo con el cliente/catálogo antes de decidir si se añade o se borra el PDF.

## 3. Enlaces rotos

Ninguno. Los 285 `href` de `product-card`/`product-variant-item` resuelven a un archivo existente.

## 4. Inconsistencias detectadas (sin corregir, solo señaladas)

### 4.1 Solapamiento real Industrial ↔ Exterior en "Farolas"
Dos productos están duplicados **con el mismo código de referencia** en dos categorías distintas, con el PDF físicamente repetido en dos carpetas:

- `00FAROLVILLAN` — "Farol Villa, acero negro IP20": vive en `industrial / detail-farolas-gen` (`1 INDUSTRIALES/FAROLAS/FAROLAS/00FAROLVILLAN.pdf`) **y** en `exterior / detail-ext-farolas` (`3 EXTERIORES/FAROLAS/00FAROLVILLAN.pdf`).
- `00MDVILLA50W4` — "Módulo LED Villa 50W": mismo patrón, `industrial / detail-farolas-gen` y `exterior / detail-ext-farolas`.

Es el mismo producto físico (mismo ref, nombre casi idéntico) mostrado dos veces bajo criterios de categoría distintos. Sugiere que "Farolas" nunca se decidió si es Industrial (viario/nave) o Exterior, y ambas fichas técnicas se duplicaron en disco para no tener que elegir.

### 4.2 Colisión de referencia (dato, no solapamiento de negocio)
`00PLAF22CCTIP` aparece dos veces con el **mismo código pero para dos productos completamente distintos**:

- `exterior / detail-ext-plafones`: "Plafón pared/techo 22W IP45 2500lm con emergencia 3H" (`3 EXTERIORES/PLAFONES/00PLAF22CCTIP- LEDWALLCIRC22W.pdf`)
- `interior / detail-int-lineales`: "Lineal aluminio adosar/suspender 30W" (`2 INTERIORES/LINEALES/00PLAF22CCTIP.pdf`)

Esto no es un problema de categorización sino de datos: el código de referencia se ha reutilizado por error para dos fichas distintas. Si `00PLAF22CCTIP` se usa alguna vez como clave (buscador, filtro, analítica), estos dos productos colisionarán.

### 4.3 Producto "Decorativo" cuya ficha vive en Interiores
`00LCEP644037W` — "Círculo 640 empotrable decorativa 37W 4000K" — está en `decorativas / detail-dec-suspendidas` ("Lámparas Suspendidas"), pero su PDF está archivado en `2 INTERIORES/DOWNLIGHTS EMPOTRADOS/LUZ DIFUSA/00LCEP644037W.pdf`. Por nombre y ubicación real del PDF es un downlight empotrable, no una lámpara suspendida — probablemente se coló en Decorativas por criterio estético ("es un círculo, es decorativo") en lugar de por tipo de instalación.

### 4.4 Emergencias no sigue el mismo criterio de agrupación que el resto
Industrial (105 productos) e Interior (138 productos) organizan la grid en **6 tarjetas de nivel superior** cada una, agrupando por familia/tipo de producto (Campanas, Estancas, Paneles… / Downlights, Tiras, Lineales…), con subfamilias anidadas debajo. Emergencias, con solo 19 productos, expone **11 tarjetas de nivel superior**, casi una por modelo comercial (`AXP 3.0`, `EXIT S`, `LEÓN S`, `LINCE S`, `Teide Slim`, `Omega`, `Proyector Vesubio`, `Microspot Empotrable`, `Autotest`…) en vez de agrupar por tipo (autónomos, alumbrado de señalización, kits de conversión, etc.). No es un error, pero rompe el patrón de information architecture del resto de "Productos" y hace que el filtro "Emergencias" se vea desproporcionadamente denso frente a Exterior (16 productos / 5 tarjetas) o Industrial.

### 4.5 Decorativas y Bombillas son categorías casi vacías
Decorativas: 6 productos / 2 tarjetas. Bombillas y Accesorios: 1 producto / 1 tarjeta. Ambas existen como filtro completo en el nav (`data-filter="decorativas"`, `data-filter="bombillas"`) pero el contenido real es mínimo porque las carpetas en disco también lo son (`5 DECORATIVAS` = 5 PDFs, `BOMBILLAS Y ACCESORIOS` = 1 PDF). No es un bug del HTML — es que falta material — pero visualmente da la impresión de una sección "vacía" comparada con Interior/Industrial. Merece una decisión de negocio: ¿se completan estas categorías con más referencias, o se ocultan/fusionan hasta tener más catálogo?

### 4.6 4 productos sin código de referencia visible
En `interior / detail-int-fuentes` ("Fuentes de Alimentación"), 4 fichas no muestran "Ref. XXXX" en su `product-card-meta` (solo dicen "Ver ficha técnica ↗"), a diferencia de los otros 281 productos que sí muestran referencia. Son las 4 fuentes de alimentación (`FUENTES-DE-ALIMENTACIÓN-24V-IP20-ON-O.pdf`, `…IP67…`, `…LIFUD…`, `…LIFUF…`). Probablemente no tienen código de fábrica asignado, pero rompe la consistencia visual/de datos del resto de la grid.

### 4.7 Nota aparte: recuento de paneles vs. CLAUDE.md
`Claude.md` describe "48 paneles de detalle con fichas PDF" en Productos. El recuento real de `.product-detail-view` de producto es 63 (55 con fichas propias + 8 "hubs" de familia sin ficha directa, como Campanas o Proyectores, que solo enlazan a subpaneles). No es una inconsistencia del código, solo un dato desactualizado en la documentación si en algún momento se quiere corregir esa cifra.

## 5. Opinión: ¿externalizar los datos de producto a JSON?

Para ~280 productos escritos a mano dentro de un único `index.html` de 352 KB, sí merece la pena separarlos a un JSON cargado por JS — pero con matices:

**A favor:**
- Cada producto es un objeto casi idéntico (ref, nombre, categoría, pdf, imagen) repetido 285 veces a mano; ahora mismo cualquier cambio de estructura (p. ej. añadir un campo "novedad" o corregir una categoría) implica editar HTML a mano 285 veces con altísimo riesgo de errores de copy-paste — de hecho ya hay dos ejemplos reales de eso en este audit (`00PLAF22CCTIP` duplicado, Farolas repetidas en dos categorías).
- Un JSON permite validar en build/CI (refs únicas, PDF existente, categoría válida) antes de publicar — habría detectado los hallazgos de este informe automáticamente.
- El HTML pasaría de ~350 KB a algo mucho más pequeño (markup + templating JS), mejorando el peso inicial de página aunque sea estático.

**En contra / a tener en cuenta:**
- El sitio es estático puro (GitHub Pages, sin build). Cargar 285 productos por `fetch()` de un JSON en el cliente añade una petición extra y un parpadeo (FOUC) si no se gestiona bien el render inicial — hay que decidir si se pre-renderiza en build time (necesitaría introducir un paso de build, aunque sea mínimo con Node) o se acepta el coste de render en cliente.
- Con 285 ítems el JSON pesará poco (unos 60-80 KB estimados), así que la ganancia de peso de red es modesta comparado con el beneficio de mantenibilidad.

**Recomendación:** sí, merece la pena, pero como paso de build simple (un script que lee `products.json` y genera el HTML estático de las grids/paneles antes de publicar) en lugar de fetch en cliente — así se mantiene "sin backend" y sin JS de render en el navegador, pero se elimina la edición manual repetitiva. Es un cambio de infraestructura no trivial y no se ha tocado nada en esta tarea; quedaría como una decisión aparte antes de abordar el resto de pendientes (fotos reales, email, PDF de catálogo).
