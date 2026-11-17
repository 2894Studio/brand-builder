---
name: gusto
description: "Entrena el gusto visual de la marca sin depender de ningún servicio externo. Úsala cuando alguien diga «se ve genérico», «parece hecho por IA», «quiero que se vea más profesional / más humano / más tecnológico», «te paso referencias», «¿cuál te gusta más?», o antes de diseñar posts, banners, láminas o pantallas. Mide las referencias, fija la proporción de tonos (serio, divertido, tecnológico), aplica los patrones de cada tono, revisa el render con un crítico mecánico y registra las elecciones A/B de la persona."
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Gusto

El gusto no se «entrena» en el modelo: cada conversación empieza de cero. Se entrena **en archivos**: referencias medidas, notas de la persona, una proporción de tonos y las elecciones que ha hecho. Esta skill construye y usa ese archivo (`gusto.json`) y no necesita MCP, Taste ni Pinterest.

Lo que hace bien: medir, aplicar patrones y detectar defectos mecánicos. Lo que **no** hace: decidir qué es bonito. Esa señal es la persona; si no hay veredicto suyo, el gusto está sin entrenar aunque haya muchas referencias.

## Cuándo se carga

Después de `estrategia` y antes de `identidad` (si la marca es nueva), o en cualquier momento para piezas de contenido. Si la persona solo quiere una pieza suelta, salta al paso 4.

## Flujo

### 0. Comprobar el equipo (2 min, una vez)
Antes de prometer una revisión visual, comprueba qué puede hacer este ordenador:
```
python3 skills/gusto/tools/comprobar_entorno.py --marca marca.json
```
Abre una página en Chromium de verdad y dice qué capacidades hay (medir referencias, revisar piezas, contraste sobre degradados, mapas) y qué instalar para el resto. Lo que falte se dice **una vez** y se sigue con lo que sí hay; una pieza sin crítico se entrega como «no revisada mecánicamente».

### 1. Reunir (5 min)
Las referencias las aporta **la persona**: no las inventes ni las elijas por ella. **Si es para el logo, bastan 3** (2 que le gustan y 1 que no quiere parecer). Para entrenar el gusto de toda la cadena visual, pide de 6 a 8 imágenes y que las guarde en `referencias/`: **4 que le gustan, 2 que no quiere parecer, 2 de otra categoría**. Si no sabe dónde buscarlas, dale **las 3 palabras clave generales** para Behance, Pinterest y Dribbble, deducidas del brief (`references/palabras-clave.md`; solo da más si las pide), y `references/buscar-referencias.md` (con o sin MCP). Una nota suya por imagen: *qué* le gusta («el aire», «la persona con su rol»), no solo «me gusta». Si la persona no tiene imágenes, que describa marcas y tú buscas páginas públicas para que elija qué captura guardar; no inventes atributos de marcas que no has visto.

Las imágenes de otras marcas son referencia interna: no se reutilizan en las piezas, no se publican y no se copian en el plugin.

**Forma fácil:** `python3 skills/gusto/tools/etiquetador.py` abre una interfaz para cargar las imágenes, etiquetarlas (me gusta / no / otra), escribir la nota y las decisiones por dimensión, y guardarlo todo en `referencias/` y `gusto.json` (o `etiquetador.html` + `importar_etiquetado.py` si no hay servidor). Ver `references/entrenar.md`.

### 2. Medir
```
python3 skills/gusto/tools/analizar_referencias.py referencias/ --gusto gusto.json [--tipo si|no|otra]
```
Mide colores dominantes, claro/oscuro, saturación, aire (zonas lisas), detalle y cuántas familias de tono hay. Necesita Pillow (`pip install pillow`); sin él lo dice y no cambia nada. **No mide el tono ni la voz**: eso lo rellenas tú en el paso 3.

### 3. Interpretar y confirmar
Mira cada imagen. En `interpretacion` rellena `tono` (serio, divertido o tecnologico), `imagen`, `voz_del_texto` y `forma`, usando `references/tonos.md` como vocabulario. Escribe lo que **ves**, no lo que supones de la marca. Enseña a la persona tu lectura de cada una y pídele que la corrija o la confirme (diálogo con «es correcto» / «hay que ajustar», hasta 4 imágenes por diálogo; la nota de qué le gusta va en el chat); solo entonces `confirmado: true` y su `nota_usuario`.

Fija la proporción de tonos con ella (tono dominante en un diálogo: serio, divertido o tecnológico; el reparto lo propones tú y ella lo corrige) («serio 60, divertido 30, tecnologico 10»). Valida:
```
python3 skills/gusto/tools/gusto.py validar --gusto gusto.json
```

### 3b. Extraer decisiones transferables (obligatorio, es lo que hace que las referencias sirvan)
Para cada referencia «sí» escribe **qué copio y qué no**, por dimensión, con `gusto.py decision` (ver `references/entrenar.md`): al menos **2 dimensiones distintivas** (nombre, símbolo, tipografía, imagen, composición, firma) además de forma y color. Las referencias «no» dan decisiones a evitar. `gusto.py reglas` lista R1…Rn. Sin decisiones, las referencias solo eligen un tono y las piezas salen genéricas.

### 4. Aplicar
Antes de maquetar, lee `references/tonos.md` y `references/patrones-saas.md`. La proporción manda: el tono dominante decide la forma de la pieza y el secundario aparece en **un** elemento (una persona con rol, una cifra). No mezcles los tres a partes iguales.

### 4b. Mirar antes de diseñar
Antes de componer un post, un bento o un logo: `contacto_referencias.py --para post|bento|logo|web` deja una hoja con **solo** las referencias y reglas de ese destino. Ábrela, escribe el concepto (qué reglas traduces y cómo) y diseña (`lanzamiento/references/composicion-a-medida.md`).

### 5a. Contrastar con las referencias
Con las piezas hechas: `python3 skills/gusto/tools/contacto_referencias.py --gusto gusto.json --referencias referencias/ --piezas lanzamiento/ --salida lanzamiento/` (`kit_lanzamiento.py` ya lo hace). Mira `contacto-gusto.png` y rellena `revision-gusto.md` regla por regla; lo que no cumple se corrige.

### 5. Revisar el render (máximo 2 vueltas)
Con la pieza en HTML:
```
python3 skills/gusto/tools/critico_render.py pieza.html --ancho 1080 --alto 1440 --marca marca.json --png pieza.png
```
Corrige los **errores** y vuelve a pasarlo. Después mira la captura tú mismo con `references/criterio.md`. Dos vueltas como máximo: si sigue mal, cambia el planteamiento, no el píxel. Si no hay Playwright, dilo y revisa a ojo; **no des la pieza por revisada**.

### 6. Que elija la persona (A/B)
Si tiene dudas entre dos caminos, hazle dos variantes, enséñalas y pregúntale cuál prefiere con un diálogo (una opción por variante) y el porqué en el chat (`references/protocolo-ab.md`). Regístralo:
```
python3 skills/gusto/tools/gusto.py ab --a serio --b tecnologico --elige a --motivo "se entiende antes"
```
Cada elección mueve la proporción 10 puntos como máximo. Es una heurística visible, no aprendizaje.

## Qué entregas

- `gusto.json` actualizado y validado.
- Las piezas, con la lista de errores y avisos del crítico, y qué corregiste.
- Una línea honesta de lo que **no** está resuelto (foto real, cifra con fuente, texto de ejemplo).

## Reglas

- Una referencia sin atributo no cuenta. Repregunta una vez; si sigue vacía, queda como «pendiente».
- Nunca des como gusto de la persona lo que dedujiste de las imágenes sin confirmarlo.
- Las piezas llevan datos reales o un marcador visible («ejemplo»); nunca cifras inventadas presentadas como ciertas.
- Colores y fuentes salen de `marca.json`; si una pieza necesita un tinte nuevo, se añade a la marca primero.
