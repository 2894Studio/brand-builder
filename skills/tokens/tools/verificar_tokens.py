#!/usr/bin/env python3
"""Autotest de tokens y del puente a motion-architect, con la marca de prueba PULSO.

Uso:  python3 verificar_tokens.py
Comprueba: los 6 archivos de tokens, el contraste obligatorio, el fallo con un texto ilegible,
la forma exacta de brand.json de motion-architect y que no se sobrescribe sin --forzar.
"""
import copy
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
FIX = os.path.join(RAIZ, "evals", "fixtures", "pulso", "marca.json")
fallos = []


def ok(cond, msg):
    if not cond:
        fallos.append(msg)
        print("  FALLO", msg)


def run(*args):
    return subprocess.run([sys.executable] + list(args), capture_output=True, text=True)


marca = json.load(open(FIX, encoding="utf-8"))
with tempfile.TemporaryDirectory() as tmp:
    # 1) tokens
    r = run(os.path.join(AQUI, "generar_tokens.py"), FIX, "--salida", os.path.join(tmp, "t"))
    ok(r.returncode == 0, "generar_tokens debe salir con 0 con PULSO: " + r.stderr[-200:])
    for f in ("tokens.json", "tokens.css", "tailwind.preset.js", "tailwind-v4.css", "contraste.md", "ejemplo.html"):
        ok(os.path.isfile(os.path.join(tmp, "t", f)), "falta " + f)
    ok("--color-text-default" in open(os.path.join(tmp, "t", "tokens.css"), encoding="utf-8").read(), "tokens.css sin variables semánticas")

    # 2) un texto ilegible debe impedir generar
    mala = copy.deepcopy(marca)
    for c in mala["visual"]["colores"]:
        if c["rol"] == "texto":
            c["hex"] = "#9AA0AA"
    pm = os.path.join(tmp, "mala.json")
    json.dump(mala, open(pm, "w"))
    ok(run(os.path.join(AQUI, "generar_tokens.py"), pm, "--salida", os.path.join(tmp, "m")).returncode == 1,
       "un texto con contraste 2,4:1 debe fallar")

    # 3) puente a motion-architect
    brand = os.path.join(tmp, "brand.json")
    r = run(os.path.join(AQUI, "exportar_motion.py"), FIX, "--salida", brand)
    ok(r.returncode == 0, "exportar_motion debe salir con 0: " + r.stderr[-200:])
    b = json.load(open(brand, encoding="utf-8"))
    ok(list(b) == ["name", "tagline", "colors", "fonts", "radius", "style"], f"claves de primer nivel: {list(b)}")
    ok(list(b["colors"]) == ["background", "surface", "text", "muted", "accent", "accent2"], "claves de colors")
    ok(list(b["fonts"]) == ["display", "body"], "claves de fonts")
    ok(isinstance(b["radius"], (int, float)) and not isinstance(b["radius"], bool), "radius debe ser número")
    ok(b["colors"]["accent"] == "#2F4BD8", "accent debe ser el primario (legible sobre el fondo)")
    ok(b["colors"]["accent2"] == "#00C27A", "accent2 debe ser el acento")
    ok(not b["style"].endswith(" ") and len(b["style"]) <= 141, "style demasiado largo o con espacio final")
    ok(b["fonts"]["display"] == "Space Grotesk", "fuente de títulos")

    # 4) protecciones de sobrescritura
    ok(run(os.path.join(AQUI, "exportar_motion.py"), FIX, "--salida", brand).returncode == 1, "no debe sobrescribir sin --forzar")
    r = run(os.path.join(AQUI, "exportar_motion.py"), FIX, "--salida", brand, "--forzar")
    ok(r.returncode == 0 and os.path.isfile(brand + ".bak"), "--forzar debe dejar brand.json.bak")

if fallos:
    print(f"\n{len(fallos)} fallo(s)")
    sys.exit(1)
print("tokens y puente a motion-architect: todas las comprobaciones pasan")
