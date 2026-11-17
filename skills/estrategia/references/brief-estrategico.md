# El brief estratégico (`estrategia.md`)

Es el entregable de la fase. Una página o poco más, sin relleno y **sin recomendaciones visuales**. `python3 skills/estrategia/tools/verificar_brief.py estrategia.md` lo comprueba antes de enseñarlo.

## Plantilla (los títulos tienen que estar tal cual)

```markdown
# Brief estratégico: <nombre>

## Situación
Qué es, qué vende, a quién, en qué momento está (2 a 4 líneas, hechos y con las palabras de la persona).

## Público y tensión
Quién es el cliente que decide, qué quiere y qué le da hoy la categoría. Una escena real si la contó.
**Tensión:** «<lo que quiere> pero <lo que la categoría le da>» (una frase con las dos mitades).

## Mapa de la categoría
| Alternativa | Qué promete | Cómo habla |
|---|---|---|
| … | … | … |
(mínimo 3, incluida una alternativa que no se parece pero resuelve lo mismo, aunque sea «hacerlo uno mismo»)
**Lo que todas dicen o hacen:** … **Lo que haremos distinto (solo una cosa):** …

## Posicionamiento
Para **<público>** que **<necesidad o momento>**, **<marca>** es **<categoría reconocible>** que **<beneficio>**, porque **<razón creíble: un hecho>**.

## Promesa y prueba
La promesa en una frase y la prueba que la sostiene (proceso, cifra, caso). Lo que aún no puede probar, dicho.

## Personalidad
Tres rasgos con comportamiento («es el ingeniero senior que…», no «es innovadora»). Arquetipo dominante y su riesgo.

## No es
- Qué nunca debe parecer ni sonar (mínimo 3), con el motivo de cada uno, en actitud y en lo que dice.

## Las tres vías
(La plantilla y las reglas están en `vias.md`: tres subsecciones `### Vía A/B/C`, con idea, a quién habla y qué promete, cómo suena, sensación general, riesgo y «encaja si». Sin colores, logos ni tipografías.)
**Recomendada:** … porque …

## Vía elegida
La que eligió la persona (o la mezcla), o «pendiente» con lo que falta para decidir.

## Idea rectora
Una sola frase (máximo 25 palabras) que resuma la vía elegida y de la que se deduzca el resto.

## Lo que aún no sabes
Tres o más cosas que faltan por descubrir, cada una con **cómo averiguarla esta semana** (hablar con tres clientes, probar la frase con alguien del sector, conseguir un dato).

## Palabras clave para buscar referencias
Las 3 generales, en una línea cada una (`palabras-clave.md`): sector + `brand identity`, cliente + producto, actitud de la vía + `branding`.
- `…`
- `…`
- `…`
Guardar 3 referencias (2 que le gustan y 1 que no quiere parecer), con la actitud de cada una.

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
Nombre (anterioridades pendientes de validación), claims, lo que no se puede prometer, *Supuestos* que hizo el agente sin confirmación.
```

## Reglas de calidad

- **Hechos y palabras de la persona, no adjetivos.** «Cada candidato habla antes con un ingeniero» es un hecho; «profesionales de calidad» no.
- **Ninguna frase vale para un competidor** cambiando el nombre.
- **Sin léxico prohibido** (`lexico-prohibido.md`): el verificador lo cuenta.
- **El posicionamiento sigue la fórmula**, completa. Si falta la razón para creerlo, es un hueco que se dice, no se rellena con un adjetivo.
- **La tensión tiene dos mitades.**
- **Los supuestos se marcan** como *Supuesto* para que la persona los corrija.
- **Nada visual** en las vías, la idea rectora, el posicionamiento ni la personalidad: ni colores, ni logos, ni tipografías, ni estilos, ni prompts. Lo visual solo aparece, en general y con «porque», en «Qué buscar y qué evitar en las referencias».
