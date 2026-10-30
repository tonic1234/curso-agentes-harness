#!/bin/bash
# Falla (exit 1) si el repo no cumple el contrato mínimo para agentes.
# Uso en CI:  ./ci/check-agents.sh        Uso local: ./ci/check-agents.sh ruta/al/repo
repo="${1:-.}"
archivo="$repo/AGENTS.md"
errores=0
falla() { echo "✗ $1"; errores=$((errores + 1)); }

[ -f "$archivo" ] || { echo "✗ Falta AGENTS.md en $repo"; exit 1; }

# 1) Secciones obligatorias
for seccion in Comandos Zonas "Listo significa"; do
  grep -q "^## $seccion" "$archivo" || falla "Falta la sección «## $seccion»"
done

# 2) Tamaño: un contrato largo no se lee
lineas=$(wc -l < "$archivo")
[ "$lineas" -le 150 ] || falla "AGENTS.md tiene $lineas líneas (máximo 150)"

# 3) Lo que nunca debe estar en un contrato
grep -Eqi '(api[_-]?key|password|secret)[[:space:]]*[:=]' "$archivo" && falla "Parece contener una credencial"

# 4) Todo lo que se menciona como comando existe en package.json (si el repo es Node)
if [ -f "$repo/package.json" ]; then
  for s in $(grep -oE 'npm run [a-z:_-]+' "$archivo" | awk '{print $3}' | sort -u); do
    jq -e --arg s "$s" '.scripts[$s]' "$repo/package.json" >/dev/null 2>&1 \
      || falla "AGENTS.md menciona «npm run $s» pero no existe en package.json"
  done
fi

[ "$errores" -eq 0 ] && echo "✓ Contrato de agentes correcto" || { echo "$errores problema(s)"; exit 1; }
