"""
Recorre fuentes/fichas/ y escribe data/catalogo.json con la estructura de Productos.

Cada carpeta es un nivel de navegación, sin acortar rutas: si dentro de una familia hay más
carpetas, se conservan tal cual. Los .xlsx que cuelgan de una carpeta son botones de ese nivel.

De dónde sale cada cosa:
  - Nombre de cada nivel: el nombre de la carpeta sin la numeración ("4.1.1 - CAMPANAS ALFA" -> "Campanas ALFA").
  - Código y nombre del botón: del NOMBRE DEL ARCHIVO, con formato "CÓDIGO - descripción".
    La celda de debajo de "FICHA TÉCNICA" solo se usa para comprobar, y como recambio cuando el
    nombre del archivo no trae código.
  - Nombre del botón = la descripción cortada en el primer dato técnico (ver `cortar`).
  - Dentro de una misma carpeta, las fichas con el mismo nombre se agrupan en un solo botón.

No se publica (y se explica en el informe): fichas cuyos datos del nombre no cuadran con su tabla,
fichas sin código localizable, la plantilla vacía, códigos repetidos en dos carpetas con contenido
distinto, y lo que no es una ficha (.docx, .rar, .pdf, temporales ~$).

Uso:  python scripts/catalogo/construir_estructura.py
"""
import json, os, re, sys, unicodedata, warnings
from collections import defaultdict

warnings.filterwarnings('ignore')
import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FUENTE = os.path.join(RAIZ, 'fuentes', 'fichas')
SALIDA = os.path.join(RAIZ, 'data', 'catalogo.json')
IGNORAR_CARPETAS = {'CARATULAS'}
# Fichas duplicadas que ensucian la navegación. El archivo se llama "farolas.xlsx" pero
# dentro lleva la ficha del Tubo LED T8, que ya está en Bombillas y Accesorios: hacía que
# Industriales mostrara un producto suelto detrás de sus cinco secciones.
IGNORAR_FICHAS = {os.path.join('4 - INDUSTRIALES', 'farolas.xlsx')}

# ── corte del nombre ──────────────────────────────────────────────────────────
UNIDADES = r'W|K|Kº|lm|Lm|LM|V|mA|Ah|h|H|mm|cm|m|º|°|%'
NUM = r'\d+(?:[.,]\d+)?'
# un rango cuenta entero: "60-80-100W"
RANGO_CON_UNIDAD = rf'{NUM}(?:\s*[-/]\s*{NUM})*\s*(?:{UNIDADES})\b'
# una medida encadenada cuenta entera aunque solo la última cifra lleve unidad: "19,5 X 20H X 2000mm"
MEDIDA_ENCADENADA = rf'{NUM}\s*[Hh]?\s*[Xx]\s*{NUM}'
TERMINOS = (r'CRI|IP\d*|IK\d*|UGR|DALI\s*2?|CCT|SMD\s*\d*|RGB|RGBW|PWM|TRIAC|PUSH\s*DIM|CASAMBI|'
            r'BLUETOOTH|AUTOTEST|ON\s*[-/]\s*OFF|MULTIVAT\w*|\d\s*-\s*10\s*V|3000K')
CORTE = re.compile(rf'(?<![\w.]) (?: {MEDIDA_ENCADENADA} | {RANGO_CON_UNIDAD} | (?:{TERMINOS})\b )',
                   re.I | re.X)

# la 'x' solo se quita si va suelta: 'calleS x' sí, pero 'mod. NEX' no
RESTOS = re.compile(r'(?:[\s\-–—_,.;:/(]+|\s+[xX×])+$')


def cortar(descripcion):
    """Deja el nombre comercial: corta en el primer dato técnico y limpia lo que quede suelto."""
    m = CORTE.search(descripcion)
    nombre = descripcion[:m.start()] if m else descripcion
    nombre = re.sub(r'\s+', ' ', nombre).strip()
    anterior = None
    while anterior != nombre:                       # "… 1 calle x" -> "… 1 calle"
        anterior = nombre
        nombre = RESTOS.sub('', nombre).strip()
    return nombre


# ── nombres de carpeta ────────────────────────────────────────────────────────
# Solo es numeración si detrás lleva guion: "4.1.1 - CAMPANAS" sí, "12V" o "5CLIM" no.
NUMERACION = re.compile(r'^\s*\d+(?:\s*\.\s*\d+)*\s*[-–]\s*')
SIGLAS = {'LED', 'CCT', 'RGB', 'SMD', 'COB', 'AC', 'DC', 'DALI', 'UGR', 'CRI', 'IP', 'IK',
          'ON-OFF', 'PAR', 'SEC', 'CAP', 'ZEN', 'NEX', 'MIN', 'MIX', 'OCU', 'TAC', 'CAM', 'SOL',
          'ALFA', 'SLIM', 'PIC', 'CLIP', 'ZOOM', 'MODEN', 'GRACION', 'CJV', 'ABAX', 'EXIT', 'AXP',
          'LI', 'ST', 'SO', 'LG', 'VA', 'MN', 'TC', 'MI4', 'SLI-L'}
ENLACES = {'y', 'o', 'de', 'del', 'la', 'el', 'los', 'las', 'para', 'con', 'en', 'a', 'al', 'por'}

# Erratas del origen que estropean la navegación. Las erratas de las tablas NO se corrigen
# (van apuntadas en docs/catalogo/erratas.md); esto es solo para que un producto no salga
# partido en dos ni una sección se llame algo que no describe lo que hay dentro.
FICHAS_RENOMBRADAS = {
    # al Excel se le come un espacio y ZEN salía como dos productos distintos
    'Downlight empotradofijo mod. ZEN': 'Downlight empotrado fijo mod. ZEN',
    # esta ficha no trae código ni descripción al principio, y el nombre salía de la línea
    # donde enumera los aparatos con los que miden la fuente
    '5B, generador de pulsos de grupo rápido: Everfine EMS61000-4A, analizador de espectro: '
    'KH3935, probador de alta tensión': 'Fuente de alimentación LIFUD 24V IP20',
}
CARPETAS_RENOMBRADAS = {
    # la carpeta dice "24V IP20 ON-OFF" pero dentro hay 12V y 24V, IP65 e IP67
    'Fuentes de Alimentación 24V IP20 ON-OFF': 'Fuentes de Alimentación',
}


def limpiar_nombre(carpeta):
    """'4.1.1 - CAMPANAS ALFA' -> 'Campanas ALFA'. Respeta siglas, modelos y medidas."""
    txt = re.sub(r'\s+', ' ', NUMERACION.sub('', carpeta).strip(' -–_'))
    palabras = []
    for i, p in enumerate(txt.split(' ')):
        desnudo = p.strip('()[]')
        if not desnudo:
            palabras.append(p)
        elif i and desnudo.lower() in ENLACES:                   # "Y", "DE"... antes que las siglas
            palabras.append(p.lower())
        elif desnudo.upper() in SIGLAS or re.search(r'\d', desnudo) or (len(desnudo) <= 2 and desnudo.isupper()):
            palabras.append(p)                                  # sigla, modelo o medida: tal cual
        else:
            palabras.append(p[0].upper() + p[1:].lower() if p[0].isalpha() else p.capitalize())
    # macOS guarda los acentos descompuestos en los nombres de archivo: se recomponen
    # para que las correcciones de arriba casen con lo que se escribe aquí.
    return unicodedata.normalize('NFC', ' '.join(palabras))


def slug(texto):
    sin = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', sin.lower()).strip('-')


# ── lectura de las fichas ─────────────────────────────────────────────────────
PATRON_CODIGO = re.compile(r'^\s*([A-Z0-9][A-Z0-9./\-]{4,}?)\s*[-–_]\s*(.+)$', re.I)
es_ficha = lambda f: f.lower().endswith('.xlsx') and not f.startswith('~$')


def partir_codigo(texto):
    m = PATRON_CODIGO.match(texto.replace('\n', ' '))
    if not m:
        return None, texto.strip()
    codigo, desc = m.group(1).strip(), m.group(2).strip()
    if not re.search(r'\d', codigo):                # "PERFILES PARA EMPOTRAR - ..." no es un código
        return None, texto.strip()
    return codigo, desc


def celda_ficha(ws):
    """Celda con 'CÓDIGO - descripción'. Primero la de debajo de FICHA TÉCNICA, luego cualquiera."""
    filas = list(ws.iter_rows(min_row=1, max_row=20, max_col=6))
    fila_titulo = None
    for i, fila in enumerate(filas):
        for c in fila:
            if isinstance(c.value, str) and 'FICHA TÉCNICA' in c.value.upper():
                fila_titulo = i
                break
        if fila_titulo is not None:
            break
    orden = (filas[fila_titulo + 1:] + filas[:fila_titulo]) if fila_titulo is not None else filas
    for fila in orden:
        for c in fila:
            if isinstance(c.value, str) and partir_codigo(c.value)[0]:
                return c.value.strip(), c.coordinate
    return None, None


ETIQUETAS = {'potencia': 'W', 'lúmenes': 'lm', 'lumenes': 'lm', 'temperatura de color': 'K'}


def datos_tabla(ws):
    """{'W': [..], 'lm': [..], 'K': [..]} con las cifras que declara la tabla de características."""
    datos = defaultdict(list)
    for fila in ws.iter_rows(min_row=1, max_row=40, max_col=3):
        etiqueta = fila[0].value
        if not isinstance(etiqueta, str):
            continue
        baja = etiqueta.lower()
        if 'factor de potencia' in baja:            # no es un vataje
            continue
        clave = next((v for k, v in ETIQUETAS.items() if k in baja), None)
        if not clave:
            continue
        for c in fila[1:]:
            if c.value is not None:
                datos[clave] += re.findall(NUM, str(c.value).replace('.', ''))
    return datos


def cifras_del_nombre(desc):
    salida = defaultdict(list)
    for num, uni in re.findall(rf'({NUM})\s*(W|lm|Lm|LM|K)\b', desc):
        salida['lm' if uni.lower() == 'lm' else uni.upper()].append(num.replace('.', ''))
    return salida


def cuadra(desc, tabla):
    """¿Las cifras del nombre aparecen en la tabla? Solo se comprueba lo que ambos declaran."""
    faltan = []
    for clave, valores in cifras_del_nombre(desc).items():
        if not tabla.get(clave):
            continue
        for v in valores:
            if v not in tabla[clave]:
                faltan.append(f'{v}{clave}')
    return (not faltan), faltan


# ── recorrido ─────────────────────────────────────────────────────────────────
incidencias = {'sin_codigo': [], 'sin_nombre': [], 'no_cuadra': [], 'plantilla': [], 'codigo_distinto': [],
               'no_es_ficha': [], 'repetido_distinto': [], 'repetido_igual': []}
fichas_por_codigo = defaultdict(list)


def leer_ficha(ruta, relativa):
    archivo = os.path.basename(ruta)
    codigo, desc = partir_codigo(os.path.splitext(archivo)[0])
    origen = 'nombre del archivo'
    try:
        ws = openpyxl.load_workbook(ruta, data_only=True).worksheets[0]
        texto_celda, coord = celda_ficha(ws)
        tabla = datos_tabla(ws)
    except Exception as e:
        incidencias['sin_codigo'].append((relativa, f'no se puede abrir: {type(e).__name__}'))
        return None

    if not codigo:                                   # recambio: buscarlo dentro de la hoja
        if texto_celda:
            codigo, desc = partir_codigo(texto_celda)
            origen = f'celda {coord}'
        if not codigo:
            incidencias['sin_codigo'].append((relativa, 'ni el nombre del archivo ni la hoja traen código'))
            return None

    nombre = cortar(desc)
    if re.search(r'MEDIDA\s*-\s*NOMBRE', nombre, re.I):
        incidencias['plantilla'].append((relativa, 'plantilla sin rellenar (MEDIDA-NOMBRE-WATTS-Kº)'))
        return None
    if not nombre:
        incidencias['sin_nombre'].append((relativa, f'la descripción se queda vacía al quitar los datos técnicos: {desc[:70]!r}'))
        return None

    if texto_celda:
        cod_celda = partir_codigo(texto_celda)[0]
        if cod_celda and cod_celda.upper().replace('O', '0') != codigo.upper().replace('O', '0'):
            ok, faltan = cuadra(desc, tabla)
            incidencias['codigo_distinto'].append((relativa, codigo, cod_celda, ok, faltan))
            if not ok:
                incidencias['no_cuadra'].append((relativa, codigo, faltan, dict(tabla)))
                return None

    return {'codigo': codigo, 'nombre': FICHAS_RENOMBRADAS.get(nombre, nombre), 'descripcion': desc,
            'archivo': relativa, 'origen_codigo': origen}


def recorrer(carpeta, relativa=''):
    nodo_hijos, fichas = [], []
    for entrada in sorted(os.listdir(carpeta)):
        if entrada.startswith('.') or entrada in IGNORAR_CARPETAS:
            continue
        ruta = os.path.join(carpeta, entrada)
        rel = os.path.join(relativa, entrada)
        if os.path.isdir(ruta):
            hijo = recorrer(ruta, rel)
            if hijo['hijos'] or hijo['botones']:     # las carpetas vacías no se muestran
                nodo_hijos.append(hijo)
        elif rel in IGNORAR_FICHAS:
            incidencias['no_es_ficha'].append(f'{rel} (duplicada: es el Tubo LED T8 de Bombillas)')
        elif es_ficha(entrada):
            f = leer_ficha(ruta, rel)
            if f:
                fichas.append(f)
                fichas_por_codigo[f['codigo'].upper().replace('O', '0')].append(f)
        elif entrada != '.DS_Store':
            incidencias['no_es_ficha'].append(rel)

    agrupados = defaultdict(list)
    for f in fichas:
        agrupados[f['nombre']].append(f)
    botones = [{'nombre': n, 'slug': slug(n),
                'codigos': [f['codigo'] for f in g],
                'archivos': [f['archivo'] for f in g]}
               for n, g in sorted(agrupados.items())]
    nombre_nodo = limpiar_nombre(os.path.basename(carpeta)) if relativa else 'Productos'
    nombre_nodo = CARPETAS_RENOMBRADAS.get(nombre_nodo, nombre_nodo)
    return {'nombre': nombre_nodo,
            'slug': slug(nombre_nodo) if relativa else 'productos',
            'ruta': relativa, 'hijos': nodo_hijos, 'botones': botones}


def quitar_repetidos_distintos(arbol):
    """Un mismo código en dos carpetas: si las fichas coinciden, se deja; si no, fuera las dos."""
    fuera = set()
    for codigo, lista in fichas_por_codigo.items():
        carpetas = {os.path.dirname(f['archivo']) for f in lista}
        if len(carpetas) < 2:
            continue
        nombres = {f['nombre'] for f in lista}
        if len(nombres) == 1:
            incidencias['repetido_igual'].append((codigo, sorted(f['archivo'] for f in lista)))
        else:
            incidencias['repetido_distinto'].append((codigo, sorted((f['archivo'], f['nombre']) for f in lista)))
            fuera.update(f['archivo'] for f in lista)

    def podar(nodo):
        for b in nodo['botones']:
            quedan = [(c, a) for c, a in zip(b['codigos'], b['archivos']) if a not in fuera]
            b['codigos'] = [c for c, _ in quedan]
            b['archivos'] = [a for _, a in quedan]
        nodo['botones'] = [b for b in nodo['botones'] if b['archivos']]
        nodo['hijos'] = [podar(h) for h in nodo['hijos']]
        nodo['hijos'] = [h for h in nodo['hijos'] if h['hijos'] or h['botones']]
        return nodo

    return podar(arbol)


if __name__ == '__main__':
    if not os.path.isdir(FUENTE):
        sys.exit(f'No encuentro {FUENTE}')
    arbol = quitar_repetidos_distintos(recorrer(FUENTE))
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump({'arbol': arbol, 'incidencias': {k: v for k, v in incidencias.items()}},
              open(SALIDA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    def contar(n):
        return len(n['botones']) + sum(contar(h) for h in n['hijos'])
    def fichas_de(n):
        return sum(len(b['archivos']) for b in n['botones']) + sum(fichas_de(h) for h in n['hijos'])
    print(f"{SALIDA}: {contar(arbol)} botones · {fichas_de(arbol)} fichas publicadas")
    for k, v in incidencias.items():
        print(f'   {k}: {len(v)}')
