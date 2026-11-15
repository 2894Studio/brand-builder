# ¿Qué herramienta uso para qué?

Tabla de decisión para posts estáticos y de video. Los datos de los repositorios salen de leerlos (README, manifiestos y `SKILL.md`); no se han ejecutado las tres herramientas completas con el modelo, salvo lo que se indica.

## Resumen

| Quiero… | Usa | Gasta créditos |
|---|---|---|
| Una imagen para un post | creative-architect (`direccion-de-arte`, `producto`) + Canva | Sí, por imagen |
| Un post solo con texto, cifras o citas | Canva con la fuente de la marca | No |
| Una pieza animada (intro, reel, logo, datos) sin cámara | motion-architect | No (se renderiza en tu ordenador) |
| Mover una imagen que ya tengo | creative-architect (`animar`) + un proveedor de video | Sí |
| Editar un video que he grabado yo (cortes, subtítulos, SFX) | video-editor-architect | No, salvo opciones de pago |

## Comparación

| | creative-architect | motion-architect | video-editor-architect |
|---|---|---|---|
| **Qué es** | Plugin de Claude Code, 8 skills | Plugin con instalador y un agente | Plantilla que se clona, **no es plugin** |
| **Entrada de marca** | `marca.json` | `studio/brand.json` (con el puente) | `creador.json` y estilos aprendidos |
| **Instalación** | Dos comandos | `git clone` + `./install.sh` | `git clone` + `npm ci` + `npm run instalar` |
| **Requisitos** | Ninguno duro; un proveedor para generar | Node 18+, ffmpeg, yt-dlp, Python 3, Remotion | Node 24+, ffmpeg, whisper.cpp (modelo de ~3 GB), Python con `uv`, Chrome, Remotion |
| **Sistemas** | Los de Claude Code | Linux y macOS (instalador bash) | macOS y Windows según su README |
| **Salida** | Imágenes, clips o prompts | MP4 en 9:16, 16:9, 1:1 y 4:5, más un póster | MP4 vertical de alta resolución |
| **Dificultad para empezar** | Baja | Media | Alta |

## Recomendación para la primera sesión

1. **creative-architect** para el post fijo.
2. **motion-architect** para el video, con la marca importada.
3. **video-editor-architect** más adelante, solo para quien graba su propio metraje y publica con frecuencia.

## Cosas que conviene saber

- **creative-architect no trae Canva como proveedor** (documenta Higgsfield, Magnific y OpenAI). El camino que usamos: creative-architect escribe el prompt, Canva lo ejecuta. Añadir Canva como proveedor sería una contribución a su repositorio.
- **Canva y la marca:** `generate-image` genera una imagen suelta (admite 4:5 y 9:16). Para un diseño completo con la marca del alumno hay que usar `generate-design` con su `brand_kit_id`; `create-design` no aplica Brand Kits. Los Brand Kits se suben a mano: el conector no los crea.
- **motion-architect y las fuentes:** la fuente real sale de `src/brand/brand.ts`; el campo `fonts` de `brand.json` es solo informativo. El puente imprime las líneas exactas que hay que pegar.
- **Licencia de Remotion** (motion-architect y video-editor-architect): gratis para personas, entidades sin ánimo de lucro y empresas de hasta 3 personas; las de 4 o más necesitan licencia comercial. Revisa los términos de Remotion antes de usarla en un proyecto de empresa.
- **Los repositorios son públicos**, aunque los README de motion-architect y video-editor-architect dicen que son privados (se clonaron sin credenciales).
- **Windows:** el instalador de motion-architect es un script de bash. En Windows hace falta WSL o Git Bash; no se ha probado.

## Puente de marca (Brand Kit Builder → motion-architect)

```bash
python3 skills/tokens/tools/exportar_motion.py marca.json --salida motion-architect/studio/brand.json --forzar --tagline "Tu claim" --studio motion-architect/studio
```

Qué hace y qué no:

| Hace | No hace |
|---|---|
| Convierte colores, nombre, radio y estilo al formato de motion-architect | No cambia las fuentes del proyecto: imprime las líneas para `brand.ts` |
| Usa el color primario como `accent` y el acento como `accent2`, porque `accent` lleva texto resaltado y debe leerse | No exporta el logo: va en `studio/public/brand/logo.svg` |
| Guarda una copia `.bak` antes de sobrescribir | No sobrescribe sin `--forzar` |
| Avisa de los colores que no tienen contraste suficiente | No trae el neutro de la marca: no tiene hueco en `brand.json` |

Verificado con PULSO: el archivo tiene exactamente la forma del `brand.json` original, TypeScript lo acepta tras cambiar los imports de fuentes, y un fotograma renderizado muestra los colores, las fuentes y las esquinas de la marca.
