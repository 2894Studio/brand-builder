---
name: laminas
description: Monta el manual de marca como láminas SVG con rejilla de 12 columnas, firma gráfica según el territorio, index.html navegable y PDF, sin necesitar Canva. Úsala con «hazme el manual de marca», «brand book», «kit de marca», «presentación de mi marca», «las láminas de la identidad».
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Láminas: el manual de marca

Convierte `marca.json` y un `kit.json` de contenido en un manual presentable. Solo con Claude y Python; no hace falta ninguna cuenta. Requiere logo y paleta aprobados.

Lee `references/sistema-laminas.md` (rejilla, escala, arquetipos, firmas, revisión) y `references/imperfeccion.md`. El formato de `kit.json` está en `references/kit-json.md`.

## Orden de trabajo

1. **Redacta `kit.json`** con el contenido: promesa, 3 o 4 valores (cada uno con una frase que diga qué implica en la práctica), tres rasgos de voz, fotografía sí/no, elementos, reglas de uso y las dos aplicaciones que dijo en la entrevista. Adapta: una marca de servicios no necesita envase, necesita firma de correo y plantilla de propuesta. «Artesanal» no es un valor; «hecho a mano, con oficio» sí.
2. **Genera:**

> En Windows, `python3` suele ser `python` o `py`. Necesita Python 3.11 o superior.

```
python3 tools/generar_kit.py marca.json --kit trabajo/<fecha>-marca-<slug>/kit.json --salida trabajo/<fecha>-marca-<slug>/kit
```

Sale: portada, 4 divisores y 11 láminas de contenido (12 con mockup), `index.html` con todo el pase y, si `rsvg-convert` está instalado, `manual-de-marca.pdf`. Sin él, imprime `index.html` a PDF desde el navegador.

3. **Lee los avisos.** Cada texto recortado, título largo, logo provisional o dato que falta en `kit.json` se dice en voz alta. Un título de más de dos líneas se **acorta**, no se baja el resto.
4. **Revisa el pase entero en miniatura** con las ocho preguntas de la sección 8 de `sistema-laminas.md`. El autotest (`python3 tools/verificar_laminas.py`) cubre las mecánicas; el ritmo y la coherencia los juzgas tú.

## Reglas que no se negocian

- Una sola firma gráfica, la del territorio, en todas las láminas.
- Panel opaco siempre que haya texto y foto juntos. La numeración del arquetipo D va **dentro** del panel.
- Máximo 2 tipografías y un acento por lámina; cuerpo nunca por debajo de 26 px.
- Los marcadores de fotografía son marcadores: la fotografía propia los sustituye. No generes una escena entera por lámina: una textura o un patrón sirven a todo el kit.

## Mockups (solo si se pidieron en la entrevista)

Genera el producto **en blanco**, sin rotulación (intención `imagen.generar`), y superpón el logo y la rotulación como elementos. Un producto con el logo dibujado dentro obliga a regenerar la escena entera cuando el logo cambie. Di en la lámina que es una escena generada y que el logo va plano.

Siguiente: `entrega`.
