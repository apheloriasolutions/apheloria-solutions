"""
Escribe docs/catalogo/contenido.md: qué tiene cada botón (tabla, notas, descripción,
fotos y PDF) a partir de data/catalogo.json.

Uso:  python scripts/catalogo/informe_contenido.py
"""
import json, os
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
SALIDA = os.path.join(RAIZ, 'docs', 'catalogo', 'contenido.md')
TIPOS = ('luminaria', 'medidas', 'ambiente', 'angulo')


def botones(nodo, ruta=()):
    for b in nodo['botones']:
        yield ruta, b
    for h in nodo['hijos']:
        yield from botones(h, ruta + (h['nombre'],))


def main():
    cat = json.load(open(DATOS, encoding='utf-8'))
    todos = list(botones(cat['arbol']))
    fichas = {c for _, b in todos for c in b['codigos']}
    con_tabla = [b for _, b in todos if b.get('tabla')]
    sin_tabla = [(r, b) for r, b in todos if not b.get('tabla')]
    filas = Counter(len(b['tabla']) for b in con_tabla)
    pdfs = {c for _, b in todos for c in b.get('pdf', {})}
    sin_pdf = sorted(fichas - pdfs)

    L = ['# Productos — contenido de cada botón', '',
         'Generado por `scripts/catalogo/informe_contenido.py` a partir de `data/catalogo.json`.',
         'La web todavía no lo usa: esto es el material listo para montarla.', '',
         '## Resumen', '',
         f'- **{len(todos)} botones** a partir de **{len(fichas)} fichas**.',
         f'- Con tabla de características: **{len(con_tabla)}** · sin tabla: {len(sin_tabla)}.',
         f'- Con notas al pie: {sum(1 for b in con_tabla if b.get("notas"))}.',
         f'- Con descripción: {sum(1 for b in con_tabla if b.get("descripcion"))}.',
         f'- Con foto de producto: {sum(1 for _, b in todos if (b.get("fotos") or {}).get("luminaria"))}.',
         f'- Con PDF descargable: **{len(pdfs)} fichas** de {len(fichas)}.', '',
         '## De dónde sale cada cosa', '',
         '| En la web | De dónde sale la ficha |', '|---|---|',
         '| Tabla de características | columnas A y B de la primera hoja, desde la primera etiqueta '
         'acabada en dos puntos hasta la primera fila vacía. Las filas sin valor no se muestran |',
         '| Notas al pie | las filas cuya etiqueta es una frase larga, y el bloque "NOTAS IMPORTANTES" '
         'que algunas fichas llevan debajo de la tabla |',
         '| Descripción | el párrafo de la columna D. Si las fichas de un grupo solo cambian en un dato '
         '(los vatios), se juntan en una sola: "7-12-20-25W de potencia" |',
         '| Fotos | las imágenes incrustadas en el .xlsx, en su calidad original |',
         '| PDF | la primera hoja de la ficha, convertida con LibreOffice y ajustada a una A4 |', '',
         'Lo que **no** sale: la segunda hoja del Excel, que lleva referencias de proveedor.', '',
         f'## Tamaño de las tablas', '',
         '| Filas | Botones |', '|---|---|']
    L += [f'| {n} | {c} |' for n, c in sorted(filas.items())]

    L += ['', '## Botones sin tabla', '',
          f'{len(sin_tabla)} botones. Salen con fotos y PDF, pero sin características.', '']
    L += [f"- **{b['nombre']}** — {' › '.join(r)}  \n  `{', '.join(b['codigos'])}`" for r, b in sin_tabla]

    if sin_pdf:
        L += ['', '## Fichas sin PDF', '', f'{len(sin_pdf)} fichas.', '']
        L += [f'- `{c}`' for c in sin_pdf]

    L += ['', '## Botones, uno a uno', '',
          '| Botón | Dónde | Fichas | Filas | Notas | Descr. | Fotos | PDF |',
          '|---|---|---|---|---|---|---|---|']
    for r, b in todos:
        fotos = sum(1 for t in TIPOS if (b.get('fotos') or {}).get(t))
        L.append(f"| {b['nombre']} | {' › '.join(r)} | {len(b['codigos'])} | {len(b.get('tabla', []))} "
                 f"| {len(b.get('notas', []))} | {len(b.get('descripcion', []))} | {fotos}/4 "
                 f"| {len(b.get('pdf', {}))} |")

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    open(SALIDA, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'{SALIDA}: {len(todos)} botones · {len(pdfs)} PDF')


if __name__ == '__main__':
    main()
