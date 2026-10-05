"""
Junta las carátulas de sección en un solo PDF: el catálogo general.

Las carátulas son los Word de fuentes/fichas/CARATULAS/, uno por sección, con su texto
descriptivo y sus fotos. Se convierten a PDF con LibreOffice y se encadenan en el mismo
orden en el que salen las secciones en la web.

Salida: docs/catalogo/catalogo-apheloria.pdf (piloto, todavía no se publica).

Uso:  python scripts/catalogo/construir_catalogo.py
"""
import os, shutil, subprocess, tempfile

import fitz

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORIGEN = os.path.join(RAIZ, 'fuentes', 'fichas', 'CARATULAS')
SALIDA = os.path.join(RAIZ, 'docs', 'catalogo', 'catalogo-apheloria.pdf')
SOFFICE = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

# Las grandes familias van en el orden en el que salen en Productos; dentro de cada una se
# respeta la numeración de los propios documentos. Cada entrada: (archivo, título del marcador).
# "CARATULAS ILUMINACIÓN.docx" no entra: es una recopilación antigua de cuatro de estas
# mismas páginas, idéntica a sus versiones sueltas.
ORDEN = [
    ('1 Equipos LED de Iluminación para Interiores',              'Interiores'),
    ('1.1 interiores - Equipos LED de superficie',                'Interiores · De superficie'),
    ('1.1.1 PROYECTORES',                                         'Interiores · Proyectores de carril'),
    ('1.2 interiores - Equipos LED para empotrar',                'Interiores · Para empotrar'),
    ('2 Equipos LED de Iluminación para Exteriores',              'Exteriores'),
    ('2.1 Exteriores - Equipos LED para empotrar (Techo – pared – piso)',
                                                                  'Exteriores · Para empotrar'),
    ('3 Equipos LED de Iluminación Decorativa',                   'Decorativas'),
    ('4 Equipos LED de Iluminación para Industriales',            'Industriales'),
    ('5 Equipos LED de Iluminación Hospitalaria',                 'Hospitalarias · Salas blancas'),
    ('6 Equipos LED de Iluminación de Emergencia',                'Emergencia'),
]

ORO = (0.69, 0.66, 0.60)
TINTA = (0.10, 0.086, 0.07)


def portada(doc, ancho, alto):
    """Una portada sobria: el logo, el título y el pie de la empresa."""
    pagina = doc.new_page(0, width=ancho, height=alto)
    icono = os.path.join(RAIZ, 'logo-icon.png')
    if os.path.exists(icono):
        lado = ancho * 0.17
        pagina.insert_image(fitz.Rect((ancho - lado) / 2, alto * 0.26,
                                      (ancho + lado) / 2, alto * 0.26 + lado), filename=icono)
    def centrado(texto, y, tam, color, fuente='helv', espaciado=0):
        if espaciado:
            texto = (' ' * espaciado).join(texto)
        w = fitz.get_text_length(texto, fontname=fuente, fontsize=tam)
        pagina.insert_text(((ancho - w) / 2, y), texto, fontname=fuente, fontsize=tam, color=color)
    centrado('APHELORIA SOLUTIONS', alto * 0.49, 15, TINTA, espaciado=1)
    centrado('Catálogo General', alto * 0.565, 27, TINTA)
    centrado('Iluminación técnica y material eléctrico', alto * 0.60, 10.5, ORO)
    centrado('Av. Emilio Arrieta, 8 · Puerta 36 · 28706 San Sebastián de los Reyes, Madrid',
             alto * 0.90, 7.5, ORO)
    centrado('comercial@apheloria.es · +34 607 591 975', alto * 0.915, 7.5, ORO)
    pagina.draw_line(fitz.Point(ancho * 0.38, alto * 0.525), fitz.Point(ancho * 0.62, alto * 0.525),
                     color=ORO, width=0.6)


def main():
    temporal = tempfile.mkdtemp(prefix='apheloria-catalogo-')
    pendientes = []
    for archivo, _ in ORDEN:
        ruta = os.path.join(ORIGEN, archivo + '.docx')
        if not os.path.exists(ruta):
            print(f'  FALTA: {archivo}.docx')
            continue
        destino = os.path.join(temporal, archivo + '.docx')
        shutil.copy(ruta, destino)
        pendientes.append(destino)

    subprocess.run([SOFFICE, '--headless', '--norestore',
                    f'-env:UserInstallation=file://{temporal}/perfil',
                    '--convert-to', 'pdf', '--outdir', temporal] + pendientes,
                   check=True, capture_output=True, timeout=900)

    catalogo = fitz.open()
    indice, hechas = [], []
    for archivo, titulo in ORDEN:
        pdf = os.path.join(temporal, archivo + '.pdf')
        if not os.path.exists(pdf):
            continue
        with fitz.open(pdf) as d:
            indice.append([1, titulo, len(catalogo) + 2])   # +2: la portada va delante
            catalogo.insert_pdf(d)
            hechas.append((titulo, len(d)))

    primera = catalogo[0].rect
    portada(catalogo, primera.width, primera.height)
    catalogo.set_toc(indice)
    catalogo.set_metadata({'title': 'Apheloria Solutions — Catálogo General',
                           'author': 'Apheloria Solutions, S.L.',
                           'subject': 'Iluminación técnica y material eléctrico'})
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    catalogo.save(SALIDA, garbage=4, deflate=True)
    catalogo.close()
    shutil.rmtree(temporal, ignore_errors=True)

    doc = fitz.open(SALIDA)
    print(f'{SALIDA}')
    print(f'  {len(doc)} páginas · {os.path.getsize(SALIDA) / 1048576:.1f} MB')
    for titulo, n in hechas:
        print(f'    {titulo:40} {n} pág')
    doc.close()


if __name__ == '__main__':
    main()
