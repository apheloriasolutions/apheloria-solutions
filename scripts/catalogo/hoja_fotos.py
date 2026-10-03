"""
Genera docs/catalogo/fotos.html: una fila por botón con sus fotos etiquetadas y su tamaño,
para revisarlas todas de un vistazo.

En rojo: las que faltan, las que no llegan a 800 px y las fichas que no siguen la plantilla.

Uso:  python scripts/catalogo/hoja_fotos.py
"""
import html, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
AVISOS = os.path.join(RAIZ, 'docs', 'catalogo', 'avisos-fotos.json')
SALIDA = os.path.join(RAIZ, 'docs', 'catalogo', 'fotos.html')
TIPOS = ('luminaria', 'medidas', 'ambiente')
MINIMO = 800


def botones(nodo, ruta=()):
    for b in nodo['botones']:
        yield ruta, b
    for h in nodo['hijos']:
        yield from botones(h, ruta + (h['nombre'],))


def main():
    catalogo = json.load(open(DATOS, encoding='utf-8'))
    avisos = json.load(open(AVISOS, encoding='utf-8')) if os.path.exists(AVISOS) else {}
    por_codigo = {}
    for clave, lista in avisos.items():
        for texto in lista:
            por_codigo.setdefault(texto.split(':')[0].strip(), []).append(clave)

    filas, n_fotos, n_pequenas, n_faltan = [], 0, 0, 0
    conteo = 0
    for ruta, b in botones(catalogo['arbol']):
        fotos = b.get('fotos')
        if fotos is None:
            continue
        conteo += 1
        celdas = []
        for tipo in TIPOS:
            f = fotos.get(tipo)
            if not f:
                celdas.append(f'<td class="falta">{tipo}<br>no hay</td>')
                n_faltan += 1
                continue
            n_fotos += 1
            w, h = f['px']
            pequena = max(w, h) < MINIMO
            n_pequenas += pequena
            rel = os.path.relpath(os.path.join(RAIZ, f['ruta']), os.path.dirname(SALIDA))
            celdas.append(
                f'<td class="{"pequena" if pequena else ""}">'
                f'<img src="{html.escape(rel)}" loading="lazy" alt="{tipo}">'
                f'<span class="pie">{tipo} · {w}×{h}</span></td>')
        marcas = sorted({m for c in b['codigos'] for m in por_codigo.get(c, [])})
        filas.append(
            '<tr>'
            f'<th><span class="ruta">{html.escape(" › ".join(ruta))}</span>'
            f'<span class="nombre">{html.escape(b["nombre"])}</span>'
            f'<span class="codigos">{html.escape(", ".join(b["codigos"]))}</span>'
            + (f'<span class="aviso">{html.escape(", ".join(marcas))}</span>' if marcas else '')
            + '</th>' + ''.join(celdas) + '</tr>')

    doc = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<title>Fotos de las fichas — revisión</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 1.5rem;
         background: #F2EDE4; color: #1a1612; }}
  h1 {{ font-size: 1.3rem; font-weight: 500; }}
  .resumen {{ font-size: .85rem; color: #857a68; margin-bottom: 1.2rem; }}
  table {{ border-collapse: collapse; width: 100%; background: #fff; }}
  th, td {{ border: 1px solid #e6e0d6; padding: .5rem; vertical-align: top; }}
  th {{ text-align: left; width: 22%; font-weight: 400; }}
  td {{ width: 26%; text-align: center; }}
  img {{ max-width: 100%; max-height: 220px; object-fit: contain; display: block; margin: 0 auto; }}
  .pie {{ display: block; font-size: .72rem; color: #857a68; margin-top: .35rem; }}
  .ruta {{ display: block; font-size: .68rem; text-transform: uppercase; letter-spacing: .08em; color: #857a68; }}
  .nombre {{ display: block; font-weight: 600; margin: .25rem 0; }}
  .codigos {{ display: block; font-size: .72rem; color: #857a68; }}
  .aviso {{ display: inline-block; margin-top: .4rem; font-size: .7rem; color: #fff;
            background: #a34a3f; padding: .15rem .45rem; border-radius: 3px; }}
  .falta {{ background: #fbeceb; color: #a34a3f; font-size: .8rem; }}
  .pequena {{ background: #fdf3e7; }}
  .pequena .pie {{ color: #a34a3f; font-weight: 600; }}
</style></head><body>
<h1>Fotos sacadas de las fichas</h1>
<p class="resumen">{conteo} botones · {n_fotos} fotos · {n_faltan} huecos sin foto ·
{n_pequenas} por debajo de {MINIMO} px (fondo naranja). En rojo, las fichas que no siguen la plantilla.</p>
<table>{''.join(filas)}</table>
</body></html>
"""
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    open(SALIDA, 'w', encoding='utf-8').write(doc)
    print(f'{SALIDA}: {conteo} botones · {n_fotos} fotos · {n_faltan} huecos · {n_pequenas} pequeñas')


if __name__ == '__main__':
    main()
