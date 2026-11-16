---
name: estrategia
description: Entrevista de marca en tres rondas, tres territorios anclados fuera de la categoría y manifiesto en primera persona. Úsala al empezar una marca o cuando alguien diga «no sé cómo posicionarme», «qué me hace distinto», «qué personalidad tiene mi marca», «no sé qué quiero transmitir». Termina con un borrador de marca.json.
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Estrategia

Antes de dibujar nada se decide qué es la marca. Aquí no se genera ninguna imagen y no cuesta nada: es donde se ahorra todo lo que se gastaría después.

Lee ahora `references/referencias.md` (cómo entrenar el gusto), `references/entrevista.md` (banco de preguntas y cómo leer las respuestas) y `references/posicionamiento.md` (jerarquía de decisiones, posicionamiento, arquetipos). Lee `../identidad/references/lexico-prohibido.md`: decide cómo escribes durante todo el proceso.

Si la marca ya existe y solo hay que documentarla, salta los territorios y usa las respuestas para completar `marca.json`.

## 1. Entrevista: tres rondas, no treinta preguntas

Un solo mensaje por ronda, **de tú** y sin adelantar soluciones (nada de «lo normal sería un logo tipográfico» antes de cerrar la entrevista). Ofrece opciones cuando la herramienta lo permita; la persona siempre puede escribir otra cosa.

- **Ronda 1, qué es:** nombre · qué vende · a quién · promesa en una frase · categoría y si quiere sentirse accesible o exclusiva.
- **Ronda 2, quién es:** por qué existe · qué la distingue · tres rasgos de personalidad · un adjetivo · **qué nunca debe parecer** (la pregunta que más decisiones ahorra).
- **Ronda 3, dónde vive:** tuteo o usted · territorio geográfico o cultural · símbolo obligatorio · referencias y **qué** le gusta de ellas · soportes principales · **¿incluimos mockups?** (sí / no / al ver el logo) · ¿necesita la marca funcionar en una web o app?

Cierra con un resumen de 3 a 5 líneas y pide confirmación. **No sigas sin ella.**

**Sí:** reconoce lo que ya contó y pregunta solo lo que falta · insiste en el «nunca debe parecer» · si le gusta una referencia, pregunta qué atributo.
**No:** no preguntes por colores ni tipografías (son consecuencia) · no aceptes «moderno, limpio, profesional» sin un ejemplo concreto · no sigas sin saber qué nunca debe parecer.

## 1b. Referencias (5 minutos, antes de los territorios)

Pide **ocho referencias visuales**: 4 que le encantan, 2 que no quiere parecer y 2 de otra categoría. Por cada una, **qué atributo** le gusta o rechaza (la escala del titular, el color que aparece una vez…), nunca solo el nombre. Si falta el atributo, repregunta una vez por referencia y **no lo inventes**. Guárdalas en `marca.json` → `referencias`. Método, ejemplos y ejercicios en `references/referencias.md`. Esto entrena el gusto de la persona y evita que la marca salga como la media.

## 1c. Comprueba el nombre

Si tienes búsqueda web, busca el nombre **ahora**, antes de dibujar un logo: si ya existe una empresa con ese nombre en el sector, díselo en este momento. «Es descriptivo» no basta. Dilo como pendiente de validación profesional, no como asesoría legal.

## 2. Tres territorios (texto, coste cero)

Tres, en media página cada uno: nombre, idea central, tipo de logo propuesto, paleta tentativa con hex, registro tipográfico y una frase escrita con su voz. Cada uno **anclado fuera de la categoría** (tensión narrativa, sistema natural, concepto cultural u oficio ajeno): ver `references/anclajes-y-manifiesto.md`. Un territorio anclado en la competencia devuelve la media del sector, que es lo que delata a una marca generada.

Indica a qué firma gráfica apunta cada territorio (`artesanal`, `editorial`, `tecnologico`, `natural`, `cercano`): se usará en las láminas y en el radio de los componentes.

Pide que elija uno o mezcle dos.

## 3. Manifiesto

Con el territorio elegido, escribe el manifiesto en primera persona antes de dibujar nada (estructura en `references/anclajes-y-manifiesto.md`). **El miedo de la marca es obligatorio**: le da aristas.

## Qué dejas escrito

- `trabajo/<fecha>-marca-<slug>/estrategia.md`: resumen confirmado, posicionamiento en una frase, territorio elegido, manifiesto.
- Un **borrador** de `marca.json` en la raíz con `nombre`, `categoria`, `tono`, `idioma`, `publico`, `competidores` y `brandKit.territorio`. Parte de `../tokens/marca.plantilla.json`. Lo demás se completa en `identidad` y `voz`.

Señales de alarma que hay que decir en voz alta: nombre descriptivo y común (difícil de registrar) · símbolo obligatorio que es el tópico de la categoría · promesa con un claim regulado («de especialidad», «natural», «sostenible») · referencia de otra categoría y otro precio.

Siguiente: `identidad`.
