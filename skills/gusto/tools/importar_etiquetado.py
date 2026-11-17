#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Importa las referencias etiquetadas con el etiquetador (ZIP o carpeta) a referencias/ y gusto.json.

Uso:  python3 importar_etiquetado.py referencias-etiquetadas.zip [--gusto gusto.json] [--referencias referencias/]
      python3 importar_etiquetado.py carpeta_con_etiquetas_json/ ...
Hace tres cosas: (1) copia las imágenes a referencias/ (solo png, jpg, jpeg o webp, con nombre seguro), (2) las mide con analizar_referencias.py
(colores, aire, saturación…) y (3) vuelca en gusto.json lo que dijo la persona: tipo (sí, no, otra), su nota, las decisiones por dimensión, y marca
la referencia como confirmada. Valida al final y dice qué falta. No borra referencias que ya existan.
"""
import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gusto_lib as G  # noqa: E402

SEGURO = re.compile(r"^[a-z0-9_\-]{1,60}\.(png|jpg|jpeg|webp)$")


def importar(meta, imagen_de, gusto, carpeta_ref):
    """meta: {referencias:[{archivo, nombre, tipo, nota_usuario, decisiones}]}; imagen_de(r) -> bytes. Devuelve (mensaje, errores, avisos)."""
    os.makedirs(carpeta_ref, exist_ok=True)
    escritas = []
    for r in meta.get("referencias", []):
        nombre = os.path.basename(str(r.get("archivo", "")))
        if not SEGURO.match(nombre):
            print(f"  aviso «{nombre}»: nombre o formato no admitido (solo png, jpg, jpeg, webp en minúsculas); se omite")
            continue
        datos = imagen_de(r)
        if not datos:
            print(f"  aviso «{nombre}»: sin imagen; se omite")
            continue
        with open(os.path.join(carpeta_ref, nombre), "wb") as fh:
            fh.write(datos)
        escritas.append(nombre)
    if not os.path.exists(gusto):
        G.guardar(G.nuevo(), gusto)
    subprocess.run([sys.executable, os.path.join(AQUI, "analizar_referencias.py"), carpeta_ref, "--gusto", gusto], capture_output=True, text=True)
    g = G.cargar(gusto)
    por_archivo = {x.get("archivo"): x for x in g.get("referencias", [])}
    for r in meta.get("referencias", []):
        nombre = os.path.basename(str(r.get("archivo", "")))
        if nombre not in escritas:
            continue
        x = por_archivo.get(nombre)
        if x is None:
            x = {"nombre": r.get("nombre") or os.path.splitext(nombre)[0], "archivo": nombre}
            g.setdefault("referencias", []).append(x)
        x["tipo"] = r.get("tipo") if r.get("tipo") in ("si", "no", "otra") else "si"
        x["nota_usuario"] = (r.get("nota_usuario") or "").strip()
        x["decisiones"] = [d for d in r.get("decisiones", []) if (d.get("regla") or "").strip()]
        x["confirmado"] = bool(x["nota_usuario"])
    G.guardar(g, gusto)
    err, av = G.validar(g)
    return f"{len(escritas)} referencia(s) en {carpeta_ref} y {gusto}", err, av


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("origen")
    ap.add_argument("--gusto", default="gusto.json")
    ap.add_argument("--referencias", default="referencias")
    a = ap.parse_args()
    if a.origen.lower().endswith(".zip"):
        z = zipfile.ZipFile(a.origen)
        meta = json.loads(z.read("etiquetas.json").decode("utf-8"))
        def imagen_de(r):
            try:
                return z.read("referencias/" + os.path.basename(r["archivo"]))
            except KeyError:
                return None
    else:
        meta = json.load(open(os.path.join(a.origen, "etiquetas.json"), encoding="utf-8"))
        def imagen_de(r):
            p = os.path.join(a.origen, "referencias", os.path.basename(r["archivo"]))
            return open(p, "rb").read() if os.path.exists(p) else None
    msg, err, av = importar(meta, imagen_de, a.gusto, a.referencias)
    print("ok", msg)
    for e in err:
        print("  ERROR ", e)
    for x in av:
        print("  aviso ", x)
    print("Siguiente: python3 skills/gusto/tools/gusto.py reglas   (lista R1…Rn) y seguir con la skill gusto (tonos, aplicar, contrastar).")
    return 1 if err else 0


def desde_dataurl(r):
    d = r.get("_datos", "")
    return base64.b64decode(d.split(",", 1)[1]) if "," in d else None


if __name__ == "__main__":
    sys.exit(main())
