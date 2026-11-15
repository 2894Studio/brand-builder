# Prueba guiada (para el profesor)

Tres pruebas de 10 minutos cada una antes de enseñar la skill a tus alumnos. Todas funcionan sin gastar créditos de imagen.

## Preparación

```bash
claude plugin marketplace add ./brand-kit-builder
claude plugin install brand-kit-builder@brand-kit-builder
```

Crea una carpeta vacía por prueba y abre Claude Code dentro de ella. Si no quieres instalar, arranca con `claude --plugin-dir /ruta/a/brand-kit-builder`.

Estado de lo verificado antes de entregártelo: las pruebas 1, 2 y 3 se ejecutaron con el modelo en Linux y pasaron con las incidencias que se indican abajo. No se ha probado en Windows ni en macOS, ni con generación real de imágenes.

## Prueba 1. Humo

Escribe: `/brand-kit-builder ¿qué puedes hacer?`

**Debe pasar:**
- Responde en unas cinco líneas: estrategia, identidad, voz, tokens, manual y revisión.
- Dice que Canva es opcional.
- Pregunta por dónde quieres empezar.
- Comprueba si hay `marca.json` y, si no, lo dice.

## Prueba 2. Entrevista sin imágenes

Escribe: `Necesito crear la marca de una panadería de barrio en Lavapiés. Llevamos dos años vendiendo pan de masa madre y queremos algo que se note artesanal pero que no sea caro. No tengo logo ni nada.`

**Debe pasar:**
- Hace la **ronda 1 en un solo mensaje** y no genera ningún logo ni prompt de imagen.
- Te trata de tú.
- No adelanta soluciones («lo normal sería un logo tipográfico»).
- Reconoce lo que ya le has contado y solo pregunta lo que falta.

**Sigue la conversación** respondiendo a las rondas 2 y 3 y comprueba además:
- Pregunta **qué nunca debe parecer** la marca.
- Pregunta si quieres mockups **antes** de generar nada.
- Cierra con un resumen de 3 a 5 líneas y espera tu «confirmado».
- Propone **tres territorios**, ninguno anclado en otras panaderías.
- Al llegar al logo, ofrece **exactamente dos** opciones.

## Prueba 3. Marca existente → tokens y manual

```bash
mkdir -p prueba3/trabajo/pulso
cp brand-kit-builder/evals/fixtures/pulso/marca.json prueba3/marca.json
cp brand-kit-builder/evals/fixtures/pulso/kit.json prueba3/trabajo/pulso/kit.json
```

Abre Claude Code en `prueba3/` y escribe: `Ya tengo marca.json y el contenido del manual en trabajo/pulso/kit.json. Genera los tokens de diseño para mi web con Tailwind y el manual de marca. Guarda todo dentro de trabajo/pulso/.`

**Debe pasar:**
- Existen `tokens/` (con `tokens.css`, `tailwind.preset.js`, `contraste.md`, `ejemplo.html`) y las láminas con `index.html`.
- Avisa del **acento verde sin contraste** (2,12:1) sin tratarlo como error.
- Avisa de que el **logo es provisional**.
- Abre `ejemplo.html` e `index.html` en el navegador y mira las láminas.

**Resultado en la verificación:** pasó. El manual salió en `kit-manual/` en lugar de `kit/`: es el nombre que eligió el modelo; no afecta al contenido.

## Prueba 4 (opcional). Un contraste que falla

En `prueba3/marca.json`, cambia el hex del color con rol `texto` a `#9AA0AA` y pide de nuevo los tokens. **Debe** negarse a generar y decir que el texto sobre el fondo da 2,39:1.

## Cómo anotar un fallo

| Qué pediste | Qué esperabas | Qué pasó | Skill |
|---|---|---|---|
| | | | |

Añade tu sistema operativo y versión de Python (`python3 --version`). Con esa tabla se corrige la skill concreta que falló.

## Incidencias ya corregidas durante la verificación

- Trataba de usted. Ahora trata de tú.
- Adelantaba una solución antes de cerrar la entrevista. Ahora no.
