# kit.json: el contenido del manual

`marca.json` guarda lo que **es** la marca; `kit.json` guarda lo que se **cuenta** en el manual. Va en `trabajo/<fecha>-marca-<slug>/kit.json`. Todo es opcional: lo que falte sale como «Pendiente de redactar» y `generar_kit.py` lo avisa.

```json
{
  "promesa": "Una frase, con un hecho, que no sirva para la competencia.",
  "valores": [
    { "nombre": "Puntualidad", "frase": "Qué implica en la práctica, con un dato." }
  ],
  "voz": {
    "rasgos": [
      { "rasgo": "Directo", "asi_si": "Frase real.", "asi_no": "Frase real de la competencia." }
    ]
  },
  "fotografia": { "si": "Qué se fotografía y cómo.", "no": "Lo que no." },
  "elementos": [ { "nombre": "Cuadrícula de taller", "uso": "Dónde y cómo se usa." } ],
  "usos": [ "Regla de aplicación sobre una superficie." ],
  "aplicacion_principal": { "titulo": "Caja de recogida", "lead": "Una línea.", "descripcion": "Hasta 6 líneas." },
  "aplicacion_secundaria": { "titulo": "Ticket de servicio", "lead": "Una línea.", "descripcion": "Hasta 6 líneas." },
  "mockups": false
}
```

| Campo | Lámina | Límite |
|---|---|---|
| `promesa` | La marca (entradilla) | 2 líneas |
| `valores` | La marca | 3 o 4; frase de 2 líneas |
| `voz.rasgos` | Voz | 3 |
| `fotografia` | Fotografía | 3 líneas por pie |
| `elementos` | Elementos | 3 a 5 |
| `usos` | Usos sobre superficie | 5 reglas, 3 líneas cada una |
| `aplicacion_*` | Aplicaciones | cuerpo de 6 líneas |
| `mockups` | Añade la lámina de mockup | `true` o `false` |

El texto que no cabe se recorta con «…» y se avisa: lo largo va al documento de marca, no a la lámina. El ejemplo completo está en `evals/fixtures/pulso/kit.json`.
