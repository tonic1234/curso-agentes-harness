#!/bin/bash
# Claude Code: recibe un JSON por stdin. Sale con 2 para BLOQUEAR.
ruta=$(jq -r '.tool_input.file_path // empty')

if [[ "$ruta" == *"/migrations/"* ]]; then
  echo "Bloqueado: no se editan migraciones. Usá: npm run migrate:nueva -- <nombre>" >&2
  exit 2          # 2 = bloquear y devolverle el mensaje al agente
fi
exit 0            # 0 = dejar pasar
