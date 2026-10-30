#!/bin/bash
# Aplica la regla de decisión del experimento. Uso: ./evals/comparar.sh base.csv variante.csv
# Regla: pasa >= base  Y  tiempo medio baja >= 15 %  Y  ninguna tarea estable empieza a fallar.
base="$1"; var="$2"
metricas() {
  awk -F, 'NR>1 { c++; p+=$3; s+=$4; t[$1]++; o[$1]+=$3 }
    END { for (k in t) if (o[k]==t[k]) printf "%s ", k > "/dev/stderr";
          printf "%d %.3f\n", p, s/c }' "$1" 2> "$1.estables"
}
read -r pb sb <<< "$(metricas "$base")"
read -r pv sv <<< "$(metricas "$var")"
estables_base=$(tr ' ' '\n' < "$base.estables" | sort | grep . || true)
estables_var=$(tr ' ' '\n' < "$var.estables" | sort | grep . || true)
rm -f "$base.estables" "$var.estables"
perdidas=$(comm -23 <(echo "$estables_base") <(echo "$estables_var") | grep . || true)

mejora=$(awk -v b="$sb" -v v="$sv" 'BEGIN { if (b==0) print 0; else printf "%.1f", 100*(b-v)/b }')
echo "corridas que pasan:  base $pb  →  variante $pv"
echo "tiempo medio:        base ${sb}s →  variante ${sv}s  (mejora ${mejora} %)"
[ -n "$perdidas" ] && echo "tareas estables que ahora fallan: $perdidas"

if [ "$pv" -ge "$pb" ] && awk -v m="$mejora" 'BEGIN { exit !(m >= 15) }' && [ -z "$perdidas" ]; then
  echo "DECISIÓN: ACEPTADA"
else
  echo "DECISIÓN: RECHAZADA"; exit 1
fi
