# Explorar direcciones con FLORA: «Logo to Brand Identity» (opcional, de pago)

**Qué es:** una técnica guardada de FLORA (`tech_ts71w3sw3e1ghhyz6reejcgrch85ass0`). Entra **un logo** sobre fondo liso y salen **tres tableros de identidad** (paleta, tipografía, aplicaciones e imagen en una misma dirección), generados con GPT Image. Lee las letras, la construcción, el color y el acabado del logo e **infiere** la categoría y el público.

**Cuándo sí:** el logo y la paleta ya están aprobados, la marca no tiene sistema de imagen claro y la persona tiene el conector de FLORA con saldo. Sirve para **explorar** tres direcciones, sobre todo en una demo o en un encargo.
**Cuándo no:** alumnos sin cuenta de FLORA (es de pago), o cuando ya hay referencias claras en `gusto.json`.

## Coste (decirlo siempre antes)
Se lee **en vivo** con `flora_get_technique` (`run_cost`, en USD, nunca créditos). Referencia: 4,282 USD el 2026-11-16 (la documentación de la skill decía 3,52 USD a principios de mes: **cambia**). Una ejecución, un presupuesto, un sí. Nunca se repite sin otro sí.

## Pasos (los llamas tú con el conector; los scripts no gastan nada)
1. **Prepara la entrada:** `python3 skills/identidad/tools/flora_logo.py preparar marca.json --salida trabajo/<…>/flora` → `logo-entrada.png` (logo principal centrado sobre fondo liso).
2. **Workspace:** `flora_list_workspaces`; si hay varios, di cuál se factura. Dile que `flora_run_technique` factura el workspace por defecto.
3. **Sube el logo:** `flora_create_asset` con `source: "signed-url"` (la técnica solo lee medios de FLORA) y sube el archivo con el descriptor que devuelve; termina con `flora_complete_asset`. Usa la `url` resultante.
4. **Presupuesto y sí:** `flora_get_technique` → «Logo to Brand Identity cuesta X USD por ejecución. ¿La ejecuto?» **Espera el sí.**
5. **Ejecuta:** `flora_run_technique` con `{"logo": "<url>"}` (y `skill: "flora-logo-to-brand-identity"` con un `skill_run_id` inventado, solo para el registro). Consulta con `flora_list_generations` pasando `run_ids` y `technique_id` hasta `completed` o `failed`. Si falla, no reintentes.
6. **Trae los tableros:** las 3 `outputs[].url` se descargan con `curl`. Guárdalas y mídelas: `python3 skills/identidad/tools/flora_logo.py guardar URL1 URL2 URL3 --salida trabajo/<…>/flora` → `tableros/`, `medidas-flora.json` y `direccion-flora.md`.
7. **Míralos de verdad** (abre cada `tablero-N.png`) y rellena en `direccion-flora.md` qué propone cada uno y qué **no** se copia.
8. **Decide con la persona** con un diálogo (tablero 1, 2, 3 o mezcla).

## Reglas
- **Los tableros son inspiración, no la marca.** Un modelo de imagen dibuja los textos, las tipografías y los códigos de color: no son fiables. De la dirección elegida se toma la **paleta medida** (hay que comprobar el contraste con `contraste.py`), el estilo de imagen y el gráfico firma, y se anota en `marca.json` → `visual.estilo` y en `kit.json` → `fotografia`.
- **La técnica infiere solo del logo.** Si contradice la estrategia (público, tono, léxico prohibido, «nunca debe parecer»), gana la estrategia.
- **No se copia ninguna marca ni imagen** que aparezca en un tablero.
- **No verificado con una ejecución real en este plugin** (la integración se probó con tableros simulados): la primera ejecución real dirá qué ajustar.
