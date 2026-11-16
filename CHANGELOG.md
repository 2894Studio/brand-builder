# Changelog

## 2.1.1

Cambios a partir de la prueba real de punta a punta (ver `docs/informe-prueba-real.md`).

- **Nuevo:** `incrustar_fuente.py`. Incrusta la fuente en los logos SVG y quita las clases CSS compartidas, para que el logo se vea igual dentro de `<img>`, sin conexión y junto a otros logos. Verificado con la red bloqueada.
- **Nuevo:** paso de **referencias** en `estrategia` y campo `referencias` en `marca.json` (esquema, validador y plantilla), para entrenar el gusto visual con el atributo concreto de cada referencia.
- **Nuevo:** láminas más expresivas: portada con inicial gigante a sangre, divisores con número recortado, lámina de principio a página completa y lámina de referencias. `kit.json` admite `"expresivo": false`.
- **Nuevo:** `criterio-visual.md`, las cinco preguntas para juzgar un manual, y comprobaciones en la skill de entrega.
- **Arreglo:** las tarjetas de valores se salían de la lámina con 4 valores; ahora pasan a rejilla 2×2.
- **Arreglo:** doble punto en el tono, palabras prohibidas genéricas en lugar de las del sector, licencia de fuentes cortada, y `;` final en el `style` del puente a motion-architect.
- **Arreglo:** el autotest comprueba que el texto a sangre asoma en el lienzo (un error propio lo dejó fuera de la lámina) y cubre las variantes con 4 valores, sobrio y con referencias.
- **Cambio:** `estrategia` busca el nombre en la web antes de dibujar el logo, e `identidad` exige ver el logo renderizado antes de presentarlo.
- **Documentación:** informe de la prueba real; la guía recoge que la imagen de Canva solo llega como miniatura y hay que descargarla.

## 2.1.0

- **Nuevo:** `exportar_motion.py`, puente de `marca.json` a `brand.json` de motion-architect (esquema verificado contra su repositorio; renderizado de un fotograma comprobado con PULSO).
- **Nuevo:** `verificar_tokens.py`, autotest de tokens y del puente.
- **Nuevo:** guion de introducción, guion de la sesión de contenido, guía de ahorro de tokens y tabla para elegir herramienta.
- **Nuevo:** la skill `canva` recoge los hechos verificados del conector (4:5 y 9:16, `generate-design` con `brand_kit_id`, `create-design` sin Brand Kit).
- **Cambio:** la skill de entrada indica pedir «usa mi `marca.json`» al crear contenido, tras comprobar que sin ella el modelo no siempre lo lee.

## 2.0.0

- **Documentación:** guía del alumno, guion de clase y prueba guiada.
- **Arreglo tras la primera prueba con el modelo:** trata siempre de tú y no adelanta soluciones antes de cerrar la entrevista.
- **Nuevo:** aviso de Python 3.11+ y del nombre del comando en Windows.

Reestructurado como plugin de Claude Code con varias skills.

- **Nuevo:** skill de entrada que enruta a `estrategia`, `identidad`, `voz`, `tokens`, `laminas`, `entrega` y `canva`.
- **Nuevo:** `marca.json` como salida, compatible con creative-architect, con esquema y validador (contraste y léxico prohibido incluidos).
- **Nuevo:** `tokens`: `tokens.json` (W3C), variables CSS, Tailwind v3 y v4, tabla de contraste y página de ejemplo.
- **Nuevo:** `laminas` sin Canva: manual en SVG, `index.html` y PDF opcional, en cinco territorios, con autotest.
- **Cambio:** Canva pasa de núcleo a módulo opcional; el resto del plugin no depende de él.
- **Cambio:** la producción de imagen se pide por intención (`imagen.generar`); sin proveedor, se entregan prompts.
- **Cambio:** el SKILL.md de 14 KB se divide por oficio; el contenido de las referencias se conserva y se reparte.
- **Arreglo:** el script de pruebas original usaba una fuente fija y `rsvg-convert` sin comprobar; la librería nueva avisa con un mensaje claro.
- **Arreglo:** los divisores y la portada no se numeran; la numeración del arquetipo D queda dentro del panel.

## 1.x

Una sola skill, `brand-kit-builder`, acoplada a Canva: entrevista, territorios, dos logos, láminas y control de créditos.
