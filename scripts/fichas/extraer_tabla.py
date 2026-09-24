"""
Extrae la tabla "Características técnicas" de una ficha técnica en PDF de Apheloria.

Probado con 00EMEEXITS150.pdf (19 filas), 00DLZEN07W27X.pdf (21) y 00PLAFIP6512W.pdf (21).
Por qué no sirven pdfplumber.extract_tables() ni la lectura de texto normal:
  - la tabla no tiene líneas, solo fondos beige alternos, así que no se detecta como tabla;
  - en el texto plano, los valores de dos líneas (p. ej. "Protecciones") acaban al final de la página;
  - la estrategia "text" parte celdas por la mitad ("poli | carbonato blanco").

Cómo lee este script: las bandas beige de la columna izquierda marcan una fila sí y otra no, así que
las bandas y los huecos entre ellas dan la rejilla exacta de filas, incluidas las más altas de lo
normal (p. ej. "Opcional regulación DALI..." ocupa 3 líneas de etiqueta con un solo valor).
Dentro de cada fila, es etiqueta lo que empieza en el margen izquierdo y valor todo lo demás.

Uso:  python extraer_tabla.py ficha.pdf
"""
import pdfplumber, re, sys, json

X_TABLA_MAX = 340   # la tabla ocupa la mitad izquierda de la página (A4 = 595 pt de ancho)
MARGEN_ETIQ = 3     # tolerancia en pt para considerar que una palabra empieza en el margen izquierdo
Y_CABECERA = 170    # por encima solo hay logo y línea de cabecera (fichas sin el título de la tabla)


class TablaNoExtraible(Exception):
    """La ficha no sigue la plantilla (otro proveedor, PDF escaneado...). No inventamos datos."""


def _mediana(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2]


def _filas_por_bandas(bandas, y_fin):
    """Devuelve los intervalos (top, bottom) de todas las filas: cada banda y cada hueco entre bandas.

    Por debajo de la última banda se sigue el mismo ritmo (banda/hueco alternos) en vez de meter todo
    lo que quede en una sola fila, porque algunas plantillas terminan la tabla sin banda.
    """
    cortes = []
    for b in bandas:
        cortes += [b['top'], b['bottom']]
    cortes = sorted(set(round(c, 1) for c in cortes))

    alto = _mediana([b['bottom'] - b['top'] for b in bandas])
    huecos = [bandas[i + 1]['top'] - bandas[i]['bottom'] for i in range(len(bandas) - 1)]
    hueco = _mediana(huecos) if huecos else alto
    y = cortes[-1]
    siguiente = hueco
    while y < y_fin:                               # continúa la rejilla hasta pasar el último texto
        cortes.append(round(y + siguiente, 1))
        y += siguiente
        siguiente = alto if siguiente == hueco else hueco
    return [(cortes[i], cortes[i + 1]) for i in range(len(cortes) - 1)]


def extraer_tabla(ruta):
    p = pdfplumber.open(ruta).pages[0]
    if not p.chars:
        raise TablaNoExtraible("PDF sin texto (escaneado): habría que pasarle OCR")

    words = p.extract_words(keep_blank_chars=True, x_tolerance=2)
    head = next((w for w in words if w['text'].startswith('Características')), None)
    y_titulo = head['bottom'] + 2 if head else Y_CABECERA   # algunas fichas no llevan ese título

    bandas = sorted([r for r in p.rects
                     if r['x1'] <= X_TABLA_MAX and r['top'] > y_titulo and 8 <= r['bottom'] - r['top'] <= 25],
                    key=lambda r: r['top'])
    if not bandas:
        raise TablaNoExtraible("no encuentro las bandas de fondo de la tabla (otra plantilla)")

    # la tabla empieza en la primera banda: lo de más arriba es cabecera o subtítulo, no una fila
    y_inicio = bandas[0]['top'] - 2
    zona = [w for w in words if (w['top'] + w['bottom']) / 2 > y_inicio and w['x1'] <= X_TABLA_MAX]
    if not zona:
        raise TablaNoExtraible("no hay texto en la zona de la tabla")

    filas = _filas_por_bandas(bandas, max(w['bottom'] for w in zona))
    margen = min(w['x0'] for w in zona)

    celdas = [{'etiqueta': [], 'valor': []} for _ in filas]
    for w in sorted(zona, key=lambda w: (w['top'], w['x0'])):
        centro = (w['top'] + w['bottom']) / 2
        i = next((k for k, (t, b) in enumerate(filas) if t <= centro < b), None)
        if i is None:                                   # fuera de la rejilla: a la fila más cercana
            i = min(range(len(filas)), key=lambda k: abs((filas[k][0] + filas[k][1]) / 2 - centro))
        celdas[i]['etiqueta' if w['x0'] <= margen + MARGEN_ETIQ else 'valor'].append(w['text'].strip())

    limpiar = lambda ps: re.sub(r'\s+', ' ', re.sub(r'-\s+', '- ', ' '.join(ps))).strip()
    salida = []
    for c in celdas:
        etiqueta = limpiar(c['etiqueta']).rstrip(':').strip()
        valor = limpiar(c['valor'])
        if etiqueta or valor:
            salida.append({'etiqueta': etiqueta, 'valor': valor})
    if not salida:
        raise TablaNoExtraible("la tabla sale vacía")
    return salida


if __name__ == '__main__':
    print(json.dumps(extraer_tabla(sys.argv[1]), ensure_ascii=False, indent=2))
