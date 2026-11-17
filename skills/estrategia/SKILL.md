---
name: estrategia
description: "Ayuda a explorar una marca con buenas preguntas en 3 rondas (la primera abierta, para que la persona cuente con sus palabras), devuelve un espejo tras cada ronda, escribe un brief estratégico con tres vías generales de actitud y promesa y termina con tres palabras clave para buscar referencias en Behance, Pinterest y Dribbble. Sin recomendaciones visuales. Úsala con «quiero crear una marca», «ayúdame con mi marca», «no sé cómo posicionarme»."
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Estrategia: explorar la marca con buenas preguntas

El producto es **la conversación**: que la persona salga sabiendo de su marca cosas que no sabía al entrar. No hay recomendaciones visuales: ni colores, ni logos, ni tipografías, ni estilos, ni prompts. Lo único «visual» permitido es la **sensación general** de cada una de las tres vías del cierre, con una palabra de registro (sobria, cálida, atrevida…).

Lee antes: `../brand-kit-builder/references/criterio-experto.md`, `references/entrevista.md` (qué preguntar y cómo escuchar), `references/vias.md`, `references/palabras-clave.md`, `references/brief-estrategico.md` (la plantilla) y `references/lexico-prohibido.md`.

## Reglas de la conversación

- **3 rondas, no más.** Cada una es un solo mensaje tuyo, de tú.
- **Ronda 1 abierta; rondas 2 y 3 en diálogo nativo** (`AskUserQuestion`; en Antigravity, `ask_question`) con **3 o 4 preguntas** y 2 a 4 opciones cada una. Las opciones **se construyen con lo que la persona ya contó** (sus palabras, sus alternativas, sus dudas), **nunca respuestas genéricas de catálogo**. «Other» siempre queda para ampliar. Sin herramienta de diálogo: opciones numeradas en el chat (`../brand-kit-builder/references/preguntas-interactivas.md`).
- **Una pregunta, un solo signo de interrogación, una idea.** El porqué, solo si no es obvio y en menos de 12 palabras.
- **Si una respuesta sale delgada** (una etiqueta, una palabra), haz **una** pregunta abierta corta para que cuente más («¿qué pasó exactamente?») antes de seguir. Es mejor una escena que cuatro etiquetas.
- **Breve, para ahorrar tokens:** sin preámbulos, sin explicar el método, sin relleno entre mensajes.
- **No repreguntes lo que ya contó.** Si la ronda 1 ya responde algo, sube el nivel.
- **El nombre:** si no lo ha dado, se pregunta en la ronda 1; **nunca lo inventes**. Si lo delega, propón tres con su razón. Con búsqueda web, compruébalo y dilo como pendiente de validación profesional (OEPM, EUIPO).
- **Búsqueda web** (si la tienes): antes de la ronda 2 mira 3 o 4 alternativas del sector para **preguntar mejor** (qué prometen, cómo hablan). Sin búsqueda, di que no has comprobado el mercado. No inventes datos.

## Las tres rondas

1. **Ronda 1, abierta.** Una sola petición, en el chat: «Cuéntame con tus palabras qué haces, para quién y una escena real de un cliente (o inventado), y por qué lo haces tú». Si no ha dado el nombre, añádelo al final. Nada de opciones: aquí se necesita su voz. Después, el **espejo**.
2. **Ronda 2, diálogo: diferencia y fronteras.** Con las alternativas que nombró y lo que le irrita, pregunta: qué le haría ganar frente a esa alternativa, qué demuestra hoy, qué no haría nunca y dónde se coloca (accesible o exclusiva). Opciones hechas con sus datos. Después, el **espejo**.
3. **Ronda 3, diálogo: cómo se comporta la marca.** Como persona en una reunión, con qué marca no quiere que la confundan, cómo quiere que se sienta el cliente. Opciones hechas con sus datos y, si hace falta, **una pregunta abierta final** («¿qué se me escapa que debería saber?»).

Si tras la ronda 2 hay material de sobra, acorta la 3. Preguntas, repreguntas y cómo escuchar: `references/entrevista.md`.

## El espejo (después de cada ronda, máximo 5 líneas)

- **Lo que oigo:** dos o tres ideas con sus palabras.
- **Lo que me llama la atención:** una contradicción o un hueco («dices cercana, pero describes rigor»). Es lo que más hace pensar.
- **Lo que aún no sé:** lo que preguntarás a continuación.
Sin soluciones ni recomendaciones.

## El cierre: tres vías generales

Con lo que tienes, escribe **tres vías** (`references/vias.md`): formas generales de ser esa marca, separadas por **actitud y promesa**, no por estética. Cada una con idea, a quién habla y qué promete, cómo suena, sensación general (una palabra), riesgo y «encaja si». Recomienda una y di por qué. **Enséñalas y espera a que la persona elija** (una, o una mezcla de dos) con un diálogo: no elijas por ella. Si no contesta, «Vía elegida: pendiente». Después, la **idea rectora** en una frase.

## Lo que dejas escrito

`trabajo/<fecha>-marca-<slug>/estrategia.md`, con la plantilla de `references/brief-estrategico.md`. Compruébalo:

```
python3 skills/estrategia/tools/verificar_brief.py trabajo/<fecha>-marca-<slug>/estrategia.md
```

No lo presentes hasta que salga «BRIEF CORRECTO».

## El final: las palabras clave

Lo último. Del brief deduce **las 3 palabras clave generales** que sirven igual en Behance, Pinterest y Dribbble (`references/palabras-clave.md`), ponlas en la sección «Palabras clave para buscar referencias» y dáselas. Más búsquedas, solo si las pide. Dile que guarde **3 referencias** (2 que le gustan y 1 que no quiere parecer) y apunte **qué actitud** le gusta de cada una.

## Cómo cierras

A la persona, **8 líneas como máximo**: qué descubrimos, la tensión, la vía elegida y la idea rectora, lo que aún no sabe (con qué hacer esta semana), las 3 palabras clave y la ruta del archivo. No pegues el documento. Con eso **termina el plugin**: no ofrezcas más pasos. Si pide colores, logo o tipografía, di que queda fuera de este plugin.

Señales de alarma que dices en voz alta: nombre descriptivo y común · claim regulado («natural», «sostenible») · promesa sin prueba · referencia de otra categoría y otro precio · dos cosas que no caben juntas («exclusiva» y «para todos»).
