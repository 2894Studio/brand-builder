#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Avisa cuando una pieza se parece demasiado a otra (señal de plantilla).

Uso:  python3 variedad.py pieza.html otra1.html otra2.html ... [--umbral 0.6]
      python3 variedad.py pieza.html --carpeta trabajo     (compara con todo trabajo/*/lanzamiento/*.html)

Compara la estructura (clases CSS y etiquetas usadas, sin textos ni colores) con el índice de Jaccard y, además, el arquetipo
(<meta name="arquetipo">: ui, foto, datos, mapa, tipografico:cifra…): dos piezas del mismo arquetipo son la misma plantilla.
Sale con 1 si alguna pareja supera el umbral. Es una alarma, no un juez: si dos piezas comparten
generador y aun así son distintas a propósito, justifícalo en el LEEME.md.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import argparse
import glob
import os
import re
import sys


def firma(ruta):
    h = open(ruta, encoding="utf-8").read()
    h = re.sub(r"data:[^\"')]+", "", h)  # fuera imágenes incrustadas
    clases = set()
    for m in re.finditer(r'class="([^"]+)"', h):
        clases.update(m.group(1).split())
    etiquetas = set(re.findall(r"<([a-z][a-z0-9]*)", h))
    return {"c:" + x for x in clases} | {"t:" + x for x in etiquetas}


def arquetipo(ruta):
    m = re.search(r'<meta name="arquetipo" content="([^"]+)"', open(ruta, encoding="utf-8").read())
    return m.group(1) if m else ""


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pieza")
    ap.add_argument("otras", nargs="*")
    ap.add_argument("--carpeta")
    ap.add_argument("--umbral", type=float, default=0.6)
    a = ap.parse_args()
    otras = list(a.otras)
    if a.carpeta:
        otras += glob.glob(os.path.join(a.carpeta, "*", "lanzamiento", "*.html"))
    base = os.path.abspath(a.pieza)
    otras = [o for o in otras if os.path.abspath(o) != base and os.path.exists(o)]
    if not otras:
        print("sin piezas con las que comparar")
        return 0
    f0 = firma(a.pieza)
    mal = 0
    for o in otras:
        j = jaccard(f0, firma(o))
        fam0, fam1 = arquetipo(a.pieza), arquetipo(o)
        misma = bool(fam0) and fam0 == fam1          # mismo arquetipo de composición = misma plantilla, aunque cambien textos y colores
        ambas = bool(fam0) and bool(fam1)
        # con arquetipo declarado en las dos piezas manda el arquetipo (otro arquetipo = otra composición); sin él, el índice de clases
        parecida = misma or (j >= (0.9 if ambas else a.umbral))
        print(f"  {'PARECIDA' if parecida else 'ok':9} {j:.2f}  {os.path.relpath(o)}" + (f"  (mismo arquetipo: {fam0})" if misma else ""))
        mal += parecida
    if mal:
        print(f"{a.pieza}: se parece demasiado a {mal} pieza(s). Cambia la composición (otro recurso, otra jerarquía), no solo los textos y colores.")
    return 1 if mal else 0


if __name__ == "__main__":
    sys.exit(main())
