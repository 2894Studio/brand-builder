#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Post «principal atributo: cerca de ti» con un mapa de puntos de geografía real (1080×1440).

Muestra una zona (anillo con radio en kilómetros reales), marcadores en ciudades reales dentro del radio, una persona destacada
con su distancia verdadera y una tarjeta de cristal con la cifra. Misma composición que el post de mapa que mejor ha funcionado.

Antes, una vez, en tu carpeta de trabajo:  npm i world-atlas topojson-client d3-geo   (necesita Node)
Uso:  python3 post_mapa.py marca.json --salida lanzamiento/post-2-atributo.html --titular "Profesionales de IA <b>cerca de ti.</b>" \\
        --centro "Madrid|-3.70,40.42" --bbox "-10.5,35.3,7,46.8" --radio 200 \\
        --puntos "Toledo|-4.02,39.86;Guadalajara|-3.17,40.63;Segovia|-4.12,40.95;Ávila|-4.70,40.66" \\
        [--apoyo "Armamos tu equipo con perfiles de tu zona."] [--destacada "Marta|Datos|Toledo"] [--fotos lanzamiento/fotos]
Las ciudades y los perfiles son tuyos: si son de ejemplo, anótalo en el LEEME.md. La distancia de la persona destacada se calcula
con las coordenadas, no se escribe a mano.
"""
import argparse
import json
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402

MAPA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gusto", "tools", "mapa_puntos.mjs"))


def par(s):
    lo, la = s.split(",")
    return float(lo), float(la)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--titular", required=True)
    ap.add_argument("--apoyo", default="")
    ap.add_argument("--centro", required=True, help='"Nombre|lon,lat"')
    ap.add_argument("--bbox", required=True, help="lonMin,latMin,lonMax,latMax")
    ap.add_argument("--radio", type=float, default=200)
    ap.add_argument("--puntos", required=True, help='"Ciudad|lon,lat;Ciudad|lon,lat"')
    ap.add_argument("--destacada", default="", help='"Nombre|Rol|Ciudad" (la ciudad debe estar en --puntos)')
    ap.add_argument("--tarjeta", default="")
    ap.add_argument("--fotos")
    ap.add_argument("--pie", default="")
    ap.add_argument("--declarar-ia", action="store_true")
    # «--bbox -10.5,…» empieza por «-»: argparse lo tomaría por otra opción; se une con «=»
    av, i = [], 1
    while i < len(sys.argv):
        if sys.argv[i] == '--bbox' and i + 1 < len(sys.argv):
            av.append('--bbox=' + sys.argv[i + 1]); i += 2
        else:
            av.append(sys.argv[i]); i += 1
    a = ap.parse_args(av)

    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    cn, cc = a.centro.split("|")
    centro = par(cc)
    ciudades = []
    for s in a.puntos.split(";"):
        if s.strip():
            n, co = s.split("|")
            ciudades.append((n.strip(), par(co)))
    r = subprocess.run(["node", MAPA, "--bbox", a.bbox, "--centro", cc, "--puntos", ";".join(f"{lo},{la}" for _, (lo, la) in ciudades)], capture_output=True, text=True)
    if r.returncode != 0:
        print("No se pudo generar el mapa:", (r.stderr or r.stdout).strip()[:300])
        print("¿Falta Node o los paquetes? En tu carpeta de trabajo:  npm i world-atlas topojson-client d3-geo")
        return 2
    d = json.loads(r.stdout)
    kpx, (mx, my) = d["kmPx"], d["centro"]
    R1, R2 = a.radio * kpx, a.radio * 2 * 0.8 * kpx
    puntos = []
    for x, y in d["dots"]:
        rr = math.hypot(x - mx, y - my)
        if rr <= R1:
            puntos.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{c["neutro"]}"/>')
        elif rr <= R2:
            puntos.append(f'<circle cx="{x}" cy="{y}" r="3.4" fill="#fff" fill-opacity="{0.62 - 0.2 * (rr - R1) / (R2 - R1):.2f}"/>')
        else:
            puntos.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#fff" fill-opacity=".38"/>')
    dentro = [(n, co, xy) for (n, co), xy in zip(ciudades, d["puntos"]) if L.haversine_km(centro, co) <= a.radio]
    fuera = [n for n, co in ciudades if L.haversine_km(centro, co) > a.radio]
    marcadores = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{c["primario"]}" stroke-width="3"/>' for _, _, (x, y) in dentro)
    # persona destacada
    dest_html, linea = "", ""
    elegidas = L.elegir_fotos(a.fotos) if a.fotos else {}
    declarar = a.declarar_ia and any(v.get("pie") for v in elegidas.values())
    if a.destacada:
        pn, pr, pc = [x.strip() for x in a.destacada.split("|")]
        hit = next(((n, co, xy) for n, co, xy in dentro if n == pc), None)
        if not hit:
            print(f"La ciudad «{pc}» de --destacada no está entre los puntos dentro del radio.")
            return 1
        km = round(L.haversine_km(centro, hit[1]))
        px, py = hit[2][0] - 150, hit[2][1] + 150
        linea = f'<line x1="{hit[2][0]}" y1="{hit[2][1]}" x2="{px}" y2="{py}" stroke="#fff" stroke-width="2.5" stroke-opacity=".85"/>'
        retrato = elegidas.get("retrato")
        img = f'<img src="{L.data_uri(retrato["ruta_3x4"])}" style="width:100%;height:100%;object-fit:cover;object-position:50% 14%">' if retrato and os.path.exists(retrato["ruta_3x4"]) else f'<div style="width:100%;height:100%;display:grid;place-items:center;background:{c["profundo"]};color:#fff;font:700 34px var(--f-titulos)">{L.esc(L.iniciales(pn))}</div>'
        dest_html = (f'<div class="avatar" style="left:{40 + px - 46}px;top:{330 + py - 46}px">{img}</div>'
                     f'<div class="rotulo" style="left:{40 + px + 58}px;top:{330 + py - 34}px"><b>{L.esc(pn)} · {L.esc(pr)}</b>A {km} km de ti</div>')
    t1, t2 = (a.tarjeta.split("|") + [""])[:2] if a.tarjeta else (f"En tu zona ({a.radio:.0f} km)", f"{len(dentro)} perfiles")
    if "invertida" in lg:
        logo = f'<img class="logo" src="{L.data_uri(lg["invertida"])}" alt="{L.esc(nombre)}">'
    else:
        logo = f'<div class="logo-texto">{L.esc(nombre)}</div>'
    pie = " · ".join(x for x in ["Imagen generada con IA" if declarar else "", a.pie] if x)
    mask = "-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 14%,#000 78%,transparent 100%),linear-gradient(to right,#000 0,#000 78%,transparent 100%);-webkit-mask-composite:source-in;mask-composite:intersect"
    svg = (f'<svg width="{d["W"]}" height="{d["H"]}" viewBox="0 0 {d["W"]} {d["H"]}" style="position:absolute;left:40px;top:330px;{mask}">'
           f'<defs><radialGradient id="h"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>'
           f'<circle cx="{mx}" cy="{my}" r="{R1 * 1.25:.0f}" fill="url(#h)" opacity=".5"/>{"".join(puntos)}'
           f'<circle cx="{mx}" cy="{my}" r="{R1:.0f}" fill="none" stroke="#fff" stroke-width="2.5" stroke-opacity=".9"/>'
           f'<circle cx="{mx}" cy="{my}" r="{R2:.0f}" fill="none" stroke="#fff" stroke-width="1.5" stroke-opacity=".35" stroke-dasharray="3 9" stroke-linecap="round"/>'
           f'{linea}{marcadores}<circle cx="{mx}" cy="{my}" r="20" fill="{c["primario"]}" stroke="#fff" stroke-width="6"/><circle cx="{mx}" cy="{my}" r="6" fill="#fff"/></svg>')
    css = L.css_variables(m) + L.css_luz(m) + """
.p{width:1080px;height:1440px;position:relative;overflow:hidden}
.titular{position:absolute;left:70px;top:84px;font-size:100px}.apoyo{position:absolute;left:70px;top:296px;font-size:34px;color:var(--sobre-primario);opacity:.9;margin:0}
.avatar{position:absolute;width:92px;height:92px;border-radius:50%;overflow:hidden;border:4px solid #fff;box-shadow:0 14px 34px rgba(5,15,70,.5)}
.etq{position:absolute;border-radius:99px;background:rgba(10,20,60,.7);border:1.5px solid rgba(255,255,255,.45);padding:8px 18px;font-size:23px;font-weight:600;color:#fff}
.logo{position:absolute;left:70px;bottom:70px;height:66px}.logo-texto{position:absolute;left:70px;bottom:70px;font:700 56px var(--f-titulos);letter-spacing:-.03em}
.cristal b{font-size:50px}
"""
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · principal atributo</title>
<meta name="arquetipo" content="mapa">
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}</style>
<div class="p campo">
<h1 class="titular">{L.con_negrita(a.titular)}</h1>{('<p class="apoyo">' + L.esc(a.apoyo) + '</p>') if a.apoyo else ''}
{svg}
<div class="etq" style="left:{40 + mx - 90:.0f}px;top:{330 + my - R1 - 64:.0f}px">Tu zona · {L.esc(cn)}</div>
<div class="cristal" style="right:56px;top:{330 + my - 180:.0f}px;width:330px"><small>{L.esc(t1)}</small><b>{L.esc(t2)}</b></div>
{dest_html}{logo}{('<div class="pie-ejemplo">' + L.esc(pie) + '</div>') if pie else ''}
</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}  ({len(puntos)} puntos de mapa, {len(dentro)} marcadores dentro de {a.radio:.0f} km)")
    for n in fuera:
        print(f"  aviso «{n}» queda fuera del radio y no se dibuja")
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--marca", a.marca)
    return 0


if __name__ == "__main__":
    sys.exit(main())
