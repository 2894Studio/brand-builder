#!/usr/bin/env python3
"""Autotest del sistema de láminas. Genera el kit de PULSO en los cinco territorios y comprueba
las reglas de maquetación: rejilla, márgenes, título en ≤2 líneas, SVG bien formado, pie y numeración.

Uso:  python3 verificar_laminas.py
Sale con 0 si todo pasa y con 1 si alguna regla falla.
"""
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
kit = json.load(open(os.path.join(FIX, "kit.json"), encoding="utf-8"))
for terr in m.TERRITORIOS:
    mc = copy.deepcopy(marca0)
    mc["brandKit"]["territorio"] = terr
    with tempfile.TemporaryDirectory() as tmp:
        g = G.Generador(mc, kit, tmp)
        g.generar()
        comprobar(len(g.laminas) == 16, f"[{terr}] debe haber 16 láminas, hay {len(g.laminas)}")
        for nombre, titulo, s in g.laminas:
            try:
                raiz = ET.fromstring(s)
            except ET.ParseError as ex:
                comprobar(False, f"[{terr}] {nombre}: SVG mal formado ({ex})")
                continue
            es_div = "divisor" in nombre
            es_portada = nombre.endswith("portada.svg")
            textos = [e for e in raiz.iter(NS + "text")]
            for e in textos:
                xx, anc = float(e.get("x")), e.get("text-anchor")
                if anc == "start":
                    comprobar(xx >= L.MARGIN_X - 1, f"[{terr}] {nombre}: texto en x={xx} invade el margen izquierdo")
                elif anc == "end":
                    comprobar(xx <= L.W - L.MARGIN_X + 1, f"[{terr}] {nombre}: texto en x={xx} invade el margen derecho")
            pies = [e for e in textos if e.text == mc["nombre"] and float(e.get("y")) > 900]
            if es_div or es_portada:
                comprobar(not pies, f"[{terr}] {nombre}: divisores y portada no llevan pie")
            else:
                comprobar(bool(pies), f"[{terr}] {nombre}: falta el pie con el wordmark")
        titulos_largos = [a for a in g.est.avisos if "ocupa" in a and "líneas" in a]
        comprobar(not titulos_largos, f"[{terr}] títulos de más de 2 líneas: {titulos_largos}")
    print(f"ok  {terr:12} 16 láminas")

if fallos:
    print(f"\n{len(fallos)} fallo(s)")
    sys.exit(1)
print("\ntodas las comprobaciones pasan")
