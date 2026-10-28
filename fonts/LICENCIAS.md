# Tipografías del sitio

Las cuatro familias que usa Apheloria están alojadas en este mismo servidor, en `fonts/`,
y se declaran en [`css/tipografias.css`](../css/tipografias.css).

| Familia | Pesos | Licencia | Origen |
|---|---|---|---|
| Montserrat | 100, 200 | SIL Open Font License 1.1 | https://fonts.google.com/specimen/Montserrat |
| Raleway | 300, 400, 600, 800 + cursiva 400 | SIL Open Font License 1.1 | https://fonts.google.com/specimen/Raleway |
| Inter | 200, 300, 400 | SIL Open Font License 1.1 | https://fonts.google.com/specimen/Inter |
| Cormorant Garamond | 300 + cursiva 400 | SIL Open Font License 1.1 | https://fonts.google.com/specimen/Cormorant+Garamond |

La OFL permite usarlas, modificarlas y redistribuirlas, también en un sitio comercial. La
única condición que nos afecta es no venderlas por separado y no usar los nombres reservados
de las fuentes para una versión modificada. Recortar el juego de caracteres, que es lo que se
ha hecho aquí, está expresamente permitido.

Texto completo de la licencia: https://openfontlicense.org

## Cómo se generaron

Descargadas de Google Fonts en TTF, recortadas al alfabeto latino más los signos que usa el
sitio y convertidas a WOFF2 con `fontTools.subset`. De 2.550 KB a 246 KB en total.
