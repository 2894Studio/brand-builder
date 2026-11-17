#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Autotest de la skill gusto. Comprueba gusto_lib, gusto.py, el analizador de imágenes y el crítico de render.
Lo que no se puede ejecutar por falta de Pillow o de Playwright se marca SALTADO, nunca como superado.

Uso:  python3 verificar_gusto.py     (sale con 1 si algo falla; los SALTADO no hacen fallar)
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
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
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


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
    gj = json.load(open(ruta, encoding="utf-8"))
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
        refs = {x["nombre"]: x for x in json.load(open(gr, encoding="utf-8"))["referencias"]}
        ok(refs["lisa"]["medido"]["aire_pct"] >= 90, f"imagen lisa: aire alto ({refs['lisa']['medido']['aire_pct']}%)")
        ok(refs["ruido"]["medido"]["aire_pct"] < refs["lisa"]["medido"]["aire_pct"], "imagen con detalle: menos aire que la lisa")
        ok(refs["lisa"]["medido"]["dominantes"][0]["hex"].startswith("#1"), "color dominante de la lisa ≈ azul")
        ok(refs["lisa"]["tipo"] == "no" and refs["lisa"]["interpretacion"]["tono"] is None, "el tono queda sin interpretar (no se inventa)")
        n1 = len(json.load(open(gr, encoding="utf-8"))["referencias"])
        py(os.path.join(AQUI, "analizar_referencias.py"), carp, "--gusto", gr)
        ok(len(json.load(open(gr, encoding="utf-8"))["referencias"]) == n1, "volver a analizar no duplica referencias")
    except ImportError:
        saltados.append("analizador (falta Pillow)")
        print("  SALTADO analizador: falta Pillow")

    # 4b. comprobador de entorno
    r = py(os.path.join(AQUI, "comprobar_entorno.py"))
    ok(r.returncode == 0 and "Python 3.11+" in r.stdout and "Con esta configuración puedes" in r.stdout, "comprobar_entorno informa de las capacidades")

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
        ok("«Aa»" not in s, "un titular gigante con line-height < 1 no da falso solape con el texto de debajo")
        ok("GHOSTWORD" not in s, "un texto data-decorativo no se juzga (ni se sale del lienzo ni se pisa)")
        r = py(os.path.join(AQUI, "critico_render.py"), os.path.join(FIX, "plantilla.html"))
        for frag, msg in (("tipografía por defecto", "tipografía por defecto"), ("texto gris sobre un fondo de color", "gris sobre color"), ("negro o gris puro", "negro o gris puro"), ("degradado morado a azul", "degradado morado a azul"), ("tarjetas dentro de tarjetas", "tarjetas anidadas")):
            ok(frag in r.stdout, f"anti-plantilla detecta: {msg}")
        r = py(os.path.join(AQUI, "critico_render.py"), os.path.join(FIX, "bien.html"), "--marca", marca)
        ok(r.returncode == 0 and not any(x in r.stdout for x in ("gris sobre un fondo", "negro o gris puro", "degradado morado", "tarjetas dentro")), "una pieza correcta no da falsos positivos de color, degradado ni tarjetas")
        r = py(os.path.join(AQUI, "critico_render.py"), os.path.join(FIX, "recorte.html"))
        ok(r.returncode == 1 and "recortado por su contenedor" in r.stdout and r.stdout.count("recortado") == 1, "detecta el texto recortado por un contenedor (y solo ese)")
        r = py(os.path.join(AQUI, "critico_render.py"), os.path.join(FIX, "partida.html"), "--ancho", "800", "--alto", "300")
        ok("«#1B2430» se parte a mitad" in r.stdout and r.stdout.count("mitad de palabra") == 1, "detecta una palabra partida a mitad (y no una frase que salta entre palabras)")
        try:
            import PIL  # noqa: F401
            ok("Blanco sobre degradado claro" in s and "medido sobre la captura" in s, "mide el contraste sobre un degradado con la captura")
            ok("Azul oscuro sobre degradado" not in s, "no marca el texto oscuro que sí contrasta sobre el degradado")
        except ImportError:
            saltados.append("contraste muestreado (falta Pillow)")

# ---- decisiones transferables y contraste con referencias ----
import json as _j
GJ = os.path.join(AQUI, "gusto.py")
with tempfile.TemporaryDirectory() as td:
    gj = os.path.join(td, "gusto.json")
    py(GJ, "init", "--gusto", gj)
    gd = _j.load(open(gj, encoding="utf-8"))
    gd["referencias"] = [{"nombre": "ref_si", "archivo": "ref_si.png", "tipo": "si", "nota_usuario": "me gusta el aire"}, {"nombre": "ref_no", "archivo": "ref_no.png", "tipo": "no"}]
    _j.dump(gd, open(gj, "w", encoding="utf-8"))
    r = py(GJ, "validar", "--gusto", gj)
    ok("sin decisiones transferables" in r.stdout, "validar avisa de referencias «sí» sin decisiones transferables")
    r = py(GJ, "decision", "--ref", "ref_si", "--dimension", "inventada", "--regla", "x", "--gusto", gj)
    ok(r.returncode != 0, "decision rechaza una dimensión que no existe")
    py(GJ, "decision", "--ref", "ref_si", "--dimension", "forma", "--regla", "esquinas de 30 px", "--aplica", "post", "--gusto", gj)
    r = py(GJ, "validar", "--gusto", gj)
    ok("solo tocan forma o color" in r.stdout, "validar avisa si las decisiones solo son forma o color (lo genérico)")
    py(GJ, "decision", "--ref", "ref_si", "--dimension", "simbolo", "--regla", "geometría 2D plana sin 3D", "--aplica", "logo", "--gusto", gj)
    py(GJ, "decision", "--ref", "ref_si", "--dimension", "composicion", "--regla", "elemento recortado por el borde", "--aplica", "post,bento", "--gusto", gj)
    py(GJ, "decision", "--ref", "ref_no", "--dimension", "imagen", "--regla", "ilustración 3D hinchada", "--gusto", gj)
    r = py(GJ, "reglas", "--gusto", gj)
    ok("R1 [forma]" in r.stdout and "R4 [imagen] EVITAR:" in r.stdout, "reglas numera las decisiones R1…Rn y marca las de «no» como EVITAR")
    r = py(GJ, "validar", "--gusto", gj)
    ok("solo tocan forma o color" not in r.stdout and "sin decisiones transferables" not in r.stdout, "con dimensiones distintivas desaparecen los avisos")
    try:
        from PIL import Image
        rd = os.path.join(td, "referencias"); os.makedirs(rd)
        Image.new("RGB", (800, 600), "#336699").save(os.path.join(rd, "ref_si.png"))
        pz = os.path.join(td, "pz"); os.makedirs(pz)
        Image.new("RGB", (1080, 1440), "#EE9933").save(os.path.join(pz, "post-1-que-es.png"))
        CR = os.path.join(AQUI, "contacto_referencias.py")
        r = py(CR, "--gusto", gj, "--referencias", rd, "--piezas", pz, "--salida", pz)
        ok(r.returncode == 0 and os.path.exists(os.path.join(pz, "contacto-gusto.png")) and "R3" in open(os.path.join(pz, "revision-gusto.md"), encoding="utf-8").read(), "contacto_referencias genera la hoja de contraste y revision-gusto.md con todas las reglas")
    except ImportError:
        saltados.append("contacto_referencias (falta Pillow)")

# ---- etiquetador: importar ZIP y servidor local ----
try:
    import io as _io
    import zipfile as _z
    import threading as _th
    import base64 as _b64
    import urllib.request as _ur
    from PIL import Image as _PI
    def _png(c):
        b = _io.BytesIO(); _PI.new("RGB", (300, 400), c).save(b, "PNG"); return b.getvalue()
    meta = {"version": 1, "referencias": [
        {"archivo": "uno.png", "nombre": "uno", "tipo": "si", "nota_usuario": "me gusta", "decisiones": [{"dimension": "nombre", "regla": "minúsculas gordas", "aplica_en": ["logo"]}, {"dimension": "firma", "regla": "sello", "aplica_en": ["post"]}]},
        {"archivo": "../../peligro.png", "nombre": "p", "tipo": "no", "nota_usuario": "x", "decisiones": []},
        {"archivo": "malo.exe", "nombre": "m", "tipo": "si", "nota_usuario": "x", "decisiones": []}]}
    with tempfile.TemporaryDirectory() as te:
        zp = os.path.join(te, "e.zip")
        with _z.ZipFile(zp, "w") as zf:
            zf.writestr("etiquetas.json", _j.dumps(meta)); zf.writestr("referencias/uno.png", _png("#3355CC")); zf.writestr("referencias/peligro.png", _png("#CC5533")); zf.writestr("referencias/malo.exe", b"x")
        r = py(os.path.join(AQUI, "importar_etiquetado.py"), zp, "--gusto", os.path.join(te, "g.json"), "--referencias", os.path.join(te, "refs"))
        gi = _j.load(open(os.path.join(te, "g.json"), encoding="utf-8")) if os.path.exists(os.path.join(te, "g.json")) else {"referencias": []}
        uno = next((x for x in gi["referencias"] if x.get("archivo") == "uno.png"), {})
        ok(r.returncode == 0 and uno.get("tipo") == "si" and uno.get("confirmado") and len(uno.get("decisiones", [])) == 2 and uno.get("medido"), "importar_etiquetado copia, mide y vuelca tipo, nota y decisiones")
        ok(os.path.exists(os.path.join(te, "refs", "uno.png")) and not os.path.exists(os.path.join(te, "refs", "malo.exe")) and not os.path.exists(os.path.join(te, "..", "peligro.png")), "importar_etiquetado rechaza nombres y formatos peligrosos")
        sys.path.insert(0, AQUI)
        import etiquetador as _E
        srv = _E.servidor(os.path.join(te, "proy"), 0)
        _th.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_port}"
        ok(_j.loads(_ur.urlopen(base + "/ping").read()).get("ok") is True and b"Etiquetador de referencias" in _ur.urlopen(base + "/").read(), "el servidor del etiquetador sirve la interfaz y responde al sondeo")
        m2 = {"version": 1, "referencias": [{"archivo": "a.png", "nombre": "a", "tipo": "si", "nota_usuario": "n", "decisiones": [], "_datos": "data:image/png;base64," + _b64.b64encode(_png("#118833")).decode()}]}
        rq = _ur.Request(base + "/guardar", data=_j.dumps(m2).encode(), headers={"Content-Type": "application/json"})
        resp = _j.loads(_ur.urlopen(rq).read())
        ok(resp.get("ok") and os.path.exists(os.path.join(te, "proy", "referencias", "a.png")) and os.path.exists(os.path.join(te, "proy", "gusto.json")), "el servidor guarda referencias/ y gusto.json en el proyecto")
        srv.shutdown()
except ImportError:
    saltados.append("etiquetador (falta Pillow)")

print()
if saltados:
    print("SALTADO:", "; ".join(saltados))
print("TODO OK" if not fallos else f"{len(fallos)} FALLO(S)")
sys.exit(1 if fallos else 0)
