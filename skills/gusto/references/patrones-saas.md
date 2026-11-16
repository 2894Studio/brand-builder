# Patrones para marcas de SaaS

Piezas habituales y cómo hacerlas sin que parezcan plantilla. Cada patrón lleva su origen y su riesgo.

| Patrón | Cómo se hace | Riesgo |
|---|---|---|
| **Tablero de marca (bento)** | módulos de tamaños mezclados con huecos iguales (12–16 px) y esquinas iguales; píldora de rótulo en cada uno: Logo, Color, Tipografía, Fotografía, Voz | rejilla de cajas del mismo tamaño = plantilla |
| **Módulo de cifra** | número grande (≥ 2,5× el texto) + etiqueta corta + **fuente** | cifra inventada: usa un dato real o un marcador «ejemplo» visible |
| **Persona con nombre y rol** | foto real, nombre y rol en una tarjeta pequeña | avatar genérico o ilustración de persona: baja la confianza |
| **Prueba de producto** | una tarjeta de interfaz flotando sobre una foto o sobre el campo de color | capturas con datos falsos presentados como reales |
| **Titular en primera persona** | «Somos la persona con la que…», «Te presentamos al equipo antes de…» | tuteo y trato coherentes con la voz de la marca |
| **Campo continuo con filetes** | fondo de un color, filetes finos verticales, tres columnas de texto | si hay tarjetas, ya no es este patrón |
| **Un acento pequeño** | un solo color vivo en menos del 5 % de la pieza | acento sobre fondo claro: comprueba contraste (un ámbar sobre crema da ~1,6:1) |

## Patrones del estilo «moderno de producto»

| Patrón | Cómo se hace | Riesgo |
|---|---|---|
| **Palabra fantasma** | nombre de marca en 260–330 px, blanco al 13 %, detrás de todo; en el HTML con `data-decorativo` | si se corta una letra («FINDPR») parece un error: ajusta el tamaño hasta que quepa entera |
| **Maqueta con interfaz** | teléfono dibujado en CSS (esquinas 70 px, isla, borde oscuro) con una pantalla de **producto real o plausible** (lista, cifra, botón) | texto de interfaz menor de 19 px: no se lee en una red social |
| **Tarjeta de cristal** | `background: rgba(255,255,255,.16)`, `backdrop-filter: blur(14px)`, borde 1,5 px blanco al 35 % | sobre fondo claro desaparece; comprueba el contraste del texto |
| **Foto en tarjeta** | esquinas 30–34 px, borde blanco al 55 %, rótulo oscuro translúcido con nombre y rol | rótulo claro sobre camisa blanca: usa un fondo oscuro translúcido |
| **Desvanecido inferior** | degradado a azul profundo en el último tercio para que el titular se lea | sin él, el titular pisa la maqueta |
| **Personas sintéticas** | generadas (por ejemplo con Canva) y declaradas en el pie de la pieza | en una firma de personas reales, sustituir por fotos reales antes de publicar |

## Tamaños que funcionan (post vertical 1080 × 1440)

- Titular: 96–130 px, peso ligero si es serif.
- Etiqueta o sobretítulo: ≥ 24 px en mayúsculas con espaciado.
- Texto de apoyo: 26–34 px. **Nada por debajo de 19 px.**
- Margen exterior 60–96 px; huecos del bento 16 px; esquinas 16–20 px.

## Antes de dar la pieza por buena

Pasa `critico_render.py`, mira la captura y responde las cinco preguntas de `criterio.md`.
