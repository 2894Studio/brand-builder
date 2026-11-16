# Fotos para el bento y los posts

Los posts llevan imágenes cuando hay fotos. Esta guía dice **cómo dárselas a la skill**, de dónde sacarlas y qué cuidar. Canva **no** es una fuente de fotos reales: genera imágenes con IA (sintéticas). Es la única vía que se ha probado aquí, y es opcional.

## Generarlas con Gemini o Google Flow

```
python3 skills/lanzamiento/tools/prompts_fotos.py marca.json --salida lanzamiento/prompts-fotos.md [--equipo "…"] [--retrato "…"] [--producto "…"] [--escena "…"]
```

Escribe 4 prompts (equipo 4:3, retrato 3:4, producto 1:1, lugar 4:3) con el estilo fotográfico y la paleta de `marca.json`, sin texto ni logos. Se pegan en Gemini o en Flow, se guarda la mejor variante en `fotos/` y se anota con origen `ia` en `creditos.md`. Son personas sintéticas: no se presentan como tu equipo ni tus clientes reales.

## Pexels con clave gratuita (opcional)

Con una cuenta gratuita en pexels.com/api se obtiene una clave al momento. Cada persona usa la suya (compartirla agota el límite por hora):

```
export PEXELS_API_KEY=tu_clave
python3 skills/lanzamiento/tools/buscar_fotos.py buscar "equipo trabajando en una oficina" --orientacion landscape
python3 skills/lanzamiento/tools/buscar_fotos.py elegir <id> --como equipo-1
```

`buscar` deja miniaturas en `fotos/_candidatas/` para mirarlas; `elegir` descarga la foto y añade su fila a `creditos.md` (banco, autor con enlace, «Pexels License»). Sin clave, descarga a mano de pexels.com y rellena la fila como arriba. **Una persona de banco no es tu equipo ni tus clientes**: no se presenta con nombre ni cargo reales.

## 1. Cómo se las das a la skill (igual con cualquier origen)

1. Guarda las fotos en una carpeta `fotos/` de tu proyecto, con estos nombres para que las encuentre solas:
   `equipo-1.jpg` (varias personas) · `retrato-1.jpg` (una persona) · `producto-1.jpg` · `local-1.jpg`
2. Crea la tabla de créditos y rellénala, una fila por foto:
   ```
   python3 skills/lanzamiento/tools/preparar_fotos.py fotos --crear-creditos
   ```
   | archivo | origen | autor o fuente | licencia | permiso de las personas |
   |---|---|---|---|---|
   | equipo-1.jpg | propia | Estudio X | propia | sí |
   | retrato-1.jpg | banco | Nombre del autor, unsplash.com/... | Unsplash License | n/a |
   | equipo-2.png | ia | Canva (generada) | n/a | n/a |

   `origen` es **propia**, **banco** o **ia**. `banco` exige autor y licencia. `propia` con personas exige un «sí» en el permiso.
3. Prepárelas:
   ```
   python3 skills/lanzamiento/tools/preparar_fotos.py fotos --salida lanzamiento/fotos
   ```
   Revisa la resolución (lado corto ≥ 1080 px), recorta a 3:4, 4:3 y 1:1 y escribe `manifiesto.json`. Las de origen `ia` quedan marcadas en el manifiesto. **No se escribe nada sobre las piezas** salvo que lo pidas (`--declarar-ia` en el bento y en `post_base.py`). Si falta una fila o falta una licencia, **da error y no sigue**.
4. El bento y el andamio de los posts las cogen con `--fotos lanzamiento/fotos`.

## 2. De dónde sacarlas (orden de preferencia)

| # | Fuente | Cuándo | Qué cuidar |
|---|---|---|---|
| 1 | **Fotos propias** (equipo, local, producto) | Siempre que se pueda: es lo que da confianza | Permiso por escrito de las personas que salen |
| 2 | **Bancos con licencia**: **Pexels** con `tools/buscar_fotos.py` (clave gratuita), o Unsplash, Pixabay y los de pago a mano | No hay fotos propias y se necesita una imagen real | Leer la licencia de **cada** foto: uso comercial, personas reconocibles y marcas visibles. Anotar autor y licencia en `creditos.md` |
| 3 | **Imágenes generadas con IA** (Canva u otro generador) | Sin fotos propias ni de banco que encajen | Anotarlas en `creditos.md`. Declararlas en la pieza es decisión tuya (conviene si se publican). **No se presentan como el equipo real de una empresa** |
| 4 | **Sin fotos** | Todavía no hay nada | Recursos que se sostienen solos (mapa, interfaz, cifra) o marcador visible |

Una marca que vende **confianza entre personas** (reclutamiento, salud, consultoría) no debe mostrar personas sintéticas como su equipo: úsalas solo como ejemplo, o no las uses.

## 3. Generarlas con Canva (receta verificada)

Úsala si no tienes fotos propias ni clave de banco. Con el conector de Canva y la persona de acuerdo:

0. **Prompts a medida:** `python3 skills/lanzamiento/tools/prompts_fotos.py marca.json --proveedor canva` escribe 4 prompts con la marca y la proporción de Canva de cada uno (`LANDSCAPE_4_3`, `PORTRAIT_3_4`, `SQUARE_1_1`). Úsalos en vez de las plantillas del paso 1.
1. **Generar:** `generate-image` con proporción `LANDSCAPE_4_3` (equipo) o `PORTRAIT_3_4` (retrato). Prompt-plantilla, si no usas el paso 0, adaptando perfiles y colores de ropa a la marca:
   - Equipo: «Fotografía realista y natural de un equipo de cuatro profesionales [perfil] reunidos alrededor de un portátil en una oficina luminosa y moderna, sonriendo con naturalidad, ropa casual elegante en tonos [colores de la marca], luz natural suave, estilo de fotografía corporativa editorial. Sin texto, sin logotipos, sin marcas visibles.»
   - Retrato: «Retrato fotográfico realista de [persona], [rol], mirando a cámara con expresión tranquila, fondo desenfocado de oficina moderna, plano medio, luz natural. Sin texto, sin logotipos.»
2. **Traerlas a disco:** el conector solo deja una miniatura y el enlace de la imagen da 403 con `curl`. Crea un diseño con `create-design` (formato `Instagram Post (Portrait)`, las imágenes en `references`, «una página por imagen a página completa, sin texto ni gráficos») y expórtalo con `export-design` en PNG. Descarga con `curl` las URL firmadas a `fotos/`. Salen **1080×1440**.
3. **Encuadre:** al ser la página 3:4, una foto de equipo 4:3 pierde los laterales. Pide el equipo ya **centrado en el encuadre** o genéralo en 3:4.
4. **Cuenta y créditos:** cada generación gasta créditos (tope de la skill `canva`: 8 por kit), y el diseño de exportación queda en la cuenta. Dilo antes.
5. Anota cada foto: `python3 skills/lanzamiento/tools/registrar_foto.py fotos/equipo-1.png --origen ia --fuente "Canva (generada)"`, y después `preparar_fotos.py`.

## 4. Sin Canva

El flujo es el mismo desde el paso 1. La foto llega de tus archivos, de un banco con licencia (descargas y rellenas la fila) o de otro generador de imágenes (creative-architect documenta algunos proveedores). Los bancos y otros generadores **no se han ejecutado desde este plugin**: antes de depender de uno, comprueba su licencia y sus condiciones actuales.

## Reglas

- Una persona generada o de banco **nunca** se presenta como un empleado o cliente con nombre y cargo reales.
- Lo que se escribe sobre la pieza (por ejemplo «Imagen generada con IA») lo decide la persona. Lo que no es opcional es dejarlo anotado en `creditos.md` y en el `LEEME.md`.
- Si más de un tercio de un post son marcadores, cambia de recurso: no está terminado.
- Referencias de otras marcas: se toma el atributo, no la imagen.
