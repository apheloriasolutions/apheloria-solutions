"""
Una sola ficha por producto, en lugar de una por referencia.

Los productos con varias referencias tienen hoy una ficha por cada una, casi idénticas:
el ZEN son 21 hojas que solo se diferencian en los vatios y los grados K. Aquí se coge la
ficha de la primera referencia y se le cambian tres cosas:

  - el encabezado, que nombraba una referencia suelta, pasa a nombrar el modelo;
  - la tabla de características, la del resumen de la web, con todos los valores juntos
    ("7W - 12W - 20W…") y con la fila "Medida", que en el Excel no existe;
  - la descripción, la fundida de todas sus fichas.

Las fotos, los planos, la curva fotométrica y el pie se quedan como están.

Salida: fichas/resumidas/<código de la primera referencia>.pdf

Uso:  python scripts/catalogo/fichas_resumidas.py [--solo TEXTO]
"""
import argparse
import json
import os

import fitz

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEB = os.path.join(RAIZ, 'js', 'catalogo-web.js')
DESTINO = os.path.join(RAIZ, 'fichas', 'resumidas')

BEIGE = (0.9255, 0.8980, 0.8588)
TINTA = (0.10, 0.086, 0.07)
GRIS = (0.52, 0.48, 0.41)
TAM = 6.2
HOLGURA = 1.10          # "Ø" y "·" salen más anchos de lo que mide helv
BLANCO = (1, 1, 1)


def productos(nodo, ruta=()):
    for p in nodo.get('productos', []):
        yield ruta, p
    for h in nodo.get('hijos', []):
        yield from productos(h, ruta + (h['nombre'],))


def ancho(txt, tam=TAM, fuente='helv'):
    return fitz.get_text_length(txt, fuente, tam) * HOLGURA


def partir(valor, limite, tam=TAM):
    """Reparte el valor en varias líneas si no cabe, cortando por sus separadores."""
    if ancho(valor, tam) <= limite:
        return [valor]
    for sep in (' / ', ' - ', ', ', ' '):
        if sep not in valor:
            continue
        lineas, actual = [], ''
        for trozo in valor.split(sep):
            prueba = trozo if not actual else actual + sep.rstrip() + ' ' + trozo
            if ancho(prueba, tam) <= limite:
                actual = prueba
            else:
                if actual:
                    lineas.append(actual)
                actual = trozo
        if actual:
            lineas.append(actual)
        if all(ancho(l, tam) <= limite for l in lineas):
            return lineas
    return [valor]


def parecido(color, objetivo=BEIGE, tolerancia=0.03):
    return color and len(color) == 3 and all(abs(a - b) < tolerancia for a, b in zip(color, objetivo))


def zona_tabla(pagina):
    """El rectángulo que ocupa la tabla de características, por sus bandas de color."""
    bandas = [d['rect'] for d in pagina.get_drawings()
              if parecido(d.get('fill')) and d['rect'].x0 < 70
              and d['rect'].x1 < 340 and d['rect'].width > 150]
    if not bandas:
        return None
    x0 = min(b.x0 for b in bandas)
    x1 = max(b.x1 for b in bandas)
    y0 = min(b.y0 for b in bandas)
    etiquetas = [b for b in pagina.get_text('blocks')
                 if b[6] == 0 and abs(b[0] - x0) < 6 and b[1] >= y0 - 2]
    y1 = max([b[3] for b in etiquetas] + [max(b.y1 for b in bandas)])
    return fitz.Rect(x0, y0, x1, y1)


def zona_descripcion(pagina):
    """El hueco de la descripción: desde su rótulo hasta la primera imagen que tiene debajo."""
    rotulo = next((b for b in pagina.get_text('blocks')
                   if b[6] == 0 and 'Descripci' in b[4] and b[0] > 300), None)
    if not rotulo:
        return None, None
    debajo = [i['bbox'][1] for i in pagina.get_image_info()
              if i['bbox'][0] > 300 and i['bbox'][1] > rotulo[1] + 8]
    tope = min(debajo) if debajo else rotulo[1] + 120
    return fitz.Rect(rotulo[0] - 6, rotulo[1] - 3, 518, tope - 6), rotulo


def zona_encabezado(pagina, codigo):
    """La línea que nombra la referencia, justo debajo de 'FICHA TÉCNICA'."""
    bloques = [b for b in pagina.get_text('blocks') if b[6] == 0]
    for b in bloques:
        if b[4].strip().startswith(codigo):
            return fitz.Rect(b[0] - 2, b[1] - 2, 520, b[3] + 2)
    # en 37 fichas el código de la celda no es el del nombre del archivo: se busca por
    # posición, la primera línea que va debajo de "FICHA TÉCNICA"
    titulo = next((b for b in bloques if b[4].strip().startswith('FICHA TÉCNICA')), None)
    if titulo:
        debajo = [b for b in bloques if b[1] > titulo[1] and abs(b[0] - titulo[0]) < 6]
        if debajo:
            b = min(debajo, key=lambda x: x[1])
            return fitz.Rect(b[0] - 2, b[1] - 2, 520, b[3] + 2)
    return None


def resumir(prod, aviso):
    base = os.path.join(RAIZ, prod['fichas'][0]['pdf'])
    doc = fitz.open(base)
    pg = doc[0]

    tabla = zona_tabla(pg)
    if tabla is None:
        aviso.append(f"{prod['nombre']}: no encuentro la tabla en {os.path.basename(base)}")
        doc.close()
        return None

    # las notas al pie de la tabla vuelven como filas, que si no se perderían
    filas = [(e, v) for e, v in prod['tabla']]
    for nota in prod.get('notas', []):
        if ':' in nota:
            e, v = nota.rsplit(':', 1)
            filas.append((e.strip(), v.strip()))

    col_val = tabla.x0 + 88
    ancho_val = tabla.x1 - col_val - 2
    partidas = [(e, partir(v, ancho_val)) for e, v in filas]
    n_lineas = sum(len(v) for _, v in partidas)
    alto = (tabla.y1 - tabla.y0) / n_lineas
    if alto < 6.6:                       # no cabe sin que las líneas se toquen
        aviso.append(f"{prod['nombre']}: la tabla no cabe ({n_lineas} líneas en "
                     f"{tabla.height:.0f} pt)")

    pg.draw_rect(fitz.Rect(tabla.x0 - 2, tabla.y0 - 3, tabla.x1 + 2, tabla.y1 + 3),
                 color=None, fill=BLANCO)
    y = tabla.y0
    for i, (etiqueta, trozos) in enumerate(partidas):
        h = alto * len(trozos)
        if i % 2 == 0:
            pg.draw_rect(fitz.Rect(tabla.x0, y, tabla.x1, y + h), color=None, fill=BEIGE)
        pg.insert_text((tabla.x0 + 3.5, y + alto * 0.72), etiqueta + ':',
                       fontname='helv', fontsize=TAM, color=TINTA)
        for j, trozo in enumerate(trozos):
            pg.insert_text((col_val + (ancho_val - ancho(trozo)) / 2, y + alto * (j + 0.72)),
                           trozo, fontname='helv', fontsize=TAM, color=TINTA)
        y += h

    cabecera = zona_encabezado(pg, prod['fichas'][0]['codigo'])
    if cabecera:
        pg.draw_rect(cabecera, color=None, fill=BLANCO)
        linea = cabecera.y1 - 3
        pg.insert_text((cabecera.x0 + 2, linea), prod['nombre'],
                       fontname='hebo', fontsize=9.5, color=TINTA)
        pg.insert_text((cabecera.x0 + 2 + fitz.get_text_length(prod['nombre'], 'hebo', 9.5) + 6,
                        linea), f"· {len(prod['fichas'])} referencias",
                       fontname='helv', fontsize=8.5, color=GRIS)
    else:
        aviso.append(f"{prod['nombre']}: no encuentro el encabezado")

    hueco, rotulo = zona_descripcion(pg)
    if hueco and prod.get('descripcion'):
        pg.draw_rect(hueco, color=None, fill=BLANCO)
        titulo = 'Descripción'
        w = fitz.get_text_length(titulo, 'hebo', 7.5)
        pg.insert_text((hueco.x0 + (hueco.width - w) / 2, hueco.y0 + 12),
                       titulo, fontname='hebo', fontsize=7.5, color=TINTA)
        caja = fitz.Rect(hueco.x0 + 2, hueco.y0 + 18, hueco.x1 - 2, hueco.y1)
        texto = prod['descripcion'][0]
        for tam in (6.3, 6.0, 5.7, 5.4, 5.1):
            if pg.insert_textbox(caja, texto, fontname='helv', fontsize=tam, color=TINTA) >= 0:
                break
        else:
            aviso.append(f"{prod['nombre']}: la descripción no cabe entera")

    os.makedirs(DESTINO, exist_ok=True)
    salida = os.path.join(DESTINO, prod['fichas'][0]['codigo'] + '.pdf')
    doc.save(salida, garbage=4, deflate=True)
    doc.close()
    return salida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solo', help='solo los productos cuyo nombre contenga este texto')
    args = ap.parse_args()

    texto = open(WEB, encoding='utf-8').read()
    arbol = json.loads(texto[texto.index('{', texto.index('=')):texto.rindex('}') + 1])
    varias = [p for _, p in productos(arbol) if len(p['fichas']) > 1]
    if args.solo:
        varias = [p for p in varias if args.solo.lower() in p['nombre'].lower()]

    aviso, hechas = [], 0
    for p in varias:
        if resumir(p, aviso):
            hechas += 1
    print(f'{DESTINO}: {hechas} fichas resumidas')
    print(f'  sustituyen a {sum(len(p["fichas"]) for p in varias)} hojas: '
          f'{sum(len(p["fichas"]) for p in varias) - hechas} páginas menos')
    if aviso:
        print(f'  avisos ({len(aviso)}):')
        for a in aviso:
            print('   ', a)


if __name__ == '__main__':
    main()
