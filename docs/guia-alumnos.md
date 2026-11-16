# Guía del alumno: crea tu marca con Brand Kit Builder

Esta guía te lleva de cero a una marca completa: estrategia, logo, paleta, tipografía, voz, tokens para tu web o app y un manual. Tardas entre 60 y 90 minutos la primera vez.

## 1. Qué es y qué te llevas

Brand Kit Builder es un plugin de Claude Code. Le hablas normal y te guía por seis pasos, pidiéndote aprobación en cada uno.

Al terminar tienes:

- `marca.json`: los datos de tu marca en un solo archivo. Otras herramientas (como creative-architect) lo leen y no tienes que explicar tu marca otra vez.
- Un manual de marca que se abre en el navegador.
- Tokens de diseño: colores, fuentes y tamaños listos para pegar en tu web (CSS o Tailwind).
- Una lista honesta de lo que todavía tienes que hacer a mano.

**Lo que NO hace:** no sustituye a un abogado (no comprueba si tu nombre está registrado) ni a un diseñador que dibuje tu logotipo final. Las imágenes que genera la IA son una referencia, no el archivo definitivo.

## 2. Antes de empezar

Necesitas tres cosas:

1. **Claude Code**, en la terminal o en la app de escritorio, con tu sesión iniciada.
2. **Python 3.11 o superior.** Compruébalo en la terminal:

   ```bash
   python3 --version
   ```

   En Windows prueba `python --version` o `py --version`. Si no tienes Python, instálalo desde python.org. Sin Python puedes hacer la entrevista, el logo, la paleta y la voz, pero no se generan los tokens, el manual ni la validación.
3. **Una carpeta vacía por cada marca.** Abre Claude Code dentro de ella. Todo lo que se cree quedará ahí.

> Se ha probado en Linux. Si algo falla en Windows o macOS, apunta tu sistema operativo y cuéntaselo a tu profesor.

## 3. Instalación

### Opción A: desde la carpeta que te ha pasado tu profesor (disponible ya)

1. Descomprime `brand-kit-builder.zip`. Te queda una carpeta `brand-kit-builder`.
2. En la terminal, ejecuta estos dos comandos, uno detrás de otro. Sustituye la ruta por la de tu carpeta:

   ```bash
   claude plugin marketplace add ./brand-kit-builder
   ```

   ```bash
   claude plugin install brand-kit-builder@brand-kit-builder
   ```

3. Abre una sesión nueva de Claude Code en tu carpeta de marca (o escribe `/reload-plugins` en la que ya tienes abierta).
4. Comprueba que está instalado:

   ```bash
   claude plugin list
   ```

   Debes ver `brand-kit-builder` con versión 2.0.0 y estado enabled.

### Opción B: desde GitHub (cuando tu profesor lo publique)

```bash
claude plugin marketplace add 2894Studio/brand-kit-builder
```

```bash
claude plugin install brand-kit-builder@brand-kit-builder
```

Todavía no está publicado. Usa la opción A hasta que te avisen.

### Opcional: creative-architect, para generar imágenes y contenido

Es otro plugin, de otro autor, que se conecta con esta skill a través de `marca.json`. No lo necesitas para crear la marca: sin él, la skill te da los prompts para pegar en la herramienta de imagen que prefieras.

```bash
claude plugin marketplace add Hainrixz/creative-architect
```

```bash
claude plugin install creative-architect@creative-architect
```

Si te pide credenciales, el repositorio no está accesible para ti en ese momento: consúltalo con tu profesor.

## 4. Tu primera marca en seis pasos

Escribe en Claude Code. Las frases de ejemplo sirven tal cual, pero habla con tus palabras.

### Paso 1. Estrategia

> `/brand-kit-builder Quiero crear la marca de [lo que haces, en una frase].`

Te hace **tres rondas de preguntas**, una por mensaje. La más importante es la segunda: **qué nunca debe parecer tu marca**. Responde con ejemplos concretos, no con «moderna y profesional».

Después te pide **ocho referencias visuales**: 4 que te encantan, 2 que no quieres parecer y 2 de otra categoría (una revista, un cartel, un edificio). De cada una te pregunta **qué te gusta**: «la escala enorme del titular», no «me gusta Deloitte». Es el paso que más educa tu gusto y evita que la marca salga como la media.

Cuando termina, te resume lo entendido. Si es correcto, di «confirmado». Hasta entonces no se genera nada.

Después recibes **tres territorios** (tres direcciones para tu marca). Elige uno o mezcla dos, y te escribe el manifiesto de la marca en primera persona.

### Paso 2. Logo, paleta y tipografía

> `Pasemos al logo.`

Recibes **dos propuestas de logo**, siempre dos, y la recomendada. También una paleta de cinco colores con su contraste calculado.

- Si tienes un generador de imagen conectado, crea las imágenes. Si no, te da **un prompt por propuesta**: pégalo en la herramienta que uses.
- Guarda el logo elegido en `trabajo/…/logo/` y dile: «Este es el logo elegido».
- Cuando apruebas logo y paleta, la skill escribe `marca.json` y lo valida.
- Los logos son archivos SVG con tu nombre en texto. La skill incrusta la fuente dentro del archivo para que se vea igual en cualquier sitio; mira el resultado en el navegador antes de aprobar.

### Paso 3. Voz

> `Ahora la voz de la marca.`

Define cómo habla tu marca con ejemplos de «así sí» y «así no», y lo que haría en seis situaciones difíciles (una queja, un error propio, el precio…). Acaba con una lista de palabras que tu marca no usa.

### Paso 4. Tokens (si tu marca va a una web o app)

> `Genera los tokens para mi web con Tailwind.`

Se crean los archivos de colores, fuentes y tamaños. Abre `ejemplo.html` en el navegador: es tu marca funcionando en una página real. Si un color de texto no se lee bien, la skill lo dice y te manda de vuelta a revisar la paleta.

### Paso 5. Manual de marca

> `Monta el manual de marca.`

Te pide el contenido (promesa, valores, ejemplos) y genera el manual. Ábrelo desde `kit/index.html`.

### Paso 6. Entrega

> `Revisa la marca y dime qué me falta.`

Recibes una revisión con fortalezas y riesgos reales, el paquete de archivos y la lista de lo que queda a mano.

## 5. Dónde queda cada cosa

```
tu-carpeta/
├── marca.json                       ← tu marca, en un archivo
└── trabajo/2026-11-15-marca-nombre/
    ├── estrategia.md                ← entrevista, territorio y manifiesto
    ├── voz.md
    ├── logo/                        ← tus archivos de logo
    ├── tokens/                      ← CSS, Tailwind, contraste, ejemplo.html
    ├── kit.json                     ← el contenido del manual
    ├── kit/                         ← el manual (abre index.html)
    └── entrega/                     ← el paquete final
```

## 6. Sacar el manual en PDF

Abre `kit/index.html` en el navegador y usa **Imprimir → Guardar como PDF**, con orientación horizontal. Si tu ordenador tiene `rsvg-convert`, el PDF se genera solo, pero no es necesario.

## 7. Problemas frecuentes

| Qué ves | Qué pasa | Qué hacer |
|---|---|---|
| «python3: command not found» | Python no está instalado, o en tu sistema se llama distinto | Prueba `python` o `py`. Si no existe, instala Python 3.11+ |
| La skill no aparece | La sesión no ha cargado el plugin | Abre una sesión nueva, o `/reload-plugins`, y mira `claude plugin list` |
| `ERROR el texto … da 2.39:1; mínimo 4,5:1` | El color de tu texto casi no se lee sobre el fondo | Cambia el color de texto o el de fondo en `marca.json`. La skill no parchea los tokens |
| `aviso el acento … no para texto` | Tu color de acento es bonito pero no sirve para letra pequeña | No es un error. Úsalo en líneas, iconos grandes o fondos |
| El logo del manual es solo tu nombre en letras | Falta el archivo del logo | Es el logotipo provisional. Guarda tu logo en `logo/` y vuelve a generar el manual |
| La imagen de Canva solo llega pequeña | El conector deja una miniatura en el equipo; la imagen completa está en Canva | El enlace no se descarga con `curl` (403): mete la imagen en un diseño de Canva y expórtalo a PNG (ver `skills/canva/SKILL.md`) |
| El manual se ve correcto pero aburrido | Es normal: la herramienta cumple reglas, no tiene gusto | Pasa las cinco preguntas de `criterio-visual.md` y completa tus referencias |
| Las fuentes se ven distintas a las elegidas | Se cargan desde Google Fonts y no hay conexión | Conéctate, o instala la fuente en tu ordenador |
| Un texto del manual acaba en «…» | No cabía en la lámina | Es intencionado: lo largo va al documento, no a la lámina |

Si no lo resuelves, copia el mensaje de error completo y pégaselo a Claude.

## 7. Lo que queda por hacer a mano

La IA construye el andamio; la fachada la haces tú. Antes de publicar:

- **Logotipo a contornos y retocado.** Conviértelo a vector y ajusta a ojo el espaciado entre letras y algún detalle propio. Es lo que separa una marca de una fuente escrita en grande.
- **Fotografía propia** que sustituya a los marcadores del manual.
- **Comprobar el nombre:** búsqueda de marcas registradas (OEPM, EUIPO) y dominio libre.
- **Revisar los claims** de tu sector («artesanal», «natural», «sostenible» pueden estar regulados).
- **Confirmar la licencia de las fuentes** para uso comercial y web.

## 8. Actualizar y desinstalar

Cuando tu profesor te pase una versión nueva, reemplaza la carpeta y ejecuta:

```bash
claude plugin marketplace update brand-kit-builder
```

```bash
claude plugin update brand-kit-builder@brand-kit-builder
```

Después, **reinicia Claude Code** para que cargue la versión nueva. Si el segundo comando responde «already at the latest version», es que la versión nueva todavía no tiene un número distinto (por ejemplo 2.0.1): pídele a tu profesor que la publique con número nuevo.

Para quitarlo:

```bash
claude plugin uninstall brand-kit-builder@brand-kit-builder
```
