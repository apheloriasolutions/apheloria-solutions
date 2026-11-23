"""
Compara _publicar/ con lo que hay ahora mismo en https://apheloria.es y dice qué
archivos hay que subir por FTP: los que faltan y los que han cambiado.

Así no hay que volver a subir los 133 MB enteros por cada cambio. Se ejecuta después
de preparar_publicacion.py:

    python3 scripts/preparar_publicacion.py
    python3 scripts/comprobar_publicado.py

Las fichas PDF (fichas/) no se comparan una a una porque son 96 MB: se avisa solo
de las que faltan. El .htaccess tampoco, porque el servidor no deja descargarlo.
"""
import concurrent.futures
import os
import urllib.error
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, '_publicar')
WEB = 'https://apheloria.es/'


def estado(rel):
    url = WEB + urllib.parse.quote(rel)
    fichas = rel.startswith('fichas/')
    peticion = urllib.request.Request(url, method='HEAD' if fichas else 'GET',
                                      headers={'User-Agent': 'Mozilla/5.0',
                                               'Accept-Encoding': 'identity'})
    try:
        with urllib.request.urlopen(peticion, timeout=30) as r:
            if fichas:
                return 'igual'
            with open(os.path.join(SALIDA, rel), 'rb') as f:
                return 'igual' if r.read() == f.read() else 'cambiado'
    except urllib.error.HTTPError:
        return 'falta'
    except Exception as e:
        return f'error ({e})'


def main():
    archivos = sorted(
        os.path.relpath(os.path.join(raiz, a), SALIDA)
        for raiz, _, nombres in os.walk(SALIDA) for a in nombres
        if a != '.htaccess')
    with concurrent.futures.ThreadPoolExecutor(12) as hilos:
        estados = dict(zip(archivos, hilos.map(estado, archivos)))

    subir = [a for a in archivos if estados[a] != 'igual']
    print(f'{WEB}: {len(archivos) - len(subir)} archivos al día, {len(subir)} por subir\n')
    for a in subir:
        print(f'  {estados[a]:9} {a}')
    if subir:
        print('\nSúbelos desde _publicar/ a la misma ruta en el hosting.')


if __name__ == '__main__':
    main()
