# turnos

API de reserva de turnos para salas. Node 20, Express, PostgreSQL.

## Comandos
- Instalar:       `npm ci`
- Pruebas:        `npm test` (rápidas, corren antes de cada commit)
- Pruebas de BD:  `npm run test:db` (necesitan Docker levantado)
- Lint:           `npm run lint`
- Nueva migración: `npm run migrate:nueva -- <nombre>`

## Estructura
- `src/rutas/`      un archivo por recurso, sin lógica de negocio
- `src/dominio/`    reglas de negocio (reservas, disponibilidad)
- `migrations/`     historial de la BD; sólo se agrega, nunca se edita

## Convenciones
- Las fechas viajan y se guardan en UTC; se convierten sólo en la interfaz.
- Todo endpoint nuevo lleva una prueba de contrato en `tests/contrato/`.
- Los errores de dominio son `ErrorDeDominio`, no `Error` genérico.

## Zonas
- No edites `migrations/`: crear una nueva con `npm run migrate:nueva`.
  (Editar una migración ya aplicada rompe a quien tenga la base al día.)
- No leas ni escribas `.env`: las credenciales las inyecta el entorno.

## Decisiones
- Las decisiones de arquitectura están en `docs/adr/`.
  Leé la que corresponda antes de proponer un cambio estructural.

## Listo significa
- `npm test` y `npm run lint` en verde.
- No modificaste pruebas existentes sin avisar y explicar por qué.
- El cambio tiene una prueba que falla sin él.
