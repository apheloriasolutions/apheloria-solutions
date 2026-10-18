"""
Endereza las imágenes que en las fichas salen deformadas.

En el Excel hay fotos y planos metidos en un recuadro con una proporción que no es la suya:
al pasar a PDF se estiran o se aplastan. El caso más bestia es un panel de 941x305 px
dibujado en un recuadro de 226x192 pt, más del doble de lo que le toca.

Aquí se vuelven a colocar dentro de su mismo recuadro, pero con su proporción: se tapa de
blanco solo la franja que sobra y se dibuja la imagen encima, así no se toca nada de
alrededor. La imagen no crece: como mucho se queda igual de ancha o igual de alta.

Se pasa después de convertir_pdf.py y antes de fichas_resumidas.py.

Uso:  python scripts/catalogo/enderezar_fichas.py [--solo CÓDIGO]
"""
import argparse
import glob
import os

import fitz

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHAS = os.path.join(RAIZ, 'fichas')
DESVIO = 1.08        # por debajo de esto no se nota y no se toca
MINIMO = 25          # puntos: por debajo son iconos y sellos, no fotos


def enderezar(pagina):
    """Devuelve cuántas imágenes se han recolocado en esta página."""
    hechas = 0
    for info in pagina.get_image_info(xrefs=True):
        caja = fitz.Rect(info['bbox'])
        if caja.width < MINIMO or caja.height < MINIMO or not info.get('xref'):
            continue
        natural = info['width'] / info['height']
        if not natural:
            continue
        dibujada = caja.width / caja.height
        if max(dibujada / natural, natural / dibujada) < DESVIO:
            continue

        lado = min(caja.width / natural, caja.height)
        ancho, alto = lado * natural, lado
        x = caja.x0 + (caja.width - ancho) / 2
        y = caja.y0 + (caja.height - alto) / 2
        destino = fitz.Rect(x, y, x + ancho, y + alto)

        # solo se borra lo que deja de estar ocupado, nunca el resto de la hoja
        if destino.width < caja.width - 0.5:
            pagina.draw_rect(fitz.Rect(caja.x0, caja.y0, destino.x0, caja.y1),
                             color=None, fill=(1, 1, 1))
            pagina.draw_rect(fitz.Rect(destino.x1, caja.y0, caja.x1, caja.y1),
                             color=None, fill=(1, 1, 1))
        if destino.height < caja.height - 0.5:
            pagina.draw_rect(fitz.Rect(caja.x0, caja.y0, caja.x1, destino.y0),
                             color=None, fill=(1, 1, 1))
            pagina.draw_rect(fitz.Rect(caja.x0, destino.y1, caja.x1, caja.y1),
                             color=None, fill=(1, 1, 1))
        try:
            pagina.insert_image(destino, xref=info['xref'])
        except Exception:
            continue
        hechas += 1
    return hechas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solo', help='solo esta ficha')
    args = ap.parse_args()

    archivos = sorted(glob.glob(os.path.join(FICHAS, '*.pdf')))
    if args.solo:
        archivos = [a for a in archivos if args.solo.lower() in os.path.basename(a).lower()]

    tocadas, imagenes = 0, 0
    for ruta in archivos:
        doc = fitz.open(ruta)
        n = sum(enderezar(p) for p in doc)
        if n:
            doc.save(ruta + '.tmp', garbage=4, deflate=True)
            doc.close()
            os.replace(ruta + '.tmp', ruta)
            tocadas += 1
            imagenes += n
        else:
            doc.close()
    print(f'{FICHAS}: {imagenes} imágenes enderezadas en {tocadas} fichas')


if __name__ == '__main__':
    main()
