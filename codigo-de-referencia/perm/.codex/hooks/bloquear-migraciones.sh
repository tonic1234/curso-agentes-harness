#!/bin/bash
# Codex: el JSON llega por stdin con .tool_input. Sale con 2 para bloquear.
# Primero mirá qué recibe tu versión:  cat > /tmp/entrada.json  y revisalo.
cmd=$(jq -r '.tool_input.command // empty')

if echo "$cmd" | grep -q "migrations/" && echo "$cmd" | grep -Eq '(>|sed -i|rm |mv |cp |tee )'; then
  echo "Bloqueado: no se editan migraciones. Usá: npm run migrate:nueva -- <nombre>" >&2
  exit 2
fi
exit 0
