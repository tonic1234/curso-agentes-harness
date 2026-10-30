const test = require("node:test");
const assert = require("node:assert");
const { reservar, vaciar } = require("./turnos");

test("no permite doble reserva del mismo turno", async () => {
  vaciar();
  const t = { sala: "A", hora: "10:00" };
  const [a, b] = await Promise.all([reservar(t), reservar(t)]);
  assert.strictEqual([a.ok, b.ok].filter(Boolean).length, 1);
});

test("permite turnos distintos", async () => {
  vaciar();
  const [a, b] = await Promise.all([
    reservar({ sala: "A", hora: "10:00" }),
    reservar({ sala: "A", hora: "11:00" }),
  ]);
  assert.ok(a.ok && b.ok);
});
