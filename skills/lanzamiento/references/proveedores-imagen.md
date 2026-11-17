# Proveedores de imagen: cuál usar y cómo

Las piezas de calidad necesitan **imágenes buenas** (fotos de personas, objetos sobre color liso, lugares). Se pregunta **una vez** al empezar (ver abajo) y se guarda con `skills/brand-kit-builder/tools/proveedor_imagen.py`. Los prompts salen de `tools/prompts_fotos.py` (con `--proveedor auto` usa el guardado), la foto va a `fotos/`, se anota con `tools/registrar_foto.py` (origen `ia`) y se prepara con `preparar_fotos.py`.

| Proveedor | Cómo se usa | Coste | Estado en este plugin |
|---|---|---|---|
| **Canva** | Conector: `generate-image` + exportar un diseño y descargar (receta en `fotos.md`) | Créditos de Canva | **Verificado** con una cuenta real. Imágenes 1080×1440; Canva a veces añade una página en blanco |
| **FLORA** | Conector: `flora_create_generations` con presupuesto previo (`quote: true`); descarga directa con `curl` | USD por imagen (0,02–0,18) | **Verificado** (3 imágenes). Plan gratuito con tope de proyectos |
| **Gemini (API)** | `tools/generar_gemini.py` con `GEMINI_API_KEY` (la clave se pide en AI Studio) | **De pago por uso**: el nivel gratuito tiene límite 0 para imágenes | Verificado con una clave real el 2026-11-17: lista 6 modelos de imagen y **responde 429 «free tier, limit: 0»** hasta activar la facturación. La generación completa solo está probada con un servidor simulado |
| **Gemini / Google Flow (web)** | Pegar el prompt a mano y guardar la imagen | Cuota gratuita con cuenta Google (según el plan) | Sin ejecutar desde el plugin |
| **Higgsfield** | Su conector MCP si lo tienes; si no, a mano | De pago | **No verificado** |
| **Magnific** | Sobre todo **mejorar** una foto (ampliar, dar detalle): pasa por él la foto elegida | De pago | **No verificado** (existe un ampliador Magnific dentro de FLORA) |
| **Spaces** (p. ej. de Freepik) | A mano o por su conector si lo hay | De pago | **No verificado** |
| **Ninguno** | Fotos propias o de banco (`buscar_fotos.py` con Pexels; descarga a mano de Unsplash o Pixabay) | Gratis | Verificado el flujo de créditos |

## La pregunta (una vez, con un diálogo)
«¿Tienes algún proveedor de imagen para mejorar la calidad de las piezas?» Opciones: **Canva** · **FLORA, Higgsfield, Magnific, Spaces u otro de pago** (que escriba cuál) · **Gemini o Flow (gratis)** · **Ninguno por ahora**. Se pregunta tras aprobar logo y paleta (cuando ya hacen falta fotos) o antes si pide imágenes en `identidad`. Se guarda con `proveedor_imagen.py guardar` y no se vuelve a preguntar.

## Reglas
- **Con proveedor, no se entregan marcas visuales sin fotos:** la puerta de entrega ya lo exige. Sin proveedor, se dice qué queda por hacer a mano.
- **Coste antes de generar** siempre (en USD o créditos) y un sí por tanda.
- **Resolución:** el lado corto debe llegar a 1080 px; si un proveedor da menos (Gemini suele dar ~1024), pide `--tamano 2K` si el modelo lo admite o ampliala (Magnific, o el ampliador de FLORA).
- **Personas sintéticas** no se presentan como el equipo ni los clientes reales.
