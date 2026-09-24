"""
Extrae la tabla "Características técnicas" de una ficha técnica en PDF de Apheloria.

Probado con 00EMEEXITS150.pdf: saca las 19 filas completas y en orden.
Por qué no sirven pdfplumber.extract_tables() ni la lectura de texto normal:
  - la tabla no tiene líneas, solo fondos beige alternos, así que no se detecta como tabla;
  - en el texto plano, los valores de dos líneas (p. ej. "Protecciones") acaban al final de la página;
  - la estrategia "text" parte celdas por la mitad ("poli | carbonato blanco").
Este script lee por coordenadas: columna de etiquetas a la izquierda, columna de valores a la derecha,
y asigna cada línea de valor a la etiqueta más cercana en vertical.

Uso:  python extraer_tabla.py ficha.pdf
"""
import pdfplumber, re, sys, json

X_TABLA_MAX = 330   # la tabla ocupa la mitad izquierda de la página (A4 = 595 pt de ancho)
X_CORTE = 195       # a la izquierda de esta x están las etiquetas y a la derecha los valores

def extraer_tabla(ruta):
    p = pdfplumber.open(ruta).pages[0]
    words = p.extract_words(keep_blank_chars=True, x_tolerance=2)
    head = next((w for w in words if w['text'].startswith('Características')), None)
    if head is None:
        raise ValueError(f"{ruta}: no encuentro el título 'Características técnicas' (¿otra plantilla o PDF escaneado?)")
    zona = [w for w in words if w['top'] > head['bottom'] + 2 and w['x1'] <= X_TABLA_MAX]

    def lineas(ws):
        out = []
        for w in sorted(ws, key=lambda w: (round(w['top']), w['x0'])):
            if out and abs(out[-1]['top'] - w['top']) < 3:
                out[-1]['text'] += ' ' + w['text']; out[-1]['bottom'] = max(out[-1]['bottom'], w['bottom'])
            else:
                out.append(dict(text=w['text'], top=w['top'], bottom=w['bottom']))
        return out

    filas = [{'etiqueta': e['text'].strip().rstrip(':').strip(), 'valor': [], 'y': (e['top'] + e['bottom']) / 2}
             for e in lineas([w for w in zona if w['x0'] < X_CORTE])]
    for v in lineas([w for w in zona if w['x0'] >= X_CORTE]):
        yc = (v['top'] + v['bottom']) / 2
        min(filas, key=lambda f: abs(f['y'] - yc))['valor'].append(v['text'].strip())
    return [{'etiqueta': f['etiqueta'], 'valor': re.sub(r'-\s+', '- ', ' '.join(f['valor']))} for f in filas]

if __name__ == '__main__':
    print(json.dumps(extraer_tabla(sys.argv[1]), ensure_ascii=False, indent=2))
