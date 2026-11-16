#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Gestiona gusto.json: crear, validar, ver la proporción de tonos y registrar una elección A/B.

  python3 gusto.py init  [--gusto gusto.json] [--producto SaaS]
  python3 gusto.py ver   [--gusto gusto.json]
  python3 gusto.py validar [--gusto gusto.json]
  python3 gusto.py ab --a serio --b tecnologico --elige a --motivo "se entiende antes" [--gusto gusto.json]
"""
import argparse
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gusto_lib as G  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("accion", choices=["init", "ver", "validar", "ab"])
    ap.add_argument("--gusto", default="gusto.json")
    ap.add_argument("--producto", default="SaaS")
    ap.add_argument("--a"); ap.add_argument("--b")
    ap.add_argument("--elige", choices=["a", "b"])
    ap.add_argument("--motivo", default="")
    x = ap.parse_args()
    if x.accion == "init":
        if os.path.exists(x.gusto):
            print(f"{x.gusto} ya existe; no lo sobrescribo.")
            return 1
        G.guardar(G.nuevo(x.producto), x.gusto)
        print(f"creado {x.gusto}")
        return 0
    g = G.cargar(x.gusto)
    if x.accion == "ver":
        t = g["tonos"]
        print("Proporción de tonos:  " + "  ".join(f"{k} {v}" for k, v in t.items()))
        print(f"{len(g['referencias'])} referencia(s), {len(g['elecciones_ab'])} elección(es) A/B")
        return 0
    if x.accion == "validar":
        err, av = G.validar(g)
        for e in err:
            print("  ERROR ", e)
        for a_ in av:
            print("  aviso ", a_)
        print("válido: " + x.gusto if not err else "NO válido: " + x.gusto)
        return 1 if err else 0
    # ab
    if not (x.a and x.b and x.elige):
        print("Faltan --a, --b y --elige")
        return 2
    for v in (x.a, x.b):
        if v not in G.TONOS:
            print(f"Tono «{v}» no válido (usa {', '.join(G.TONOS)})")
            return 2
    ganador = x.a if x.elige == "a" else x.b
    antes = dict(g["tonos"])
    if x.a != x.b:
        g["tonos"] = G.mover(g["tonos"], ganador, 10)
    g["elecciones_ab"].append({"fecha": datetime.date.today().isoformat(), "a": x.a, "b": x.b,
                               "elige": ganador, "motivo": x.motivo, "antes": antes, "despues": g["tonos"]})
    G.guardar(g, x.gusto)
    print(f"elegiste «{ganador}»: {antes} → {g['tonos']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
