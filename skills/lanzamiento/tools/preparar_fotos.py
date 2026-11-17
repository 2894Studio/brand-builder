#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Prepara las fotos de una marca para el bento y los posts: las revisa, recorta a los formatos que se usan y controla su origen.

Uso:  python3 preparar_fotos.py fotos/ --salida lanzamiento/fotos [--min 1080] [--crear-creditos]

Convención de nombres (para que el bento y los posts las encuentren solos):
  equipo*.jpg   varias personas      retrato*.jpg   una persona      producto*.jpg   el producto      local*.jpg   el sitio
Cada foto necesita una fila en fotos/creditos.md (tabla Markdown):
  | archivo | origen | autor o fuente | licencia | permiso de las personas |
  origen = propia, banco o ia. «banco» exige autor y licencia; «propia» con personas exige permiso = sí.
Con --crear-creditos escribe esa tabla con las fotos que encuentre y sale sin más.

Salida: recortes 3:4, 4:3 y 1:1 en JPEG y un manifiesto.json con el origen de cada foto. Las de origen «ia» quedan marcadas
en el manifiesto; que la pieza lo diga o no lo decide la persona (opción --declarar-ia del bento y de los posts). Necesita Pillow (pip install pillow).
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover
    Image = None

EXT = (".jpg", ".jpeg", ".png", ".webp")
FORMATOS = {"3x4": (3, 4), "4x3": (4, 3), "1x1": (1, 1)}
ORIGENES = ("propia", "banco", "ia")
CON_PERSONAS = ("equipo", "retrato", "persona")


def leer_creditos(ruta):
    filas = {}
    if not os.path.exists(ruta):
        return filas
    for linea in open(ruta, encoding="utf-8"):
        l = linea.strip()
        if not l.startswith("|") or set(l.replace("|", "").strip()) <= set("-: "):
            continue
        c = [x.strip() for x in l.strip("|").split("|")]
        if len(c) < 5 or c[0].lower() in ("archivo", ""):
            continue
        filas[c[0]] = {"origen": c[1].lower(), "autor": c[2], "licencia": c[3], "permiso": c[4].lower()}
    return filas


def recortar(im, rw, rh, foco_y=0.35):
    w, h = im.size
    objetivo = rw / rh
    if w / h > objetivo:
        nw, nh = round(h * objetivo), h
    else:
        nw, nh = w, round(w / objetivo)
    x = (w - nw) // 2
    y = round((h - nh) * foco_y)
    return im.crop((x, y, x + nw, y + nh))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("carpeta")
    ap.add_argument("--salida", default="lanzamiento/fotos")
    ap.add_argument("--min", type=int, default=1080, help="lado corto mínimo en píxeles")
    ap.add_argument("--crear-creditos", action="store_true")
    a = ap.parse_args()
    if Image is None:
        print("Falta Pillow. Instálalo con:  pip install pillow\nNo se ha cambiado nada.")
        return 2
    if not os.path.isdir(a.carpeta):
        print(f"No existe la carpeta {a.carpeta}")
        return 2
    archivos = sorted(f for f in os.listdir(a.carpeta) if f.lower().endswith(EXT))
    if not archivos:
        print(f"No hay fotos en {a.carpeta} (formatos: jpg, png, webp).")
        return 2
    ruta_cred = os.path.join(a.carpeta, "creditos.md")
    if a.crear_creditos:
        if os.path.exists(ruta_cred):
            print(f"{ruta_cred} ya existe; no lo sobrescribo.")
            return 1
        with open(ruta_cred, "w", encoding="utf-8") as fh:
            fh.write("# Créditos de las fotos\n\nUna fila por foto. origen = propia, banco o ia.\n\n"
                     "| archivo | origen | autor o fuente | licencia | permiso de las personas |\n|---|---|---|---|---|\n")
            for f in archivos:
                fh.write(f"| {f} |  |  |  |  |\n")
        print(f"creado {ruta_cred}: rellena una fila por foto y vuelve a ejecutar.")
        return 0
    cred = leer_creditos(ruta_cred)
    os.makedirs(a.salida, exist_ok=True)
    manifiesto, errores, avisos = [], [], []
    for f in archivos:
        stem = os.path.splitext(f)[0]
        im = ImageOps.exif_transpose(Image.open(os.path.join(a.carpeta, f))).convert("RGB")
        w, h = im.size
        c = cred.get(f)
        reg = {"archivo": f, "ancho": w, "alto": h, "origen": None, "recortes": {}, "pie": None, "avisos": []}
        if min(w, h) < a.min:
            reg["avisos"].append(f"baja resolución ({w}×{h}; el lado corto debe ser ≥ {a.min}px): se verá borrosa")
        if c is None or c["origen"] not in ORIGENES:
            errores.append(f"{f}: falta su fila en creditos.md o el origen no es propia, banco ni ia")
        else:
            reg["origen"] = c["origen"]
            if c["origen"] == "banco" and (not c["autor"] or not c["licencia"]):
                errores.append(f"{f}: origen «banco» sin autor o sin licencia")
            if c["origen"] == "propia" and stem.lower().startswith(CON_PERSONAS) and c["permiso"] not in ("sí", "si"):
                errores.append(f"{f}: foto propia con personas sin «sí» en el permiso de las personas")
            if c["origen"] == "ia":
                reg["pie"] = "Imagen generada con IA"
                if stem.lower().startswith(CON_PERSONAS):
                    reg["avisos"].append("persona sintética: ojo si se presenta como el equipo real de una empresa")
        for nombre, (rw, rh) in FORMATOS.items():
            rec = recortar(im, rw, rh)
            if max(rec.size) > 2400:
                rec.thumbnail((2400, 2400))
            dest = f"{stem}-{nombre}.jpg"
            rec.save(os.path.join(a.salida, dest), quality=88)
            reg["recortes"][nombre] = dest
        manifiesto.append(reg)
        for x in reg["avisos"]:
            avisos.append(f"{f}: {x}")
    json.dump(manifiesto, open(os.path.join(a.salida, "manifiesto.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for r in manifiesto:
        print(f"  {r['archivo']}: {r['ancho']}×{r['alto']} · origen {r['origen'] or '¿?'}" + (f" · {r['pie']}" if r["pie"] else ""))
    for x in errores:
        print("  ERROR ", x)
    for x in avisos:
        print("  aviso ", x)
    print(f"{len(manifiesto)} foto(s) → {a.salida}  ({len(errores)} error(es), {len(avisos)} aviso(s))")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
