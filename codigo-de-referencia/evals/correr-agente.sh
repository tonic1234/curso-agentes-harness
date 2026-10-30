#!/bin/bash
# Uso: ./correr-agente.sh <id-de-tarea> <corrida>
# Corre TU agente sobre una tarea y escribe una línea CSV: tarea,corrida,paso,segundos
# Configurá cómo se invoca tu agente en AGENTE_CMD. Debe leer el issue por stdin
# y devolver el JSON de la spec por stdout. Ejemplos:
#   AGENTE_CMD='claude -p "$(cat AGENTE.md)"'      (Claude Code, modo no interactivo)
#   AGENTE_CMD='codex exec "$(cat AGENTE.md)"'     (Codex)
#   AGENTE_CMD='python agente_minimo.py'           (tu propio bucle)
set -euo pipefail
cd "$(dirname "$0")"
id="$1"; corrida="$2"
entrada=$(jq -r --arg id "$id" '.[] | select(.id==$id) | .entrada' tareas.json)
esperado=$(jq -r --arg id "$id" '.[] | select(.id==$id) | .esperado' tareas.json)

inicio=$(date +%s)
salida=$(cat "$entrada" | bash -c "$AGENTE_CMD" 2>/dev/null || true)
fin=$(date +%s)

obtenido=$(echo "$salida" | jq -r '.tipo // "invalido"' 2>/dev/null || echo "invalido")
# La puerta la decide este script, no el agente:
if [ "$obtenido" = "$esperado" ]; then paso=1; else paso=0; fi
echo "$id,$corrida,$paso,$((fin - inicio))"
