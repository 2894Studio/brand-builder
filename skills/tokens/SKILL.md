---
name: tokens
description: Convierte marca.json en tokens de diseño para producto digital: tokens.json (W3C Design Tokens), variables CSS, preset de Tailwind v3 y bloque @theme de v4, tabla de contraste y una página de ejemplo con botón, tarjeta y formulario. Úsala con «que mi marca funcione en mi web o app», «design tokens», «variables CSS», «Tailwind con mis colores», «mi desarrollador necesita los colores y fuentes».
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Tokens de diseño

Lo que separa una marca que se ve bien en un manual de una que funciona en el producto: que quien programa no tenga que reinterpretarla. Los tokens son la marca convertida en valores que el código consume.

Requiere un `marca.json` válido y aprobado (`identidad`). Lee `references/formato-tokens.md` y `references/escala-web.md`.

## Generar

> En Windows, `python3` suele ser `python` o `py`. Necesita Python 3.11 o superior.

```
python3 tools/validar_marca.py marca.json
python3 tools/generar_tokens.py marca.json --salida trabajo/<fecha>-marca-<slug>/tokens
```

Solo usa la librería estándar de Python (probado en 3.11 y 3.13). Salida:

| Archivo | Para qué |
|---|---|
| `tokens.json` | Fuente de verdad, formato W3C (`$value`, `$type`), con primitivos y semánticos |
| `tokens.css` | Variables CSS `:root` para cualquier proyecto |
| `tailwind.preset.js` | Preset de Tailwind v3 (`presets: [require(...)]`) |
| `tailwind-v4.css` | Bloque `@theme` de Tailwind v4 |
| `contraste.md` | Pares texto/fondo con su ratio real |
| `ejemplo.html` | Botón, tarjeta y formulario con los tokens |

## Qué comprueba y qué hace si falla

- **Falla (sale con error)** si un par obligatorio de texto no llega a 4,5:1: tinta sobre base, texto atenuado, texto sobre marca, texto sobre acento. No inventa un gris que no se lea: si el atenuado no pasa, usa la tinta.
- **Avisa, no falla**, de los colores que no sirven para texto (un acento verde sobre claro suele quedarse en 2:1): se documentan para qué sí valen.
- Si el contraste falla por un color aprobado, **vuelve a `identidad`**. No parchees los tokens: el problema está en la paleta.

## Después de generarlos

1. Enséñale a la persona `ejemplo.html`: es la prueba de que la marca funciona en producto. Si no le convence, el ajuste va en `marca.json`, no en los archivos generados.
2. Explica en cuatro líneas cómo se usan: copiar `tokens.css` al proyecto, o el preset a `tailwind.config.js`, o el `@theme` en el CSS de Tailwind v4.
3. Anota en `marca.json` → `brandKit.tokens` la ruta de la carpeta.

**Límites:** sin modo oscuro en esta versión (se hace invirtiendo base y tinta y comprobando de nuevo el contraste) y la fuente se carga desde Google Fonts si hay conexión; para producción, autoaloja las fuentes y confirma su licencia.

Siguiente: `laminas`.
