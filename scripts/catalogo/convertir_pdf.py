"""
Convierte cada ficha .xlsx a PDF con LibreOffice, dejando SOLO la primera hoja
y ajustada a una página A4 vertical.

La segunda hoja (Hoja2) lleva referencias de proveedor y no se publica nunca: antes de
convertir se hace una copia temporal del .xlsx y se le quita esa hoja **a nivel de ZIP**,
sin reescribir el archivo con openpyxl (eso perdería las fotos, que van en xl/media).

Uso:  python scripts/catalogo/convertir_pdf.py [--prueba] [--rehacer]
      --prueba   solo tres fichas de muestra, a docs/catalogo/pdf-prueba/
      --rehacer  vuelve a convertir las que ya existen
"""
import json, os, re, shutil, subprocess, sys, tempfile, zipfile

import fitz

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHAS = os.path.join(RAIZ, 'fuentes', 'fichas')
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
SALIDA = os.path.join(RAIZ, 'fichas')
SOFFICE = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
PRUEBA = ('00CARD20W3KBL', '00PANEL25WXXX', '00PSFB1S2020')


def solo_primera_hoja(origen, destino):
    """Copia el .xlsx dejando únicamente la primera hoja, y la ajusta a una A4 vertical.
    Devuelve el nombre de las hojas que se han quitado."""
    z = zipfile.ZipFile(origen)
    libro = z.read('xl/workbook.xml').decode('utf-8')
    rels = z.read('xl/_rels/workbook.xml.rels').decode('utf-8')
    tipos = z.read('[Content_Types].xml').decode('utf-8')

    hojas = re.findall(r'<sheet\b[^>]*/>', libro)
    quitadas = [re.search(r'name="([^"]*)"', h).group(1) for h in hojas[1:]]

    # qué partes del zip hay que borrar: la de cada hoja que se va, y sus rels
    destino_de = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    fuera = set()
    for h in hojas[1:]:
        rid = re.search(r'r:id="([^"]+)"', h)
        if rid and rid.group(1) in destino_de:
            parte = 'xl/' + destino_de[rid.group(1)].lstrip('/')
            fuera.add(parte)
            fuera.add(os.path.dirname(parte) + '/_rels/' + os.path.basename(parte) + '.rels')
        libro = libro.replace(h, '')
        if rid:
            rels = re.sub(rf'<Relationship[^>]*Id="{rid.group(1)}"[^>]*/>', '', rels)
    # los nombres definidos que apuntaban a las hojas que se van
    for nombre in re.findall(r'<definedName\b[^>]*>.*?</definedName>', libro, re.S):
        if any(f"'{q}'" in nombre or f'{q}!' in nombre for q in quitadas):
            libro = libro.replace(nombre, '')
    for parte in fuera:
        tipos = re.sub(rf'<Override[^>]*PartName="/{re.escape(parte)}"[^>]*/>', '', tipos)
    # calcChain apunta a celdas por número de hoja: si sobra, Calc lo recalcula
    fuera.add('xl/calcChain.xml')
    tipos = re.sub(r'<Override[^>]*PartName="/xl/calcChain\.xml"[^>]*/>', '', tipos)

    hoja1 = z.read('xl/worksheets/sheet1.xml').decode('utf-8')
    if '<sheetPr' in hoja1:
        if 'fitToPage' not in hoja1:
            hoja1 = re.sub(r'<sheetPr\b([^>]*)/>', r'<sheetPr\1><pageSetUpPr fitToPage="1"/></sheetPr>', hoja1, count=1)
            hoja1 = re.sub(r'(<sheetPr\b[^>]*>)(?!<pageSetUpPr)', r'\1<pageSetUpPr fitToPage="1"/>', hoja1, count=1)
    else:
        hoja1 = re.sub(r'(<worksheet\b[^>]*>)', r'\1<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>', hoja1, count=1)
    # el r:id de pageSetup apunta a la configuración de impresora guardada, que manda
    # sobre el ajuste; se quita para que valgan fitToWidth/fitToHeight
    hoja1 = re.sub(r'<pageSetup\b[^>]*/>',
                   '<pageSetup paperSize="9" orientation="portrait" fitToWidth="1" fitToHeight="1"/>',
                   hoja1, count=1)
    if '<pageSetup' not in hoja1:
        hoja1 = hoja1.replace('</worksheet>',
                              '<pageSetup paperSize="9" orientation="portrait" '
                              'fitToWidth="1" fitToHeight="1"/></worksheet>')

    nuevos = {'xl/workbook.xml': libro, 'xl/_rels/workbook.xml.rels': rels,
              '[Content_Types].xml': tipos, 'xl/worksheets/sheet1.xml': hoja1}
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as salida:
        for info in z.infolist():
            if info.filename in fuera:
                continue
            salida.writestr(info, nuevos.get(info.filename) or z.read(info.filename))
    z.close()
    return quitadas


def convertir(origenes, carpeta):
    """LibreOffice de una tacada: arrancarlo por cada archivo cuesta un segundo largo."""
    perfil = os.path.join(tempfile.gettempdir(), 'apheloria-soffice')
    subprocess.run([SOFFICE, '--headless', '--norestore', f'-env:UserInstallation=file://{perfil}',
                    '--convert-to', 'pdf', '--outdir', carpeta] + origenes,
                   check=True, capture_output=True, timeout=1800)


def quitar_paginas_en_blanco(ruta):
    """LibreOffice deja a veces una página final vacía. Se mira si tiene un solo color."""
    doc = fitz.open(ruta)
    sobran = []
    for i in range(len(doc) - 1, 0, -1):
        muestra = doc[i].get_pixmap(dpi=40)
        colores = {muestra.samples[j:j + muestra.n] for j in range(0, len(muestra.samples), muestra.n)}
        if len(colores) > 1:
            break
        sobran.append(i)
    if sobran:
        doc.delete_pages(sobran)
        provisional = ruta + '.tmp'
        doc.save(provisional, garbage=3, deflate=True)
        doc.close()
        os.replace(provisional, ruta)
        return len(sobran)
    doc.close()
    return 0


def botones(nodo):
    for b in nodo['botones']:
        yield b
    for h in nodo['hijos']:
        yield from botones(h)


def main():
    prueba, rehacer = '--prueba' in sys.argv, '--rehacer' in sys.argv
    catalogo = json.load(open(DATOS, encoding='utf-8'))
    pares = {}
    for b in botones(catalogo['arbol']):
        for cod, rel in zip(b['codigos'], b['archivos']):
            pares.setdefault(cod, rel)
    if prueba:
        pares = {c: pares[c] for c in PRUEBA if c in pares}

    carpeta = os.path.join(RAIZ, 'docs', 'catalogo', 'pdf-prueba') if prueba else SALIDA
    os.makedirs(carpeta, exist_ok=True)
    temporal = tempfile.mkdtemp(prefix='apheloria-fichas-')
    pendientes, quitadas, fallos = [], {}, []
    for cod, rel in sorted(pares.items()):
        if not rehacer and os.path.exists(os.path.join(carpeta, cod + '.pdf')):
            continue
        copia = os.path.join(temporal, cod + '.xlsx')
        try:
            quitadas[cod] = solo_primera_hoja(os.path.join(FICHAS, rel), copia)
            pendientes.append(copia)
        except Exception as e:
            fallos.append((cod, rel, f'no se puede preparar: {e}'))

    for i in range(0, len(pendientes), 40):
        lote = pendientes[i:i + 40]
        try:
            convertir(lote, carpeta)
        except Exception as e:
            for c in lote:
                fallos.append((os.path.basename(c)[:-5], '', f'LibreOffice: {e}'))
        print(f'  convertidas {min(i + 40, len(pendientes))}/{len(pendientes)}', flush=True)

    hechos = [c for c in pares if os.path.exists(os.path.join(carpeta, c + '.pdf'))]
    limpiadas = sum(quitar_paginas_en_blanco(os.path.join(carpeta, c + '.pdf')) for c in hechos)
    print(f'páginas en blanco quitadas: {limpiadas}')
    if not prueba:
        rutas = {c: f'fichas/{c}.pdf' for c in hechos}
        for b in botones(catalogo['arbol']):
            b['pdf'] = {c: rutas[c] for c in b['codigos'] if c in rutas}
        json.dump(catalogo, open(DATOS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    shutil.rmtree(temporal, ignore_errors=True)
    print(f'{carpeta}: {len(hechos)} PDF de {len(pares)} fichas')
    con2 = [c for c, q in quitadas.items() if q]
    print(f'fichas a las que se les ha quitado una segunda hoja: {len(con2)}')
    for cod, rel, motivo in fallos:
        print(f'  FALLA {cod}: {motivo}')


if __name__ == '__main__':
    main()
