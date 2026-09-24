"""
Saca de una ficha técnica en PDF de Apheloria las fotos por tipo:
  luminaria.jpg  foto del producto (arriba en la columna derecha)
  medidas.jpg    dibujo de dimensiones (en esta ficha viene en 3 piezas; se recomponen sobre blanco)
  ambiente.jpg   foto de ejemplo en un espacio real (columna izquierda, debajo de la tabla)
  curva.jpg      curva fotométrica (abajo en la columna derecha), por si se quiere usar
Descarta el logo de cabecera, el del pie y la franja de iconos de certificación.

Las reglas son relativas (qué imagen va primero o última en cada columna) y no coordenadas fijas,
para que sigan funcionando aunque la tabla sea más larga o más corta. Solo se ha probado con
00EMEEXITS150.pdf: hay que validarlas con más fichas mirando la hoja de contactos.

Uso:  python extraer_fotos.py ficha.pdf carpeta_salida
"""
import pymupdf as fitz, io, sys, os
from PIL import Image

COL_X = 330        # divide la columna izquierda (tabla, ambiente) de la derecha (luminaria, medidas, curva)
CABECERA_Y = 165   # por encima de esta altura solo está el logo de cabecera

def a_pil(doc, xref):
    """Imagen incrustada -> PIL sobre blanco. Hay que aplicar a mano la /SMask del PDF (la máscara de
    transparencia va como una imagen aparte); si no, las zonas transparentes salen NEGRAS."""
    info = doc.extract_image(xref)
    im = Image.open(io.BytesIO(info["image"]))
    if info.get("smask"):
        mascara = Image.open(io.BytesIO(doc.extract_image(info["smask"])["image"])).convert("L")
        im = im.convert("RGB")
        im.putalpha(mascara if mascara.size == im.size else mascara.resize(im.size))
    if im.mode in ("RGBA", "LA", "P"):
        im = Image.alpha_composite(Image.new("RGBA", im.size, "white"), im.convert("RGBA"))
    return im.convert("RGB")

def clasificar(ruta):
    doc = fitz.open(ruta); p = doc[0]; avisos = []
    imgs = []
    for i in p.get_image_info(xrefs=True):
        x0, y0, x1, y1 = i['bbox']
        if y1 < CABECERA_Y or y0 > p.rect.height - 110: continue          # logos de cabecera y pie
        imgs.append(dict(xref=i['xref'], bbox=fitz.Rect(i['bbox']), pequena=(y1 - y0) < 25))
    peq = [i for i in imgs if i['pequena']]; imgs = [i for i in imgs if not i['pequena']]
    cx = lambda i: (i['bbox'].x0 + i['bbox'].x1) / 2
    izq = [i for i in imgs if cx(i) < COL_X]
    der = sorted([i for i in imgs if cx(i) >= COL_X], key=lambda i: i['bbox'].y0)
    roles = {}
    if izq: roles['ambiente'] = [max(izq, key=lambda i: abs(i['bbox']))]   # abs(Rect) = área (PyMuPDF 1.26)
    else: avisos.append('sin foto de ambiente')
    if len(der) < 3:
        avisos.append(f'columna derecha con {len(der)} imágenes (esperaba luminaria + medidas + curva): revisar a mano')
    if der:
        roles['luminaria'] = [der[0]]
        if len(der) >= 3:
            roles['curva'] = [der[-1]]
            arriba, abajo = der[0]['bbox'].y1 - 10, der[-1]['bbox'].y0
            roles['medidas'] = der[1:-1] + [i for i in peq if cx(i) >= COL_X and arriba < (i['bbox'].y0 + i['bbox'].y1) / 2 < abajo]
        elif len(der) == 2:
            roles['medidas'] = [der[1]]
    return doc, roles, avisos

def componer(doc, piezas):
    if len(piezas) == 1: return a_pil(doc, piezas[0]['xref'])
    union = fitz.Rect(piezas[0]['bbox'])
    for pz in piezas[1:]: union |= pz['bbox']
    escala = max(a_pil(doc, pz['xref']).width / pz['bbox'].width for pz in piezas)
    lienzo = Image.new("RGB", (int(union.width * escala), int(union.height * escala)), "white")
    for pz in piezas:
        b = pz['bbox']
        im = a_pil(doc, pz['xref']).resize((int(b.width * escala), int(b.height * escala)), Image.LANCZOS)
        lienzo.paste(im, (int((b.x0 - union.x0) * escala), int((b.y0 - union.y0) * escala)))
    return lienzo

if __name__ == '__main__':
    ruta, salida = sys.argv[1], sys.argv[2]; os.makedirs(salida, exist_ok=True)
    doc, roles, avisos = clasificar(ruta)
    for rol, piezas in roles.items():
        im = componer(doc, piezas); im.save(f"{salida}/{rol}.jpg", quality=90)
        print(f"{rol:10} {im.size[0]}x{im.size[1]} px  (piezas: {len(piezas)})")
    for a in avisos: print("AVISO:", a)
