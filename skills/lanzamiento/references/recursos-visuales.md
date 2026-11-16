# Catálogo de recursos visuales

Cada recurso muestra algo con una **prueba**. Elige según el mensaje y el tono dominante de `gusto.json`. Esto es un catálogo de **ideas y andamios**, no de plantillas: ver `direccion-creativa.md`. Todos usan los componentes de `post_base.py` (`.cristal`, `.foto`, `.rotulo`, `.telefono`, `.pantalla`). Medidas del post: 1080×1440, márgenes de 70 px, nada de texto por debajo de 19 px (el crítico lo comprueba).

| Quiero mostrar… | Recurso | Tono que encaja | Prueba que lleva |
|---|---|---|---|
| La foto como protagonista (marca visual: fotografía, gastronomía, moda, viajes; o cualquiera con fotos buenas) | **Foto a sangre + bloque opaco** | cualquiera | `post_foto.py`: foto real, titular en bloque opaco, `--notas` para anotar sobre la foto |
| Producto web, panel, curso o código | **Ventana de escritorio** | tecnológico / serio | `post_pantalla.py`: menú, cifra, filas o bloque de código |
| Precio o modelo frente a la alternativa | **Comparativa** | serio | `post_comparativa.py`; el dato del competidor lleva fuente o no se muestra |
| Qué hace el producto o servicio | **Teléfono con la interfaz** | tecnológico | una pantalla plausible: lista, cifra, botón |
| Que está cerca, por zona | **Mapa de puntos** | tecnológico, cercano | distancias reales a ciudades reales |
| Rigor, seriedad | **Cifra gigante con su fuente** | serio | el dato y la fuente citada |
| Trato humano | **Persona con nombre y rol** | cercano | foto real, nombre, rol |
| Cambio, mejora | **Antes y después** | serio, tecnológico | dos estados medidos |
| Proceso | **Pasos con filetes finos** (3 o 4 columnas) | serio | un verbo y una consecuencia por paso |
| Producto físico | **Foto del producto** sobre campo liso | cualquiera | la fotografía |

## Teléfono con interfaz

**Generador:** `tools/post_telefono.py` (ver `SKILL.md`). Lo que sigue explica cómo está hecho, por si hay que construir uno distinto.

```html
<div class="telefono" style="left:50%;top:60px;width:470px;height:930px;margin-left:-235px"><div class="pantalla">
  <!-- 19 px como mínimo en TODO el texto de la pantalla -->
  <p style="font-size:20px">Contexto</p><p style="font:600 38px var(--f-titulos)">Título de la pantalla</p>
  <!-- filas de lista, una cifra grande, un botón en color primario -->
</div></div>
```
Termínalo antes del titular (≥ 80 px de margen) para que el teléfono no choque con el texto de abajo, y con un degradado a color profundo en el último tercio.

## Mapa de puntos

**Generador:** `tools/post_mapa.py`. Lo que sigue explica cómo está hecho.

1. Una vez: `npm i world-atlas topojson-client d3-geo` en la carpeta de trabajo.
2. `node skills/gusto/tools/mapa_puntos.mjs --bbox lonMin,latMin,lonMax,latMax --centro lon,lat > puntos.json`
3. Dibuja los puntos como círculos SVG; el radio de «tu zona» es `km × kmPx`, no «más o menos».
4. Marcadores solo en **ciudades reales** dentro del radio, con la distancia verdadera. Difumina los bordes con `mask-image`.

Detalle y riesgos en `../../gusto/references/patrones-saas.md`.

## Cifra con fuente

Un número enorme (≥ 2,5× el texto de apoyo), una línea que dice qué es y la **fuente** debajo. Si no hay dato real, anótalo en el `LEEME.md` y, si la persona lo pide, `ejemplo` junto a la cifra.

## Persona con nombre y rol

Foto en tarjeta de esquinas ≥ 30 px, rótulo oscuro translúcido con nombre, rol y (si aplica) una distancia. Foto real si la hay; si es generada, solo se anota en los créditos (y en la pieza si la persona lo pide); sin foto, marcador.

## Lo que sale de este catálogo en el bento

El bento no lleva recurso propio: reúne logo, símbolo, color, tipografía, voz, fotografía, persona y proporción, con una tarjeta de **prueba** (`--prueba`) que repite la del post 1.

## Dos casos

- **Findpro (equipos de IA):** post 1 = teléfono con «Equipo propuesto»; post 2 = mapa de puntos «cerca de ti». Hecho y revisado.
- **PULSO (mantenimiento de bicicletas por suscripción) — propuesta sin ejecutar:** post 1 = pantalla de la suscripción con «Próxima revisión: martes» y las tres cosas que incluye; post 2 = si el atributo es «te la recogemos en el portal», un mapa de puntos de Madrid con la ruta de recogida. Hay que confirmar con datos reales antes de montarlo.
