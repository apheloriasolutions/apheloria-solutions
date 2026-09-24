"""
Lee "CÓDIGOS GENERALES.xlsx" y devuelve un registro por código de producto:
  codigo, familia (nombre de la hoja), descripcion, codigo_celdas (el código deletreado letra a letra),
  opciones: temperaturas de color, potencias y mA que aparecen en la descripción,
  cct_modelo: todas las temperaturas en las que existe ese mismo modelo (aunque sean códigos distintos).

Lo que hay que saber del Excel (comprobado):
  - NO contiene la tabla de características técnicas: solo el código, una descripción de una línea
    y referencias de proveedor. La tabla completa tiene que salir del PDF.
  - El código aparece dos veces: deletreado letra a letra en celdas sueltas y al principio de la
    descripción. En decenas de filas no coinciden (O/0 cambiados, o códigos distintos). Aquí se toma
    el de la descripción y se deja el otro en codigo_celdas para poder cruzar con los PDF por los dos.
  - Las columnas de la derecha (LEDME, LEDSHOME, DELUXE, CELUX, OPPLE, GARMALUX...) son referencias de
    proveedor. Este script las ignora a propósito: NO deben publicarse en la web.
  - Las hojas "... TODO" repiten los productos de las hojas por familia; se usa la hoja de familia si existe.

Uso:  python leer_excel.py "CÓDIGOS GENERALES.xlsx" salida.json
"""
import openpyxl, re, sys, json
from collections import defaultdict
from openpyxl.cell.cell import MergedCell

HOJAS_TODO = {"INTERIORES TODO", "INDUSTRIAL TODO", "EXTERIORES TODO", "EMERGENCIA TODO"}
IGNORAR = {"Hoja1", "HOJAS DELANTERAS"}
norm = lambda c: c.upper().replace("O", "0")          # para comparar: la O y el 0 se confunden a menudo

def filas(wb):
    for ws in wb.worksheets:
        if ws.title in IGNORAR: continue
        inicio = 3 if ws.title in HOJAS_TODO else 1       # en las hojas TODO la columna A es un nº de orden
        for row in ws.iter_rows(min_col=inicio, max_col=17):
            desc, letras = None, []
            for c in row:
                if isinstance(c, MergedCell) or c.value is None: continue
                v = c.value
                if isinstance(v, str) and len(v) > 20: desc = v.strip(); break
                if len(str(v)) == 1: letras.append(str(v))
            if desc and len(letras) >= 6:
                yield ws.title, "".join(letras), desc

FIN = r'(?![A-Za-z0-9])'      # como \b pero dejando pasar "_" ("4000K_IP65", "40W_")

def opciones(desc):
    desc = desc.split(None, 1)[-1]                      # sin el código, que también lleva cifras y W/K
    cct = sorted({int(m) for m in re.findall(r'(\d{4})\s?K' + FIN, desc)})
    pot = []
    for m in re.finditer(r'(?<![\d.,])(\d+(?:[.,]\d+)?(?:\s*-\s*\d+(?:[.,]\d+)?)*)\s*W' + FIN, desc):
        pot += [p.strip() for p in m.group(1).split('-')]
    ma = sorted({int(m) for m in re.findall(r'(\d+)\s*mA', desc)})
    return dict(cct=cct, cct_seleccionable=bool(re.search(r'\bCCT\b', desc)) or len(cct) > 1,
                potencias=pot, ma=ma)

def leer(ruta):
    wb = openpyxl.load_workbook(ruta, data_only=True)
    productos = {}
    for hoja, celdas, desc in filas(wb):
        codigo = desc.split()[0].rstrip('-_ ')
        clave = norm(codigo)
        if clave in productos and hoja in HOJAS_TODO: continue      # ya lo tenemos de la hoja de familia
        productos[clave] = dict(codigo=codigo, familia=hoja, descripcion=desc,
                                codigo_celdas=celdas, codigos_distintos=norm(celdas) != clave,
                                opciones=opciones(desc))
    # mismo modelo en varias temperaturas de color = misma descripción quitando código y "xxxxK"
    modelo = lambda d: re.sub(r'\s+', ' ', re.sub(r'\d{4}\s?K' + FIN, '', d.split(None, 1)[-1], flags=re.I)).lower().strip(' -_.')
    grupos = defaultdict(list)
    for p in productos.values(): grupos[modelo(p['descripcion'])].append(p)
    for g in grupos.values():
        todas = sorted({t for p in g for t in p['opciones']['cct']})
        for p in g: p['cct_modelo'] = todas
    return list(productos.values())

if __name__ == '__main__':
    datos = leer(sys.argv[1])
    json.dump(datos, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    print(f"{len(datos)} códigos | con códigos distintos en celdas y descripción: {sum(p['codigos_distintos'] for p in datos)}")
