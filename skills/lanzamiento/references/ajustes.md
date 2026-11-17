# Vocabulario de ajustes: decir «más atrevido» y que cambie algo concreto

Cuando la persona dice que una pieza «no convence», pídele **un verbo** y aplica el cambio de la tabla en el `brief.json` (o en el generador). Una sola cosa a la vez; se renderiza y se mira. Inspirado en el vocabulario de comandos de otros proyectos de diseño (por ejemplo Impeccable, Apache-2.0), reescrito para piezas de marca y no para código.

| Verbo | Qué significa | Qué cambiar (ejemplos concretos) |
|---|---|---|
| **más atrevido** | menos plantilla, más carácter | pasar a `expresivo_gigante`/`expresivo_precio` o a `manifiesto`; `tema` oscuro; titular un nivel mayor; acento en un bloque a sangre; una foto con personalidad |
| **más sobrio** | más calma | `tema` claro; `pasos` o `cifra`; quitar insignias y ornamentos; un solo acento pequeño; más aire |
| **simplificar** | quitar hasta lo esencial | un mensaje, un recurso, un dato; menos de 25 palabras; menos de 4 tamaños de letra |
| **más humano** | persona delante | `foto` con persona; nota manuscrita o rol con nombre real; voz en primera persona |
| **más técnico** | prueba tangible | `pantalla`/`telefono` si el producto es digital; una cifra con fuente; una línea de código o dato real |
| **más tipografía** | el texto manda | `manifiesto` o `cifra`; titular 120 px o más; una palabra en color; la inicial de la marca a sangre |
| **más aire** | respirar | quitar elementos, subir márgenes a 90 px, reducir el texto de apoyo |
| **más contraste** | se lee mejor | pasar a `tema` oscuro o claro del extremo; tinta más oscura; acento solo en grande |
| **menos genérico** | que no parezca de otra marca | cambiar la tipografía de títulos; añadir el gráfico firma; usar una foto propia; revisar `revision-gusto.md` |

## Reglas
- **Un verbo, un cambio, un render.** Si se aplican tres a la vez, no se sabe cuál funcionó.
- Tras el ajuste, se vuelve a ejecutar `kit_lanzamiento.py`: el crítico, las huellas de plantilla y la puerta se aplican igual.
- Si el verbo contradice las reglas de `gusto.json` (`gusto.py reglas`), gana la regla y se dice por qué.
