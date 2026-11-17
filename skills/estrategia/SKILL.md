---
name: estrategia
description: "Ayuda a explorar una marca con buenas preguntas en 2 o 3 rondas, devolviendo un espejo después de cada una, y termina con un brief estratégico y tres vías generales de actitud y promesa (sin recomendaciones visuales: ni colores, ni logos, ni tipografías). Úsala al empezar una marca o con «no sé cómo posicionarme», «qué me hace distinto», «qué personalidad tiene mi marca», «ayúdame a pensar mi marca»."
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Estrategia: explorar la marca con buenas preguntas

El producto de este paso es **la conversación**: que la persona salga sabiendo cosas de su marca que no sabía al entrar. No se genera ninguna imagen y **no se hacen recomendaciones visuales**: ni colores, ni logos, ni tipografías, ni estilos, ni prompts. Lo único «visual» que se permite es **la sensación general de cada una de las tres vías** del final, dicha con una palabra de registro (sobria, cálida, atrevida…), nunca con elementos concretos.

Lee antes: `../brand-kit-builder/references/criterio-experto.md`, `references/entrevista.md` (el banco de preguntas y cómo escuchar) y `references/vias.md` (cómo construir las tres vías). La plantilla del brief está en `references/brief-estrategico.md`; el léxico de relleno, en `../identidad/references/lexico-prohibido.md`.

## Cómo es la conversación

- **Cada ronda es UN diálogo nativo** (`AskUserQuestion`; en Antigravity, `ask_question`), con 3 o 4 preguntas y de 2 a 4 respuestas típicas por pregunta; la persona escribe lo suyo en «Other». **No hagas las preguntas en texto del chat** salvo que no haya herramienta de diálogo (`../brand-kit-builder/references/preguntas-interactivas.md`).
- **Sé breve, ahorra tokens:** sin preámbulos ni explicaciones del método; pregunta de una línea; el porqué, en menos de 12 palabras y solo si hace falta; espejo de máximo 5 líneas; nada de relleno entre diálogos.

- **Dos o tres rondas.** Cada ronda es **un solo mensaje** tuyo, **de tú**, con **3 o 4 preguntas numeradas, nunca más** (la pregunta cerrada también cuenta). **Cada pregunta es UNA sola, con un solo signo de interrogación**: si te salen dos en la misma, es otra pregunta, y la quitas o la dejas para la siguiente ronda. Mejor pocas y buenas que muchas: la persona tiene que poder contestarlas de una sentada.
- **Preguntas buenas, no un formulario:** abiertas, concretas y sobre **situaciones reales** («cuéntame el último cliente que casi no te compró»), nunca abstracciones («¿cuál es tu propuesta de valor?»). Cada pregunta lleva, en una línea, **por qué la haces** (la persona aprende a pensar su marca mientras contesta). Si la pregunta es difícil, da **dos ejemplos de respuesta contrapuestos** para que no copie uno.
- **Entre rondas, un espejo** (ver abajo). Es lo que más ayuda: devolver lo que has oído, señalar lo que chirría y decir lo que aún no sabes.
- **No repreguntes lo que ya contó.** Si el primer mensaje ya responde algo, lo das por recogido y subes el nivel de la pregunta.
- **Si una respuesta es vaga** («moderna, cercana, profesional»), pide **una escena o un ejemplo**, una sola vez. No es un interrogatorio.
- Las preguntas **cerradas** (elegir entre opciones, confirmar un resumen, escoger una vía) van en un diálogo con opciones (y cuentan dentro de las 3 o 4); las **abiertas**, en el chat. Reglas en `../brand-kit-builder/references/preguntas-interactivas.md`.
- **El nombre**: si no lo ha dado, pregúntalo en la ronda 1 (y cómo se pronuncia, y por qué ese). **Nunca lo inventes.** Si lo delega, propón tres con su razón y deja que elija. Si tienes búsqueda web, comprueba el nombre y di lo que encuentres como pendiente de validación profesional (OEPM, EUIPO), no como asesoría legal.
- **Si tienes búsqueda web**, antes de la ronda 2 mira 3 o 4 alternativas del sector **para preguntar mejor** (qué prometen, cómo hablan). No vuelques la investigación a la persona: úsala para afinar preguntas y, después, el mapa del brief. Sin búsqueda, usa lo que sabes y dilo; nunca inventes datos de mercado.

## Las rondas

1. **Ronda 1, qué haces y para quién, en la vida real.** Un cliente concreto, qué hacía antes, qué cambia cuando funciona, por qué lo haces tú, el nombre.
2. **Ronda 2, tu diferencia y tus fronteras.** Por qué te elegirían, lo que no soportas del sector, lo que nunca harías, lo que puedes demostrar hoy y lo que te gustaría poder decir.
3. **Ronda 3, cómo se comporta la marca.** Una persona entrando en una reunión, una marca cuya **actitud** (no su aspecto) admira, una que no querría parecer, cómo debe sentirse el cliente después.

Si tras la ronda 2 ya hay material de sobra, haz la ronda 3 más corta o únela con el cierre; **no pases de tres rondas**. Las preguntas exactas, con su porqué y sus repreguntas, están en `references/entrevista.md`.

## El espejo (después de cada ronda)

Antes de preguntar de nuevo, escribe en pocas líneas:
- **Lo que oigo:** dos o tres ideas con sus palabras, no con las tuyas.
- **Lo que me llama la atención:** una contradicción, un hueco o algo que repite («dices que es accesible pero describes un servicio de lujo»). Nómbralo con respeto, es lo que más hace pensar.
- **Lo que aún no sé:** lo que vas a preguntar a continuación y por qué.
No des soluciones ni recomendaciones en el espejo: solo ayuda a ver.

## El cierre: tres vías generales

Con lo que tienes, escribe **tres vías** (`references/vias.md`): formas **generales** de ser esa marca, que se separan por **actitud y promesa**, no por estética. Cada una con: idea, a quién habla y qué promete, cómo suena (comportamiento al hablar), sensación general (una palabra de registro), riesgo, y «encaja si…». Recomienda una y di por qué. **Enséñale las tres vías en el chat y espera a que elija** (una o una mezcla de dos, con un diálogo): no elijas por ella. Si no contesta, deja «Vía elegida: pendiente» y la idea rectora provisional. Cuando elija, escribe la **idea rectora** en una frase.

**No des nada más visual que eso.** Si te piden colores, logo o tipografía, di que esta fase es para tener claro qué es la marca y que eso viene después; ofrécelo como siguiente paso (`identidad` o `brief-logo`), no lo hagas ahora.

## Lo que dejas escrito

`trabajo/<fecha>-marca-<slug>/estrategia.md`, con la plantilla de `references/brief-estrategico.md`. Compruébalo antes de dárselo:

```
python3 skills/estrategia/tools/verificar_brief.py trabajo/<fecha>-marca-<slug>/estrategia.md
```

No lo presentes hasta que salga «BRIEF CORRECTO». A la persona, enséñale un resumen de 8 líneas (qué descubrimos, la tensión, las tres vías con la elegida y **lo que aún no sabe**) y las rutas, no el documento pegado. Termina con **qué hacer esta semana** para resolver lo que falta saber (por ejemplo, hablar con tres clientes).

Señales de alarma que dices en voz alta: nombre descriptivo y común (difícil de registrar) · promesa con un claim regulado («natural», «sostenible», «de especialidad») · una promesa sin prueba · referencia de otra categoría y otro precio · dos cosas que no caben a la vez («exclusiva» y «para todos»).

Si la persona pide **referencias** o dice que no sabe dónde buscarlas, dale solo **las 3 palabras clave generales** para Behance, Pinterest y Dribbble, deducidas del brief (`../gusto/references/palabras-clave.md`); más, solo si las pide. Siguiente, **solo si la persona lo pide**: `identidad` (logo, paleta, tipografía) o `brief-logo` (brief y prompts para explorar logos con IA).
