#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Puerta de entrega del kit visual: no deja decir «terminado» si las piezas no están a nivel.

Uso:  python3 verificar_entrega.py trabajo/<fecha>-marca-<slug>/lanzamiento --marca marca.json [--kits trabajo]
Comprueba, en este orden:
  1. Existen logo/, bento y los dos posts (HTML y PNG) y el LEEME.md.
  2. Los PNG tienen el tamaño correcto (bento 1920×1080, posts 1080×1440).
  3. El crítico de render da 0 errores en cada pieza.
  4. Ninguna pieza deja marcadores («Foto real», «Nombre y apellido», lorem…).
  5. Si la marca es visual (fotografía, gastronomía, moda, viajes…), alguna pieza lleva una foto (o el brief declara «sin_fotos» con el motivo).
  6. Los dos posts no comparten composición (variedad.py < 0,6), ni se parecen a los de otros kits (--kits).
Sale con 1 si algo falla. Sin esta puerta en verde no se entrega ni se dice «revisado».
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CRITICO = os.path.join(RAIZ, "skills", "gusto", "tools", "critico_render.py")
VARIEDAD = os.path.join(RAIZ, "skills", "lanzamiento", "tools", "variedad.py")
MARCADORES = ("Foto real", "sustituir por una propia", "Nombre y apellido", "Rol · Ciudad", "lorem ipsum", "Lorem ipsum", "[hecho por confirmar", "pendiente de")
PIEZAS = [("bento", 1920, 1080), ("post-1-que-es", 1080, 1440), ("post-2-atributo", 1080, 1440)]
fallos, avisos = [], []


def ok(c, msg):
    print(("  ok     " if c else "  FALLO  ") + msg)
    if not c:
        fallos.append(msg)


def tam_png(ruta):
    with open(ruta, "rb") as f:
        h = f.read(24)
    if h[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(h[16:20], "big"), int.from_bytes(h[20:24], "big")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--marca")
    ap.add_argument("--kits", help="carpeta trabajo/ con kits anteriores para comparar la variedad")
    a = ap.parse_args()
    c = a.carpeta
    print("1. Archivos")
    ok(os.path.isdir(os.path.join(c, "logo")) and bool(glob.glob(os.path.join(c, "logo", "*"))), "hay logo/ con archivos")
    ok(os.path.exists(os.path.join(c, "LEEME.md")), "hay LEEME.md (qué es real, qué es de ejemplo, qué queda a mano)")
    for n, w, h in PIEZAS:
        ok(os.path.exists(os.path.join(c, n + ".html")), f"{n}.html")
        p = os.path.join(c, n + ".png")
        ok(os.path.exists(p), f"{n}.png")
        if os.path.exists(p):
            t = tam_png(p)
            ok(t == (w, h) or (t and t[0] % w == 0 and t[1] * w == t[0] * h), f"{n}.png mide {w}×{h} (o múltiplo exacto): {t}")
    print("2. Crítico de render")
    for n, w, h in PIEZAS:
        p = os.path.join(c, n + ".html")
        if not os.path.exists(p):
            continue
        cmd = [sys.executable, CRITICO, p, "--ancho", str(w), "--alto", str(h)] + (["--marca", a.marca] if a.marca else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 2:
            avisos.append("el crítico no se pudo ejecutar (falta Playwright): las piezas NO están revisadas")
            print("  SALTADO crítico: falta Playwright")
            break
        errs = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ERROR")]
        ok(r.returncode == 0, f"{n}: el crítico da 0 errores" + ("" if r.returncode == 0 else " → " + "; ".join(errs[:3])))
    print("3. Marcadores")
    for n, _, _ in PIEZAS:
        p = os.path.join(c, n + ".html")
        if os.path.exists(p):
            t = re.sub(r"data:[^\"')]+", "", open(p, encoding="utf-8").read())
            malos = [m for m in MARCADORES if m in t]
            ok(not malos, f"{n}: sin marcadores" + (f" ({', '.join(malos)})" if malos else ""))
    print("4. Fotografía")
    visual = False
    if a.marca and os.path.exists(a.marca):
        try:
            mj = json.load(open(a.marca, encoding="utf-8"))
            txt = " ".join(str(mj.get(k, "")) for k in ("categoria", "publico", "nombre")).lower()
            visual = bool(re.search(r"fotograf|ilustraci|moda\b|gastronom|restaurante|viaje|arquitect|interiorism|joyer|cosm[eé]t|floristeri|tatuaj", txt))
        except Exception:  # noqa: BLE001
            pass
    hay_foto = False
    for n, _, _ in PIEZAS:
        pth = os.path.join(c, n + ".html")
        if os.path.exists(pth) and re.search(r"data:image/(jpe?g|png|webp)", open(pth, encoding="utf-8").read()):
            hay_foto = True
    motivo = ""
    bp = os.path.join(c, "brief.json")
    if os.path.exists(bp):
        try:
            motivo = str(json.load(open(bp, encoding="utf-8")).get("sin_fotos", "")).strip()
        except Exception:  # noqa: BLE001
            pass
    if visual and not hay_foto:
        if motivo:
            avisos_foto = f"marca visual sin fotos por decisión explícita: {motivo}"
            print("  aviso  " + avisos_foto)
        else:
            ok(False, "la marca es visual (fotografía, gastronomía, moda…) y ninguna pieza lleva una foto: genera fotos (prompts_fotos.py, Canva, Gemini, Flow o fotos propias) o declara «sin_fotos» con el motivo en el brief")
    else:
        ok(True, "fotografía: " + ("hay fotos en las piezas" if hay_foto else "la marca no depende de la fotografía"))
    ui = [n for n, _, _ in PIEZAS if n != "bento" and os.path.exists(os.path.join(c, n + ".html")) and 'name="arquetipo" content="ui"' in open(os.path.join(c, n + ".html"), encoding="utf-8").read()]
    if ui and a.marca and os.path.exists(a.marca):
        try:
            mj = json.load(open(a.marca, encoding="utf-8"))
            txt = " ".join(str(mj.get(k, "")) for k in ("categoria", "publico")).lower()
            digital = bool(re.search(r"software|\bapp\b|aplicaci|plataforma|saas|\bweb\b|digital|programaci|c[oó]digo|desarrollo|tecnolog|ciberseg|fintech|datos", txt))
            ui_ok = False
            if os.path.exists(bp):
                ui_ok = bool(json.load(open(bp, encoding="utf-8")).get("ui_ok"))
            ok(digital or ui_ok, "la interfaz de móvil o de escritorio solo para productos digitales" + ("" if digital or ui_ok else f" ({', '.join(ui)}): elige otro recurso o añade «ui_ok» con motivo al brief"))
        except Exception:  # noqa: BLE001
            pass
    print("5. Variedad")
    p1, p2 = (os.path.join(c, f"{n}.html") for n in ("post-1-que-es", "post-2-atributo"))
    if os.path.exists(p1) and os.path.exists(p2):
        r = subprocess.run([sys.executable, VARIEDAD, p1, p2], capture_output=True, text=True)
        ok(r.returncode == 0, "los dos posts no comparten composición ni arquetipo" + ("" if r.returncode == 0 else ": " + r.stdout.strip().splitlines()[0]))
        if a.kits:
            otros = glob.glob(os.path.join(a.kits, "*", "lanzamiento", "post-*.html"))
            otros = [o for o in otros if os.path.abspath(os.path.dirname(o)) != os.path.abspath(c)]
            for p in (p1, p2):
                if otros:
                    r = subprocess.run([sys.executable, VARIEDAD, p] + otros, capture_output=True, text=True)
                    ok(r.returncode == 0, f"{os.path.basename(p)} no se parece a los posts de otros kits")
    print()
    for x in avisos:
        print("AVISO:", x)
    print("PUERTA DE ENTREGA: ABIERTA" if not fallos else f"PUERTA CERRADA: {len(fallos)} fallo(s). Corrige antes de entregar.")
    marca = os.path.join(c, ".puerta-ok")
    if not fallos and not avisos:
        open(marca, "w").write("puerta abierta\n")      # lo lee hooks/guardia_entrega.py
    elif os.path.exists(marca):
        os.remove(marca)
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
