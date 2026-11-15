---
name: voz
description: Define cómo habla la marca: trato, tres rasgos con ejemplos así sí / así no, las seis situaciones difíciles (queja, error propio, humor, precio, competencia, mala noticia) y la lista de palabras prohibidas. Úsala con «cómo debe sonar mi marca», «tono de voz», «qué no debo decir», «escribe mi copy con mi marca».
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Voz

La voz es comportamiento, no adjetivos. «Somos cercanos» no le sirve a nadie que tenga que escribir un correo el martes. Lee `references/voz.md` y `../identidad/references/lexico-prohibido.md`.

Requiere el manifiesto de `estrategia`, en especial las dos últimas líneas: lo que la marca diría y lo que nunca diría.

## Qué se decide

1. **Trato:** tutea o usted. Es lo que más se nota y lo que más se incumple.
2. **Tres rasgos**, cada uno con un «así sí» y un «así no» **escritos de verdad**, con hechos concretos de la marca.
3. **Las seis situaciones**, cada una con su ejemplo literal: queja · error propio · humor · precio · competencia · mala noticia.
4. **Palabras que no se usan:** al menos cinco, propias de la categoría (las del léxico general ya están prohibidas). Es más operativa que cualquier descripción de tono.

## Qué dejas escrito

- `trabajo/<fecha>-marca-<slug>/voz.md` con todo lo anterior.
- En `marca.json`: `tono` (una frase con trato, distancia, humor y ritmo) y `palabrasProhibidas`.
- Para el manual: `voz.rasgos` en `kit.json` (tres, con `asi_si` y `asi_no`). Formato en `../laminas/references/kit-json.md`.

## Antes de dar nada por bueno

Escribe cada «así sí» de modo que **no sirva para un competidor cambiando el nombre**. Pasa el texto por el validador (`python3 ../tokens/tools/validar_marca.py marca.json`): avisa del léxico prohibido en `tono` y `visual.estilo`.

**Sí:** ejemplos con precios, plazos, piezas, nombres reales · frases cortas si el ritmo es corto.
**No:** tríos de adjetivos con ritmo · «no es solo X, es Y» · humor sin límite definido.

Siguiente: `tokens` si la marca va a un producto digital; si no, `laminas`.
