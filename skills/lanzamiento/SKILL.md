---
name: lanzamiento
description: "Produce el kit visual final de una marca: el logo en SVG y PNG, un bento (tablero de marca) y dos posts, el primero explica qué es la marca y el segundo muestra su principal atributo, ambos de forma visual. Úsala cuando la marca ya tiene logo, paleta y tipografía aprobados y la persona diga «hazme el bento», «los posts de lanzamiento», «cómo se ve mi marca en redes», «qué publico primero» o «dame las piezas finales»."
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Lanzamiento

El resultado final de usar la skill no es solo un manual: son **cuatro cosas listas para usar**. El logo, el bento de la marca y dos posts. El post 1 explica **qué es la marca** y el post 2 muestra **su principal atributo**, y los dos lo hacen con un recurso visual (una interfaz, un mapa, una cifra con su fuente, una persona con su rol), no con una frase sobre fondo de color.

Requiere `marca.json` válido con logo y paleta aprobados (`identidad`). Mejora con `gusto.json` (el tono dominante decide el recurso visual) y con `estrategia.md` (de ahí salen los dos mensajes). Sin la referencia a las skills de arriba, vuelve a ellas.

Lee `references/direccion-creativa.md` (cómo evitar que las piezas parezcan plantillas), `references/mensajes.md` (cómo elegir los dos mensajes), `references/recursos-visuales.md` (el catálogo de recursos) y `references/fotos.md` (de dónde salen las fotos), y `../brand-kit-builder/references/preguntas-interactivas.md` (cómo preguntar).

## Flujo

### 0. Comprobar el equipo
```
python3 skills/gusto/tools/comprobar_entorno.py --marca marca.json
```
Sin Chromium no se puede revisar ni exportar PNG: se entrega el HTML y se dice que **no está revisado**. Una vez, sin dramatizar.

### 0b. ¿Hay gusto entrenado?
Mira si `gusto.json` tiene referencias **confirmadas**. Si no, dilo una vez: las piezas saldrán con el tono por defecto y sin el criterio visual de la persona. Ofrece pasar antes por `gusto` (diálogo: «Entrenar el gusto ahora» / «Seguir sin referencias»). Con referencias, el tono dominante decide el recurso visual.

### 1. Elegir los dos mensajes (con la persona)
- **Post 1, qué es:** una frase de **6 a 10 palabras** que diga qué es la marca y para quién. Sale de la promesa y del manifiesto de `estrategia.md`.
- **Post 2, principal atributo:** **uno solo**, el que más la distingue (la respuesta a «qué la distingue» de la ronda 2). Si es genérico («calidad», «cercanía») no vale: repregunta qué lo hace verificable.

Propón **tres candidatos de atributo**, cada uno con el recurso visual con que lo mostrarías, y deja que la persona elija con un diálogo (una opción por candidato). **Antes, pregunta si hay fotos reales.** Sin fotos, descarta los candidatos cuyo recurso dependa de personas: el post se queda en marcadores vacíos y no explica nada. Elige entonces recursos que se sostienen solos (un mapa, una interfaz, una cifra con su fuente, pasos con filetes). Detalles y ejemplos en `references/mensajes.md`.

### 1b. Conseguir las fotos
Primero el **proveedor de imagen**: `python3 skills/brand-kit-builder/tools/proveedor_imagen.py leer`. Si no está guardado, pregúntalo **una vez** con un diálogo («¿Tienes algún proveedor de imagen para mejorar la calidad de las piezas?») y guárdalo; usa `tools/prompts_fotos.py` (toma el proveedor guardado) y `references/proveedores-imagen.md`. Con Gemini API y clave, `tools/generar_gemini.py`.
Los posts llevan imágenes. Pregunta con un diálogo **qué fotos hay**: «Tengo fotos propias», «Usaré un banco con licencia», «Genera imágenes con IA (se declaran)» o «Sin fotos por ahora». Según la respuesta, sigue `references/fotos.md`:
- **Propias o de banco:** si tiene clave gratuita de Pexels, `tools/buscar_fotos.py` las busca, las descarga y rellena los créditos (ver `references/fotos.md`); si no, que las guarde a mano en `fotos/` (`equipo-1.jpg`, `retrato-1.jpg`…) y rellene `fotos/creditos.md` (origen, autor, licencia, permiso de las personas).
- **Generadas:** `tools/prompts_fotos.py` escribe los prompts (con `--proveedor canva|gemini|flow`) para **Canva, FLORA, Gemini o Google Flow** (gratis con cuenta Google, según cuota); también hay receta de Canva en `references/fotos.md` (con el aviso de que son sintéticas y gastan créditos) y se anotan con `origen = ia`. **Pregunta una vez, con un diálogo, si se declara en la pieza** («No, solo en el LEEME» / «Sí, en el pie de los posts» / «Sí, en el bento y en los posts»). Por defecto **no se escribe nada sobre las piezas**: solo queda en los créditos y en el `LEEME.md`. Recomiéndalo si se van a publicar, pero la decisión es de la persona.
- **Sin fotos:** recursos que se sostienen solos.

Después prepáralas (revisa resolución y créditos, recorta y marca las de IA):
```
python3 skills/lanzamiento/tools/preparar_fotos.py fotos --salida lanzamiento/fotos
```
Si da **error**, no sigas: falta una fila de créditos o una licencia.

### 2. Elegir el recurso visual de cada post (que no sea siempre el mismo)

Ejecuta primero:
```
python3 skills/lanzamiento/tools/proponer_posts.py marca.json --fotos lanzamiento/fotos
```
Propone **tres combinaciones de arquetipos distintos** (mostrar el producto, contarlo con tipografía, probarlo con un dato), adaptadas a la categoría, a las fotos que haya y a si el producto es digital. **Se las enseñas a la persona con un diálogo (A, B o C) y ella elige**; tú no eliges por defecto. Reglas que no se rompen (las comprueba `kit_lanzamiento.py` y la puerta de entrega):

- Con gusto entrenado que tenga reglas de composición para posts, **los dos posts son `compuesto`** (composición a medida, `references/composicion-a-medida.md`); dos composiciones a medida valen si su disposición es distinta. Sin ese gusto: los dos posts son de **arquetipos distintos** (`ui`, `foto`, `datos`, `mapa`, `compuesto`, `expresivo:gigante|precio`, `tipografico:cifra|pasos|manifiesto`). Dos interfaces, aunque una sea móvil y otra ventana, son la misma plantilla.
- La **interfaz** (móvil o ventana) solo para productos digitales. Una academia de fotografía, una panadería o un servicio local no enseñan una pantalla.
- Cada recurso lleva su prueba: una cifra con fuente, una foto real, una interfaz real, un paso real. Sin prueba, es un eslogan.
- El tono dominante de `gusto.json` y la categoría deciden el tema (`claro` u `oscuro`); los dos posts no usan el mismo.

| Recurso | Generador | Qué hay que aportar |
|---|---|---|
| Campaña expresiva: palabra gigante recortada, foto en sello, insignia | `post_expresivo.py --modo gigante` | una foto con personalidad y una palabra clave |
| Precio enorme con beneficios (oferta, destino, curso) | `post_expresivo.py --modo precio` | precio real (o `--ejemplo`) y 3 beneficios |
| Frase enorme de la voz, con la inicial a sangre | `post_tipografico.py --modo manifiesto` | una frase del manifiesto |
| Pasos numerados (verbo + consecuencia) | `post_tipografico.py --modo pasos` | 3 o 4 pasos reales |
| Un número gigante con su explicación | `post_tipografico.py --modo cifra` | una cifra real (propia o con fuente) |
| Foto a sangre con bloque opaco y notas | `post_foto.py` | una foto buena |
| Ventana de escritorio / móvil con la interfaz | `post_pantalla.py` / `post_telefono.py` | solo productos digitales |
| Ellos / nosotros | `post_comparativa.py` | dato del competidor con **fuente** |
| Mapa de puntos | `post_mapa.py` | zona y ciudades reales (necesita Node y `npm i world-atlas topojson-client d3-geo`) |
| Cualquier otro | `post_base.py` y lo construyes con los componentes | — |

`--tema claro` (fondo de la marca con bloque de color) o `oscuro` (campo del color profundo): elige el que encaje con `visual.estilo`. **Elige el generador por el producto y la persona, no por costumbre.**

Solo construyes a mano un recurso nuevo si ninguno encaja.

### 3. Exportar el logo
```
python3 skills/lanzamiento/tools/exportar_logos.py marca.json --salida lanzamiento/logo
```
SVG (el original) y PNG con fondo transparente a 3000 px. Si no hay Chromium ni `rsvg-convert`, se copian los SVG y se dice.

### 4. Escribir el brief y montar el kit (camino principal)

**No dibujes el bento ni los posts a mano (ni como SVG ni como HTML suelto): se montan con los generadores.** Escribe `lanzamiento/brief.json` con tus decisiones (variante del bento, recurso y texto de cada post, datos reales o de ejemplo, notas) y ejecuta una sola orden:
```
python3 skills/lanzamiento/tools/kit_lanzamiento.py lanzamiento/brief.json
```
Exporta el logo, genera el bento y los dos posts, captura los PNG, pasa el crítico a cada pieza, crea el `LEEME.md` y cierra con la puerta de entrega. El formato del brief y las opciones de cada recurso están en la cabecera de `tools/kit_lanzamiento.py`. Si sale algún error, **corriges el brief** (texto más corto, otro recurso) y repites; máximo 2 vueltas por pieza.

Variante del bento por la categoría (tabla en `direccion-creativa.md`): `educativa` pide `--ruta` (el recorrido real), `producto` pide foto, `generica` para el resto. **Sin fotos, nada de marcadores:** `datos` (cifras reales del producto) y `puntos` (lo que incluye). Si ningún recurso encaja con el concepto elegido, `"recurso": "html"` con un archivo compuesto con `post_base.py`: sigue pasando por el crítico y la puerta.

Las órdenes sueltas de cada generador siguen existiendo para una pieza aislada:
```
python3 skills/lanzamiento/tools/bento.py marca.json --gusto gusto.json --fotos lanzamiento/fotos --salida lanzamiento/bento.html --lema "…" --prueba "Título|Valor" [--variante generica|educativa|producto] [--persona "Nombre|Rol"]
# teléfono con interfaz (qué es la marca)
python3 skills/lanzamiento/tools/post_telefono.py marca.json --salida lanzamiento/post-1-que-es.html --titular "Frase con <b>palabra clave</b>." \
  --pantalla "Contexto|Título" --cifra "4|perfiles" --filas "Rol|detalle;Rol|detalle;Rol|detalle" --estado "Disponible" --boton "Acción" \
  --tarjeta-izq "Etiqueta|Cifra" --tarjeta-der "Etiqueta|Cifra" --fotos lanzamiento/fotos --persona "Nombre|Rol"
# mapa de puntos (principal atributo: cerca de ti)
python3 skills/lanzamiento/tools/post_mapa.py marca.json --salida lanzamiento/post-2-atributo.html --titular "Frase <b>cerca de ti.</b>" \
  --centro "Ciudad|lon,lat" --bbox "lonMin,latMin,lonMax,latMax" --radio 200 --puntos "Ciudad|lon,lat;Ciudad|lon,lat" --destacada "Nombre|Rol|Ciudad" --fotos lanzamiento/fotos
# cualquier otro recurso: andamio y lo construyes tú
python3 skills/lanzamiento/tools/post_base.py marca.json --tipo atributo --fotos lanzamiento/fotos --salida lanzamiento/post-2-atributo.html --titular "…"
```
`post_base.py` da el andamio (campo de color, titular, logo) y **lista las fotos disponibles** en un comentario. **El recurso visual lo construyes tú** dentro de `.visual` con los componentes de `recursos-visuales.md`, y **si hay fotos, las usas**: un post con fotos disponibles y sin fotos es un post incompleto. Si la persona pidió declarar las generadas con IA, usa `--declarar-ia`; si no, no escribas nada sobre ellas ni sobre la pieza. Después, el crítico a 1080×1440.

### 4b. Contrastar con las referencias
Si `gusto.json` tiene decisiones, `kit_lanzamiento.py` deja `contacto-gusto.png` y `revision-gusto.md`: míralos y revisa **cada regla** (cumple, parcial, no cumple, no aplica y dónde se ve). Lo que no cumple se corrige en el brief y se vuelve a ejecutar. La puerta de entrega lo exige.

### 4c. Ajustes con verbos
Si la persona dice que una pieza no convence, pídele un verbo (más atrevido, más sobrio, simplificar, más humano, más técnico, más tipografía, más aire, más contraste, menos genérico) y aplica **un** cambio de `references/ajustes.md`; vuelve a ejecutar `kit_lanzamiento.py`.

### 5. Revisar (máximo 2 vueltas por pieza)
```
python3 skills/gusto/tools/critico_render.py pieza.html --ancho 1080 --alto 1440 --marca marca.json --png pieza.png
```
Corrige los **errores**, vuelve a pasarlo y mira la captura con `../gusto/references/criterio.md`. Si tras dos vueltas sigue mal, cambia el planteamiento, no el píxel.

### 6. Puerta de entrega (obligatoria)
```
python3 skills/entrega/tools/verificar_entrega.py trabajo/<fecha>-marca-<slug>/lanzamiento --marca marca.json --kits trabajo
```
Comprueba archivos, tamaños de PNG, crítico sin errores, **huellas de plantilla** (2 o más por pieza cierran la puerta salvo `tells_ok` con motivo en el brief), ausencia de marcadores y variedad. **Si sale «PUERTA CERRADA», no entregas ni dices «terminado»**: corriges y repites (máximo 2 vueltas por pieza; si no se puede, la entrega dice qué falla).

### 7. Entregar
En `trabajo/<fecha>-marca-<slug>/lanzamiento/`: `logo/`, `bento.png` y `.html`, `post-1-que-es.png` y `.html`, `post-2-atributo.png` y `.html`, y un `LEEME.md` que diga, pieza por pieza, qué es, qué es **de ejemplo** y qué queda por hacer a mano. Los PNG se capturan con `--png` del crítico; los HTML son la fuente editable.

## Reglas

- **Nada inventado se presenta como real.** Los datos, nombres, ubicaciones y personas de ejemplo se anotan en el `LEEME.md` y, en la pieza, **solo donde aparece el dato inventado** (por ejemplo, un campo «Nombre de ejemplo»). **No añadas rótulos, etiquetas ni pies sobre las fotos o las piezas que no se hayan pedido** («imagen generada con IA», «equipo de ejemplo», «personas ilustrativas»). Si la persona quiere un pie, `post_base.py --pie "…"`; si quiere declarar la IA, `--declarar-ia`.
- **Fotos:** `preparar_fotos.py` no deja pasar una foto sin origen ni licencia. Las generadas con IA se anotan siempre en `creditos.md` y en el `LEEME.md`; escribirlo sobre la pieza lo decide la persona. Aviso de una línea: no se publican como el equipo real de una empresa. Canva **no** es fuente de fotos reales. Orden de preferencia, receta de Canva y riesgos en `references/fotos.md`.
- **Datos de competidores:** nunca se inventan ni se «redondean». Una comparativa lleva fuente y fecha, o se retira (publicidad comparativa falsa es ilegal).
- **Cifras:** una cifra o la fuente es real, o es de ejemplo y lo dice. Nunca una cifra inventada con apariencia de dato.
- **Referencias de otras marcas:** se toma el atributo, nunca la marca ni su imagen.
- **Sin plantillas.** Las dos piezas del kit no comparten esquema y ninguna se parece a las de otras marcas: pasa `tools/variedad.py` y, si sale «PARECIDA», recompón.
- **Texto recortado = error.** El crítico detecta texto cortado por su contenedor; no se entrega con ese error.
- **Sin crítico, sin «revisado».** Si no se pudo pasar, la entrega lo dice.
- **Una pieza, un mensaje.** Si un post intenta explicar dos cosas, se parte en dos. El post 1 no debe adelantar el atributo del post 2.
- **Un post con más marcadores que contenido no está terminado:** si más de un tercio de la superficie son marcadores, cambia de recurso.
