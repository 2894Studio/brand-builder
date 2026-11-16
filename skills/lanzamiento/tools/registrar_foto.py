#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Añade (o reemplaza) la fila de una foto en fotos/creditos.md.

Uso:  python3 registrar_foto.py fotos/equipo-1.png --origen ia --fuente "Canva (generada)"
      python3 registrar_foto.py fotos/retrato-1.jpg --origen banco --fuente "Autor, https://…" --licencia "Pexels License"
      python3 registrar_foto.py fotos/equipo-2.jpg --origen propia --fuente "Estudio X" --permiso sí
origen: propia | banco | ia. banco exige --fuente y --licencia. propia con personas (equipo, retrato) exige --permiso sí.
"""
import argparse
import os
import sys

CON_PERSONAS = ("equipo", "retrato", "persona")


def limpio(s):
    return " ".join(str(s or "").replace("|", "/").split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("foto")
    ap.add_argument("--origen", required=True, choices=["propia", "banco", "ia"])
    ap.add_argument("--fuente", default="")
    ap.add_argument("--licencia", default="")
    ap.add_argument("--permiso", default="")
    a = ap.parse_args()
    if not os.path.exists(a.foto):
        sys.exit(f"no existe {a.foto}")
    archivo = os.path.basename(a.foto)
    if a.origen == "banco" and not (a.fuente and a.licencia):
        sys.exit("origen banco exige --fuente (autor y enlace) y --licencia")
    if a.origen == "propia" and archivo.startswith(CON_PERSONAS) and a.permiso.lower() != "sí":
        sys.exit("una foto propia con personas exige --permiso sí (permiso de las personas que salen)")
    if a.origen == "ia":
        fuente, lic, perm = a.fuente or "Generada con IA", "n/a", "n/a"
    elif a.origen == "banco":
        fuente, lic, perm = a.fuente, a.licencia, "n/a"
    else:
        fuente, lic, perm = a.fuente or "propia", a.licencia or "propia", a.permiso or "n/a"
    ruta = os.path.join(os.path.dirname(os.path.abspath(a.foto)), "creditos.md")
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write("# Créditos de las fotos\n\nUna fila por foto. origen = propia, banco o ia.\n\n"
                     "| archivo | origen | autor o fuente | licencia | permiso de las personas |\n|---|---|---|---|---|\n")
    lineas = open(ruta, encoding="utf-8").read().splitlines(keepends=True)
    lineas = [x for x in lineas if not x.lstrip("| ").startswith(archivo + " ")]
    if lineas and not lineas[-1].endswith("\n"):
        lineas[-1] += "\n"
    lineas.append(f"| {archivo} | {a.origen} | {limpio(fuente)} | {limpio(lic)} | {limpio(perm)} |\n")
    open(ruta, "w", encoding="utf-8").write("".join(lineas))
    print(f"ok {ruta}: {archivo} · {a.origen}")


if __name__ == "__main__":
    main()
