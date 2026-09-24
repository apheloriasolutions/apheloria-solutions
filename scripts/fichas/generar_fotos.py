"""
Regenera images/productos/<ref>/ con las fotos identificadas por su papel, no numeradas:

    luminaria.jpg   la foto del producto  -> es la que se ve primero en la ficha
    ambiente.jpg    foto de ejemplo en un espacio real
    medidas.jpg     dibujo de cotas

La curva fotométrica NO se guarda: es un diagrama técnico, no una foto de producto (antes se
colaba en la galería de algunas fichas).

Para cada ref se usa el PDF que le asigna data/productos.json. Si una ficha no sigue la plantilla,
se deja lo que ya hubiera en su carpeta y se lista al final.

Uso:  python generar_fotos.py
"""
import os, sys, json
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extraer_fotos import clasificar, componer

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'productos.json')
ROLES = ('luminaria', 'ambiente', 'medidas')       # en este orden salen en la ficha
LADO_MAX, CALIDAD = 1600, 82


def guardar(im, destino):
    if max(im.size) > LADO_MAX:
        im.thumbnail((LADO_MAX, LADO_MAX), Image.LANCZOS)
    im.save(destino, quality=CALIDAD, optimize=True)


def procesar(ref, ruta_pdf):
    """Devuelve la lista de roles guardados, o None si el PDF no sigue la plantilla."""
    try:
        doc, roles, _avisos = clasificar(os.path.join(RAIZ, ruta_pdf))
    except Exception:
        return None
    if 'luminaria' not in roles:
        return None

    carpeta = os.path.join(RAIZ, 'images', 'productos', ref)
    os.makedirs(carpeta, exist_ok=True)
    for f in os.listdir(carpeta):                       # fuera los 01.jpg/02.jpg del método anterior
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            os.remove(os.path.join(carpeta, f))

    guardados = []
    for rol in ROLES:
        if rol in roles:
            try:
                guardar(componer(doc, roles[rol]), os.path.join(carpeta, rol + '.jpg'))
                guardados.append(rol)
            except Exception:
                pass
    return guardados


if __name__ == '__main__':
    fichas = json.load(open(DATOS, encoding='utf-8'))
    pdf_de_ref = {d['ref']: d['pdf'] for f in fichas for d in f['descargas']}

    ok, fallos, sin_medidas = 0, [], []
    for ref, pdf in sorted(pdf_de_ref.items()):
        res = procesar(ref, pdf)
        if res is None:
            fallos.append((ref, pdf))
        else:
            ok += 1
            if 'medidas' not in res:
                sin_medidas.append(ref)

    print(f"{ok} refs con fotos por rol · {len(fallos)} sin poder clasificar · {len(sin_medidas)} sin dibujo de medidas")
    for ref, pdf in fallos[:15]:
        print(f"   sin clasificar: {ref}  ({pdf})")
    if len(fallos) > 15:
        print(f"   ... y {len(fallos) - 15} más")
