# Sistema de láminas

Cómo se compone un brand kit que se sostiene delante de un cliente. Todo está calculado para lienzo **1920 × 1080**; para otros tamaños, escala proporcionalmente.

## Índice

1. Por qué unas láminas no se sienten profesionales
2. Rejilla
3. Escala tipográfica
4. Arquetipos de lámina
5. Firma gráfica: de dónde sale la personalidad
6. Color en la lámina
7. Invariantes de maquetación
8. Revisión antes de entregar

---

## 1. Por qué unas láminas no se sienten profesionales

Seis causas, por orden de frecuencia. Cada una tiene su arreglo.

| Síntoma | Causa | Arreglo |
|---|---|---|
| Todas las láminas parecen la misma | Un solo arquetipo repetido 13 veces | Alterna cuatro arquetipos y mete un divisor cada 3–4 láminas |
| El contenido flota arriba a la izquierda | No hay rejilla; se colocó «a ojo» | Rejilla de 12 columnas y márgenes fijos que nadie invade |
| Se ve vacía pero recargada a la vez | Un bloque de texto grande junto a mucho aire muerto | Reparte en dos zonas (texto / visual) y reduce el cuerpo a 6 líneas |
| Parece una plantilla genérica | El acento es siempre el mismo filete | Una firma gráfica elegida por territorio (sección 5) |
| Cuesta leerla | Texto sobre foto, o cuerpo a 20 px | Panel opaco siempre; cuerpo nunca por debajo de 26 px |
| No se sabe dónde estás | Sin pies ni numeración | Pie con wordmark y número en todas menos portada y divisores |

La personalidad **no** está en poner más cosas. Está en que una decisión pequeña se repita con disciplina: un tipo de filete, una forma de numerar, un modo de recortar las fotos.

---

## 2. Rejilla

- **Márgenes**: 120 a izquierda y derecha, 100 arriba y abajo. **Los respeta el contenido: texto, fichas y pies.** Los fondos no: una imagen, una textura o un bloque de color de fondo sangra hasta el borde del lienzo. Un bloque de color que se queda a 120 px del borde se lee como un error de montaje, no como una decisión.
- **Columnas**: 12 de 118 px, medianil de 24. Ancho de contenido 1680.
- **Inicio de cada columna (x)**: 120, 262, 404, 546, 688, 830, 972, 1114, 1256, 1398, 1540, 1682.

Tramos útiles:

| Tramo | x | ancho | Uso |
|---|---|---|---|
| 1–3 | 120 | 402 | Ficha estrecha |
| 1–4 | 120 | 544 | Columna de apoyo |
| 1–5 | 120 | 686 | Columna de texto (la buena para leer) |
| 1–6 | 120 | 828 | Texto ancho |
| 6–12 | 830 | 970 | Zona visual |
| 7–12 | 972 | 828 | Visual equilibrado |
| 1–12 | 120 | 1680 | Ancho completo |

Fichas repartidas a lo ancho: 3 fichas de 544 (paso 568) · 4 de 402 (paso 426) · 5 de 316 (paso 340).

**Alturas fijas** (y desde arriba):

| Elemento | y | Altura |
|---|---|---|
| Antetítulo | 120 | 20 |
| Título (banda reservada) | 160 | 170 |
| Firma gráfica | 352 | 4–12 |
| Entradilla | 384 | ~46 |
| Cuerpo | 470 | variable |
| Zona visual | 352 | 548 (hasta y=900) |
| Pie | 946 | 20 |

Que el título caiga siempre a la misma altura es lo que hace que un pase de láminas no «salte».

**La banda del título es fija: 170 px, una o dos líneas, nunca tres.** A 72 px con interlineado 1,1 dos líneas ocupan 158 px más los descendentes. Si el título no cabe en dos líneas, **acorta el título**; no bajes lo que viene debajo, porque entonces cada lámina empieza a una altura distinta. Reservar la banda completa aunque el título tenga una sola línea es lo que evita que la firma gráfica se monte sobre la segunda línea.

El borde superior de la zona visual coincide con la firma gráfica (y=352). Así el bloque de texto y el visual arrancan a la misma altura.

---

## 3. Escala tipográfica

| Rol | px | Interlineado | Peso |
|---|---|---|---|
| Display (portada) | 120 | 1,0 | Bold |
| Título de lámina | 72 | 1,1 | Bold |
| Número de sección | 160 | 1,0 | Bold |
| Entradilla | 34 | 1,35 | Regular o cursiva |
| Cuerpo | 28 | 1,5 | Regular |
| Etiqueta / dato | 22 | 1,4 | Medium |
| Pie y numeración | 20 | 1,4 | Regular |

Reglas:

- **Dos familias como máximo** en toda la presentación y en cada lámina. La jerarquía sale del tamaño y del peso.
- **45–60 caracteres por línea** en cuerpo. A 28 px eso es una columna de 686 a 828 px: por eso el texto va en el tramo 1–5 o 1–6, nunca a todo el ancho.
- **Seis líneas de cuerpo por lámina.** Lo que no quepa, va al documento de marca, no a la lámina.
- No centres párrafos. Centrar vale para una frase suelta, no para un bloque.

---

## 4. Arquetipos de lámina

Alterna estos cuatro. Un pase de 13 láminas con un divisor cada 3 o 4 respira.

**A — Portada.** Fondo a sangre (textura o color de marca). Logo centrado, de 500 a 700 px. Título display debajo o encima. Sin pie.

**B — Divisor de sección.** Fondo en el color de marca a sangre. Número de sección en grande en el tramo 1–4 y el título de la sección debajo. Tres o cuatro palabras, nada más. Sin pie.

**C — Contenido.** Antetítulo, título y firma en el tramo 1–5; cuerpo debajo. Zona visual en el tramo 6–12, entre y=330 e y=900. Es el arquetipo por defecto.

**D — Espécimen a sangre.** Imagen a 1920 × 1080 y un panel opaco del color base de 0 a 760 px de ancho, a toda la altura. Todo el texto va dentro del panel, nunca sobre la imagen. Comprueba que el objeto fotografiado se ve entero y no queda cortado por el panel.

**E — Rejilla de fichas.** Para paleta, versiones del logo o elementos. 3, 4 o 5 fichas con los pasos de la sección 2. Las fichas arrancan a la altura del cuerpo (y=470), no justo debajo de la firma: si no, pisan la entradilla. Cada ficha: muestra arriba, nombre y dato abajo, alineados a la izquierda dentro de la ficha. En la lámina de paleta, el hex va siempre visible.

---

## 5. Firma gráfica: de dónde sale la personalidad

Elige **una** fila según el territorio de la marca y aplícala en las 13 láminas. No mezcles dos.

| Territorio | Filete bajo el título | Numeración | Fondo | Recorte de foto |
|---|---|---|---|---|
| Artesanal, sello, oficio | Trazo irregular dibujado, 120 × 10 | Romana (I, II, III) | Textura de papel al 6 % | Cuadrado, bordes rectos |
| Editorial, premium | Línea de 1 px a todo el ancho del tramo | Versalitas con guiones, –01– | Color base liso | Rectángulo alto 3:4 |
| Tecnológico, moderno | Barra sólida 72 × 4 | Monoespaciada, 01 / 13 | Base con un bloque de color en el margen | Esquinas de 4 px |
| Natural, orgánico | Arco o línea ondulada, 120 de ancho | Número dentro de un círculo | Tinte del color tierra al 8 % | Esquinas de 24 px |
| Cercano, popular | Bloque de color sólido detrás de una palabra del título | Número grande en el margen exterior | Color plano saturado | Círculo o esquinas muy redondeadas |

Si el logo es un sello dibujado a mano, la firma geométrica lo desmiente. La coherencia entre el logo y la firma es lo que el cliente lee como «esto está diseñado».

**Un solo acento por lámina.** La firma gráfica consume ese acento. Si además pones un dato en color, ya van dos.

---

## 6. Color en la lámina

- Reparto 60 / 30 / 10: base, tinta, color de marca. El acento es un porcentaje mínimo, no un cuarto color.
- **Comprueba el contraste antes de usar un color para texto.** Mínimo 4,5:1 para cuerpo y 3:1 para texto de 24 px o más en negrita. Un ocre o un dorado sobre crema suele quedarse en 2,5:1: sirve para un filete, no para una palabra.
- Sobre fondo oscuro, el texto va en el color base, no en blanco puro, si la base no es blanca.
- Las fichas de paleta llevan el hex visible. Un brand kit sin hex no es un brand kit.

---

## 7. Invariantes de maquetación

[Do]
- Mantén el título a la misma altura en todas las láminas de tipo C.
- Pon pie con wordmark y número en todas menos portada y divisores.
- Deja el texto en una sola columna dentro del tramo 1–5 o 1–6.
- Usa panel opaco siempre que haya texto y foto en la misma lámina.
- Alinea el borde superior de la zona visual con el cuerpo de texto.

[Don't]
- No invadas los márgenes con texto.
- No uses tres tipografías ni tres acentos.
- No centres bloques de párrafo.
- No pongas una foto como fondo de toda la lámina con texto suelto encima.
- No estires una imagen para que cuadre: recórtala.
- No dejes una lámina con un solo bloque de texto en el centro y el resto vacío.

---

## 8. Revisión antes de entregar

Mira el pase entero en miniatura, no lámina a lámina. Comprueba:

1. ¿Hay ritmo o parecen todas iguales?
2. ¿Los títulos caen a la misma altura?
3. ¿Alguna lámina tiene más de dos tipografías o más de un acento?
4. ¿Se lee todo el texto sobre su fondo?
5. ¿La firma gráfica aparece igual en todas?
6. ¿La numeración es correlativa y está en todas las que toca?
7. ¿Alguna imagen está deformada o cortada en mal sitio?
8. ¿El logo es el mismo archivo en todas partes, incluidas las fotos y los mockups?

El punto 8 es el que más se escapa: cuando cambia el logo hay que revisar también las imágenes que lo llevan dibujado dentro.
