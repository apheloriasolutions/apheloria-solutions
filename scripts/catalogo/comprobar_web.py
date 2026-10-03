"""
Comprueba que la web de Productos está completa: que cada producto tiene tabla, foto y PDF,
que todos los archivos a los que apunta existen de verdad y que no hay direcciones repetidas.

Uso:  python scripts/catalogo/comprobar_web.py
"""
import json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'js', 'catalogo-web.js')


def cargar():
    texto = open(DATOS, encoding='utf-8').read()
    return json.loads(texto[texto.index('{'):texto.rindex('}') + 1])


def recorrer(nodo, ruta=()):
    yield '/'.join(ruta), nodo, None
    for p in nodo['productos']:
        yield '/'.join(ruta + (p['slug'],)), nodo, p
    for h in nodo['hijos']:
        yield from recorrer(h, ruta + (h['slug'],))


def main():
    cat = cargar()
    todo = list(recorrer(cat))
    pantallas = [(r, n) for r, n, p in todo if p is None]
    productos = [(r, p) for r, _, p in todo if p is not None]

    faltan_archivo, sin_tabla, sin_foto, sin_pdf, sin_texto = [], [], [], [], []
    rutas = {}
    for ruta, _, p in todo:
        rutas.setdefault(ruta, 0)
        rutas[ruta] += 1

    for ruta, nodo in pantallas:
        if not nodo['texto']:
            sin_texto.append(ruta or '(raíz)')
        for f in (nodo['hero'], nodo['portada']):
            if f and not os.path.exists(os.path.join(RAIZ, f['ruta'])):
                faltan_archivo.append((ruta, f['ruta']))

    for ruta, p in productos:
        if not p['tabla']:
            sin_tabla.append((ruta, p['nombre']))
        if not p['fotos'].get('luminaria'):
            sin_foto.append((ruta, p['nombre']))
        if not p['fichas']:
            sin_pdf.append((ruta, p['nombre']))
        for f in p['fotos'].values():
            if f and not os.path.exists(os.path.join(RAIZ, f['ruta'])):
                faltan_archivo.append((ruta, f['ruta']))
        for ficha in p['fichas']:
            if not os.path.exists(os.path.join(RAIZ, ficha['pdf'])):
                faltan_archivo.append((ruta, ficha['pdf']))

    repetidas = [r for r, n in rutas.items() if n > 1]

    print(f'{len(pantallas)} pantallas de navegación · {len(productos)} productos')
    print(f'  sin tabla: {len(sin_tabla)} · sin foto de producto: {len(sin_foto)} · sin PDF: {len(sin_pdf)}')
    print(f'  pantallas sin texto de cabecera: {len(sin_texto)}')
    print(f'  archivos que no existen: {len(faltan_archivo)}')
    print(f'  direcciones repetidas: {len(repetidas)}')
    for titulo, lista in (('SIN TABLA', sin_tabla), ('SIN FOTO', sin_foto), ('SIN PDF', sin_pdf)):
        for ruta, nombre in lista:
            print(f'    {titulo}: {nombre[:52]}  →  #{ruta}')
    for ruta, archivo in faltan_archivo[:20]:
        print(f'    NO EXISTE: {archivo}  (en #{ruta})')
    for r in repetidas:
        print(f'    REPETIDA: #{r}')
    return 1 if faltan_archivo or repetidas else 0


if __name__ == '__main__':
    sys.exit(main())
