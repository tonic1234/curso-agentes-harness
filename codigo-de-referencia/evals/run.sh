#!/bin/bash
# Corre todas las tareas N veces y guarda una fila por corrida.
# Uso: ./evals/run.sh [archivo-de-salida]     (por defecto evals/resultados.csv)
set -euo pipefail
cd "$(dirname "$0")/.."
salida="${1:-evals/resultados.csv}"
corridas="${CORRIDAS:-3}"

echo "tarea,corrida,paso,segundos" > "$salida"
for id in $(jq -r '.[].id' evals/tareas.json); do
  for i in $(seq 1 "$corridas"); do
    ./evals/correr-agente.sh "$id" "$i" >> "$salida"
  done
done
./evals/resumen.sh "$salida"
