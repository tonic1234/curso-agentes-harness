import os, sys, types, json
sys.path.insert(0, os.path.dirname(__file__))
os.environ["OPENCODE_API_KEY"] = "x"
import jev_cliente, ruteo

def jev_falso(dif, conf_d, alc="uno", conf_a=0.9):
    return lambda estado, preguntas: {
        "dificultad": {"type": "choice", "choice": dif, "confidence": conf_d, "probabilities": {}},
        "alcance": {"type": "choice", "choice": alc, "confidence": conf_a, "probabilities": {}}}

def caso(nombre, decidir_falso, esperado):
    ruteo.decidir = decidir_falso
    n, m = ruteo.elegir_nivel("tarea")
    assert n == esperado, (nombre, n, m); print("ok", nombre, "->", n, m)

caso("fácil y seguro", jev_falso("facil", 0.9), "chico")
caso("normal", jev_falso("normal", 0.9), "medio")
caso("difícil", jev_falso("dificil", 0.9), "fuerte")
caso("fácil pero poca confianza", jev_falso("facil", 0.5), "fuerte")
def roto(*a): raise TimeoutError()
caso("jev falla", roto, "fuerte")

# escalada por puerta: el chico falla, el medio pasa
if os.path.exists(ruteo.REGISTRO): os.remove(ruteo.REGISTRO)
ruteo.decidir = jev_falso("facil", 0.95)
llamadas = []
def agente(modelo, tarea): llamadas.append(modelo); return modelo
res, intentos = ruteo.resolver("t", agente, puerta=lambda r: r != "haiku")
assert llamadas == ["haiku", "sonnet"] and res == "sonnet", llamadas
ruteo.resumen()
os.remove(ruteo.REGISTRO)
print("TODO OK")
