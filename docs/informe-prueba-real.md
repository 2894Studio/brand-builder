# Informe de la prueba real (Findpro)

Recorrido completo de la versión 2.1.0 con una marca nueva, ejecutando las skills con el modelo en una instalación aislada, como lo haría un alumno. Marca de prueba: **Findpro**, una firma de equipos de IA para corporaciones europeas. Resultado: el camino funciona de punta a punta, y la prueba destapó **diez defectos reales**, de los que se corrigieron ocho en la versión 2.1.1.

## Cómo se hizo

- **Instalación:** brand-kit-builder 2.1.0 desde el ZIP, creative-architect 1.0.1 y motion-architect 0.2.0 con su instalador real, en una configuración aislada. En Linux el instalador de motion-architect exigió `yt-dlp`, que había que aportar.
- **Conversación:** una sesión real de Claude Code, reanudada entre rondas. La persona de prueba contestó la entrevista y eligió territorio, logo y estilo. **Algunas respuestas las escribió el asistente** (la aclaración de las tres referencias, la confirmación del resumen, el ajuste del logo y la aprobación del guion de video). Están registradas aparte y no son criterio de un alumno real.
- **Limitación:** una sola persona y una sola marca. No se probó en Windows ni en macOS.

## Resultado por tramo

| Tramo | Resultado | Turnos | Coste |
|---|---|---|---|
| Entrevista y territorios | Pasa | 17 | $1,24 |
| Identidad (logo, paleta, tipografía) | Pasa con defectos | 44 | $2,65 |
| Voz | Pasa | 9 | $1,27 |
| Tokens | Pasa | 11 | $1,40 |
| Manual de marca | Funciona con defectos de maquetación | 21 | $1,68 |
| Entrega | Pasa | 26 | $2,10 |
| Post estático: prompt | Pasa | 7 | $0,16 |
| Post estático: imagen en Canva | Pasa; **falta el montaje del texto** | — | 1 de 4 créditos |
| Video con motion-architect | Pasa (MP4 de 7 s) | 19 | $0,48 |
| **Total** | | | **~$11,00** |

Los costes son los de cada llamada del modelo; el consumo real depende del modelo, del plan y de la longitud de cada conversación.

## Lo que funcionó

- **La entrevista cumple su diseño:** tres rondas más una aclaración justificada, sin imágenes antes de confirmar, sin adelantar soluciones, y señaló por sí sola dos tensiones («rápido» frente a «exclusiva»; «cercana» frente a «elegante»).
- **Territorios anclados fuera de la categoría** y respeto de la regla «que no parezca hecho por IA».
- **Control de contraste honesto:** los cinco contrastes declarados coincidieron con la medición independiente, y la skill oscureció el rojo (de 4,17:1 a 4,84:1) cuando no valía para texto.
- **`marca.json` válido** en la raíz, con el contrato de creative-architect; creative-architect lo leyó cuando se le pidió explícitamente.
- **La skill se corrige sola cuando ve un problema:** al generar los tokens detectó que el radio redondeado chocaba con «elegante» y propuso cambiar el territorio.
- **motion-architect** leyó la marca importada, escribió un guion visual, esperó aprobación y renderizó un MP4 de 1080×1920, 7 s, 30 fps; además **quitó por su cuenta el degradado** de un fondo para respetar «superficies planas».
- **El paso de referencias (2.1.1) funciona con el modelo:** con tres marcas sin atributo, **se negó a anotarlas**, avisó de que una era justo el competidor declarado, las contrastó con el estilo de la marca y pidió las cinco que faltaban para las ocho del método (3 turnos, ~$0,11).
- **Honestidad:** la skill avisó de lo que no podía hacer (renderizar sus logos, generar el PDF, arreglar el aspecto «sencillo» del manual).

## Defectos encontrados

| # | Defecto | Dónde | Estado |
|---|---|---|---|
| 1 | El logo con texto vivo cargaba su fuente de Google Fonts: dentro de `<img>`, en el manual o sin conexión salía en una fuente de reserva, sin la ligadura «fi» | Identidad | **Corregido:** `incrustar_fuente.py`, verificado con la red bloqueada |
| 2 | Clases CSS compartidas (`.nombre`) en los SVG: dos logos en la misma página se pisan | Identidad | **Corregido** (mismo script) |
| 3 | La skill entregó los logos sin haberlos visto renderizados | Identidad | Corregido en las instrucciones; no se puede automatizar del todo |
| 4 | Primera propuesta de logo incoherente con su propia tipografía (trazo redondeado frente a serif) | Identidad | Pendiente: depende del modelo |
| 5 | Las tarjetas de valores se salían de la lámina con 4 valores | Manual | **Corregido:** rejilla 2×2; el autotest lo cubre |
| 6 | Doble punto en «frases cortas..» | Manual | **Corregido** |
| 7 | «No decimos» mostraba las palabras genéricas, no las del sector | Manual | **Corregido** |
| 8 | La licencia de las fuentes salía como una frase larga y cortada | Manual | **Corregido** |
| 9 | La firma gráfica `cercano` (esquinas de 16 px) para una marca elegante | Tokens/Manual | Detectado por la skill; la elección del territorio sigue siendo manual |
| 10 | El nombre «Findpro» ya existe como empresa de recursos humanos; la skill solo dijo «es descriptivo» | Estrategia | **Corregido en las instrucciones** (búsqueda web del nombre); no es asesoría legal |

Además: el campo `style` del puente a motion-architect salía con un «;» final (**corregido**), y el conector de Canva **solo deja en disco una miniatura de 160×199 px**; la imagen completa hay que descargarla desde su enlace (**documentado**).

## Sobre el gusto visual

La persona de prueba juzgó que el manual **«se siente muy IA y sencillo»**, y la skill lo admitió: dijo que no lo puede automatizar. Lo que lo hacía parecer generado: misma escala de letra en todo, tarjetas simétricas, aire sin intención, marcadores en lugar de imágenes, y ninguna decisión que sorprenda.

En la versión 2.1.1 se aborda de tres formas, **sin pretender sustituir a un diseñador**:

1. **Paso de referencias** en estrategia: ocho referencias (4 que sí, 2 que no, 2 de otra categoría) con el **atributo** concreto, guardadas en `marca.json`.
2. **Láminas más expresivas:** inicial gigante a sangre en la portada, números recortados en los divisores, lámina de principio a página completa y lámina de referencias.
3. **Criterio visual** (`criterio-visual.md`): las cinco preguntas y la lista de señales de plantilla para juzgar un manual.

Lo que sigue sin poder hacer el plugin: fotografía real, composición con desalineaciones intencionadas y una portada con una idea propia.

## Hallazgo sobre el consumo

| | Turnos | Coste por turno |
|---|---|---|
| Sesiones nuevas (post, vídeo) | 5–14 | $0,02–0,03 |
| Tramos finales de la sesión larga | 9–26 | $0,08–0,14 |

Con una sola ejecución por caso y tareas distintas no es una comparación limpia, pero apunta en la dirección que ya enseñábamos: **una conversación larga arrastra todo lo anterior en cada mensaje**. La guía de ahorro recoge la regla de abrir una sesión nueva por pieza.

## Qué no se pudo verificar

- Windows y macOS.
- Una segunda marca o una segunda persona.
- La composición final del post estático: **queda pendiente de que se descargue la imagen de Canva** (el conector no la entrega a resolución completa).
- Un `/motion` con un logo real y con imágenes (el cierre del video usa el nombre en texto).
- El PDF, porque falta `rsvg-convert` en el entorno.
- El repositorio de GitHub: no existía cuando se hizo esta prueba. Se publicó después (2894Studio/brand-kit-builder) y la instalación desde GitHub se verificó en una configuración limpia (versión 2.4.0).
