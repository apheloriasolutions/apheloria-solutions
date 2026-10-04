"""
Prepara lo que necesita la web a partir de data/catalogo.json y data/textos.json:

  js/catalogo-web.js   el árbol con lo justo para pintar Productos (window.CATALOGO)
  data/textos.json     los textos de cabecera; se crea la primera vez y después
                       solo se le añaden las secciones nuevas, nunca se pisa lo escrito

Las rutas de las fichas (carpetas de fuentes/) no se publican.

Uso:  python scripts/catalogo/construir_web.py
"""
import json, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
TEXTOS = os.path.join(RAIZ, 'data', 'textos.json')
SALIDA = os.path.join(RAIZ, 'js', 'catalogo-web.js')

POTENCIA = re.compile(r'^Potencia\b', re.I)
TEMPERATURA = re.compile(r'^Temperatura de color', re.I)


def valor(tabla, patron):
    for etiqueta, v in tabla:
        if patron.match(etiqueta):
            return v
    return ''


def resumen(prod):
    """Los dos o tres datos que se ven en la tarjeta: '20W - 30W · 3000K · 2 versiones'."""
    partes = [p for p in (valor(prod['tabla'], POTENCIA), valor(prod['tabla'], TEMPERATURA)) if p]
    n = len(prod['codigos'])
    if n > 1:
        partes.append(f'{n} versiones')
    return ' · '.join(partes)


def etiquetas_de_ficha(boton):
    """Para los botones de descarga: lo que distingue a cada ficha del grupo.
    Si entre ellas cambian los vatios y los grados, la etiqueta es "20W 3000K"."""
    por_codigo = boton.get('tabla_por_codigo') or {}
    codigos = [c for c in boton['codigos'] if c in boton.get('pdf', {})]
    if len(codigos) < 2:
        return {c: '' for c in codigos}

    filas = {c: dict(f for f in por_codigo.get(c, {}).get('filas', [])) for c in codigos}
    etiquetas = []
    for et in dict.fromkeys(e for c in codigos for e in filas[c]):
        valores = {filas[c].get(et, '') for c in codigos}
        if len(valores) > 1:
            etiquetas.append(et)
    # primero potencia y temperatura, que es lo que de verdad distingue una ficha de otra
    orden = sorted(etiquetas, key=lambda e: (0 if POTENCIA.match(e) else 1 if TEMPERATURA.match(e) else 2))
    salida = {}
    for c in codigos:
        trozos = [filas[c].get(e, '') for e in orden[:2]]
        salida[c] = ' '.join(t for t in trozos if t).strip()
    if len(set(salida.values())) < len(codigos):      # no las distingue: mejor el código
        return {c: c for c in codigos}
    return salida


def foto(d, tipo):
    f = (d or {}).get(tipo)
    return {'ruta': f['ruta'], 'px': f['px']} if f else None


def primera_foto(nodo, tipo):
    """La primera foto de ese tipo que se encuentre bajando por la sección."""
    for b in nodo['botones']:
        f = foto(b.get('fotos'), tipo)
        if f:
            return f
    for h in nodo['hijos']:
        f = primera_foto(h, tipo)
        if f:
            return f
    return None


def cuenta_productos(nodo):
    return len(nodo['botones']) + sum(cuenta_productos(h) for h in nodo['hijos'])


def sin_repetir(slug, usados):
    """Dos fichas cuyo nombre solo cambia en una tilde o una mayúscula dan el mismo slug
    ("Plafón LED superficie" y "Plafón Led superficie"): la segunda se quedaría sin
    dirección propia. Se le añade un número."""
    if slug not in usados:
        usados.add(slug)
        return slug
    n = 2
    while f'{slug}-{n}' in usados:
        n += 1
    usados.add(f'{slug}-{n}')
    return f'{slug}-{n}'


def portada_de(nodo, textos, clave):
    """Por defecto, la foto de producto del primero que haya dentro. Si en textos.json se le
    ha puesto una `portada` a mano (las grandes familias llevan fotos de banco), manda esa."""
    a_mano = (textos.get(clave) or {}).get('portada')
    if a_mano and os.path.exists(os.path.join(RAIZ, a_mano)):
        from PIL import Image
        with Image.open(os.path.join(RAIZ, a_mano)) as im:
            return {'ruta': a_mano, 'px': list(im.size), 'ambiente': True}
    return primera_foto(nodo, 'luminaria')


def convertir(nodo, textos, ruta=()):
    clave = '/'.join(ruta)
    usados = {h['slug'] for h in nodo['hijos']}
    productos = []
    for b in nodo['botones']:
        etiquetas = etiquetas_de_ficha(b)
        productos.append({
            'nombre': b['nombre'],
            'slug': sin_repetir(b['slug'], usados),
            'codigos': b['codigos'],
            'resumen': resumen(b),
            'tabla': b.get('tabla', []),
            'notas': b.get('notas', []),
            'descripcion': b.get('descripcion', []),
            'fotos': {t: foto(b.get('fotos'), t) for t in ('luminaria', 'medidas', 'ambiente', 'angulo')},
            'fichas': [{'codigo': c, 'pdf': r, 'etiqueta': etiquetas.get(c, '')}
                       for c, r in (b.get('pdf') or {}).items()],
        })
    hijos = [convertir(h, textos, ruta + (h['slug'],)) for h in nodo['hijos']]
    return {
        'nombre': nodo['nombre'],
        'slug': nodo['slug'],
        'texto': (textos.get(clave) or {}).get('texto', ''),
        'hero': primera_foto(nodo, 'ambiente'),
        'portada': portada_de(nodo, textos, clave),
        'cuenta': cuenta_productos(nodo),
        'hijos': hijos,
        'productos': productos,
    }


def rutas(nodo, ruta=()):
    """Todas las pantallas de navegación: la raíz y cada sección."""
    yield '/'.join(ruta), nodo
    for h in nodo['hijos']:
        yield from rutas(h, ruta + (h['slug'],))


def main():
    cat = json.load(open(DATOS, encoding='utf-8'))
    textos = json.load(open(TEXTOS, encoding='utf-8')) if os.path.exists(TEXTOS) else {}

    nuevas = 0
    for clave, nodo in rutas(cat['arbol']):
        if clave not in textos:
            textos[clave] = {'texto': '', 'borrador': True}
            nuevas += 1
    json.dump(textos, open(TEXTOS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    arbol = convertir(cat['arbol'], textos)
    arbol['nombre'] = 'Productos'
    js = ('/* Generado por scripts/catalogo/construir_web.py — no editar a mano.\n'
          '   Los textos de cabecera se cambian en data/textos.json. */\n'
          'window.CATALOGO = ' + json.dumps(arbol, ensure_ascii=False, separators=(',', ':')) + ';\n')
    open(SALIDA, 'w', encoding='utf-8').write(js)

    total = sum(1 for _ in rutas(cat['arbol']))
    print(f'{SALIDA}: {len(js) / 1024:.0f} KB · {total} pantallas · {arbol["cuenta"]} productos')
    print(f'{TEXTOS}: {len(textos)} secciones ({nuevas} nuevas)')
    sin = [k for k, v in textos.items() if not v.get('texto')]
    print(f'secciones sin texto: {len(sin)}')


if __name__ == '__main__':
    main()
