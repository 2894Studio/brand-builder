# Entrenar el gusto visual: de «me gusta» a reglas que se comprueban

Las referencias **no entrenan un modelo**. Funcionan si se convierten en **decisiones concretas** que después se **comprueban** en cada pieza. Una referencia sin decisiones solo elige un tono y las piezas salen genéricas (pasó en la prueba de la escuela de código: las reglas eran «bento con esquinas de 16–20 px» y «fondo claro con bloque oscuro», que valen para cualquier marca tech).

## 1. Qué referencias traer
- **6 a 8, de piezas y no solo de webs**: posts, logos, packaging, carteles, tableros de marca. Un logo o un post enseña más que una landing.
- **3 de la categoría** (para saber qué se espera), **2 de fuera de la categoría** (para no parecer la media) y **2 que NO quieres parecer**.
- Con un MCP (Mobbin, Refero, Taste) o buscando a mano en Pinterest, Behance, Savee o Dribbble: la búsqueda importa menos que lo que haces después.

## 2. Qué escribir por cada una (lo que el plugin necesita)
Una frase por dimensión que de verdad destaque en esa referencia, con **qué copio (la técnica)** y **qué no copio (la marca)**:

| Dimensión | Pregunta | Ejemplo (Maze) |
|---|---|---|
| nombre | ¿Cómo se trata el nombre? | minúsculas, peso alto, sin símbolo si no hace falta |
| simbolo | ¿Qué forma tiene el símbolo? | geometría 2D plana, trazo grueso redondeado, sin 3D ni degradados |
| tipografia | ¿Peso, tamaño, tracking de titulares? | titulares muy grandes, negrita, tracking cerrado |
| imagen | ¿Qué tipo de imagen y cómo se encuadra? | capturas de producto con una persona real con su rol |
| composicion | ¿Cómo se organiza la pieza? | asimétrica, un elemento recortado por el borde, mucho aire |
| firma | ¿Qué gráfico se repite? | un trazo o forma propia en todas las piezas |
| forma / color / voz | radios y bloques; reparto y papel del color; cómo habla el texto | un solo bloque de color por pieza; frases cortas en imperativo |

**Mínimo:** al menos **2 dimensiones de las distintivas** (nombre, símbolo, tipografía, imagen, composición, firma). Forma y color solas son lo genérico.

## 2b. La forma fácil: el etiquetador (interfaz)
```
python3 skills/gusto/tools/etiquetador.py          # abre el navegador y guarda directo en el proyecto
```
Arrastras las imágenes (o las pegas), eliges «Me gusta / No quiero parecerme / De otra categoría», escribes tu nota y las decisiones por dimensión (con ejemplos), y una lista de comprobación te dice qué falta. «Guardar en el proyecto» crea `referencias/` y `gusto.json` (mide las imágenes y guarda tus notas y decisiones). Sin servidor, abre `skills/gusto/tools/etiquetador.html` a mano, usa **Descargar ZIP** y ejecuta `python3 skills/gusto/tools/importar_etiquetado.py referencias-etiquetadas.zip`.

## 3. Cómo se registran (a mano, si no usas el etiquetador)
```
python3 skills/gusto/tools/gusto.py decision --ref maze_landing --dimension simbolo --regla "geometría 2D plana, trazo grueso redondeado, sin 3D" --aplica logo
python3 skills/gusto/tools/gusto.py decision --ref maze_landing --dimension composicion --regla "un elemento recortado por el borde y mucho aire" --aplica post,bento
python3 skills/gusto/tools/gusto.py reglas        # lista R1…Rn
python3 skills/gusto/tools/gusto.py validar --gusto gusto.json
```
Las decisiones de las referencias «no» se leen como **EVITAR**. Lo que dice la persona de cada imagen (`nota_usuario`) manda sobre lo que el modelo crea ver.

## 4. Cómo se comprueban (cada vez)
`kit_lanzamiento.py` genera `contacto-gusto.png` (referencias | piezas | reglas) y `revision-gusto.md`. Se mira la hoja de verdad y, por cada regla, se escribe `cumple`, `parcial`, `no cumple` o `no aplica` y **dónde se ve**. Lo que no cumple se corrige y se marca `corregido`. La puerta de entrega no se abre con reglas sin revisar.

## 5. Entrenar con el uso
Tras cada entrega, tres preguntas a la persona: ¿qué pieza te gusta más y por qué?, ¿cuál no?, ¿qué cambiarías? Lo que contesta se guarda como **referencia nueva** (la pieza propia con nota) y como decisiones. Así el gusto se afina con ejemplos propios, no con más capturas ajenas.

## Límites
- La comprobación la hace el propio modelo mirando la hoja: es autoevaluación, mejor que nada pero no infalible. La persona decide.
- Con pocas referencias (menos de 5) las reglas son hipótesis.
