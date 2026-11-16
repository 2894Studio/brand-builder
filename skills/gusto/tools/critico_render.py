#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Revisión mecánica de una pieza HTML (post, lámina, banner) abierta en Chromium.

Uso:  python3 critico_render.py pieza.html [--ancho 1080 --alto 1440] [--marca marca.json] [--json salida.json] [--png captura.png]

Detecta (errores): texto fuera del lienzo, cajas de texto que se pisan, fuente que cae a una de reserva,
contraste de texto < 4,5:1 (3:1 si es grande), texto de menos de ~1,8 % del lado corto.
Avisa de: colores fuera de marca.json, titular poco dominante, última línea con una sola palabra,
demasiado texto, texto sobre imagen/degradado (contraste no medible).
Texto que debe sangrar a propósito: ponle el atributo data-bleed.
NO juzga si la pieza es bonita ni si transmite lo que debe: eso lo valoran el modelo y la persona.

Necesita Playwright (Node: npm i playwright · o Python: pip install playwright) y un Chromium.
Sin él, lo dice y sale con código 2 sin dar la pieza por buena.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
MEDIR = os.path.join(AQUI, "medir.js")


def medir_con_node(url, ancho, alto, png):
    node = shutil.which("node")
    if not node:
        return None
    runner = r"""
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [url,w,h,png,js]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+h}});
await p.goto(url);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
if(png)await p.screenshot({path:png});
const fn=eval(fs.readFileSync(js,'utf8'));
const r=await p.evaluate(fn,{});console.log(JSON.stringify(r));await b.close()})().catch(e=>{console.error(e.message);process.exit(3)})
"""
    d = tempfile.mkdtemp()
    ruta = os.path.join(d, "run.js")
    open(ruta, "w").write(runner)
    # busca playwright instalado globalmente o en el proyecto
    env = dict(os.environ)
    try:
        raiz = subprocess.run([shutil.which("npm") or "npm", "root", "-g"], capture_output=True, text=True, timeout=20).stdout.strip()
        env["NODE_PATH"] = os.pathsep.join(filter(None, [env.get("NODE_PATH", ""), raiz, os.path.join(os.getcwd(), "node_modules")]))
    except Exception:
        pass
    r = subprocess.run([node, ruta, url, str(ancho), str(alto), png or "", MEDIR], capture_output=True, text=True, env=env, timeout=120)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def medir_con_python(url, ancho, alto, png):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    js = open(MEDIR, encoding="utf-8").read()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": ancho, "height": alto})
        pg.goto(url)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(400)
        if png:
            pg.screenshot(path=png)
        r = pg.evaluate(js, {})
        b.close()
    return r


def hex_a_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hex_en(obj, acc):
    if isinstance(obj, dict):
        for v in obj.values():
            hex_en(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            hex_en(v, acc)
    elif isinstance(obj, str) and len(obj) == 7 and obj[0] == "#":
        try:
            acc.add(hex_a_rgb(obj))
        except ValueError:
            pass


def juzgar(r, marca_ruta):
    """Convierte las medidas en errores y avisos. Cada hallazgo cita lo medido."""
    W, H = r["W"], r["H"]
    err, av = [], []
    escala = min(W, H) / 1080.0
    for t in r["textos"]:
        if not t["bleed"]:
            if t["x"] < -1 or t["y"] < -1 or t["x"] + t["w"] > W + 1 or t["y"] + t["h"] > H + 1:
                err.append(f"«{t['texto']}» se sale del lienzo (caja {round(t['x'])},{round(t['y'])} {round(t['w'])}×{round(t['h'])} en {W}×{H})")
        minimo = 18 * escala + 1 * escala  # ≈ 1,8 % del lado corto
        if t["size"] < minimo:
            err.append(f"«{t['texto']}» mide {t['size']:.0f}px; el mínimo para este ancho es {minimo:.0f}px")
        if t["contraste"] is not None:
            grande = t["size"] >= 24 or (t["size"] >= 18.7 and t["peso"] >= 700)
            if t["contraste"] < (3.0 if grande else 4.5):
                err.append(f"«{t['texto']}» tiene contraste {t['contraste']}:1 (mínimo {'3' if grande else '4,5'}:1)")
        elif t["fondoNoMedible"]:
            av.append(f"«{t['texto']}» está sobre {t['fondoNoMedible']}: contraste no medible; compruébalo a ojo con un panel opaco debajo")
        if t["lineas"] >= 3 and len(t["ultima"]) == 1 and t["size"] >= 40:
            av.append(f"«{t['texto']}» termina en una línea con una sola palabra («{t['ultima'][0]}»)")
    for s in r["solapes"]:
        err.append(f"«{s['a']}» y «{s['b']}» se pisan ({s['ix']}×{s['iy']}px)")
    for f in r["fuentesDisponibles"]:
        if not f["ok"]:
            err.append(f"la fuente «{f['familia']}» no está disponible: se está viendo una de reserva")
    for f in r["fuentesCargadas"]:
        if f["estado"] == "error":
            err.append(f"la fuente «{f['familia']}» no se pudo cargar")
    tam = sorted(set(round(x) for x in r["tamanos"]))
    if tam:
        mayor, mediana = max(r["tamanos"]), sorted(r["tamanos"])[len(r["tamanos"]) // 2]
        if mayor / max(mediana, 1) < 2.5 and len(r["tamanos"]) > 2:
            av.append(f"jerarquía débil: el texto mayor ({mayor:.0f}px) es solo {mayor / mediana:.1f}× la mediana ({mediana:.0f}px); busca al menos 2,5×")
        if len(tam) > 6:
            av.append(f"{len(tam)} tamaños de letra distintos; la pieza pierde ritmo (apunta a 4 o menos)")
    if r["caracteres"] > 320:
        av.append(f"{r['caracteres']} caracteres de texto: pieza densa para una red social")
    if marca_ruta and os.path.exists(marca_ruta):
        paleta = set()
        hex_en(json.load(open(marca_ruta, encoding="utf-8")), paleta)
        paleta |= {(255, 255, 255), (0, 0, 0)}
        fuera = []
        for c in r["colores"]:
            rgb = tuple(c["rgb"])
            if not any(sum((a - b) ** 2 for a, b in zip(rgb, p)) ** 0.5 < 14 for p in paleta):
                fuera.append("#%02X%02X%02X" % rgb)
        if fuera:
            av.append("colores fuera de marca.json: " + ", ".join(sorted(set(fuera))) + " (¿son tintes intencionados? añádelos a la marca o quítalos)")
    return err, av


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pieza")
    ap.add_argument("--ancho", type=int, default=1080)
    ap.add_argument("--alto", type=int, default=1440)
    ap.add_argument("--marca")
    ap.add_argument("--json")
    ap.add_argument("--png")
    a = ap.parse_args()
    url = "file://" + os.path.abspath(a.pieza)
    r = medir_con_node(url, a.ancho, a.alto, a.png) or medir_con_python(url, a.ancho, a.alto, a.png)
    if r is None:
        print("No puedo abrir la pieza: falta Playwright con Chromium.\n"
              "  Node:   npm i -g playwright && npx playwright install chromium\n"
              "  Python: pip install playwright && playwright install chromium\n"
              "La pieza NO se da por revisada.")
        return 2
    err, av = juzgar(r, a.marca)
    if a.json:
        json.dump({"errores": err, "avisos": av, "medidas": r}, open(a.json, "w"), ensure_ascii=False, indent=1)
    for e in err:
        print("  ERROR ", e)
    for x in av:
        print("  aviso ", x)
    print(f"{a.pieza}: {len(err)} error(es), {len(av)} aviso(s)" + ("  → corregir antes de enseñarla" if err else ""))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
