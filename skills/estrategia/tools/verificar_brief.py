#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Comprueba que el brief estratégico (estrategia.md) es un brief y no un formulario rellenado.

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
    ("posicionamiento", "Posicionamiento", 60),
    ("promesa", "Promesa y prueba", 40),
    ("personalidad", "Personalidad", 60),
    ("no es", "No es", 40),
    ("idea rectora", "Idea rectora", 10),
    ("riesgos", "Riesgos y pendientes", 20),
    ("cómo sabremos", "Cómo sabremos que acierta", 40),
]
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
    filas = [l for l in mapa.splitlines() if l.strip().startswith("|") and not re.match(r"^\s*\|[\s:|-]+\|\s*$", l) and "competidor" not in l.lower()]
    items = [l for l in mapa.splitlines() if re.match(r"^\s*[-*]\s+\S", l)]
    ok(len(filas) >= 3 or len(items) >= 3, f"el mapa nombra al menos 3 competidores o alternativas ({max(len(filas), len(items))})")
    ok(bool(re.search(r"rompemos", mapa, re.I)) and bool(re.search(r"respetamos", mapa, re.I)), "el mapa dice qué convención se respeta y cuál se rompe")
    pos = cuerpo["Posicionamiento"].replace("*", "")
    ok(bool(re.search(r"^\s*para\b.+\bque\b.+\bes\b.+\bque\b.+\bporque\b", pos, re.I | re.S)), "el posicionamiento sigue la fórmula (Para… que…, X es… que…, porque…)")
    nes = [l for l in cuerpo["No es"].splitlines() if re.match(r"^\s*([-*]|\d+[.)])\s+\S", l)]
    ok(len(nes) >= 3, f"«No es» tiene al menos 3 puntos ({len(nes)})")
    idea = re.sub(r"[*_>«»\"“”]", "", cuerpo["Idea rectora"]).strip()
    ok(1 <= len(idea.split()) <= 25 and len([x for x in re.split(r"(?<=[.!?])\s+", idea) if x.strip()]) <= 2, f"la idea rectora es una frase de máximo 25 palabras ({len(idea.split())})")
    crit = [l for l in cuerpo["Cómo sabremos que acierta"].splitlines() if re.match(r"^\s*([-*]|\d+[.)])\s+\S", l)]
    ok(len(crit) >= 3, f"hay al menos 3 criterios de acierto ({len(crit)})")
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
