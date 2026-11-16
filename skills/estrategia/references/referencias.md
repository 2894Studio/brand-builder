# Referencias: entrenar el gusto

La IA promedia: si no le das un criterio propio, devuelve lo que ya existe en mil marcas. El gusto no se pide, se entrena: mirando mucho, eligiendo y **nombrando por qué**. Este paso mete el gusto de la persona dentro de la marca.

## Qué se pide

**Ocho referencias**, ni más ni menos:

| Cuántas | Qué | Para qué |
|---|---|---|
| 4 | Cosas que le encantan | Dirección |
| 2 | Cosas que no quiere parecer | Límite. Sin ellas el gusto no se educa |
| 2 | De otra categoría (revista, arquitectura, cartel, packaging, un libro) | Sacar a la marca de la media del sector |

Mejor **manuales de marca, publicaciones editoriales, carteles y webs con carácter** que marcas de la competencia: la competencia devuelve la media.

## Cómo se describe cada una

Siempre el **atributo**, nunca solo la marca. Una referencia sin atributo no se anota.

| Mal | Bien |
|---|---|
| «Me gusta Deloitte» | «La solidez: titulares grandes y mucho blanco, sin adornos» |
| «Quiero algo como LinkedIn» | «Que se vea profesional y fácil de leer, sin parecer una red social» |
| «Algo moderno y limpio» | Pide una marca que lo sea, y qué hace que lo sea |

Familias de atributos útiles para preguntar: **escala** (cuánto contrasta el titular con el cuerpo) · **ritmo** (cómo se alternan lo lleno y lo vacío) · **color** (cuánto, dónde, cuándo aparece) · **material** (papel, grano, textura) · **fotografía** (posada o real, luz) · **tipografía** (carácter, peso) · **tono** (cómo habla).

## Cómo se guarda

En `marca.json`, campo `referencias` (opcional; las demás herramientas lo ignoran):

```json
"referencias": [
  { "nombre": "Una revista de arquitectura", "atributo": "la escala enorme del titular y el silencio a su alrededor", "tipo": "si" },
  { "nombre": "Marcas de neón con degradados", "atributo": "los brillos y degradados que parecen generados", "tipo": "no" }
]
```

`tipo` es `si` (por defecto) o `no`. El validador avisa si no hay ninguna `no`. El manual añade una lámina «Referencias» con las primeras cinco.

## Reglas para quien conduce el paso

1. **Nunca inventes el atributo** de una referencia que no has visto o que la persona no ha descrito. Si falta, repregunta una vez por marca.
2. **No copies**: se extrae un atributo (la escala, el color que aparece una vez), no una marca.
3. **No juzgues una imagen que no puedes ver.** Si no hay forma de ver la referencia, pide que la describan.
4. Si una referencia choca con lo que dijo (por ejemplo, admira una red social y dice que no quiere parecer una), dilo y pregunta qué atributo exacto quiere quedarse.
5. Las referencias alimentan `visual.estilo` y la elección del territorio; no se usan para imitar.

## Dónde buscar (ejemplos; comprueba que sigan activos)

Archivos de identidades y casos de estudio (Brand New de UnderConsideration), portafolios de estudios (Pentagram, Collins), catálogos de tipografía en uso (Fonts In Use, Typewolf), tableros de inspiración (Are.na, Behance), y fuera del diseño gráfico: revistas, arquitectura, cartelería de museos.

## Ejercicios para enseñar el criterio

1. **Tres diferencias.** Poner el manual propio junto a una referencia y escribir tres diferencias concretas.
2. **El atributo robado.** Elegir un atributo de una referencia y aplicarlo a una sola lámina.
3. **La prueba del tapado.** Tapar el nombre de la marca: ¿se sabría de quién es?
