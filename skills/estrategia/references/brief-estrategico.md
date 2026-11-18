# El brief estratégico (`estrategia.md`)

Es el entregable de la fase y **está escrito en primera persona, como las instrucciones de un proyecto de Claude**: se puede pegar tal cual en las instrucciones de un proyecto (Claude Projects, ChatGPT Projects, cualquier IA) para que trabaje con la marca. Una página o poco más, sin relleno y **sin recomendaciones visuales**. `python3 skills/estrategia/tools/verificar_brief.py estrategia.md` lo comprueba antes de enseñarlo.

## Plantilla (los títulos tienen que estar tal cual)

```markdown
# Brief estratégico: <nombre>

## Quién soy y qué hago
Soy …, que … Qué es, qué vendo (o quiero vender), a quién y en qué etapa estoy: idea, ya vendo o replanteo (2 a 4 líneas, hechos y con mis palabras).

## Mi audiencia y su tensión
Quién es la persona que decide (o decidirá), qué quiere y qué le da hoy la categoría. Una situación real si la conté. Si aún no hay clientes, lo digo y describo a quien imagino.
**Tensión:** «<lo que quiere> pero <lo que la categoría le da>» (una frase con las dos mitades).

## Mi categoría y mis alternativas
| Alternativa | Qué promete | Cómo habla |
|---|---|---|
| … | … | … |
(mínimo 3; marca cada fila: *directa* si resuelve lo mismo, *otra solución* si resuelve el mismo problema de otra forma, *hábito* si es hacerlo uno mismo o no hacer nada)
**Lo que todas dicen o hacen:** … **Lo que haré distinto (solo una cosa):** …

## Por qué me elegiría y qué le frena
Las cuatro fuerzas de por qué alguien cambia (una línea cada una, con lo que dije):
- **Lo que le empuja:** qué le frustra de lo que usa hoy.
- **Lo que le atrae de mi marca:** qué ve en mí que no ve en lo de ahora.
- **Lo que le frena (hábito):** qué le mantiene con lo de siempre.
- **Lo que le da miedo (ansiedad):** qué teme de cambiar.

## Cómo habla mi cliente
- Frases literales con las que describe su problema: «…», «…» (del cliente, de alguien con quien hablé o de reseñas y foros con su fuente; si son mías, lo digo; si aún no hay ninguna, dos como *Supuesto*)
- **Palabras que usar:** … **Palabras que evitar:** …

## Mi posicionamiento
Para **<público>** que **<necesidad o momento>**, **<marca>** es **<categoría reconocible>** que **<beneficio>**, porque **<razón creíble: un hecho>**.

## Mi promesa y mi prueba
La promesa en una frase y lo que la sostiene hoy (proceso, cifra, caso, experiencia). Si aún es una idea, qué me da credibilidad y qué todavía no puedo probar.

## Mi personalidad y mi voz
Tres rasgos con comportamiento («soy la ingeniera senior que…», no «soy innovadora»). Arquetipo dominante y su riesgo.

## Lo que mi marca no es
- Qué nunca debe parecer ni sonar (mínimo 3), con el motivo de cada uno, en actitud y en lo que dice.

## Mis objeciones y a quién no sirvo
- «…» → cómo respondo con un hecho.
- «…» → …
**A quién no sirvo:** quién no es buen cliente y por qué.

## Mis tres vías
(Plantilla y reglas en `vias.md`: tres subsecciones `### Vía A/B/C`, con idea, a quién habla y qué promete, cómo suena, sensación general, riesgo y «encaja si». Sin colores, logos ni tipografías.)
**Recomendada:** … porque …

## Mi vía elegida
La que elegí (o la mezcla), o «pendiente» con lo que falta para decidir.

## Mis pilares de mensaje
De 3 a 5 temas de los que hablará mi marca, cada uno ligado a un dolor, una objeción o una prueba (como los «pilares de contenido»: de qué se habla y por qué).
- **Tema:** …, porque …

## Mi idea rectora
Una sola frase (máximo 25 palabras) que resuma la vía elegida y de la que se deduzca el resto.

## Lo que aún no sé
Tres o más cosas que faltan por descubrir, cada una con **cómo averiguarla esta semana** (hablar con tres personas, probar la frase con alguien del sector, conseguir un dato).

## Palabras clave para buscar referencias
Las 3 generales, en una línea cada una (`palabras-clave.md`): sector + `brand identity`, cliente + producto, actitud de la vía + `branding`.
- `…`
- `…`
- `…`
Guardar 3 referencias (2 que me gustan y 1 que no quiero parecer), con la actitud de cada una.

## Qué buscar y qué evitar en las referencias
(El único lugar con aspectos visuales, en general y con «porque»; ver `palabras-clave.md`.)
**Buscar:**
- …, porque …
- …, porque …
- …, porque …
**Evitar:**
- …, porque …
- …, porque …
- …, porque …

## Riesgos y pendientes
Nombre (anterioridades pendientes de validación), claims, lo que no puedo prometer, *Supuestos* que hizo el agente sin mi confirmación.
```

## Reglas de calidad

- **Primera persona, la de la propia persona** («soy», «mi audiencia», «mi marca»): el brief se pega tal cual como instrucciones de proyecto. Las frases de otros (clientes, reseñas) van entre comillas y con su fuente.
- **Las frases del cliente van literales**, entre comillas, tal como se las contaron; no las pules. Si son de la propia persona, se dice.
- **Hechos y palabras de la persona, no adjetivos.** «Cada candidato habla antes con un ingeniero» es un hecho; «profesionales de calidad» no.
- **Ninguna frase vale para un competidor** cambiando el nombre.
- **Sin léxico prohibido** (`lexico-prohibido.md`): el verificador lo cuenta.
- **El posicionamiento sigue la fórmula**, completa, con las cuatro partes en negrita. Si falta la razón para creerlo, es un hueco que se dice, no se rellena con un adjetivo.
- **La tensión tiene dos mitades.**
- **Los supuestos se marcan** como *Supuesto* para que la persona los corrija.
- **Nada visual** en las vías, la idea rectora, el posicionamiento ni la personalidad: ni colores, ni logos, ni tipografías, ni estilos, ni prompts. Lo visual solo aparece, en general y con «porque», en «Qué buscar y qué evitar en las referencias».
