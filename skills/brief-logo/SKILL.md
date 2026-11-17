---
name: brief-logo
description: "Paso opcional, solo si la persona lo pide después de la estrategia: un brief de logo sólido y prompts listos para explorar opciones de logo con IA (modelos de imagen como Ideogram, Recraft, Midjourney, GPT Image, Flux, y Claude o Claude Design en SVG). Úsala con «dame el brief de logo», «un prompt para crear mi logo con IA», «quiero explorar opciones de logo». Parte del brief estratégico y deja brief-logo.md y prompts-logo.md."
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Brief de logo y prompts para explorarlo con IA

**Este paso es opcional y posterior a `estrategia`: no se ofrece ni se hace hasta que la persona tenga clara su marca y pida el logo.** Su objetivo no es dibujar el logo: es darle a la persona **un brief tan bueno que cualquier modelo de diseño produzca opciones útiles**, y los prompts para pegar. Un logo genérico casi siempre viene de un brief genérico.

Requiere `trabajo/<fecha>-marca-<slug>/estrategia.md` verificado (`estrategia`). Sin él, vuelve allí: un brief de logo sobre un brief estratégico flojo sale flojo. Lee `../brand-kit-builder/references/criterio-experto.md`, `../identidad/references/logo.md` y `references/direcciones.md`.

## 1. Aprende de lo que ya hay

- La **idea rectora**, la tensión, la personalidad y el «No es» de `estrategia.md`. Todo logo se defiende contra ellos.
- Si hay `gusto.json`, las reglas que tocan al logo (nombre, símbolo, tipografía, forma, color) y lo que hay que **evitar**. Se incluyen solas en el brief.
- Si la persona dio referencias de logo, qué atributo le gusta de cada una.

## 2. Piensa tres direcciones (tú, no la persona)

Lee `references/direcciones.md`. Tres direcciones que se diferencien en el **tipo** de marca (wordmark, símbolo + nombre, emblema, monograma, abstracto, pictórico), no en el acabado. Cada una con: la **idea** (qué concepto expresa), **por qué** (apunta a la idea rectora), la **forma** (descripción visual concreta, construible con geometría), el **riesgo** (qué puede fallar, normalmente la reducción) y un **prompt en inglés**. Más: los **tópicos de la categoría que no se usan** (mínimo 3, también en inglés), las **restricciones** duras y los colores tentativos si los hay.

## 3. Escribe `brief-logo.json` y ensámblalo

```
python3 skills/brief-logo/tools/brief_logo.py --ejemplo > trabajo/<…>/brief-logo.json     # formato; edítalo con tu brief
python3 skills/brief-logo/tools/brief_logo.py trabajo/<…>/brief-logo.json
```

El script se niega si `estrategia.md` no pasa su verificador, si no hay exactamente tres direcciones, si no se diferencian en el tipo, si algo es de relleno o si falta el inglés. Deja `brief-logo.md` (para leer y aprobar) y `prompts-logo.md` (modelos de imagen, Claude en SVG, refinamiento). **Lee el resultado antes de entregarlo:** si una dirección podría ser el logo de cualquier competidor, rehaz la dirección.

## 4. Entrega

Enséñale a la persona, en este orden: el **brief de logo** resumido (idea rectora, las tres direcciones en una línea cada una, lo que no puede parecer), cuál **recomiendas** y por qué, y las **rutas** de los dos archivos. Dile cómo usarlos (`references/plataformas.md`): empezar por el prompt B (Claude, tablero SVG), usar los A para explorar ideas con modelos de imagen, y refinar de a un cambio con el C. Con un diálogo, pregunta si el brief es correcto o hay que ajustar una dirección.

**Sé honesto con lo que no se puede garantizar:** las imágenes generadas fallan con las letras; el logo definitivo se reconstruye en vector; las anterioridades del nombre y del símbolo (OEPM, EUIPO) son pendiente de validación profesional.

Si la persona quiere seguir con el kit completo (paleta con contraste, manual, bento y posts), la cadena sigue en `identidad`.
