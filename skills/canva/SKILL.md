---
name: canva
description: Opcional. Monta o publica el brand kit en Canva controlando el gasto de créditos de generación. Úsala solo cuando la persona tenga Canva conectado y lo pida («pásalo a Canva», «brand kit en Canva», «quiero editarlo en Canva»). No es necesaria para ninguna otra skill del plugin.
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Canva (opcional)

Es la skill del plugin que nombra una herramienta concreta; las demás hablan en intenciones. El kit base ya existe sin Canva (`laminas`); esta skill sirve para quien quiere **editarlo allí** o dejar la marca nativa en su Brand Kit. Si no hay conector de Canva disponible, dilo y quédate con el kit SVG/HTML: no es un bloqueo.

Lee `references/canva-creditos.md` **antes de la primera llamada**: recetas del conector, trampas conocidas y qué no puede hacer.

## Presupuesto

**8 generaciones de imagen o menos** para un kit completo con mockups: logo 2 · fondo de portada 1 · elementos y fotografía 2 · mockups 2–3. Si vas a pasarte, dilo antes de gastar y ofrece recortar.

## Reglas de ahorro (resumen)

- Sube el logo **una vez** y reutiliza su identificador; no repitas la ruta vectorial por lámina.
- Genera los productos **en blanco** y superpón el logo.
- Lee los diseños filtrando campos y páginas, nunca enteros.
- Agrupa las ediciones en una transacción y confirma una sola vez.
- Ante un encuadre malo, recorta y recoloca; no regeneres.
- Fondos: color plano o una textura reutilizada.

## Qué cambia respecto al kit SVG

Las medidas, la rejilla, las firmas gráficas y los arquetipos son los mismos (`../laminas/references/sistema-laminas.md`): la composición no cambia, cambia el soporte. Los valores salen de `marca.json` y `kit.json`; no los reinventes.

## Límites conocidos

El conector no crea ni modifica Brand Kits, no elige tipografía al crear texto nuevo y no borra páginas. Qué vía sirve para cada sección del Brand Kit está en la sección 7 de `references/canva-creditos.md`. Las secciones de recursos solo aceptan archivos del disco: prepara el paquete de `entrega`, no dejes instrucciones sueltas.

Estas notas describen el conector tal como se documentó; **no están verificadas de nuevo en esta versión del plugin**. Si una llamada falla distinto, manda lo que dice el conector.
