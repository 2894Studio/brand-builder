# Dirección creativa: que cada marca tenga sus piezas

Una pieza que podría ser de cualquier otra marca cambiando el logo es una plantilla, y una plantilla no es un resultado. Los generadores (`post_telefono.py`, `post_pantalla.py`…) son **andamios y ejemplos de calidad**, no la respuesta por defecto. Lo normal es **componer la pieza con `post_base.py`** y los componentes, a partir de lo que esa marca necesita enseñar.

## Antes de tocar nada: el brief de cada pieza (5 líneas)

Escríbelo en el chat o en `lanzamiento/brief.md`:

1. **Qué tiene que entender quien lo ve en 2 segundos.** Una frase.
2. **Qué prueba lo demuestra** y de dónde sale (dato real, foto real, interfaz real, de ejemplo marcado).
3. **Tres conceptos visuales que difieran en estructura**, no en acabado (por ejemplo: «ventana de producto», «pizarra con apuntes a mano», «cifra gigante con su fuente»). Dos versiones del mismo esquema no son dos conceptos.
4. **Cuál eliges y por qué encaja con esta marca** (categoría, tono de `gusto.json`, lo que prohíben sus referencias).
5. **Qué lo haría intercambiable** con otra marca, y cómo lo evitas.

## La categoría manda

| Categoría | Qué suele pedir el post «qué es» | Qué suele pedir el post «atributo» | Bento |
|---|---|---|---|
| **Educativa / formación** | un temario o recorrido, una sesión en directo, una libreta, una pizarra, el docente en clase | el resultado (proyecto final, portfolio) o el formato (grupo pequeño, en vivo) con su dato | `--variante educativa` (recorrido como tarjeta principal) o uno propio |
| **SaaS / software** | la interfaz real del producto en su soporte natural (web, escritorio, móvil) | una métrica del producto o un flujo de 3 pasos | generica; datos y puntos reales |
| **Servicio local o profesional** | la persona y el oficio en su contexto; una zona | cercanía (mapa), garantía con su condición, un antes y después | generica con fotos o `--puntos` |
| **Producto físico** | el producto sobre campo liso, en uso | un detalle de material o proceso | `--variante producto` (exige foto) |
| **Marca personal / editorial** | tipografía como protagonista, una cita propia | una idea propia en gran formato | uno propio, sin foto |

Es una guía, no una tabla cerrada: si la marca pide otra cosa, la haces.

## Variar de verdad

- **Las dos piezas de un mismo kit no comparten esquema.** Si el post 1 es una ventana, el post 2 es otra cosa (cifra, pasos, foto, mapa, comparativa).
- **Entre marcas, tampoco.** Antes de entregar, pasa `tools/variedad.py` contra la otra pieza del kit y contra los kits anteriores:
  ```
  python3 skills/lanzamiento/tools/variedad.py lanzamiento/post-2-atributo.html lanzamiento/post-1-que-es.html --carpeta trabajo
  ```
  Si sale «PARECIDA» (≥ 0,6), cambia la composición, no los textos ni los colores.
- **Jerarquía y encuadre distintos:** cambia dónde cae el peso (arriba/abajo, a sangre, recorte grande), no solo el recurso.
- **Si usas un generador, personalízalo:** `--tema`, otro orden, un elemento propio dentro de `.visual`. Un generador sin tocar es el punto de partida, no la entrega.

## Bento a medida

`bento.py` ofrece `--variante generica | educativa | producto`. Cuando ninguna encaje, **copia `bento.py` a la carpeta de trabajo y cambia la rejilla y las tarjetas** (las tarjetas ya son módulos: logo, símbolo, color, tipografía, voz, prueba, datos, recorrido…). Decide el conjunto de tarjetas por la marca, no por la plantilla: una marca educativa necesita recorrido y formato; una de producto, la fotografía; una personal, la tipografía y la voz.
