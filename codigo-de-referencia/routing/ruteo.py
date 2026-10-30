"""Router de modelos con umbral de confianza, falla hacia el modelo fuerte y escalada por puerta.

Idea: una decisión barata (¿qué tan difícil es esta tarea?) elige el modelo; una PUERTA verifica el
resultado; si no pasa, se sube de nivel. Cada decisión queda registrada para calibrar el umbral después.
"""
import json
import time

from jev_cliente import decidir

NIVELES = ["chico", "medio", "fuerte"]                 # de menor a mayor costo
MODELOS = {"chico": "haiku", "medio": "sonnet", "fuerte": "opus"}   # alias: mapealos a tu herramienta
UMBRAL = 0.75                                          # empezá conservador y ajustalo con el registro
REGISTRO = "ruteo-decisiones.jsonl"

PREGUNTAS = {
    "dificultad": {
        "type": "choice",
        "instructions": "¿Qué tan difícil es esta tarea de programación para un asistente de código?",
        "criteria": {
            "facil": "Cambio local y obvio: renombrar, texto, una función corta, un test simple",
            "normal": "Cambio acotado que exige leer algo de contexto: un bug claro, una feature chica",
            "dificil": "Diseño, bug sin causa conocida, concurrencia, seguridad o muchos módulos",
        },
    },
    "alcance": {
        "type": "choice",
        "instructions": "¿Cuántos archivos hay que tocar?",
        "criteria": {"uno": "Uno solo", "varios": "Dos o más, con cambios coordinados"},
    },
}


def elegir_nivel(tarea):
    """Devuelve (nivel, motivo). Ante cualquier duda o falla: el nivel fuerte (falla abierta)."""
    try:
        r = decidir(tarea, PREGUNTAS)
        dif, alc = r["dificultad"], r["alcance"]
    except Exception as e:                              # Jev caído, lento o respuesta rara
        return "fuerte", f"jev-fallo:{type(e).__name__}"

    if min(dif["confidence"], alc["confidence"]) < UMBRAL:
        return "fuerte", "baja-confianza"
    if dif["choice"] == "dificil" or alc["choice"] == "varios":
        return "fuerte" if dif["choice"] == "dificil" else "medio", "decision"
    return ("chico" if dif["choice"] == "facil" else "medio"), "decision"


def resolver(tarea, correr_agente, puerta):
    """correr_agente(modelo, tarea) -> resultado ; puerta(resultado) -> True/False.
    Prueba el nivel elegido y, si la puerta falla, sube hasta el fuerte."""
    nivel, motivo = elegir_nivel(tarea)
    intentos = []
    for n in NIVELES[NIVELES.index(nivel):]:
        t0 = time.time()
        resultado = correr_agente(MODELOS[n], tarea)
        paso = bool(puerta(resultado))
        intentos.append({"nivel": n, "paso": paso, "segundos": round(time.time() - t0, 2)})
        if paso:
            break
    with open(REGISTRO, "a", encoding="utf-8") as f:    # para etiquetar y calibrar después
        f.write(json.dumps({"tarea": tarea[:80], "elegido": nivel, "motivo": motivo,
                            "intentos": intentos}, ensure_ascii=False) + "\n")
    return resultado, intentos


def resumen(ruta=REGISTRO):
    """Cuántas tareas resolvió cada nivel y cuántas escalaron (si escalan mucho, el router está mal)."""
    total = escaladas = 0
    por_nivel = {}
    for linea in open(ruta, encoding="utf-8"):
        d = json.loads(linea)
        total += 1
        escaladas += len(d["intentos"]) > 1
        final = d["intentos"][-1]
        if final["paso"]:
            por_nivel[final["nivel"]] = por_nivel.get(final["nivel"], 0) + 1
    print(f"tareas: {total} | resueltas por nivel: {por_nivel} | escaladas: {escaladas}")
