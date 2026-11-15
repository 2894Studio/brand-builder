# Guion de la sesión de contenido (2 horas)

Para el profesor. Empieza con `guion-introduccion.md` (20 min, ya cuenta dentro de la primera franja). Los prompts van en citas para copiar tal cual.

**Lo que verás en esta sesión:** que una marca bien definida se aplica sola a un post fijo y a una pieza animada, sin gastar créditos hasta el último bloque, y que el criterio de ahorro es enseñable.

## Requisitos (comprueba 48 horas antes)

| Qué | Para qué | Si falta |
|---|---|---|
| `marca.json` válido en la carpeta del alumno | Todo | Usa `evals/fixtures/pulso/marca.json` |
| creative-architect instalado | Escribir el prompt del post | Modo prompt sin instalar: pide el prompt a Claude con la marca en la conversación |
| Conector de Canva activo | Generar la imagen | Pegar el prompt a mano en Canva |
| Node 18+, ffmpeg, yt-dlp, Python 3 | motion-architect | Haz el bloque 3 como demo tuya |

Instalar motion-architect es la parte pesada: hazlo tú antes de la clase y pide a los alumnos que lo intenten en casa. Su instalador es un script de bash; en Windows hace falta WSL o Git Bash (no verificado).

## Mapa

| Min | Bloque | Gasto |
|---|---|---|
| 0–20 | Introducción (`guion-introduccion.md`) | 0 |
| 20–55 | 1. Post estático: prompt → Canva | Imágenes de Canva |
| 55–95 | 2. Pieza animada con motion-architect | 0 |
| 95–110 | 3. Demo del profesor: animar con IA | Créditos del proveedor |
| 110–120 | 4. Revisión y calendario | 0 |

## 1. Post estático (35 min)

**Objetivo:** un post de Instagram 4:5 con la marca aplicada, escrito como prompt y ejecutado en Canva.

**Paso 1, el prompt (10 min).** Cada alumno escribe, cambiando lo que anuncia:

> `Usa mi marca.json (está en esta carpeta). Necesito un post estático de Instagram (4:5) para anunciar [lo que sea]. No tengo proveedor de imagen conectado: entrégame el prompt listo para pegar, no generes nada.`

**Qué debe pasar** (verificado en la prueba con PULSO):
- Lee `marca.json` y usa sus colores y su estilo.
- Entrega la imagen **sin texto** y con una zona libre para ponerlo después. Es intencionado: la tipografía que dibuja un modelo no es fiable.
- No genera nada.

**Qué enseñas aquí:** el texto del post NO va en la imagen; va encima, con la fuente de la marca. Muestra cómo el prompt reserva el tercio superior.

**Paso 2, la imagen en Canva (15 min).** Con el conector activo, pide:

> `Genera esta imagen en Canva en formato 4:5 con el prompt anterior.`

Lo que hace el conector (por su descripción, verificada): `generate-image` acepta la proporción vertical 4:5 y devuelve un trabajo que hay que esperar; la imagen queda en Canva con un enlace. Dos advertencias para la clase:
- **Un intento razonado.** Si el resultado no convence, cambia el prompt y di qué cambiaste. No regeneres a ciegas.
- **Para un diseño completo con la marca de Canva** (no solo una imagen), `create-design` no puede aplicar un Brand Kit; hay que usar `generate-design` con el `brand_kit_id` del alumno, y el Brand Kit hay que haberlo subido a mano a Canva (el conector no los crea). Con el manual de la clase anterior, ya tienen el paquete.

**Paso 3, el texto encima (10 min).** En Canva, añade el titular con la fuente de la marca y el color de texto del manual. Revisa el contraste con `tokens/contraste.md`.

**Errores típicos:** «Me sale con letras raras» → el prompt pedía texto en la imagen; que lo quiten. «Los colores no son los míos» → no dijeron «usa mi marca.json». «Sale genérico» → revisa el `visual.estilo` de `marca.json`: si es una lista de adjetivos, hay que reescribirlo como técnica (luz, grano, encuadre).

## 2. Pieza animada con motion-architect (40 min)

**Objetivo:** un video corto de 9:16 con la marca, hecho en local, sin créditos.

**Paso 1, importar la marca (5 min).** Con motion-architect ya instalado:

```bash
python3 brand-kit-builder/skills/tokens/tools/exportar_motion.py marca.json \
  --salida motion-architect/studio/brand.json --forzar \
  --tagline "El claim corto de tu marca" --studio motion-architect/studio
```

(En Windows, `python` en lugar de `python3`.) El script guarda una copia `brand.json.bak` y **imprime dos líneas que hay que pegar a mano** en `motion-architect/studio/src/brand/brand.ts`: las fuentes reales salen de esos imports, no del JSON. Pídele a Claude que las aplique.

**Qué enseñas aquí:** una sola fuente de verdad. Cambia un color en `marca.json`, vuelve a ejecutar el comando y la animación cambia.

**Paso 2, pedir el video (25 min).**

> `/motion Una pieza de 9:16 y 8 segundos que anuncie [lo que sea] con el titular "[frase corta]" y el logo al final.`

Motion-architect propone un guion visual, **espera tu aprobación**, construye la pieza y renderiza. Ten paciencia: la primera vez descarga dependencias.

**Paso 3, ver el resultado (10 min).** Comparan la pieza con el manual: ¿se ve la misma marca? ¿Se lee el texto? La zona segura de 9:16 evita que la interfaz de Instagram tape el titular.

**Honestidad con la clase:** la verificación que se hizo con PULSO fue renderizar un fotograma de la pieza de demostración con la marca importada (colores, fuentes y esquinas correctas). No se ejecutó un `/motion` completo con el modelo; la primera vez que lo hagas en clase, es la prueba.

**Licencia.** Remotion es gratis para personas, organizaciones sin ánimo de lucro y empresas de hasta 3 personas; las de 4 o más necesitan licencia. Pregunta a tus alumnos si trabajan para una empresa grande.

## 3. Demo del profesor: animar con IA (15 min)

**Objetivo:** que vean el coste real antes de gastar. La haces tú, ellos miran.

1. Elige la imagen del bloque 1.
2. Pide con creative-architect: `Anima esta imagen: que la cámara se acerque despacio.` (`animar`).
3. **Antes de generar**, di en voz alta la duración y la proporción: son lo que más mueve el precio.
4. Enseña el prompt: describe **solo el movimiento**, no la escena, porque la escena ya está en la imagen.

Necesita un proveedor de video conectado (creative-architect documenta Higgsfield y Magnific). **Canva no se usa aquí:** creative-architect no lo conoce como proveedor y su herramienta de video no se ha verificado en este plugin. Si no tienes proveedor, haz la demo solo con el prompt de movimiento y explica qué se enviaría.

## 4. Revisión y calendario (10 min)

Cada alumno escribe, en `trabajo/…/calendario.md`, **una semana de contenido** con tres piezas: una fija, una animada y una que reutilice la imagen del lunes. Revisión por parejas con esta lista:

- [ ] ¿Usa colores y fuentes de `marca.json`?
- [ ] ¿La imagen va sin texto y el texto se añadió encima?
- [ ] ¿El contraste del texto está comprobado?
- [ ] ¿Hay un solo intento razonado por pieza?
- [ ] ¿La lista de lo que queda a mano está al final?

## Rúbrica

| Criterio | 0 | 1 | 2 |
|---|---|---|---|
| Marca aplicada | Colores inventados | Parcial | Salen de `marca.json` |
| Texto | Dentro de la imagen | Encima, sin comprobar | Encima, contraste comprobado |
| Ahorro | Repitió a ciegas | Un reintento sin cambiar nada | Cambió el prompt y dijo qué |
| Movimiento | Sin guion | Con guion | Con guion y zona segura |
| Calendario | Ninguno | Tres piezas | Tres piezas con reutilización |

## Después

Si quieres seguir, la herramienta que falta es una skill de posts tipográficos (plantillas con los tokens que se renderizan a PNG): sin generar ni una imagen y con la letra exacta de la marca. Es el siguiente paso recomendado.
