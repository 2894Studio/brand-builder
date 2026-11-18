"""Comprueba que el brief estratégico (estrategia.md) es un brief y no un formulario rellenado, y que no trae recomendaciones visuales.

Uso:  python3 verificar_brief.py trabajo/<fecha>-marca-<slug>/estrategia.md
Comprueba: todas las secciones (Situación, Público y tensión, Mapa de la categoría, Por qué te elegiría y qué le frena (cuatro fuerzas), Cómo habla tu cliente (frases literales), Objeciones y a quién no, Pilares de mensaje (de 3 a 5), Posicionamiento, Promesa y prueba, Personalidad,
No es, Las tres vías, Vía elegida, Idea rectora, Lo que aún no sabes, Palabras clave para buscar referencias, Riesgos y pendientes) con contenido real; la tensión con dos mitades;
al menos 3 alternativas; la fórmula del posicionamiento completa; al menos 3 «no es»; EXACTAMENTE tres vías con sus campos; una idea rectora
de máximo 25 palabras; al menos 3 cosas por descubrir; 3 palabras clave para buscar referencias; 3 cosas que buscar y 3 que evitar en las referencias, con «porque» y sin colores concretos; sin recomendaciones visuales (colores, hex, logo, tipografía, paleta, prompts) en las
vías, la idea rectora, el posicionamiento y la personalidad; sin marcadores sin rellenar ni léxico prohibido. No juzga el acierto: sí impide
entregar un brief vacío o que se salte la fase. Sale con 1 si algo falla.
Comprueba que el brief estratégico (estrategia.md) es un brief y no un formulario rellenado.

Uso:  python3 verificar_brief.py trabajo/<fecha>-marca-<slug>/estrategia.md
Comprueba: todas las secciones (Situación, Público y tensión, Mapa de la categoría, Posicionamiento, Promesa y prueba,
Personalidad, No es, Idea rectora, Riesgos y pendientes, Cómo sabremos que acierta) con contenido real; la tensión con dos
mitades; al menos 3 competidores o alternativas; la fórmula del posicionamiento completa; al menos 3 «no es»; una idea rectora
de máximo 25 palabras; sin marcadores sin rellenar ni léxico prohibido. No juzga el acierto: sí impide entregar un brief vacío.
Sale con 1 si algo falla.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: salida en tubería → cp1252
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import re
import sys

SECCIONES = [
    ("situaci", "Situación", 60),
    ("público y tensión", "Público y tensión", 80),
    ("mapa de la categor", "Mapa de la categoría", 80),
    ("por qué te elegir", "Por qué te elegiría y qué le frena", 150),
    ("cómo habla tu cliente", "Cómo habla tu cliente", 80),
    ("objeciones", "Objeciones y a quién no", 100),
    ("posicionamiento", "Posicionamiento", 60),
    ("promesa", "Promesa y prueba", 40),
    ("personalidad", "Personalidad", 60),
    ("no es", "No es", 40),
    ("las tres v", "Las tres vías", 300),
    ("vía elegida", "Vía elegida", 10),
    ("pilares", "Pilares de mensaje", 120),
    ("idea rectora", "Idea rectora", 10),
    ("lo que aún no sabes", "Lo que aún no sabes", 60),
    ("palabras clave", "Palabras clave para buscar referencias", 30),
    ("qué buscar", "Qué buscar y qué evitar en las referencias", 150),
    ("riesgos", "Riesgos y pendientes", 20),
]
VISUAL = [r"#[0-9a-f]{3,8}\b", r"\blogo", r"\blogotipo", r"\bisotipo", r"\bs[ií]mbolo", r"\bicono", r"\btipograf", r"\bpaleta", r"\bmockup", r"\bprompt", r"\bserif", r"\bsans\b", r"\bdegradado", r"\bfotograf", r"\bilustraci",
          r"\b(azul|rojo|verde|amarillo|naranja|morado|violeta|rosa|dorado|negro|blanco|gris|turquesa|beige|marr[oó]n)\b"]
LEXICO = ["sinergia", "ecosistema", "tapiz", "universo", "viaje", "propuesta de valor", "solución integral", "apuesta",
          "elevar", "potenciar", "revolucionar", "transformar", "empoderar", "impulsar",
          "innovador", "innovadora", "disruptivo", "disruptiva", "único", "excepcional", "premium", "a medida", "de vanguardia",
          "no es solo", "en un mundo donde", "se encuentra con"]
MARCADORES = [r"\[…\]", r"\[\.\.\.\]", r"\bTODO\b", r"\blorem\b", r"<[^>\n]{2,40}>", r"\bpor definir\b", r"\bpendiente de rellenar\b"]


def secciones(texto):
    partes, actual = {}, None
    for linea in texto.splitlines():
        m = re.match(r"^##\s+(.*)$", linea)
        if m:
            actual = m.group(1).strip().lower()
            partes[actual] = []
        elif actual is not None:
            partes[actual].append(linea)
    return {k: "\n".join(v).strip() for k, v in partes.items()}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    texto = open(sys.argv[1], encoding="utf-8").read()
    sec = secciones(texto)
    errores, avisos = [], []

    def ok(c, msg, aviso=False):
        print(("  ok     " if c else ("  aviso  " if aviso else "  FALLO  ")) + msg)
        if not c:
            (avisos if aviso else errores).append(msg)

    cuerpo = {}
    for clave, nombre, minimo in SECCIONES:
        k = next((t for t in sec if t.startswith(clave)), None)
        cuerpo[nombre] = sec.get(k, "") if k else ""
        ok(k is not None and len(cuerpo[nombre]) >= minimo, f"sección «{nombre}» con contenido (mínimo {minimo} caracteres)" + ("" if k else " — falta el título"))
    pub = cuerpo["Público y tensión"]
    ok(bool(re.search(r"tensi[oó]n", pub, re.I)) and bool(re.search(r"\b(pero|aunque|sin embargo|mientras|en cambio|frente a)\b", pub, re.I)),
       "la tensión tiene dos mitades («quiere… pero…»)")
    mapa = cuerpo["Mapa de la categoría"]
    filas = [l for l in mapa.splitlines() if l.strip().startswith("|") and not re.match(r"^\s*\|[\s:|-]+\|\s*$", l) and not re.match(r"^\s*\|\s*(alternativa|competidor)", l, re.I)]
    items = [l for l in mapa.splitlines() if re.match(r"^\s*[-*]\s+\S", l)]
    ok(len(filas) >= 3 or len(items) >= 3, f"el mapa nombra al menos 3 competidores o alternativas ({max(len(filas), len(items))})")
    ok(bool(re.search(r"todas dicen", mapa, re.I)) and bool(re.search(r"haremos distinto", mapa, re.I)), "el mapa dice lo que todas dicen o hacen y lo único que se hará distinto")
    pos = cuerpo["Posicionamiento"].replace("*", "")
    ok(bool(re.search(r"^\s*para\b.+\bque\b.+\bes\b.+\bque\b.+\bporque\b", pos, re.I | re.S)), "el posicionamiento sigue la fórmula (Para… que…, X es… que…, porque…)")
    nes = [l for l in cuerpo["No es"].splitlines() if re.match(r"^\s*([-*]|\d+[.)])\s+\S", l)]
    ok(len(nes) >= 3, f"«No es» tiene al menos 3 puntos ({len(nes)})")
    idea = re.sub(r"[*_>«»\"“”]", "", cuerpo["Idea rectora"]).strip()
    ok(1 <= len(idea.split()) <= 25 and len([x for x in re.split(r"(?<=[.!?])\s+", idea) if x.strip()]) <= 2, f"la idea rectora es una frase de máximo 25 palabras ({len(idea.split())})")
    vias = re.split(r"(?m)^###\s+", cuerpo["Las tres vías"])[1:]
    ok(len(vias) == 3, f"hay exactamente tres vías ({len(vias)})")
    for i, v in enumerate(vias[:3], 1):
        faltan = [c for c in ("idea", "cómo suena", "riesgo", "encaja si") if c not in v.lower()]
        ok(len(v) >= 150 and not faltan, f"la vía {i} está completa" + (f" (faltan: {', '.join(faltan)})" if faltan else ("" if len(v) >= 150 else " (muy corta)")))
    ok(bool(re.search(r"\brecomendad[ao]\b|\brecomiendo\b", cuerpo["Las tres vías"], re.I)), "se recomienda una de las tres vías")
    fz = cuerpo["Por qué te elegiría y qué le frena"].lower()
    ok(all(k in fz for k in ("empuja", "atrae", "frena", "miedo")), "las cuatro fuerzas están (lo que empuja, atrae, frena y da miedo)")
    hb = cuerpo["Cómo habla tu cliente"]
    ok(len(re.findall(r"«[^»\n]{6,}»", hb)) >= 2 and "evitar" in hb.lower(), "hay al menos 2 frases literales del cliente y palabras que evitar")
    ob = cuerpo["Objeciones y a quién no"]
    ok(len([l for l in ob.splitlines() if re.match(r"^\s*([-*]|\d+[.)])\s+\S", l)]) >= 2 and "a quién no" in ob.lower(), "hay al menos 2 objeciones y a quién no sirve")
    pil = [l for l in cuerpo["Pilares de mensaje"].splitlines() if re.match(r"^\s*([-*]|\d+[.)])\s+\S", l)]
    ok(3 <= len(pil) <= 5, f"hay de 3 a 5 pilares de mensaje ({len(pil)})")
    claves = re.findall(r"`([^`\n]{4,60})`", cuerpo["Palabras clave para buscar referencias"])
    ok(len(claves) >= 3 and not any(c.strip() in ("…", "...") for c in claves), f"hay 3 palabras clave para buscar referencias ({len(claves)})")
    bq = cuerpo["Qué buscar y qué evitar en las referencias"]
    i_ev = bq.lower().find("evitar:")
    buscar, evitar = (bq[:i_ev], bq[i_ev:]) if i_ev >= 0 else (bq, "")
    pts = lambda t: [l for l in t.splitlines() if re.match(r"^\s*([-*]|\d+[.)])\s+\S", l)]  # noqa: E731
    ok(len(pts(buscar)) >= 3 and len(pts(evitar)) >= 3, f"hay 3 cosas que buscar y 3 que evitar ({len(pts(buscar))} y {len(pts(evitar))})")
    ok(all("porque" in l.lower() for l in pts(buscar) + pts(evitar)) and bool(pts(buscar)), "cada cosa que buscar o evitar lleva su «porque»")
    prohibido = sorted({m.group(0).lower() for pat in (VISUAL[0], VISUAL[-1]) for m in re.finditer(pat, bq, re.I)})
    ok(not prohibido, "lo visual de «qué buscar y evitar» va en general: sin colores concretos ni hex" + (f" ({', '.join(prohibido[:4])})" if prohibido else ""))
    pend = [l for l in cuerpo["Lo que aún no sabes"].splitlines() if re.match(r"^\s*([-*]|\d+[.)])\s+\S", l)]
    ok(len(pend) >= 3, f"hay al menos 3 cosas por descubrir, con cómo averiguarlas ({len(pend)})")
    for nombre in ("Las tres vías", "Idea rectora", "Posicionamiento", "Personalidad"):
        vis = sorted({m.group(0).lower() for pat in VISUAL for m in re.finditer(pat, cuerpo[nombre], re.I)})
        ok(not vis, f"sin recomendaciones visuales en «{nombre}»" + (f" ({', '.join(vis[:4])}): esta fase no las hace" if vis else ""))
    sin = [m for m in MARCADORES if re.search(m, texto, 0 if m == r"\bTODO\b" else re.I)]
    ok(not sin, "sin marcadores sin rellenar" + (f" ({', '.join(sin[:3])})" if sin else ""))
    bajo = texto.lower()
    def patron(w):
        if " " in w:
            return re.escape(w)
        if w.endswith("o"):
            return re.escape(w[:-1]) + r"(?:o|a|os|as)"      # innovador no, pero único → única, únicos
        if w.endswith("r"):
            return re.escape(w) + r"(?:se|lo|la|los|las)?"
        return re.escape(w) + r"s?"
    hallados = sorted({w for w in LEXICO if re.search(r"(?<![a-záéíóúñ])" + patron(w) + r"(?![a-záéíóúñ])", bajo)})
    ok(len(hallados) < 2, "léxico prohibido: " + (", ".join(hallados) if hallados else "ninguno") + (" (reescribe con hechos)" if hallados else ""))
    print()
    print("BRIEF CORRECTO" if not errores else f"BRIEF INCOMPLETO: {len(errores)} fallo(s). Corrige antes de enseñarlo.")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
