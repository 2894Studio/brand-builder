#!/usr/bin/env python3
"""Autotest del sistema de láminas. Genera el kit de PULSO en los cinco territorios y comprueba
las reglas de maquetación: rejilla, márgenes, título en ≤2 líneas, SVG bien formado, pie y numeración.

Uso:  python3 verificar_laminas.py
Sale con 0 si todo pasa y con 1 si alguna regla falla.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import copy
import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import lib_laminas as L  # noqa: E402  (ya comprueba la rejilla al importar)
import marca_lib as m  # noqa: E402
import generar_kit as G  # noqa: E402

RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
FIX = os.path.join(RAIZ, "evals", "fixtures", "pulso")
NS = "{http://www.w3.org/2000/svg}"
fallos = []


def comprobar(cond, msg):
    if not cond:
        fallos.append(msg)
        print("  FALLO", msg)


# 1) rejilla y escala
comprobar(L.x(1) == 120 and L.x(12) == 1682, "inicio de columnas")
comprobar(L.span(1, 12) == (120, 1680), "ancho de contenido")

# 2) contraste: el acento verde de PULSO sobre su base no sirve para texto
comprobar(m.contraste("#00C27A", "#F3F4F6") < 3, "el acento verde debería quedar bajo 3:1")
comprobar(m.contraste("#14181F", "#F3F4F6") > 15, "tinta sobre base")

# 3) léxico prohibido
comprobar("potenciar" in m.hallar_lexico("Vamos a potenciar tu marca"), "léxico: verbo inflado")
comprobar(m.hallar_lexico("No es solo un taller, es una forma de vida"), "léxico: «no es solo X, es Y»")
comprobar(not m.hallar_lexico("Cambiamos la cadena el jueves. 18 €."), "léxico: frase limpia no debe saltar")

# 4) kit en los cinco territorios
marca0 = m.cargar(os.path.join(FIX, "marca.json"))
kit0 = json.load(open(os.path.join(FIX, "kit.json"), encoding="utf-8"))
# 4 valores con frases largas: el caso que desbordaba las tarjetas
kit4 = copy.deepcopy(kit0)
kit4["valores"] = [{"nombre": f"Valor {i}", "frase": "Una frase larga que ocupa dos líneas completas dentro de la tarjeta de la lámina y que antes se salía."} for i in range(4)]
kit4["principio"] = "Subes mejor cuando todos llevan la misma cuerda."
refs = [{"nombre": "Revista editorial", "atributo": "la escala enorme del titular y el silencio alrededor", "tipo": "si"},
        {"nombre": "Marca de neón", "atributo": "los degradados y brillos que parecen generados", "tipo": "no"}]
variantes = [(t_, k_, ex) for t_ in m.TERRITORIOS for k_, ex in ((kit0, True), (kit4, True), (kit0, False))]
variantes.append(("editorial", kit0, True))          # y una con referencias, que añade una lámina
for terr, kit, expresivo in variantes:
    con_refs = (terr, kit, expresivo) == variantes[-1]
    mc = copy.deepcopy(marca0)
    if con_refs:
        mc["referencias"] = refs
    mc["brandKit"]["territorio"] = terr
    kit = copy.deepcopy(kit)
    kit["expresivo"] = expresivo
    etiqueta = f"{terr}/{'expresivo' if expresivo else 'sobrio'}/{len(kit.get('valores', []))}v" + ("+refs" if con_refs else "")
    with tempfile.TemporaryDirectory() as tmp:
        g = G.Generador(mc, kit, tmp)
        g.generar()
        esperadas = (17 if expresivo else 16) + (1 if con_refs else 0)
        comprobar(len(g.laminas) == esperadas, f"[{etiqueta}] debe haber {esperadas} láminas, hay {len(g.laminas)}")
        for nombre, titulo, s in g.laminas:
            try:
                raiz = ET.fromstring(s)
            except ET.ParseError as ex:
                comprobar(False, f"[{etiqueta}] {nombre}: SVG mal formado ({ex})")
                continue
            es_div = "divisor" in nombre or "principio" in nombre
            es_portada = nombre.endswith("portada.svg")
            textos = [e for e in raiz.iter(NS + "text")]
            for e in textos:
                if e.get("data-sangre"):                 # tipografía decorativa a sangre: puede salirse...
                    # ...pero tiene que asomar dentro del lienzo, o es un adorno invisible (error real que ya ocurrió)
                    xs, anc_s, tam = float(e.get("x")), e.get("text-anchor"), float(e.get("font-size"))
                    n_car = max(1, len(e.text or ""))
                    ancho_est = 0.5 * tam * n_car
                    x0, x1 = (xs - ancho_est, xs) if anc_s == "end" else (xs, xs + ancho_est)
                    comprobar(x0 < L.W - 150 and x1 > 150, f"[{etiqueta}] {nombre}: el texto a sangre no asoma en el lienzo (x {x0:.0f}..{x1:.0f})")
                    continue
                if e.text and ".." in e.text and "…" not in e.text:
                    comprobar(False, f"[{etiqueta}] {nombre}: doble punto en «{e.text[:40]}»")
                xx, anc = float(e.get("x")), e.get("text-anchor")
                if anc == "start":
                    comprobar(xx >= L.MARGIN_X - 1, f"[{etiqueta}] {nombre}: texto en x={xx} invade el margen izquierdo")
                elif anc == "end":
                    comprobar(xx <= L.W - L.MARGIN_X + 1, f"[{etiqueta}] {nombre}: texto en x={xx} invade el margen derecho")
            pies = [e for e in textos if e.text == mc["nombre"] and float(e.get("y")) > 900]
            if es_div or es_portada:
                comprobar(not pies, f"[{etiqueta}] {nombre}: divisores y portada no llevan pie")
            else:
                comprobar(bool(pies), f"[{etiqueta}] {nombre}: falta el pie con el wordmark")
        titulos_largos = [a for a in g.est.avisos if "ocupa" in a and "líneas" in a]
        comprobar(not titulos_largos, f"[{etiqueta}] títulos de más de 2 líneas: {titulos_largos}")
        no_caben = [a for a in g.est.avisos if "no caben" in a]
        comprobar(not no_caben, f"[{etiqueta}] valores que no caben: {no_caben}")
        if expresivo:
            port = g.laminas[0][2]
            comprobar('data-sangre="1"' in port, f"[{etiqueta}] la portada expresiva debe llevar tipografía a sangre")
    print(f"ok  {etiqueta:34} {len(g.laminas)} láminas")

# el PDF se monta con los logos incrustados (rsvg-convert no carga rutas relativas): se comprueba con un rsvg falso
import subprocess  # noqa: E402
RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
marca_p = os.path.join(RAIZ, "evals", "fixtures", "pulso", "marca.json")
if os.path.exists(marca_p) and sys.platform != "win32":      # el rsvg falso es un script de shell
    with tempfile.TemporaryDirectory() as tmp:
        falso = os.path.join(tmp, "rsvg-convert")
        reg = os.path.join(tmp, "visto.txt")
        with open(falso, "w", encoding="utf-8") as fh:
            fh.write('#!/bin/sh\nfor a in "$@"; do case "$a" in *.svg) grep -c "../logo/" "$a" >> %s;; esac; done\ntouch "$4"\n' % reg)
        os.chmod(falso, 0o755)
        env = dict(os.environ, PATH=tmp + os.pathsep + os.environ.get("PATH", ""))
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "generar_kit.py"), marca_p, "--salida", os.path.join(tmp, "kit")], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        visto = open(reg, encoding="utf-8").read().split() if os.path.exists(reg) else []
        comprobar(bool(visto) and all(v == "0" for v in visto), "PDF: las láminas llegan a rsvg-convert con los logos incrustados, sin rutas «../logo/»")

if fallos:
    print(f"\n{len(fallos)} fallo(s)")
    sys.exit(1)
print("\ntodas las comprobaciones pasan")
