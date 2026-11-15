# Canva: recetas y control de gasto

Lo que cuesta caro y cómo evitarlo, más las trampas del conector que hacen perder llamadas.

## Índice

1. Qué cuesta y qué no
2. Las ocho reglas de ahorro
3. Presupuesto por fase
4. Recetas del conector
5. Trampas conocidas
6. Qué no puede hacer el conector
7. Dejar la marca nativa en el Brand Kit

---

## 1. Qué cuesta y qué no

| Operación | Coste | Comentario |
|---|---|---|
| Generar imagen | Alto | Es el gasto real. Cuéntalas. |
| Quitar fondo | Bajo | No es una generación |
| Leer un diseño entero | Medio | Devuelve todos los elementos de todas las páginas; se dispara con 13 láminas |
| Editar con una ruta vectorial larga | Medio | La ruta de un sello ocupa unos 5 KB **cada vez** que se emite |
| Editar texto, color, posición | Bajo | Barato; úsalo sin miedo |
| Confirmar una transacción | Bajo | Una sola al final |

La factura se va en dos sitios: **generar imágenes de más** y **repetir contenido largo** (rutas vectoriales y lecturas completas).

---

## 2. Las ocho reglas de ahorro

1. **Pregunta por los mockups antes de generar nada.** Un «no» ahorra dos o tres generaciones.
2. **Dos opciones de logo.** Una generación cada una.
3. **Sube el logo una vez y reutiliza su identificador de recurso.** Colocarlo con ese identificador cuesta una fracción de lo que cuesta volver a dibujar la ruta vectorial en cada lámina. Reserva la ruta vectorial para **una** lámina: la de versiones del logo.
4. **Genera los productos en blanco.** Nunca pidas una escena con el logo ya dibujado dentro: cuando el logo cambie, hay que regenerar la escena entera. Pide el envase, el vaso o el rótulo sin rotulación alguna y superpón el logo como elemento.
5. **Lee filtrando.** Pide solo los campos y las páginas que necesitas, y miniaturas solo de las páginas que vas a revisar.
6. **Agrupa.** Varias ediciones sobre páginas distintas dentro de la misma transacción, y una sola confirmación al final.
7. **Ante un encuadre malo, recorta.** Recolocar, redimensionar y recortar es barato; regenerar es caro.
8. **Fondos de color plano o una textura reutilizada.** No una imagen por lámina.

---

## 3. Presupuesto por fase

Objetivo para un kit completo: **8 generaciones o menos**.

| Fase | Generaciones | Qué |
|---|---|---|
| Logo | 2 | Una por propuesta |
| Portada | 1 | Textura o fondo, reutilizable en otras láminas |
| Elementos y fotografía | 2 | Dos ejemplos fijan el estilo |
| Mockups | 2–3 | Solo productos en blanco |
| Ajustes | 0 | Se resuelven recortando y recolocando |

Si el usuario pide una ronda más de logos, dile cuánto suma antes de lanzarla.

---

## 4. Recetas del conector

**Transacciones.** Abre la transacción al leer el diseño, aplica las ediciones manteniéndola abierta y confirma una sola vez al final. Si algo sale mal, se descarta entera.

**Páginas.** Se numeran desde 1. Si reordenas una página, los índices de las siguientes se desplazan: vuelve a leer antes de seguir editando por índice.

**Texto nuevo.** Sale con la tipografía por defecto, pequeña y negra. Hay que darle formato después. Para conservar la tipografía de marca de una plantilla, es mejor **reemplazar el texto de un elemento existente** que crear uno nuevo.

**Formas.** Acepta rutas con comandos relativos y varios subtrazados, y los huecos se rellenan bien. No admite curvas cuadráticas: conviértelas a cúbicas o a arcos.

**Orden de capas.** Todo lo que se inserta se coloca encima. Un panel nuevo tapa el texto que había debajo: hay que subir el texto al frente, o mandar el panel al fondo.

**Recortes.** Cambiar la imagen de un elemento o redimensionarlo conserva el recuadro de recorte anterior. Después de cambiar tamaño o imagen, restablece el recorte.

**Opacidad.** Bajar la opacidad de una textura la aclara y la desatura sin gastar otra generación.

**Traer diseños de fuera.** Para incorporar un diseño propio a otra hoja, usa la operación de combinar diseños, una por llamada; las páginas conservan su tamaño.

**Verificación.** Después de editar, compara la miniatura con la anterior y revisa los valores devueltos. No des por buena una edición sin mirarla.

---

## 5. Trampas conocidas

- **Plantillas con contenido de ejemplo.** Revisa todas las láminas: suelen esconder logotipos, fechas y lemas inventados que no son de la marca.
- **Un logo con su fondo parece una pegatina.** Quita el fondo y baja un poco la opacidad al colocarlo sobre fotografía.
- **Títulos que se parten.** Un título grande en una columna estrecha salta a dos líneas y pisa lo de abajo. Baja el cuerpo antes de recolocar.
- **URL firmadas de exportación.** No sirven para volver a subir un recurso; el import falla.
- **Imágenes con el logo dibujado dentro.** Cuando cambie el logo hay que regenerarlas. Audita también las fotos y los mockups, no solo los elementos sueltos.
- **Paneles que tapan el objeto.** Al poner un panel de texto sobre una foto a sangre, comprueba que el objeto fotografiado sigue viéndose entero.
- **Mockups a medias.** Si el soporte real lleva nombre, líneas de marca y peso, el mockup los lleva. Con el logo solo, está incompleto.

---

## 6. Qué no puede hacer el conector

Dilo claro en vez de intentarlo varias veces:

- **No escribe en las secciones del Brand Kit** (colores, fuentes, voz, logos). La sección 7 explica qué vía sirve para cada una.
- **No elige tipografía** al crear texto nuevo. Las fuentes de marca se aplican a mano, o se reutilizan elementos que ya las tengan.
- **No borra páginas.** Se pueden reordenar, no eliminar.
- **No da perspectiva.** Un logo superpuesto sobre un vaso o una bolsa va plano. Es una aproximación válida para presentar, no una maqueta de imprenta.
- **No exporta en alta a un archivo local** que se pueda procesar aquí: para vectorizar un logo con calidad hace falta que la persona lo exporte y lo adjunte.

---

## 7. Dejar la marca nativa en el Brand Kit

El Brand Kit de Canva tiene secciones propias: Pautas, Plantillas de la marca, Logos, Colores, Fuentes, Voz de la marca, Fotos, Componentes, Elementos gráficos, Iconos y Gráficos. Cada una se alimenta por una vía distinta, y conviene saber cuál antes de prometer nada.

| Sección | Vía | Automatizable |
|---|---|---|
| Plantillas de la marca | `publish-brand-template` con el id del diseño | Sí, una llamada |
| Colores | Navegador | Sí, con automatización de navegador |
| Fuentes | Navegador, sobre los estilos de texto del kit | Sí, igual |
| Voz de la marca | Navegador, campo de texto de 500 caracteres | Sí, igual |
| Pautas | Navegador, documento de Canva con plantilla | Sí, con cuidado (ver abajo) |
| Logos, Fotos, Componentes, Elementos gráficos, Iconos | Solo «Subir archivos» | **No** |

**Las cinco secciones de recursos son el muro.** Solo ofrecen subir un archivo del disco; no hay forma de elegir desde las subidas que ya existen en la cuenta. El campo de archivo está en el DOM cuando el menú está abierto, pero una subida automatizada necesita la aprobación de una persona. No hay rodeo: o la persona arrastra el archivo una vez, o esas secciones se quedan vacías.

**La ruta que sí cierra el círculo.** Para que el archivo del logo entre en Canva sin intervención:

1. Aloja los archivos del logo en una URL pública (por ejemplo, el repositorio de la marca).
2. `upload-asset-from-url` los importa a las Subidas de la cuenta. Una llamada por archivo.
3. Monta las láminas con esos recursos.
4. `publish-brand-template` publica el diseño como plantilla de marca.

Así el logo queda dentro del Brand Kit **como plantilla**, que es lo que el equipo va a usar de verdad para crear piezas, aunque la ranura «Logos» siga vacía.

**Aviso sobre la plantilla de marca.** `publish-brand-template` publica a nivel de organización y no deja elegir a qué Brand Kit se asocia: hay que vincularla después desde el menú de la plantilla, «Añadir al Kit de Marca». Antes de publicar, comprueba si ya existe una plantilla del mismo diseño, porque publicar otra vez crea un duplicado en lugar de actualizar. Para borrar un duplicado: lista de plantillas, menú de la tarjeta, Eliminar. El borrado no se puede deshacer y no afecta a los diseños creados a partir de ella.

**El documento de Pautas.** Es un documento de Canva, no un contenedor. Su menú solo ofrece editar, descargar como PDF y vaciar el contenido: **no se puede sustituir por un diseño que ya exista**, así que el deck del kit no puede ocupar ese sitio. El deck va en «Plantillas de la marca», que es su sección, y las Pautas se quedan para las reglas escritas, que es lo que de verdad se consulta y se descarga en PDF.

Al pulsar «Añadir pautas», Canva abre un documento largo con plantilla, texto de relleno y marcadores de imagen. Para rellenarlo por navegador:

[Do]
- Selecciona **párrafo a párrafo con triple clic** y escribe encima.
- Comprueba con una captura que la selección es solo ese párrafo antes de escribir.
- Deja los marcadores de imagen como están si no puedes subir archivos.

[Don't]
- No uses seleccionar todo: unas veces coge el párrafo y otras el documento entero, y sobrescribe la plantilla.
- No escribas dos puntos seguidos de espacio dentro de ciertos bloques: abre el selector de emojis y el texto acaba descolocado.
- No des por buena una escritura sin mirarla: el texto puede caer en otro elemento y partirse en letras sueltas.

**El bloque que va pegado a una rejilla de imágenes es el que falla.** Un párrafo con una cuadrícula de imágenes justo debajo se come la escritura y la parte en letras sueltas, una por línea. Pasa de forma repetible. Déjalos para el final, y si fallan dos veces, no insistas: deshaz y dilo.

Dos cosas más que conviene saber antes de prometer un documento acabado:

- **El triple clic no siempre coge un solo párrafo.** En un grupo de líneas cortas coge el grupo entero. Mira la captura antes de escribir y, si cogió de más, escribe el contenido de todas esas líneas de una vez.
- **La plantilla trae muestras de color de ejemplo** (turquesa, azul) que contradicen la paleta de la marca. Son bloques gráficos, no texto, así que no se arreglan escribiendo. Avisa de que hay que recolorearlos o borrarlos a mano.

Si algo se rompe, deshacer repetidamente devuelve la plantilla a su estado original sin dañar el documento. Ojo: deshacer de más también borra bloques que sí habías escrito bien, así que cuenta los pasos.
