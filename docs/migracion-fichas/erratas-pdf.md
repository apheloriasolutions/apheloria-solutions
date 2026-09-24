# Erratas detectadas en los PDF de fichas técnicas

Lo que aparece aquí **no se corrige** al generar `data/productos.json`: la web publica el valor tal
cual viene del PDF. Esta lista es para que el proveedor/cliente corrija el PDF de origen; cuando se
corrija el PDF, la ficha de la web se actualiza sola al volver a extraer.

Detectadas al validar la muestra (EXIT S, ZEN, plafón IP65) y al generar las fichas de
**industrial e interior** — 2026-09-24.

## Unidad equivocada en "Lúmenes reales" (dice `lm/W`, debería decir `lm`)

Afecta a 14 fichas. El valor es correcto, lo que está mal es la unidad; se publica tal cual.

| Refs | Dice |
|---|---|
| 00DLZEN25W27X / 30X / 40X | `2500 lm/W` |
| 00DLZEN30W27X / 30X / 40X | `2980 lm/W` |
| 00DLZEN40W27X / 30X / 40X | `3800 lm/W` |
| 00DLZEN50W27X / 30X / 40X | `4650 lm/W` |
| 0DLROM10W3CCT | `1000 lm/W` |
| 0DLROM20W3CCT | `2000 lm/W` |

Además, en la misma gama ZEN: `00DLZEN20W27X` pone los lúmenes **sin unidad** (`2150`), y la fila
"Lm / W reales" trae `95lm/W` (sin espacio) en los de 40W y `116.25 m/W` (sin la "l") en los de 50W.

## Fichas sin potencia

| Ref | Fila | Dice |
|---|---|---|
| 00FAROLVILLAN | Potencia total luminaria | *(vacío)* |

## Texto mal escrito

| Ficha (ref) | Fila | Dice | Debería decir |
|---|---|---|---|
| 00EMEEXITS150, 00EMGEXITS200, 00EMEEXITS250, 00EMEEXITS350, 00EMEEXITS450 | Garantía | `2 ños` | `2 años` |
| 00EMGEXITS200, 00EMEEXITS250, 00EMEEXITS350, 00EMEEXITS450 | Temperatura de trabajo | `0o - 40oC` (letra "o" en vez del símbolo de grado) | `0º - 40ºC` |
| 00PLAFIP6512W | *(etiqueta)* | `Temperatura de color correlacionada (CC` — la etiqueta está cortada en el propio PDF | `Temperatura de color correlacionada (CCT):` |

## Valores que faltan

| Ficha (ref) | Fila | Dice | Observación |
|---|---|---|---|
| 00EMGEXITS200, 00EMEEXITS250, 00EMEEXITS350, 00EMEEXITS450 | Potencia total luminaria | `W` (sin número) | El de 150 lm sí trae `1W`. Sin el número, la fila sale vacía de contenido útil |
| 00PLAFIP6512W | Driver | *(vacío)* | La fila existe en la tabla pero no tiene valor |
| 00PLAFIP6512W | Protocolo de regulación | *(vacío)* | Ídem |
| 00PLAFIP6512W | Luminaria fácilmente reciclable | *(vacío)* | Parece una fila de "sello"/icono más que un dato |

## Contradicciones entre el PDF y la descripción del Excel

| Ref | El PDF dice | El Excel dice | Nota |
|---|---|---|---|
| 00EMEEXITS250, 00EMEEXITS350 | Acabado difusor: `Transparente` | `...difusor opal` | Los otros tres de la misma gama (150, 200, 450) sí ponen `opal`/`Opal` en el PDF. Hay que decidir cuál es el bueno: la web publicará lo que diga el PDF |
