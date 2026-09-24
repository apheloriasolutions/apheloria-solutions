"""
Escribe data/productos.json con una estructura única para toda la web:

  {id, nombre, categoria, familia, refs[], specs[{etiqueta,valor}], imagenes[], descargas[], generada}

  - generada = true  -> ficha nueva: una por producto real, con la tabla sacada de los PDF y
                        fusionada entre todos sus códigos (industrial e interior, de momento).
  - generada = false -> lo que ya había para las demás categorías, convertido a esta misma forma
                        para no perderlo. Se regenerará cuando se apliquen las mismas reglas.

También deja el informe en docs/migracion-fichas/fichas-generadas.md.

Uso:  python generar_json.py "CÓDIGOS GENERALES.xlsx"
"""
import os, re, sys, json, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from construir_productos import construir, RAIZ, SEP, imagenes_de

SALIDA = os.path.join(RAIZ, 'data', 'productos.json')
INFORME = os.path.join(RAIZ, 'docs', 'migracion-fichas', 'fichas-generadas.md')
REHECHAS = {'industrial', 'interior'}

slug = lambda s: re.sub(r'[^a-z0-9]+', '-',
                        ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()).strip('-')


def convertir_antiguas(ruta_json):
    """Pasa las fichas viejas de las categorías aún no rehechas a la estructura nueva."""
    if not os.path.exists(ruta_json):
        return []
    salida = []
    for e in json.load(open(ruta_json, encoding='utf-8')):
        if e.get('categoria') in REHECHAS:
            continue
        if 'tipo' not in e:                       # ya estaba convertida (al regenerar): se mantiene
            e['imagenes'] = imagenes_de(e['refs'])    # ...pero las fotos se recalculan por si cambiaron
            e.setdefault('seccion', e.get('familia', 'Otros'))
            e.setdefault('gama', None)
            salida.append(e)
            continue
        if e['tipo'] == 'producto':
            salida.append({'id': slug(e['nombre'] + '-' + e['ref']), 'nombre': e['nombre'],
                           'categoria': e['categoria'], 'seccion': e['subfamilia'], 'gama': None,
                           'familia': e['subfamilia'], 'refs': [e['ref']],
                           'specs': e['specs'], 'imagenes': imagenes_de([e['ref']]),
                           'descargas': [{'ref': e['ref'], 'titulo': e['ref'], 'pdf': e['pdf_path']}],
                           'generada': False})
        else:
            salida.append({'id': e['grupo_id'], 'nombre': e['nombre'], 'categoria': e['categoria'],
                           'seccion': e['subfamilia'], 'gama': None,
                           'familia': e['subfamilia'], 'refs': [v['ref'] for v in e['variantes']],
                           'specs': [{'etiqueta': s['etiqueta'], 'valor': SEP.join(s['valores'])}
                                     for s in e['specs_resumen']],
                           'imagenes': imagenes_de([v['ref'] for v in e['variantes']]),
                           'descargas': [{'ref': v['ref'], 'titulo': v['ref'], 'pdf': v['pdf_path']}
                                         for v in e['variantes']],
                           'generada': False})
    return salida


def informe(fichas, inc):
    n_gen = [f for f in fichas if f['generada']]
    L = ['# Fichas generadas desde los PDF', '',
         'Una ficha por producto real (no por código): los códigos que son el mismo producto con',
         'distinta potencia, temperatura de color, mA o acabado se fusionan en una sola tabla, y los',
         'valores que cambian entre ellos van separados por " | ". La tabla sale **del PDF**; el Excel',
         'solo aporta la corriente en mA y qué códigos son el mismo producto.', '',
         f'- **{len(n_gen)} fichas generadas** a partir de {sum(len(f["refs"]) for f in n_gen)} códigos '
         f'({sum(f["categoria"] == "industrial" for f in n_gen)} industrial, '
         f'{sum(f["categoria"] == "interior" for f in n_gen)} interior).',
         f'- {len(fichas) - len(n_gen)} fichas de las demás categorías siguen con los datos antiguos '
         '(`"generada": false`), pendientes de aplicarles el mismo criterio.', '']

    L += ['## Códigos del Excel sin PDF en el repo', '',
          f'{len(inc["sin_pdf"])} códigos de INDUSTRIAL TODO / INTERIORES TODO no tienen ficha PDF, '
          'así que no aportan nada a la tabla. Hay que pedirlos o confirmar que ya no se venden.', '',
          '| Código | Descripción del Excel |', '|---|---|']
    L += [f'| `{x["codigo"]}` | {x["descripcion"][:110]} |' for x in sorted(inc['sin_pdf'], key=lambda x: x['codigo'])]

    L += ['', '## PDF que no se han podido leer', '']
    if inc['pdf_ilegible']:
        L += ['| Código | PDF | Motivo |', '|---|---|---|']
        L += [f'| `{x["codigo"]}` | `{x["pdf"]}` | {x["motivo"]} |' for x in inc['pdf_ilegible']]
    else:
        L.append('Ninguno: todas las fichas encontradas se han leído bien.')

    L += ['', '## Códigos con más de un PDF posible', '']
    if inc['pdf_ambiguo']:
        L += ['Se ha usado el primero. Conviene comprobar cuál es el bueno.', '',
              '| Código | PDFs |', '|---|---|']
        L += [f'| `{x["codigo"]}` | {"<br>".join("`" + p + "`" for p in x["pdfs"])} |' for x in inc['pdf_ambiguo']]
    else:
        L.append('Ninguno.')

    L += ['', '## Fichas generadas', '', '| Categoría | Familia | Ficha | Códigos | Filas | Fotos |', '|---|---|---|---|---|---|']
    L += [f'| {f["categoria"]} | {f["familia"]} | {f["nombre"]} | {len(f["refs"])} | {len(f["specs"])} | {len(f["imagenes"])} |'
          for f in n_gen]
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    nuevas, inc = construir(sys.argv[1])
    for f in nuevas:
        f['generada'] = True
    fichas = nuevas + convertir_antiguas(SALIDA)
    json.dump(fichas, open(SALIDA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(INFORME, 'w', encoding='utf-8').write(informe(fichas, inc))
    print(f"data/productos.json: {len(fichas)} fichas ({len(nuevas)} generadas, {len(fichas)-len(nuevas)} antiguas)")
    print(f"informe: {os.path.relpath(INFORME, RAIZ)}")
    for k, v in inc.items():
        print(f"  {k}: {len(v)}")
