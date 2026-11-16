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
Los posts llevan imágenes. Pregunta con un diálogo **qué fotos hay**: «Tengo fotos propias», «Usaré un banco con licencia», «Genera imágenes con IA (se declaran)» o «Sin fotos por ahora». Según la respuesta, sigue `references/fotos.md`:
- **Propias o de banco:** si tiene clave gratuita de Pexels, `tools/buscar_fotos.py` las busca, las descarga y rellena los créditos (ver `references/fotos.md`); si no, que las guarde a mano en `fotos/` (`equipo-1.jpg`, `retrato-1.jpg`…) y rellene `fotos/creditos.md` (origen, autor, licencia, permiso de las personas).
- **Generadas:** `tools/prompts_fotos.py` escribe los prompts (con `--proveedor canva|gemini|flow`) para **Canva, Gemini o Google Flow** (gratis con cuenta Google, según cuota); también hay receta de Canva en `references/fotos.md` (con el aviso de que son sintéticas y gastan créditos) y se anotan con `origen = ia`. **Pregunta una vez, con un diálogo, si se declara en la pieza** («No, solo en el LEEME» / «Sí, en el pie de los posts» / «Sí, en el bento y en los posts»). Por defecto **no se escribe nada sobre las piezas**: solo queda en los créditos y en el `LEEME.md`. Recomiéndalo si se van a publicar, pero la decisión es de la persona.
- **Sin fotos:** recursos que se sostienen solos.

Después prepáralas (revisa resolución y créditos, recorta y marca las de IA):
```
python3 skills/lanzamiento/tools/preparar_fotos.py fotos --salida lanzamiento/fotos
```
Si da **error**, no sigas: falta una fila de créditos o una licencia.

### 2. Elegir el recurso visual de cada post
Del catálogo de `references/recursos-visuales.md`, según el mensaje **y** el tono dominante de `gusto.json`. Cada recurso lleva su prueba: una cifra con fuente, una persona con rol o una pieza de interfaz. Sin prueba, es un eslogan.

**Primero la dirección creativa, luego la herramienta.** Lee `references/direccion-creativa.md` y escribe el brief de cada pieza (3 conceptos que difieran en estructura, elegir uno). Los generadores de abajo son **andamios con buena calidad**, no la respuesta por defecto: si la salida podría ser de cualquier otra marca cambiando el logo, es una plantilla y no se entrega. Úsalos cuando el concepto elegido encaje y personalízalos; si no encaja, compón la pieza con `post_base.py`.

| Recurso | Generador |
|---|---|
| Teléfono con la interfaz del producto o servicio (qué es) | `post_telefono.py` |
| Mapa de puntos con una zona y personas a distancia real (cerca de ti) | `post_mapa.py` (necesita Node y `npm i world-atlas topojson-client d3-geo`) |
| Ventana de escritorio: panel web, curso o código (producto web, SaaS, formación) | `post_pantalla.py` (`--codigo` para marcas de código) |
| Comparativa «ellos / nosotros» (precio, modelo) | `post_comparativa.py`: **exige `--fuente`** del dato del competidor; sin fuente solo con `--ejemplo` y queda marcado |
| Cualquier otro (cifra con fuente, pasos, antes y después…) | `post_base.py` y lo construyes con los componentes |

`post_telefono.py`, `post_pantalla.py` y `post_comparativa.py` aceptan `--tema claro` (fondo blanco con bloque de color) cuando `marca.json` → `visual.estilo` o el gusto piden una marca limpia y no un campo degradado. **Elige el generador por el producto**, no por costumbre: si el producto no es una app móvil, no uses el teléfono. Los dos posts de una marca no pueden ser la misma composición que los de otra marca del mismo grupo.

Solo construyes a mano un recurso nuevo si ninguno encaja.

### 3. Exportar el logo
```
python3 skills/lanzamiento/tools/exportar_logos.py marca.json --salida lanzamiento/logo
```
SVG (el original) y PNG con fondo transparente a 3000 px. Si no hay Chromium ni `rsvg-convert`, se copian los SVG y se dice.

### 4. El bento
Elige la **variante por la categoría** (tabla en `direccion-creativa.md`): `educativa` para formación (pide `--ruta` con el recorrido real), `producto` para producto físico (pide foto), `generica` para el resto, o una rejilla propia si ninguna encaja.
```
python3 skills/lanzamiento/tools/bento.py marca.json --gusto gusto.json --fotos lanzamiento/fotos --salida lanzamiento/bento.html --lema "…" --prueba "Título|Valor" [--persona "Nombre|Rol"] [--variante generica|educativa|producto]
```
Lo que no se aporta queda como **marcador visible** («Foto real»), nunca inventado. **Sin fotos, no lo dejes con marcadores:** sustituye las tarjetas por contenido real con `--datos "Etiqueta|Valor;…"` (cifras del producto: precio, tamaño de grupo, formato) y `--puntos "a;b;c"` (lo que incluye). Revísalo con el crítico a 1920×1080.

### 5. Los dos posts
```
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

### 6. Revisar (máximo 2 vueltas por pieza)
```
python3 skills/gusto/tools/critico_render.py pieza.html --ancho 1080 --alto 1440 --marca marca.json --png pieza.png
```
Corrige los **errores**, vuelve a pasarlo y mira la captura con `../gusto/references/criterio.md`. Si tras dos vueltas sigue mal, cambia el planteamiento, no el píxel.

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
