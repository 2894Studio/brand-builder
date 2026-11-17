#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Apoyo para la técnica «Logo to Brand Identity» de FLORA (opcional, de pago): prepara el logo de entrada y mide los tableros de salida.

  preparar  python3 flora_logo.py preparar marca.json --salida trabajo/<…>/flora
            Genera logo-entrada.png: el logo principal, centrado y sobre un fondo liso (la técnica lo pide «sobre fondo liso, PNG limpio»).
  guardar   python3 flora_logo.py guardar URL_O_RUTA [URL_O_RUTA …] --salida trabajo/<…>/flora
            Descarga (o copia) los tableros a tablero-1.png…, **mide** sus colores dominantes con gusto/tools/analizar_referencias.py
            y escribe direccion-flora.md con las medidas y las preguntas que hay que contestar antes de pasar nada a marca.json.
Las llamadas a FLORA (subir el logo con flora_create_asset, presupuesto, flora_run_technique) las hace el agente con el conector; este script
no gasta nada ni se conecta a FLORA con credenciales: solo descarga URLs públicas de media.flora.ai.
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
import shutil
import subprocess
import sys
import tempfile
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
EXPORTAR = os.path.join(RAIZ, "skills", "lanzamiento", "tools", "exportar_logos.py")
ANALIZAR = os.path.join(RAIZ, "skills", "gusto", "tools", "analizar_referencias.py")


def preparar(a):
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Falta Pillow (pip install pillow).")
    os.makedirs(a.salida, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, EXPORTAR, a.marca, "--salida", tmp, "--ancho", "1600"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        png = os.path.join(tmp, "principal.png")
        if not os.path.exists(png):
            cand = [f for f in os.listdir(tmp) if f.endswith(".png")]
            if not cand:
                sys.exit("No se pudo exportar el logo a PNG (hace falta rsvg-convert o Chromium con Playwright):\n" + (r.stdout + r.stderr)[-400:])
            png = os.path.join(tmp, cand[0])
        logo = Image.open(png).convert("RGBA")
        from PIL import ImageStat
        mascara = logo.getchannel("A").point(lambda v: 255 if v > 200 else 0)
        media = ImageStat.Stat(logo.convert("RGB"), mask=mascara).mean if mascara.getbbox() else [128, 128, 128]
        lum = (0.2126 * media[0] + 0.7152 * media[1] + 0.0722 * media[2]) / 255
        fondo = (255, 255, 255) if lum < 0.7 else (17, 17, 17)       # fondo liso que contraste con el logo
        w, h = 2000, 1200
        logo.thumbnail((int(w * .6), int(h * .6)))
        lienzo = Image.new("RGB", (w, h), fondo)
        lienzo.paste(logo, ((w - logo.width) // 2, (h - logo.height) // 2), logo)
        destino = os.path.join(a.salida, "logo-entrada.png")
        lienzo.save(destino)
    print(f"ok {destino}  ({w}×{h}, fondo liso {'blanco' if lum < 0.7 else 'oscuro'})")
    print("Siguiente: subirlo con flora_create_asset (source signed-url), pedir el coste con flora_get_technique y, con el sí de la persona, flora_run_technique.")


def distintos(dominantes, umbral=45):
    out = []
    for d in dominantes:
        h = d["hex"].lstrip("#")
        rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        if all(sum((x - y) ** 2 for x, y in zip(rgb, o[0])) ** .5 > umbral for o in out):
            out.append((rgb, d["hex"], d["pct"]))
    return [(hx, pct) for _, hx, pct in out]


def guardar(a):
    os.makedirs(a.salida, exist_ok=True)
    carpeta = os.path.join(a.salida, "tableros")
    os.makedirs(carpeta, exist_ok=True)
    for i, fuente in enumerate(a.fuentes, 1):
        destino = os.path.join(carpeta, f"tablero-{i}.png")
        if fuente.startswith("http"):
            req = urllib.request.Request(fuente, headers={"User-Agent": "brand-kit-builder/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r, open(destino, "wb") as fh:
                fh.write(r.read())
        else:
            shutil.copy(fuente, destino)
        print("ok", destino)
    medidas = os.path.join(a.salida, "medidas-flora.json")
    r = subprocess.run([sys.executable, ANALIZAR, carpeta, "--gusto", medidas, "--tipo", "otra"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not os.path.exists(medidas):
        sys.exit("No se pudieron medir los tableros (¿falta Pillow?):\n" + (r.stdout + r.stderr)[-300:])
    refs = {x["archivo"]: x["medido"] for x in json.load(open(medidas, encoding="utf-8"))["referencias"]}
    md = ["# Dirección de identidad con FLORA (Logo to Brand Identity)\n",
          "Los tableros son imágenes generadas por un modelo: **los textos, tipografías y códigos de color dibujados en ellos no son fiables**. "
          "Los colores de abajo están **medidos** sobre los píxeles; úsalos en lugar de lo que el tablero «diga».\n"]
    for i in range(1, len(a.fuentes) + 1):
        m = refs.get(f"tablero-{i}.png", {})
        pal = distintos(m.get("dominantes", []))
        md.append(f"## Tablero {i}\n")
        md.append(f"- Colores dominantes medidos: {', '.join(f'{h} ({p}%)' for h, p in pal) or '—'}")
        md.append(f"- Luminosidad {m.get('luminosidad')}, saturación {m.get('saturacion')}, temperatura {m.get('temperatura')}, aire {m.get('aire_pct')} %, detalle {m.get('detalle')}")
        md.append("- Qué propone (míralo tú): tipografía · estilo de imagen · aplicaciones · gráfico firma:\n- Qué NO se copia:\n")
    md.append("## Decisión (con la persona, con un diálogo)\n")
    md.append("1. ¿Qué tablero (o qué mezcla) se sigue? ¿Encaja con las referencias de `gusto.json` y con lo que la marca **nunca** debe parecer?")
    md.append("2. Del elegido se toma **solo**: la paleta medida (comprobada con `contraste.py`), el estilo de imagen y el gráfico firma. Se anota en `marca.json` → `visual.estilo` y en `kit.json` → `fotografia`.")
    md.append("3. Se descarta todo lo que contradiga la estrategia (público, tono, léxico prohibido). La técnica infiere la categoría **solo del logo**.")
    open(os.path.join(a.salida, "direccion-flora.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"ok {os.path.join(a.salida, 'direccion-flora.md')}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preparar")
    p.add_argument("marca")
    p.add_argument("--salida", required=True)
    g = sub.add_parser("guardar")
    g.add_argument("fuentes", nargs="+")
    g.add_argument("--salida", required=True)
    a = ap.parse_args()
    (preparar if a.cmd == "preparar" else guardar)(a)


if __name__ == "__main__":
    main()
