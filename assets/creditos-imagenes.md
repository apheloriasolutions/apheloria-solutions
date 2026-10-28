# Créditos de las imágenes

Fotografías que no son del catálogo de Apheloria, con su origen y su licencia.
Todas con licencia que permite uso comercial **sin atribución obligatoria**; se dejan
apuntadas aquí por trazabilidad. Las portadas de sección se buscaron con la API de Pixabay
y su licencia está comprobada en la página de origen de cada una; la API sirve como mucho
1280 px de ancho, que es el tamaño con el que se publican.

## Portadas de las secciones de Productos

Se cambian en `data/textos.json`, con la clave `portada` de cada sección, y se publican
volviendo a ejecutar `scripts/catalogo/construir_web.py`.

| Sección | Título original | Banco | Licencia | Publicada |
|---|---|---|---|---|
| interiores | Plafón de superficie encendido en un salón | aportada por el cliente | — | 1196×824 |
| exteriores | Escalera de acceso iluminada de noche | Pixabay | Pixabay Content License | 1280×720 |
| decorativas | Esferas suspendidas | Pixabay | Pixabay Content License | 1280×853 |
| industriales | Nave industrial con luminarias lineales | Pixabay | Pixabay Content License | 1280×762 |
| hospitalarias-salas-blancas | Pasillo hospitalario con paneles empotrados | aportada por el cliente | — | 918×612 |
| emergencia | Señal de salida en techo perforado | Pixabay | Pixabay Content License | 1280×849 |
| bombillas-y-accesorios | Bombilla de filamento LED | Pixabay | Pixabay Content License | 1280×853 |
| salas-blancas | Pasillo hospitalario con paneles empotrados | aportada por el cliente | — | 918×690 |
| interiores/downlights-empotrados (cabecera) | Salón con downlights empotrados | aportada por el cliente | — | 1150×822 |
- **interiores**: foto aportada por Apheloria (28-10-2026), sustituye a la de Pixabay
- **exteriores**: https://pixabay.com/photos/evening-building-illuminated-stairs-4579176/
- **decorativas**: https://pixabay.com/photos/light-bulbs-lights-spheres-lamps-407239/
- **industriales**: https://pixabay.com/photos/lost-places-empty-factory-building-1801660/
- **hospitalarias-salas-blancas**: foto aportada por Apheloria (28-10-2026)
- **emergencia**: https://pixabay.com/photos/emergency-exit-escape-fire-4168808/
- **bombillas-y-accesorios**: https://pixabay.com/photos/light-bulb-light-led-lighting-1358917/
- **salas-blancas**: foto aportada por Apheloria (28-10-2026), mismo pasillo con otro encuadre
- **downlights-empotrados**: foto aportada por Apheloria (28-10-2026). Es la cabecera de la
  sección (`hero` en `data/textos.json`), no una portada de gran familia; sustituye a la foto
  de ambiente de los cardanes, un bar con el rótulo del local a la vista
- **Fuentes de Alimentación 24V IP20 ON-OFF**: no hay nada decente en los bancos libres

## Fotos de ambiente que no salen de la ficha

Se ponen en `IMAGENES_SUSTITUIDAS`, dentro de `scripts/catalogo/extraer_fotos.py`, con el
md5 de la imagen del Excel que sustituyen; alcanzan a todas las fichas que la comparten.

| Dónde sale | Título original | Banco | Licencia | Publicada |
|---|---|---|---|---|
| Campanas ALFA y Campanas › Especial (9 fotos) | Nave con estanterías de gran altura | Pixabay | Pixabay Content License | 1280×720 |
| Paneles: LINC luz indirecta y panel ABAX (3 fotos) | Sala de reuniones con paneles en el techo | Pixabay | Pixabay Content License | 1280×855 |

- **Campanas ALFA**: https://pixabay.com/photos/industrial-material-logistic-fires-612297/
  Sustituye a la nave con puente grúa que traía el Excel, de 486×332 px. La original queda
  en `_revision/fotos-retiradas/nave-puente-grua-486px.jpg`.
- **Paneles**: https://pixabay.com/photos/meeting-room-table-screen-conference-730679/
  Sustituye a una oficina de 307×394 px con dos personas reconocibles de frente. La
  original queda en `_revision/fotos-retiradas/oficina-linc-307px.jpg`.

## Fotos de la portada (Inicio)

El carrusel del hero usa **cuatro fotos de proyectos de Apheloria** (Ciudad de la Justicia,
Santalucía, Avenida de América y Plaza Castilla); la cabecera de Nosotros, fotos de las
propias fichas técnicas. La foto del conector (la Apheloria que brilla) la aportó el
cliente. Nada de esto viene de bancos de imágenes.

## Secciones sin foto de banco

- **Fuentes de Alimentación** y **Fuentes de 24V**: usan la foto de producto de su
  propia ficha. En los bancos libres no hay nada que represente un driver LED.
- **Farolas SO (solar)**: usa la foto de producto de la Farola Led SOLAR JY. Lo que
  devuelven los bancos buscando "solar street light" son fotos de prensa con personas
  identificables.
- **Pantallas Hospitalarias 600 × 600 mm**: usa la foto de producto de su propia ficha.
