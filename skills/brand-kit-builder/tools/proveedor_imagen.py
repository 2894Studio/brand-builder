#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Guarda y lee el proveedor de imagen de la persona (para no volver a preguntarlo).

  python3 proveedor_imagen.py guardar --carpeta trabajo/<fecha>-marca-<slug> --proveedor canva [--nota "plan gratuito"]
  python3 proveedor_imagen.py leer [--carpeta trabajo/<…>]        (sin --carpeta busca el más reciente en trabajo/*/)
Escribe/lee trabajo/<…>/proveedor-imagen.json. Proveedores: canva, flora, higgsfield, magnific, spaces, gemini, flow, otro, ninguno.
Sale con 0 y escribe el nombre si hay proveedor; con 1 si no se ha preguntado todavía (así las skills saben que toca preguntar).
"""
import argparse
import glob
import json
import os
import sys
import time

VALIDOS = ("canva", "flora", "higgsfield", "magnific", "spaces", "gemini", "flow", "otro", "ninguno")


def buscar(carpeta):
    if carpeta:
        p = os.path.join(carpeta, "proveedor-imagen.json")
        return p if os.path.exists(p) else None
    c = sorted(glob.glob(os.path.join("trabajo", "*", "proveedor-imagen.json")), key=os.path.getmtime)
    return c[-1] if c else None


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("guardar")
    g.add_argument("--carpeta", required=True)
    g.add_argument("--proveedor", required=True, choices=VALIDOS)
    g.add_argument("--nota", default="")
    r = sub.add_parser("leer")
    r.add_argument("--carpeta")
    a = ap.parse_args()
    if a.cmd == "guardar":
        os.makedirs(a.carpeta, exist_ok=True)
        ruta = os.path.join(a.carpeta, "proveedor-imagen.json")
        json.dump({"proveedor": a.proveedor, "nota": a.nota, "fecha": time.strftime("%Y-%m-%d")}, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"ok {ruta}: {a.proveedor}")
        return 0
    ruta = buscar(a.carpeta)
    if not ruta:
        print("sin proveedor: hay que preguntarlo")
        return 1
    d = json.load(open(ruta, encoding="utf-8"))
    print(d.get("proveedor", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
