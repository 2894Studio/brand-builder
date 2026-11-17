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
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
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
    ap.add_argument("--gusto", help="gusto.json: si tiene decisiones, exige revision-gusto.md resuelta")
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
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 2:
            avisos.append("el crítico no se pudo ejecutar (falta Playwright): las piezas NO están revisadas")
            print("  SALTADO crítico: falta Playwright")
            break
        errs = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ERROR")]
        ok(r.returncode == 0, f"{n}: el crítico da 0 errores" + ("" if r.returncode == 0 else " → " + "; ".join(errs[:3])))
        tells = [l.strip() for l in r.stdout.splitlines() if "anti-plantilla:" in l]
        justificado = False
        bpath = os.path.join(c, "brief.json")
        if os.path.exists(bpath):
            try:
                justificado = bool(str(json.load(open(bpath, encoding="utf-8")).get("tells_ok", "")).strip())
            except Exception:  # noqa: BLE001
                pass
        if len(tells) >= 2 and not justificado:
            ok(False, f"{n}: {len(tells)} huellas de plantilla (" + "; ".join(t.split("anti-plantilla:")[1].strip()[:60] for t in tells[:2]) + ") — corrígelas o justifícalas con «tells_ok» en el brief")
        elif tells:
            print("  aviso  " + f"{n}: " + tells[0].split("anti-plantilla:")[1].strip()[:110])
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
    if a.gusto and os.path.exists(a.gusto):
        print("5. Referencias (gusto)")
        gj, reglas = {}, []
        try:
            sys.path.insert(0, os.path.join(RAIZ, "skills", "gusto", "tools"))
            import gusto_lib as GL
            gj = GL.cargar(a.gusto)
            reglas = GL.reglas_numeradas(gj)
        except Exception:  # noqa: BLE001
            pass
        if not reglas:
            if any(r.get("tipo") == "si" for r in gj.get("referencias", [])):
                avisos.append("hay referencias «sí» pero sin decisiones transferables: las piezas no se han contrastado con ellas (gusto/references/entrenar.md)")
                print("  aviso  referencias sin decisiones: no hay nada que contrastar")
        else:
            # composición a medida: si el gusto tiene reglas de composición para posts, al menos un post no puede ser de plantilla
            comp = [r for r in reglas if r["dimension"] == "composicion" and "post" in (r["aplica_en"] or []) and not r["prohibe"]]
            if comp:
                arqs = []
                for n in ("post-1-que-es", "post-2-atributo"):
                    hp = os.path.join(c, n + ".html")
                    if os.path.exists(hp):
                        mm = re.search(r'<meta name="arquetipo" content="([^"]+)"', open(hp, encoding="utf-8").read())
                        arqs.append(mm.group(1) if mm else "propio")
                plantillas_ok = False
                bpg = os.path.join(c, "brief.json")
                if os.path.exists(bpg):
                    try:
                        plantillas_ok = bool(str(json.load(open(bpg, encoding="utf-8")).get("plantillas_ok", "")).strip())
                    except Exception:  # noqa: BLE001
                        pass
                a_medida = [x in ("compuesto", "propio") for x in arqs]
                ok(all(a_medida) or plantillas_ok or not arqs, "tu gusto tiene reglas de composición para posts: los dos posts son composición a medida (post_compuesto.py o HTML propio), no plantillas" + (f" (ahora: {', '.join(arqs)})" if arqs else ""))
            ids = {r["id"] for r in reglas}
            for cf in sorted(glob.glob(os.path.join(c, "composicion-*.json"))):
                try:
                    rf = (json.load(open(cf, encoding="utf-8")).get("concepto") or {}).get("referencias") or []
                except Exception:  # noqa: BLE001
                    rf = []
                ok(bool(rf) and all(x in ids for x in rf), f"{os.path.basename(cf)} cita reglas de gusto que existen" + ("" if rf and all(x in ids for x in rf) else f" ({', '.join(x for x in rf if x not in ids) or 'sin referencias'})"))
                # la composición debe aplicar al menos una regla de símbolo, forma, firma o imagen (no solo «aire»), y llevar algún elemento gráfico
                graf = {r["id"] for r in reglas if r["dimension"] in ("simbolo", "firma", "forma", "imagen") and "post" in (r["aplica_en"] or []) and not r["prohibe"]}
                if graf:
                    ok(bool(graf & set(rf)), f"{os.path.basename(cf)} aplica al menos una regla gráfica de tus referencias ({', '.join(sorted(graf)[:6])}), no solo las de aire y tipografía")
                try:
                    els = json.load(open(cf, encoding="utf-8")).get("elementos") or []
                except Exception:  # noqa: BLE001
                    els = []
                ok(any(e.get("tipo") in ("forma", "firma", "foto", "insignia", "simbolo", "palabra") for e in els), f"{os.path.basename(cf)} lleva algún elemento gráfico (forma, firma, foto, insignia, símbolo o palabra gigante), no solo texto")
            rev = os.path.join(c, "revision-gusto.md")
            ok(os.path.exists(rev), "revision-gusto.md existe (contraste de las piezas con las referencias)")
            if os.path.exists(rev):
                lineas = open(rev, encoding="utf-8").read().splitlines()
                pend, mal_ = [], []
                for r in reglas:
                    l = next((x for x in lineas if f" {r['id']} " in x or x.lstrip("- ").startswith(r["id"] + " ")), "")
                    bajo = l.lower().split("→", 1)[-1]
                    if not any(w in bajo for w in ("cumple", "parcial", "no aplica")) or "(pendiente)" in bajo:
                        pend.append(r["id"])
                    elif "no cumple" in bajo and "corregido" not in bajo:
                        mal_.append(r["id"])
                ok(not pend, "todas las reglas de las referencias están revisadas" + (f" (faltan {', '.join(pend)})" if pend else ""))
                # «parcial» con dientes: no más de un 25 % de las reglas aplicables, y ninguna que confiese trabajo sin hacer
                estados = {}
                for r in reglas:
                    l = next((x for x in lineas if f" {r['id']} " in x or x.lstrip("- ").startswith(r["id"] + " ")), "")
                    bajo = l.lower().split("→", 1)[-1]
                    estados[r["id"]] = "noaplica" if "no aplica" in bajo else ("nocumple" if "no cumple" in bajo else ("parcial" if "parcial" in bajo else "cumple"))
                aplicables = [i for i, e in estados.items() if e != "noaplica"]
                parciales = [i for i in aplicables if estados[i] == "parcial"]
                ok(len(parciales) <= max(1, int(0.25 * len(aplicables))), f"«parcial» en {len(parciales)} de {len(aplicables)} reglas aplicables (máximo 25 %): mejora las piezas en vez de matizar la revisión" + (f" ({', '.join(parciales[:6])})" if len(parciales) > max(1, int(0.25 * len(aplicables))) else ""))
                confesiones = [r["id"] for r in reglas if any(w in next((x for x in lineas if f" {r['id']} " in x), "").lower() for w in ("pendiente de cambiar", "queda pendiente", "lo dejo para", "más adelante", "no lo he podido"))]
                ok(not confesiones, "ninguna regla confiesa trabajo sin hacer" + (f" ({', '.join(confesiones)})" if confesiones else ""))
                ok(not mal_, "ninguna regla queda en «no cumple» sin corregir" + (f" ({', '.join(mal_)})" if mal_ else ""))
    print("6. Variedad")
    p1, p2 = (os.path.join(c, f"{n}.html") for n in ("post-1-que-es", "post-2-atributo"))
    if os.path.exists(p1) and os.path.exists(p2):
        r = subprocess.run([sys.executable, VARIEDAD, p1, p2], capture_output=True, text=True, encoding="utf-8", errors="replace")
        ok(r.returncode == 0, "los dos posts no comparten composición ni arquetipo" + ("" if r.returncode == 0 else ": " + r.stdout.strip().splitlines()[0]))
        if a.kits:
            otros = glob.glob(os.path.join(a.kits, "*", "lanzamiento", "post-*.html"))
            otros = [o for o in otros if os.path.abspath(os.path.dirname(o)) != os.path.abspath(c)]
            for p in (p1, p2):
                if otros:
                    r = subprocess.run([sys.executable, VARIEDAD, p] + otros, capture_output=True, text=True, encoding="utf-8", errors="replace")
                    ok(r.returncode == 0, f"{os.path.basename(p)} no se parece a los posts de otros kits")
    print()
    for x in avisos:
        print("AVISO:", x)
    print("PUERTA DE ENTREGA: ABIERTA" if not fallos else f"PUERTA CERRADA: {len(fallos)} fallo(s). Corrige antes de entregar.")
    marca = os.path.join(c, ".puerta-ok")
    if not fallos and not avisos:
        open(marca, "w", encoding="utf-8").write("puerta abierta\n")      # lo lee hooks/guardia_entrega.py
    elif os.path.exists(marca):
        os.remove(marca)
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
