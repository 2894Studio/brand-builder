# brand-kit-builder

Plugin de Claude Code para crear la identidad de una marca de principio a fin: **entrevista, estrategia, logo, paleta, tipografía, voz, tokens de diseño para web y app, y manual de marca**. Funciona sin ninguna herramienta de pago, y deja un `marca.json` que [creative-architect](https://github.com/Hainrixz/creative-architect) ya sabe leer.

Desarrollado por [2894 Studio](https://github.com/2894Studio) a partir del caso práctico de la formación **Marketing potenciado por IA**.

## Qué resuelve

- **Una marca que se defiende:** entrevista en tres rondas, territorios anclados fuera de la categoría y un manifiesto con el miedo de la marca. Contra la marca promedio que devuelve la IA por defecto.
- **Una marca que funciona en producto:** los tokens (`tokens.json`, variables CSS, Tailwind v3 y v4) salen del mismo `marca.json` que el manual, con el contraste comprobado. Quien programa no reinterpreta nada.
- **Una marca que no se explica dos veces:** `marca.json` se escribe en cuanto se aprueban logo y paleta, y lo leen las demás skills de creative-architect.
- **Sin dependencias:** el manual sale como SVG y HTML con Python estándar. Canva es un módulo opcional.

## Guías

- [Guía del alumno](docs/guia-alumnos.md): instalación, uso paso a paso y problemas frecuentes.
- [Guion de clase](docs/guion-clase.md): sesión de 90 minutos con demo, ejercicio y rúbrica.
- [Prueba guiada](docs/prueba-guiada.md): tres pruebas para comprobar la skill antes de enseñarla.
- [Guion de introducción](docs/guion-introduccion.md) y [guion de la sesión de contenido](docs/guion-sesion-contenido.md): la clase siguiente, con posts fijos y animados.
- [Elegir herramienta](docs/elegir-herramienta.md): creative-architect, motion-architect y video-editor-architect, comparadas.
- [Ahorro de tokens y créditos](docs/ahorro-tokens.md): dónde se gasta y qué hacer, con datos medidos.

## Instalación

Mientras el repositorio no esté publicado, se instala desde la carpeta (o desde el ZIP descomprimido): `claude plugin marketplace add ./brand-kit-builder` y después `claude plugin install brand-kit-builder@brand-kit-builder`. Las dos rutas están explicadas en la [guía del alumno](docs/guia-alumnos.md).

Como plugin, igual que creative-architect:

```bash
claude plugin marketplace add 2894Studio/brand-kit-builder
claude plugin install brand-kit-builder@brand-kit-builder
```

Desde una copia local:

```bash
git clone https://github.com/2894Studio/brand-kit-builder.git ~/brand-kit-builder
claude plugin marketplace add ~/brand-kit-builder
claude plugin install brand-kit-builder@brand-kit-builder
```

Para producir imágenes con un proveedor, instala también creative-architect (opcional; sin él, la skill entrega prompts para pegar):

```bash
claude plugin marketplace add Hainrixz/creative-architect
claude plugin install creative-architect@creative-architect
```

## Uso

Habla normal:

> «Necesito crear la marca de una panadería de barrio en Lavapiés.»
> «Quiero que mi marca funcione en mi web con Tailwind.»

Skills, cada una con su comando:

| Skill | Hace |
|---|---|
| `/brand-kit-builder` | Entrada: lee la petición y enruta |
| `/estrategia` | Entrevista, tres territorios, manifiesto |
| `/identidad` | Dos logos, paleta de cinco colores, tipografía |
| `/voz` | Trato, rasgos, seis situaciones, palabras prohibidas |
| `/tokens` | `marca.json` → tokens para web y app |
| `/laminas` | Manual de marca en SVG, HTML y PDF |
| `/entrega` | Revisión, paquete y lista de lo que queda a mano |
| `/canva` | Opcional: montar el kit en Canva |

## Cómo se conecta con creative-architect

`marca.json` en la raíz del proyecto es el contrato. Esta skill escribe exactamente los campos que creative-architect documenta (`nombre`, `categoria`, `tono`, `palabrasProhibidas`, `idioma`, `visual.colores`, `visual.estilo`) y añade extensiones que sus oficios ignoran (`tipografia`, `publico`, `competidores`, `brandKit`). El neutro de la paleta va en `brandKit.neutro`, porque el contrato solo admite los roles `primario`, `fondo`, `acento` y `texto`. Detalle en [docs/arquitectura.md](docs/arquitectura.md).

## Estructura

```
.claude-plugin/        plugin.json · marketplace.json
agents/                brand-kit-builder.md
skills/
  brand-kit-builder/   entrada
  estrategia/          references/
  identidad/           references/ · tools/contraste.py
  voz/                 references/
  tokens/              references/ · tools/ · marca.schema.json · marca.plantilla.json
  laminas/             references/ · tools/
  entrega/             references/
  canva/               references/ (opcional)
evals/                 casos de evaluación y marca de prueba (PULSO)
docs/arquitectura.md
```

## Comprobar que funciona

```bash
python3 skills/laminas/tools/verificar_laminas.py
python3 skills/tokens/tools/verificar_tokens.py
python3 skills/tokens/tools/validar_marca.py evals/fixtures/pulso/marca.json
python3 skills/tokens/tools/generar_tokens.py evals/fixtures/pulso/marca.json --salida /tmp/pulso-tokens
```

Probado con Python 3.11 y 3.13. Solo librería estándar.

## Puente a motion-architect

`skills/tokens/tools/exportar_motion.py` convierte `marca.json` en el `brand.json` de motion-architect, para que sus animaciones usen tu marca. Detalle y límites en `skills/tokens/SKILL.md`.

## Límites conocidos

- Un logo generado por IA es referencia: el logotipo final se reconstruye en vector y se retoca a mano (kerning, ligaduras). La skill lo dice en cada entrega.
- Sin `rsvg-convert` no se genera el PDF directamente; se imprime `index.html` desde el navegador.
- Los marcadores de fotografía del manual se sustituyen por fotografía propia.
- Sin modo oscuro en los tokens de esta versión.
- Las comprobaciones de nombre, claims y licencias de fuentes quedan señaladas como pendientes de validación profesional. La skill no da asesoría legal.
- El módulo de Canva describe el conector tal como se documentó en la versión anterior y no se ha vuelto a verificar.

## Hoja de ruta

Naming con comprobación guiada de dominio y anterioridades · arquitectura de marca y submarcas · kit de lanzamiento (perfiles, firma de correo, plantilla de propuesta, icono de app) · modo oscuro en los tokens.

## Licencia

MIT. Créditos en [NOTICE](NOTICE).
