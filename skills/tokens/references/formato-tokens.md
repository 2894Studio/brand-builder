# Formato de los tokens

`tokens.json` sigue el formato de la comunidad W3C Design Tokens: cada token es un objeto con `$value`, `$type` y, si hace falta, `$description`. Las herramientas de diseño y de transformación (por ejemplo Style Dictionary) lo leen sin adaptar.

## Dos capas

**Primitivos:** lo que la marca *es*. `color.primitive.ink`, `.base`, `.brand`, `.accent`, `.neutral`. Cambian solo si cambia la marca.

**Semánticos:** para qué se usa. Referencian a los primitivos con `{color.primitive.ink}`.

| Token | Uso | Garantía |
|---|---|---|
| `color.text.default` | Texto principal | ≥ 4,5:1 sobre `surface.base` |
| `color.text.muted` | Texto secundario | ≥ 4,5:1 sobre `surface.base`; si no llega, es la tinta |
| `color.text.on-brand` | Texto sobre `surface.brand` | ≥ 4,5:1 |
| `color.text.accent` | Solo existe si el acento llega a 4,5:1 sobre la base | ≥ 4,5:1 |
| `color.surface.base` / `.brand` / `.subtle` | Fondos | |
| `color.accent.default` / `.on-accent` | Acento y texto sobre él | `on-accent` ≥ 4,5:1 |
| `color.border.default` | Bordes decorativos | No cumple 3:1: no usar en campos de formulario |

**Regla para quien programa:** usa siempre semánticos en componentes; los primitivos solo para definir los semánticos.

## Cómo se consumen

- **CSS:** `var(--color-text-default)`. Los nombres salen de la ruta del token con guiones.
- **Tailwind v3:** `presets: [require('./tailwind.preset.js')]` → `bg-brand`, `text-ink`, `font-heading`.
- **Tailwind v4:** pega el bloque `@theme` de `tailwind-v4.css` en tu CSS de entrada.

## Radio por territorio

El radio sale de la firma gráfica: artesanal y editorial 0 · tecnológico 4 px · cercano 16 px · natural 24 px. Un `pill` de 9999 px está siempre disponible.
