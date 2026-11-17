---
name: estrategia
description: "Estrategia de marca como la haría un director: investiga la categoría, propone una hipótesis completa (público, tensión, posicionamiento, personalidad, lo que nunca debe parecer), la contrasta con la persona en una o dos rondas, escribe un brief estratégico verificable y deriva tres territorios y una idea rectora. Úsala al empezar una marca o con «no sé cómo posicionarme», «qué me hace distinto», «qué personalidad tiene mi marca». Termina con estrategia.md y un borrador de marca.json."
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Estrategia

Antes de dibujar nada se decide qué es la marca y por qué ganaría. Aquí no se genera ninguna imagen y no cuesta nada: es donde se ahorra lo que se gastaría después.

**Tú pones el criterio. La persona pone los hechos.** No es una entrevista de formulario: llegas con una hipótesis, la enseñas y la persona la corrige. Lee ahora, en este orden:
1. `../brand-kit-builder/references/criterio-experto.md` (los nueve hábitos y las cinco pruebas; es lo que separa un brief de un formulario relleno).
2. `references/brief-estrategico.md` (la plantilla que vas a producir).
3. `references/posicionamiento.md` y `../identidad/references/lexico-prohibido.md`.
`references/entrevista.md` y `references/referencias.md` los consultas cuando toquen.

Si la marca ya existe y solo hay que documentarla, salta los territorios y completa el brief con lo que hay.

## 1. Lee la petición y la categoría (sin preguntar nada todavía)

1. Del mensaje de la persona saca todo lo que ya dijo: qué es, para quién, tono, nombre. **Lo que ya contó no se vuelve a preguntar.**
2. **Investiga** (si tienes búsqueda web): de 4 a 6 competidores o alternativas, incluida al menos una que no se parezca pero resuelva lo mismo; qué promete cada uno, cuánto cuesta, y qué convención visual y verbal repite. Sin búsqueda, usa lo que sabes y dilo («no he podido comprobarlo»). **Nunca inventes datos de mercado.**
3. **Comprueba el nombre** ahora, antes de dibujar: si existe una empresa con ese nombre en el sector, díselo. Dilo como pendiente de validación profesional (OEPM, EUIPO), no como asesoría legal.
4. Escribe para ti la **tensión**: qué quiere el cliente frente a qué le da hoy la categoría.

## 2. Una hipótesis, no quince preguntas

Un solo mensaje, **de tú**, con este orden:
1. «Esto es lo que entiendo» (3 líneas con lo que ya sabes) y **tu hipótesis**: público que decide, tensión, posicionamiento tentativo, tres rasgos de personalidad y **tres cosas que nunca debe parecer** (propón pares opuestos y que elija de qué lado no quiere estar). Con tus razones en una línea cada una.
2. Un diálogo cerrado: «¿Voy bien?» (voy bien / ajusta esto / el enfoque es otro). Si ajusta, pregunta **qué** en el chat.
3. **Como mucho tres preguntas** que solo la persona puede responder y que cambian el resultado: el dato o la prueba que puede demostrar, el precio o el rango real, una restricción (símbolo obligatorio, color fijo, canal principal). Cada pregunta lleva tu respuesta recomendada por defecto.
4. Una vez, con un diálogo, cuatro cuestiones de producción (no de estrategia): **alcance** (por defecto, brief de logo y prompts; alternativa, el kit completo), **mockups** (sí / no / al ver el logo), si la marca necesita **web o app**, y **el trato** (tutea o usted).

Máximo **dos rondas**. Si la persona dice «decide tú», «no sé» o no contesta, decides, lo marcas como *Supuesto* en el brief y sigues. Un resumen confirmado cierra la fase: pídelo con un diálogo («es correcto» / «hay que ajustar») y **no avances sin él**.

Referencias, versión corta (3 minutos): pide **tres** (2 que le gustan, 1 que no quiere parecer) y **qué atributo** de cada una; guárdalas en `marca.json` → `referencias` con `tipo` `"si"` o `"no"`. No inventes el atributo. El entrenamiento completo va en `gusto`. Método en `references/referencias.md`.

## 3. Escribe el brief

Crea `trabajo/<fecha>-marca-<slug>/estrategia.md` con la plantilla de `references/brief-estrategico.md` y ejecútale:

```
python3 skills/estrategia/tools/verificar_brief.py trabajo/<fecha>-marca-<slug>/estrategia.md
```

No lo enseñes hasta que salga «BRIEF CORRECTO». Después, aplica tú las **cinco pruebas** a tu propio brief y arregla lo que falle (sobre todo la del competidor). Enséñaselo a la persona en un resumen de 8 líneas, no pegando el documento entero.

## 4. Tres territorios derivados del brief

Cada territorio responde a la misma pregunta: **cómo rompemos la convención que elegimos romper**. Tres, en media página cada uno: nombre, idea central, **por qué ganaría y por qué podría fallar**, tipo de logo propuesto, paleta tentativa con hex, registro tipográfico y una frase con su voz. Cada uno **anclado fuera de la categoría** (tensión narrativa, sistema natural, concepto cultural u oficio ajeno): `references/anclajes-y-manifiesto.md`. Un territorio anclado en la competencia devuelve la media del sector, que es lo que delata a una marca generada.

Indica a qué firma gráfica apunta cada territorio (`artesanal`, `editorial`, `tecnologico`, `natural`, `cercano`). Recomienda uno y di por qué; la persona elige uno o mezcla dos con un diálogo.

## 5. Manifiesto e idea rectora

Con el territorio elegido: el manifiesto en primera persona (estructura en `references/anclajes-y-manifiesto.md`; **el miedo de la marca es obligatorio**) y la **idea rectora** en una frase. Anótalos en `estrategia.md` y vuelve a ejecutar el verificador.

## Qué dejas escrito

- `trabajo/<fecha>-marca-<slug>/estrategia.md`: el brief completo, el territorio elegido y el manifiesto. **Es el documento contra el que se defiende todo lo demás.**
- Un **borrador** de `marca.json` en la raíz con `nombre`, `categoria`, `tono`, `idioma`, `publico`, `competidores` y `brandKit.territorio`. Parte de `../tokens/marca.plantilla.json`.

Señales de alarma que dices en voz alta: nombre descriptivo y común (difícil de registrar) · símbolo obligatorio que es el tópico de la categoría · promesa con un claim regulado («de especialidad», «natural», «sostenible») · referencia de otra categoría y otro precio · una promesa sin prueba.

Siguiente: `gusto` (referencias) y después `brief-logo` (el resultado por defecto: brief de logo y prompts). Si la persona pidió la marca completa, `identidad`.
