# Informe de la prueba de la skill gusto (2.2.0)

## Qué se probó

1. **Autotest** (`verificar_gusto.py`): proporción de tonos, validación, A/B, analizador de imágenes y crítico de render con una pieza correcta y una con defectos conocidos. Pasa; lo que no puede ejecutar lo marca SALTADO.
2. **Sesión real con el modelo** en una instalación aislada, con una petición de alumno («usa mi marca.json… te dejé 7 capturas… hazme un post vertical»).

## Resultado de la sesión real

| | |
|---|---|
| Carga la skill `gusto` | Sí (Skill `brand-kit-builder:gusto`) |
| Mide las referencias con el script antes de opinar | Sí |
| Mira cada imagen y explica qué toma de cada una | Sí |
| Pasa el crítico y corrige | Sí: 0 errores, 1 aviso (441 caracteres) |
| Registra como gusto de la persona lo no confirmado | **No**: dejó `gusto.json` sin notas y lo dijo |
| Marca como ejemplo lo inventado (foto, nombre, frase, pasos) | Sí, con una píldora visible «EJEMPLO» |
| Coste | 22 turnos, ~$0,31 |

## Lo que salió mal en el camino (y qué cambió)

- **La primera sesión no valía.** `rsync` no existía en el entorno, la copia del plugin falló y la sesión corrió con la 2.1.1: la skill ni estaba. Se detectó porque no había ninguna llamada a Skill en la traza. Moraleja para alumnos: tras actualizar, comprobar con `claude plugin list` que la versión es la nueva.
- **Esa misma sesión salió de la carpeta de prueba** y leyó archivos ajenos de la máquina (incluida una pieza anterior), así que parte de su resultado era copia. En la repetición se apartaron esos archivos y el proyecto era autocontenido.
- **El crítico encontró defectos reales en piezas propias**: un pie de 18 px, textos de 16 px en un tablero y un color de tarjeta que no estaba en la marca.
- **Un error del propio crítico:** `document.fonts.check` da «verdadero» para una fuente inexistente. Se sustituyó por una medición de anchos y el autotest lo cubre.

## Límites

- Una sesión no interactiva (`claude -p`): **no se ejercitaron** la entrevista de notas, la confirmación del tono ni el A/B con una persona.
- Una persona, una marca, siete referencias SaaS. Los patrones de `tonos.md` son hipótesis.
- **No se ha comprobado que el resultado tenga «mejor gusto»**: eso solo lo dice la persona. El crítico detecta defectos, no calidad.
- No se probó en Windows ni macOS. El crítico necesita Playwright con Chromium; el analizador, Pillow.
