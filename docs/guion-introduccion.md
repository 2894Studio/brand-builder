# Guion de introducción: de la marca al contenido

Para el profesor. Dura 20 minutos y abre la sesión de contenido. Lo que va entre comillas está pensado para decirse casi literal; el resto son indicaciones. Antes de empezar, ten abierto el manual de PULSO (`kit/index.html`) y la página `tokens/ejemplo.html`.

## 1. Gancho (3 min)

**Enseña** dos posts de Instagram de la misma marca ficticia: uno hecho con un prompt suelto («haz un post para una panadería») y otro hecho con la marca ya definida.

> «Los dos los ha hecho una IA. En el primero, cada pieza sale con otros colores, otra letra y otra personalidad. En el segundo parece que los ha hecho la misma persona. La diferencia no es la herramienta: es que la marca estaba decidida antes de pedir nada.»

**Pregunta a la clase:** «¿Cuál de los dos publicaríais?» Deja que lo discutan un minuto.

## 2. Qué construimos en la clase anterior (5 min)

**Muestra** la carpeta de una marca terminada y señala solo tres archivos.

> «Os llevasteis tres cosas. Primera: `marca.json`, la marca en un archivo. Segunda: los tokens, que son esa marca convertida en colores y fuentes que entiende el código. Tercera: el manual. Hoy usamos la primera y la segunda para producir contenido sin volver a explicar quiénes somos.»

**Comprobación rápida:** «Levantad la mano los que tengáis `marca.json` válido.» Los que no, se sientan con alguien que sí y siguen en pareja. No pares la clase.

## 3. El mapa de herramientas (6 min)

**Dibuja en la pizarra** tres columnas: *imagen fija*, *movimiento sin cámara*, *video con tu metraje*.

> «Hay tres herramientas y cada una hace una cosa distinta. No son tres formas de hacer lo mismo.»

| Herramienta | Qué hace | La usamos hoy |
|---|---|---|
| **creative-architect** | Imágenes y video con IA; escribe buenos prompts | Sí, para el post estático |
| **motion-architect** | Animaciones y reels en código, sin cámara, en tu ordenador y sin créditos | Sí, para el video |
| **video-editor-architect** | Edita un video que tú has grabado | No hoy: instalación pesada |

> «Para imagen usaremos Canva como herramienta de generación. Os aviso de algo: creative-architect no trae Canva entre sus proveedores. Así que haremos lo siguiente: creative-architect escribe el prompt, y Canva lo ejecuta. Es un buen ejercicio porque veis dónde acaba una herramienta y empieza la otra.»

## 4. Tres reglas antes de tocar nada (4 min)

Escríbelas en la pizarra y déjalas visibles toda la sesión.

> «**Regla uno: lo barato primero.** Si algo se puede hacer sin generar una imagen, no se genera. **Regla dos: la marca se pide por su nombre.** Cuando le pidáis algo a Claude, escribid "usa mi `marca.json`". Lo he medido y, si no lo decís, a veces no lo lee. **Regla tres: un intento razonado, no tres a ciegas.** Cada reintento de imagen vuelve a gastar créditos.»

**Detalle para la regla dos (verificado en las pruebas):** sin la frase, el modelo entregó un prompt genérico; con «usa mi `marca.json`», leyó el archivo y usó los colores y el estilo de la marca. Cuéntalo así, sin exagerar: fue una prueba, no una estadística.

## 5. Transición a la práctica (2 min)

> «Vamos a hacer tres cosas. Un post fijo para Instagram, una pieza animada con la misma marca, y por último os enseño yo cuánto cuesta animar con IA, para que lo veáis antes de gastarlo. En cada paso, antes de pedir, os pregunto: ¿ya está la marca dicha? ¿Se puede hacer sin gastar? Empezamos.»

Pasa a `guion-sesion-contenido.md`, bloque «Post estático».

## Si algo falla en directo

| Pasa | Haz |
|---|---|
| Un alumno no tiene `marca.json` | Dale `evals/fixtures/pulso/marca.json` y que practique con PULSO |
| No funciona la instalación de creative-architect | Que trabaje en modo prompt: la skill entrega el texto igualmente |
| El conector de Canva no responde | Pega el prompt a mano en Canva (`Crear diseño → Generar imagen`); el resultado es el mismo |
| La clase va más lenta de lo previsto | Salta la demo de video con IA (bloque 3 de la sesión); es la que menos falta hace |
