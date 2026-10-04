"""
Saca las fotos de las fichas .xlsx en su calidad original y prepara la versión para la web.

Un .xlsx es un zip: las imágenes están enteras en xl/media/ y xl/drawings/ dice dónde va cada una.
Se leen de ahí directamente, sin capturas ni conversiones intermedias.

Cómo se decide qué es cada imagen (regla confirmada):
  - Se descartan por contenido las tres fijas de la plantilla (logo de cabecera, logo del pie y la
    franja de certificaciones: aparecen en casi todas las fichas) y los iconos de <=90 px (el del
    ángulo de apertura).
  - Columna izquierda (A-B): la de mayor superficie EN LA HOJA es la foto de ambiente. Si hay más,
    se avisa (en las de emergencia la primera es una tabla de pictogramas).
  - Columna derecha (C en adelante), de arriba abajo: si la última antes de la franja es cuadrada
    (1:1 ±3%) y mide >=350 px, es la curva fotométrica y se descarta. De las que quedan, la primera
    es el producto y el resto son las medidas, que se juntan en una sola imagen.
  - Si tras quitar la curva solo queda una imagen, no se puede saber si es producto o medidas: se
    decide contando manchas con forma de cota y se avisa igualmente.

Cuidado con dos cosas:
  - La transparencia: los PNG llevan canal alfa y hay que componerlos SOBRE BLANCO. Convertirlos a
    RGB directamente deja las zonas transparentes en negro.
  - Las proporciones: se usan siempre las del archivo original, nunca las de la hoja, donde la foto
    de ambiente aparece estirada para encajar en su hueco.

Uso:  python scripts/catalogo/extraer_fotos.py [--solo texto] [--limite N]
"""
import argparse, hashlib, io, json, os, re, sys, zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from PIL import Image

NS = {'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
EMU_CM = 360000

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHAS = os.path.join(RAIZ, 'fuentes', 'fichas')
ORIGINALES = os.path.join(RAIZ, 'fuentes', 'fotos')
WEB = os.path.join(RAIZ, 'images', 'productos')
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')

LADO_MAX, CALIDAD = 1600, 88
ICONO_MAX = 90          # px: por debajo de esto es un icono, no una foto
# La curva fotométrica (el "ángulo lumínico") es el último dibujo de la columna derecha y siempre
# sale aproximadamente cuadrada. Se pide además que haya al menos 3 imágenes a la derecha, para no
# confundirla con el dibujo de cotas en las fichas que solo traen producto y medidas.
ANGULO_PROPORCION = (0.70, 1.25)
ANGULO_MINIMO_DERECHA = 3

avisos = defaultdict(list)

# Fichas con una sola imagen en la columna derecha donde el recuento de manchas se equivoca:
# son dibujos de cotas, no fotos de producto. Comprobadas a ojo una a una — ninguna medida
# automática (manchas, colores, líneas largas) separa un plano gris de una foto en gris.
SOLO_COTAS = {'00PSFB4S2020', '00PERFLEXACER', '00FASO16WCCTK', 'EMS61000',
              '00FUAL20024IP', '00FA36W12VIP2'}

# Fichas sin foto de producto donde la imagen de la izquierda TAMPOCO es de ambiente, sino otro
# plano de cotas: no se asciende a foto de producto. Comprobadas a ojo.
IZQUIERDA_ES_PLANO = {'00FASO16WCCTK', 'EMS61000'}

# Fichas donde el origen trae la columna derecha al revés: primero las cotas y debajo el producto.
INTERCAMBIAR = {'00LAMSP300NG', '00BE6TI20W30K', '00BALIZ8W3KIP'}


# ── lectura del .xlsx ─────────────────────────────────────────────────────────
def imagenes_de(ruta):
    """Lista de imágenes con su anclaje, tamaño real y tamaño en la hoja."""
    z = zipfile.ZipFile(ruta)
    salida = []
    dibujos = sorted([n for n in z.namelist() if re.match(r'xl/drawings/drawing\d+\.xml$', n)],
                     key=lambda n: int(re.search(r'(\d+)', n.split('/')[-1]).group()))
    for dib in dibujos[:1]:     # algunas fichas traen una segunda hoja interna que repite las imágenes
        rels = {}
        rp = dib.replace('drawings/', 'drawings/_rels/') + '.rels'
        if rp in z.namelist():
            for rel in ET.fromstring(z.read(rp)):
                rels[rel.get('Id')] = rel.get('Target', '').split('/')[-1]
        for anc in ET.fromstring(z.read(dib)):
            pic = anc.find('.//xdr:pic', NS)
            de = anc.find('xdr:from', NS)
            if pic is None or de is None:
                continue
            blip = pic.find('.//a:blip', NS)
            if blip is None or blip.get('{%s}embed' % NS['r']) is None:
                continue
            nombre = rels.get(blip.get('{%s}embed' % NS['r']), '')
            try:
                datos = z.read('xl/media/' + nombre)
            except KeyError:
                continue
            ext = pic.find('.//a:xfrm/a:ext', NS)
            cm = ((int(ext.get('cx')) / EMU_CM, int(ext.get('cy')) / EMU_CM)
                  if ext is not None and ext.get('cx') else (0, 0))
            col = int(de.find('xdr:col', NS).text)
            fila = int(de.find('xdr:row', NS).text)
            desp_x = int((de.find('xdr:colOff', NS).text or 0)) / EMU_CM
            desp_y = int((de.find('xdr:rowOff', NS).text or 0)) / EMU_CM
            item = {'nombre': nombre, 'datos': datos, 'col': col, 'fila': fila,
                    'x': col + desp_x, 'y': fila + desp_y, 'cm': cm, 'area_cm': cm[0] * cm[1],
                    'hash': hashlib.md5(datos).hexdigest(),
                    'ext': os.path.splitext(nombre)[1].lower().lstrip('.')}
            try:
                if item['ext'] in ('emf', 'wmf'):
                    raise ValueError('vectorial')     # Pillow la abre pero no sabe leerla
                im = Image.open(io.BytesIO(datos))
                im.load()                             # fuerza la lectura real de los píxeles
                item['px'] = im.size
            except Exception:
                item['px'] = None                     # EMF/WMF y demás vectoriales
            salida.append(item)
    return salida


def hashes_fijos(archivos, umbral=0.5):
    """Las imágenes de plantilla (logos y franja) salen en casi todas las fichas."""
    cuenta = Counter()
    for rel in archivos:
        try:
            vistos = {i['hash'] for i in imagenes_de(os.path.join(FICHAS, rel))}
        except Exception:
            continue
        cuenta.update(vistos)
    return {h for h, n in cuenta.items() if n >= len(archivos) * umbral}


# ── clasificación ─────────────────────────────────────────────────────────────
def manchas_de_cota(im):
    """Las cotas llevan muchas cifras pequeñas; una foto de producto, no."""
    try:
        from scipy import ndimage
        import numpy as np
    except ImportError:
        return 0
    g = im.convert('L').resize((240, int(240 * im.height / im.width)) if im.width else (240, 240))
    arr = np.array(g) < 128
    etiquetas, n = ndimage.label(arr)
    bien = 0
    for corte in ndimage.find_objects(etiquetas):
        alto = corte[0].stop - corte[0].start
        ancho = corte[1].stop - corte[1].start
        if 4 <= alto <= 20 and 3 <= ancho <= 20 and alto >= ancho * 0.6:
            bien += 1
    return bien


def clasificar(imgs, fijos, ref):
    """Devuelve {'luminaria': img, 'medidas': [imgs], 'ambiente': img} y avisa de lo raro."""
    utiles = [i for i in imgs if i['hash'] not in fijos]
    iconos = [i for i in utiles if i['px'] and max(i['px']) <= ICONO_MAX]
    utiles = [i for i in utiles if i not in iconos]
    sin_leer = [i for i in utiles if not i['px']]
    if sin_leer:
        avisos['vectoriales'].append(f"{ref}: {len(sin_leer)} imagen(es) EMF/WMF que no se pueden abrir")
        utiles = [i for i in utiles if i['px']]

    izq = sorted([i for i in utiles if i['col'] <= 1], key=lambda i: -i['area_cm'])
    der = sorted([i for i in utiles if i['col'] > 1], key=lambda i: (i['y'], i['x']))

    roles = {'luminaria': None, 'medidas': [], 'ambiente': None, 'angulo': None}
    if izq:
        roles['ambiente'] = izq[0]
        if len(izq) > 1:
            avisos['izquierda_extra'].append(f"{ref}: {len(izq)-1} imagen(es) más a la izquierda, se ignoran")

    if der:
        ultima = der[-1]
        w, h = ultima['px']
        if len(der) >= ANGULO_MINIMO_DERECHA and ANGULO_PROPORCION[0] <= w / h <= ANGULO_PROPORCION[1]:
            roles['angulo'] = ultima
            der = der[:-1]
        if len(der) == 1:
            unica = der[0]
            cotas = manchas_de_cota(Image.open(io.BytesIO(unica['datos'])))
            if ref in SOLO_COTAS or cotas >= 4:
                roles['medidas'] = [unica]
                avisos['sin_luminaria'].append(f"{ref}: solo hay dibujo de medidas, no hay foto de producto")
            else:
                roles['luminaria'] = unica
                avisos['una_sola_imagen'].append(
                    f"{ref}: una sola imagen a la derecha, se toma como foto de producto (comprobar que no sean cotas)")
        elif der:
            roles['luminaria'] = der[0]
            roles['medidas'] = der[1:]
    # la izquierda a veces repite la foto del producto: entonces no hay foto de ambiente
    if roles['ambiente'] and roles['luminaria'] and roles['ambiente']['hash'] == roles['luminaria']['hash']:
        otras = [i for i in izq if i['hash'] != roles['luminaria']['hash']]
        roles['ambiente'] = otras[0] if otras else None
        if not roles['ambiente']:
            avisos['ambiente_era_el_producto'].append(
                f'{ref}: a la izquierda solo está repetida la foto del producto, no hay foto de ambiente')
    # Fichas de dos fotos (producto + cotas): lo que hay a la izquierda no es ambiente, es el
    # producto. Pasa en los perfiles de aluminio, el controlador y las fuentes de alimentación.
    if not roles['luminaria'] and roles['ambiente'] and ref not in IZQUIERDA_ES_PLANO:
        roles['luminaria'] = roles['ambiente']
        roles['ambiente'] = None
        avisos['izquierda_es_el_producto'].append(
            f'{ref}: la ficha solo trae dos fotos; la de la izquierda se publica como foto de producto')
    if ref in INTERCAMBIAR and roles['luminaria'] and roles['medidas']:
        roles['luminaria'], roles['medidas'] = roles['medidas'][0], [roles['luminaria']]
        avisos['intercambiadas'].append(f'{ref}: en el origen las cotas van antes que el producto, se intercambian')
    if not roles['luminaria']:
        avisos['sin_luminaria'].append(f'{ref}: sin foto de producto')
    if not roles['ambiente']:
        avisos['sin_ambiente'].append(f'{ref}: sin foto de ambiente')
    return roles


# ── imágenes ──────────────────────────────────────────────────────────────────
def sobre_blanco(datos):
    """Abre la imagen y le pone fondo blanco. OJO: convertir a RGB sin componer deja el
    transparente en NEGRO, que es lo que salía mal antes."""
    im = Image.open(io.BytesIO(datos))
    if im.mode == 'P' and 'transparency' in im.info:
        im = im.convert('RGBA')
    if im.mode in ('RGBA', 'LA'):
        fondo = Image.new('RGBA', im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(fondo, im.convert('RGBA'))
    return im.convert('RGB')


def juntar_medidas(piezas):
    """Une las piezas en una sola imagen sobre blanco, respetando su colocación en la hoja."""
    if len(piezas) == 1:
        return sobre_blanco(piezas[0]['datos'])
    # misma escala para todas: se toma la pieza con más píxeles por cm
    escala = max(p['px'][0] / p['cm'][0] for p in piezas if p['cm'][0])
    puestas = []
    for p in piezas:
        im = sobre_blanco(p['datos'])
        ancho = max(1, int(round(p['cm'][0] * escala)))
        alto = max(1, int(round(ancho * im.height / im.width)))     # proporción del original
        puestas.append((p, im.resize((ancho, alto), Image.LANCZOS)))
    filas_solapan = max(p['y'] for p, _ in puestas) - min(p['y'] for p, _ in puestas) < 2
    hueco = int(0.04 * max(im.width for _, im in puestas))
    if filas_solapan:                                               # una al lado de otra
        puestas.sort(key=lambda t: t[0]['x'])
        ancho = sum(im.width for _, im in puestas) + hueco * (len(puestas) - 1)
        alto = max(im.height for _, im in puestas)
        lienzo = Image.new('RGB', (ancho, alto), 'white')
        x = 0
        for _, im in puestas:
            lienzo.paste(im, (x, (alto - im.height) // 2)); x += im.width + hueco
    else:                                                           # una debajo de otra
        puestas.sort(key=lambda t: t[0]['y'])
        ancho = max(im.width for _, im in puestas)
        alto = sum(im.height for _, im in puestas) + hueco * (len(puestas) - 1)
        lienzo = Image.new('RGB', (ancho, alto), 'white')
        y = 0
        for _, im in puestas:
            lienzo.paste(im, ((ancho - im.width) // 2, y)); y += im.height + hueco
    return lienzo


def guardar(im, destino, max_lado=LADO_MAX):
    if max(im.size) > max_lado:                                     # nunca se amplía
        im = im.copy(); im.thumbnail((max_lado, max_lado), Image.LANCZOS)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    im.save(destino, quality=CALIDAD, optimize=True)
    return im.size


# ── recorrido del catálogo ────────────────────────────────────────────────────
def botones_del_arbol(nodo, ruta=()):
    for b in nodo['botones']:
        yield ruta, b
    for h in nodo['hijos']:
        yield from botones_del_arbol(h, ruta + (h['nombre'],))


def carpeta_de(ruta, codigo):
    partes = [re.sub(r'[^A-Za-z0-9áéíóúñÁÉÍÓÚÑ ().-]', '', p).strip() for p in ruta]
    return os.path.join(*partes, codigo) if partes else codigo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solo', help='solo los botones cuyo nombre contenga este texto')
    ap.add_argument('--limite', type=int)
    args = ap.parse_args()

    catalogo = json.load(open(DATOS, encoding='utf-8'))
    todos = list(botones_del_arbol(catalogo['arbol']))
    muestra = [a for r, b in todos for a in b['archivos']][:60]
    fijos = hashes_fijos(muestra)
    print(f'imágenes de plantilla detectadas (logos y franja): {len(fijos)}')

    elegidos = [(r, b) for r, b in todos
                if not args.solo or args.solo.lower() in b['nombre'].lower()]
    if args.limite:
        elegidos = elegidos[:args.limite]

    ya_guardadas = {}                      # hash -> ruta web, para no repetir la misma imagen
    hechos = 0
    for ruta, boton in elegidos:
        fotos, por_codigo = {}, {}
        huellas_producto = set()
        for codigo, rel in zip(boton['codigos'], boton['archivos']):
            try:
                imgs = imagenes_de(os.path.join(FICHAS, rel))
            except Exception as e:
                avisos['no_abre'].append(f'{codigo}: {type(e).__name__}')
                continue
            roles = clasificar(imgs, fijos, codigo)
            if roles['luminaria']:
                huellas_producto.add(roles['luminaria']['hash'])
            guardadas = {}
            for tipo in ('luminaria', 'medidas', 'ambiente', 'angulo'):
                piezas = roles[tipo] if tipo == 'medidas' else ([roles[tipo]] if roles[tipo] else [])
                if not piezas:
                    continue
                clave = '+'.join(p['hash'] for p in piezas)
                if clave in ya_guardadas:
                    guardadas[tipo] = ya_guardadas[clave]
                    continue
                carpeta = carpeta_de(ruta, codigo)
                # original, tal cual viene del Excel
                for n, p in enumerate(piezas, 1):
                    sufijo = '' if len(piezas) == 1 else f'-{n}'
                    d = os.path.join(ORIGINALES, carpeta, f'{tipo}{sufijo}.{p["ext"]}')
                    os.makedirs(os.path.dirname(d), exist_ok=True)
                    open(d, 'wb').write(p['datos'])
                # versión para la web
                try:
                    im = juntar_medidas(piezas) if tipo == 'medidas' else sobre_blanco(piezas[0]['datos'])
                    rel_web = os.path.join('images', 'productos', carpeta, f'{tipo}.jpg')
                    tam = guardar(im, os.path.join(RAIZ, rel_web))
                except Exception as e:
                    avisos['imagen_ilegible'].append(f'{codigo} · {tipo}: {type(e).__name__}')
                    continue
                guardadas[tipo] = {'ruta': rel_web.replace(os.sep, '/'), 'px': list(tam)}
                ya_guardadas[clave] = guardadas[tipo]
            por_codigo[codigo] = guardadas
            if not fotos:
                fotos = dict(guardadas)
        if len(huellas_producto) > 1:
            avisos['producto_distinto'].append(
                f"{boton['nombre']}: las fichas del grupo tienen fotos de producto distintas ({len(huellas_producto)})")
        boton['fotos'] = fotos
        boton['fotos_por_codigo'] = por_codigo
        hechos += 1

    json.dump(catalogo, open(DATOS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{hechos} botones con fotos')
    for k, v in sorted(avisos.items(), key=lambda x: -len(x[1])):
        print(f'   {k}: {len(v)}')
    json.dump({k: v for k, v in avisos.items()},
              open(os.path.join(RAIZ, 'docs', 'catalogo', 'avisos-fotos.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
