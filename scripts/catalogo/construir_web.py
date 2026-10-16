"""
Prepara lo que necesita la web a partir de data/catalogo.json y data/textos.json:

  js/catalogo-web.js   el árbol con lo justo para pintar Productos (window.CATALOGO)
  data/textos.json     los textos de cabecera; se crea la primera vez y después
                       solo se le añaden las secciones nuevas, nunca se pisa lo escrito

Las rutas de las fichas (carpetas de fuentes/) no se publican.

Uso:  python scripts/catalogo/construir_web.py
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from construir_estructura import de_superficie

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS = os.path.join(RAIZ, 'data', 'catalogo.json')
TEXTOS = os.path.join(RAIZ, 'data', 'textos.json')
MEDIDAS = os.path.join(RAIZ, 'data', 'medidas.json')
SALIDA = os.path.join(RAIZ, 'js', 'catalogo-web.js')

LAS_MEDIDAS = {}
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


def medidas_de(boton, medidas):
    """Un producto puede venir en varias medidas, cada una con su dibujo acotado. La medida
    en texto no está en ninguna celda del Excel: se ha leído del propio dibujo y vive en
    data/medidas.json, que se edita a mano."""
    por_codigo = boton.get('fotos_por_codigo') or {}
    vistas = {}
    for c in boton['codigos']:
        m = (por_codigo.get(c) or {}).get('medidas')
        if not m:
            continue
        v = vistas.setdefault(m['ruta'], {'texto': '', 'foto': {'ruta': m['ruta'], 'px': m['px']},
                                          'codigos': []})
        v['codigos'].append(c)
        if not v['texto'] and medidas.get(c):
            v['texto'] = medidas[c]
    return list(vistas.values())


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


def hero_de(nodo, textos, clave):
    """Por defecto, la foto de ambiente del primer producto de la sección. Si en textos.json
    se le ha puesto un `hero` a mano, manda ese: las de banco llenan el hueco y las de
    producto se dejan centradas sobre blanco."""
    a_mano = (textos.get(clave) or {}).get('hero')
    if a_mano and os.path.exists(os.path.join(RAIZ, a_mano)):
        from PIL import Image
        with Image.open(os.path.join(RAIZ, a_mano)) as im:
            # una fotografía llena el hueco; una foto de producto va centrada sobre blanco
            es_foto = '/portadas/' in a_mano or a_mano.endswith('/ambiente.jpg')
            return {'ruta': a_mano, 'px': list(im.size), 'ambiente': es_foto}
    f = primera_foto(nodo, 'ambiente')
    if f:
        f = dict(f, ambiente=True)
    return f


# Marcas de los fabricantes de driver. No son nuestras y la norma es que las referencias de
# proveedor no se publican nunca, así que la fila "Driver" se cae cuando su valor es solo una
# marca. Los valores que sí dicen algo al cliente ("Integrado", "Externo", "No incluido") se
# quedan. LIFUD se mantiene a propósito: es el único que el cliente ha querido publicar.
MARCAS_DRIVER = ('vossloh', 'tci', 'tridonic', 'philips', 'boke')
MARCAS_QUITADAS = []

# Productos cuya descripción se queda duplicada porque las dos fichas solo se diferencian en
# una palabra, y esa palabra es un dato que no se puede perder. Se indica cuál se publica.
DESCRIPCION_ELEGIDA = {
    # las dos versiones del CJV 625 son ON-OFF y DALI; la que lo dice es la buena, porque
    # la tabla ya recoge los dos protocolos
    '00PANSP544K': 1,
}


def sin_marcas_de_proveedor(tabla, avisos):
    """Quita de la tabla las filas de driver cuyo valor es solo una marca de fabricante."""
    limpia = []
    for etiqueta, valor in tabla:
        if 'driver' in etiqueta.lower():
            desnudo = re.sub(r'[^a-z]', ' ', valor.lower())
            palabras = set(desnudo.split())
            marcas = [m for m in MARCAS_DRIVER if m in palabras]
            # solo se tira si la marca es TODO lo que dice la fila
            resto = palabras - set(MARCAS_DRIVER) - {'led', 'reemplazable', 'reenplazable'}
            if marcas and not resto:
                avisos.append(f'{etiqueta}: {valor}')
                continue
        limpia.append([etiqueta, valor])
    return limpia


def descripcion_de(boton):
    """Una sola descripción cuando el origen trae dos casi iguales. Y, como en los nombres,
    "adosado" pasa a "de superficie": es la palabra que se usa aquí."""
    desc = [de_superficie(d) for d in boton.get('descripcion', [])]
    for codigo, i in DESCRIPCION_ELEGIDA.items():
        if codigo in boton['codigos'] and len(desc) > i:
            return [desc[i]]
    return desc


def convertir(nodo, textos, ruta=()):
    clave = '/'.join(ruta)
    usados = {h['slug'] for h in nodo['hijos']}
    productos = []
    for b in nodo['botones']:
        etiquetas = etiquetas_de_ficha(b)
        medidas = medidas_de(b, LAS_MEDIDAS)
        tabla = sin_marcas_de_proveedor(list(b.get('tabla', [])), MARCAS_QUITADAS)
        textos_medida = [m['texto'] for m in medidas if m['texto']]
        if textos_medida and not any(e.lower().startswith(('medida', 'dimensi')) for e, _ in tabla):
            # cada medida ya lleva " · " dentro, así que entre medidas se usa " / " y la
            # web las pinta una por línea
            tabla.append(['Medida', ' / '.join(dict.fromkeys(textos_medida))])
        productos.append({
            'nombre': b['nombre'],
            'slug': sin_repetir(b['slug'], usados),
            'codigos': b['codigos'],
            'resumen': resumen(b),
            'tabla': tabla,
            'medidas': medidas,
            'notas': b.get('notas', []),
            'descripcion': descripcion_de(b),
            'fotos': {t: foto(b.get('fotos'), t) for t in ('luminaria', 'medidas', 'ambiente', 'angulo')},
            'fichas': [{'codigo': c, 'pdf': r, 'etiqueta': etiquetas.get(c, '')}
                       for c, r in (b.get('pdf') or {}).items()],
        })
    hijos = [convertir(h, textos, ruta + (h['slug'],)) for h in nodo['hijos']]
    return {
        'nombre': nodo['nombre'],
        'slug': nodo['slug'],
        'texto': (textos.get(clave) or {}).get('texto', ''),
        'hero': hero_de(nodo, textos, clave),
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
    global LAS_MEDIDAS
    LAS_MEDIDAS = json.load(open(MEDIDAS, encoding='utf-8')) if os.path.exists(MEDIDAS) else {}

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
    if MARCAS_QUITADAS:
        from collections import Counter
        print(f'filas de driver retiradas por llevar marca de proveedor: {len(MARCAS_QUITADAS)}')
        for v, n in Counter(MARCAS_QUITADAS).most_common():
            print(f'   {v}  ({n})')


if __name__ == '__main__':
    main()
