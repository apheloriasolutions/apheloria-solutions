"""
Genera una ficha por PRODUCTO REAL (no por código) para las hojas INDUSTRIAL TODO e INTERIORES TODO.

Muchos códigos son el mismo producto con distinta potencia, temperatura de color, mA o acabado
(p. ej. los 21 códigos del downlight ZEN). Aquí se agrupan en una sola ficha:
  - la tabla se saca de los PDF de todos sus códigos y se fusiona: donde los PDF coinciden va el
    valor tal cual, y donde no (potencia, lúmenes, K, mA...) van todos separados por " | ";
  - debajo quedan todos los PDF para descargar, cada uno etiquetado con lo que lo distingue.

Nunca se lee ni se publica ninguna referencia de proveedor del Excel (leer_excel.py ya las ignora).

Uso:  python construir_productos.py "CÓDIGOS GENERALES.xlsx"
"""
import os, re, sys, json, hashlib, unicodedata
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extraer_tabla import extraer_tabla, TablaNoExtraible
from leer_excel import leer, filas, norm
import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEP = ' | '
FIN = r'(?![A-Za-z0-9])'
CATEGORIAS = {'INDUSTRIAL TODO': 'industrial', 'INTERIORES TODO': 'interior'}

sin_tildes = lambda s: ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
clave_etiq = lambda e: re.sub(r'[^a-z0-9]', '', sin_tildes(e).lower())


# ── agrupar códigos que son el mismo producto ──
def modelo(desc):
    """Clave de producto: la descripción sin código ni los valores que cambian entre variantes."""
    d = desc.split(None, 1)[-1] if len(desc.split()) > 1 else desc
    d = re.sub(r'\d{3,4}\s?K' + FIN, '', d, flags=re.I)
    d = re.sub(r'(?<![\d.,])\d+(?:[.,]\d+)?(?:\s*-\s*\d+(?:[.,]\d+)?)*\s*W' + FIN, '', d, flags=re.I)
    d = re.sub(r'\d+\s*mA' + FIN, '', d, flags=re.I)
    d = re.sub(r'\d[\d.,]*\s*(lm|lumen\w*)' + FIN, '', d, flags=re.I)
    return re.sub(r'[^a-z0-9]', '', sin_tildes(d).lower())


RANGO = r'\d+(?:[.,]\d+)?(?:\s*[-_]\s*\d+(?:[.,]\d+)?)*'    # "24", "12-15-18-24", "2900_4420"


def _nombre_de(desc):
    d = desc.split(None, 1)[-1] if len(desc.split()) > 1 else desc
    for patron in (r'(?<![\dXx])' + RANGO + r'\s?K' + FIN,          # 4000K, 3000-4000K
                   r'(?<![\d.,Xx])' + RANGO + r'\s*W' + FIN,        # 24W, 12-15-18-24W (no "60X60")
                   r'\d+\s*mA' + FIN,
                   r'(?<![\d.,])' + RANGO + r'\s*(?:lm|lumen\w*)' + FIN,
                   r'\bCRI\s?\d+', r'\d+\s?[º°]', r'\b\d?CCT\b', r'\bmod\.?\b'):
        d = re.sub(patron, ' ', d, flags=re.I)
    d = re.sub(r'(?<!\d)[-_,.]+(?!\d)|(?<=\d)[-_,.]+(?!\d)|(?<!\d)[-_,.]+(?=\d)', ' ', d)   # sin romper decimales
    d = re.sub(r'\s+', ' ', d).strip(' -_.–—')
    return re.sub(r'\b(IP|IK)\b(?!\s*\d)', '', d).strip(' -_.')          # "IP"/"IK" sin número detrás


def nombre_producto(descripciones):
    """Nombre legible del producto. Se toma el más repetido: algunas descripciones traen erratas
    (p. ej. "empotradofijo" en 3 de los 21 códigos de ZEN) y así gana la forma correcta."""
    nombres = [n for n in (_nombre_de(d) for d in descripciones) if n]
    return Counter(nombres).most_common(1)[0][0] if nombres else 'Producto'


def codigos_por_categoria(ruta_excel):
    """Qué códigos son de industrial y cuáles de interior.

    Base: las hojas INDUSTRIAL TODO e INTERIORES TODO. Pero hay productos publicados en la web cuyo
    código solo aparece en una hoja de familia (SALAS BLANCAS, PANELES, PROYECTORES, TIRAS LED...) y
    no en las hojas TODO; esos se recuperan de la auditoría de la web, que ya dice su categoría.
    """
    wb = openpyxl.load_workbook(ruta_excel, data_only=True)
    cat = {}
    for hoja, _celdas, desc in filas(wb):
        if hoja in CATEGORIAS:
            cat.setdefault(norm(desc.split()[0]), CATEGORIAS[hoja])

    auditoria = os.path.join(RAIZ, 'docs', 'migracion-fichas', 'audit-productos.json')
    if os.path.exists(auditoria):
        for p in json.load(open(auditoria, encoding='utf-8')):
            if p.get('ref') and p.get('categoria') in CATEGORIAS.values():
                cat.setdefault(norm(p['ref']), p['categoria'])
    return cat


# ── PDFs del repo ──
def indexar_pdfs():
    idx = defaultdict(list)
    for base, _, ficheros in os.walk(RAIZ):
        if os.sep + '.git' in base:
            continue
        for f in ficheros:
            if f.lower().endswith('.pdf'):
                ruta = os.path.relpath(os.path.join(base, f), RAIZ)
                idx[norm(os.path.splitext(f)[0])].append(ruta)
    return idx


def pdfs_de(idx_pdfs, codigo):
    """PDFs cuyo nombre empieza por el código (la O y el 0 se tratan igual)."""
    c = norm(codigo)
    return sorted({r for stem, rutas in idx_pdfs.items() if stem.startswith(c) for r in rutas})


# ── fusión de tablas ──
def _num(v):
    m = re.search(r'\d+(?:[.,]\d+)?', v)
    return float(m.group().replace(',', '.')) if m else None


def ordenar_valores(vals):
    nums = [_num(v) for v in vals]
    return [v for _, v in sorted(zip(nums, vals))] if all(n is not None for n in nums) else vals


def fusionar(tablas):
    """tablas: [(ref, [{etiqueta,valor}])] -> una sola tabla con los valores que difieren unidos por ' | '."""
    orden, etiqueta_de, valores = [], {}, defaultdict(list)
    for _ref, t in tablas:
        for fila in t:
            k = clave_etiq(fila['etiqueta'])
            if not k:
                continue
            existente = next((o for o in orden if o.startswith(k) or k.startswith(o)), None)
            if existente is None:
                orden.append(k); etiqueta_de[k] = fila['etiqueta']; existente = k
            elif len(fila['etiqueta']) > len(etiqueta_de[existente]):
                etiqueta_de[existente] = fila['etiqueta']      # nos quedamos con la etiqueta completa
            valores[existente].append(fila['valor'].strip())

    salida = []
    for k in orden:
        unicos = list(dict.fromkeys(v for v in valores[k] if v))
        salida.append({'etiqueta': etiqueta_de[k].strip(),
                       'valor': SEP.join(ordenar_valores(unicos)) if len(unicos) > 1 else (unicos[0] if unicos else '')})
    return salida


def fila_ma(tabla, prods):
    """Añade/actualiza la corriente en mA con lo que diga la descripción de cada código."""
    vals = list(dict.fromkeys(f'{m} mA' for p in prods for m in p['opciones']['ma']))
    if not vals:
        return tabla
    valor = SEP.join(ordenar_valores(vals))
    for f in tabla:
        if 'corriente' in clave_etiq(f['etiqueta']) or re.search(r'\bmA\b', f['etiqueta']):
            f['valor'] = valor
            return tabla
    return tabla + [{'etiqueta': 'Corriente (mA)', 'valor': valor}]


# ── imágenes y descargas ──
def imagenes_de(refs):
    vistas, salida = set(), []
    for ref in refs:
        carpeta = os.path.join(RAIZ, 'images', 'productos', ref)
        if not os.path.isdir(carpeta):
            continue
        for f in sorted(os.listdir(carpeta)):
            if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            ruta = os.path.join(carpeta, f)
            h = hashlib.md5(open(ruta, 'rb').read()).hexdigest()
            if h not in vistas:                       # la misma foto se repite en todas las variantes
                vistas.add(h)
                salida.append(f'images/productos/{ref}/{f}')
    return salida


def titulo_descarga(prod):
    op = prod['opciones']
    bits = [f'{p}W' for p in op['potencias']] + [f'{c}K' for c in op['cct']] + [f'{m} mA' for m in op['ma']]
    if op['cct_seleccionable'] and not op['cct']:
        bits.append('CCT')
    return ' · '.join(bits) or prod['codigo']


# ── construcción ──
def construir(ruta_excel):
    productos = leer(ruta_excel)
    cat = codigos_por_categoria(ruta_excel)
    idx_pdfs = indexar_pdfs()

    grupos = defaultdict(list)
    for p in productos:
        c = cat.get(norm(p['codigo']))
        if c:
            grupos[(c, modelo(p['descripcion']))].append(p)

    fichas, incidencias = [], {'sin_pdf': [], 'pdf_ilegible': [], 'pdf_ambiguo': []}
    for (categoria, clave), prods in grupos.items():
        tablas, descargas = [], []
        for p in sorted(prods, key=lambda p: (p['opciones']['potencias'] or ['0'])[0].zfill(4)):
            rutas = pdfs_de(idx_pdfs, p['codigo'])
            if not rutas:
                incidencias['sin_pdf'].append({'codigo': p['codigo'], 'descripcion': p['descripcion']})
                continue
            if len(rutas) > 1:
                incidencias['pdf_ambiguo'].append({'codigo': p['codigo'], 'pdfs': rutas})
            ruta = rutas[0]
            try:
                tablas.append((p['codigo'], extraer_tabla(os.path.join(RAIZ, ruta))))
            except (TablaNoExtraible, Exception) as e:
                incidencias['pdf_ilegible'].append({'codigo': p['codigo'], 'pdf': ruta, 'motivo': str(e)})
                continue
            descargas.append({'ref': p['codigo'], 'titulo': titulo_descarga(p), 'pdf': ruta})

        if not tablas:
            continue
        refs = [p['codigo'] for p in prods]
        fichas.append({
            'id': re.sub(r'[^a-z0-9]+', '-', sin_tildes(nombre_producto([p['descripcion'] for p in prods])).lower()).strip('-'),
            'nombre': nombre_producto([p['descripcion'] for p in prods]),
            'categoria': categoria,
            'familia': Counter(p['familia'] for p in prods).most_common(1)[0][0],
            'refs': refs,
            'specs': fila_ma(fusionar(tablas), prods),
            'imagenes': imagenes_de(refs),
            'descargas': descargas,
        })

    # dos modelos distintos pueden quedarse con el mismo nombre (el Excel no los distingue en texto):
    # se les añade la potencia para poder diferenciarlos
    repetidos = {n for n, c in Counter((f['categoria'], f['nombre']) for f in fichas).items() if c > 1}
    for f in fichas:
        if (f['categoria'], f['nombre']) in repetidos:
            pot = next((s['valor'] for s in f['specs'] if clave_etiq(s['etiqueta']).startswith('potenciatotal')), '')
            if pot:
                f['nombre'] += f" ({pot.replace(SEP, '/')})"
                f['id'] = re.sub(r'[^a-z0-9]+', '-', sin_tildes(f['nombre']).lower()).strip('-')

    fichas.sort(key=lambda f: (f['categoria'], f['familia'], f['nombre']))
    return fichas, incidencias


if __name__ == '__main__':      # solo para inspeccionar; el JSON lo escribe generar_json.py
    fichas, inc = construir(sys.argv[1])
    print(f"{len(fichas)} fichas generadas "
          f"({sum(f['categoria']=='industrial' for f in fichas)} industrial, "
          f"{sum(f['categoria']=='interior' for f in fichas)} interior)")
    for k, v in inc.items():
        print(f"  {k}: {len(v)}")
