# Cómo pensar las tres direcciones

Una exploración compara. Tres direcciones que son tres acabados del mismo dibujo no son tres opciones.

## 1. Separa por tipo, no por estilo

Elige tres **tipos de marca** distintos entre: wordmark (el nombre dibujado), símbolo + nombre, emblema o sello, monograma, abstracto, pictórico. Criterio rápido:
- **Nombre corto y distintivo** → wordmark o símbolo + nombre.
- **Nombre largo o genérico** → monograma o símbolo fuerte.
- **Oficio, origen, tradición** → emblema (pero verifica la reducción).
- **Sin símbolo evidente** → abstracto, y di qué significa.
- **Objeto con giro propio** → pictórico, solo si no es el tópico de la categoría.
Al menos una de las tres debe ser la «segura» (la que funcionaría casi sin discusión) y una la «atrevida» (la que rompe la convención que el brief decidió romper).

## 2. De la idea rectora a una forma

Camino en tres saltos, escrito:
1. **Idea rectora** del brief («la prueba técnica antes del contrato»).
2. **Metáfora visual** concreta, que no sea el tópico de la categoría («una criba»: lo que pasa y lo que se queda fuera).
3. **Forma construible**: qué figuras geométricas, cuántas, dónde (un círculo con huecos en diagonal, dos rellenos). Si no puedes describirla con tres formas simples, es demasiado compleja para un logo.

## 3. Los tópicos de la categoría

Antes de proponer, lista **3 a 6 símbolos típicos** de la categoría y descártalos por escrito (una agencia de talento: apretón de manos, silueta con lupa, cerebro con nodos). Van al brief y a los prompts como «Avoid». Son lo que evita el logo genérico.

## 4. Cada dirección lleva su riesgo

Escribe qué puede fallar y cómo se comprobaría: a 32 px los detalles se funden; sin símbolo el avatar depende de la inicial; un emblema pierde legibilidad por debajo de 25 mm. Un riesgo escrito se puede comprobar; uno callado aparece cuando ya hay material impreso.

## 5. El prompt en inglés

Los modelos de imagen responden mejor en inglés. Describe **la forma, no el sentimiento**: «a solid circle with a diagonal row of small round cut-outs», no «a logo that conveys trust». Sin adjetivos de relleno (modern, clean, professional). Una sola tinta. El nombre solo si el tipo lo lleva.

## Ejemplo completo

`python3 skills/brief-logo/tools/brief_logo.py --ejemplo` imprime un brief de logo de ejemplo con tres direcciones (símbolo + nombre, wordmark y emblema) para una agencia de selección técnica.
