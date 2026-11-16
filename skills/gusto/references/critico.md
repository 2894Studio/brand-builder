# Qué hace y qué no hace `critico_render.py`

| Detecta (error) | Avisa |
|---|---|
| texto fuera del lienzo (salvo `data-bleed`) | colores fuera de `marca.json` |
| cajas de texto que se pisan | jerarquía débil (el mayor < 2,5× la mediana) |
| fuente que cae a una de reserva | más de 6 tamaños de letra |
| contraste < 4,5:1 (3:1 si es grande) | última línea con una sola palabra |
| texto menor de ~1,8 % del lado corto | más de 320 caracteres |
| | texto sobre imagen o degradado (no medible) |

**No detecta:** si es bonita, si el mensaje convence, si la foto es adecuada, si una ilustración es de mal gusto, solapes entre un texto y una imagen, ni el texto dentro de imágenes. Una pieza puede pasar el crítico y seguir siendo anodina.

Requisitos: Playwright con Chromium (Node o Python). Sin él, el script sale con código 2 y la pieza **no** se da por revisada.

Texto que debe sangrar a propósito (una inicial gigante): atributo `data-bleed` en el elemento.
