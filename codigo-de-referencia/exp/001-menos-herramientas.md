# Experimento 001 — menos herramientas

## Hipótesis
Si quito 2 de las 5 herramientas, baja el tiempo medio por corrida porque el
agente duda menos entre opciones parecidas.

## Regla de decisión (escrita ANTES de correr nada)
Se acepta si se cumplen las tres:
1. Las corridas que pasan la puerta son iguales o más que en la línea base.
2. El tiempo medio baja 15 % o más.
3. Ninguna tarea que pasaba siempre empieza a fallar.

## Línea base
- Etiqueta: `baseline-v0`      Archivo: `evals/base.csv`
- Resultado: (pegá la salida de `./evals/resumen.sh evals/base.csv`)

## Variante (un solo cambio, reversible)
- Se quitan: `herramienta-buscar`, `herramienta-web`
- Rama: `exp/001`

## Resultado
- Archivo: `evals/exp-001.csv`
- Veredicto del script: (pegá la salida de `./evals/comparar.sh evals/base.csv evals/exp-001.csv`)

## Decisión
ACEPTADA / RECHAZADA (la dice el script, no la impresión)

## Lección (con evidencia)
Una frase que otro equipo pueda reutilizar, con el nombre del archivo que la prueba.
