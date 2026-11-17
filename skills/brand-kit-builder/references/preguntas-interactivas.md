# Preguntas interactivas (cómo preguntan las skills)

Cuando el entorno lo permite, las preguntas **cerradas** se hacen con la herramienta nativa de preguntas con opciones: la persona elige con el teclado o el ratón en vez de escribir. En Claude Code esa herramienta se llama `AskUserQuestion`. Si el entorno tiene otra equivalente, úsala igual (en Google Antigravity, según `AGENTS.md`, es `ask_question`). Si no hay ninguna (modo no interactivo, otro agente o una superficie sin diálogos), pasa a la **alternativa en el chat** de más abajo. Esta convención no cambia qué se pregunta ni el orden: solo cómo.

## Qué va en diálogo y qué no

| En diálogo (cerradas) | En el chat (abiertas) |
|---|---|
| Elegir entre territorios, logo A o B, tono (serio, divertido, tecnológico) | Qué hace el negocio, a quién, por qué existe |
| Mockups: sí / no / al ver el logo · ¿web o app? · soporte principal | **Qué nunca debe parecer la marca** |
| Confirmar un resumen o una lectura: «es correcto» / «hay que ajustar» | Qué le gusta de una referencia (el atributo) |
| Aprobar un paso y pasar al siguiente · tipo de referencia (sí / no / otra) · **proveedor de imagen** (Canva / otro de pago / Gemini o Flow gratis / ninguno) | Cualquier ajuste: «qué cambia exactamente» |

Regla práctica: si hay 2 a 4 respuestas razonables, diálogo; si la respuesta es una frase propia, chat. Una pregunta abierta forzada a opciones empobrece la respuesta, y la entrevista depende de respuestas ricas.

## Reglas del diálogo

1. **Hasta 4 preguntas por diálogo** y de 2 a 4 opciones cada una. No añadas «Otro»: la herramienta ya deja escribir otra respuesta.
2. **Cada pregunta se entiende sola.** Quien responde puede ver solo el diálogo: di de qué pieza o decisión hablas y nombra las opciones por lo que son, no «la de antes».
3. **Etiqueta corta** (1 a 5 palabras) y una descripción con **la consecuencia** de elegirla.
4. **Recomendación solo si la tienes y puedes justificarla:** ponla primera y añade «(Recomendada)». Si no hay motivo, no recomiendes.
5. **Selección múltiple** solo si las opciones no se excluyen.
6. **Las imágenes no caben en el diálogo.** Enseña primero las opciones (los dos logos, los territorios) y después pregunta cuál. Nunca preguntes por algo que la persona aún no ha visto.
7. **No uses el diálogo para pedir permiso de seguir** («¿procedo?»). Pregunta para decidir, no para avanzar sin más.
8. **Mantén las tres rondas de la entrevista:** cada ronda sigue siendo un solo turno. Dentro de la ronda, lo abierto va en el chat y lo cerrado en un único diálogo.

## Alternativa en el chat (sin herramienta de diálogo)

Mismas preguntas, en un solo mensaje, con opciones numeradas y la opción de contestar otra cosa:

```
¿Incluimos mockups?
  1) Sí, desde el principio
  2) No
  3) Decido cuando vea el logo
(o escribe otra cosa)
```

Las reglas 2 a 7 se mantienen. Una pregunta por línea, y no mezcles cerradas y abiertas en la misma frase.

## Qué decir si no hay herramienta

Una vez, sin dramatizar: «Voy a preguntarte con opciones numeradas». No lo repitas en cada paso.
