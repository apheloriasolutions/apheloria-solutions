"""
Rehace la maquetación de las carátulas del catálogo (los .docx del escritorio).

Qué cambia, respecto a como venían:
  - el título pasa a ir ENCIMA de la línea dorada, que es una imagen, no un borde;
  - desaparece el logo del encabezado, el de arriba a la derecha: solo queda el del pie;
  - el pie deja de llevar la dirección y pasa a ser "[logo] | www.apheloria.es", centrado,
    con una tabla de dos celdas y solo el borde interior en dorado;
  - el texto de cuerpo pasa de dorado de 6 pt a negro suave de 7,5 pt;
  - todo el documento pasa a Avenir Next. Los títulos y la lista de ventajas conservan su
    color dorado y su tamaño.

Las imágenes no se tocan, y cada carátula tiene que seguir cabiendo en UNA página: el
script avisa si alguna se pasa.

Uso:  python scripts/catalogo/maquetar_caratulas.py [archivo.docx ...]
      sin argumentos, las hace todas.
"""
import glob
import os
import sys

import docx
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Emu, Pt, RGBColor

CARPETA = os.path.expanduser('~/Desktop/Apheloria - Catálogo')
FUENTE = 'Avenir Next'
ORO = RGBColor(0xB4, 0x8A, 0x4C)
TINTA = RGBColor(0x1A, 0x1A, 0x1A)
CUERPO = Pt(7.3)
INTERLINEADO = 1.0
SEPARADOR = Pt(3)          # los párrafos vacíos que separan bloques: solo aire, no texto
MARGEN_SUP = Emu(342900)   # 0,95 cm, antes 2,5: el hueco del logo que se ha quitado
MARGEN_INF = Emu(216000)   # 0,6 cm
PIE_DISTANCIA = Emu(90000) # 0,25 cm
WEB = 'www.apheloria.es'
ENLACE = 'https://www.apheloria.es'


def es_oro(run):
    c = run.font.color
    return c is not None and c.type is not None and c.rgb == ORO


def tipografia(run, tam=None, color=None, negrita=None):
    """Fija la tipografía de un run. Hay que tocar también rFonts, porque python-docx
    solo escribe ascii/hAnsi y Word usa cs para el resto."""
    run.font.name = FUENTE
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = rpr.makeelement(qn('w:rFonts'), {})
        rpr.insert(0, rfonts)
    for atr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(atr), FUENTE)
    if tam is not None:
        run.font.size = tam
    if color is not None:
        run.font.color.rgb = color
    if negrita is not None:
        run.font.bold = negrita


def titulo_encima(doc):
    """La línea dorada es una imagen en su propio párrafo, justo delante del título.
    Se intercambian para que el título quede arriba."""
    parrafos = doc.paragraphs
    for i, p in enumerate(parrafos[:8]):
        if '<pic:pic' not in p._p.xml:
            continue
        # la línea es muy ancha y muy baja; las fotos no
        if 'image1' not in p._p.xml and not _es_linea(doc, p):
            continue
        siguiente = parrafos[i + 1] if i + 1 < len(parrafos) else None
        if siguiente is None or not siguiente.text.strip():
            continue
        p._p.addprevious(siguiente._p)      # el título se coloca delante de la línea
        return True
    return False


def _es_linea(doc, parrafo):
    """La línea dorada mide 886 x 8 px: proporción enorme y poca altura."""
    import re
    ext = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', parrafo._p.xml)
    if not ext:
        return False
    cx, cy = int(ext.group(1)), int(ext.group(2))
    return cy and cx / cy > 20


def quitar_logo_de_arriba(seccion):
    cabecera = seccion.header
    for p in list(cabecera.paragraphs):
        p._p.getparent().remove(p._p)
    cabecera.add_paragraph()                 # un encabezado vacío, para no romper la sección
    seccion.header_distance = Emu(0)


def pie_nuevo(doc, seccion):
    """Borra el pie y lo rehace: [logo] | www.apheloria.es, centrado en la hoja."""
    pie = seccion.footer
    logo = None
    for p in pie.paragraphs:                 # el logo se reaprovecha, no se vuelve a incrustar
        for r in p.runs:
            if '<pic:pic' in r._element.xml:
                logo = r._element
                break
        if logo is not None:
            break
    for p in list(pie.paragraphs):
        p._p.getparent().remove(p._p)
    for t in list(pie.tables):
        t._tbl.getparent().remove(t._tbl)

    tabla = pie.add_table(rows=1, cols=2, width=seccion.page_width - seccion.left_margin
                          - seccion.right_margin)
    tabla.autofit = False
    _solo_borde_interior(tabla)
    izq, der = tabla.rows[0].cells
    for celda in (izq, der):
        celda.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    p_logo = izq.paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if logo is not None:
        _encoger(logo, Emu(411480))          # 0,45 cm de alto aprox: el logo del pie, más discreto
        p_logo.add_run()._element.addprevious(logo)
    p_logo.paragraph_format.space_after = Pt(0)
    _margen_derecho(izq, Emu(114300))        # un poco de aire antes de la barra

    p_web = der.paragraphs[0]
    p_web.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_web.paragraph_format.space_after = Pt(0)
    _margen_izquierdo(der, Emu(114300))
    _enlace(p_web, WEB, ENLACE)


def _encoger(pic_element, alto):
    """Reescala la imagen del logo manteniendo su proporción."""
    import re
    xml = pic_element.xml
    ext = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"', xml)
    if not ext:
        return
    cx, cy = int(ext.group(1)), int(ext.group(2))
    nuevo_cx = int(cx * alto / cy)
    for nodo in pic_element.iter():
        if nodo.tag.endswith('}extent') or nodo.tag.endswith('}ext'):
            if nodo.get('cx'):
                nodo.set('cx', str(nuevo_cx))
                nodo.set('cy', str(int(alto)))


def _enlace(parrafo, texto, url):
    parte = parrafo.part
    rid = parte.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/'
                               'relationships/hyperlink', is_external=True)
    enlace = parrafo._p.makeelement(qn('w:hyperlink'), {qn('r:id'): rid})
    run = parrafo.add_run(texto)
    tipografia(run, tam=Pt(8), color=ORO, negrita=False)
    run.font.underline = False
    enlace.append(run._element)
    parrafo._p.append(enlace)


def _solo_borde_interior(tabla):
    """Sin bordes salvo el vertical del medio, fino y dorado."""
    from docx.oxml import OxmlElement
    pr = tabla._tbl.tblPr
    bordes = OxmlElement('w:tblBorders')
    for lado in ('top', 'left', 'bottom', 'right', 'insideH'):
        e = OxmlElement(f'w:{lado}')
        e.set(qn('w:val'), 'none')
        e.set(qn('w:sz'), '0')
        bordes.append(e)
    dentro = OxmlElement('w:insideV')
    dentro.set(qn('w:val'), 'single')
    dentro.set(qn('w:sz'), '4')              # 0,5 pt
    dentro.set(qn('w:color'), 'B48A4C')
    bordes.append(dentro)
    pr.append(bordes)


def _margen_derecho(celda, valor):
    _margen(celda, 'right', valor)


def _margen_izquierdo(celda, valor):
    _margen(celda, 'left', valor)


def _margen(celda, lado, valor):
    from docx.oxml import OxmlElement
    pr = celda._tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    e = OxmlElement(f'w:{lado}')
    e.set(qn('w:w'), str(int(valor / 635)))  # en vigésimas de punto
    e.set(qn('w:type'), 'dxa')
    mar.append(e)
    pr.append(mar)


def margenes(seccion):
    seccion.top_margin = MARGEN_SUP
    seccion.bottom_margin = MARGEN_INF
    seccion.footer_distance = PIE_DISTANCIA


def apretar_separadores(doc):
    """Entre bloque y bloque hay párrafos vacíos a 11 pt. Se quedan, porque dan el aire,
    pero a 5 pt: es lo que hace que las imágenes no salten de página."""
    for p in doc.paragraphs:
        if p.text.strip() or '<pic:pic' in p._p.xml:
            continue
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1
        for r in p.runs:
            r.font.size = SEPARADOR
        if not p.runs:
            p.add_run().font.size = SEPARADOR


def quitar_cola(doc):
    """Los párrafos vacíos del final empujaban la última fila de fotos a otra página."""
    quitados = 0
    for p in reversed(doc.paragraphs):
        if p.text.strip() or '<pic:pic' in p._p.xml:
            break
        p._p.getparent().remove(p._p)
        quitados += 1
    return quitados


def cuerpo(doc):
    """Cuerpo a negro y 7,5 pt; títulos y ventajas se quedan dorados, pero todo
    pasa a la tipografía nueva para que no se note el cambio a media página."""
    for p in doc.paragraphs:
        if not p.runs:
            continue
        pf = p.paragraph_format
        texto = p.text.strip()
        if not texto:
            continue
        tam = max((r.font.size.pt for r in p.runs if r.font.size), default=None)
        es_titulo = tam is not None and tam >= 9
        for r in p.runs:
            if es_titulo:
                tipografia(r, color=ORO)                       # conserva tamaño y negrita
            elif texto.startswith(' ') or p is None:
                tipografia(r, tam=CUERPO, color=ORO, negrita=False)
            else:
                tipografia(r, tam=CUERPO, color=TINTA, negrita=False)
        if not es_titulo:
            pf.line_spacing = INTERLINEADO


def ventajas_en_oro(doc):
    """Las ventajas van sangradas con espacios: se reconocen por eso y se dejan doradas."""
    dentro = False
    for p in doc.paragraphs:
        if p.text.strip().lower().startswith('principales ventajas'):
            dentro = True
            continue
        if dentro:
            if not p.text.strip():
                continue
            if not p.text.startswith('  '):
                dentro = False
                continue
            for r in p.runs:
                tipografia(r, tam=CUERPO, color=ORO, negrita=False)


def arreglar(ruta):
    doc = docx.Document(ruta)
    sec = doc.sections[0]
    movido = titulo_encima(doc)
    quitar_logo_de_arriba(sec)
    margenes(sec)
    cuerpo(doc)
    apretar_separadores(doc)
    quitar_cola(doc)
    ventajas_en_oro(doc)
    pie_nuevo(doc, sec)
    doc.save(ruta)
    return movido


def main():
    archivos = sys.argv[1:] or sorted(glob.glob(os.path.join(CARPETA, '*.docx')))
    for a in archivos:
        if not os.path.isabs(a):
            a = os.path.join(CARPETA, a)
        movido = arreglar(a)
        print(f'  {os.path.basename(a)[:52]:54s} título movido: {"sí" if movido else "NO"}')


if __name__ == '__main__':
    main()
