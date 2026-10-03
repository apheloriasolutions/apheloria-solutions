"""
Escribe docs/catalogo/productos.html: todas las pantallas de Productos, una detrás de otra,
para poder revisar de un vistazo cómo ha quedado la sección sin ir pulsando una por una.

No reescribe el diseño: abre la web de verdad y copia lo que pinta js/productos.js, con
sus mismas hojas de estilo. Lo que se ve aquí es exactamente lo que se ve en la web.

Necesita playwright.  Uso:  python scripts/catalogo/hoja_productos.py
"""
import html, json, os, re

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'js', 'catalogo-web.js')
SALIDA = os.path.join(RAIZ, 'docs', 'catalogo', 'productos.html')


def cargar():
    t = open(DATOS, encoding='utf-8').read()
    return json.loads(t[t.index('{'):t.rindex('}') + 1])


def recorrer(nodo, ruta=()):
    yield '/'.join(ruta), nodo['nombre'], 'pantalla', len(ruta)
    for p in nodo['productos']:
        yield '/'.join(ruta + (p['slug'],)), p['nombre'], 'ficha', len(ruta) + 1
    for h in nodo['hijos']:
        yield from recorrer(h, ruta + (h['slug'],))


def arreglar_rutas(trozo):
    """La hoja vive en docs/catalogo/, dos carpetas por debajo de la web."""
    trozo = re.sub(r'(src|href)="(images/|fichas/)', r'\1="../../\2', trozo)
    trozo = trozo.replace('<img ', '<img loading="lazy" ')
    # los enlaces internos saltan dentro de esta misma hoja
    trozo = re.sub(r'href="#([^"]*)"', lambda m: f'href="#p-{m.group(1)}"', trozo)
    return trozo


def main():
    cat = cargar()
    pantallas = list(recorrer(cat))

    bloques, indice = [], []
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(viewport={'width': 1440, 'height': 900})
        pagina.goto('file://' + os.path.join(RAIZ, 'productos.html'))
        pagina.wait_for_timeout(600)
        for i, (ruta, nombre, tipo, prof) in enumerate(pantallas):
            pagina.evaluate(f'location.hash = {json.dumps(ruta)}')
            pagina.wait_for_timeout(12)
            trozo = pagina.evaluate('document.getElementById("catalogo").innerHTML')
            bloques.append(
                f'<section class="bloque" id="p-{html.escape(ruta)}">'
                f'<p class="rotulo"><span class="tipo tipo-{tipo}">{tipo}</span>'
                f'<a href="../../productos.html#{html.escape(ruta)}" target="_blank">'
                f'#{html.escape(ruta) or "(portada)"} ↗</a></p>'
                f'<div class="pagina pagina-productos">{arreglar_rutas(trozo)}</div></section>')
            indice.append(f'<a href="#p-{html.escape(ruta)}" class="idx idx-{tipo}" '
                          f'style="--prof:{prof}">{html.escape(nombre)}</a>')
            if (i + 1) % 50 == 0:
                print(f'  {i + 1}/{len(pantallas)}', flush=True)
        navegador.close()

    n_fichas = sum(1 for _, _, t, _ in pantallas if t == 'ficha')
    doc = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Productos — cómo ha quedado</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;1,400&family=Inter:wght@200;300;400&family=Montserrat:wght@100;200&family=Raleway:ital,wght@0,300;0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../css/estilos.css">
<link rel="stylesheet" href="../../css/productos.css">
<style>
  /* Esto es una hoja de revisión: no hay barra de navegación ni pie fijos.
     Ojo: en el CSS común la etiqueta <nav> va fija arriba, así que aquí la cabecera
     y el índice son <div>. */
  body {{ padding: 0; }}
  .cabecera {{ padding: 1.6rem 2rem 1.2rem; background: #F2EDE4; }}
  .cabecera h1 {{ font-family: 'Raleway', sans-serif; font-size: 1.2rem; font-weight: 600; }}
  .cabecera p {{ font-family: 'Raleway', sans-serif; font-size: .82rem; color: #857a68;
                 max-width: 78ch; line-height: 1.6; margin-top: .4rem; }}
  .indice {{ columns: 4; column-gap: 2rem; padding: 1rem 2rem 1.8rem; background: #F2EDE4; }}
  .idx {{ display: block; break-inside: avoid; font-family: 'Raleway', sans-serif;
          font-size: .72rem; line-height: 1.75; color: #857a68; text-decoration: none;
          padding-left: calc(var(--prof) * .7rem);
          overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .idx:hover {{ color: #1a1612; text-decoration: underline; }}
  .idx-ficha {{ color: #a09684; }}
  .bloque {{ border-top: 12px solid #F2EDE4; }}
  .rotulo {{ display: flex; align-items: center; gap: .7rem;
             font-family: 'Raleway', sans-serif; font-size: .7rem; letter-spacing: .1em;
             padding: .7rem 3rem; background: #faf7f2; }}
  .rotulo a {{ color: #857a68; text-decoration: none; }}
  .rotulo a:hover {{ color: #1a1612; text-decoration: underline; }}
  .tipo {{ font-size: .6rem; text-transform: uppercase; letter-spacing: .1em;
           padding: .12rem .45rem; border-radius: 3px; }}
  .tipo-pantalla {{ background: #e4ece2; color: #4a6b47; }}
  .tipo-ficha {{ background: #f6e7cd; color: #8a6a24; }}
  /* la miga de pan y la foto de la ficha se quedan fijas al desplazar en la web;
     aquí, al ir todo seguido, estorban */
  .cat-ruta, .ficha-galeria {{ position: static; }}
  @media (max-width: 1100px) {{ .indice {{ columns: 2; }} }}
  @media (max-width: 700px) {{ .indice {{ columns: 1; padding: 1rem 1.5rem; }}
                               .rotulo {{ padding: .7rem 1.5rem; }} }}
</style></head>
<body>
<div class="cabecera">
  <h1>Productos — cómo ha quedado</h1>
  <p>Las {len(pantallas)} pantallas de la sección, una detrás de otra: {len(pantallas) - n_fichas}
  de navegación y {n_fichas} fichas de producto. Está copiado de la web de verdad y con sus mismas
  hojas de estilo, así que se ve igual. Pulsa cualquier dirección para abrirla en la web.
  Para probar la navegación y el botón atrás, abre <code>productos.html</code>.</p>
</div>
<div class="indice">{''.join(indice)}</div>
{''.join(bloques)}
</body></html>
"""
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    open(SALIDA, 'w', encoding='utf-8').write(doc)
    print(f'{SALIDA}: {len(pantallas)} pantallas ({n_fichas} fichas) · {len(doc) / 1024 / 1024:.1f} MB')


if __name__ == '__main__':
    main()
