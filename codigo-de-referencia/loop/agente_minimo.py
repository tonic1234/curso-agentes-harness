"""Agente mínimo: un modelo, dos herramientas y un tope de pasos.
Uso:  python agente_minimo.py "Listá los archivos y decime qué hace este repo"
Requiere:  pip install anthropic   y la variable ANTHROPIC_API_KEY
"""
import os
import subprocess
import sys

import anthropic

client = anthropic.Anthropic()                      # lee ANTHROPIC_API_KEY
MODELO = os.environ.get("MODELO", "claude-sonnet-5-5")
MAX_PASOS = 10                                      # tope: primera defensa barata

# 1) Herramientas: lo único que el agente puede hacer en el mundo
HERRAMIENTAS = [
    {"name": "leer",
     "description": "Lee un archivo de texto del repo y devuelve su contenido.",
     "input_schema": {"type": "object",
                      "properties": {"ruta": {"type": "string"}},
                      "required": ["ruta"]}},
    {"name": "correr",
     "description": "Corre un comando de shell y devuelve su salida.",
     "input_schema": {"type": "object",
                      "properties": {"cmd": {"type": "string"}},
                      "required": ["cmd"]}},
]


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()[:20000]                     # recortar: el contexto es finito


def correr(cmd):
    # OJO: sin permisos ni filtros. Esto es lo que falta (unidad 4).
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
    return (r.stdout + r.stderr)[-20000:] or "(sin salida)"


IMPLEMENTACION = {"leer": leer, "correr": correr}


def agente(tarea):
    # 2) El primer mensaje es el contexto inicial
    mensajes = [{"role": "user", "content": tarea}]

    # 3) Tope de pasos
    for paso in range(MAX_PASOS):
        resp = client.messages.create(model=MODELO, max_tokens=2000,
                                      tools=HERRAMIENTAS, messages=mensajes)
        mensajes.append({"role": "assistant", "content": resp.content})

        # 5) Criterio de parada: el modelo ya no pide herramientas
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")

        # 4) Ejecutar lo pedido y devolver lo que pasó de verdad
        resultados = []
        for b in resp.content:
            if b.type == "tool_use":
                print(f"[paso {paso + 1}] {b.name} {b.input}", file=sys.stderr)
                try:
                    salida = IMPLEMENTACION[b.name](**b.input)
                except Exception as e:              # el error también es información
                    salida = f"ERROR: {e}"
                resultados.append({"type": "tool_result",
                                   "tool_use_id": b.id, "content": salida})
        mensajes.append({"role": "user", "content": resultados})

    return "me quedé sin pasos"


if __name__ == "__main__":
    pedido = " ".join(sys.argv[1:]) or "Listá los archivos y decime qué hace este repo"
    print(agente(pedido))
