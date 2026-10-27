"""
Agranda el dibujo de medidas en las fichas donde sale diminuto.

En la columna derecha de la ficha van, de arriba abajo: la foto del producto, el dibujo
acotado con sus marcas de corte, y la curva fotométrica. En las tiras de LED el dibujo es
muy apaisado y queda en 116 x 45 pt, con las cotas ilegibles, mientras la curva se lleva
146 pt de alto.

Lo que se hace: encoger la curva y dar ese hueco al bloque de medidas, que además se
estira hasta el ancho de la columna. El bloque se mueve entero —dibujo, tijera y medida
de corte— para no romper la relación entre ellos.

Se trabaja por recorte de la página, no imagen a imagen: se rasteriza la zona tal y como
se ve y se vuelve a colocar al tamaño nuevo, así da igual cómo esté montada por dentro.

Uso:  python scripts/catalogo/agrandar_medidas.py [--probar CÓDIGO]
"""
import argparse
import io
import json
import os

import fitz
import numpy as np
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
FICHAS = os.path.join(RAIZ, 'fichas')

COLUMNA = (325.0, 505.0)      # la columna derecha de la plantilla
DPI = 400                     # con qué finura se rasteriza antes de agrandar
CRECE_MINIMO = 1.15           # si no va a crecer al menos esto, no se toca
ANCHO_MINIMO = 60.0           # por debajo de esto no es un dibujo acotado, es una mota
ALTO_MINIMO = 14.0
ENCOGER_CURVA = 0.72          # cuánto se queda la curva fotométrica
AIRE = 8.0
MARCA = 'medidas-agrandadas'      # para no pasar dos veces por la misma ficha


def huella(img, n=12):
    g = np.asarray(img.convert('L').resize((n, n), Image.LANCZOS), dtype=np.float32)
    return g > g.mean()


def botones(nodo):
    for b in nodo['botones']:
        yield b
    for h in nodo['hijos']:
        yield from botones(h)


def curva_de(doc, pagina, referencia):
    """La curva fotométrica, por parecido con la que se extrajo del Excel."""
    if referencia is None:
        return None
    mejor, dist_mejor = None, 99
    for im in pagina.get_images(full=True):
        try:
            datos = doc.extract_image(im[0])
            img = Image.open(io.BytesIO(datos['image'])).convert('RGB')
        except Exception:
            continue
        d = int((huella(img) != referencia).sum())
        rects = pagina.get_image_rects(im[0])
        if d < dist_mejor and rects and rects[0].x0 > COLUMNA[0] - 10:
            mejor, dist_mejor = rects[0], d
    return mejor if dist_mejor <= 6 else None


def bloque_de_medidas(pagina, curva):
    """La franja entre la foto del producto y la curva, acotada a lo que de verdad tiene
    tinta. Antes se usaba la caja de las imágenes, pero parte del dibujo —cotas como
    "57 mm"— cae fuera de ella, y al recortar por ahí se perdía."""
    derecha = []
    for im in pagina.get_image_info():
        b = fitz.Rect(im['bbox'])
        if b.x0 > COLUMNA[0] - 10 and 340 < b.y0 < curva.y0 - 2:
            derecha.append(b)
    if not derecha:
        return None
    derecha.sort(key=lambda r: r.y0)
    producto = next((r for r in derecha if r.height > 40), None)
    if producto is None:
        return None

    franja = fitz.Rect(COLUMNA[0], producto.y1 + 1, COLUMNA[1], curva.y0 - 1)
    if franja.height < 12:
        return None
    lupa = 150 / 72
    pix = pagina.get_pixmap(clip=franja, matrix=fitz.Matrix(lupa, lupa))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    tinta = (a[:, :, :3] < 238).any(axis=2)
    filas = np.where(tinta.any(axis=1))[0]
    columnas = np.where(tinta.any(axis=0))[0]
    if not len(filas) or not len(columnas):
        return None
    return fitz.Rect(franja.x0 + columnas[0] / lupa, franja.y0 + filas[0] / lupa,
                     franja.x0 + (columnas[-1] + 1) / lupa, franja.y0 + (filas[-1] + 1) / lupa)


def arreglar(ruta, referencias):
    doc = fitz.open(ruta)
    # pasar dos veces encogería la curva otra vez, y así hasta dejarla en nada
    if MARCA in (doc.metadata or {}).get('keywords', ''):
        doc.close()
        return None
    pagina = doc[0]
    curva = curva_de(doc, pagina, referencias.get('angulo'))
    if curva is None:
        doc.close()
        return None
    caja = bloque_de_medidas(pagina, curva)
    # si lo que hay en la franja es una mota suelta, no es el dibujo: en alguna ficha el
    # acotado va por encima de la foto del producto y abajo solo queda un resto
    if caja is None or caja.width < ANCHO_MINIMO or caja.height < ALTO_MINIMO:
        doc.close()
        return None

    # se guardan los dos recortes tal y como se ven ahora
    escala = DPI / 72
    pix_medidas = pagina.get_pixmap(clip=caja, matrix=fitz.Matrix(escala, escala))
    pix_curva = pagina.get_pixmap(clip=curva, matrix=fitz.Matrix(escala, escala))

    # la curva encoge y se queda abajo del todo; el hueco que deja es para las medidas
    alto_curva = curva.height * ENCOGER_CURVA
    ancho_curva = curva.width * ENCOGER_CURVA
    centro = (curva.x0 + curva.x1) / 2
    curva_nueva = fitz.Rect(centro - ancho_curva / 2, curva.y1 - alto_curva,
                            centro + ancho_curva / 2, curva.y1)

    disponible_alto = curva_nueva.y0 - AIRE - caja.y0
    disponible_ancho = COLUMNA[1] - COLUMNA[0]
    factor = min(disponible_ancho / caja.width, disponible_alto / caja.height)
    if factor < CRECE_MINIMO:
        doc.close()
        return None
    ancho, alto = caja.width * factor, caja.height * factor
    medio = (COLUMNA[0] + COLUMNA[1]) / 2
    medidas_nueva = fitz.Rect(medio - ancho / 2, caja.y0, medio + ancho / 2, caja.y0 + alto)

    blanco = fitz.Rect(COLUMNA[0] - 4, caja.y0 - 2, COLUMNA[1] + 4, curva.y1 + 2)
    pagina.draw_rect(blanco, color=None, fill=(1, 1, 1))
    pagina.insert_image(medidas_nueva, pixmap=pix_medidas)
    pagina.insert_image(curva_nueva, pixmap=pix_curva)

    meta = dict(doc.metadata or {})
    meta['keywords'] = (meta.get('keywords') or '') + ' ' + MARCA
    doc.set_metadata(meta)
    provisional = ruta + '.tmp'
    doc.save(provisional, garbage=3, deflate=True)
    doc.close()
    os.replace(provisional, ruta)
    return round(factor, 2), round(caja.width, 1), round(caja.height, 1), round(alto, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--probar', help='solo esta referencia')
    args = ap.parse_args()

    catalogo = json.load(open(DATOS, encoding='utf-8'))
    referencias = {}
    for b in botones(catalogo['arbol']):
        f = (b.get('fotos') or {}).get('angulo')
        if f and os.path.exists(os.path.join(RAIZ, f['ruta'])):
            referencias[b['codigos'][0]] = {'angulo': huella(Image.open(os.path.join(RAIZ, f['ruta'])))}

    hechas = []
    for codigo, refs in sorted(referencias.items()):
        if args.probar and codigo != args.probar:
            continue
        # solo las fichas de origen: las resumidas se montan después, a partir de estas,
        # así que heredan el dibujo ya agrandado. Pasar por ellas las agrandaría dos veces.
        ruta = os.path.join(FICHAS, codigo + '.pdf')
        if os.path.exists(ruta):
            r = arreglar(ruta, refs)
            if r:
                hechas.append((codigo, 'fichas', *r))

    print(f'fichas con el dibujo de medidas agrandado: {len(hechas)}')
    for codigo, _, factor, ancho, antes, ahora in hechas:
        print(f'   {codigo:16s} x{factor}  bloque de {ancho:.0f} pt de ancho, '
              f'{antes} -> {ahora} pt de alto')


if __name__ == '__main__':
    main()
