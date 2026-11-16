#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Autotest de la skill gusto. Comprueba gusto_lib, gusto.py, el analizador de imágenes y el crítico de render.
Lo que no se puede ejecutar por falta de Pillow o de Playwright se marca SALTADO, nunca como superado.

Uso:  python3 verificar_gusto.py     (sale con 1 si algo falla; los SALTADO no hacen fallar)
"""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gusto_lib as G  # noqa: E402

RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
FIX = os.path.join(RAIZ, "evals", "fixtures", "gusto")
fallos, saltados = [], []


def ok(cond, msg):
    print(("  ok     " if cond else "  FALLO  ") + msg)
    if not cond:
        fallos.append(msg)


def py(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True)


# 1. proporción de tonos
t = {"serio": 50, "divertido": 20, "tecnologico": 30}
for hacia in G.TONOS:
    n = G.mover(t, hacia, 10)
    ok(sum(n.values()) == 100, f"mover hacia {hacia} mantiene la suma en 100 ({n})")
    ok(n[hacia] > t[hacia], f"mover hacia {hacia} lo sube")
ok(G.mover({"serio": 100, "divertido": 0, "tecnologico": 0}, "serio")["serio"] == 100, "mover no se pasa de 100")
ok(sum(G.normalizar({"serio": 1, "divertido": 1, "tecnologico": 1}).values()) == 100, "normalizar suma 100")

# 2. validación
g = G.nuevo()
g["referencias"] = [{"nombre": "A", "tipo": "si", "confirmado": True}]
err, av = G.validar(g)
ok(any("nota_usuario" in e for e in err), "una referencia confirmada sin nota se rechaza")
g["referencias"][0]["confirmado"] = False
g["tonos"]["serio"] = 70
err, _ = G.validar(g)
ok(any("sumar 100" in e for e in err), "tonos que no suman 100 se rechazan")
g = G.nuevo(); g["referencias"] = [{"nombre": "X", "tipo": "raro"}]
ok(any("tipo" in e for e in G.validar(g)[0]), "tipo desconocido se rechaza")

# 3. CLI A/B
with tempfile.TemporaryDirectory() as d:
    ruta = os.path.join(d, "gusto.json")
    ok(py(os.path.join(AQUI, "gusto.py"), "init", "--gusto", ruta).returncode == 0, "gusto.py init crea el archivo")
    ok(py(os.path.join(AQUI, "gusto.py"), "init", "--gusto", ruta).returncode == 1, "init no sobrescribe")
    r = py(os.path.join(AQUI, "gusto.py"), "ab", "--gusto", ruta, "--a", "serio", "--b", "divertido", "--elige", "b", "--motivo", "prueba")
    ok(r.returncode == 0, "ab registra una elección")
    gj = json.load(open(ruta))
    ok(gj["tonos"]["divertido"] > 20 and sum(gj["tonos"].values()) == 100 and len(gj["elecciones_ab"]) == 1, "la elección mueve la proporción y se guarda")

    # 4. analizador (Pillow)
    try:
        from PIL import Image, ImageDraw
        carp = os.path.join(d, "refs"); os.makedirs(carp)
        lisa = Image.new("RGB", (400, 300), (20, 76, 221)); lisa.save(os.path.join(carp, "lisa.png"))
        ruido = Image.new("RGB", (400, 300), (255, 255, 255)); dr = ImageDraw.Draw(ruido)
        for i in range(0, 400, 10):
            dr.rectangle([i, (i * 7) % 300, i + 6, (i * 7) % 300 + 40], fill=((i * 3) % 255, (i * 5) % 255, (i * 11) % 255))
        ruido.save(os.path.join(carp, "ruido.png"))
        gr = os.path.join(d, "g.json")
        r = py(os.path.join(AQUI, "analizar_referencias.py"), carp, "--gusto", gr, "--tipo", "no")
        ok(r.returncode == 0, "analizar_referencias termina bien")
        refs = {x["nombre"]: x for x in json.load(open(gr))["referencias"]}
        ok(refs["lisa"]["medido"]["aire_pct"] >= 90, f"imagen lisa: aire alto ({refs['lisa']['medido']['aire_pct']}%)")
        ok(refs["ruido"]["medido"]["aire_pct"] < refs["lisa"]["medido"]["aire_pct"], "imagen con detalle: menos aire que la lisa")
        ok(refs["lisa"]["medido"]["dominantes"][0]["hex"].startswith("#1"), "color dominante de la lisa ≈ azul")
        ok(refs["lisa"]["tipo"] == "no" and refs["lisa"]["interpretacion"]["tono"] is None, "el tono queda sin interpretar (no se inventa)")
        n1 = len(json.load(open(gr))["referencias"])
        py(os.path.join(AQUI, "analizar_referencias.py"), carp, "--gusto", gr)
        ok(len(json.load(open(gr))["referencias"]) == n1, "volver a analizar no duplica referencias")
    except ImportError:
        saltados.append("analizador (falta Pillow)")
        print("  SALTADO analizador: falta Pillow")

    # 5. crítico
    marca = os.path.join(FIX, "marca.json")
    r = py(os.path.join(AQUI, "critico_render.py"), os.path.join(FIX, "bien.html"), "--marca", marca)
    if r.returncode == 2:
        saltados.append("crítico (falta Playwright)")
        print("  SALTADO crítico: falta Playwright")
    else:
        ok(r.returncode == 0 and "0 error" in r.stdout, "pieza correcta: 0 errores")
        r = py(os.path.join(AQUI, "critico_render.py"), os.path.join(FIX, "mal.html"), "--marca", marca)
        s = r.stdout
        ok(r.returncode == 1, "pieza defectuosa: sale con 1")
        ok("se sale del lienzo" in s, "detecta texto fuera del lienzo")
        ok("se pisan" in s, "detecta textos que se pisan")
        ok("mide 12px" in s, "detecta texto diminuto")
        ok("tiene contraste" in s, "detecta contraste bajo")
        ok("no está disponible" in s, "detecta fuente de reserva")
        ok("#FF00AA" in s, "avisa del color fuera de marca")
        r = py(os.path.join(AQUI, "critico_render.py"), os.path.join(FIX, "degradado.html"))
        s = r.stdout
        ok("GHOSTWORD" not in s, "un texto data-decorativo no se juzga (ni se sale del lienzo ni se pisa)")
        try:
            import PIL  # noqa: F401
            ok("Blanco sobre degradado claro" in s and "medido sobre la captura" in s, "mide el contraste sobre un degradado con la captura")
            ok("Azul oscuro sobre degradado" not in s, "no marca el texto oscuro que sí contrasta sobre el degradado")
        except ImportError:
            saltados.append("contraste muestreado (falta Pillow)")

print()
if saltados:
    print("SALTADO:", "; ".join(saltados))
print("TODO OK" if not fallos else f"{len(fallos)} FALLO(S)")
sys.exit(1 if fallos else 0)
