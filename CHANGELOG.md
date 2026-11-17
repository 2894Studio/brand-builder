# Changelog

## 3.2.0 (2026-11-17)

- **Palabras clave para buscar referencias** (`gusto/references/palabras-clave.md`): por defecto, **tres búsquedas generales** que sirven igual en Behance, Pinterest y Dribbble (sector + `brand identity`, cliente + producto, actitud de la vía elegida + `branding`), deducidas del brief; más, por plataforma y para el rechazo, solo si la persona las pide. Enlazado desde `estrategia`, `gusto` y el router.

## 3.1.0 (2026-11-17)

- **Las rondas de la estrategia se hacen siempre con el diálogo nativo** (`AskUserQuestion`; `ask_question` en Antigravity), también las abiertas: las opciones son 2 a 4 respuestas típicas y contrapuestas, que hacen de ejemplos, y la persona escribe lo suyo en «Other». Antes las abiertas iban en texto del chat y no aparecían como preguntas nativas.
- **Brevedad para ahorrar tokens:** sin preámbulos ni explicación del método, pregunta de una línea, el porqué en menos de 12 palabras, espejo de máximo 5 líneas y cero relleno entre diálogos.

## 3.0.1 (2026-11-17)

- **Rondas más ligeras:** 3 o 4 preguntas por ronda como máximo (la cerrada cuenta) y cada pregunta con un solo signo de interrogación; el porqué y los ejemplos de respuesta van sin interrogaciones. En una prueba con Sonnet las rondas llegaron a 5 preguntas numeradas más una cerrada, con varias interrogaciones encadenadas.
- **La persona elige la vía:** se enseñan las tres vías en el chat y se espera su elección; si no contesta, «Vía elegida: pendiente».
- Arnés e2e: las rondas de la persona se contestan en orden.

## 3.0.0 (2026-11-17)

**Nuevo objetivo: ayudar a explorar la marca con buenas preguntas, sin recomendaciones visuales.** El resultado por defecto ya no es un logo ni un brief de logo, sino la conversación y un brief estratégico con tres vías generales.

- **`estrategia` reescrita como exploración:** 2 o 3 rondas (un mensaje y de 3 a 5 preguntas por ronda), cada pregunta con su porqué; piden **escenas reales** y no definiciones. Banco de preguntas por ronda, repreguntas y cómo escuchar en `estrategia/references/entrevista.md`. **Espejo entre rondas** (lo que oigo, lo que me llama la atención, lo que aún no sé), sin soluciones.
- **Cierre con tres vías generales** (`estrategia/references/vias.md`): se separan por actitud y promesa, no por estética; cada una con idea, a quién habla y qué promete, cómo suena, sensación general (una palabra de registro), riesgo y «encaja si»; una recomendada; la persona elige o mezcla dos y se resume en la idea rectora.
- **Nada visual en esta fase:** ni colores, ni logos, ni tipografías, ni estilos, ni prompts. `verificar_brief.py` lo comprueba en las vías, la idea rectora, el posicionamiento y la personalidad, exige exactamente tres vías completas, una recomendación y al menos tres «cosas por descubrir» con cómo averiguarlas.
- **Router y `AGENTS.md`:** cadena por defecto = solo `estrategia`. `brief-logo` y la cadena visual (`gusto → identidad → … → entrega`) pasan a ser pasos posteriores y opcionales; no se pregunta el proveedor de imagen salvo que se pida la cadena visual.
- **Criterio experto** adaptado: «preguntas para hacer pensar, no para rellenar»; investigación solo para preguntar mejor.
- **Arnés e2e:** escenario `estrategia_exploracion` con las rondas de un alumno y medidas de preguntas por ronda y de lenguaje visual que se cuela.

## 2.10.3 (2026-11-17)

- **Prompt de Claude (B) sin repeticiones ni contradicciones:** ya no incluye dos veces las tres direcciones (van una sola vez, detalladas) y la regla de color coincide con el brief («una tinta más un acento que se pueda sustituir por la misma tinta»).

## 2.10.2 (2026-11-17)

- **Prompts de imagen más limpios:** el prompt «natural» va solo en positivo (nombrar lo que no quieres, como «literal bee», puede hacer que el modelo lo dibuje) y los «negative prompt» van aparte, con la indicación de usarlos solo si la herramienta tiene ese campo. Se corrige la contradicción «una sola tinta» frente a «tinta más acento»: ahora dice «one ink colour plus one accent colour» cuando hay acento.

## 2.10.1 (2026-11-17)

- **El proveedor de imagen ya no se pregunta en la cadena por defecto** (brief de logo y prompts): no se genera ninguna imagen. Solo con el kit completo. Salió de la prueba con Sonnet, que lo preguntaba sin necesitarlo.

- **El nombre es obligatorio y no se inventa** (`estrategia`): si falta, se pregunta en el primer mensaje; si la persona lo delega, se proponen tres con su razón y se comprueban. Salió de una prueba real con Sonnet en la que el agente inventó un nombre «provisional» y lo arrastró por todo el brief.
- **`brief_logo.py` marca las reglas de gusto sin confirmar** (referencias armadas por el agente de memoria) en lugar de presentarlas como gustos de la persona.
- **Arnés e2e:** el primer turno contesta siempre con los datos de la persona; escenario `agencia_talento_ia` para el flujo por defecto (brief de logo) y mediciones del brief.

## 2.10.0 (2026-11-17)

**Nuevo objetivo por defecto: un buen brief de logo y prompts para explorar logos con IA.** El resultado de «crea mi marca» deja de ser el kit completo: ahora es `estrategia.md` (brief estratégico), `brief-logo.md` y `prompts-logo.md`. El kit completo (paleta, manual, tokens, bento y posts) sigue disponible si la persona lo pide.

- **Skill `brief-logo`** (`skills/brief-logo/`): el agente piensa **tres direcciones de tipo distinto** (idea, por qué, forma construible, riesgo, prompt en inglés), los tópicos de la categoría que no se usan y las restricciones; `tools/brief_logo.py` lo comprueba (se niega con estrategia.md sin verificar, con menos o más de tres direcciones, del mismo tipo, de relleno, sin inglés o sin tópicos) y lo ensambla con lo ya decidido: idea rectora, posicionamiento, tensión, personalidad, «no es» y las reglas de tu `gusto.json` que tocan al logo (y lo que hay que evitar).
- **`prompts-logo.md`** trae: prompts para **modelos de imagen** (uno por dirección, en versión natural y de Midjourney, con «avoid» de los tópicos y las restricciones en inglés), un prompt para **Claude o Claude Design** que pide un tablero SVG con las tres direcciones sobre claro, oscuro y a 32 px, con autocrítica (tres debilidades y las cinco pruebas) y recomendación, y un prompt de **refinamiento** de un solo cambio por vuelta, más cómo decidir.
- Router, estrategia y `AGENTS.md`: la cadena por defecto es `estrategia → gusto → brief-logo`; la completa pasa a ser opcional. El alcance por defecto es «brief de logo + prompts».
- No verificado: qué sale de cada plataforma con estos prompts. `references/plataformas.md` recoge lo esperable y lo marca como tal.

## 2.9.0 (2026-11-17)

**Cambio de enfoque.** Los resultados no acertaban porque el plugin trataba la estrategia como un cuestionario: preguntaba cinco cosas de «quién es la marca» y transcribía las respuestas, sin investigar ni opinar, y el resto de pasos solo comprobaba la forma. Ahora el agente trabaja como un director de marca:

- **Criterio experto** (`brand-kit-builder/references/criterio-experto.md`): nueve hábitos (propone en vez de interrogar, investiga la categoría, busca la tensión, respeta una convención y rompe una, defiende cada decisión contra el brief, una pieza un mensaje, se critica antes de enseñar, dice la verdad con alternativa, no promete lo que no controla) y cinco pruebas de acierto (competidor, tres segundos, reducción, «no», defensor). El router lo exige al empezar.
- **Estrategia reescrita:** investiga competidores y alternativas, comprueba el nombre y llega con una **hipótesis** (público, tensión, posicionamiento, personalidad, lo que nunca debe parecer) que la persona confirma o corrige; como mucho tres preguntas con respuesta recomendada y dos rondas. Si dice «decide tú», decide y marca el *Supuesto*.
- **Brief estratégico verificable** (`estrategia.md`, plantilla en `estrategia/references/brief-estrategico.md`): situación, público y tensión, mapa de la categoría (convención que se respeta y la única que se rompe), posicionamiento con fórmula, promesa y prueba, personalidad, «no es», **idea rectora** en una frase, riesgos y criterios de acierto. `estrategia/tools/verificar_brief.py` lo comprueba (secciones con contenido, tensión con dos mitades, al menos tres competidores, fórmula completa, tres «no es», idea de máximo 25 palabras, sin marcadores ni léxico prohibido).
- **Identidad:** parte de un concepto escrito (idea rectora, convención que se rompe, tipo de marca, qué debe verse a 25 mm), y critica sus dos logos (tres debilidades y las cinco pruebas) antes de enseñarlos, diciendo qué idea del brief expresa cada uno y por qué podría fallar. **Voz** sale de la personalidad y el «no es» del brief.
- **Lanzamiento:** cada post declara su **intención** (mensaje, gancho, prueba, llamada) en `brief.json`; se copia al `LEEME.md`.
- **Puerta de entrega:** comprueba `estrategia.md` con el verificador (se cierra si está vacío o es un formulario) y avisa si falta o si un post no tiene intención. `estrategia_ok` con motivo lo exceptúa.

Aún no se ha repetido una prueba de punta a punta con este flujo: el efecto real sobre la calidad de los briefs hay que comprobarlo con casos reales.

## 2.8.0 (2026-11-17)

La prueba 3 con tu gusto entrenado (2.7.0) dio un post de titular sobre fondo liso y otro con una cifra: seguía siendo plantilla. Se cierran las vías fáciles:

- **Los dos posts a medida:** con reglas de composición para posts en el gusto, **ambos** posts deben ser `compuesto` (o `html` propio). `kit_lanzamiento.py` lo comprueba antes de renderizar y la puerta de nuevo. Dos composiciones a medida solo cuentan como distintas si cambia su disposición (`variedad.py` compara dónde están los elementos).
- **Nada de «solo aire»:** cada composición debe citar al menos una regla gráfica del gusto (símbolo, forma, firma o imagen) y llevar al menos un elemento gráfico; `post_compuesto.py` se niega a dibujar una composición que es solo texto. Elemento nuevo `simbolo`: el símbolo del logo a gran tamaño y recortado por el borde.
- **El crítico mira lo que hay debajo del texto:** un círculo o bloque opaco bajo un texto cuenta como su fondo (se mide el peor punto). Una prueba real con un texto sobre un círculo del mismo color se había escapado con «0 errores».
- **Logo con símbolo, gratis:** `identidad/tools/simbolo_geometrico.py` genera dos opciones de logo con símbolo (baldosa, órbita, pliegue, bloques, arcos) con la paleta de la marca: principal, invertida, monocroma, símbolo y símbolo invertido (para fondos oscuros), más una hoja de comparación. El agente elige los dos tipos con una razón escrita y el resultado alimenta el bento y los posts. Es un punto de partida honesto, no sustituye a un dibujo a mano.

## 2.7.0 (2026-11-17)

- **Composición a medida (contra las plantillas):** `post_compuesto.py` dibuja una composición que **diseña el agente** con una especificación JSON (texto, palabra gigante recortada, formas, gráfico firma, foto con marco de sello o redondeado, insignia, cifra, línea, logo), con la paleta y fuentes de la marca; exige `concepto.referencias` que cite reglas de gusto (R#). `contacto_referencias.py --para post|logo|bento|web` deja una hoja con solo las referencias y reglas de ese destino para **mirarlas antes de diseñar**. Guía en `lanzamiento/references/composicion-a-medida.md`; recurso `compuesto` en `kit_lanzamiento.py`.
- **La puerta tiene más dientes con gusto entrenado:** si el gusto tiene reglas de composición para posts, al menos un post debe ser composición a medida (o HTML propio), salvo `plantillas_ok` con motivo; «parcial» no puede pasar del 25 % de las reglas aplicables; ninguna regla puede confesar trabajo pendiente; cada `composicion-*.json` debe citar reglas que existan.
- **Bento:** sin símbolo en el logo ya no pinta una inicial en un cuadrado (contradecía reglas como «símbolo que no sea una letra»): muestra el gráfico firma.
- **Windows (descubierto con el nuevo CI):** salida y lectura en UTF-8 en todas las herramientas y `relpath` seguro entre unidades. **CI** en Linux, macOS y Windows (Python 3.11 y 3.13) en `.github/workflows/pruebas.yml`.
- **Prueba de punta a punta** (`evals/e2e/ejecutar.py`, tres escenarios): un agente barato recorre el flujo y se mide con la puerta, las huellas de plantilla y la revisión contra el gusto (unos 0,3 USD con Haiku).

## 2.6.3 (2026-11-17)

- **Huellas de plantilla en el crítico (`anti-plantilla:`):** avisa de tipografía solo por defecto (Inter, Arial, Roboto…), texto gris sobre un fondo de color, negro o gris puro sin tintar, degradado morado a azul y tarjetas dentro de tarjetas dentro de tarjetas. La puerta de entrega se cierra con **2 o más por pieza**, salvo `tells_ok` con motivo en el brief. Ideas tomadas de la lista de anti-patrones de [Impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0), reescritas y medidas sobre el render.
- **Vocabulario de ajustes** (`lanzamiento/references/ajustes.md`): más atrevido, más sobrio, simplificar, más humano, más técnico, más tipografía, más aire, más contraste, menos genérico; cada verbo, un cambio concreto en el brief.

## 2.6.2 (2026-11-17)

- **Etiquetador de referencias (interfaz):** `gusto/tools/etiquetador.html` (un solo archivo, funciona sin conexión) para arrastrar o pegar imágenes, marcarlas (me gusta / no quiero parecerme / otra categoría), escribir la nota y las decisiones por dimensión (con ejemplos y la marca de «distintiva»), y una lista de comprobación viva (6 a 8 referencias, al menos 3 sí y 2 no, notas y decisiones completas). Guarda con `etiquetador.py` (servidor local solo en 127.0.0.1: crea `referencias/` y actualiza `gusto.json`) o con **Descargar ZIP** + `importar_etiquetado.py` (copia, mide con `analizar_referencias.py` y vuelca tipo, nota y decisiones; rechaza nombres y formatos peligrosos). Probado en Chromium de punta a punta.

## 2.6.1 (2026-11-17)

- **Entrenar el gusto de verdad (a partir de la prueba de la escuela de código, donde las referencias no mejoraron nada):** las referencias ahora se convierten en **decisiones transferables por dimensión** (nombre, símbolo, tipografía, imagen, composición, firma, forma, color, voz) con `gusto.py decision`, numeradas R1…Rn con `gusto.py reglas` (las de las referencias «no» son «EVITAR»); `validar` avisa si una referencia «sí» no tiene decisiones o si solo toca forma y color (lo genérico). `kit_lanzamiento.py` deja `contacto-gusto.png` (referencias | piezas | reglas) y `revision-gusto.md`, y la **puerta de entrega** no se abre con reglas sin revisar o en «no cumple» sin corregir. Protocolo para la persona: `gusto/references/entrenar.md`.
- **Gemini API verificada con una clave real:** lista 6 modelos de imagen, pero el nivel gratuito responde **429 «limit: 0»**: generar imágenes por API exige activar la facturación. Se corrigen los textos que decían «gratis»; el script explica el motivo y prefiere el modelo más reciente.

## 2.6.0 (2026-11-17)

Resumen: la calidad de las piezas pasa de «plantilla» a «campaña». Compatibilidad con Google Antigravity, nuevos generadores (pantalla, comparativa, foto, tipográfico, expresivo), puerta de entrega y hook de parada, proveedores de imagen (Canva y FLORA verificados; Gemini API, Higgsfield, Magnific y Spaces sin verificar), tres direcciones de identidad y la pregunta del proveedor de imagen.

- **Pregunta del proveedor de imagen:** el router pregunta una vez, con un diálogo, «¿Tienes algún proveedor de imagen para mejorar la calidad de las piezas?» (Canva · FLORA, Higgsfield, Magnific, Spaces u otro de pago · Gemini o Flow gratis · Ninguno) y lo guarda con `proveedor_imagen.py`; `identidad` y `lanzamiento` lo leen. Guía en `lanzamiento/references/proveedores-imagen.md`. `generar_gemini.py` usa la API de Gemini con `GEMINI_API_KEY` (probado solo con un servidor simulado); `prompts_fotos.py --proveedor higgsfield|magnific|spaces` avisa de que esas recetas no están verificadas.

- **Nuevo:** `plugin.json` en la raíz (manifiesto de Antigravity) y `AGENTS.md`, un **puntero** corto al router (`skills/brand-kit-builder/SKILL.md`), que es la única fuente de las reglas: así no se desincronizan. `verificar_skills.py` comprueba que sus enlaces existan. Claude Code sigue leyendo solo `.claude-plugin/`.
- **Arreglo importante:** 5 de las 10 skills (el router, `entrega`, `lanzamiento`, `tokens` y `voz`) las **saltaba en silencio** un lector de YAML estricto, porque su `description` llevaba «: » sin comillas. Claude Code lo toleraba. Ahora todas las descripciones van entre comillas y `verificar_skills.py` lo comprueba (con un YAML estricto) para que no vuelva a pasar.
- **Documentación:** instalación en Antigravity en el README (`git clone` a `~/.gemini/config/plugins/`) y mención de `ask_question` en la convención de preguntas.
- **Arreglos a partir de una prueba completa en Antigravity (marca «fullstacker»):**
  - El **crítico** detecta ahora texto **recortado por su contenedor** (`overflow` oculto) y acepta `ui-monospace` y otras familias genéricas modernas.
  - `post_telefono.py` ya no desborda: presupuesto de contenido, avisos de textos largos y `--tema claro`.
  - **Nuevos generadores:** `post_pantalla.py` (ventana de escritorio, con modo código) y `post_comparativa.py` (exige `--fuente` del competidor: no se inventan datos de terceros).
  - `bento.py` sin fotos: `--datos` y `--puntos` sustituyen los marcadores por contenido real.
  - `identidad` extrae primero de las referencias el tratamiento del nombre, la morfología del símbolo y lo que prohíben, antes de proponer logos.
  - `lanzamiento` elige el generador por el producto (no siempre el teléfono) y prohíbe entregar con texto recortado.
- **Contra las plantillas:** nueva `lanzamiento/references/direccion-creativa.md` (brief de 5 líneas por pieza, tres conceptos que difieran en estructura, la categoría manda) y `tools/variedad.py`, que compara la estructura de una pieza con la otra del kit y con los kits anteriores y avisa si se parecen (≥ 0,6). Los generadores pasan a ser **andamios**, no la respuesta por defecto. `bento.py` gana `--variante educativa` (el recorrido es la tarjeta principal, exige `--ruta`) y `--variante producto` (la foto manda, exige foto).
- **Arreglos a partir de una prueba en Claude (marca «DPROMA»):**
  - `generar_kit.py`: el **PDF del manual salía sin logos** (rsvg-convert no carga rutas relativas); ahora los incrusta en copias temporales. Probado con un `rsvg-convert` falso en `verificar_laminas.py`.
  - La lámina de **usos** avisa cuando una regla pisaría el pie (y la omite), en vez de dibujarla encima.
  - «La marca»: el público ya no sale como «Para Empresas…» ni con doble punto; la portada respeta las mayúsculas del nombre.
  - **Marca sosa:** `gusto` no se salta con «interprétalo tú» (se construye el punto de partida desde la categoría), el alcance recomendado es el kit completo y `identidad` exige un **sistema de imagen** (fotografía, gráfico firma, momento de color) antes de cerrar. Nueva invariante 11.
  - README: instalar el plugin, no clonarlo solo para leerlo.
- **Fotos gratis:** `buscar_fotos.py` busca en Pexels (clave gratuita opcional), descarga y rellena `creditos.md` con autor, enlace y licencia; `prompts_fotos.py` escribe los prompts para generar las fotos en Gemini o Google Flow. Probado con un servidor Pexels simulado: **no se ha probado contra la API real** (no había clave).
- **Canva como proveedor de fotos:** `prompts_fotos.py --proveedor canva` da la proporción de Canva (`aspectRatio`) de cada prompt y `registrar_foto.py` anota la foto en `creditos.md` (origen, fuente, licencia, permiso) con las mismas reglas que `preparar_fotos.py`.
- **Prueba de punta a punta con Haiku (marca educativa «Tuvista»):** el agente dibujó el bento y los posts a mano en SVG, no usó ningún generador, se saltó el crítico y la puerta, y dejó marcadores. Respuesta: `kit_lanzamiento.py` (brief.json → generadores → PNG → crítico → puerta, una sola orden), invariante 12 «las piezas finales no se dibujan a mano» y puerta de entrega `entrega/tools/verificar_entrega.py`.
- **Calidad (segunda vuelta de la prueba «Tuvista»):** nuevo `post_foto.py` (foto a sangre, bloque opaco con el titular y notas sobre la foto); el crítico detecta **palabras partidas a mitad** (los hex del bento se cortaban); la muestra de color del bento pasa a filas; la puerta de entrega exige fotos a las marcas visuales (fotografía, gastronomía, moda…) salvo `sin_fotos` con motivo; hook de parada (`hooks/`) que no deja terminar un kit que no pasó la puerta.
- **Posts siempre del mismo tipo (aviso de la persona usuaria):** causa, `variedad.py` medía clases CSS (móvil y ventana daban 0,50 y pasaban) y los generadores de interfaz eran el camino cómodo. Ahora cada pieza lleva su **arquetipo** (`ui`, `foto`, `datos`, `mapa`, `tipografico:cifra|pasos|manifiesto`); dos posts del mismo arquetipo son la misma plantilla y la puerta y `kit_lanzamiento.py` los rechazan; la **interfaz solo para productos digitales**; nuevo `post_tipografico.py` (cifra gigante, pasos, frase enorme con inicial a sangre) y `proponer_posts.py`, que ofrece tres combinaciones adaptadas a la categoría (y que rotan según la marca) para que la persona elija con un diálogo.
- **Canva de punta a punta (probado con una cuenta real):** 2 imágenes generadas, exportadas y descargadas, registradas con `registrar_foto.py`, preparadas y montadas en el kit; la receta recoge los formatos que funcionaron y la página en blanco que Canva puede añadir. `bento.py`: con retrato y sin `--persona` no inventa un nombre; con las dos fotos la variante educativa les da dos filas; cae al territorio si `gusto.json` no trae proporciones.
- **Estilo divertido expresivo (a partir de una referencia de agencia de viajes):** nuevo `post_expresivo.py` con modos `gigante` (palabra enorme recortada, foto en marco de sello de correos, insignia con el símbolo, estrellas y matasellos) y `precio` (precio gigante con decimales en superíndice, píldora y beneficios); recursos `expresivo_gigante` y `expresivo_precio` en `kit_lanzamiento.py`, propuestos por `proponer_posts.py` cuando el tono es divertido; sección nueva en `gusto/references/tonos.md` (hipótesis con n = 1). `variedad.py` da prioridad al arquetipo declarado frente al índice de clases.
- **FLORA como proveedor de imágenes (probado con una cuenta real, 0,207 USD):** `prompts_fotos.py --proveedor flora` (con `aspect_ratio`, presupuesto previo `quote: true` y modelos probados) y nuevo prompt `objeto-1` (objeto sobre fondo liso del color de acento). Las imágenes se descargan directamente con `curl`, sin exportar un diseño como en Canva. Receta y límites (tope de proyectos del plan gratuito, la API no crea ni borra proyectos) en `lanzamiento/references/fotos.md`.
- **Técnica «Logo to Brand Identity» de FLORA (opcional, de pago):** `identidad/tools/flora_logo.py` (`preparar` el logo de entrada sobre fondo liso; `guardar` y **medir** los tableros de salida con `analizar_referencias.py`), `identidad/references/direccion-flora.md` (pasos con el conector, presupuesto en vivo —4,282 USD el 2026-11-16—, reglas: los tableros son inspiración y la estrategia manda) y el paso 4c de `identidad`. **Aún sin una ejecución real de la técnica**; la integración se probó con tableros simulados.
- **Tres direcciones de identidad dentro del plugin, gratis (alternativa a la técnica de FLORA):** `identidad/tools/tableros_identidad.py` renderiza 2 o 3 direcciones (`direcciones.json`: paleta, tipografía, gráfico firma, radio, estilo de imagen) como tableros HTML+PNG con el logo, la paleta, la tipografía, una tarjeta y un post de muestra; `identidad/references/tres-direcciones.md` explica cómo leer el logo y cruzarlo con la estrategia. El paso 4c de `identidad` pasa a ser este camino y deja FLORA como opción de pago.

## 2.5.1

- **Arreglo:** `estrategia` dice ahora que `referencias[].tipo` solo admite `"si"` o `"no"`. Dos modelos distintos escribieron valores inválidos («a favor», «gusta») porque la instrucción no lo decía.
- **Documentación:** «Qué modelo usar» en `ahorro-tokens.md`, con coste y calidad medidos con Sonnet 5.5 y Haiku 5.5 y lo que no se ha probado.
- Incluye todos los cambios añadidos tras la primera publicación de la 2.5.0 (generadores, fotos, bento con degradado, criterio de nivel): quien tenga instalada la 2.5.0 antigua verá la actualización.

## 2.5.0

Nueva skill **lanzamiento**: el resultado final de usar el plugin incluye el logo, el bento y dos posts.

- **Nuevo:** `lanzamiento`, paso entre `laminas` y `entrega`. Entrega el logo (SVG y PNG), un bento de la marca y dos posts: el 1 explica qué es la marca y el 2 muestra su principal atributo, ambos con un recurso visual.
- **Nuevo:** `bento.py` genera el bento (1920×1080) desde `marca.json` y, si existe, `gusto.json`; lo que no se aporta queda como marcador visible. `post_base.py` da el andamio de los posts; `exportar_logos.py` saca los PNG transparentes. Todos con autotest (`verificar_lanzamiento.py`).
- **Nuevo:** `mensajes.md` (cómo elegir los dos mensajes, con tres candidatos de atributo), `recursos-visuales.md` (catálogo: teléfono con interfaz, mapa de puntos, cifra con fuente, persona con rol) y `fotos.md` (de dónde salen las fotos, con y sin Canva).
- **Nuevo:** `preparar_fotos.py` recibe las fotos de la persona en `fotos/`, comprueba resolución y créditos (`creditos.md`: origen propia, banco o ia; un banco sin licencia o una foto sin fila da error), recorta a 3:4, 4:3 y 1:1 y escribe un manifiesto. `bento.py` y `post_base.py` las cogen con `--fotos`. Con autotest.
- **Aclarado:** Canva **genera** imágenes con IA (sintéticas); no es fuente de fotos reales. Receta verificada para traerlas a disco, orden de preferencia (fotos propias, bancos con licencia, generadas, sin fotos) y plantillas de prompt en `fotos.md`.
- **Decisión de la persona:** escribir «Imagen generada con IA» sobre una pieza es **opcional** (`--declarar-ia`); por defecto no se escribe nada. Siempre queda anotado en `creditos.md` y en el `LEEME.md`.
- **Nuevo:** generadores de las dos composiciones que mejor han funcionado: `post_telefono.py` (teléfono con la interfaz, tarjetas de cristal, fotos con borde) y `post_mapa.py` (mapa de puntos de geografía real, anillo en kilómetros, distancia calculada). El modelo pone los datos; no compone cada vez desde cero. `mapa_puntos.mjs` proyecta además las ciudades (`--puntos`).
- **Cambio:** el bento lleva por defecto degradado con luz en la tarjeta del logo (`--plano` para color liso). Antes salía más plano que el hecho a mano.
- **Aprendido:** una prueba con el modelo sin generadores produjo piezas correctas pero con poco diseño (una foto con dos rótulos): el crítico detecta defectos, no calidad. `criterio.md` define el nivel mínimo (tres capas) y `lanzamiento` avisa si no hay referencias entrenadas.
- **Cambio:** la cadena por defecto añade `lanzamiento` antes de `entrega`, y `entrega` comprueba que existen los cuatro resultados.
## 2.4.0

- **Nuevo:** `preguntas-interactivas.md`, convención para que las preguntas cerradas (territorio, logo A o B, tono, mockups, confirmaciones) salgan como diálogo nativo con opciones (`AskUserQuestion` en Claude Code) y las abiertas vayan en el chat. Con alternativa numerada cuando no hay diálogo. No verificado el aspecto del diálogo en este entorno.
- **Documentación:** banner y infografía del paso a paso en el README (`assets/`, con las fuentes HTML en `assets/src/` para editarlas), con la marca 2894_ y una tabla equivalente en texto.
- **Publicado** en GitHub (`2894Studio/brand-kit-builder`). Instalación desde GitHub verificada en una configuración limpia: instala la 2.4.0 con todas sus skills y el autotest de `gusto` pasa desde la copia instalada.

Para que los alumnos lleguen a piezas de este nivel con su propio equipo y sus propias referencias.

- **Nuevo:** `comprobar_entorno.py` prueba de verdad la cadena (Python, Pillow, Node, Playwright, Chromium y las fuentes de la marca), dice qué capacidades hay y el comando para instalar lo que falta. Probado completo y sin Node.
- **Nuevo:** `buscar-referencias.md`: qué es una buena referencia, cuántas, dónde buscarlas con y sin MCP, cómo entregarlas y cómo no copiar.
- **Cambio:** las referencias se piden en dos momentos. En `estrategia`, una versión corta (3, también en palabras) solo para orientar los territorios; el entrenamiento completo (6 a 8 imágenes medidas y confirmadas) pasa a `gusto`, después de elegir territorio y antes de `identidad`. Razón: en la prueba real, las referencias de la primera fase se quedaron sin atributo y fue con las imágenes concretas cuando salieron patrones útiles.
- **Cambio:** la cadena por defecto incluye `gusto`: `estrategia → gusto → identidad → voz → tokens → laminas → entrega`.
- **Documentación:** la guía del alumno recoge lo recomendado a instalar y el paso de referencias; `elegir-herramienta.md` añade la regla «¿quién edita después?» y el flujo híbrido HTML + Canva.

## 2.3.0

Cambios tras repetir un rebranding «moderno» de Findpro con dos referencias nuevas.

- **Nuevo:** `critico_render.py` estima el **contraste sobre degradados e imágenes** con los píxeles de la captura (necesita Pillow). Detectó iniciales blancas sobre un avatar degradado a ~4:1.
- **Nuevo:** atributo `data-decorativo` para la palabra fantasma de fondo: no se juzga, no se compara con otros textos.
- **Nuevo:** `mapa_puntos.mjs` genera un mapa de puntos con geografía real (proyección cónica, malla hexagonal, `kmPx` para radios en kilómetros) y el patrón «mapa de puntos» en `patrones-saas.md`. Verificado con la península ibérica: Madrid–Toledo 68 km.
- **Arreglo:** el crítico daba falsos solapes con titulares gigantes de `line-height` menor que 1 (la caja del texto incluía el espacio de la fuente); ahora se recorta a la caja del elemento. Con prueba.
- **Cambio:** el texto dentro de una maqueta de interfaz también debe medir ≥ 19 px; dos pruebas con 15–17 px lo habían dejado pasar como «es la interfaz».
- **Nuevo:** `tonos.md` y `patrones-saas.md` recogen el estilo «moderno de producto» (degradado, palabra fantasma, maqueta con interfaz, tarjetas de cristal, fotos en tarjetas), con sus riesgos.
- **Verificado:** las imágenes de Canva se pueden traer a resolución completa metiéndolas en un diseño y exportando a PNG (el enlace «Open generated image» da 403 con `curl`). Documentado en `skills/canva/SKILL.md` y en la guía.
- **Aviso:** las personas generadas son sintéticas; la skill pide declararlo en la pieza o sustituirlas.

## 2.2.0

Skill nueva: **gusto**, para entrenar el gusto visual sin servicios externos (sin MCP).

- **Nuevo:** `gusto.json` con referencias medidas, notas de la persona, proporción de tonos (serio, divertido, tecnológico) y elecciones A/B. Validación incluida.
- **Nuevo:** `analizar_referencias.py` mide colores, aire, detalle y familias de tono de una carpeta de imágenes (necesita Pillow). No mide ni inventa el tono: queda pendiente de interpretación y confirmación.
- **Nuevo:** `critico_render.py` abre una pieza HTML en Chromium y detecta texto fuera del lienzo, textos que se pisan, fuente de reserva, contraste, texto diminuto, colores fuera de `marca.json` y jerarquía débil. Sin Playwright sale con código 2 y no da la pieza por revisada.
- **Nuevo:** `gusto.py ab` registra elecciones A/B y mueve la proporción de tonos como máximo 10 puntos por elección (heurística visible, no aprendizaje).
- **Nuevo:** referencias `tonos.md`, `patrones-saas.md`, `criterio.md`, `protocolo-ab.md` y `critico.md`. Salen de siete referencias SaaS de una persona: son hipótesis con n = 7 y así constan.
- **Nuevo:** `verificar_gusto.py`, autotest con piezas de defectos conocidos; lo que no puede ejecutar lo marca SALTADO.
- **Cambio:** el enrutador envía a `gusto` las peticiones de «menos genérico», «más profesional/humano/tecnológico» y de piezas de contenido.

## 2.1.1

Cambios a partir de una prueba real de punta a punta con una marca nueva.

- **Nuevo:** `incrustar_fuente.py`. Incrusta la fuente en los logos SVG y quita las clases CSS compartidas, para que el logo se vea igual dentro de `<img>`, sin conexión y junto a otros logos. Verificado con la red bloqueada.
- **Nuevo:** paso de **referencias** en `estrategia` y campo `referencias` en `marca.json` (esquema, validador y plantilla), para entrenar el gusto visual con el atributo concreto de cada referencia.
- **Nuevo:** láminas más expresivas: portada con inicial gigante a sangre, divisores con número recortado, lámina de principio a página completa y lámina de referencias. `kit.json` admite `"expresivo": false`.
- **Nuevo:** `criterio-visual.md`, las cinco preguntas para juzgar un manual, y comprobaciones en la skill de entrega.
- **Arreglo:** las tarjetas de valores se salían de la lámina con 4 valores; ahora pasan a rejilla 2×2.
- **Arreglo:** doble punto en el tono, palabras prohibidas genéricas en lugar de las del sector, licencia de fuentes cortada, y `;` final en el `style` del puente a motion-architect.
- **Arreglo:** el autotest comprueba que el texto a sangre asoma en el lienzo (un error propio lo dejó fuera de la lámina) y cubre las variantes con 4 valores, sobrio y con referencias.
- **Cambio:** `estrategia` busca el nombre en la web antes de dibujar el logo, e `identidad` exige ver el logo renderizado antes de presentarlo.
- **Documentación:** la guía recoge que la imagen de Canva solo llega como miniatura y hay que descargarla.

## 2.1.0

- **Nuevo:** `exportar_motion.py`, puente de `marca.json` a `brand.json` de motion-architect (esquema verificado contra su repositorio; renderizado de un fotograma comprobado con PULSO).
- **Nuevo:** `verificar_tokens.py`, autotest de tokens y del puente.
- **Nuevo:** guion de introducción, guion de la sesión de contenido, guía de ahorro de tokens y tabla para elegir herramienta.
- **Nuevo:** la skill `canva` recoge los hechos verificados del conector (4:5 y 9:16, `generate-design` con `brand_kit_id`, `create-design` sin Brand Kit).
- **Cambio:** la skill de entrada indica pedir «usa mi `marca.json`» al crear contenido, tras comprobar que sin ella el modelo no siempre lo lee.

## 2.0.0

- **Documentación:** guía del alumno, guion de clase y prueba guiada.
- **Arreglo tras la primera prueba con el modelo:** trata siempre de tú y no adelanta soluciones antes de cerrar la entrevista.
- **Nuevo:** aviso de Python 3.11+ y del nombre del comando en Windows.

Reestructurado como plugin de Claude Code con varias skills.

- **Nuevo:** skill de entrada que enruta a `estrategia`, `identidad`, `voz`, `tokens`, `laminas`, `entrega` y `canva`.
- **Nuevo:** `marca.json` como salida, compatible con creative-architect, con esquema y validador (contraste y léxico prohibido incluidos).
- **Nuevo:** `tokens`: `tokens.json` (W3C), variables CSS, Tailwind v3 y v4, tabla de contraste y página de ejemplo.
- **Nuevo:** `laminas` sin Canva: manual en SVG, `index.html` y PDF opcional, en cinco territorios, con autotest.
- **Cambio:** Canva pasa de núcleo a módulo opcional; el resto del plugin no depende de él.
- **Cambio:** la producción de imagen se pide por intención (`imagen.generar`); sin proveedor, se entregan prompts.
- **Cambio:** el SKILL.md de 14 KB se divide por oficio; el contenido de las referencias se conserva y se reparte.
- **Arreglo:** el script de pruebas original usaba una fuente fija y `rsvg-convert` sin comprobar; la librería nueva avisa con un mensaje claro.
- **Arreglo:** los divisores y la portada no se numeran; la numeración del arquetipo D queda dentro del panel.

## 1.x

Una sola skill, `brand-kit-builder`, acoplada a Canva: entrevista, territorios, dos logos, láminas y control de créditos.
