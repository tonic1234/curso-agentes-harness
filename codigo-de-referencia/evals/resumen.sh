#!/bin/bash
# KPIs calculados por script (nunca a ojo): tareas que pasan, corridas que pasan, tiempo medio.
f="${1:-evals/resultados.csv}"
awk -F, 'NR>1 {
  corridas++; pasos+=$3; seg+=$4
  total[$1]++; ok[$1]+=$3
}
END {
  for (t in total) { tareas++; if (ok[t]==total[t]) estables++ }
  printf "corridas que pasan: %d de %d (%.0f%%)\n", pasos, corridas, 100*pasos/corridas
  printf "tareas que pasan SIEMPRE: %d de %d\n", estables, tareas
  printf "tiempo medio por corrida: %.1f s\n", seg/corridas
}' "$f"
