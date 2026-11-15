# Escala web

Derivada de la escala de láminas (1920 × 1080), llevada a `rem` con razón 1,25.

| Token | rem | px (16 base) | Equivalente en láminas |
|---|---|---|---|
| `font.size.xs` | 0,8 | 12,8 | pie y numeración (20) |
| `font.size.sm` | 0,875 | 14 | etiqueta (22) |
| `font.size.base` | 1 | 16 | **cuerpo (28)** |
| `font.size.lg` | 1,25 | 20 | entradilla (34) |
| `font.size.xl` | 1,563 | 25 | subtítulo |
| `font.size.2xl` | 1,953 | 31 | |
| `font.size.3xl` | 2,441 | 39 | **título de lámina (72)** |
| `font.size.4xl` | 3,052 | 49 | |
| `font.size.display` | 3,815 | 61 | display de portada (120) |

La correspondencia es de **jerarquía**, no de tamaño literal: una lámina de 1920 px y una pantalla de 390 px no comparten escala absoluta. Lo que se conserva es la relación entre cuerpo, entradilla y título.

**Interlineado:** display 1,0 · títulos 1,1 · cuerpo 1,5 · etiquetas 1,4 (los mismos que las láminas).
**Pesos:** regular 400 · medium 500 · bold 700.

## Espaciado

Base 8, con 4 para ajustes finos: 0, 4, 8, 12, 16, 20, 24, 32, 48, 64, 96, 128 px (`space.1`…`space.32`). El medianil de 24 px de la rejilla de láminas es `space.6`.
