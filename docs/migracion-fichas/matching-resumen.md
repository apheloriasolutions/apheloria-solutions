# Fase 2 — Cruce Excel "CÓDIGOS GENERALES.xlsx" ↔ productos publicados

Fecha: 2026-09-11. Solo lectura y análisis — no se ha tocado `index.html` ni ningún PDF.
Fuente 1: `audit-productos.json` (fase 1, 285 fichas publicadas).
Fuente 2: `CÓDIGOS GENERALES.xlsx` (28 hojas — ver metodología).

## 0. Dos avisos previos sobre las fuentes

1. `audit-productos.json` empieza con `tch[` en vez de `[` (3 caracteres sobrantes) y no es JSON válido tal cual está en disco — se ha leído ignorando ese prefijo. Sigue pendiente corregirlo.
2. **4 productos de `audit-productos.json` tienen `"ref": null`** (todos en Fuentes de Alimentación, interior): no llevan código de referencia porque el PDF no tiene un código corto en el nombre de archivo. Sin ref no hay forma de cruzarlos con el Excel — quedan fuera de este análisis y se listan en el punto 6. Habría que decidir un código para ellos antes de la fase 3.

## 1. Metodología

- El Excel **no tiene columnas de especificaciones separadas** (lúmenes, potencia, IP, CCT...). Cada hoja reparte el código letra a letra en celdas individuales y mete referencia + specs en **una sola celda de texto libre** (p. ej. `"OOCAMP100W4KA - Campana... 60-80-100W ...4000K 1-10V IP65 negro."`).
- La referencia real y fiable es la que aparece **dentro de ese texto libre** (antes del primer `" - "`), no el código repartido letra a letra — se encontró al menos un caso (`DECORATIVAS SOBREPONER`, fila 5) donde ambos códigos no coinciden porque la fila se copió de una plantilla sin actualizar las celdas letra a letra.
- Se recorrieron las 28 hojas (excepto `Hoja1` y `HOJAS DELANTERAS`, sin datos de producto) y se descartaron 113 filas que resultaron ser cabeceras de sección (p. ej. "SLIM", "TIRA", "FAROLA") en vez de códigos de producto, filtrando por "el candidato a ref debe contener al menos un dígito".
- Cuando un ref aparece en una hoja "TODO" (resumen por categoría) y también en su hoja de familia específica, se usa la hoja de familia como fuente canónica.
- Normalización de referencia para el cruce: mayúsculas, sin espacios/guiones/puntos/barras bajas (`00-DL-NEX 07W` y `00DLNEX07W` casan igual).
- Specs: se parsean con reglas por patrón (regex) sobre el texto libre — potencia, lúmenes, temperatura de color (incluye listas tipo `2700K-3200K-4000K`), IP, IK, CRI, ángulo, mA, mm, V, autonomía (h), regulación/control (DALI, 0-10V, 1-10V, ON-OFF, Autotest...), acabado. El orden de los pares en cada producto es el **orden de aparición en el texto** (no hay "orden de columnas" porque no hay columnas de specs). Lo que el parser no reconoce se conserva aparte para poder revisarlo — nunca se descarta en silencio.

## 2. Cifras

| | nº |
|---|---|
| Refs únicas válidas en `audit-productos.json` (285 fichas, 4 sin ref) | 278 |
| Refs únicas válidas encontradas en el Excel | 367 |
| **Match** (publicado + en Excel) → van a `data/productos.json` | **187** |
| Publicado en la web, SIN fila en el Excel | 91 |
| Fila en el Excel, SIN producto publicado | 180 |
| Refs con descripciones contradictorias entre hojas del Excel | 9 |

## 3. Productos con match (187) — van a `data/productos.json`

| categoría | nº con match |
|---|---|
| interior | 90 |
| industrial | 70 |
| emergencias | 17 |
| exterior | 10 |

<details><summary>interior (90)</summary>

- `00CAPGL488W30` — CAP GOLD carril magnético 48V 8W 3000K 550lm CRI90 36º
- `00CARD20W3KBL` — Cardan CAR blanco 20W 3000K 2540lm CRI90
- `00DLZEN07W27X` — ZEN 7W 2700K 70º
- `00DLZEN07W30X` — ZEN 7W 3000K 70º
- `00DLZEN07W40X` — ZEN 7W 4000K 70º
- `00DLZEN12W27X` — ZEN 12W 2700K 70º
- `00DLZEN12W30X` — ZEN 12W 3000K 70º
- `00DLZEN12W40X` — ZEN 12W 4000K 70º
- `00DLZEN20W27X` — ZEN 20W 2700K 70º
- `00DLZEN20W30X` — ZEN 20W 3000K 70º
- `00DLZEN20W40X` — ZEN 20W 4000K 70º
- `00DLZEN25W27X` — ZEN 25W 2700K 70º
- `00DLZEN25W30X` — ZEN 25W 3000K 70º
- `00DLZEN25W40X` — ZEN 25W 4000K 70º
- `00DLZEN30W27X` — ZEN 30W 2700K 70º
- `00DLZEN30W30X` — ZEN 30W 3000K 70º
- `00DLZEN30W40X` — ZEN 30W 4000K 70º
- `00DLZEN40W27X` — ZEN 40W 2700K 70º
- `00DLZEN40W30X` — ZEN 40W 3000K 70º
- `00DLZEN40W40X` — ZEN 40W 4000K 70º
- `00DLZEN50W27X` — ZEN 50W 2700K 70º
- `00DLZEN50W30X` — ZEN 50W 3000K 70º
- `00DLZEN50W40X` — ZEN 50W 4000K 70º
- `00DO40W30N` — NIX orientable 40W 3000K CRI95 40º negro
- `00DOMIN12WB` — MIN 12W 1440lm 2700-3200-4000K IP65
- `00DOMIN1OWB` — MIN 10W 1000lm 2700-3200-4000K IP65
- `00DOWDALI254K` — DIA 25W 4000K 2750lm IP44 blanco
- `00DOWN6WIP654` — ARCA 6W 4000K IP65 blanco
- `00DOWSUP303IP` — Downlight superficie aluminio 30W 3000K 3150lm IP65 negro
- `00DTBIO49W27K` — BIO40 trimless 9.2W 2700K 32º UGR10 ON-OFF
- `00MOTA10WGL3` — MOTA spot gold 10W 36º 760lm 3000K CRI90
- `00PEFA10E2020` — Perfil A10 empotrar difusor opal 2MT
- `00PEFA11E2020` — Perfil A11 empotrar difusor opal 2MT
- `00PEFA12E2020` — Perfil A12 empotrar difusor opal 2MT
- `00PEFA13E2020` — Perfil A13 empotrar difusor opal 2MT
- `00PEFA14E2020` — Perfil A14 empotrar difusor opal 2MT
- `00PEFA15E2020` — Perfil A15 empotrar difusor opal 2MT
- `00PEFA16E2020` — Perfil A16 empotrar difusor opal 2MT
- `00PEFA1E2020` — Perfil A1 empotrar difusor opal 2MT
- `00PEFA2E2020` — Perfil A2 empotrar difusor opal 2MT
- `00PEFA3E2020` — Perfil A3 empotrar difusor opal 2MT
- `00PEFA4E2020` — Perfil A4 empotrar difusor opal 2MT
- `00PEFA4E2020B` — Perfil A4 empotrar difusor opal 2MT · Blanco
- `00PEFA4E2020N` — Perfil A4 empotrar difusor opal 2MT · Negro
- `00PEFA5E2020` — Perfil A5 empotrar difusor opal 2MT
- `00PEFA5E2020B` — Perfil A5 empotrar difusor opal 2MT · Blanco
- `00PEFA5E2020N` — Perfil A5 empotrar difusor opal 2MT · Negro
- `00PEFA6E2020` — Perfil A6 empotrar difusor opal 2MT
- `00PEFA7E2020` — Perfil A7 empotrar difusor opal 2MT
- `00PEFA8E2020` — Perfil A8 empotrar difusor opal 2MT
- `00PEFA9E2020` — Perfil A9 empotrar difusor opal 2MT
- `00PEFB12S2020` — Perfil B12 superficie difusor opal 2MT
- `00PEFB13S2020` — Perfil B13 superficie difusor opal 2MT
- `00PERFLEXACER` — Perfil flexible acero inoxidable 20m
- `00PROCA10W30B` — CAP LED 10W 3000K 1145lm CRI95 36º blanco
- `00PROCA20W30B` — CAP LED 20W 3000K 2290lm CRI95 36º blanco
- `00PROCA20W30N` — CAP LED 20W 3000K 2290lm CRI95 36º negro
- `00PROCA20W40B` — CAP LED 20W 4000K 2290lm CRI95 36º blanco
- `00PROCA20W40N` — CAP LED 20W 4000K 2290lm CRI95 36º negro
- `00PROCA30W30B` — CAP LED 30W 3000K 3470lm CRI95 36º blanco
- `00PROCA30W30N` — CAP LED 30W 3000K 3470lm CRI95 36º negro
- `00PROCA30W40B` — CAP LED 30W 4000K 3470lm CRI95 36º blanco
- `00PROCA30W40N` — CAP LED 30W 4000K 3470lm CRI95 36º negro
- `00TLEDC12WXXX` — TIP COB 12W 24V 1200lm IP20 CRI90 x mt
- `00TLEDC13WXXX` — TIP COB corte libre 13W 24V 1200lm IP20 CRI90 x mt
- `00TLEDS12WXXX` — Flexible 12W 24V 1140lm SMD2835 IP20 CRI80 x mt
- `00TLEDS9WXXX` — Flexible 9W 24V 800lm SMD2835 IP20 CRI80 x mt
- `00TLIPC13WXXX` — TIP COB corte libre 13W 24V 1200lm IP65 CRI90 x mt
- `00TLIPS12WXXX` — Flexible 12W 24V 1200lm SMD2835 IP65 CRI90 x mt
- `00TLIPS18WXXX` — Flexible 18W 24V 1800lm SMD2835 IP65 CRI90 x mt
- `00TLIPS9WXXX` — Flexible 9W 24V 800lm SMD2835 IP65 CRI80 x mt
- `00VENIC8WGOL` — Venice Retro Gold 8W 3000K 630lm CRI90 24º
- `0DLNEX07W30BB` — NEX 7W 3000K 60º blanco
- `0DLNEX07W30BN` — NEX 7W 3000K 60º negro
- `0DLNEX07W40BB` — NEX 7W 4000K 60º blanco
- `0DLNEX07W40BN` — NEX 7W 4000K 60º negro
- `0DLNEX12W30BB` — NEX 12W 3000K 60º blanco
- `0DLNEX12W30BN` — NEX 12W 3000K 60º negro
- `0DLNEX12W40BB` — NEX 12W 4000K 60º blanco
- `0DLNEX12W40BN` — NEX 12W 4000K 60º negro
- `0DLNEX20W30BB` — NEX 20W 3000K 60º blanco
- `0DLNEX20W30BN` — NEX 20W 3000K 60º negro
- `0DLNEX20W40BB` — NEX 20W 4000K 60º blanco
- `0DLNEX20W40BN` — NEX 20W 4000K 60º negro
- `0DLNEX25W30BN` — NEX 25W 3000K 60º negro
- `0DLNEX25W40BB` — NEX 25W 4000K 60º blanco
- `0DLNEX25W40BN` — NEX 25W 4000K 60º negro
- `0DLROM10W3CCT` — ROM 10W CCT ajustable IP44 blanco
- `0DLROM20W3CCT` — ROM 20W CCT ajustable IP44 blanco
- `0DTBIO49W27KD` — BIO40 trimless 9.2W 2700K 32º UGR10 DALI

</details>

<details><summary>industrial (70)</summary>

- `0030512440` — Estanca SLE-T 1200mm 24W IP66
- `0031413540` — Estanca Integrado 1175mm 35W IP65 IK08
- `00FALI30WXXXK` — Farola LI 30W · 4200lm
- `00FALI60WXXXK` — Farola LI 60W · 4200lm
- `00FALI90WXXXK` — Farola LI 90W · 12600lm
- `00FASOH16WCCT` — Solar 16W · 6000lm
- `00FASOH20WCCT` — Solar Híbrida 20W · 9000lm
- `00FAST30WXXXK` — Farola ST 30W · 4500lm
- `00FAST60WXXXK` — Farola ST 60W · 9000lm
- `00FAST90WXXXK` — Farola ST 90W · 13500lm
- `00FAVA60WXXXK` — Farola VA 60W · 6900lm
- `00LINC3160040` — LINC luz indirecta 600×600 31W
- `00PAES12W4K60` — Estanca 12W 4000K 600mm
- `00PAES12W6K60` — Estanca 12W 6000K 600mm
- `00PAES17W4K60` — Estanca 17W 4000K 600mm
- `00PAES17W6K60` — Estanca 17W 6000K 600mm
- `00PAN18-36W4K` — Estanca 18-36W 4000K 1200mm
- `00PAN36-50W4K` — Estanca 36-50W 4000K 1500mm
- `00PANE30W4K16` — Estanca 30W 4000K 1600mm
- `00PANEL23344K` — Panel Slim 60×60 23-34W 4000K
- `00PANEL25W40K` — Panel HI 25W 60×60 4000K
- `00PANEL25WXXX` — Panel HI 25W 60×60 · 4500lm
- `00PANEL34W4KD` — Panel Slim 60×60 34W 4000K DALI
- `00PANEL40W60K` — Panel AQUA 40W 60×60 · 4200lm
- `00PANEL42W45K` — Panel LED 595×595 42W
- `00PANEL42WXXX` — Panel BURO 42W 60×60 · 4200lm
- `00PANEL60WXXX` — Panel TRI 60W 60×60 · 6000lm
- `00PANER42W3CCT` — Panel BURO 42W 120×30 3CCT
- `00PANEST19W4K` — Estanca 19W 4000K 1200mm
- `00PANEST30W4K` — Estanca 30W 4000K 1200mm
- `00PANEST45W4K` — Estanca 45W 4000K 1600mm
- `00PANST36W4KD` — Estanca 36W 4000K 1200mm DALI2
- `00PANST44W4KD` — Estanca 44W 4000K 1500mm DALI2
- `00PHIPA45W40K` — Adosable 1235×335mm 45W 4000K ON-OFF
- `00PHIPE45W30K` — Empotrable 1235×335mm 45W 3000K ON-OFF
- `00PHIPE45W40K` — Empotrable 1235×335mm 45W 4000K ON-OFF
- `00PSLI21740KB` — Panel empotrable SLI-L 2×17W DALI
- `0FAMN100WXXK` — Farola MN 100W · 4500lm
- `0LINC3160040D` — LINC luz indirecta 600×600 31W DALI
- `0PE1C24W4KIP4` — Pantalla empotrable 1 calle 24W blanco
- `0PE2C24W4KIP4` — Pantalla empotrable 2 calles 24W blanco
- `0PE2C34W4KIP4` — Pantalla empotrable 2 calles 34W blanco
- `0PE2C48W4KIP4` — Pantalla empotrable 2 calles 48W blanco
- `0PE2C48W4KIPD` — Pantalla empotrable 2 calles 48W DALI blanco
- `0PHE36WICIP1D` — Empotrable 1160×335mm 36W IC DALI
- `0PHE45W4KIP6D` — Empotrable 600×600mm 45W 4000K DALI
- `0PHE60W4KIP6D` — Clean Regular 635×635mm 60W 4000K DALI
- `0PHEIPAS41W30KD` — Acceso superior 600×600mm 41,6W 3000K DALI2
- `0PHEIPAS41W40KD` — Acceso superior 600×600mm 41,6W 4000K DALI2
- `0PHEIPAS65W30KD` — Acceso superior 630×630mm 65W 3000K DALI2
- `0PHEIPAS65W40KD` — Acceso superior 630×630mm 65W 4000K DALI2
- `0PHIP6E45W30K` — Empotrable 635×635mm 45W 3000K ON-OFF
- `0PHIP6E45W3KD` — Empotrable 635×635mm 45W 3000K DALI2
- `0PHIP6E45W40K` — Empotrable 635×635mm 45W 4000K ON-OFF
- `0PHIP6E45W4KD` — Empotrable 635×635mm 45W 4000K DALI2
- `0PHIPE45W30KD` — Empotrable 1235×335mm 45W 3000K DALI2
- `0PHIPE45W40KD` — Empotrable 1235×335mm 45W 4000K DALI2
- `OOCAMP100W4KA` — ALFA 100W 4000K · hasta 18000lm
- `OOCAMP100W5KA` — ALFA 100W 5000K · regulable
- `OOCAMP100W5KS` — SOL 100W 5000K · hasta 14000lm
- `OOCAMP120W5KB` — CAM 120W 5000K · 15600lm
- `OOCAMP150W4KA` — ALFA 150W 4000K · hasta 27000lm
- `OOCAMP150W5KA` — ALFA 150W 5000K · hasta 27000lm
- `OOCAMP200W4KA` — ALFA 200W 4000K · hasta 36000lm
- `OOCAMP200W5KA` — ALFA 200W 5000K · hasta 36000lm
- `OOCAMP200W5KB` — CAM 200W 5000K · 26000lm
- `OOCAMP200W5KS` — SOL 200W 5000K · hasta 28000lm
- `OOCAMP300W4KA` — ALFA 300W 4000K · 54000lm
- `OOCAMP300W5KA` — ALFA 300W 5000K · 54000lm
- `OPANABAX344KD` — Pantalla Eco ABAX 31,4W DALI

</details>

<details><summary>emergencias (17)</summary>

- `0080132000` — LEÓN S 320lm IP42 superficie Autotest
- `0080140000` — LEÓN S 400lm IP42 superficie Autotest
- `0080223000` — LINCE S 230lm IP65 superficie Autotest
- `0080235000` — LINCE S 350lm IP65 superficie Autotest
- `0081320001` — Teide Slim 200lm IP20 Autotest
- `0081518000` — Proyector Vesubio 1800lm IP65
- `0081920002` — Omega 200lm IP65 lente antipánico
- `00EMEAXP3.01W` — AXP 3.0 espacios abiertos 1W 250lm IP20 1h no permanente
- `00EMEAXP3.0AT` — AXP 3.0 espacios abiertos 1W 250lm IP20 1h no permanente Autotest
- `00EMEAXP3.0RE` — AXP 3.0 recorrido evacuación 1W 250lm IP20 1h no permanente
- `00EMEEXITS150` — EXIT S superficie 150lm 1h IP65 no permanente difusor opal
- `00EMEEXITS250` — EXIT S superficie 250lm 1h IP65 no permanente difusor opal
- `00EMEEXITS350` — EXIT S superficie 350lm 1h IP65 no permanente difusor opal
- `00EMEEXITS450` — EXIT S superficie 450lm 1h IP65 no permanente difusor opal
- `00EMEMCSPO25` — Microspot empotrable 1W 250lm Eco IP20 óptica U
- `00EMER270IP42` — Emergencia 270lm IP42 superficie Autotest
- `00EMGEXITS200` — EXIT S superficie 200lm 1h IP65 no permanente difusor opal

</details>

<details><summary>exterior (10)</summary>

- `0043814440` — Villalba Maxi circular empotrar 44W blanco
- `0070211540` — Aplique superficie circular SAJ-6000 15W
- `00APL12WCCTIP` — Aplique cubo 12W CCT IP54 1200lm Up/Downlight ángulo regulable
- `00BALIZ8W3KIP` — Baliza bolardo 8W 3000-4000K 1000mm regulación Triac
- `00FAROLVILLAN` — Farol Villa acero pintado al horno negro IP20
- `00PLAF22CCTIP` — Plafón pared/techo 22W IP45 2500lm con emergencia 3H
- `00PLAFIP6512W` — Plafón superficie IP65 12-15-18-24W CCT
- `00PLAFON500DA` — Plafón superficie 500mm 4000K DALI 40W blanco
- `00PML12WIP65N` — Plafón MARS 12-18-24W CCT negro
- `00PML20WIP65N` — Plafón MARS 20W CCT negro

</details>

## 4. Publicados en la web SIN fila en el Excel (92) — requieren decisión manual

No se encontró ninguna fila en el Excel (con ningún criterio de normalización) para estas referencias. Puede ser porque el producto es nuevo y aún no está en el maestro de códigos, porque el código cambió, o porque en el Excel el texto no sigue el patrón `"REF - descripción"` esperado. Antes de dejarlas sin specs habría que revisarlas una a una.

<details><summary>interior (43)</summary>

- `0043910540` — ARCADIA 5W 4000K IP54 blanco
- `00CARD60W40KB` — Cardan triple 60W 4000K IP20 500mm
- `00CONTROLADOR` — Controlador Smart RF433+ Tuya WiFi monocolor CCT RGB
- `00DLEP30W30N` — PLANET orientable 30W 4000K CRI95 40º negro
- `00DOWN7WIP65` — Downlight difuso 7W SMD2835 IP65 · 574lm
- `00DWN15WIP654` — ARCA 15W 4000K IP65 blanco
- `00MANDOCOTR` — Mando a distancia RF 2.4GHz monocolor CCT RGB
- `00NDPRO` — Equipo lineal compacto
- `00PEFA11E2020B` — Perfil A11 empotrar difusor opal 2MT · Blanco
- `00PEFA11E2020N` — Perfil A11 empotrar difusor opal 2MT · Negro
- `00PEFB10S2020` — Perfil B10 superficie difusor opal 2MT
- `00PEFB11S2020` — Perfil B11 superficie difusor opal 2MT
- `00PEFB14S2020` — Perfil B14 superficie difusor opal 2MT
- `00PEFB15S2020` — Perfil B15 superficie difusor opal 2MT
- `00PEFB16S2065` — Perfil B16 superficie difusor opal 2MT IP65
- `00PEFB1S2020` — Perfil B1 superficie difusor opal 2MT
- `00PEFB2S2020` — Perfil B2 superficie difusor opal 2MT
- `00PEFB3S2020` — Perfil B3 superficie difusor opal 2MT
- `00PEFB4S2020` — Perfil B4 superficie difusor opal 2MT
- `00PEFB5S2020` — Perfil B5 superficie difusor opal 2MT
- `00PEFB6S2020` — Perfil B6 superficie difusor opal 2MT
- `00PEFB7S2020` — Perfil B7 superficie difusor opal 2MT
- `00PEFB8S2020` — Perfil B8 superficie difusor opal 2MT
- `00PEFB9S2020` — Perfil B9 superficie difusor opal 2MT
- `00PERALU40WCC` — Lineal aluminio adosar/suspender 24W 4000K 1200mm
- `00PERALUE30W40B` — Lineal aluminio empotrar 30W 4000K 250mA 1410mm IP40
- `00PROCAXXWXXX` — CAP para carril CRI95
- `00PROCLIP2730B` — CLIP 27W 2700-3000-4000K 2700lm CRI95 20-50º blanco
- `00PROCLIP2730N` — CLIP 27W 2700-3000-4000K 2700lm CRI95 20-50º negro
- `00PROMODE30W40K` — MODEN 30W 3460lm 4000K CRI95 40º negro
- `00PROMODE40WXK` — MODEN 40W 4450lm CRI95 negro
- `00PROPIC10W30B` — PIC LED 10W 3000K 600lm CRI92 36º blanco
- `00PROPIC10W30N` — PIC LED 10W 3000K 600lm CRI92 36º negro
- `00PROPIC15W30B` — PIC LED 15W 3000K 890lm CRI92 36º blanco
- `00PROPIC15W30N` — PIC LED 15W 3000K 890lm CRI92 36º negro
- `00TLEDS24WXXX` — Flexible 24W 24V SMD2216 IP20 CRI90 x mt
- `00TLRGB12WXXX` — Flexible RGB 12W 24V SMD3535 IP20 CRI80 x mt
- `00TRGBI12WXXX` — Flexible RGB 12W 24V SMD3535 IP65 CRI80 x mt
- `0DEOCU15W30KB` — OCU orientable 15W 2400lm 3000K IP20 blanco
- `0DEWWL10W40BD` — LINK wall washer 10W 4000K DALI blanco
- `0DMIXE10WCCTB` — MIX wall washer 10W CCT multivoltaje blanco
- `0DTBI612W27KD` — BIO60 trimless 12.8W 2700K 42º UGR10 DALI
- `0DZE1820W40BD` — ZEN Ø185mm 20W 4000K DALI blanco

</details>

<details><summary>industrial (33)</summary>

- `0072701500` — BABILOM 150W CCT · superficie rectangular
- `00FALG50WXXXK` — Farola LG 50W · 4500lm
- `00FASOJY20WXXK` — Solar JY 20W · 3000lm
- `00PREX100W3KB` — PAR 100W 3000K · 11000lm
- `00PREX100W4KB` — PAR 100W 4000K · 11000lm
- `00PREX100W4KS` — SLIM 100W 4000K · 14000lm
- `00PREX100W5KS` — SLIM 100W 5000K · 14000lm
- `00PREX100W6KB` — PAR 100W 6000K · 11000lm
- `00PREX150W3KB` — PAR 150W 3000K · 16500lm
- `00PREX150W4KB` — PAR 150W 4000K · 16500lm
- `00PREX150W4KS` — SLIM 150W 4000K · 21000lm
- `00PREX150W5KS` — SLIM 150W 5000K · 21000lm
- `00PREX150W6KB` — PAR 150W 6000K · 16500lm
- `00PREX200W4KS` — SLIM 200W 4000K · 28000lm
- `00PREX200W5KS` — SLIM 200W 5000K · 28000lm
- `00PREX300W4KS` — SLIM 300W 4000K · 42000lm
- `00PREX300W5KS` — SLIM 300W 5000K · 42000lm
- `00PREX50W3KB` — PAR 50W 3000K · 5500lm
- `00PREX50W4KB` — PAR 50W 4000K · 5500lm
- `00PREX50W6KB` — PAR 50W 6000K · 5500lm
- `00PROEX100XK` — SEC 100W · 17000lm
- `00PROEX150XK` — SEC 150W · 25500lm
- `00PROEX200W4K` — SEC 200W CCT · 34000lm · negro
- `00PROEX200XK` — SEC 200W · 34000lm
- `00PROEX300XK` — SEC 300W · 51000lm
- `00PROEX50XK` — SEC 50W · 8500lm
- `0PHE27WICIP1D` — Empotrable 1160×335mm 33W IC DALI
- `APESL-SLE_1200` — Estanca SLE 1200mm 18-36W IP65
- `APESL-SLE_1500-23` — Estanca SLE 1500mm 23-43W IP65
- `APESL-SLE_1500-36` — Estanca SLE 1500mm 36-50W IP65
- `APESL-SLE_1500-44` — Estanca SLE 1500mm 44W IP66 DALI2
- `APPLED` — Panel Slim 59×59 23-34W multivoltaje
- `APPLEDD` — Panel Slim 59×59 34W DALI

</details>

<details><summary>decorativas (6)</summary>

- `0051714800` — Galaxy circular suspendida 600mm 48W CCT blanco
- `00LCCR644037W` — Círculo 640 colgante decorativa 37W 4000K
- `00LCEP644037W` — Círculo 640 empotrable decorativa 37W 4000K
- `APLCCIRULO1000` — Aplique circular 1000mm 4000K DALI 47W
- `APLCCIRULO1500` — Aplique circular 1500mm 4000K DALI 71W
- `APLCCIRULO500` — Aplique circular 500mm 4000K DALI 23W

</details>

<details><summary>exterior (6)</summary>

- `0074710730` — Baliza empotrar suelo GU10 7W 3000K IP67
- `00MDVILLA50W4` — Módulo LED Villa 50W 6500lm 4000K-6000K IP65 90º
- `00PINCHOGU10` — Foco jardín pincho GU10 7W IP54 IK08 negro
- `APAPOT-19W-DALI` — Aplique pared/techo circular 19W DALI
- `APAPOT-22W` — Aplique pared/techo circular 22W ON-OFF
- `APAPOT-DMLD` — Aplique pared/techo 14-19W sensor movimiento

</details>

<details><summary>emergencias (2)</summary>

- `0080115000` — LEÓN S 150lm IP42 IK06 superficie Autotest
- `0080123000` — LEÓN S 230lm IP42 superficie Autotest

</details>

<details><summary>bombillas (1)</summary>

- `00TLT824W60K` — Tubo LED T8 1500mm 24W cristal conexión un lateral

</details>

## 5. Filas del Excel SIN producto publicado (180)

Códigos que existen en el maestro de Excel pero no tienen ficha `product-card` en `index.html` todavía (no llegan a `data/productos.json` en esta fase). Repartidos por hoja de origen:

| hoja Excel | nº sin publicar |
|---|---|
| DRIVER | 31 |
| DOWN.EMPOT. | 21 |
| GOLDRETRO | 20 |
| PSUP. | 20 |
| DOWN.ADOSABLES | 19 |
| LINEALES | 13 |
| PROYECTORES | 12 |
| EXTERIORES | 9 |
| LMINI | 8 |
| TIRAS LED | 7 |
| DECORATIVAS COLGANTES | 6 |
| ESTANCAS | 3 |
| EXTERIORES TODO | 2 |
| PEMP | 2 |
| ADOSADOS | 1 |
| P.ESPECIALES | 1 |
| APLIQUES EXT. | 1 |
| FAROLAS | 1 |
| INDUSTRIAL TODO | 1 |
| SALAS BLANCAS | 1 |
| CAMPANAS | 1 |

<details><summary>DRIVER (31)</summary>

- `00F100WIP20OF` — 
- `00F100WIP67OF` — 
- `00F150WIP20OF` — 
- `00F150WIP67OF` — 
- `00F200WIP20OF` — 
- `00F25WIP67OOF` — 
- `00F36WIP670OF` — 
- `00F400WIP20OF` — 
- `00F60WIP670OF` — 
- `00FA36W12VIP2` — Fuente de alimentación 36W 12V IP65 con toma a tierra.
- `00FL40WIP20DP` — 
- `00FL45WIP20OF` — 
- `00FL75WIP2010` — 
- `00FL75WIP20DP` — 
- `00FL75WIP20OF` — 
- `00FL75WIP20TR` — 
- `0FL100WIP20OF` — 
- `0FL150WIP2010` — 
- `0FL150WIP20BC` — 
- `0FL150WIP20DP` — 
- `0FL150WIP20OF` — 
- `0FL150WIP20TR` — 
- `0FL150WIP2BCA` — 
- `0FL150WIP2DPC` — 
- `0FL200WIP20OF` — 
- `0FL240WIP20DP` — 
- `0FL240WIP20OF` — 
- `0FL300WIP20OF` — 
- `0FL350WIP20OF` — 
- `0FL400WIP20OF` — 
- `0FL75WIP20DPC` — 

</details>

<details><summary>DOWN.EMPOT. (21)</summary>

- `00DLECSL5WXXX` — Downlight empotrable circular SLIM LED 5W 3000K-4500K-6000K CRI80 120°
- `00DLECSL6WCCT-` — Downlight empotrable circular SLIM LED 6W 3CCT CRI80 120°
- `00DLECSL6WXXX` — Downlight empotrable circular SLIM LED 6W 3000K-4500K-6000K CRI80 120°
- `00DLECSL9WCCT-` — Downlight empotrable circular SLIM LED 9W 3CCT CRI80 120°
- `00DLECSL9WXXX` — Downlight empotrable circular SLIM LED 9W 3000K-4500K-6000K CRI80 120°
- `00DWCOR20W30K` — Downlight empotrable mod. COR 20W-3000K 1900lm 30º IP20 blanco
- `0DECUSL12WCCT-` — Downlight empotrable cuadrado SLIM LED 12W 3CCT CRI80 120°
- `0DECUSL12WXXX` — Downlight empotrable cuadrado SLIM LED 12W 3000K-4500K-6000K CRI80 120°
- `0DECUSL20WCCT-` — Downlight empotrable cuadrado SLIM LED 20W 3CCT CRI80 120°
- `0DECUSL20WXXX` — Downlight empotrable cuadrado SLIM LED 20W 3000K-4500K-6000K CRI80 120°
- `0DECUSL25WCCT-` — Downlight empotrable cuadrado SLIM LED 25W 3CCT CRI80 120°
- `0DECUSL25WXXX` — Downlight empotrable cuadrado SLIM LED 25W 3000K-4500K-6000K CRI80 120°
- `0DLECSL12WCCT-` — Downlight empotrable circular SLIM LED 12W 3CCT CRI80 120°
- `0DLECSL12WXXX` — Downlight empotrable circular SLIM LED 12W 3000K-4500K-6000K CRI80 120°
- `0DLECSL20WCCT-` — Downlight empotrable circular SLIM LED 20W 3CCT CRI80 120°
- `0DLECSL20WXXX` — Downlight empotrable circular SLIM LED 20W 3000K-4500K-6000K CRI80 120°
- `0DLECSL25WCCT-` — Downlight empotrable circular SLIM LED 25W 3CCT CRI80 120°
- `0DLECSL25WXXX` — Downlight empotrable circular SLIM LED 25W 3000K-4500K-6000K CRI80 120°
- `0DLECUSL6WCCT-` — Downlight empotrable cuadradoSLIM LED 6W 3CCT CRI80 120°
- `0DLECUSL6WXXX` — Downlight empotrable cuadrado SLIM LED 6W 3000K-4500K-6000K CRI80 120°
- `0DLNEX25W30BB` — Downlight empotrado fijo mod. NEX 25W 3000K CRI90 60º 600mA

</details>

<details><summary>GOLDRETRO (20)</summary>

- `00DGR6M10W27K` — Downlight empotrado mod. MOTA gold retro D.60 10W 36º 2700K CRI90.
- `00DGR6M10W30K` — Downlight empotrado mod. MOTA gold retro D.60 10W 36º 3000K CRI90.
- `00DGR6M10W40K` — Downlight empotrado mod. MOTA gold retro D.60 10W 36º 4000K CRI90
- `00DGR8M15W27K` — Downlight empotrado mod. MOTA gold retro D.80 15W 36º 2700K CRI90
- `00DGR8M15W30K` — Downlight empotrado mod. MOTA gold retro D.80 15W 36º 3000K CRI90
- `00DGR8M15W40K` — Downlight empotrado mod. MOTA gold retro D.80 15W 36º 4000K CRI90
- `0LA15SL6W27KD` — Luminaria adosada SLIM GOLD RETRO 150mm 6W-2700K-24º-CRI90-IP20-DALI
- `0LA15SL6W30KD` — Luminaria adosada SLIM GOLD RETRO 150mm 6W-3000K-24º-CRI90-IP20-DALI
- `0LA20SL6W27KD` — Luminaria adosada SLIM GOLD RETRO 200mm 6W-2700K-24º-CRI90-IP20-DALI
- `0LA20SL6W30KD` — Luminaria adosada SLIM GOLD RETRO 200mm 6W-3000K-24º-CRI90-IP20-DALI
- `0LC15SL6W27KD` — Lámpara colgante SLIM GOLD RETRO 150mm 6W-2700K-24º-CRI90-IP20-DALI
- `0LC15SL6W30KD` — Lámpara colgante SLIM GOLD RETRO 150mm 6W-3000K-24º-CRI90-IP20-DALI
- `0LC20SL6W27KD` — Lámpara colgante SLIM GOLD RETRO 200mm 6W-2700K-24º-CRI90-IP20-DALI
- `0LC20SL6W30KD` — Lámpara colgante SLIM GOLD RETRO 200mm 6W-3000K-24º-CRI90-IP20-DALI
- `0LC30SL6W27KD` — Lámpara colgante SLIM GOLD RETRO 300mm 6W-2700K-24º-CRI90-IP20-DALI
- `0LC30SL6W30KD` — Lámpara colgante SLIM GOLD RETRO 300mm 6W-3000K-24º-CRI90-IP20-DALI
- `0P3CG706W30KD` — Proyector mod. Capi Gold retro 70mm D.35mm  6W-3000K-36º-48V CRI90-IP20-DALI
- `0P3G1008W30KD` — Proyector mod. Capi Gold retro 100mm D.35mm 8W-3000K-36º-48V CRI90-IP20-DALI
- `0P410010W30KD` — Proyector mod. Capi Gold retro 100mm D.45mm 10W-3000K-36º-48V CRI90-IP20-DALI
- `0P4CG708W30KD` — Proyector mod. Capi Gold retro 70mm D.45mm 8W-3000K-36º-48V CRI90-IP20-DALI

</details>

<details><summary>PSUP. (20)</summary>

- `00PS45S2020` — Perfil de aluminio 45º de superficie 15,8 X 15,8H X 2000mm difusor opal color aluminio IP20
- `00PSFB10S2020` — Perfil de aluminio B10 de superficie 19,5 X 20H X 2000mm, difusor opal color aluminio-IP20
- `00PSFB11S2020` — Perfil de aluminio B11 de superficie 20 X 10H X 2000mm, difusor opal color aluminio-IP20.
- `00PSFB14S2020` — Perfil de aluminio B14 de superficie 30 X 21H X 2000mm, difusor opal color aluminio-IP20.
- `00PSFB15S2020` — Perfil de aluminio B15 de superficie 35 X 37,5H X 2000mm difusor opal color aluminio IP20.
- `00PSFB16S2065` — Perfil de aluminio B16 de superficie 17,5 X 13H X 2000mm difusor opal color aluminio IP65
- `00PSFB17S2020` — Perfil de aluminio B17 de superficie 14,5 X 14,5H X 2000mm difusor opal color aluminio IP20.
- `00PSFB1S2020` — Perfil de aluminio B1 de superficie 7,2 X 9H X 2000mm, difusor opal, color aluminio, IP20.
- `00PSFB2S2020` — Perfil de aluminio B2 de superficie 8 X 7,2H X 2000 mm, difusor opal, color aluminio, IP20.
- `00PSFB3S2020` — Perfil de aluminio B3 de superficie 10 X 10H X 2000mm, difusor opal, color aluminio-IP20.
- `00PSFB4S2020` — Perfil de aluminio B4 de superficie 10 X 13H X 2000mm, difusor opal, color aluminio-IP20.
- `00PSFB5S2020` — Perfil de aluminio B5 de superficie 12 X 8H X 2000mm, difusor opal, color aluminio-IP20.
- `00PSFB6S2020` — Perfil de aluminio B6 de superficie 8,8 X 14,4H X 2000mm, difusor opal, color aluminio-IP20.
- `00PSFB7S2020` — Perfil de aluminio B7 de superficie 17 X 7H X 2000mm, difusor opal, color aluminio-IP20.
- `00PSFB8S2020` — Perfil de aluminio B7 de superficie 17 X 15H X 2000mm, difusor opal, color aluminio-IP20.
- `00PSFB9S2020` — Perfil de aluminio B9 de superficie 19,5 X 15H X 2000mm, difusor opal, color aluminio-IP20.
- `0PSFB7S2020B` — Perfil de aluminio B7 de superficie 17 X 7H X 2000mm, difusor opal, color blanco-IP20.
- `0PSFB7S2020N` — Perfil de aluminio B7 de superficie 17 X 7H X 2000mm, difusor opal, color blanco-IP20.
- `0PSFB8S2020B` — Perfil de aluminio B7 de superficie 17 X 15H X 2000mm, difusor opal, color blanco-IP20.
- `0PSFB8S2020N` — Perfil de aluminio B7 de superficie 17 X 15H X 2000mm, difusor opal, color negro-IP20.

</details>

<details><summary>DOWN.ADOSABLES (19)</summary>

- `00DLAT10WCCTB` — Downlight para adosar o supender fijo mod. TUBE led 10W 3CCT CRI80 36° blanco.
- `00DLAT10WCCTN` — Downlight para adosar o supender fijo mod. TUBE led 10W 3CCT CRI80 36° negro
- `00DLAT20WCCTB` — Downlight para adosar o supender fijo mod. TUBE led 20W 3CCT CRI80 36° blanco.
- `00DLAT20WCCTN` — Downlight para adosar o supender fijo mod. TUBE led 20W 3CCT CRI80 36° negro
- `0DACSL12WCCTX` — Downlight adosable circular SLIM LED 12W 3CCT CRI80 120°
- `0DACSL12WXXXX` — Downlight adosable circular SLIM LED 12W 3000K-4500K-6000K CRI80 120°
- `0DACSL20WCCTX` — Downlight adosable circular SLIM LED 20W 3CCT CRI80 120°
- `0DACSL20WXXXX` — Downlight adosable circular SLIM LED 20W 3000K-4500K-6000K CRI80 120°
- `0DACSL25WCCTX` — Downlight adosable circular SLIM LED 25W 3CCT CRI80 120°
- `0DACSL25WXXXX` — Downlight adosable circular SLIM LED 25W 3000K-4500K-6000K CRI80 120°
- `0DACUSL12WCCT` — Downlight adosable circular SLIM LED 12W 3000K-4500K-6000K CRI80 120°
- `0DACUSL12WXXX` — Downlight adosable circular SLIM LED 12W 3000K-4500K-6000K CRI80 120°
- `0DACUSL20WCCT` — Downlight adosable circular SLIM LED 20W 3000K-4500K-6000K CRI80 120°
- `0DACUSL20WXXX` — Downlight adosable circular SLIM LED 20W 3000K-4500K-6000K CRI80 120°
- `0DACUSL25WCCT` — Downlight adosable circular SLIM LED 25W 3000K-4500K-6000K CRI80 120°
- `0DACUSL25WXXX` — Downlight adosable circular SLIM LED 25W 3000K-4500K-6000K CRI80 120°
- `0DLACSL5WXXXX` — Downlight adosable circular SLIM LED 5W 3000K-4500K-6000K CRI80 120°
- `0DLACSL6WCCTX` — Downlight adosable circular SLIM LED 6W 3CCT CRI80 120°
- `0DLACSL6WXXXX` — Downlight adosable circular SLIM LED 6W 3000K-4500K-6000K CRI80 120

</details>

<details><summary>LINEALES (13)</summary>

- `0020300000` — SMCE 40W 4000K 350mA 2810mm IP40 SV0 PERFIL EXTRUSIÓN EMPOTRAR GRIS
- `0020341740` — SMCE 68W 4000K 350mA 2250mm IP40 SV0 PERFIL EXTRUSIÓN EMPOTRAR GRIS
- `00LIS5819W40K` — Perfil lineal 58 para adosar o suspender 19.1W 124.8lm.-mt. 200mA 1130x58x68mm IP40
- `00LXX107XXWXK` — Perfil lineal 107 para adosar o suspender XX x 107 x 68mm XXW 124.8lm.-mt. IP40.
- `00LXX40XXWXXK` — Perfil lineal 40 para adosar o suspender XX x 40 x 40mm XXW 124.8lm.-mt. IP20
- `00LXX58XXWXXK` — Perfil lineal 58 para adosar o suspender XX x 58 x 68mm XXW 124.8lm.-mt. IP40.
- `00LXXDIXXWXXK` — Luminaria lineal decorativa DI suspendida, de luz directa e indirecta XX x 39x125mm XXW 108.9lm.-mt.
- `00LXXMIXXWXXK` — Perfil lineal MINI para adosar o suspender XX x 28 x 25mm XXW 108.9lm.-mt. IP40
- `00LXXOVXXWXXK` — Perfil lineal OVAL para adosar o suspender XX x 28 x 25mm XXW 108.9lm.-mt. IP40
- `00LXXRCXXWXXK` — Perfil lineal RC para adosar o suspender XX x 28 x 75mm XXW 108.9lm.-mt. IP40.
- `00LXXREXXWXXK` — Perfil lineal RE para adosar o suspender XX x 28 x 60mm XXW 108.9lm.-mt. IP40
- `0LEM05C12W40K` — Perfil lineal EM05 empotrable 570 x 40 x 65mm 12W 1975lm 4000K IP40
- `0LXXIP65XXWXK` — Perfil lineal 58 para adosar o suspender XX x 58 x 76mm XXW 124.8lm.-mt. IP65

</details>

<details><summary>PROYECTORES (12)</summary>

- `00PRCLIP2730B` — Proyector LED 27W mod. CLIP 27-30-40K 2700lm CRI95 apertura 20º-50º - blanco
- `00PRCLIP2730N` — Proyector LED 27W mod. CLIP 27-30-40K 2700lm CRI95 apertura 20º-50º - negro
- `00PRMOD30W40K` — Proyector LED MODEM 30W 3460lm 4000K CRI95 40º negro
- `00PRMOD40W40K` — Proyector LED MODEM 40W 3460lm 4000KCRI95 40º negro.
- `00PROYZOOM20B` — Proyector LED mod. ZOOM 20W 920lm CRI90, 6-60º, 500mA. blanco
- `00PROYZOOM20N` — Proyector LED mod. ZOOM 20W 920lm CRI90, 6-60º, 500mA. Negro.
- `00PROYZOOM25B` — Proyector LED mod. ZOOM 25W 1125lm CRI90, 6-60º, 650mA. blanco
- `00PROYZOOM25N` — Proyector LED mod. ZOOM 25W 1125lm CRI90, 6-60º, 650mA. Negro.
- `00PRPIC10W30B` — Proyector PIC LED 10W 3000K 600lm CRI92 36º blanco
- `00PRPIC10W30N` — Proyector PIC LED10W 3000K 600lm CRI92 36º Negro.
- `00PRPIC15W30B` — Proyector PIC LED 15W 3000K 890lm CRI92 36º blanco
- `00PRPIC15W30N` — Proyector PIC LED 15W 3000K 890lm CRI92 36º negro.

</details>

<details><summary>EXTERIORES (9)</summary>

- `00BE6TI20W30K` — Baliza para exteriores mod. TI IP65 H.800mm 20W 3000K 600mA.
- `00BE8TI24W30K` — Baliza para exteriores mod. TI IP65 H.800mm 24W 3000K 600mA.
- `0BAALA05WXXKX` — Baliza de paso adosable mod. LARGE rectangular 5W IP54  30x230x81mm
- `0BACGO03WXXKX` — Baliza de paso adosable mod. GO cuadrada IP65 3W 3000K 180mA. 33x117x117mm.
- `0BARGO03WXXKX` — Baliza de paso adosable mod. GO circular IP65 3W 3000K 180mA. Ø117 mm
- `0BE20TI48W30K` — Baliza para exteriores mod. TI IP65 H.2000mm 48W 3000K 1200mA.
- `0BETE3012W30K` — Baliza para exteriores mod. TE IP65 H:300mm 12W 3000K 300mA
- `0BETE5012W30K` — Baliza para exteriores mod. TE IP65 H:500mm 12W 3000K 300mA
- `APB75T-DMLD` — BOLARDO75_8W_30-40_IP65 - Bolardo para exteriores 8W 3000 - 4000K - h750mm con regulación Triac

</details>

<details><summary>LMINI (8)</summary>

- `00L05MI13W30K` — Perfil lineal MINI para adosar o suspender 590mm x 28mm 13W 1300lm IP40
- `00L05MI13W40K` — Perfil lineal MINI para adosar o suspender 590mm x 28mm 13W 1350lm IP40
- `00L08MI19W30K` — Perfil lineal MINI para adosar o suspender 870mm x 28mm 19W 1950lm IP40
- `00L08MI19W40K` — Perfil lineal MINI para adosar o suspender 870mm x 28mm 19W 2025lm IP40
- `00L11MI25W30K` — Perfil lineal MINI para adosar o suspender 1150mm x 28mm 25W 2700lm IP40
- `00L11MI25W40K` — Perfil lineal MINI para adosar o suspender 1150mm x 28mm 25W 2700lm IP40
- `00L14MI31W30K` — Perfil lineal MINI para adosar o suspender 1400mm x 28mm 31W 3250lm IP40
- `00L14MI31W40K` — Perfil lineal MINI para adosar o suspender 1400mm x 28mm 31W 3375lm IP40

</details>

<details><summary>TIRAS LED (7)</summary>

- `00TLEDC10WXXX` — Tira Led flexible mod. TIP 24v SMD2835 IP20 monocolor 10W 800lm x mt. 120º, CRI80
- `00TLIPS26WXXX` — Tira de Led flexible 26W 24V mod. C monocolor 3003lm x mt. Smd2835 IP20 120º  CRI80
- `0TIR12V27KIP2-` — TIRA LED 14W 12V 2700K IP20 SMD5050
- `0TL12W220VIP6` — TIRA LED 12W_mt 220V 1400lm-mt IP65 SMD2835
- `0TLRGB12WIP20` — Tira de Led flexible 12W x mt 24V mod. A RGB-SMD3535 IP20 120º CRI80
- `0TLRGB12WIP65` — Tira de Led flexible 12W x mt 24V mod. A RGB-SMD3535 IP65 120º CRI80
- `0TLRGB14WIP65` — Tira de Led flexible 14W x mt 12V mod. B RGB-Smd 5050 IP65 120º CRI80, 5 metros

</details>

<details><summary>DECORATIVAS COLGANTES (6)</summary>

- `00LAMSP300NG` — Luminaria suspendida decorativa ESILE E27 3000K - negro exterior - interior oro.
- `00LSG51714800` — Luminaria suspendida circular mod. GALAXY 48W CCT 600mm BLANCO
- `00VENIC8WG30K` — Luminaria suspendida mod. VENICE RETRO GOLD 8W 3000K 630lm CRI90 24º
- `0LSCR64037W4K` — Luminaria suspendida mod. Circulo 640 decorativa circular para suspender 37W 3286lm 4000K
- `APLCCIRULO1500_40D_71W` — Luminaria slim decorativa circular de luz directa para adosar o suspender
- `APLCCIRULO500_40D_23W` — Luminaria slim decorativa circular de luz directa para adosar o suspender.

</details>

<details><summary>ESTANCAS (3)</summary>

- `0030513440` — luminaria LED estanca SLE-T LED 34W 4000K 5360Lm 1200mm IP66
- `00PAEST24W4K` — Pantalla estanca LED 24W 4000K 3950Lm 250mA. 1200mm IP66
- `00PAN23_43W4K` — Pantalla LED estanca 23_43W4000K - 1500mm IP66-IK08

</details>

<details><summary>EXTERIORES TODO (2)</summary>

- `00APLCUB093KB` — Aplique pared tipo cubo 9W 3000K IP67
- `00PINCHOGU10N-` — Foco jadín pincho GU10 7W IP54 IK08 - Negro

</details>

<details><summary>PEMP (2)</summary>

- `0PEFA11E2020B` — Perfil de aluminio A11 para empotrar 30 X 11H X 2000mm difusor opal, color blanco IP20.
- `0PEFA11E2020N` — Perfil de aluminio A11 para empotrar 30 X 11H X 2000mm difusor opal, color negro IP20.

</details>

<details><summary>ADOSADOS (1)</summary>

- `00AP19W30KDIP` — Aplique Led superficie circular para montaje en pared o techo 19W-DALI IP65

</details>

<details><summary>P.ESPECIALES (1)</summary>

- `00P45S2020` — PERFIL DE ALUMINIO 45º DE SUPERFICIE CON DIFUSOR OPAL 2MT-IP20

</details>

<details><summary>APLIQUES EXT. (1)</summary>

- `0APACU06WCCTX` — Aplique de pared adosable mod. CUBE 6W IP54 600lm. 3CCT.

</details>

<details><summary>FAROLAS (1)</summary>

- `0FASOJY20WXXK` — Farola Led SOLAR JY 20W 3000lm IP65 IK08 120° -

</details>

<details><summary>INDUSTRIAL TODO (1)</summary>

- `0PANABAX344KD` — Pantalla Eco ABAX Dali 31,4W 2C 5900lm 180lm_W 120º UGR 19, difusor microprisma blanco L80B10.

</details>

<details><summary>SALAS BLANCAS (1)</summary>

- `0PHE27WICIP6D-` — Pantalla hospitalaria empotrable 600 x 600mm 27,3W 4000K IP65 5214 lm DALI - IC (intelligent colors)

</details>

<details><summary>CAMPANAS (1)</summary>

- `OOCAMU200W4KD` — Campana grandes alturas para suspender mod. UF 200W DALI 32000lm IP65 negro.

</details>

## 6. Productos publicados sin ref (4) — no cruzables

- (sin ref) — Fuente alimentación 24V IP20 ON-OFF — `2 INTERIORES/TIRAS Y PERFILES LED/FUENTES DE ALIMENTACIÓN 24V IP20 ON-OFF/FUENTES-DE-ALIMENTACIÓN-24V-IP20-ON-O.pdf`
- (sin ref) — Fuente alimentación 24V IP67 ON-OFF — `2 INTERIORES/TIRAS Y PERFILES LED/FUENTES DE ALIMENTACIÓN 24V IP20 ON-OFF/FUENTES-DE-ALIMENTACIÓN-24V-IP67-ON-O.pdf`
- (sin ref) — Fuente LIFUD 24V IP20 ON-OFF — `2 INTERIORES/TIRAS Y PERFILES LED/FUENTES DE ALIMENTACIÓN 24V IP20 ON-OFF/FUENTES-DE-ALIMENTACIÓN-LIFUD-24V-IP2.pdf`
- (sin ref) — Fuente LIFUF 24V IP20 regulables — `2 INTERIORES/TIRAS Y PERFILES LED/FUENTES DE ALIMENTACIÓN 24V IP20 ON-OFF/FUENTES-DE-ALIMENTACIÓN-LIFUF-24V-IP2.pdf`

## 7. Candidatos a fusionar en menos fichas (para la fase 3, aviso del punto 5)

Como comentaste con el ejemplo de "ZEN": muchos códigos distintos dentro de la misma subfamilia no son productos distintos, sino el mismo producto con distinta potencia y/o temperatura de color. Heurística usada: quito de `nombre` los tokens de potencia (W), lúmenes (lm) y temperatura de color (K/CCT) y agrupo lo que queda dentro de la misma subfamilia — si 3 o más refs colapsan en el mismo texto restante, es candidato a fusión. Esto **no se ha aplicado todavía** a `data/productos.json` (sigue siendo 1 entrada = 1 ref, tal y como pediste para esta fase); es solo la lista para decidir antes de tocar el HTML.

Se detectaron **12 grupos** con 3+ variantes:

- **Downlight ZEN** — "ZEN 70º" · 21 refs → agruparían en 7 panel(es) por potencia: 12W (3 variantes), 20W (3 variantes), 25W (3 variantes), 30W (3 variantes), 40W (3 variantes), 50W (3 variantes), 7W (3 variantes)
  - refs: 00DLZEN07W27X, 00DLZEN07W30X, 00DLZEN07W40X, 00DLZEN12W27X, 00DLZEN12W30X, 00DLZEN12W40X, 00DLZEN20W27X, 00DLZEN20W30X, 00DLZEN20W40X, 00DLZEN25W27X, 00DLZEN25W30X, 00DLZEN25W40X, 00DLZEN30W27X, 00DLZEN30W30X, 00DLZEN30W40X, 00DLZEN40W27X, 00DLZEN40W30X, 00DLZEN40W40X, 00DLZEN50W27X, 00DLZEN50W30X, 00DLZEN50W40X
- **Downlight NEX** — "NEX 60º negro" · 8 refs → agruparían en 4 panel(es) por potencia: 12W (2 variantes), 20W (2 variantes), 25W (2 variantes), 7W (2 variantes)
  - refs: 0DLNEX07W30BN, 0DLNEX07W40BN, 0DLNEX12W30BN, 0DLNEX12W40BN, 0DLNEX20W30BN, 0DLNEX20W40BN, 0DLNEX25W30BN, 0DLNEX25W40BN
- **Downlight NEX** — "NEX 60º blanco" · 7 refs → agruparían en 4 panel(es) por potencia: 12W (2 variantes), 20W (2 variantes), 25W (1 variantes), 7W (2 variantes)
  - refs: 0DLNEX07W30BB, 0DLNEX07W40BB, 0DLNEX12W30BB, 0DLNEX12W40BB, 0DLNEX20W30BB, 0DLNEX20W40BB, 0DLNEX25W40BB
- **EXIT S** — "EXIT S superficie 1h IP65 no permanente difusor opal" · 5 refs → agruparían en 1 panel(es) por potencia: ? (5 variantes)
  - refs: 00EMEEXITS150, 00EMEEXITS250, 00EMEEXITS350, 00EMEEXITS450, 00EMGEXITS200
- **Gama CAP CRI95 · 10-30W** — "CAP LED CRI95 36º blanco" · 5 refs → agruparían en 3 panel(es) por potencia: 10W (1 variantes), 20W (2 variantes), 30W (2 variantes)
  - refs: 00PROCA10W30B, 00PROCA20W30B, 00PROCA20W40B, 00PROCA30W30B, 00PROCA30W40B
- **Gama ALFA IP65 · Negro** — "ALFA · hasta" · 5 refs → agruparían en 3 panel(es) por potencia: 100-125-150W (2 variantes), 100-150-200W (2 variantes), 60-80-100W (1 variantes)
  - refs: OOCAMP100W4KA, OOCAMP150W4KA, OOCAMP150W5KA, OOCAMP200W4KA, OOCAMP200W5KA
- **Pantallas Estancas** — "Estanca 600mm" · 4 refs → agruparían en 2 panel(es) por potencia: 12W (2 variantes), 17W (2 variantes)
  - refs: 00PAES12W4K60, 00PAES12W6K60, 00PAES17W4K60, 00PAES17W6K60
- **Gama CAP CRI95 · 10-30W** — "CAP LED CRI95 36º negro" · 4 refs → agruparían en 2 panel(es) por potencia: 20W (2 variantes), 30W (2 variantes)
  - refs: 00PROCA20W30N, 00PROCA20W40N, 00PROCA30W30N, 00PROCA30W40N
- **Farola LI IP65 · Regulable 0-10V** — "Farola LI" · 3 refs → agruparían en 3 panel(es) por potencia: 30W (1 variantes), 60W (1 variantes), 90W (1 variantes)
  - refs: 00FALI30WXXXK, 00FALI60WXXXK, 00FALI90WXXXK
- **Farola ST IP65 · Regulable 1-10V** — "Farola ST" · 3 refs → agruparían en 3 panel(es) por potencia: 30W (1 variantes), 60W (1 variantes), 90W (1 variantes)
  - refs: 00FAST30WXXXK, 00FAST60WXXXK, 00FAST90WXXXK
- **Pantallas Estancas** — "Estanca 1200mm" · 3 refs → agruparían en 3 panel(es) por potencia: 18-36W (1 variantes), 19W (1 variantes), 30W (1 variantes)
  - refs: 00PAN18-36W4K, 00PANEST19W4K, 00PANEST30W4K
- **Paneles LED** — "Pantalla empotrable 2 calles blanco" · 3 refs → agruparían en 3 panel(es) por potencia: 24W (1 variantes), 34W (1 variantes), 48W (1 variantes)
  - refs: 0PE2C24W4KIP4, 0PE2C34W4KIP4, 0PE2C48W4KIP4


## 8. Punto 8 — texto suelto del Excel, ya clasificado (2026-09-21)

Quedaba pendiente decidir qué hacer con fragmentos de la descripción del Excel que no encajaban
en ningún spec ya definido (ejemplos que diste: `UGR19`, `"No fliker"`, `"monocolor"`,
`"difusor opal"`). Decisión: **se añaden como specs propios**, con su propia etiqueta, igual que
el resto — no como nota de texto libre ni descartados.

Se revisaron las 187 referencias comparando su descripción original del Excel contra los specs ya
extraídos, para aislar qué quedaba sin clasificar. Se detectaron 12 conceptos recurrentes y se
añadieron como specs nuevos donde aparecían (88 specs nuevos en total, sobre 70 referencias):

| Etiqueta nueva | Refs afectadas | Ejemplo |
|---|---|---|
| Difusor | 28 | `Opal`, `Microprisma` |
| Uso recomendado | 14 | `Ambientes estériles / hospitalarios`, `Grandes alturas` |
| Deslumbramiento (UGR) | 12 | `UGR19` |
| Tipo de color | 8 | `Monocolor` |
| Parpadeo | 6 | `Sin parpadeo (No flicker)` |
| Chip LED | 5 | `SMD2835` |
| Regulación / control (DALI2 no capturado antes) | 5 | `DALI2` |
| Mantenimiento | 4 | `Acceso superior` |
| Régimen de funcionamiento | 3 | `Permanente` / `No permanente` |
| Ajuste del ángulo | 1 | `Orientable (ángulo regulable)` |
| Tecnología | 1 | `IC (Intelligent Colors)` |
| Vida útil (LED) | 1 | `L80B10` |

En las 11 fichas de grupo donde el valor nuevo es igual en **todas** las variantes, también se
promovió a `specs_resumen` (p. ej. el grupo de Tiras LED SMD2835 pasó a mostrar `Chip LED: SMD2835`
y `Tipo de color: Monocolor` en el resumen, no solo en cada variante).

De paso, revisando el texto original se encontraron y corrigieron 3 errores de parseo previos
(no relacionados con el punto 8, pero descubiertos al revisar el mismo texto):
- `OPANABAX344KD`: la potencia se había leído como `4W` en vez de `31,4W` (el Excel usa coma
  decimal); también tenía un `Flujo luminoso: 180 lm` erróneo — en realidad es la eficacia
  (`180 lm/W`), separada ahora en su propio spec "Eficacia luminosa".
- `0PHEIPAS41W40KD` y `0PHEIPAS41W30KD`: potencia leída como `6W` en vez de `41,6W` (mismo motivo,
  coma decimal).
- `00CAPGL488W30`: el Excel tiene un typo (`48V 8V` en vez de `48V 8W` — el nombre público del
  producto, que ya usa "8W", confirma que es un error del Excel); se quitó el `Voltaje: 8V`
  duplicado/erróneo y se añadió `Potencia: 8W`.
