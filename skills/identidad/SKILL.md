---
name: identidad
description: "Diseña el logo con exactamente dos propuestas, la paleta de cinco colores con contraste comprobado y el emparejamiento tipográfico. Úsala con «hazme el logo», «qué colores uso», «qué fuentes pongo», «mi logo se ve genérico», «necesito versiones del logo». Al aprobarse, escribe marca.json y lo valida."
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Identidad: logo, paleta y tipografía

Este paso decide todo lo demás. Requiere la entrevista confirmada y un territorio elegido (`estrategia`). Sin eso, vuelve allí.

Lee `references/logo.md`, `references/color.md` y `references/tipografia.md`. Para generar imágenes, `references/prompts-logo.md`.

## 0. Antes de dibujar: qué enseñan las referencias

Si existe `gusto.json` (o la persona nombró marcas de referencia, p. ej. «estilo Maze» o «como Notion»), **extrae por escrito, en 3 líneas, antes de proponer nada**:

1. **Tratamiento del nombre**: caja alta o minúsculas, peso, tracking, si el nombre va solo o con símbolo.
2. **Morfología del símbolo**: trazo plano, forma sólida, símbolo integrado en una letra, o sin símbolo.
3. **Estilo gráfico de la categoría**: 2D plano, editorial, ingeniería… y qué **prohíben** esas referencias (p. ej. sin 3D, sin degradados dentro del vector, sin sellos institucionales).

Las dos propuestas heredan esas 3 líneas; lo que la persona pidió en palabras («un libro con código») se resuelve **dentro** de ese lenguaje, no con el icono literal. Si una propuesta contradice las referencias, no se enseña.

## 1. Dos propuestas de logo

1. Del territorio elegido, define **exactamente dos** que se diferencien en el *tipo* de marca (emblema circular frente a wordmark con símbolo integrado), no en el acabado. Dos acabados del mismo dibujo no son dos opciones.
2. Una imagen por propuesta, con la intención `imagen.generar`. Si creative-architect está instalado, carga su skill `proveedores` y `direccion-de-arte`; si no, entrega **un prompt por propuesta** para pegar. Cada prompt describe: tipo de marca, símbolo, tratamiento (trazo a mano, geométrico, grabado), **una sola tinta**, color de tinta y de fondo, y **fondo liso**.
3. Preséntalas **a la vez**, nunca de una en una, y di cuál recomiendas en dos líneas.
4. Enseña **primero** los dos logos y luego pregunta cuál con un diálogo (A, B, «ninguno, hay que ajustar»). Si piden ajustes, **no regeneres a ciegas**: pregunta en el chat qué cambia y regenera una sola vez con ese cambio explícito.

**Sí:** comprueba el logo a 25 mm y en una sola tinta · busca anterioridades del nombre (OEPM, EUIPO, WIPO) y dominio; si no puedes, déjalo anotado como pendiente.
**No:** no propongas una tercera «por si acaso» · no des por bueno un logo que solo funciona en grande · no uses el acento para texto pequeño.

## 2. Paleta: cinco colores con papel

> En Windows, `python3` suele ser `python` o `py`. Necesita Python 3.11 o superior.

Base, tinta, marca, acento y neutro, cada uno con **nombre, hex y papel**. Comprueba el contraste con el hex real, no de memoria:

```
python3 tools/contraste.py --base "#F3F4F6" "#2F4BD8" "#00C27A" "#14181F"
```

Si el acento no llega a 4,5:1 sobre la base, dilo: ese color sirve para filetes, iconos grandes o fondos, no para texto. Elige el color **contra la categoría**, no con una psicología de color que no sostiene nada.

## 3. Tipografía

Dos familias (títulos y texto) con contraste real de registro, o una sola superfamilia. Comprueba la eñe, los acentos, los números y la **licencia** (uso comercial, web y producto).

## 4. Aprobación y `marca.json`

Logo y paleta se aprueban **juntos**. Con la elegida:

1. Pide el archivo del logo en SVG si existe; si solo hay imagen, quita el fondo y guarda en `trabajo/<fecha>-marca-<slug>/logo/`. Registra cada versión (`principal`, `invertida`, `monocroma`, `simbolo`, `reducida`).
2. Completa `marca.json`: `visual.colores` (roles `primario`, `fondo`, `acento`, `texto`; el neutro va en `brandKit.neutro`, porque el contrato no tiene rol para él), `visual.estilo` (técnica: luz, grano, paleta, encuadre; no adjetivos), `tipografia` y `brandKit.logo`.
3. Valida: `python3 ../tokens/tools/validar_marca.py marca.json`. Corrige los errores; lee los avisos.

## 4b. Sistema de imagen: que la marca no sea sosa

Logo, paleta y tipografía no bastan: una marca que solo tiene eso sale plana. Antes de cerrar `identidad`, decide y anota en `marca.json` → `visual.estilo` (y en `kit.json` → `fotografia`):

1. **Fotografía:** qué sujetos (personas en su contexto real, el producto en uso, el lugar), encuadre, luz y color, y **de dónde saldrán** (propias, banco con licencia o generadas; ver `lanzamiento/references/fotos.md`). «Sin fotos» solo si la persona lo decide, y entonces el recurso protagonista es otro (interfaz, cifra, mapa).
2. **Gráfico firma:** un elemento propio derivado del logo o de la idea de marca (una forma recortada, un patrón, un trazo, un indicador) que aparezca en todas las piezas. No es un degradado ni una caja redondeada genérica.
3. **Un momento de color:** dónde ocupa el color la pieza entera (un bloque a sangre, un fondo de portada) y dónde se queda blanco.

Pregúntalo contra las referencias de `gusto.json`: si las referencias tienen fotografía y la marca no, está mal. Una marca para empresas o técnica también lleva personas y contexto real, no solo iconos.

## 4c. Opcional: explorar tres direcciones con FLORA

Si la persona tiene el conector de FLORA con saldo y quiere explorar direcciones para el sistema de imagen, `references/direccion-flora.md` explica cómo pasar el logo aprobado por la técnica **Logo to Brand Identity** (tres tableros de identidad, de pago: pide el presupuesto en USD y espera el sí). Los tableros son inspiración: se toma la paleta **medida** y el estilo de imagen, nunca los textos que dibuja el modelo, y la estrategia manda sobre lo que infiera del logo. Sin FLORA o sin saldo, se salta sin más.

## 5. Que el logo se vea igual en todas partes

Si el nombre del logo es **texto vivo** (usa una fuente), el archivo no es seguro tal cual: dentro de `<img>`, en el manual o sin conexión sale en una fuente de reserva, y si usa una clase CSS compartida dos logos en la misma página se pisan. Antes de dar el logo por cerrado:

```
python3 tools/incrustar_fuente.py <carpeta-logo>/*.svg --google <Familia>
```

Incrusta la fuente en el propio SVG y pasa las clases a atributos. Con `pip install fonttools` el archivo queda en unos 5 KB; sin él, incrusta la fuente completa (unos 140 KB). Comprueba la licencia de la fuente. La versión definitiva sigue siendo convertir a contornos en un editor vectorial.

**Mira el resultado renderizado** antes de presentarlo: ábrelo en un navegador o dilo claramente si no puedes verlo. Un logo que nadie ha visto no se presenta como terminado.

Siguiente: `voz`.
