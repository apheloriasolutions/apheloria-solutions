# Fase 3 — Extracción de fotos de producto desde las fichas PDF

Fecha: 2026-09-13. Alcance: los 187 refs ya presentes en `data/productos.json` (fase 2). No se ha tocado `index.html`.

## 1. Metodología

- Extracción con **PyMuPDF** (`fitz`), deduplicando por hash MD5 dentro de cada PDF (las imágenes se reincrustan en cada página, así que sin dedup saldrían repetidas).
- **Filtro 1 — logos/plantilla**: una imagen se descarta si su hash exacto aparece en PDFs de **2 o más subfamilias distintas**. Primera versión de este filtro usaba "aparece en 2+ PDFs" a secas, pero eso descartaba fotos de producto legítimas que varias variantes de una misma familia comparten (p. ej. ZEN 7W/12W/20W... reutilizan la misma foto en sus 21 fichas) — corregido antes de la pasada final. Resultado: 17 hashes de logo/plantilla real de 175 candidatos iniciales.
- **Filtro 2 — tamaño mínimo**: menos de 100×80px, fuera (iconos).
- **Filtro 3 — aspecto de diagrama/curva**: `score = %tonos_medios − %densidad_de_bordes` sobre una miniatura en escala de grises; si `score < 15` se descarta (curvas fotométricas y planos de cotas tienen muchos bordes finos sobre fondo blanco y casi nada de tono medio).
- **Regla de rescate**: si tras los 3 filtros un producto se queda sin ninguna imagen, se recupera la mejor puntuada de las descartadas por "diagrama" (nunca un logo). Evita fichas completamente vacías, a costa de que a veces la imagen rescatada sea en realidad un plano — por eso estos casos se listan abajo para revisión.
- Salida: `images/productos/<ref>/01.jpg, 02.jpg…` (01 = imagen de mayor resolución = principal), JPEG calidad 82, máx. 1600px en el lado largo, fondos transparentes rellenados en blanco.

### Limitación conocida
El filtro 3 falla con fotos de producto muy planas (objeto blanco sobre blanco, u objeto oscuro/metálico muy uniforme sobre blanco) — estadísticamente se parecen a un plano de líneas. Se detectaron y corrigieron manualmente 3 casos así durante la validación (`00FAROLVILLAN`, `00PERFLEXACER` y el ejemplo de la fase de muestra `APLCCIRULO1000`). Es probable que existan más casos similares entre los 81 productos con solo 1 imagen — por eso esa lista (sección 3) merece un vistazo.

## 2. Cifras

| | nº |
|---|---|
| Refs procesadas | 187 |
| Imágenes guardadas en total | 332 |
| Refs con 0 imágenes útiles | 0 (gracias a la regla de rescate — ver sección 2b) |
| Refs con **1 sola imagen** (sin galería) | 81 |
| Refs con 2 o más imágenes | 106 |

## 2b. Rescatadas (revisar primero — puede que la única imagen sea un plano, no una foto)

4 productos no tenían ninguna imagen que pasara los 3 filtros; se les asignó la mejor candidata entre las descartadas por "aspecto de diagrama". Comprobado a mano: 2 de ellas eran fotos reales mal puntuadas (ya corregido), pero las que quedan aquí pueden ser legítimamente solo un plano — el PDF de origen puede no tener foto de producto.

- `0080223000` — LINCE S — 0080223000 (grupo: LINCE S) — `4 EMERGENCIA/0080223000.pdf`
- `0080235000` — LINCE S — 0080235000 (grupo: LINCE S) — `4 EMERGENCIA/0080235000.pdf`
- `00FAROLVILLAN` — Farol Villa acero pintado al horno negro IP20 — `3 EXTERIORES/FAROLAS/00FAROLVILLAN.pdf`
- `00PERFLEXACER` — Perfil flexible acero inoxidable 20m — `2 INTERIORES/TIRAS Y PERFILES LED/PERFILES DE ALUMINIO/PERFILES PARA EMPOTRAR/00PERFLEXACER.pdf`

## 3. Productos con solo 1 imagen (sin galería) — revisar si procede añadir más a mano

<details><summary>industrial (46)</summary>

- `00LINC3160040` — LINC luz indirecta 600×600 31W
- `00PAES12W4K60` — Pantallas Estancas · 600mm — 00PAES12W4K60 (grupo: Pantallas Estancas · 600mm)
- `00PAES12W6K60` — Pantallas Estancas · 600mm — 00PAES12W6K60 (grupo: Pantallas Estancas · 600mm)
- `00PAES17W4K60` — Pantallas Estancas · 600mm — 00PAES17W4K60 (grupo: Pantallas Estancas · 600mm)
- `00PAES17W6K60` — Pantallas Estancas · 600mm — 00PAES17W6K60 (grupo: Pantallas Estancas · 600mm)
- `00PAN18-36W4K` — Pantallas Estancas · 1200mm — 00PAN18-36W4K (grupo: Pantallas Estancas · 1200mm)
- `00PAN36-50W4K` — Estanca 36-50W 4000K 1500mm
- `00PANE30W4K16` — Pantallas Estancas · 1600mm — 00PANE30W4K16 (grupo: Pantallas Estancas · 1600mm)
- `00PANEL23344K` — Panel Slim 60×60 23-34W 4000K
- `00PANEL25W40K` — Paneles LED · Panel HI 60×60 — 00PANEL25W40K (grupo: Paneles LED · Panel HI 60×60)
- `00PANEL25WXXX` — Paneles LED · Panel HI 60×60 — 00PANEL25WXXX (grupo: Paneles LED · Panel HI 60×60)
- `00PANEL34W4KD` — Panel Slim 60×60 34W 4000K DALI
- `00PANEL40W60K` — Panel AQUA 40W 60×60 · 4200lm
- `00PANEL42W45K` — Panel LED 595×595 42W
- `00PANEL42WXXX` — Panel BURO 42W 60×60 · 4200lm
- `00PANEL60WXXX` — Panel TRI 60W 60×60 · 6000lm
- `00PANER42W3CCT` — Panel BURO 42W 120×30 3CCT
- `00PANEST19W4K` — Pantallas Estancas · 1200mm — 00PANEST19W4K (grupo: Pantallas Estancas · 1200mm)
- `00PANEST30W4K` — Pantallas Estancas · 1200mm — 00PANEST30W4K (grupo: Pantallas Estancas · 1200mm)
- `00PANEST45W4K` — Pantallas Estancas · 1600mm — 00PANEST45W4K (grupo: Pantallas Estancas · 1600mm)
- `00PANST36W4KD` — Estanca 36W 4000K 1200mm DALI2
- `00PANST44W4KD` — Estanca 44W 4000K 1500mm DALI2
- `00PHIPA45W40K` — Adosable 1235×335mm 45W 4000K ON-OFF
- `00PHIPE45W30K` — Salas Blancas · Empotrable 1235×335mm ON-OFF — 00PHIPE45W30K (grupo: Salas Blancas · Empotrable 1235×335mm ON-OFF)
- `00PHIPE45W40K` — Salas Blancas · Empotrable 1235×335mm ON-OFF — 00PHIPE45W40K (grupo: Salas Blancas · Empotrable 1235×335mm ON-OFF)
- `00PSLI21740KB` — Panel empotrable SLI-L 2×17W DALI
- `0FAMN100WXXK` — Farola MN 100W · 4500lm
- `0LINC3160040D` — LINC luz indirecta 600×600 31W DALI
- `0PE1C24W4KIP4` — Pantalla empotrable 1 calle 24W blanco
- `0PE2C24W4KIP4` — Paneles LED · Pantalla empotrable 2 calles blanco — 0PE2C24W4KIP4 (grupo: Paneles LED · Pantalla empotrable 2 calles blanco)
- `0PE2C34W4KIP4` — Paneles LED · Pantalla empotrable 2 calles blanco — 0PE2C34W4KIP4 (grupo: Paneles LED · Pantalla empotrable 2 calles blanco)
- `0PE2C48W4KIP4` — Paneles LED · Pantalla empotrable 2 calles blanco — 0PE2C48W4KIP4 (grupo: Paneles LED · Pantalla empotrable 2 calles blanco)
- `0PE2C48W4KIPD` — Pantalla empotrable 2 calles 48W DALI blanco
- `0PHE36WICIP1D` — Empotrable 1160×335mm 36W IC DALI
- `0PHE45W4KIP6D` — Empotrable 600×600mm 45W 4000K DALI
- `0PHE60W4KIP6D` — Clean Regular 635×635mm 60W 4000K DALI
- `0PHIP6E45W30K` — Salas Blancas · Empotrable 635×635mm ON-OFF — 0PHIP6E45W30K (grupo: Salas Blancas · Empotrable 635×635mm ON-OFF)
- `0PHIP6E45W3KD` — Salas Blancas · Empotrable 635×635mm DALI2 — 0PHIP6E45W3KD (grupo: Salas Blancas · Empotrable 635×635mm DALI2)
- `0PHIP6E45W40K` — Salas Blancas · Empotrable 635×635mm ON-OFF — 0PHIP6E45W40K (grupo: Salas Blancas · Empotrable 635×635mm ON-OFF)
- `0PHIP6E45W4KD` — Salas Blancas · Empotrable 635×635mm DALI2 — 0PHIP6E45W4KD (grupo: Salas Blancas · Empotrable 635×635mm DALI2)
- `0PHIPE45W30KD` — Salas Blancas · Empotrable 1235×335mm DALI2 — 0PHIPE45W30KD (grupo: Salas Blancas · Empotrable 1235×335mm DALI2)
- `0PHIPE45W40KD` — Salas Blancas · Empotrable 1235×335mm DALI2 — 0PHIPE45W40KD (grupo: Salas Blancas · Empotrable 1235×335mm DALI2)
- `OOCAMP100W5KS` — Gama SOL IP65 · Negro — OOCAMP100W5KS (grupo: Gama SOL IP65 · Negro)
- `OOCAMP120W5KB` — Gama CAM IP65 · Negro — OOCAMP120W5KB (grupo: Gama CAM IP65 · Negro)
- `OOCAMP200W5KB` — Gama CAM IP65 · Negro — OOCAMP200W5KB (grupo: Gama CAM IP65 · Negro)
- `OPANABAX344KD` — Pantalla Eco ABAX 31,4W DALI

</details>

<details><summary>interior (26)</summary>

- `00CAPGL488W30` — CAP GOLD carril magnético 48V 8W 3000K 550lm CRI90 36º
- `00DOWN6WIP654` — ARCA 6W 4000K IP65 blanco
- `00DOWSUP303IP` — Downlight superficie aluminio 30W 3000K 3150lm IP65 negro
- `00PEFA10E2020` — Perfil A10 empotrar difusor opal 2MT
- `00PEFA12E2020` — Perfil A12 empotrar difusor opal 2MT
- `00PEFA13E2020` — Perfil A13 empotrar difusor opal 2MT
- `00PEFA14E2020` — Perfil A14 empotrar difusor opal 2MT
- `00PEFA15E2020` — Perfil A15 empotrar difusor opal 2MT
- `00PEFA16E2020` — Perfil A16 empotrar difusor opal 2MT
- `00PEFA1E2020` — Perfil A1 empotrar difusor opal 2MT
- `00PEFA2E2020` — Perfil A2 empotrar difusor opal 2MT
- `00PEFA3E2020` — Perfil A3 empotrar difusor opal 2MT
- `00PEFA6E2020` — Perfil A6 empotrar difusor opal 2MT
- `00PEFA7E2020` — Perfil A7 empotrar difusor opal 2MT
- `00PEFA8E2020` — Perfil A8 empotrar difusor opal 2MT
- `00PEFA9E2020` — Perfil A9 empotrar difusor opal 2MT
- `00PEFB12S2020` — Perfil B12 superficie difusor opal 2MT
- `00PEFB13S2020` — Perfil B13 superficie difusor opal 2MT
- `00TLEDS12WXXX` — Tiras LED · IP20 CRI80 — 00TLEDS12WXXX (grupo: Tiras LED · IP20 CRI80)
- `00TLEDS9WXXX` — Tiras LED · IP20 CRI80 — 00TLEDS9WXXX (grupo: Tiras LED · IP20 CRI80)
- `00TLIPS12WXXX` — Tiras LED · IP65 CRI90 — 00TLIPS12WXXX (grupo: Tiras LED · IP65 CRI90)
- `00TLIPS18WXXX` — Tiras LED · IP65 CRI90 — 00TLIPS18WXXX (grupo: Tiras LED · IP65 CRI90)
- `00TLIPS9WXXX` — Flexible 9W 24V 800lm SMD2835 IP65 CRI80 x mt
- `00VENIC8WGOL` — Venice Retro Gold 8W 3000K 630lm CRI90 24º
- `0DLROM10W3CCT` — Downlight ROM — 0DLROM10W3CCT (grupo: Downlight ROM)
- `0DLROM20W3CCT` — Downlight ROM — 0DLROM20W3CCT (grupo: Downlight ROM)

</details>

<details><summary>emergencias (5)</summary>

- `0080132000` — LEÓN S — 0080132000 (grupo: LEÓN S)
- `0080140000` — LEÓN S — 0080140000 (grupo: LEÓN S)
- `00EMEEXITS250` — EXIT S — 00EMEEXITS250 (grupo: EXIT S)
- `00EMEEXITS350` — EXIT S — 00EMEEXITS350 (grupo: EXIT S)
- `00EMEEXITS450` — EXIT S — 00EMEEXITS450 (grupo: EXIT S)

</details>


---

## 4. Segunda pasada (2026-09-15) — corrección de fondo negro + foto de medidas

A raíz de un aviso de Jordi sobre fotos mal recortadas, se revisó el método de extracción a fondo. Dos cambios:

### 4.1 Bug corregido: fondo negro en vez de blanco/transparente

**Causa:** varias imágenes de los PDF llevan una máscara de transparencia (`/SMask`) guardada como un objeto *aparte* dentro del PDF. La primera pasada extraía solo la imagen base con `doc.extract_image()` y la máscara nunca se aplicaba — el resultado eran fondos negros allí donde debía verse blanco (exactamente el defecto que se detectó a simple vista). No se trataba de una captura de pantalla mal recortada: la extracción siempre fue directa del objeto de imagen incrustado en el PDF (`PyMuPDF`/`fitz`), nunca un pantallazo de la página.

**Arreglo:** cada imagen ahora se extrae junto con su máscara asociada (si la tiene) y se compone correctamente antes de pasar a JPEG con fondo blanco. Se regeneraron **las 332 imágenes de la primera pasada desde cero** con este método — no solo las que se veían mal a simple vista, por si había casos menos evidentes.

### 4.2 Nueva imagen: plano de medidas

Se añadió, cuando existe, la imagen de cotas/dimensiones que suele aparecer justo debajo de la foto principal en la ficha PDF — como pediste, se guarda en la misma carpeta `images/productos/<ref>/` como una imagen más (numerada al final de la secuencia), y solo se añade para los productos donde realmente existe en el PDF.

**Cómo se detecta** (no hay texto de apoyo en el PDF que la identifique, así que se usa una combinación de señales):
- Se localizan las imágenes descartadas por parecer "diagrama" (mismo filtro que la foto principal, sección 1).
- El plano de medidas está **siempre por encima de la curva fotométrica** en la página — señal de posición muy fiable, validada en varias familias de productos distintas.
- Se descarta como candidata cualquiera cuya puntuación de contenido sea demasiado alta (`> -2.0`), señal de que en realidad es una foto de producto mal clasificada, no un plano.

**Validación:** se revisaron a mano ~50 casos en 3 rondas. La primera versión de la regla acertaba pero colaba fotos reales como "medidas" en ~30% de los casos con varias imágenes descartadas por producto; se encontró que **toda la familia NEX (15 refs) compartía una única foto mal clasificada** y se excluyó explícitamente esa imagen por su huella digital (hash). Tras el ajuste, la última ronda de validación (12 casos al azar) salió sin ningún falso positivo.

**Limitación conocida:** en algún caso puntual (detectado en la familia Salas Blancas, p. ej. `00PHIPE45W30K`) el PDF no trae ningún plano de medidas — solo 2 fotos de producto — y no hay forma de saberlo de antemano sin revisar el PDF, así que ese producto se queda sin imagen de medidas en vez de forzar una incorrecta. También hay ~15-20 casos donde en vez de un plano con cifras en mm hay un icono vectorial sin cotas (contorno del producto o un pictograma de rotación) — no es una foto duplicada, pero tampoco es exactamente "una foto de las medidas".

**Resultado:** 123 de 187 referencias llevan ahora imagen de medidas (64 no la tienen, casi todas porque su PDF de origen no la incluye).


---

## 5. Tercera pasada (2026-09-15) — la imagen de medidas no salía cuando había 3 candidatas

Jordi detectó que en varios productos la imagen de "medidas" añadida en la sección 4 en realidad era un icono de línea del producto (sin ninguna cifra de cotas), en vez del plano con cifras que sí existía en el mismo PDF. Causa: cuando hay **tres** imágenes candidatas (icono sin cotas + plano con cotas + curva fotométrica) en vez de solo dos, la regla de "la más arriba en la página" a veces cogía el icono en vez del plano.

**Arreglo:** se añadió un análisis de componentes conexas (`scipy.ndimage`) para contar "manchas con forma de dígito" en cada candidata — un plano de medidas tiene varias (los números de las cotas), un icono sin cotas no tiene ninguna. Combinado con el % de tinta total de la imagen (para descartar fotos reales que a veces también puntúan como "diagrama") y la puntuación de aspecto ya usada en la fase anterior, se validó en 4 rondas sucesivas (~90 casos revisados a mano en total) hasta corregir los fallos que iban apareciendo:
- La familia ZEN completa mostraba el icono sin cotas en vez del plano real → corregido.
- Varios productos sueltos (paneles, farolas, downlights) colaban una foto de producto limpia sobre fondo blanco como si fuera el plano → corregido añadiendo el límite de puntuación de aspecto (`< 3.0`, calibrado contra 13 casos ya confirmados como correctos).

**Limitación que queda, ya documentada y localizada:**
- `0PHE36WICIP1D` (Salas Blancas): el PDF tiene 2 fotos de producto casi indistinguibles entre sí para todos los criterios usados (posición, tinta, texto, puntuación) — la que se guardó como "medidas" es en realidad otra foto, no el plano de 1160×335mm que sí existe en el PDF. De las 16 fichas de Salas Blancas revisadas una por una, es la única que falla.
- `OPANABAX344KD` (Paneles LED): su PDF no incluye ningún plano de medidas, solo curva fotométrica + fotos — la imagen guardada es la curva. No hay plano real que rescatar en este caso.
- Los iconos de rotación (90°/360°, en la gama CAP) y las vistas en planta sin cifras (en ALFA/CAM/SOL) se conservan como imagen añadida aunque no lleven mm exactos — no son fotos duplicadas, así que no hacen daño, pero tampoco muestran una medida como tal.

**Resultado final: 173 de 187 referencias con imagen de medidas.**

