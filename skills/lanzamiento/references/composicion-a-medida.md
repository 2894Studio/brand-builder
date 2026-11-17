# Composición a medida: diseñar la pieza, no rellenar una plantilla

Los generadores de plantilla (`post_telefono`, `post_tipografico`…) dan piezas correctas y **parecidas entre sí**. Cuando la persona tiene un gusto entrenado, la pieza se **diseña** con `post_compuesto.py`: tú decides los elementos y dónde van, el script los dibuja con la paleta y las fuentes de la marca.

## Proceso (obligatorio si `gusto.json` tiene reglas de composición para posts: **los dos posts** son a medida)
1. **Mira las referencias antes de diseñar.** `python3 skills/gusto/tools/contacto_referencias.py --gusto gusto.json --referencias referencias/ --para post --salida lanzamiento/` → `contacto-post.png` con las referencias que aplican a posts y sus reglas R1…Rn. Ábrelo de verdad.
2. **Escribe el concepto** (3 líneas): qué reglas traduces (R#), qué elementos usas (palabra gigante, foto con marco, forma de acento, gráfico firma, cifra…) y cómo se organiza (dónde está el peso, qué se recorta, cuánto aire).
3. **Escribe la especificación** `composicion-post-N.json` (formato y ejemplo: `python3 skills/lanzamiento/tools/post_compuesto.py --ejemplo`). `concepto.referencias` cita las reglas; sin ellas el script se niega.
4. **Pónlo en el brief** como `"recurso": "compuesto", "args": {"spec": "composicion-post-1.json"}` y ejecuta `kit_lanzamiento.py`.
5. **Mira el resultado junto a las referencias** y ajusta una cosa cada vez (`ajustes.md`).

## Lo que la puerta exige (no es opcional)
- **Los dos posts** son `compuesto` (o `html` propio) cuando el gusto tiene reglas de composición para posts. Dos composiciones a medida no son «la misma plantilla» si su disposición cambia (`variedad.py` compara dónde están los elementos). Solo `plantillas_ok` con motivo lo evita.
- Cada composición cita **al menos una regla gráfica** (símbolo, forma, firma o imagen) además de las de aire y tipografía: «minimalista, con aire» es lo más fácil de cumplir y no es una idea.
- Cada composición lleva **al menos un elemento gráfico** (forma, firma, foto, insignia, símbolo o palabra gigante). `post_compuesto.py` se niega a dibujar una que sea solo texto: es una plantilla con otro nombre.
- El **símbolo del logo** a gran tamaño, recortado por el borde, es el gráfico firma más fuerte que tiene una marca (`{"tipo": "simbolo", "x": 560, "y": 700, "w": 700, "giro": -10}`): exige que el logo tenga versión `simbolo` (`identidad/tools/simbolo_geometrico.py`).

## Qué hace que una composición no sea plantilla
- **Una idea de composición por pieza**, distinta de la del otro post: un elemento recortado por el borde, una forma grande de acento, una foto con un marco que no sea un rectángulo, una cifra gigante, un gráfico firma que se repite.
- **Un solo foco.** Tres jerarquías claras como máximo: lo que se ve primero, segundo y tercero.
- **El color manda en bloques, no en detalles sueltos:** un campo, una forma grande y un acento pequeño.
- **Ningún elemento «por si acaso».** Cada elemento responde a una regla del gusto o a un dato real.
- **Las dos piezas del kit no comparten esqueleto:** cambian el peso, el encuadre y los elementos.

## Elementos disponibles
`texto` · `palabra` (enorme, recortada) · `forma` (círculo, rect, semicírculo, pastilla, triángulo) · `firma` (horizonte, puntos, diagonal, ondas) · `foto` (marco sello, redondeado, recto, círculo) · `simbolo` (el del logo, grande, puede salirse del lienzo) · `insignia` (con el símbolo del logo) · `cifra` · `linea` · `estrellas` · `logo`.

## Límites
- La calidad depende de cómo se componga: el script no arregla una mala idea. El crítico y la puerta detectan solapes, contraste y huellas de plantilla, no «buen gusto».
- Una insignia sin símbolo en el logo va vacía: no se usa una inicial.
