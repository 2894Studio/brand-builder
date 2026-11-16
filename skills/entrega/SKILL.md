---
name: entrega
description: "Cierra el proyecto de marca: revisión de experto con fortalezas y riesgos reales, paquete de archivos con LEEME, lista explícita de lo que queda por hacer a mano y traspaso a creative-architect. Úsala con «revisa mi marca», «qué me falta», «está lista para publicar», «entrega el kit», «qué hago ahora con esto»."
license: MIT
---
<!-- Copyright (c) 2026 2894 Studio · MIT -->

# Entrega

Una marca entregada sin decir qué falta se publica con acabado de plantilla. Aquí se cierra con honestidad. Lee `references/checklist-revision.md`, `references/a-mano.md` y `references/legal-y-claims.md`.

## 1. Revisión de experto

Recorre el checklist y escribe **fortalezas y riesgos con el mismo rigor**, no halagos. Vuelve a ejecutar `python3 ../tokens/tools/validar_marca.py marca.json` y `python3 ../laminas/tools/verificar_laminas.py`. Si algo falla, se corrige antes de entregar.

Vuelve a pasar el crítico (`../gusto/tools/critico_render.py`) sobre el bento y los dos posts: deben tener 0 errores, o decir cuáles quedan y por qué.

Pasa además la lista de `../laminas/references/criterio-visual.md` y confirma que los logos llevan la fuente incrustada (`../identidad/tools/incrustar_fuente.py`). Si no has podido ver el manual renderizado, dilo.

## 2. Paquete

En `trabajo/<fecha>-marca-<slug>/entrega/`:

- **Sueltos**, para arrastrar: las versiones del logo en SVG y, de repuesto, PNG a 3000 px con fondo transparente.
- **Un ZIP con LEEME** (plantilla en `references/leeme-plantilla.md`) que diga, archivo por archivo, qué es y para qué sirve.
- `tokens/` completo y `kit/` (`index.html` y PDF si existe).
- `lanzamiento/` completo: el logo en SVG y PNG, el bento y los dos posts (qué es la marca y su principal atributo), con sus HTML editables. Comprueba que existen los cuatro resultados; si falta alguno, vuelve a `lanzamiento` antes de entregar. Lo que sea de ejemplo (fotos, personas, datos) va en el `LEEME.md` de esa carpeta.
- Las imágenes que ya viven en otra cuenta (Canva, un proveedor de imagen) no se duplican: lista con el enlace de cada una.
- Di cuáles **no** conviene subir ni usar y por qué: una textura que en realidad es color plano no aporta nada que la paleta no cubra; inventar iconos que nadie aprobó, tampoco.

## 3. Qué queda a mano (obligatorio, no cortesía)

Como mínimo: el logotipo convertido a contornos y retocado (kerning del nombre, una ligadura propia, el asta de una letra) · la composición de los fragmentos visuales con su desalineación y su grano · la fotografía propia que sustituya a la generada. La tabla completa está en `references/a-mano.md`.

## 4. Tareas que no puedes cerrar tú

Dilas explícitamente: comprobar anterioridades del nombre y dominio · validar los claims legales del sector · confirmar la licencia de las fuentes · sustituir las imágenes generadas. No son asesoría legal.

## 5. Traspaso

Ofrece una sola vez seguir con creative-architect, que ya lee `marca.json`: `/avatar`, `/producto`, `/direccion-de-arte`. Comprueba que `marca.json` está en la raíz y es válido: es lo que le ahorra volver a explicar la marca.

Cierra con una línea y la lista de rutas de los archivos creados.
