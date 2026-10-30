"""Costo por tarea con precios de lista (USD por millón de tokens). Los precios cambian: actualizá la tabla."""
PRECIOS = {"haiku": (0.10, 0.50), "sonnet": (2.0, 10.0), "opus": (4.0, 20.0)}   # (entrada, salida)

def costo(modelo, tok_in, tok_out):
    pi, po = PRECIOS[modelo]
    return (tok_in * pi + tok_out * po) / 1e6

if __name__ == "__main__":
    tarea = (20_000, 3_000)                                  # tokens de entrada y salida por tarea
    mezcla = {"haiku": 0.6, "sonnet": 0.3, "opus": 0.1}
    todo_sonnet = costo("sonnet", *tarea)
    ruteo = sum(p * costo(m, *tarea) for m, p in mezcla.items())
    print(f"todo Sonnet: ${todo_sonnet:.4f} por tarea | ruteo 60/30/10: ${ruteo:.4f} | ahorro {100*(1-ruteo/todo_sonnet):.0f} %")
    print("10.000 triajes de 600+100 tokens:", {m: round(10_000 * costo(m, 600, 100), 2) for m in PRECIOS})
    print("Jev (0,042 de entrada, salida gratis):", round(10_000 * 600 * 0.042 / 1e6, 2))
