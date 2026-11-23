"""
Junta los diccionarios de data/*.json en un JS por idioma: js/i18n-datos-en.js y
js/i18n-datos-ar.js.

La web los carga con <script> y no con fetch() porque fetch() falla al abrir las
páginas con doble clic (file://): las descripciones se quedaban en español aunque
tuvieran traducción. Los JSON siguen siendo el original que se edita; después de
tocarlos hay que volver a ejecutar esto (preparar_publicacion.py ya lo hace).

Uso:  python3 scripts/empaquetar_traducciones.py
"""
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# En cada grupo, los posteriores pisan a los anteriores: primero la traducción
# automática y encima las correcciones a mano.
GRUPOS = {
    'textos': ['catalogo-traducciones-{l}.json', 'productos-traducciones-{l}.json',
               'catalogo-secciones-{l}-overrides.json', 'productos-{l}-overrides.json',
               'catalogo-secciones-{l}-quality-overrides.json', 'productos-{l}-quality-overrides.json'],
    'resumenes': ['catalogo-resumenes-{l}.json'],
    'etiquetas': ['tablas-traducciones-{l}-labels.json'],
    'valores': ['tablas-traducciones-{l}-values.json'],
}


def empaquetar(idioma):
    datos = {}
    for grupo, archivos in GRUPOS.items():
        mapa = {}
        for plantilla in archivos:
            ruta = os.path.join(RAIZ, 'data', plantilla.format(l=idioma))
            if os.path.exists(ruta):
                with open(ruta, encoding='utf-8') as f:
                    mapa.update(json.load(f))
        datos[grupo] = mapa
    salida = os.path.join(RAIZ, 'js', f'i18n-datos-{idioma}.js')
    with open(salida, 'w', encoding='utf-8') as f:
        f.write('/* Generado por scripts/empaquetar_traducciones.py — no editar a mano.\n'
                '   Los textos se cambian en data/*.json. */\n')
        f.write('window.APHE_I18N_DATOS = ')
        json.dump(datos, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')
    return salida, {g: len(m) for g, m in datos.items()}


def main():
    for idioma in ('en', 'ar'):
        salida, cuentas = empaquetar(idioma)
        print(f'  ✓ {os.path.relpath(salida, RAIZ)}: ' +
              ', '.join(f'{n} {g}' for g, n in cuentas.items()))


if __name__ == '__main__':
    main()
