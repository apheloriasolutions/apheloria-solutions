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
DESVIO = 1.15        # por debajo de esto no se nota y no se toca
MINIMO = 25          # puntos: por debajo son iconos y sellos, no fotos
CABECERA = 165       # puntos desde arriba: ahí vive el logo, no se toca
PIE = 130            # puntos desde abajo: el logo y los datos de contacto


def enderezar(pagina, plantilla=()):
    """Devuelve cuántas imágenes se han recolocado en esta página.

    No se tocan ni los logos de la plantilla, ni nada que caiga en la cabecera o en el pie,
    ni las imágenes con texto encima: ahí el recuadro blanco se comería las cotas."""
    hechas = 0
    textos = [fitz.Rect(b[:4]) for b in pagina.get_text('blocks') if b[6] == 0]
    for info in pagina.get_image_info(xrefs=True):
        caja = fitz.Rect(info['bbox'])
        if caja.width < MINIMO or caja.height < MINIMO or not info.get('xref'):
            continue
        if (info['width'], info['height']) in plantilla:
            continue
        if caja.y0 < CABECERA or caja.y1 > pagina.rect.height - PIE:
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

        franjas = []
        if destino.width < caja.width - 0.5:
            franjas += [fitz.Rect(caja.x0, caja.y0, destino.x0, caja.y1),
                        fitz.Rect(destino.x1, caja.y0, caja.x1, caja.y1)]
        if destino.height < caja.height - 0.5:
            franjas += [fitz.Rect(caja.x0, caja.y0, caja.x1, destino.y0),
                        fitz.Rect(caja.x0, destino.y1, caja.x1, caja.y1)]
        if any(t.intersects(f) for f in franjas for t in textos):
            continue                     # hay texto donde habría que borrar: se deja estar

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

    # Los logos salen en todas las fichas: se reconocen porque su tamaño se repite por todas
    # partes, y así no se tocan aunque vengan con la proporción cambiada.
    from collections import Counter
    cuenta = Counter()
    for ruta in archivos[:80]:
        doc = fitz.open(ruta)
        for pagina in doc:
            for i in {(x['width'], x['height']) for x in pagina.get_image_info()}:
                cuenta[i] += 1
        doc.close()
    plantilla = {t for t, n in cuenta.items() if n > 40}
    print(f'logos de la plantilla, que no se tocan: {sorted(plantilla)}')

    if args.solo:
        archivos = [a for a in archivos if args.solo.lower() in os.path.basename(a).lower()]

    tocadas, imagenes = 0, 0
    for ruta in archivos:
        doc = fitz.open(ruta)
        n = sum(enderezar(p, plantilla) for p in doc)
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
