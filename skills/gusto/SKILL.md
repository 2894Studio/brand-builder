---
name: gusto
description: Entrena el gusto visual de la marca sin depender de ningún servicio externo. Úsala cuando alguien diga «se ve genérico», «parece hecho por IA», «quiero que se vea más profesional / más humano / más tecnológico», «te paso referencias», «¿cuál te gusta más?», o antes de diseñar posts, banners, láminas o pantallas. Mide las referencias, fija la proporción de tonos (serio, divertido, tecnológico), aplica los patrones de cada tono, revisa el render con un crítico mecánico y registra las elecciones A/B de la persona.
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Gusto

El gusto no se «entrena» en el modelo: cada conversación empieza de cero. Se entrena **en archivos**: referencias medidas, notas de la persona, una proporción de tonos y las elecciones que ha hecho. Esta skill construye y usa ese archivo (`gusto.json`) y no necesita MCP, Taste ni Pinterest.

Lo que hace bien: medir, aplicar patrones y detectar defectos mecánicos. Lo que **no** hace: decidir qué es bonito. Esa señal es la persona; si no hay veredicto suyo, el gusto está sin entrenar aunque haya muchas referencias.

## Cuándo se carga

Después de `estrategia` y antes de `identidad` (si la marca es nueva), o en cualquier momento para piezas de contenido. Si la persona solo quiere una pieza suelta, salta al paso 4.

## Flujo

### 1. Reunir (5 min)
Pide de 6 a 8 imágenes y que las guarde en `referencias/`: **4 que le gustan, 2 que no quiere parecer, 2 de otra categoría**. Una nota suya por imagen: *qué* le gusta («el aire», «la persona con su rol»), no solo «me gusta». Si la persona no tiene imágenes, que describa marcas y tú buscas páginas públicas para que elija; no las inventes.

Las imágenes de otras marcas son referencia interna: no se reutilizan en las piezas, no se publican y no se copian en el plugin.

### 2. Medir
```
python3 skills/gusto/tools/analizar_referencias.py referencias/ --gusto gusto.json [--tipo si|no|otra]
```
Mide colores dominantes, claro/oscuro, saturación, aire (zonas lisas), detalle y cuántas familias de tono hay. Necesita Pillow (`pip install pillow`); sin él lo dice y no cambia nada. **No mide el tono ni la voz**: eso lo rellenas tú en el paso 3.

### 3. Interpretar y confirmar
Mira cada imagen. En `interpretacion` rellena `tono` (serio, divertido o tecnologico), `imagen`, `voz_del_texto` y `forma`, usando `references/tonos.md` como vocabulario. Escribe lo que **ves**, no lo que supones de la marca. Enseña a la persona tu lectura de cada una y pídele que la corrija o la confirme; solo entonces `confirmado: true` y su `nota_usuario`.

Fija la proporción de tonos con ella («serio 60, divertido 30, tecnologico 10»). Valida:
```
python3 skills/gusto/tools/gusto.py validar --gusto gusto.json
```

### 4. Aplicar
Antes de maquetar, lee `references/tonos.md` y `references/patrones-saas.md`. La proporción manda: el tono dominante decide la forma de la pieza y el secundario aparece en **un** elemento (una persona con rol, una cifra). No mezcles los tres a partes iguales.

### 5. Revisar el render (máximo 2 vueltas)
Con la pieza en HTML:
```
python3 skills/gusto/tools/critico_render.py pieza.html --ancho 1080 --alto 1440 --marca marca.json --png pieza.png
```
Corrige los **errores** y vuelve a pasarlo. Después mira la captura tú mismo con `references/criterio.md`. Dos vueltas como máximo: si sigue mal, cambia el planteamiento, no el píxel. Si no hay Playwright, dilo y revisa a ojo; **no des la pieza por revisada**.

### 6. Que elija la persona (A/B)
Si tiene dudas entre dos caminos, hazle dos variantes y pregúntale cuál prefiere y por qué (`references/protocolo-ab.md`). Regístralo:
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
