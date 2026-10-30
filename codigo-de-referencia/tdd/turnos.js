// Reserva de turnos en memoria. Versión CORREGIDA.
// El bug original: se verificaba la disponibilidad y se guardaba en dos pasos
// separados por un await, así que dos pedidos simultáneos pasaban la verificación.
const reservados = new Set();
let cola = Promise.resolve();            // serializa las reservas

const clave = (t) => `${t.sala}|${t.hora}`;
const pausa = (ms) => new Promise((r) => setTimeout(r, ms));

async function reservarSinProteccion(t) {            // versión con el bug
  if (reservados.has(clave(t))) return { ok: false };
  await pausa(5);                                   // simula la base de datos
  reservados.add(clave(t));
  return { ok: true };
}

function reservar(t) {                              // versión corregida
  const turno = cola.then(async () => {
    if (reservados.has(clave(t))) return { ok: false };
    await pausa(5);
    reservados.add(clave(t));
    return { ok: true };
  });
  cola = turno.catch(() => {});                     // un error no frena la cola
  return turno;
}

function vaciar() { reservados.clear(); }

module.exports = { reservar, reservarSinProteccion, vaciar };
