---
name: identidad
description: Diseña el logo con exactamente dos propuestas, la paleta de cinco colores con contraste comprobado y el emparejamiento tipográfico. Úsala con «hazme el logo», «qué colores uso», «qué fuentes pongo», «mi logo se ve genérico», «necesito versiones del logo». Al aprobarse, escribe marca.json y lo valida.
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Identidad: logo, paleta y tipografía

Este paso decide todo lo demás. Requiere la entrevista confirmada y un territorio elegido (`estrategia`). Sin eso, vuelve allí.

Lee `references/logo.md`, `references/color.md` y `references/tipografia.md`. Para generar imágenes, `references/prompts-logo.md`.

## 1. Dos propuestas de logo

1. Del territorio elegido, define **exactamente dos** que se diferencien en el *tipo* de marca (emblema circular frente a wordmark con símbolo integrado), no en el acabado. Dos acabados del mismo dibujo no son dos opciones.
2. Una imagen por propuesta, con la intención `imagen.generar`. Si creative-architect está instalado, carga su skill `proveedores` y `direccion-de-arte`; si no, entrega **un prompt por propuesta** para pegar. Cada prompt describe: tipo de marca, símbolo, tratamiento (trazo a mano, geométrico, grabado), **una sola tinta**, color de tinta y de fondo, y **fondo liso**.
3. Preséntalas **a la vez**, nunca de una en una, y di cuál recomiendas en dos líneas.
4. Si piden ajustes, **no regeneres a ciegas**: pregunta qué cambia y regenera una sola vez con ese cambio explícito.

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

Siguiente: `voz`.
