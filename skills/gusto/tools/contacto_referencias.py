#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Hoja de contraste: las referencias a la izquierda, las piezas producidas a la derecha y las reglas R1…Rn debajo, para MIRARLAS JUNTAS.
Escribe también revision-gusto.md con una línea por regla para rellenar (cumple / parcial / no cumple / no aplica).

Uso:  python3 contacto_referencias.py --gusto gusto.json --referencias referencias/ --piezas lanzamiento/ --salida lanzamiento/
      python3 contacto_referencias.py --gusto gusto.json --referencias referencias/ --para post --salida lanzamiento/     (ANTES de diseñar: solo las referencias y reglas para ese destino)
Genera  <salida>/contacto-gusto.png  y  <salida>/revision-gusto.md  (no lo sobrescribe si ya existe).
Sale con 1 si gusto.json no tiene decisiones (sin ellas no hay nada que comprobar).
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
import sys
import textwrap

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gusto_lib as G  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gusto", default="gusto.json")
    ap.add_argument("--referencias", default="referencias")
    ap.add_argument("--piezas", default="")
    ap.add_argument("--para", choices=["logo", "post", "bento", "web"], help="solo las referencias y reglas que aplican a ese destino (sin piezas): para MIRAR antes de diseñar")
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()
    g = G.cargar(a.gusto)
    reglas = G.reglas_numeradas(g)
    if not reglas:
        print("gusto.json no tiene decisiones: añade con gusto.py decision (ver gusto/references/entrenar.md)")
        return 1
    os.makedirs(a.salida, exist_ok=True)
    md = os.path.join(a.salida, "revision-gusto.md")
    if a.para:
        reglas = [r for r in reglas if a.para in (r["aplica_en"] or [])]
        if not reglas:
            print(f"Ninguna regla de gusto.json aplica a «{a.para}»: añade decisiones con aplica_en {a.para}")
            return 1
    if not a.para and not os.path.exists(md):
        with open(md, "w", encoding="utf-8") as fh:
            fh.write("# Revisión contra las referencias\n\nMira `contacto-gusto.png` (referencias a la izquierda, piezas a la derecha). Por cada regla escribe `cumple`, `parcial`, `no cumple` o `no aplica` y **dónde se ve** (pieza y elemento). Una regla `no cumple` se corrige y se marca `corregido`.\n\n")
            for r in reglas:
                fh.write(f"- {r['id']} [{r['dimension']}] {'EVITAR: ' if r['prohibe'] else ''}{r['regla']} → (pendiente)\n")
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Falta Pillow: se escribió revision-gusto.md pero no la hoja de contraste (pip install pillow)")
        return 0
    refs = []
    origenes = {r["origen"] for r in reglas}
    for r in g.get("referencias", []):
        if r.get("tipo") == "si" and r.get("archivo") and (not a.para or r.get("nombre") in origenes):
            refs.append(os.path.join(a.referencias, r["archivo"]))
    refs = [x for x in refs if os.path.exists(x)][: (6 if a.para else 4)]
    piezas = [] if a.para or not a.piezas else sorted(glob.glob(os.path.join(a.piezas, "bento.png")) + glob.glob(os.path.join(a.piezas, "post-*.png")))[:3]
    def mini(ruta, alto):
        im = Image.open(ruta).convert("RGB")
        w = int(im.width * alto / im.height)
        return im.resize((w, alto))
    ALT = 520
    col_r = [mini(x, ALT) for x in refs]
    col_p = [mini(x, ALT) for x in piezas]
    ancho = max(sum(i.width for i in col_r) + 20 * max(0, len(col_r) - 1), 200) + 60 + max(sum(i.width for i in col_p) + 20 * max(0, len(col_p) - 1), 200)
    texto = [f"{r['id']} [{r['dimension']}] {'EVITAR: ' if r['prohibe'] else ''}{r['regla']}" for r in reglas]
    try:
        fuente = ImageFont.truetype("DejaVuSans.ttf", 22)
    except OSError:
        fuente = ImageFont.load_default()
    lineas = [l for t in texto for l in textwrap.wrap(t, 120)]
    alto = 80 + ALT + 40 + 30 * len(lineas) + 30
    lienzo = Image.new("RGB", (ancho + 80, alto), "#F2F3F5")
    d = ImageDraw.Draw(lienzo)
    d.text((40, 24), "REFERENCIAS" + (f" para {a.para.upper()}" if a.para else ""), fill="#12141A", font=fuente)
    x = 40
    for im in col_r:
        lienzo.paste(im, (x, 70)); x += im.width + 20
    x = 40 + sum(i.width for i in col_r) + 20 * max(0, len(col_r) - 1) + 60
    d.text((x, 24), "PIEZAS", fill="#12141A", font=fuente)
    for im in col_p:
        lienzo.paste(im, (x, 70)); x += im.width + 20
    y = 70 + ALT + 30
    for l in lineas:
        d.text((40, y), l, fill="#12141A", font=fuente); y += 30
    destino = os.path.join(a.salida, f"contacto-{a.para}.png" if a.para else "contacto-gusto.png")
    lienzo.save(destino)
    print(f"ok {destino}" + ("" if a.para else f"\nok {md}"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
