# Cómo gastar menos (tokens y créditos)

Hay dos gastos distintos y se ahorran de formas distintas.

- **Tokens:** lo que consume Claude al leer y escribir. Se paga con tu plan de Claude.
- **Créditos:** lo que cobra el proveedor de imagen o video cada vez que genera. Se paga en el proveedor.

Lo que más cuesta es casi siempre lo segundo, y se ahorra sobre todo **no repitiendo**.

## Lo que se midió

Una prueba con la misma petición (un post estático de Instagram 4:5 para PULSO, sin proveedor, entregando solo el prompt), ejecutada con creative-architect y Brand Kit Builder instalados:

| Caso | Turnos | Coste aproximado | Resultado |
|---|---|---|---|
| Sin decir nada de la marca | 3 | ~$0,10 | Prompt genérico; **no leyó `marca.json`** |
| Diciendo «usa mi `marca.json`» | 9 | ~$0,16 | Leyó el archivo y usó sus colores y su estilo |

**Cómo leerlo, sin inflarlo:**
- Es **una ejecución por caso**, con el modelo por defecto de esa sesión. Los importes cambian con el modelo y con tu plan, y son orientativos.
- La marca **no** abarata la llamada: cuesta más porque Claude lee más archivos. Lo que ahorra es el trabajo posterior: sin ella, el prompt sale con colores inventados y hay que rehacerlo, y si ya has generado la imagen, rehacer es pagar otra vez.
- El consumo total de una sesión depende sobre todo de cuántos archivos se leen y de cuánto dura la conversación, no del tamaño de la respuesta.

## Peso de lo que se carga (medido)

El plugin creative-architect pesa unos 200 KB si se leyera entero, pero **no se carga entero**: su skill de entrada pesa 2,7 KB y cada oficio se carga solo cuando hace falta. El archivo más grande, el de un proveedor concreto (Higgsfield, 24 KB), solo se abre si ese proveedor está conectado. Un encargo típico carga la entrada, `proveedores`, `direccion-de-arte` y un oficio. Orden de magnitud: unas decenas de KB, no los 200.

## Las ocho reglas

1. **Lo barato primero.** Todo lo que se pueda hacer sin generar una imagen, no se genera. Un post de solo texto, un dato o una cita se hacen en Canva con la fuente de la marca; no necesitan un modelo de imagen.
2. **Pide la marca por su nombre.** Escribe «usa mi `marca.json`» al empezar. Sin eso, a veces no la lee.
3. **El texto va encima, no dentro de la imagen.** Los modelos escriben mal las letras, y una imagen con letras rotas se tira entera. El prompt debe pedir la imagen sin texto y con una zona libre.
4. **Un intento razonado.** Si no convence, cambia el prompt, di qué cambiaste y genera una vez más. Tras dos fallos de la misma pieza, para y cambia de enfoque. Cada reintento vuelve a cobrar.
5. **Una pieza, una conversación.** Cuando termines una pieza, `/clear` antes de empezar la siguiente. Una conversación larga arrastra todo lo anterior en cada mensaje. Si no puedes cortarla, `/compact`.
6. **Guarda el prompt en un archivo.** `trabajo/…/prompts.md`. Para la variante del martes, reutilízalo y cambia una línea, en vez de volver a pedirlo.
7. **Elige el modelo según la tarea.** Estrategia y criterio piden el modelo más potente; ejecutar un brief ya definido puede hacerse con uno más ligero. Se cambia con `/model`.
8. **Una sola fuente de verdad.** Si cambias un color, cámbialo en `marca.json` y regenera tokens y `brand.json`. Corregir cada pieza a mano cuesta más que regenerarlas.

## Antes de generar, cuenta

| Pregunta | Por qué importa |
|---|---|
| ¿Es para imagen o para video? | Se cobran de forma distinta; consulta el precio del proveedor antes de generar, si lo permite |
| ¿Cuántos segundos y en qué proporción? | En video, la duración y la resolución son lo que más mueve el precio |
| ¿Cuántas variantes? | Cada variante se cobra |
| ¿Puedo hacerlo en local? | motion-architect renderiza en tu ordenador y no gasta créditos |

Con Canva, pon un tope por kit (la regla del plugin es **8 generaciones o menos**) y cuéntalas.

## Lo que NO ahorra (y conviene no creer)

- **Escribir prompts muy cortos.** Un prompt pobre produce una imagen pobre y otro intento.
- **Saltarse la entrevista de marca.** Ahorra tokens hoy y cuesta repeticiones mañana.
- **Pedir tres versiones «por si acaso».** Son tres cobros.
