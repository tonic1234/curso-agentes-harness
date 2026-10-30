#!/bin/bash
# Uso: ./comparar-costo.sh base.csv ruteo.csv     (columnas: tarea,corrida,paso,costo_usd)
# Regla: aprobadas >= base  Y  costo por tarea aprobada baja >= 30 %  Y  ninguna tarea estable empieza a fallar.
base="$1"; var="$2"
resumen() {   # imprime: aprobadas costo_total
  awk -F, 'NR>1 { p+=$3; c+=$4 } END { printf "%d %.4f\n", p, c }' "$1"
}
estables() {  # tareas que pasan en todas sus corridas
  awk -F, 'NR>1 { t[$1]++; o[$1]+=$3 } END { for (k in t) if (o[k]==t[k]) print k }' "$1" | sort
}
read -r pb cb <<< "$(resumen "$base")"
read -r pv cv <<< "$(resumen "$var")"
[ "$pb" -eq 0 ] || [ "$pv" -eq 0 ] && { echo "sin corridas aprobadas: no se puede calcular"; exit 1; }
xb=$(awk -v c="$cb" -v p="$pb" 'BEGIN{printf "%.4f", c/p}')
xv=$(awk -v c="$cv" -v p="$pv" 'BEGIN{printf "%.4f", c/p}')
baja=$(awk -v b="$xb" -v v="$xv" 'BEGIN{printf "%.1f", 100*(b-v)/b}')
perdidas=$(comm -23 <(estables "$base") <(estables "$var") | grep . || true)
echo "aprobadas:                 base $pb → ruteo $pv"
echo "costo por tarea aprobada:  base \$$xb → ruteo \$$xv  (baja ${baja} %)"
[ -n "$perdidas" ] && echo "tareas estables que ahora fallan: $perdidas"
if [ "$pv" -ge "$pb" ] && awk -v m="$baja" 'BEGIN{exit !(m>=30)}' && [ -z "$perdidas" ]; then
  echo "DECISIÓN: ACEPTADA"
else
  echo "DECISIÓN: RECHAZADA"; exit 1
fi
