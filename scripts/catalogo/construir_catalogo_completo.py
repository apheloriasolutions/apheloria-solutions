"""
El catálogo entero en un solo PDF: cada categoría con sus fichas detrás.

De dónde sale cada cosa:
  - las 10 carátulas, de "General - páginas sueltas.pdf" (el A3 ya partido en dos A4:
    impar el texto, par las imágenes);
  - las fichas, de fichas/*.pdf, una página por referencia;
  - la portada y la hoja de "Otros equipos", dibujadas aquí.

El reparto de productos por categoría no sigue la familia de la web, sino la forma de
montaje, que es como están partidas las carátulas: Interiores se reparte entre superficie,
empotrables y carril, y lo mismo Exteriores.

Salida: docs/catalogo/catalogo-completo.pdf y, al lado, una copia ligera para correo.

Uso:  python scripts/catalogo/construir_catalogo_completo.py
"""
import json
import os
import subprocess
import sys

import fitz

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB = os.path.join(RAIZ, 'js', 'catalogo-web.js')
RESUMIDAS = os.path.join(RAIZ, 'fichas', 'resumidas')
CARATULAS = os.path.expanduser('~/Desktop/Jordi Barrachina/Finales/General - páginas sueltas.pdf')
SALIDA = os.path.join(RAIZ, 'docs', 'catalogo', 'catalogo-completo.pdf')

ORO = (0.69, 0.66, 0.60)
TINTA = (0.10, 0.086, 0.07)

# Las diez carátulas, en el orden en que vienen en el PDF. Cada una ocupa dos páginas.
SECCIONES = [
    (1, 'Interiores'),
    (2, 'Interiores · De superficie (pared o techo)'),
    (3, 'Interiores · Proyectores para carril electrificado'),
    (4, 'Interiores · Empotrables (techo o pared)'),
    (5, 'Exteriores'),
    (6, 'Exteriores · Empotrables (techo, pared y suelo)'),
    (7, 'Decorativas'),
    (8, 'Industrial'),
    (9, 'Hospitalaria'),
    (10, 'Emergencia'),
]
OTROS = 0


def productos(nodo, ruta=()):
    for p in nodo.get('productos', []):
        yield ruta, p
    for h in nodo.get('hijos', []):
        yield from productos(h, ruta + (h['nombre'],))


def seccion_de(ruta, prod):
    """A qué carátula pertenece un producto. Manda la forma de montaje, no la familia."""
    r = ' › '.join(ruta)
    nombre = prod['nombre'].lower()
    gran = ruta[0] if ruta else ''
    if gran == 'Emergencia':
        return 10
    if gran == 'Hospitalarias - Salas Blancas':
        return 9
    if gran == 'Decorativas':
        return 7
    if gran == 'Industriales':
        return 8
    if gran == 'Exteriores':
        return 6 if 'empotr' in nombre else 5
    if gran == 'Interiores':
        if 'Proyectores de Carril' in r:
            return 3
        if 'Downlights Empotrados' in r:
            return 4
        if 'Downlights de Superficie' in r:
            return 2
        if 'Retro Gold' in r:
            if 'Proyector' in r:
                return 3
            if 'Colgante' in r:
                return 7
            return 4 if 'Empotrada' in r else 2
        if 'Tiras y Perfiles LED' in r:
            if 'Accesorios' in r:
                return OTROS
            if 'Perfiles para Empotrar' in r:
                return 4
            if 'Perfiles de Aluminio' in r:
                return 2
            return 1                       # las tiras valen para cualquier montaje
        if 'Lineales' in r or 'Especiales Muebles' in r:
            return 4 if 'empotr' in nombre else 2
        return 1
    return OTROS                           # bombillas y fuentes de alimentación


def hojas_de(prod):
    """Las páginas de un producto: la resumida si la tiene, y si no, una por referencia.
    La resumida la genera scripts/catalogo/fichas_resumidas.py."""
    if prod['fichas']:
        resumida = os.path.join(RESUMIDAS, prod['fichas'][0]['codigo'] + '.pdf')
        if os.path.exists(resumida):
            return [resumida]
    return [os.path.join(RAIZ, f['pdf']) for f in prod['fichas']]


def hoja_de_titulo(doc, ancho, alto, titulo, subtitulo=None, portada=False):
    pagina = doc.new_page(-1, width=ancho, height=alto)
    icono = os.path.join(RAIZ, 'logo-icon.png')
    if os.path.exists(icono):
        lado = ancho * (0.17 if portada else 0.10)
        arriba = alto * (0.26 if portada else 0.34)
        pagina.insert_image(fitz.Rect((ancho - lado) / 2, arriba,
                                      (ancho + lado) / 2, arriba + lado), filename=icono)

    def centrado(texto, y, tam, color, espaciado=0):
        if espaciado:
            texto = (' ' * espaciado).join(texto)
        w = fitz.get_text_length(texto, fontname='helv', fontsize=tam)
        pagina.insert_text(((ancho - w) / 2, y), texto, fontname='helv', fontsize=tam, color=color)

    if portada:
        centrado('APHELORIA SOLUTIONS', alto * 0.49, 15, TINTA, espaciado=1)
        centrado(titulo, alto * 0.565, 27, TINTA)
        centrado('Iluminación técnica y material eléctrico', alto * 0.60, 10.5, ORO)
        pagina.draw_line(fitz.Point(ancho * 0.38, alto * 0.525),
                         fitz.Point(ancho * 0.62, alto * 0.525), color=ORO, width=0.6)
    else:
        centrado(titulo, alto * 0.52, 20, TINTA)
        if subtitulo:
            centrado(subtitulo, alto * 0.56, 10, ORO)
        pagina.draw_line(fitz.Point(ancho * 0.35, alto * 0.49),
                         fitz.Point(ancho * 0.65, alto * 0.49), color=ORO, width=0.6)
    centrado('www.apheloria.es', alto * 0.93, 9, ORO)
    return pagina


def main():
    texto = open(WEB, encoding='utf-8').read()
    arbol = json.loads(texto[texto.index('{', texto.index('=')):texto.rindex('}') + 1])

    por_seccion = {}
    for ruta, p in productos(arbol):
        por_seccion.setdefault(seccion_de(ruta, p), []).append((ruta, p))

    caratulas = fitz.open(CARATULAS)
    if len(caratulas) != 20:
        raise SystemExit(f'{CARATULAS} tiene {len(caratulas)} páginas; esperaba 20')

    salida = fitz.open()
    ancho, alto = caratulas[0].rect.width, caratulas[0].rect.height
    hoja_de_titulo(salida, ancho, alto, 'Catálogo General', portada=True)

    indice, resumen = [], []
    for numero, nombre in SECCIONES:
        lista = por_seccion.get(numero, [])
        indice.append([1, nombre, len(salida) + 1])
        salida.insert_pdf(caratulas, from_page=(numero - 1) * 2, to_page=(numero - 1) * 2 + 1)
        fichas = 0
        for _, p in lista:
            if not p['fichas']:
                continue
            indice.append([2, p['nombre'], len(salida) + 1])
            for ruta_pdf in hojas_de(p):
                if not os.path.exists(ruta_pdf):
                    print(f'   FALTA {os.path.basename(ruta_pdf)}')
                    continue
                with fitz.open(ruta_pdf) as fd:
                    salida.insert_pdf(fd)
                fichas += 1
        resumen.append((nombre, len(lista), fichas))

    sueltos = por_seccion.get(OTROS, [])
    if sueltos:
        indice.append([1, 'Otros equipos', len(salida) + 1])
        hoja_de_titulo(salida, ancho, alto, 'Otros equipos',
                       'Fuentes de alimentación, controladores y bombillas')
        fichas = 0
        for _, p in sueltos:
            if not p['fichas']:
                continue
            indice.append([2, p['nombre'], len(salida) + 1])
            for ruta_pdf in hojas_de(p):
                if os.path.exists(ruta_pdf):
                    with fitz.open(ruta_pdf) as fd:
                        salida.insert_pdf(fd)
                    fichas += 1
        resumen.append(('Otros equipos', len(sueltos), fichas))

    salida.set_toc(indice)
    salida.set_metadata({'title': 'Apheloria Solutions — Catálogo General',
                         'author': 'Apheloria Solutions, S.L.',
                         'subject': 'Iluminación técnica y material eléctrico'})
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    salida.save(SALIDA, garbage=4, deflate=True)
    total = len(salida)
    salida.close()
    caratulas.close()

    # La copia ligera va en un proceso aparte: recomprimir las imágenes de las carátulas
    # hace que PyMuPDF se caiga con SIGBUS, y así no se lleva por delante el catálogo.
    correo = SALIDA.replace('.pdf', '-correo.pdf')
    hecho = ligero()

    print(f'{SALIDA}')
    print(f'  {total} páginas · {os.path.getsize(SALIDA) / 1048576:.1f} MB')
    if hecho:
        print(f'  copia para correo: {os.path.getsize(correo) / 1048576:.1f} MB')
    else:
        print('  la copia para correo ha fallado al recomprimir las imágenes')
    print()
    print(f'  {"sección":52s} productos  fichas')
    for nombre, n_prod, n_fichas in resumen:
        print(f'  {nombre:52s} {n_prod:>9} {n_fichas:>7}')


LOGOS = {(214, 214), (314, 314), (580, 81), (594, 83), (578, 81), (600, 84), (192, 192)}
DPI_CORREO = 110
CALIDAD = 62


def aligerar(doc):
    """Recomprime las fotos para el correo, pero NO los logos.

    rewrite_images aplastaba también el logo del pie: lo bajaba a 110 dpi y, al reescribir
    el PNG con transparencia, el dorado salía gris. Aquí se va imagen por imagen, se saltan
    los logos de la plantilla y el resto se reduce a la resolución con la que se dibuja.
    """
    import io
    from PIL import Image

    dibujadas = {}
    for pagina in doc:
        for i in pagina.get_image_info(xrefs=True):
            if not i.get('xref'):
                continue
            caja = fitz.Rect(i['bbox'])
            previo = dibujadas.get(i['xref'], (0, 0))
            dibujadas[i['xref']] = (max(previo[0], caja.width), max(previo[1], caja.height))

    # replace_image vive en la página, no en el documento, y hay que decirle en cuál
    donde = {}
    for pagina in doc:
        for i in pagina.get_image_info(xrefs=True):
            if i.get('xref'):
                donde.setdefault(i['xref'], pagina.number)

    tocadas = 0
    for xref, (ancho_pt, alto_pt) in dibujadas.items():
        try:
            datos = doc.extract_image(xref)
        except Exception:
            continue
        if (datos['width'], datos['height']) in LOGOS or not ancho_pt:
            continue
        objetivo = max(1, round(ancho_pt / 72 * DPI_CORREO))
        if datos['width'] <= objetivo * 1.1:
            continue
        try:
            im = Image.open(io.BytesIO(datos['image']))
            if im.mode in ('RGBA', 'LA', 'P'):
                fondo = Image.new('RGBA', im.size, (255, 255, 255, 255))
                im = Image.alpha_composite(fondo, im.convert('RGBA'))
            im = im.convert('RGB')
            alto = max(1, round(im.height * objetivo / im.width))
            im = im.resize((objetivo, alto), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, 'JPEG', quality=CALIDAD, optimize=True, progressive=True)
            doc[donde[xref]].replace_image(xref, stream=buf.getvalue())
            tocadas += 1
        except Exception:
            continue
    return tocadas


def ligero(tramo=None):
    """La copia para correo, con las fotos recomprimidas y los logos intactos.

    Se hace por tramos y cada uno en su propio proceso: con el documento entero en memoria
    la recompresión se cae con SIGBUS, y no es por ninguna página en concreto sino por el
    tamaño.
    """
    correo = SALIDA.replace('.pdf', '-correo.pdf')
    if tramo is not None:
        a, b = tramo
        doc = fitz.open(SALIDA)
        doc.select(list(range(a, b)))
        aligerar(doc)
        doc.save(f'{correo}.{a:04d}', garbage=4, deflate=True, clean=True)
        doc.close()
        return True

    total = fitz.open(SALIDA).page_count
    PASO = 32
    trozos = []
    for a in range(0, total, PASO):
        b = min(a + PASO, total)
        hecho = any(subprocess.run([sys.executable, os.path.abspath(__file__),
                                    '--ligero', str(a), str(b)],
                                   capture_output=True).returncode == 0 for _ in range(3))
        if not hecho:
            return False
        trozos.append(f'{correo}.{a:04d}')

    salida = fitz.open()
    for t in trozos:
        with fitz.open(t) as d:
            salida.insert_pdf(d)
        os.remove(t)
    base = fitz.open(SALIDA)
    salida.set_toc(base.get_toc())
    salida.set_metadata(base.metadata or {})
    base.close()
    salida.save(correo, garbage=4, deflate=True)
    salida.close()
    return True


if __name__ == '__main__':
    if '--ligero' in sys.argv:
        resto = [x for x in sys.argv[2:] if x.isdigit()]
        ligero((int(resto[0]), int(resto[1])) if len(resto) == 2 else None)
    else:
        main()
