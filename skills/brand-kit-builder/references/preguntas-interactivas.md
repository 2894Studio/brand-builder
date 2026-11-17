# Preguntas interactivas (cómo preguntan las skills)

Cuando el entorno lo permite, las preguntas **cerradas** se hacen con la herramienta nativa de preguntas con opciones: la persona elige con el teclado o el ratón en vez de escribir. En Claude Code esa herramienta se llama `AskUserQuestion`. Si el entorno tiene otra equivalente, úsala igual (en Google Antigravity, según `AGENTS.md`, es `ask_question`). Si no hay ninguna (modo no interactivo, otro agente o una superficie sin diálogos), pasa a la **alternativa en el chat** de más abajo. Esta convención no cambia qué se pregunta ni el orden: solo cómo.

## Qué va en diálogo y qué va abierto

- **Ronda 1: abierta, en el chat.** Una sola petición para que la persona cuente con sus palabras. Aquí no se dan opciones.
- **Rondas 2 y 3: diálogo nativo** (3 o 4 preguntas, 2 a 4 opciones). **Las opciones se construyen con lo que la persona ya contó**, no con respuestas de catálogo; así hacen de ejemplos y la persona escribe lo suyo con «Other» cuando ninguna encaja.
- **Elegir una vía** y confirmar un resumen: diálogo.
- Si una respuesta sale delgada (una etiqueta), **una pregunta abierta corta** en el chat antes de seguir.
- Solo cuando no haya herramienta de diálogo se usa la alternativa en el chat (abajo).

## Brevedad (ahorrar tokens)

- **Nada de preámbulos**: ni «voy a empezar con…», ni explicar el método, ni repetir lo que la persona ya dijo.
- **La pregunta, corta** (una línea) y entendible sola. El porqué, solo si no es obvio y en **una frase de menos de 12 palabras**, dentro de la descripción de las opciones o del encabezado, no en un párrafo.
- **El espejo**: máximo 5 líneas (lo que oigo, lo que chirría, lo que falta), sin repetir sus palabras enteras.
- Entre diálogos, **cero texto de relleno**: el espejo y la siguiente ronda. Nada de «¡genial!» ni resúmenes de lo que vas a hacer.
- Si una respuesta ya cubre varias preguntas de la siguiente ronda, **quítalas**.

## Reglas del diálogo

1. **Hasta 4 preguntas por diálogo** y de 2 a 4 opciones cada una. No añadas «Otro»: la herramienta ya deja escribir otra respuesta ("Other").
2. **Cada pregunta se entiende sola.** Quien responde puede ver solo el diálogo: di de qué pieza o decisión hablas y nombra las opciones por lo que son, no «la de antes».
3. **Etiqueta corta** (1 a 5 palabras) y una descripción con **la consecuencia** de elegirla.
4. **Recomendación solo si la tienes y puedes justificarla:** ponla primera y añade «(Recomendada)». Si no hay motivo, no recomiendes.
5. **Selección múltiple** solo si las opciones no se excluyen.
6. **Nunca preguntes por algo que la persona aún no ha visto**: enseña primero las opciones (las tres vías) y después pregunta cuál.
7. **No uses el diálogo para pedir permiso de seguir** («¿procedo?»). Pregunta para decidir, no para avanzar sin más.
8. **Mantén las rondas de la entrevista:** cada ronda es un solo diálogo de 3 o 4 preguntas.

## Alternativa en el chat (sin herramienta de diálogo)

Mismas preguntas, en un solo mensaje, con opciones numeradas y la opción de contestar otra cosa:

```
¿Con qué vía te quedas?
  1) A
  2) B
  3) C
(o escribe otra cosa)
```

Las reglas 2 a 7 se mantienen. Una pregunta por línea, y no mezcles cerradas y abiertas en la misma frase.

## Qué decir si no hay herramienta

Una vez, sin dramatizar: «Voy a preguntarte con opciones numeradas». No lo repitas en cada paso.
