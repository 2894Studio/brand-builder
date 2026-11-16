# Criterio visual: cómo saber si un manual está trabajado

Un manual generado correctamente puede ser aburrido. El generador cumple las reglas de maquetación; **el criterio lo pones tú**. Esta es la lista para mirar el pase entero antes de aprobarlo.

## Señales de plantilla (si ves tres, falta trabajo)

- Todas las láminas con el mismo tamaño de letra y la misma distribución.
- Tarjetas simétricas del mismo peso, mucho aire sin intención.
- Marcadores de fotografía en lugar de imágenes.
- Ningún contraste de escala: nada es enorme ni diminuto.
- Un solo gesto repetido (el mismo filete) sin una decisión que sorprenda.
- Una portada que solo lleva el logo centrado.

## Las cinco preguntas

1. **¿Qué se mira primero** en cada lámina? Si no hay una respuesta clara, no hay jerarquía.
2. **¿Hay contraste de escala?** Un elemento al menos tres veces mayor que el siguiente.
3. **¿Qué decisión sorprende?** Algo que no esté en la plantilla: un recorte, un bloque de color, una foto a página completa.
4. **¿Hay material?** Papel, grano, fotografía real, textura. Lo plano y liso se lee como generado.
5. **¿Lo podría haber hecho otra marca** cambiando el nombre? Si sí, la lámina no es de esta marca.

## Los gestos que trae el generador

- **Portada con inicial gigante** a sangre, tono sobre tono.
- **Divisores con número recortado** por el borde.
- **Lámina de principio:** una frase a página completa. No se numera.
- **Rejilla de 2×2** cuando los valores no caben apilados.
- **Lámina de referencias**, con el atributo de cada una, si `marca.json` las trae.

`kit.json` admite `"expresivo": false` para volver al diseño sobrio.

## Lo que el generador NO puede hacer

Fotografía real, composición con desalineaciones intencionadas, recortes de imagen, una portada con una idea. Eso es trabajo de una persona de diseño o de fotografía propia: se anota en la lista de «lo que queda a mano».

## Cómo mirarlo

1. Abre `kit/index.html` en el navegador.
2. Aleja el zoom hasta ver todo el pase en miniatura: ¿hay ritmo o es una columna de láminas iguales?
3. Pasa las cinco preguntas por las tres láminas que más se verán (portada, logo, paleta).
4. Apunta tres cosas concretas que cambiarías.

Para posts, banners o pantallas, y para revisar mecánicamente una pieza HTML (solapes, contraste, fuentes, paleta), usa la skill `gusto`: `skills/gusto/tools/critico_render.py`.
