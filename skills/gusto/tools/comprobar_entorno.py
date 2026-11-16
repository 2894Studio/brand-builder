#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Comprueba qué puede hacer tu ordenador con la skill gusto y dice qué instalar para el resto.

Uso:  python3 comprobar_entorno.py [--marca marca.json]

No instala nada. Prueba de verdad la cadena (abre una página en Chromium y la mide), no solo que los programas existan.
Con --marca comprueba además que las fuentes de tu marca están instaladas en este equipo.
Sale con 0 si Python es suficiente; el resto son capacidades opcionales (se listan como FALTA).
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SO = platform.system()  # Linux, Darwin, Windows

INSTALAR = {
    "python": {"Windows": "winget install Python.Python.3.12   (o descarga de python.org)",
               "Darwin": "brew install python   (o descarga de python.org)",
               "Linux": "sudo apt install python3 python3-pip"},
    "pillow": {"*": "python3 -m pip install pillow   (en Windows: py -m pip install pillow)"},
    "node": {"Windows": "winget install OpenJS.NodeJS.LTS   (o descarga de nodejs.org)",
             "Darwin": "brew install node   (o descarga de nodejs.org)",
             "Linux": "instala Node 18 o superior desde nodejs.org o con tu gestor de paquetes"},
    "playwright": {"*": "npm i -g playwright   y después   npx playwright install chromium"},
}


def cmd(clave):
    d = INSTALAR[clave]
    return d.get(SO) or d.get("*") or ""


def corre(args, tiempo=60):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=tiempo)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:  # noqa: BLE001
        return 99, "", str(e)


def pieza_prueba(familias):
    """HTML mínimo con una línea por familia; el crítico avisa de las que no existen."""
    lineas = "".join(f'<p style="font-family:\'{f}\',sans-serif;font-size:40px;margin:10px">Prueba {f}</p>' for f in familias)
    return f'<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff;color:#000">{lineas}</body>'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--marca")
    a = ap.parse_args()
    filas, pendientes = [], []

    def fila(nombre, ok, detalle, para, clave=None):
        filas.append((nombre, ok, detalle, para))
        if not ok and clave:
            pendientes.append((nombre, para, cmd(clave)))

    # Python
    v = sys.version_info
    py_ok = v >= (3, 11)
    fila("Python 3.11+", py_ok, f"{v.major}.{v.minor}.{v.micro}", "validar marca.json, generar tokens y el manual", "python")

    # Pillow
    try:
        import PIL
        fila("Pillow", True, PIL.__version__, "medir referencias y medir contraste sobre degradados")
    except ImportError:
        fila("Pillow", False, "no instalado", "medir referencias y medir contraste sobre degradados", "pillow")

    # Node
    node = shutil.which("node")
    nv = ""
    if node:
        _, out, _ = corre([node, "--version"], 15)
        nv = out.strip()
    node_ok = bool(node) and nv.startswith("v") and int(nv[1:].split(".")[0]) >= 18
    fila("Node 18+", node_ok, nv or "no instalado", "revisar piezas con Chromium y generar mapas de puntos", "node")

    # Playwright + Chromium: se prueba de extremo a extremo con el propio crítico
    familias = ["sans-serif"]
    if a.marca and os.path.exists(a.marca):
        try:
            t = json.load(open(a.marca, encoding="utf-8")).get("tipografia", {})
            familias = [t[k]["familia"] for k in ("titulos", "texto") if k in t and "familia" in t[k]]
        except Exception:  # noqa: BLE001
            pass
    with tempfile.TemporaryDirectory() as d:
        html = os.path.join(d, "prueba.html")
        open(html, "w", encoding="utf-8").write(pieza_prueba(familias))
        rc, out, err = corre([sys.executable, os.path.join(AQUI, "critico_render.py"), html, "--ancho", "600", "--alto", "300"], 120)
    navegador_ok = rc in (0, 1)  # 1 = abrió y midió, aunque haya avisado de algo
    fila("Playwright + Chromium", navegador_ok, "abre y mide una página" if navegador_ok else "no se puede abrir una página",
         "revisar piezas (solapes, contraste, fuentes)", "playwright")
    if navegador_ok and a.marca:
        for f in familias:
            falta = f"«{f}» no está disponible" in out
            fila(f"Fuente {f}", not falta, "instalada" if not falta else "NO instalada en este equipo",
                 "que las piezas se vean con la tipografía de la marca (si falta, el navegador pone otra; si la marca usa Google Fonts y hay red, se carga sola)")
            if falta:
                pendientes.append((f"Fuente {f}", "ver la tipografía de la marca", "descárgala de fonts.google.com e instálala en el sistema; reinicia el navegador"))

    # Informe
    print(f"Sistema: {SO} · Python {v.major}.{v.minor}\n")
    ancho = max(len(f[0]) for f in filas)
    for nombre, ok, detalle, para in filas:
        print(f"  {'OK   ' if ok else 'FALTA'}  {nombre.ljust(ancho)}  {detalle}")
    print()
    capacidades = [
        ("Crear la marca (estrategia, identidad, voz, tokens, manual)", py_ok),
        ("Medir tus referencias de imagen", any(f[0] == "Pillow" and f[1] for f in filas)),
        ("Revisar piezas con el crítico", navegador_ok),
        ("Contraste medido sobre degradados e imágenes", navegador_ok and any(f[0] == "Pillow" and f[1] for f in filas)),
        ("Mapa de puntos (mapa_puntos.mjs)", node_ok),
    ]
    print("Con esta configuración puedes:")
    for t, ok in capacidades:
        print(f"  {'sí' if ok else 'NO'}  {t}")
    if pendientes:
        print("\nPara tener todo:")
        for nombre, para, como in pendientes:
            print(f"  · {nombre}: {como}")
    print("\nNota: la comprobación en Windows y macOS no está verificada; los comandos son los habituales de cada sistema.")
    return 0 if py_ok else 1


if __name__ == "__main__":
    sys.exit(main())
