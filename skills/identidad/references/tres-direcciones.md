# Tres direcciones de identidad, dentro del plugin (gratis)

Es la alternativa propia a la técnica «Logo to Brand Identity» de FLORA: mismo objetivo (explorar tres direcciones a partir del logo), sin coste y con resultado editable.

## Pasos
1. **Lee el logo de verdad.** Ábrelo (`logo/principal.png` o el SVG) y anota en 4 líneas: **letras** (caja, peso, anchura, remates), **construcción** (geométrica, orgánica, símbolo integrado en una letra), **color** (cuántas tintas, temperatura) y **acabado** (plano, con volumen, trazo a mano). Aquí no se inventa: lo que ves.
2. **Cruza con la estrategia** (`estrategia.md`, `gusto.json`): público, tono, «nunca debe parecer». Si el logo sugiere una cosa y la estrategia otra, gana la estrategia.
3. **Escribe `direcciones.json` con 2 o 3 direcciones que se diferencien de verdad** (otra paleta, otra tipografía de títulos, otro gráfico firma, otro radio de esquinas), p. ej. una sobria, una expresiva y una tecnológica. Formato en la cabecera de `tools/tableros_identidad.py`.
4. **Renderiza:** `python3 skills/identidad/tools/tableros_identidad.py marca.json direcciones.json --salida trabajo/<…>/direcciones [--fotos lanzamiento/fotos]` → `direccion-N.html` y `.png` (con el crítico).
5. **Míralos y que elija la persona** con un diálogo. Del elegido: paleta (comprobada con `contraste.py`), tipografías, gráfico firma y estilo de imagen pasan a `marca.json` → `visual` y a `kit.json` → `fotografia`.

## Límites (decirlos)
- Los tableros son **maquetas en HTML**, no fotografía ni mockups de objetos: para eso hace falta un proveedor de imágenes (Canva, Gemini, FLORA).
- Las direcciones son **propuestas del modelo**, no medidas: los colores se comprueban antes de adoptarlos.
- Las tipografías son de Google Fonts: sin conexión se ve una de reserva.
