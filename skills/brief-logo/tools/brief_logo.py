#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Ensambla el brief de logo y los prompts para explorar logos con IA, a partir del brief estratégico.

Uso:  python3 brief_logo.py trabajo/<fecha>-marca-<slug>/brief-logo.json
      python3 brief_logo.py --ejemplo            (imprime un brief-logo.json de ejemplo)

El agente escribe brief-logo.json (tres direcciones distintas, clichés a evitar, restricciones, colores tentativos); este script lo
COMPRUEBA, le añade lo que ya está decidido en estrategia.md (idea rectora, posicionamiento, personalidad, «no es», público y tensión) y
en gusto.json (reglas de símbolo, nombre, tipografía, forma y color; lo que hay que evitar) y deja, junto al json:
  brief-logo.md      el brief de logo, para leer y aprobar
  prompts-logo.md    prompts listos para pegar: modelos de imagen (uno por dirección), Claude (diseño en SVG), refinamiento e iteración
Se niega si estrategia.md no pasa verificar_brief.py, si no hay exactamente 3 direcciones de tipo distinto o si los prompts son de relleno.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: salida en tubería → cp1252
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
VERIF_BRIEF = os.path.join(RAIZ, "skills", "estrategia", "tools", "verificar_brief.py")
TIPOS = ("wordmark", "simbolo+nombre", "emblema", "monograma", "abstracto", "pictorico")
LEXICO = ["sinergia", "ecosistema", "universo", "viaje", "propuesta de valor", "solución integral", "elevar", "potenciar", "revolucionar",
          "transformar", "empoderar", "innovador", "disruptivo", "premium", "de vanguardia", "moderno y limpio", "minimalista y elegante"]
EJEMPLO = {
    "estrategia": "estrategia.md",
    "gusto": "../../gusto.json",
    "nombre": "Cribo",
    "escritura_nombre": "minúsculas, peso bold, espaciado justo",
    "colores": {"tinta": "#0E1A2B", "acento": "#E8B04B", "fondo": "#F5F3EE"},
    "restricciones": ["El símbolo no puede ser una letra", "Sin personas ni manos"],
    "cliches": ["apretón de manos", "silueta de persona con lupa", "circuito o cerebro con nodos", "engranaje"],
    "cliches_en": ["handshake", "person silhouette with magnifying glass", "circuit board or brain with nodes", "gear"],
    "restricciones_en": ["the symbol must not be a letter", "no people and no hands"],
    "direcciones": [
        {"nombre": "La criba", "tipo": "simbolo+nombre",
         "idea": "Una criba: lo que pasa y lo que se queda fuera. Es la prueba técnica convertida en forma.",
         "por_que": "Expresa la idea rectora (la prueba antes del contrato) sin usar ningún símbolo de la categoría.",
         "descripcion_visual": "Un círculo sólido con una fila de pequeños huecos redondos alineados en diagonal, dos de ellos rellenos en el color de acento.",
         "prompt_en": "a solid circle with a diagonal row of small round cut-outs, two of them filled with an accent colour, geometric, flat, bold, symmetrical weight",
         "riesgo": "A tamaño pequeño los huecos pueden fundirse; hay que probar a 32 px."},
        {"nombre": "Solo el nombre", "tipo": "wordmark",
         "idea": "El nombre con una sola letra «perforada».",
         "por_que": "Para el cliente que huye de la imagen corporativa: serio y reconocible sin símbolo.",
         "descripcion_visual": "El nombre en minúsculas gruesas; la «o» tiene un hueco circular excéntrico.",
         "prompt_en": "wordmark of the name in heavy lowercase geometric sans-serif, with one letter 'o' having an off-centre circular hole",
         "riesgo": "Sin símbolo, el avatar depende de la inicial."},
        {"nombre": "Sello de prueba", "tipo": "emblema",
         "idea": "Un sello de revisado, como el que se pone a un examen corregido.",
         "por_que": "Convierte la corrección del ingeniero en un gesto reconocible.",
         "descripcion_visual": "Un círculo con borde dentado, el nombre dentro y una marca de verificación abstracta.",
         "prompt_en": "a circular rubber-stamp style emblem with a scalloped edge, name inside, a minimal abstract tick mark",
         "riesgo": "Los emblemas pierden legibilidad por debajo de 25 mm."},
    ],
}


def _cargar_sec(ruta):
    sys.path.insert(0, os.path.join(RAIZ, "skills", "estrategia", "tools"))
    import verificar_brief as VB
    texto = open(ruta, encoding="utf-8").read()
    return VB.secciones(texto)


def _sec(sec, *claves):
    for k, v in sec.items():
        if any(k.startswith(c) for c in claves):
            return v.strip()
    return ""


def _en_lista(txt):
    return [re.sub(r"^\s*([-*]|\d+[.)])\s+", "", l).strip() for l in txt.splitlines() if re.match(r"^\s*([-*]|\d+[.)])\s+\S", l)]


def comprobar(b, ruta_json):
    err = []
    base = os.path.dirname(os.path.abspath(ruta_json))
    for c in ("estrategia", "nombre"):
        if not b.get(c):
            err.append(f"falta «{c}»")
    est = os.path.join(base, b.get("estrategia", "estrategia.md"))
    if not os.path.exists(est):
        err.append(f"no existe {est}: primero la estrategia (skills/estrategia)")
    else:
        r = subprocess.run([sys.executable, VERIF_BRIEF, est], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            malos = [l.replace("FALLO", "").strip() for l in r.stdout.splitlines() if l.strip().startswith("FALLO")]
            err.append("estrategia.md no pasa verificar_brief.py (un brief de logo sobre un brief estratégico flojo sale genérico): " + "; ".join(malos)[:300])
    d = b.get("direcciones") or []
    if len(d) != 3:
        err.append(f"tiene que haber exactamente 3 direcciones (hay {len(d)}): la exploración compara; una sola no es explorar y cinco es ruido")
    tipos = [x.get("tipo") for x in d]
    if len(set(tipos)) < 2:
        err.append("las 3 direcciones deben diferenciarse en el TIPO de marca (wordmark, símbolo+nombre, emblema, monograma, abstracto, pictórico), no en el acabado: al menos 2 tipos distintos")
    for i, x in enumerate(d, 1):
        if x.get("tipo") not in TIPOS:
            err.append(f"dirección {i}: «tipo» debe ser uno de {', '.join(TIPOS)}")
        for campo, minimo in (("nombre", 3), ("idea", 30), ("por_que", 30), ("descripcion_visual", 40), ("prompt_en", 40), ("riesgo", 15)):
            if len(str(x.get(campo, "")).strip()) < minimo:
                err.append(f"dirección {i}: «{campo}» es de relleno o falta (mínimo {minimo} caracteres)")
        low = " ".join(str(x.get(c, "")) for c in ("idea", "por_que", "descripcion_visual")).lower()
        if any(w in low for w in LEXICO):
            err.append(f"dirección {i}: usa léxico de relleno ({', '.join(w for w in LEXICO if w in low)}): describe formas y hechos")
        if re.search(r"[áéíóúñ¿¡]", str(x.get("prompt_en", ""))):
            err.append(f"dirección {i}: «prompt_en» debe estar en inglés (los modelos de imagen responden mejor); el nombre de la marca puede ir tal cual")
    if len(b.get("cliches") or []) < 3:
        err.append("«cliches»: mínimo 3 símbolos típicos de la categoría que NO se usan (es lo que evita el logo genérico)")
    if len(b.get("cliches_en") or []) < 3:
        err.append("«cliches_en»: los mismos tópicos en inglés (para los prompts de los modelos de imagen)")
    if (b.get("restricciones") or []) and len(b.get("restricciones_en") or []) != len(b["restricciones"]):
        err.append("«restricciones_en»: cada restricción necesita su traducción al inglés, en el mismo orden")
    return err


def reglas_gusto(b, base):
    ruta = os.path.join(base, b["gusto"]) if b.get("gusto") else ""
    if not ruta or not os.path.exists(ruta):
        return [], []
    sys.path.insert(0, os.path.join(RAIZ, "skills", "gusto", "tools"))
    import gusto_lib as GL
    g = GL.cargar(ruta)
    rs = GL.reglas_numeradas(g)
    conf = {r.get("nombre"): bool(r.get("confirmado")) for r in g.get("referencias", [])}
    for r in rs:
        r["sin_confirmar"] = not conf.get(r["origen"], False)
    dim = ("nombre", "simbolo", "tipografia", "forma", "color")
    ok = [r for r in rs if not r["prohibe"] and r["dimension"] in dim]
    no = [r for r in rs if r["prohibe"] and (r["dimension"] in dim or "logo" in (r["aplica_en"] or []))]
    return ok, no


def estilo_comun(b):
    c = b.get("colores") or {}
    tinta = c.get("tinta")
    fondo = c.get("fondo", "#FFFFFF")
    if tinta:
        tinta_txt = f"a single ink colour {tinta}"
    else:
        tinta_txt = "a single dark ink colour"
    return f"flat vector logo, solid shapes, {tinta_txt}, on a plain flat {fondo} background, centred, generous margin, crisp edges, no gradients, no shadows, no 3D, no texture, no mockup"


def prompt_imagen(b, d):
    nombre = b["nombre"]
    cuerpo = d["prompt_en"].rstrip(". ")
    texto_nombre = (f"The only text is the name \"{nombre}\", spelled exactly like that." if d["tipo"] in ("wordmark", "simbolo+nombre", "emblema") else "No text at all.")
    neg = ", ".join(["gradients", "drop shadows", "3D", "photo", "mockup", "extra text", "tiny details"] + list(b.get("cliches_en") or [])[:6])
    reglas = ("; ".join(b.get("restricciones_en") or []))
    cuerpo = cuerpo[0].upper() + cuerpo[1:]
    natural = f"Logo design. {cuerpo}. {estilo_comun(b)}. {texto_nombre}" + (f" Requirements: {reglas}." if reglas else "") + f" Avoid: {neg}."
    mj = f"{cuerpo}, {estilo_comun(b)}, vector logo, graphic design --no {neg} --ar 1:1 --style raw"
    return natural, mj


def prompt_claude(b, brief_md):  # el brief completo (con las reglas de gusto y lo que se evita) va dentro
    nombre = b["nombre"]
    dirs = "\n".join(f"{i}. **{d['nombre']}** ({d['tipo']}): {d['idea']} Forma: {d['descripcion_visual']} Riesgo: {d['riesgo']}" for i, d in enumerate(b["direcciones"], 1))
    return f"""Eres un director de diseño de marca con oficio de identidad visual. Voy a darte un brief de logo. Quiero que **explores** opciones, no que me des una sola respuesta.

# Brief
{brief_md}

# Qué quiero
Diseña **tres logos** en SVG, uno por cada dirección de abajo, en un único archivo HTML que los muestre juntos (tablero) sobre fondo claro y, debajo de cada uno, sobre fondo oscuro, y en un recuadro de 32 px y de 25 mm. Las direcciones:

{dirs}

# Reglas de oficio (no negociables)
- Solo formas vectoriales y el nombre como texto. Sin fuentes externas: usa una fuente del sistema o dibuja la letra con formas, y dime cuál usarías de verdad.
- Una sola tinta{(" (" + b['colores']['tinta'] + ")") if (b.get('colores') or {}).get('tinta') else ''}; el acento solo si la dirección lo necesita y se ve igual en una tinta.
- Sin degradados, sombras ni efectos. Geometría construida (círculos, rectángulos, arcos), no dibujo a mano alzada.
- Evita estos tópicos de la categoría: {', '.join(b['cliches'])}.
- Cumple las restricciones: {'; '.join(b.get('restricciones') or ['ninguna adicional'])}.

# Cómo trabajas
1. Antes de dibujar, escribe en dos líneas por dirección **qué idea del brief expresa** y **cómo se resuelve a 32 px**.
2. Dibuja las tres.
3. **Critícalas tú** con dureza: para cada una, tres debilidades reales y aplica las cinco pruebas (competidor, tres segundos, reducción a 25 mm y una tinta, «no», defensor).
4. Arregla la mayor debilidad de cada una y muestra la versión corregida junto a la primera.
5. Termina recomendando una y diciendo por qué, y qué haría falta para convertirla en logo definitivo (revisar kerning, contornos, anterioridades).

Entrega el tablero completo como un solo archivo HTML. No me hagas preguntas antes de empezar: si falta algo, supónlo y dímelo al final."""


def prompt_refinar(b):
    return f"""Esta es la opción que me ha gustado (adjunta la imagen o pega el SVG). Hazle **un único cambio** y deja todo lo demás igual:

- Cambio que quiero: <describe UNA cosa: simplificar el símbolo / hacer el trazo más grueso / cambiar la proporción símbolo-nombre / probar sin el acento / otra forma para X>.
- Mantén: el concepto ({b['direcciones'][0]['nombre']} u otro: <el que elijas>), la tinta y el fondo.
- No añadas elementos nuevos ni efectos.
- Dame 3 variaciones del mismo cambio, de menos a más intenso, y dime cuál recomiendas y por qué.

Después de cada vuelta, comprueba a 32 px, en una tinta y en blanco sobre oscuro. Si el nombre sale mal escrito en una imagen, no regeneres: pasa a Claude y reconstruye el nombre como texto vectorial."""


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--ejemplo":
        print(json.dumps(EJEMPLO, ensure_ascii=False, indent=1))
        return 0
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ruta = os.path.abspath(sys.argv[1])
    base = os.path.dirname(ruta)
    b = json.load(open(ruta, encoding="utf-8"))
    err = comprobar(b, ruta)
    if err:
        print("BRIEF DE LOGO INCOMPLETO:")
        for e in err:
            print("  FALLO ", e)
        return 1
    sec = _cargar_sec(os.path.join(base, b["estrategia"]))
    ok, no = reglas_gusto(b, base)
    evitar = [r["regla"] for r in no]
    idea = _sec(sec, "idea rectora")
    pos = _sec(sec, "posicionamiento")
    pers = _sec(sec, "personalidad")
    nes = _en_lista(_sec(sec, "no es"))
    pub = _sec(sec, "público")
    col = b.get("colores") or {}
    md = [f"# Brief de logo: {b['nombre']}", "",
          "## Idea rectora", idea, "",
          "## Posicionamiento", pos, "",
          "## Público y tensión", pub, "",
          "## Personalidad", pers, "",
          "## Lo que el logo NO puede parecer"]
    md += [f"- {x}" for x in nes]
    md += [f"- Tópicos de la categoría que no se usan: {', '.join(b['cliches'])}"]
    md += ["", "## El nombre", f"«{b['nombre']}»" + (f", escrito en {b['escritura_nombre']}" if b.get("escritura_nombre") else ""), ""]
    md += ["## Restricciones"] + [f"- {x}" for x in (b.get("restricciones") or ["Ninguna adicional."])] + [""]
    md += ["## Dónde tiene que funcionar", "- A 25 mm de ancho y como avatar de 32 px.", "- En una sola tinta, y en blanco sobre fondo oscuro.", "- Como símbolo suelto (sin el nombre), si el tipo de marca lo permite.", ""]
    if col:
        md += ["## Colores tentativos", ", ".join(f"{k} {v}" for k, v in col.items()) + " (se confirman en identidad con el contraste comprobado).", ""]
    if ok or evitar:
        md += ["## Lo que enseñan tus referencias para el logo"]
        md += [f"- {r['id']} [{r['dimension']}] {r['regla']}" + (" (referencia sin confirmar por la persona)" if r.get("sin_confirmar") else "") for r in ok]
        md += [f"- EVITAR {r['id']}: {r['regla']}" + (" (referencia sin confirmar por la persona)" if r.get("sin_confirmar") else "") for r in no]
        md += [""]
    md += ["## Tres direcciones a explorar (de tipo distinto)"]
    for i, d in enumerate(b["direcciones"], 1):
        md += [f"### {i}. {d['nombre']} ({d['tipo']})", f"- **Idea:** {d['idea']}", f"- **Por qué:** {d['por_que']}", f"- **Forma:** {d['descripcion_visual']}", f"- **Riesgo:** {d['riesgo']}", ""]
    md += ["## Cómo se elige", "Las cinco pruebas: competidor, tres segundos, reducción a 25 mm y una tinta, «no», defensor (`criterio-experto.md`). Una dirección que falle la de reducción o la del «no» se descarta.", ""]
    brief_md = "\n".join(md)
    open(os.path.join(base, "brief-logo.md"), "w", encoding="utf-8").write(brief_md + "\n")

    p = ["# Prompts para explorar el logo", "",
         "Tres formas de usar el brief. Las imágenes generadas fallan con las letras y con los detalles pequeños: úsalas para **explorar ideas**, y reconstruye el logo elegido en vector (Claude, Figma o Illustrator).", "",
         "## A. Modelo de imagen (uno por dirección)",
         "Pega cada prompt en Ideogram, Recraft, Midjourney, GPT Image, Imagen o Flux. Genera 4 variaciones por dirección y quédate con las que se entienden a 32 px. La versión «natural» sirve para casi todos; la de «Midjourney» lleva sus parámetros.", ""]
    for i, d in enumerate(b["direcciones"], 1):
        nat, mj = prompt_imagen(b, d)
        p += [f"### {i}. {d['nombre']} ({d['tipo']})", "**Natural (Ideogram, Recraft, GPT Image, Imagen, Flux):**", "```", nat, "```", "**Midjourney:**", "```", mj, "```", ""]
    p += ["## B. Claude (diseño en SVG, tablero de las tres direcciones)",
          "Pega esto en Claude (o en Claude Design). Te devuelve un tablero HTML con los tres logos en SVG sobre claro, oscuro y a 32 px, con su autocrítica. Es lo mejor para el logotipo con texto, porque el nombre sale bien escrito.", "",
          "````", prompt_claude(b, brief_md), "````", "",
          "## C. Refinar la opción que te guste (una vuelta = un cambio)", "```", prompt_refinar(b), "```", "",
          "## Cómo decidir", "1. Mira las tres a 32 px y en una tinta antes que a tamaño grande.", "2. Descarta la que falle la prueba de reducción o la del «no».", "3. Pregúntate si podrías defender la elección delante de un cliente exigente en una línea que empiece por «porque».", "4. Antes de usarla de verdad: anterioridades del nombre y del símbolo (OEPM, EUIPO) y reconstrucción en vector. Eso no lo hace ninguna IA por ti.", ""]
    open(os.path.join(base, "prompts-logo.md"), "w", encoding="utf-8").write("\n".join(p))
    print(f"BRIEF DE LOGO CORRECTO\n  {os.path.join(base, 'brief-logo.md')}\n  {os.path.join(base, 'prompts-logo.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
