# Curso Agentes con Harness

Curso-taller de dos días para equipos de front y back: entender, dirigir, construir, mejorar y gobernar agentes de código con harness.

**Sitio publicado:** https://tarsterminal.duckdns.org/curso-agentes-harness/
**Copia en GitHub Pages:** https://tonic1234.github.io/curso-agentes-harness/
**Repositorio:** https://github.com/tonic1234/curso-agentes-harness

## Qué hay acá

- `index.html`: la presentación completa (Día 1 y Día 2) en un solo archivo. Se abre con doble clic o se sube a cualquier hosting estático.
- `codigo-de-referencia/`: el código de las recetas (bucle mínimo, AGENTS.md, permisos y hooks, subagentes, evals, CI, telemetría y router de modelos con Jev). Es el mismo que aparece en la pestaña «Código de referencia» de cada receta.

## Cómo se usa

- Flechas ← → para avanzar; ↓ ↑ para los pasos de las animaciones.
- <kbd>N</kbd> abre las notas del orador (guion, contexto y fuentes), <kbd>G</kbd> el glosario, <kbd>A</kbd> la agenda, <kbd>F</kbd> pantalla completa.
- El selector «Día 1 / Día 2» está arriba a la derecha.
- Cada diapositiva tiene su enlace propio: `index.html#d2-57` es la diapositiva 57 del Día 2.

## Cómo servirlo

Cualquier hosting de archivos estáticos sirve, porque no hay servidor ni base de datos:

- **GitHub Pages**: Settings → Pages → Deploy from a branch → `main` / `/ (root)`.
- **Netlify Drop**: arrastrá esta carpeta a app.netlify.com/drop.
- **Vercel, Cloudflare Pages o un servidor propio**: subí la carpeta tal cual; `index.html` es la página de entrada.

En un servidor propio conviene servir `index.html` con `Cache-Control: no-cache, must-revalidate` para que una edición nueva no quede tapada por la caché del navegador.

## Tené en cuenta

- **Notas del orador**: van dentro de la presentación. Si la publicás para los alumnos, también ven el guion.
- **Termómetro del Día 1**: el código QR apunta a una encuesta privada alojada en claude.ai. Para usarla con el público, compartila desde esa página o reemplazá el enlace por un formulario propio.
- **Necesita internet** para las tipografías (Google Fonts) y para dibujar el QR (cdnjs). Sin conexión funciona igual, con tipografías del sistema y sin el QR.
- **Lo que se guarda**: lo que escriben los asistentes (plan, respuestas) se guarda sólo en su navegador.
- **Datos que vencen**: los precios y las cifras de proveedores son del 30 de octubre de 2026. Revisalos antes de cada edición del curso.

---

Material del curso · Soma · Axonica Group
