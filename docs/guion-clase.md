# Guion de clase: crea tu marca con IA (90 minutos)

Para el profesor. Cada bloque dice qué haces, qué dices y qué puede salir mal. Antes de la clase, pasa las pruebas 1 a 3 de `prueba-guiada.md`.

## Antes de la clase

- Manda a los alumnos, **48 horas antes**: `brand-kit-builder.zip`, `docs/guia-alumnos.md` y el aviso «instalad Claude Code y comprobad que `python3 --version` (o `python --version`) da 3.11 o más».
- Pídeles que lleguen con **una marca real o inventada** y una frase de lo que hace.
- Ten abierta una carpeta con el ejemplo PULSO ya generado (`evals/fixtures/pulso/`) por si falla la conexión.
- Ten dos marcas de ejemplo para el arranque: una que parezca generada por IA y otra con carácter.

## Mapa de la sesión

| Min | Bloque | Producto |
|---|---|---|
| 0–10 | El problema | Entienden qué es una marca promedio |
| 10–20 | Instalación | Todos con el plugin instalado |
| 20–45 | Demo en directo | Ven el proceso entero |
| 45–75 | Ejercicio individual | Entrevista, territorio y paleta de su marca |
| 75–90 | Revisión por parejas | Lista de lo que queda a mano |

## 0–10. El problema

**Qué dices:** «La IA promedia. Entrenada con millones de marcas, devuelve la media de todas: simétrica, plana y con las mismas palabras. Una marca que parece generada pierde lo que la hace valer: parecer de alguien.»

**Qué haces:** enseña las dos marcas. Pide que adivinen cuál parece generada y por qué. Apunta las pistas en la pizarra (vocabulario, simetría, un lema que vale para cualquiera).

**Cierra con:** «Hoy vamos a usar la IA para el andamio, la estrategia y el criterio, y a poner la fachada nosotros.»

## 10–20. Instalación en directo

Haz tú los pasos de la sección 3 de la guía mientras ellos los siguen. Pausa tras cada comando.

**Comprobación común:** que todos vean `brand-kit-builder 2.0.0` en `claude plugin list`.

| Si pasa… | Haz… |
|---|---|
| «command not found: claude» | Claude Code no está instalado o la terminal es otra; vuelve a abrirla |
| La ruta no se encuentra | Que escriban `ls` (Windows: `dir`) y comprueben que están junto a la carpeta |
| No hay Python | No bloquees la clase: pueden hacer estrategia, logo, paleta y voz. Tokens y manual los ve con la demo |
| Va muy lento por la red | Pasa a la carpeta PULSO ya generada |

No avances hasta que al menos 3 de cada 4 lo tengan funcionando. Pide a los que sí a ayudar a su compañero.

## 20–45. Demo en directo (25 min)

Usa **un voluntario** para hacer una ronda real y la marca PULSO para el resto. Así no gastas la mitad de la clase en la entrevista.

**1. Entrevista real (8 min).** Abre una carpeta vacía y escribe la petición del voluntario. Muestra que:
- hace **una ronda por mensaje**,
- **no genera nada** hasta confirmar,
- pregunta qué **nunca debe parecer**.

**Qué dices:** «Fijaos en lo que NO hace: no dibuja, no propone colores. Eso es lo que nos ahorra rehacer luego.» Contesta con el voluntario y confirma el resumen.

**2. Territorios (5 min).** Enseña los tres. Pregunta a la clase cuál elegirían y por qué. Fíjate en si alguno se ancla en la categoría: «¿esto lo podría haber dicho cualquier panadería?».

**3. Salta a PULSO (12 min).** Copia el ejemplo según la prueba 3 y pide los tokens y el manual.
- Abre `ejemplo.html`: «esto es la marca funcionando en una página».
- Enseña `contraste.md` y el acento verde: «bonito, pero no se lee como texto. La skill me lo dice, no lo esconde».
- Abre `index.html` y recorre las láminas: portada, paleta, voz.
- Muestra el **logo provisional** y explica por qué: «sin logo aprobado, no inventa uno».

**Pregunta para cerrar:** «¿Qué parte de esto le habéis visto hacer a una IA normal?» (Respuesta esperada: casi ninguna. Preguntar primero, comprobar el contraste y avisar de lo que falta.)

## 45–75. Ejercicio individual (30 min)

Cada alumno, en su carpeta y con su marca. Meta: **llegar a la paleta aprobada y un `marca.json` válido.**

| Min | Qué hacen |
|---|---|
| 45–55 | Estrategia: tres rondas y confirmar el resumen |
| 55–62 | Elegir territorio |
| 62–75 | Identidad: dos propuestas de logo (prompts), paleta y tipografía |

**Frases de arranque** para quien se bloquee:

- Marca de producto: «Quiero crear la marca de [producto] para [público].»
- Servicio o freelance: «Necesito una marca personal para [lo que haces].»
- Marca inventada: «No tengo marca; inventa una para practicar, yo respondo como si fuera la dueña.»

**Cómo circular:** mira la pantalla de cada uno y busca tres cosas. (1) ¿Respondieron con ejemplos concretos al «nunca debe parecer»? (2) ¿Les han dado exactamente **dos** logos? (3) ¿Hay un `marca.json` en su carpeta?

**Si alguien va rápido:** que pase a voz y a los tokens.

## 75–90. Revisión por parejas (15 min)

Cada pareja intercambia pantalla y revisa con esta lista:

- [ ] ¿La respuesta al «nunca debe parecer» es concreta?
- [ ] ¿El territorio está anclado fuera de la categoría?
- [ ] ¿Hay exactamente dos logos y una recomendación?
- [ ] ¿La paleta tiene cinco colores con nombre, hex y papel?
- [ ] ¿El contraste del acento está calculado, y se dice para qué sirve?
- [ ] ¿`marca.json` existe y valida?
- [ ] ¿Aparece alguna palabra del léxico prohibido en lo que ha escrito la marca?

Cada pareja anota **tres cosas que quedan a mano** de la sección 7 de la guía, con un responsable y una fecha.

**Cierre (3 min):** pregunta qué les ha sorprendido. Recuérdales el entregable: la guía, el `marca.json` y la lista de pendientes.

## Errores típicos

| Qué ves | Causa | Qué hacer |
|---|---|---|
| El alumno responde «moderna y profesional» | La respuesta vaga bloquea la entrevista | Pídele una marca que lo sea y por qué |
| El logo no se parece a lo que pidió | Las imágenes de logo generadas por IA son referencia | Que ajuste el prompt una vez; no regenerar a ciegas |
| Pide tres logos | La skill ofrece dos | Es intencionado: tres diluyen el criterio |
| El alumno quiere empezar por el logo | La entrevista no está hecha | Vuelve a la estrategia; el logo sale del territorio |
| «El manual sale con textos pendientes» | Falta contenido en `kit.json` | Que lo redacte o se lo pida a Claude |

## Rúbrica de evaluación (entregable de la clase)

| Criterio | 0 | 1 | 2 |
|---|---|---|---|
| Entrevista | Respuestas vagas | Alguna concreta | «Nunca debe parecer» con ejemplos |
| Territorio | Anclado en la competencia | Mixto | Anclado fuera de la categoría |
| Paleta | Sin contraste | Contraste calculado | Contraste calculado y usos del acento claros |
| `marca.json` | No existe | Existe, con errores | Válido |
| Pendientes | No los lista | Lista genérica | Concretos, con responsable |

## Si cambias la skill entre clases

Sube el número de versión en `.claude-plugin/plugin.json` (y en el CHANGELOG) antes de repartir la carpeta nueva. Sin un número distinto, `claude plugin update` responde que ya está en la última versión y los alumnos se quedan con la anterior.

## Después de esta clase

La siguiente sesión es la de creación de contenido con creative-architect, que lee el `marca.json` de cada alumno. Antes de esa clase comprueba que instalan creative-architect (sección 3 de la guía) y que su `marca.json` valida.
