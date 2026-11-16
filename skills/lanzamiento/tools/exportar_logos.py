#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Exporta los logos SVG de marca.json a PNG con fondo transparente (por defecto 3000 px de ancho).

Uso:  python3 exportar_logos.py marca.json --salida lanzamiento/logo [--ancho 3000]
Usa rsvg-convert si está instalado; si no, Chromium con Playwright (el mismo que el crítico de gusto).
Sin ninguno de los dos sale con código 2 y no da nada por exportado: entrega los SVG, que son el original.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402

RUNNER = r"""
const {chromium}=require('playwright');(async()=>{const [url,w,h,out]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h}});
await p.goto(url);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:out,omitBackground:true});await b.close()})().catch(e=>{console.error(e.message);process.exit(3)})
"""


def proporcion(svg):
    t = open(svg, encoding="utf-8").read()
    mv = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)', t)
    return (float(mv.group(1)), float(mv.group(2))) if mv else (4.0, 1.0)


def con_chromium(svg, png, ancho):
    node = shutil.which("node")
    if not node:
        return False
    w, h = proporcion(svg)
    alto = max(1, round(ancho * h / w))
    d = tempfile.mkdtemp()
    html = os.path.join(d, "l.html")
    open(html, "w", encoding="utf-8").write(f'<body style="margin:0;background:transparent"><img src="file://{os.path.abspath(svg)}" style="width:{ancho}px;height:{alto}px;display:block"></body>')
    run = os.path.join(d, "r.js")
    open(run, "w").write(RUNNER)
    env = dict(os.environ)
    try:
        raiz = subprocess.run([shutil.which("npm") or "npm", "root", "-g"], capture_output=True, text=True, timeout=20).stdout.strip()
        env["NODE_PATH"] = os.pathsep.join(filter(None, [env.get("NODE_PATH", ""), raiz, os.path.join(os.getcwd(), "node_modules")]))
    except Exception:  # noqa: BLE001
        pass
    r = subprocess.run([node, run, "file://" + html, str(ancho), str(alto), png], capture_output=True, text=True, env=env, timeout=120)
    return r.returncode == 0 and os.path.exists(png)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--ancho", type=int, default=3000)
    a = ap.parse_args()
    m = L.cargar_marca(a.marca)
    logos = L.logos(m, os.path.dirname(os.path.abspath(a.marca)))
    if not logos:
        print("marca.json no lista ningún logo que exista en disco (brandKit.logo).")
        return 2
    os.makedirs(a.salida, exist_ok=True)
    hechos = 0
    for version, svg in logos.items():
        if not svg.lower().endswith(".svg"):
            continue
        png = os.path.join(a.salida, f"{os.path.splitext(os.path.basename(svg))[0]}.png")
        if shutil.which("rsvg-convert"):
            w, h = proporcion(svg)
            ok = subprocess.run(["rsvg-convert", "-w", str(a.ancho), "-h", str(round(a.ancho * h / w)), "-o", png, svg]).returncode == 0
        else:
            ok = con_chromium(svg, png, a.ancho)
        print(("ok   " if ok else "FALLO"), version, "→", png if ok else "(no se pudo exportar)")
        hechos += ok
        shutil.copy(svg, os.path.join(a.salida, os.path.basename(svg)))
    if not hechos:
        print("No hay rsvg-convert ni Chromium con Playwright: se copiaron los SVG, que son el original. Para PNG: python3 skills/gusto/tools/comprobar_entorno.py")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
