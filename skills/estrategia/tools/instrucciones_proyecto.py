#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Convierte el brief estratégico verificado en INSTRUCCIONES DE PROYECTO listas para pegar (Claude Projects, ChatGPT Projects, cualquier IA).

Uso:  python3 instrucciones_proyecto.py trabajo/<fecha>-marca-<slug>/estrategia.md [--salida instrucciones-de-proyecto.md]

Se niega si el brief no pasa verificar_brief.py. No inventa nada: reordena y copia lo que ya está en el brief, con el rol de la IA al principio
(«Eres mi director de estrategia de marca para…») y unas reglas de trabajo al final. Sin recomendaciones visuales salvo «qué buscar y qué evitar».
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: salida en tubería → cp1252
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import argparse
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import verificar_brief as VB  # noqa: E402

REGLAS = """- Habla y escribe con la **voz de mi marca** (mi personalidad y «cómo suena»). Frases cortas y concretas; un hecho por frase.
- **Nunca uses** las palabras que evito ni el léxico de relleno («sinergia», «innovador», «potenciar», «no es solo X, es Y»). Si una frase vale para cualquier competidor cambiando el nombre, reescríbela.
- **No inventes** datos de mercado, cifras ni casos. Si no lo sabes, dilo. Lo que yo no he confirmado va marcado como *Supuesto*: trátalo como hipótesis y recuérdamelo.
- **No prometas** lo que mi marca no puede probar hoy (mira «Promesa y prueba» y «Lo que aún no sé»).
- Antes de proponerme algo, comprueba que encaja con mi **idea rectora**, con **lo que mi marca no es** y con **a quién no sirve**.
- Si te pido algo visual, parte de «Para buscar referencias» y **no inventes un estilo sin preguntarme**.
- Sé breve. Pregúntame lo que falte antes de suponerlo."""


def _sec(sec, *claves):
    for k, v in sec.items():
        if any(k.startswith(c) for c in claves):
            return v.strip()
    return ""


def _quita_negritas(t):
    return t.replace("**", "")


def construir(texto):
    sec = VB.secciones(texto)
    marca = (re.search(r"^#\s+Brief estratégico:\s*(.+)$", texto, re.M) or [None, "mi marca"])[1].strip()
    pos_raw = _sec(sec, "posicionamiento")
    pos = _quita_negritas(pos_raw)
    m = re.search(r"Para\s+\*\*(.+?)\*\*\s+que\s+\*\*(.+?)\*\*,\s+\*\*(.+?)\*\*\s+es\s+\*\*(.+?)\*\*\s+que\s+\*\*(.+?)\*\*,\s+porque\s+\*\*(.+?)\*\*", pos_raw, re.S)   # con negritas, como pide la plantilla
    if not m:
        m = re.search(r"Para\s+(.+?)\s+que\s+(.+?),\s+(.+?)\s+es\s+(.+?)\s+que\s+(.+?),\s+porque\s+(.+?)\.?\s*(?:\*Supuesto|$)", pos, re.S)
    if m:
        pub, nec, mc, cat, ben, porque = (g.strip() for g in m.groups())
        intro = f"Eres mi director de estrategia de marca para {marca}. {marca} es {cat} que {ben}. Mi público: {pub}, que {nec}. Esto es todo lo que necesitas saber para ayudarme a decidir, escribir y revisar con coherencia."
    else:
        intro = f"Eres mi director de estrategia de marca para {marca}. Esto es todo lo que necesitas saber para ayudarme a decidir, escribir y revisar con coherencia."
    mapa = _sec(sec, "mapa de la categor")
    diferente = "\n".join(l for l in mapa.splitlines() if re.search(r"todas dicen|haremos distinto", l, re.I))
    habla = _sec(sec, "cómo habla tu cliente")
    out = [f"# Instrucciones de proyecto: {marca}", "", intro, "",
           "## Quién soy y qué hago", _sec(sec, "situaci"), "",
           "## Mi audiencia", _sec(sec, "público y tensión"), "",
           "## Lo que le empuja, le atrae, le frena y le da miedo", _sec(sec, "por qué te elegir"), "",
           "## Cómo habla mi cliente", habla, "",
           "## Mis mayores dolores y objeciones", _sec(sec, "objeciones"), "",
           "## Mi posicionamiento", _sec(sec, "posicionamiento"), "", _sec(sec, "promesa"), ""]
    if diferente:
        out += [diferente, ""]
    out += ["## Mi vía e idea rectora", f"**Vía elegida:** {_sec(sec, 'vía elegida')}", "", f"**Idea rectora:** {_sec(sec, 'idea rectora')}", "",
            "## Mi personalidad y mi voz", _sec(sec, "personalidad"), "",
            "## Lo que mi marca NO es", _sec(sec, "no es"), "",
            "## Mis pilares de mensaje", _sec(sec, "pilares"), "",
            "## Lo que aún no sé", _sec(sec, "lo que aún no sabes"), "",
            "## Para buscar referencias", _sec(sec, "palabras clave"), "", _sec(sec, "qué buscar"), "",
            "## Riesgos y pendientes", _sec(sec, "riesgos"), "",
            "## Cómo quiero que trabajes", REGLAS, ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("brief")
    ap.add_argument("--salida")
    a = ap.parse_args()
    r = subprocess.run([sys.executable, os.path.join(AQUI, "verificar_brief.py"), a.brief], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("El brief no pasa el verificador; corrígelo antes de generar las instrucciones:")
        print("\n".join(l for l in r.stdout.splitlines() if l.strip().startswith("FALLO")))
        return 1
    salida = a.salida or os.path.join(os.path.dirname(os.path.abspath(a.brief)), "instrucciones-de-proyecto.md")
    texto = construir(open(a.brief, encoding="utf-8").read())
    open(salida, "w", encoding="utf-8").write(texto)
    print(f"INSTRUCCIONES DE PROYECTO: {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
