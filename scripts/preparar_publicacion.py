"""
Monta la carpeta _publicar/ con EXACTAMENTE lo que va al hosting, y nada más.

La idea es no tener que elegir a mano qué se sube: se ejecuta esto y lo que quede dentro
de _publicar/ es lo que se arrastra al FTP. Después comprueba que todo lo que la web pide
—las 9 páginas, el CSS, el JS, las tipografías, las 783 imágenes y las 397 fichas— está
dentro y se llama exactamente igual, porque el servidor de IONOS es Linux y distingue
mayúsculas y acentos donde macOS no.

Uso:  python3 scripts/preparar_publicacion.py
"""
import html
import json
import os
import re
import shutil
import sys
import unicodedata
import urllib.parse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, '_publicar')

# ── qué se sube ───────────────────────────────────────────────────────────────
PAGINAS = ['index.html', 'proyectos.html', 'productos.html', 'catalogo.html', 'contacto.html',
           'aviso-legal.html', 'politica-privacidad.html', 'politica-cookies.html', '404.html']
CONFIGURACION = ['.htaccess', 'robots.txt', 'sitemap.xml']
ICONOS = ['favicon.png', 'apple-touch-icon.png', 'logo.png', 'logo-icon.png',
          'og-apheloria.jpg']   # la vista previa al compartir en redes
CARPETAS = ['css', 'js', 'images', 'fonts']

# ── qué no se sube aunque esté dentro de una carpeta que sí ───────────────────
NUNCA = re.compile(r'(^|/)\.|\.(md|xlsx|xls|docx|zip|rar|py|log|bak|sql)$', re.I)
# fichas/resumidas/ es un paso intermedio del catálogo en PDF: 19 MB que la web no enlaza
FICHAS_FUERA = {'resumidas'}


def rutas_que_pide_la_web():
    """Todo lo que el sitio enlaza: páginas, hojas, imágenes y PDF."""
    pedidas = set()
    for p in PAGINAS:
        s = open(os.path.join(RAIZ, p), encoding='utf-8').read()
        for _, v in re.findall(r'(href|src|data-foto)="([^"]+)"', s):
            pedidas.add(html.unescape(v))
        for v in re.findall(r'<meta property="og:image" content="([^"]+)"', s):
            pedidas.add(html.unescape(v))
        pedidas |= {html.unescape(u) for u in re.findall(r"url\('([^']+)'\)", s)}
    for carpeta, patron in (('css', r"url\(['\"]?([^'\")]+)['\"]?\)"),):
        for f in os.listdir(os.path.join(RAIZ, carpeta)):
            s = open(os.path.join(RAIZ, carpeta, f), encoding='utf-8').read()
            for u in re.findall(patron, s):
                pedidas.add(os.path.normpath(os.path.join(carpeta, u)))
    # el catálogo de productos va en un JSON dentro del JS
    s = open(os.path.join(RAIZ, 'js', 'catalogo-web.js'), encoding='utf-8').read()
    datos = json.loads(s[s.index('=', s.index('window.CATALOGO')) + 1: s.rindex(';')])

    def recorrer(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'ruta' and isinstance(v, str):
                    pedidas.add(v)
                elif k == 'fichas' and isinstance(v, list):
                    for f in v:
                        pedidas.add(f['pdf'])
                else:
                    recorrer(v)
        elif isinstance(o, list):
            for v in o:
                recorrer(v)
    recorrer(datos)
    for f in os.listdir(os.path.join(RAIZ, 'js')):
        s = open(os.path.join(RAIZ, 'js', f), encoding='utf-8').read()
        pedidas |= set(re.findall(r'"((?:images|fichas|fonts)/[^"]+)"', s))

    limpias = set()
    for r in pedidas:
        r = urllib.parse.unquote(r.split('#')[0].split('?')[0])
        # las etiquetas og: llevan la URL entera: se comprueban igual que las demás
        for dominio in ('https://apheloria.es/', 'https://www.apheloria.es/'):
            if r.startswith(dominio):
                r = r[len(dominio):] or 'index.html'
        if r and not r.startswith(('http', 'mailto:', 'tel:', 'javascript:', 'data:')):
            limpias.add(r)
    return limpias


def copiar(pedidas):
    """pedidas: lo que la web enlaza de verdad. De images/ y fichas/ solo se copia eso,
    así no viajan al hosting las fotos de productos que dejaron de publicarse."""
    if os.path.isdir(SALIDA):
        shutil.rmtree(SALIDA)
    os.makedirs(SALIDA)
    copiados, saltados = [], []

    def copia(rel):
        destino = os.path.join(SALIDA, rel)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(os.path.join(RAIZ, rel), destino)
        copiados.append(rel)

    for f in PAGINAS + CONFIGURACION + ICONOS:
        copia(f)
    for carpeta in CARPETAS:
        for raiz, _, archivos in os.walk(os.path.join(RAIZ, carpeta)):
            for a in archivos:
                rel = os.path.relpath(os.path.join(raiz, a), RAIZ)
                if NUNCA.search(rel):
                    saltados.append(rel)
                    continue
                if carpeta == 'images' and rel not in pedidas:
                    saltados.append(rel)
                    continue
                copia(rel)
    # las fichas, solo los PDF sueltos
    for a in sorted(os.listdir(os.path.join(RAIZ, 'fichas'))):
        rel = os.path.join('fichas', a)
        if a in FICHAS_FUERA or not a.lower().endswith('.pdf') or rel not in pedidas:
            saltados.append(rel)
            continue
        copia(rel)
    return copiados, saltados


def comprobar(copiados):
    """Que esté todo lo que la web pide, con la grafía exacta (Linux distingue)."""
    dentro = set()
    for raiz, _, archivos in os.walk(SALIDA):
        for a in archivos:
            dentro.add(os.path.relpath(os.path.join(raiz, a), SALIDA))
    faltan = [r for r in rutas_que_pide_la_web() if r not in dentro]
    # y que ningún nombre venga con los acentos descompuestos (macOS lo hace a veces)
    nfd = [r for r in dentro if unicodedata.normalize('NFC', r) != r]
    sobran = sorted(dentro - rutas_que_pide_la_web() - set(PAGINAS) - set(CONFIGURACION) - set(ICONOS))
    return sorted(faltan), nfd, sobran


if __name__ == '__main__':
    copiados, saltados = copiar(rutas_que_pide_la_web())
    faltan, nfd, sobran = comprobar(copiados)
    peso = sum(os.path.getsize(os.path.join(SALIDA, f))
               for raiz, _, fs in os.walk(SALIDA)
               for f in [os.path.relpath(os.path.join(raiz, x), SALIDA) for x in fs])
    print(f'{SALIDA}')
    print(f'  {len(copiados)} archivos · {peso / 1024 / 1024:.1f} MB')
    print(f'  no se copian: {len(saltados)} (documentación, temporales y fichas/resumidas)')
    print()
    if faltan:
        print(f'  ¡OJO! la web pide {len(faltan)} archivos que no están dentro:')
        for f in faltan[:20]:
            print('     ', f)
        sys.exit(1)
    print('  ✓ todo lo que la web pide está dentro y se llama exactamente igual')
    if nfd:
        print(f'  ¡OJO! {len(nfd)} nombres con los acentos descompuestos: {nfd[:3]}')
        sys.exit(1)
    print('  ✓ ningún nombre con los acentos descompuestos')
    if sobran:
        print(f'  · {len(sobran)} archivos que se suben sin que nadie los enlace')
        for f in sobran[:10]:
            print('     ', f)
    else:
        print('  ✓ no se sube ni un archivo que la web no use')
    print()
    print('  Ya se puede arrastrar el CONTENIDO de _publicar/ a la raíz del hosting.')
    print('  El .htaccess, el último.')
