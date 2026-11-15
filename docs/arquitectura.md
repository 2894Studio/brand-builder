# Arquitectura

## Flujo

```
brand-kit-builder (entrada: lee, decide, enruta)
   │
   ├─ estrategia ──► estrategia.md + borrador de marca.json
   ├─ identidad  ──► logo/ + marca.json completo y validado      ← punto de no retorno
   ├─ voz        ──► voz.md + tono y palabrasProhibidas
   ├─ tokens     ──► tokens/  (tokens.json, css, tailwind, contraste, ejemplo)
   ├─ laminas    ──► kit/     (SVG, index.html, PDF opcional)
   ├─ entrega    ──► entrega/ (paquete, LEEME, lista de lo que queda a mano)
   └─ canva      ──► opcional
```

Cada paso termina con aprobación de la persona. Los pasos que generan archivos leen `marca.json`; nadie reintroduce datos que ya están ahí.

## Contrato `marca.json`

Raíz del proyecto. Campos que lee creative-architect (documentados en `skills/direccion-de-arte/references/marca.md` de su repositorio):

| Campo | Lo escribe | Notas |
|---|---|---|
| `nombre`, `categoria`, `idioma` | estrategia | `idioma` con forma `es` o `es-ES` |
| `tono` | voz | Una frase con trato, distancia, humor y ritmo |
| `palabrasProhibidas` | voz | Al menos cinco, propias de la categoría |
| `visual.colores[]` | identidad | `{nombre, hex, rol}`, rol ∈ `primario`, `fondo`, `acento`, `texto` |
| `visual.estilo` | identidad | Técnica (luz, grano, paleta, encuadre), mínimo 20 caracteres |

Extensiones propias, que los oficios de creative-architect ignoran:

| Campo | Para qué |
|---|---|
| `tipografia.{titulos,texto}` | Familias, pesos, licencia y fuente. Máximo dos |
| `publico`, `competidores` | Contexto estratégico |
| `brandKit.territorio` | `artesanal`, `editorial`, `tecnologico`, `natural` o `cercano`: decide la firma gráfica y el radio de los componentes |
| `brandKit.neutro` | El quinto color. El contrato no tiene rol para él |
| `brandKit.logo[]` | `{version, archivo}`, rutas relativas a `marca.json` |
| `brandKit.tokens`, `brandKit.version` | Trazabilidad |

Esquema en `skills/tokens/marca.schema.json`; la validación completa (contraste, léxico) en `skills/tokens/tools/validar_marca.py`.

## Salida adicional: motion-architect

`skills/tokens/tools/exportar_motion.py` escribe `studio/brand.json` de motion-architect: `name`, `tagline`, `colors{background, surface, text, muted, accent, accent2}`, `fonts{display, body}`, `radius`, `style`. `accent` es el primario y `accent2` el acento. Las fuentes reales se cambian en `src/brand/brand.ts`, no en el JSON.

## Decisiones

- **`marca.json` pronto, no al final.** Así creative-architect puede trabajar con la marca mientras se sigue con el manual.
- **El contraste es un error, no un consejo.** Un texto declarado que no se lee impide generar tokens y láminas.
- **El núcleo de código vive en `skills/tokens/tools/marca_lib.py`** y lo importan `laminas` e `identidad`. El plugin se instala entero, así que la ruta es estable; si alguien copia una skill suelta, el error dice qué falta.
- **Sin dependencias.** Todo con Python estándar, para que un alumno no tenga que instalar nada.
- **Las referencias se dividen por oficio** para cargar solo lo necesario en cada paso.
