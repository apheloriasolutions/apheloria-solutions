"""
Escribe los dos informes de los textos de cabecera a partir de data/textos.json:

  docs/catalogo/textos.html   para revisarlos en el navegador, con su foto y un enlace
                              que abre esa misma pantalla en la web
  docs/catalogo/textos.md     el mismo árbol en texto

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

    # ── HTML ──
    # Las fotos van sin loading="lazy": abriendo el archivo suelto (file://) no llegan a cargarse.
    bloques = []
    for clave, nodo, prof in filas:
        t = textos.get(clave, {})
        foto = primera_foto(nodo, 'ambiente')
        rel = os.path.relpath(os.path.join(RAIZ, foto), DOCS) if foto else None
        etiqueta = ('<span class="marca borrador">borrador</span>' if t.get('borrador')
                    else '<span class="marca heredado">de la web anterior</span>')
        bloques.append(f'''<article class="fila" style="--prof:{prof}" id="{html.escape(clave)}">
  <div class="foto">{f'<img src="{html.escape(rel)}" alt="">' if rel else ''}</div>
  <div class="cuerpo">
    <h2>{html.escape(nodo['nombre'])} {etiqueta}</h2>
    <p class="meta"><a href="../../productos.html#{html.escape(clave)}" target="_blank"
       >#{html.escape(clave) or '(portada)'} ↗</a> · {cuenta(nodo)} productos</p>
    <p class="texto{'' if t.get('texto') else ' vacio'}">{html.escape(t.get('texto') or
       'Sin texto: esta cabecera sale solo con el título.')}</p>
  </div>
</article>''')

    doc = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Textos de cabecera — revisión</title><style>
 body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 1.5rem;
        background: #F2EDE4; color: #1a1612; }}
 h1 {{ font-size: 1.3rem; font-weight: 500; margin: 0 0 .3rem; }}
 .resumen {{ font-size: .85rem; color: #857a68; margin: 0 0 1.5rem; max-width: 70ch; line-height: 1.6; }}
 .fila {{ display: grid; grid-template-columns: 150px 1fr; gap: 1.1rem;
          background: #fff; border: 1px solid #e6e0d6; padding: .9rem;
          margin: 0 0 .6rem calc(var(--prof) * 1.6rem); }}
 .foto {{ aspect-ratio: 3/2; background: #f4f0e9; overflow: hidden;
          display: flex; align-items: center; justify-content: center; }}
 .foto img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
 h2 {{ font-size: .98rem; font-weight: 600; margin: 0 0 .25rem; }}
 .marca {{ font-size: .62rem; font-weight: 500; text-transform: uppercase; letter-spacing: .08em;
           padding: .12rem .45rem; border-radius: 3px; vertical-align: .12em; }}
 .borrador {{ background: #f6e7cd; color: #8a6a24; }}
 .heredado {{ background: #e4ece2; color: #4a6b47; }}
 .meta {{ font-size: .72rem; color: #857a68; margin: 0 0 .5rem; }}
 .meta a {{ color: #857a68; }}
 .texto {{ font-size: .88rem; line-height: 1.65; margin: 0; max-width: 78ch; }}
 .vacio {{ color: #a34a3f; font-style: italic; }}
 @media (max-width: 700px) {{
   .fila {{ grid-template-columns: 1fr; margin-left: calc(var(--prof) * .5rem); }}
   .foto {{ max-height: 150px; }}
 }}
</style></head><body>
<h1>Textos de cabecera de Productos</h1>
<p class="resumen">{len(filas)} pantallas · {n_borradores} borradores · {len(filas) - n_borradores}
heredadas de la web anterior. La foto es la que sale en la cabecera de esa pantalla.
Pulsa la dirección para abrirla en la web. Se editan en <code>data/textos.json</code> y se
publican volviendo a ejecutar <code>scripts/catalogo/construir_web.py</code>; si dejas el
texto vacío, la cabecera sale solo con el título.</p>
{''.join(bloques)}
</body></html>
"""
    os.makedirs(DOCS, exist_ok=True)
    open(os.path.join(DOCS, 'textos.html'), 'w', encoding='utf-8').write(doc)

    # ── Markdown ──
    L = ['# Productos — textos de cabecera', '',
         'Se editan a mano en `data/textos.json` y se publican volviendo a ejecutar',
         '`python scripts/catalogo/construir_web.py`. Un texto vacío no se muestra.', '',
         'Los marcados **(borrador)** los he redactado yo a partir de las descripciones de sus',
         'productos; los demás venían ya de la web anterior.', '',
         'Para verlos con su foto: `docs/catalogo/textos.html`.', '']
    for clave, nodo, prof in filas:
        t = textos.get(clave, {})
        L.append(f"{'  ' * prof}- **{nodo['nombre']}** `#{clave}`"
                 + (' *(borrador)*' if t.get('borrador') else ''))
        if t.get('texto'):
            L.append(f"{'  ' * prof}  {t['texto']}")
    open(os.path.join(DOCS, 'textos.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    print(f'{DOCS}/textos.html y textos.md: {len(filas)} pantallas · {n_borradores} borradores')


if __name__ == '__main__':
    main()
