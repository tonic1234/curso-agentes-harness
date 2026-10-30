"""Cliente mínimo de Jev (TypeSafe System One) servido por OpenCode Zen.
Jev no genera texto: recibe un estado y preguntas con tipo, y devuelve decisiones con probabilidades.
Sólo librería estándar. Variables: OPENCODE_API_KEY (clave de tu consola de OpenCode).
"""
import json
import os
import urllib.request

URL = os.environ.get("JEV_URL", "https://opencode.ai/inference/systemone/v1/systemone")
MODELO = os.environ.get("JEV_MODELO", "jev-1.13")      # o "jev-1.13-free" mientras dure la gratuidad


def decidir(estado, preguntas, timeout=4):
    """Devuelve el dict `answers` de Jev. Lanza una excepción si algo falla (el llamador decide)."""
    cuerpo = json.dumps({"state": estado, "model": MODELO, "questions": preguntas}).encode()
    req = urllib.request.Request(
        URL, data=cuerpo, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + os.environ["OPENCODE_API_KEY"]})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)["answers"]
