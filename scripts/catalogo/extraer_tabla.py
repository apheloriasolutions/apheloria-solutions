"""
Saca de cada ficha .xlsx la tabla de características, las notas al pie y la descripción,
las junta en una sola tabla por grupo y lo guarda todo en data/catalogo.json.

Solo se lee la PRIMERA hoja: la segunda trae referencias de proveedor y no se publica nunca.

Reglas (acordadas con el cliente):
  - La tabla es columna A = etiqueta, columna B = valor. Empieza en la primera fila cuya
    columna A acaba en dos puntos (no se busca el título "Características técnicas":
    54 fichas no lo llevan y empiezan directas en "Material:").
  - Acaba en la primera fila del todo vacía.
  - Las filas con etiqueta pero sin valor se ocultan.
  - Una etiqueta de más de LARGO_NOTA caracteres no es un dato, es una frase: va a nota al pie.
  - Al juntar un grupo, los valores distintos se separan con " - ".
  - Las erratas no se corrigen: se apuntan en docs/catalogo/erratas.md.

Uso:  python scripts/catalogo/extraer_tabla.py [--prueba]
      --prueba  solo los grupos de muestra; escribe docs/catalogo/tabla-prueba.html
                y no toca data/catalogo.json
      --todo    lo mismo pero con los 214 grupos, en docs/catalogo/tablas.html
"""
import difflib, html, json, os, re, sys, warnings
from collections import Counter

warnings.filterwarnings('ignore')
import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHAS = os.path.join(RAIZ, 'fuentes', 'fichas')
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
DOCS = os.path.join(RAIZ, 'docs', 'catalogo')

LARGO_NOTA = 45       # una etiqueta más larga que esto es una frase, no un dato
MINIMO_FILAS = 3      # menos filas que esto no es una tabla
PRUEBA = ('Luminaria tipo cardan doble mod. CAR blanco', 'Luminaria tipo cardan mod. CAR blanco',
          'Downlight empotrado fijo mod. ZEN', 'Downlight empotrado fijo mod. NEX',
          'Tira de Led flexible', 'Perfil de aluminio B1 de superficie')


def limpiar(texto):
    """Junta los saltos de línea y el relleno de espacios con el que están maquetadas las celdas."""
    t = re.sub(r'\s+', ' ', str(texto)).strip()
    return re.sub(r'[\s:]+$', '', t)


def inicio_tabla(hoja):
    for r in range(1, min(hoja.max_row, 30) + 1):
        a = hoja.cell(row=r, column=1).value
        if isinstance(a, str) and a.strip().endswith(':') and len(a.strip()) > 3:
            return r
    return None


def descripcion_de(hoja):
    """El párrafo de descripción vive en una sola celda de la columna D, con la palabra
    "Descripción" delante y mucho relleno de espacios."""
    for r in range(1, min(hoja.max_row, 40) + 1):
        for c in range(3, min(hoja.max_column, 12) + 1):
            v = hoja.cell(row=r, column=c).value
            if isinstance(v, str) and 'escripci' in v:
                cuerpo = re.sub(r'^\s*Descripci[oó]n\s*', '', v.strip(), flags=re.I)
                cuerpo = re.sub(r'\s*\n\s*', ' ', cuerpo)
                return re.sub(r'\s{2,}', ' ', cuerpo).strip()
    return ''


def notas_sueltas(hoja, desde):
    """Algunas fichas (sobre todo los perfiles) llevan un bloque "NOTAS IMPORTANTES" suelto
    por debajo de la tabla, con las frases partidas en varias filas."""
    inicio = None
    for r in range(desde, hoja.max_row + 1):
        v = hoja.cell(row=r, column=1).value
        if isinstance(v, str) and v.strip().upper().startswith('NOTAS'):
            inicio = r + 1
            break
        if isinstance(v, str) and 'FICHA TÉCNICA' in v.upper():
            return []   # la hoja repite un segundo bloque entero: ahí ya no hay notas
    if inicio is None:
        return []
    notas = []
    for r in range(inicio, hoja.max_row + 1):
        v = hoja.cell(row=r, column=1).value
        if not isinstance(v, str) or len(v.strip()) < 3:
            continue
        linea = limpiar(v)
        if linea.upper().startswith('FICHA TÉCNICA'):
            break
        if notas and not re.match(r'^[–—\-•*]', linea):
            notas[-1] += ' ' + linea      # es la continuación de la frase anterior
        else:
            notas.append(re.sub(r'^[–—\-•*]\s*', '', linea))
    return notas


def leer_ficha(rel):
    """→ {filas: [[etiqueta, valor]], notas: [texto], descripcion: str} o None si no hay tabla."""
    hoja = openpyxl.load_workbook(os.path.join(FICHAS, rel), data_only=True).worksheets[0]
    ini = inicio_tabla(hoja)
    if not ini:
        return None, 'no se encuentra el arranque de la tabla'

    crudas = []
    for r in range(ini, hoja.max_row + 1):
        a, b = hoja.cell(row=r, column=1).value, hoja.cell(row=r, column=2).value
        if a in (None, '') and b in (None, ''):
            if crudas:
                break
            continue
        crudas.append((r, '' if a is None else str(a), '' if b is None else str(b)))

    if len(crudas) < MINIMO_FILAS:
        return None, f'solo {len(crudas)} filas'
    if sum(1 for _, _, v in crudas if v.strip()) * 2 < len(crudas):
        return None, 'casi ninguna fila tiene valor: es un párrafo, no una tabla'

    filas, notas = [], []
    for r, a, b in crudas:
        etiqueta, valor = limpiar(a), limpiar(b)
        if len(a.strip()) > LARGO_NOTA:
            notas.append(f'{etiqueta}: {valor}' if valor else etiqueta)
        elif valor:
            filas.append([etiqueta, valor, r])
    notas += notas_sueltas(hoja, crudas[-1][0] + 1)
    return {'filas': filas, 'notas': notas, 'descripcion': descripcion_de(hoja)}, None


DATO_SUELTO = re.compile(r'^\d+(?:[.,]\d+)?\s*(?:W|w|K|k|lm|Lm|mm|cm|m|V|v|º|°|%)?$')


def fundir_tramo(variantes):
    """Junta lo que cambia de una ficha a otra: 7W, 12W, 20W → 7-12-20W. Devuelve None si lo
    que cambia no es un dato suelto, porque entonces fundirlo dejaría una frase rota."""
    v = []
    for x in variantes:
        if x not in v:
            v.append(x)
    if len(v) == 1:
        return v[0]
    pre = os.path.commonprefix(v)
    suf = os.path.commonprefix([x[::-1] for x in v])[::-1]
    # el factor común no puede partir una cifra: con 2700K/3000K/4000K sobraría "00K"
    pre = pre.rstrip('0123456789')
    suf = suf.lstrip('0123456789')
    if len(pre) + len(suf) > min(len(x) for x in v):
        return None
    medios, espacio = [], False
    for x in v:
        medio = x[len(pre):len(x) - len(suf)]
        espacio = espacio or medio[:1].isspace()
        medio = medio.strip()
        if medio and not DATO_SUELTO.match(medio):
            return None
        if medio not in medios:
            medios.append(medio)
    medios = [m for m in medios if m]
    if not medios:
        return v[0]                      # solo cambiaban los espacios
    if all(m.isdigit() for m in medios):
        medios.sort(key=int)
    return pre.rstrip() + (' ' if espacio else '') + '-'.join(medios) + suf


def fundir_descripciones(textos):
    """Si las descripciones de un grupo solo cambian en un dato suelto (casi siempre los vatios),
    se juntan en una sola. Si cambian de verdad, se dejan por separado."""
    if len(textos) < 2:
        return textos
    base = textos[0].split()
    cambios = {}
    for t in textos[1:]:
        otros = t.split()
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, otros,
                                                           autojunk=False).get_opcodes():
            if tag == 'equal':
                continue
            if i2 - i1 > 4 or j2 - j1 > 4 or i1 == i2 or j1 == j2:
                return textos            # cambia demasiado, o sobra/falta texto
            cambios.setdefault((i1, i2), []).append(' '.join(otros[j1:j2]))
    if not cambios or len(cambios) > 3:
        return textos
    tramos = sorted(cambios)
    if any(a2 > b1 for (_, a2), (b1, _) in zip(tramos, tramos[1:])):
        return textos                    # los tramos que cambian se pisan entre sí

    salida, pos = [], 0
    for tramo in tramos:
        junto = fundir_tramo([' '.join(base[tramo[0]:tramo[1]])] + cambios[tramo])
        if junto is None:
            return textos
        salida += base[pos:tramo[0]]
        salida.append(junto)
        pos = tramo[1]
    salida += base[pos:]
    return [' '.join(salida)]


def sin_redundantes(trozos):
    """Quita el trozo que ya aparece entero dentro de otro: con "2700K-4000K-6000K" en la lista,
    el "2700K" suelto no aporta nada."""
    return [p for p in trozos
            if not any(q is not p and len(q) > len(p)
                       and re.search(rf'(?<![\w]){re.escape(p)}(?![\w])', q, re.I)
                       for q in trozos)]


def juntar(fichas):
    """Una sola tabla por grupo: etiquetas en orden de aparición, valores distintos con ' - '."""
    orden, valores = [], {}
    for f in fichas.values():
        for et, val, _ in f['filas']:
            if et not in valores:
                orden.append(et)
                valores[et] = []
            # algún valor ya trae varias opciones separadas con " - ": se parte para no repetirlas
            for trozo in [x.strip() for x in val.split(' - ')]:
                if trozo and trozo.lower() not in {v.lower() for v in valores[et]}:
                    valores[et].append(trozo)
    tabla = [[et, ' - '.join(sin_redundantes(valores[et]))] for et in orden if valores[et]]

    notas, vistas = [], set()
    for f in fichas.values():
        for n in f['notas']:
            if n.lower() not in vistas:
                vistas.add(n.lower())
                notas.append(n)
    descripciones = []
    for f in fichas.values():
        d = f['descripcion']
        if d and d not in descripciones:
            descripciones.append(d)
    return tabla, notas, fundir_descripciones(descripciones)


def erratas_de(cod, rel, ficha):
    """Lo que canta a errata del Excel. No se corrige nada: solo se apunta."""
    avisos = []
    repes = [e for e, n in Counter(e for e, _, _ in ficha['filas']).items() if n > 1]
    for e in repes:
        avisos.append((cod, rel, e, 'la etiqueta sale dos veces en la misma ficha'))
    for et, val, r in ficha['filas']:
        e, v = et.lower(), val.lower()
        if 'lúmenes' in e or 'lumenes' in e:
            if 'lm/w' in v.replace(' ', ''):
                avisos.append((cod, rel, f'A{r} {et} = {val}', 'lúmenes expresados en lm/W'))
        if 'garantía' in e and re.search(r'\d\s*h\b', v) and 'año' not in v:
            avisos.append((cod, rel, f'A{r} {et} = {val}', 'la garantía viene en horas, no en años'))
        if re.search(r'\bXX+\b', val):
            avisos.append((cod, rel, f'A{r} {et} = {val}', 'la ficha trae XX como comodín'))
        for palabra in ('Correlecionada', 'Azúl', 'BLUETHOOH', 'hospitalaría', 'támbien', 'ños'):
            if re.search(rf'\b{palabra}\b', f'{et} {val}', re.I):
                avisos.append((cod, rel, f'A{r} {et} = {val}', f'falta de ortografía: "{palabra}"'))
    return avisos


def botones(nodo, ruta=()):
    for b in nodo['botones']:
        yield ruta, b
    for h in nodo['hijos']:
        yield from botones(h, ruta + (h['nombre'],))


def pagina_prueba(muestras, salida):
    """Tabla del grupo al lado de lo que dice cada ficha, para revisarlo de un vistazo."""
    bloques = []
    for ruta, b, fichas, tabla, notas, descripciones in muestras:
        codigos = list(fichas)
        cab = ''.join(f'<th class="ficha">{html.escape(c)}</th>' for c in codigos)
        etiquetas = [e for e, _ in tabla] + [e for e in
                     dict.fromkeys(et for f in fichas.values() for et, _, _ in f['filas'])
                     if e not in {x for x, _ in tabla}]
        cuerpo = []
        for et in etiquetas:
            junto = next((v for e, v in tabla if e == et), '')
            celdas = []
            for c in codigos:
                v = next((v for e, v, _ in fichas[c]['filas'] if e == et), '')
                celdas.append(f'<td class="{"vacia" if not v else ""}">{html.escape(v)}</td>')
            vals = {v for e, v, _ in (x for f in fichas.values() for x in f['filas']) if e == et}
            cuerpo.append(f'<tr><th>{html.escape(et)}</th>'
                          f'<td class="junto{" varios" if len(vals) > 1 else ""}">{html.escape(junto)}</td>'
                          + ''.join(celdas) + '</tr>')
        bloques.append(
            f'<h2>{html.escape(b["nombre"])}</h2>'
            f'<p class="ruta">{html.escape(" › ".join(ruta))} · {len(codigos)} ficha(s)</p>'
            f'<div class="tabla"><table><tr><th></th>'
            f'<th class="junto">lo que sale en la web</th>{cab}</tr>'
            + ''.join(cuerpo) + '</table></div>'
            + (('<p class="notas"><strong>Notas al pie:</strong><br>' +
                '<br>'.join(html.escape(n) for n in notas) + '</p>') if notas else '')
            + ('<p class="desc"><strong>Descripción</strong><br>' +
               '<br><br>'.join(html.escape(d) for d in descripciones) + '</p>'
               if descripciones else '<p class="notas">sin descripción</p>'))

    doc = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Tablas de características — prueba</title><style>
 body { font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 1.5rem;
        background: #F2EDE4; color: #1a1612; }
 h1 { font-size: 1.3rem; font-weight: 500; }
 h2 { font-size: 1rem; font-weight: 600; margin: 2.2rem 0 .1rem; }
 .ruta { font-size: .75rem; text-transform: uppercase; letter-spacing: .08em;
         color: #857a68; margin: 0 0 .6rem; }
 table { border-collapse: collapse; background: #fff; font-size: .78rem; }
 .tabla { overflow-x: auto; scrollbar-width: thin; scrollbar-color: #c8bfb0 transparent; }
 .tabla::-webkit-scrollbar { width: 8px; height: 8px; }
 .tabla::-webkit-scrollbar-thumb { background: #c8bfb0; border-radius: 4px; }
 th, td { border: 1px solid #e6e0d6; padding: .3rem .5rem; text-align: left;
          vertical-align: top; white-space: nowrap; }
 tr > th:first-child { font-weight: 400; }
 .ficha { font-size: .68rem; font-weight: 400; color: #857a68; }
 .junto { background: #f7f3ec; font-weight: 600; }
 .varios { background: #eef4ec; }
 .vacia { background: #fbeceb; }
 .notas, .desc { font-size: .78rem; max-width: 60rem; background: #fff;
                 border: 1px solid #e6e0d6; padding: .6rem .8rem; margin: .5rem 0 0; }
 .desc { color: #4a4238; }
</style></head><body>
<h1>Tablas de características</h1>
<p class="ruta">Columna beige: la tabla que saldría en la web. Verde: valores que difieren
entre fichas y se juntan con " - ". Rojo: la ficha no trae ese dato.</p>
""" + ''.join(bloques) + '</body></html>'
    open(salida, 'w', encoding='utf-8').write(doc)


def main():
    todo = '--todo' in sys.argv
    prueba = todo or '--prueba' in sys.argv
    catalogo = json.load(open(DATOS, encoding='utf-8'))
    cache, erratas, sin_tabla = {}, [], []
    muestras, n_grupos, n_fichas = [], 0, 0

    for ruta, b in botones(catalogo['arbol']):
        if prueba and not todo and b['nombre'] not in PRUEBA:
            continue
        fichas = {}
        for cod, rel in zip(b['codigos'], b['archivos']):
            if rel not in cache:
                try:
                    cache[rel] = leer_ficha(rel)
                except Exception as e:
                    cache[rel] = (None, f'no se puede leer: {e}')
            ficha, motivo = cache[rel]
            if ficha is None:
                sin_tabla.append((cod, rel, motivo))
                continue
            fichas[cod] = ficha
            erratas += erratas_de(cod, rel, ficha)
            n_fichas += 1
        if not fichas:
            b['tabla'], b['notas'], b['descripcion'] = [], [], []
            continue
        tabla, notas, descripciones = juntar(fichas)
        n_grupos += 1
        if prueba:
            muestras.append((ruta, b, fichas, tabla, notas, descripciones))
        else:
            b['tabla'] = tabla
            b['notas'] = notas
            b['descripcion'] = descripciones
            b['tabla_por_codigo'] = {c: {'filas': [[e, v] for e, v, _ in f['filas']],
                                         'notas': f['notas'], 'descripcion': f['descripcion']}
                                     for c, f in fichas.items()}

    os.makedirs(DOCS, exist_ok=True)
    if prueba:
        salida = os.path.join(DOCS, 'tablas.html' if todo else 'tabla-prueba.html')
        pagina_prueba(muestras, salida)
        print(f'{salida}: {n_grupos} grupos · {n_fichas} fichas')
    else:
        json.dump(catalogo, open(DATOS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{DATOS}: tabla en {n_grupos} grupos · {n_fichas} fichas')

    vistas, lineas = set(), []
    for cod, rel, donde, motivo in erratas:
        clave = (cod, donde, motivo)
        if clave in vistas:
            continue
        vistas.add(clave)
        lineas.append(f'| `{cod}` | {motivo} | {donde} |')
    cab = ['# Erratas de las fichas', '',
           'Sacado por `scripts/catalogo/extraer_tabla.py` al leer las tablas. **Nada de esto se',
           'corrige en la web**: sale tal cual lo dice el Excel. Es la lista para quien mantiene',
           'las fichas.', '', f'{len(lineas)} avisos.', '',
           '| Ficha | Qué pasa | Dónde |', '|---|---|---|']
    pie = ['', '## Fichas sin tabla', '',
           f'{len(sin_tabla)} fichas. No se les puede sacar tabla; de momento se quedan fuera.', '']
    pie += [f'- `{cod}` — {motivo}  \n  `{rel}`' for cod, rel, motivo in sin_tabla]
    open(os.path.join(DOCS, 'erratas.md'), 'w', encoding='utf-8').write(
        '\n'.join(cab + lineas + pie) + '\n')
    print(f"{os.path.join(DOCS, 'erratas.md')}: {len(lineas)} erratas · {len(sin_tabla)} sin tabla")


if __name__ == '__main__':
    main()
