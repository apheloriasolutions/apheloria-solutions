"""
Escribe docs/catalogo/textos.md: los textos de cabecera de cada pantalla de Productos,
en forma de árbol, a partir de data/textos.json.

Los textos se editan en data/textos.json y se publican con construir_web.py.

Uso:  python scripts/catalogo/informe_textos.py
"""
import html, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
TEXTOS = os.path.join(RAIZ, 'data', 'textos.json')
DOCS = os.path.join(RAIZ, 'docs', 'catalogo')


def primera_foto(nodo, tipo):
    for b in nodo['botones']:
        f = (b.get('fotos') or {}).get(tipo)
        if f:
            return f['ruta']
    for h in nodo['hijos']:
        f = primera_foto(h, tipo)
        if f:
            return f
    return None


def cuenta(nodo):
    return len(nodo['botones']) + sum(cuenta(h) for h in nodo['hijos'])


def recorrer(nodo, ruta=(), prof=0):
    yield '/'.join(ruta), nodo, prof
    for h in nodo['hijos']:
        yield from recorrer(h, ruta + (h['slug'],), prof + 1)


def main():
    cat = json.load(open(DATOS, encoding='utf-8'))
    textos = json.load(open(TEXTOS, encoding='utf-8'))
    filas = list(recorrer(cat['arbol']))
    n_borradores = sum(1 for _, v in textos.items() if v.get('borrador'))

    # ── Markdown ──
    L = ['# Productos — textos de cabecera', '',
         'Se editan a mano en `data/textos.json` y se publican volviendo a ejecutar',
         '`python scripts/catalogo/construir_web.py`. Un texto vacío no se muestra.', '',
         'Los marcados **(borrador)** los he redactado yo a partir de las descripciones de sus',
         'productos; los demás venían ya de la web anterior.', '',
         'Para ver cómo quedan: `docs/catalogo/productos.html`.', '']
    for clave, nodo, prof in filas:
        t = textos.get(clave, {})
        L.append(f"{'  ' * prof}- **{nodo['nombre']}** `#{clave}`"
                 + (' *(borrador)*' if t.get('borrador') else ''))
        if t.get('texto'):
            L.append(f"{'  ' * prof}  {t['texto']}")
    os.makedirs(DOCS, exist_ok=True)
    open(os.path.join(DOCS, 'textos.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    print(f'{DOCS}/textos.md: {len(filas)} pantallas · {n_borradores} borradores')


if __name__ == '__main__':
    main()
