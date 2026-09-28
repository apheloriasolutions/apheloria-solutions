"""
Escribe docs/catalogo/estructura.md a partir de data/catalogo.json.

Uso:  python scripts/catalogo/informe_estructura.py
"""
import json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
SALIDA = os.path.join(RAIZ, 'docs', 'catalogo', 'estructura.md')
corto = lambda ruta: os.path.basename(ruta)


def recorrer(nodo, prof=0, camino=()):
    filas = []
    if prof:
        filas.append((prof, nodo, camino))
    for h in nodo['hijos']:
        filas += recorrer(h, prof + 1, camino + (nodo['nombre'],))
    return filas


def main():
    d = json.load(open(DATOS, encoding='utf-8'))
    arbol, inc = d['arbol'], d['incidencias']
    niveles = recorrer(arbol)
    botones = [(n, b) for _, n, _ in niveles for b in n['botones']]
    fichas = sum(len(b['archivos']) for _, b in botones)
    hondo = max(p for p, _, _ in niveles)

    L = ['# Productos — estructura sacada de las fichas técnicas', '',
         'Generado por `scripts/catalogo/construir_estructura.py` a partir de `fuentes/fichas/`',
         '(los Excel originales, que no se publican). Vuelve a ejecutarlo cada vez que cambien las fichas.', '',
         f'- **{len(botones)} botones** a partir de **{fichas} fichas** publicables.',
         f'- {len([1 for p, _, _ in niveles if p == 1])} grandes familias · hasta **{hondo} niveles** de profundidad.',
         '- Los nombres de cada nivel salen del nombre de la carpeta, quitándole la numeración.',
         '- El nombre del botón sale del nombre del archivo, cortado en el primer dato técnico.',
         '- Las fichas con el mismo nombre dentro de una carpeta se agrupan en un solo botón.', '',
         '---', '', '## Árbol completo', '']

    for prof, nodo, _ in niveles:
        sangria = '  ' * (prof - 1)
        n_b = len(nodo['botones'])
        cuenta = f" — {n_b} {'botones' if n_b != 1 else 'botón'}" if n_b else ''
        L.append(f"{sangria}- **{nodo['nombre']}**{cuenta}")
        for b in nodo['botones']:
            n = len(b['archivos'])
            agrupa = f" · agrupa {n} fichas" if n > 1 else ''
            L.append(f"{sangria}  - {b['nombre']}{agrupa}  \n{sangria}    `{', '.join(b['codigos'])}`")

    # ── botones que conviene mirar ──
    dudosos = [(n, b) for n, b in botones
               if len(b['nombre']) < 8 or len(b['nombre']) > 62 or b['nombre'].isupper()
               or re.search(r'\b(XX|XXX)\b', b['nombre']) or re.search(r'[\d,\-_]$', b['nombre'])]
    L += ['', '---', '', '## Botones cuyo nombre conviene revisar', '',
          f'{len(dudosos)} de {len(botones)}. No están mal generados: es lo que dice la ficha de origen.', '',
          '| Nombre generado | Dónde | Por qué |', '|---|---|---|']
    for n, b in dudosos:
        motivos = []
        if b['nombre'].isupper(): motivos.append('todo en mayúsculas en el origen')
        if len(b['nombre']) < 8: motivos.append('muy corto')
        if len(b['nombre']) > 62: motivos.append('muy largo')
        if re.search(r'\b(XX|XXX)\b', b['nombre']): motivos.append('la ficha trae XX como comodín')
        if re.search(r'[\d,\-_]$', b['nombre']): motivos.append('acaba en cifra o signo')
        L.append(f"| {b['nombre']} | {n['nombre']} | {', '.join(motivos)} |")

    # ── lo que no se publica ──
    L += ['', '---', '', '## Lo que no se publica, y por qué', '',
          'Esta es la lista para quien mantiene las fichas. Todo lo de aquí abajo está fuera de la web.', '']

    L += ['### 1. La ficha dice unos datos y su tabla dice otros', '',
          f'{len(inc["no_cuadra"])} fichas. El nombre del archivo declara unos vatios, lúmenes o grados K que **no aparecen '
          'en la tabla de características** de la propia hoja. Suelen ser copias de otra ficha a las que se les cambió el '
          'nombre pero no el contenido: hay que corregir el Excel.', '',
          '| Archivo | No cuadra | Lo que dice su tabla |', '|---|---|---|']
    for rel, cod, faltan, tabla in inc['no_cuadra']:
        dice = ' · '.join(f"{k}: {', '.join(v[:3])}" for k, v in tabla.items() if v)
        L.append(f"| `{corto(rel)}` | {', '.join(faltan)} | {dice} |")

    L += ['', '### 2. Fichas sin código localizable', '',
          f'{len(inc["sin_codigo"])} archivos. Ni el nombre del archivo ni ninguna celda de la hoja traen algo con forma '
          'de código seguido de descripción.', '']
    for rel, motivo in inc['sin_codigo']:
        L.append(f'- `{rel}`')

    if inc.get('sin_nombre'):
        L += ['', '### 3. Fichas cuya descripción se queda vacía', '']
        for rel, motivo in inc['sin_nombre']:
            L.append(f'- `{rel}` — {motivo}')

    L += ['', '### 4. Plantillas sin rellenar', '']
    for rel, motivo in inc['plantilla']:
        L.append(f'- `{rel}` — {motivo}')

    L += ['', '### 5. Un mismo código en dos carpetas con fichas distintas', '',
          'Una de las dos lleva el código de la otra. No se publica ninguna hasta saber cuál es la buena.', '']
    for cod, lista in inc['repetido_distinto']:
        L.append(f'- **{cod}**')
        for arch, nombre in lista:
            L.append(f'  - `{arch}` → "{nombre}"')

    L += ['', '### 6. Archivos que no son fichas', '',
          f'{len(inc["no_es_ficha"])} archivos sueltos entre las fichas (carátulas en Word, comprimidos que sobraron al '
          'descomprimir, algún PDF y temporales de Excel). Se ignoran.', '']
    for rel in inc['no_es_ficha']:
        L.append(f'- `{rel}`')

    # ── avisos que sí se publican ──
    L += ['', '---', '', '## Avisos: esto sí se publica, pero conviene mirarlo', '']
    cuadran = [x for x in inc['codigo_distinto'] if x[3]]
    L += ['### El código del archivo y el de la celda no coinciden', '',
          f'{len(inc["codigo_distinto"])} fichas. Se usa **el del nombre del archivo**, que es el bueno. '
          f'De esas, {len(cuadran)} sí cuadran con su tabla y se publican; las otras {len(inc["codigo_distinto"]) - len(cuadran)} '
          'están arriba, en la lista de lo que no se publica.', '',
          '| Archivo | Código usado | Código de la celda | ¿Cuadra con su tabla? |', '|---|---|---|---|']
    for rel, cod, cel, ok, faltan in inc['codigo_distinto']:
        L.append(f"| `{corto(rel)[:56]}` | `{cod}` | `{cel}` | {'sí' if ok else 'no, se descarta'} |")

    L += ['', '### El mismo código en dos carpetas, con la misma ficha', '',
          'Se publica en las dos: es el mismo producto listado en dos sitios.', '']
    for cod, archivos in inc['repetido_igual']:
        L.append(f'- **{cod}**: ' + ' · '.join(f'`{corto(a)}`' for a in archivos))

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    open(SALIDA, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'{SALIDA}: {len(L)} líneas')


if __name__ == '__main__':
    main()
