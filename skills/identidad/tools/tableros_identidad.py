#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Tres tableros de identidad (una dirección cada uno) a partir del logo aprobado y de un direcciones.json. Gratis y editable: HTML + PNG.

Uso:  python3 tableros_identidad.py marca.json direcciones.json --salida trabajo/<…>/direcciones [--fotos lanzamiento/fotos]

direcciones.json: lista de 2 a 3 direcciones, cada una distinta de verdad (otra paleta, otra tipografía, otro gráfico firma):
[{"nombre": "Cal y azulejo", "idea": "una frase: qué dirección es",
  "colores": {"primario": "#1F5C99", "profundo": "#1B2430", "acento": "#E8A33D", "fondo": "#F7F3EA", "texto": "#1B2430"},
  "tipografia": {"titulos": "Fraunces", "texto": "Inter"},          (familias de Google Fonts)
  "estilo_imagen": "luz de tarde, azulejo, personas reales en la calle",
  "firma": "horizonte|puntos|diagonal|ondas",                        (gráfico firma que se repite)
  "imagen": "foto|firma",                                            (qué ocupa la tarjeta grande: foto de fotos/ o el gráfico firma; por defecto foto si hay)
  "frase": "una frase con la voz de la marca (≤ 8 palabras)",
  "radio": 30}]                                                      (esquinas: 8 = sobrio, 30 = cercano)
La dirección sale del **análisis del logo hecho por el modelo** (letras, construcción, color, acabado) y de la estrategia; lo que dibuje un tablero
son decisiones, no medidas: los colores se comprueban con contraste.py antes de pasarlos a marca.json.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "skills", "lanzamiento", "tools"))
import lib_lanzamiento as L  # noqa: E402
CRITICO = os.path.join(RAIZ, "skills", "gusto", "tools", "critico_render.py")


def firma_svg(tipo, color, w=420, h=300):
    if tipo == "puntos":
        pts = "".join(f'<circle cx="{14 + x * 28}" cy="{14 + y * 28}" r="5" fill="{color}"/>' for x in range(15) for y in range(11))
        return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{pts}</svg>'
    if tipo == "diagonal":
        ls = "".join(f'<line x1="{i * 30 - 100}" y1="{h}" x2="{i * 30 + 100}" y2="0" stroke="{color}" stroke-width="8"/>' for i in range(0, 22))
        return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{ls}</svg>'
    if tipo == "ondas":
        o = "".join(f'<path d="M0 {20 + k * 34} q35 -24 70 0 t70 0 t70 0 t70 0 t70 0 t70 0 t70 0" fill="none" stroke="{color}" stroke-width="6"/>' for k in range(8))
        return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{o}</svg>'
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path d="M110 210a100 100 0 0 1 200 0z" fill="{color}"/>'
            f'<rect x="40" y="210" width="340" height="8" fill="{color}"/>'
            + "".join(f'<rect x="{40 + k * 34}" y="{236 + (k % 2) * 4}" width="22" height="6" fill="{color}" opacity=".55"/>' for k in range(10)) + '</svg>')


def tablero(m, lg, d, idx, fotos):
    nombre = m.get("nombre", "Marca")
    c = d["colores"]
    ft = d.get("tipografia", {}).get("titulos", "Inter")
    fx = d.get("tipografia", {}).get("texto", "Inter")
    r = int(d.get("radio", 24))
    fam = "&".join("family=" + urllib.parse.quote(f) + ":wght@400;600;700;800" for f in dict.fromkeys([ft, fx]))
    fuente = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fam}&display=swap">'
    sobre_p = L.legible(c["primario"])
    logo_blanco = lg.get("invertida")
    logo_color = lg.get("principal")
    def logo_en(bg):
        use = logo_blanco if (L.luminancia(bg) < 0.3 and logo_blanco) else (logo_color or logo_blanco)
        if use:
            return f'<img src="{L.data_uri(use)}" style="max-width:70%;max-height:44%" alt="{L.esc(nombre)}">'
        return f'<div style="font:800 110px var(--ft);color:{L.legible(bg)}">{L.esc(nombre)}</div>'
    pal = [("primario", "Primario"), ("profundo", "Profundo"), ("acento", "Acento"), ("fondo", "Fondo"), ("texto", "Texto")]
    sw = "".join(f'<div style="background:{c[k]};color:{L.legible(c[k])};{"border:2px solid #D5D9E0;" if L.luminancia(c[k]) > .85 else ""}"><span>{n}</span><span>{c[k]}</span></div>' for k, n in pal)
    aviso_acento = L.contraste(c["acento"], c["fondo"]) < 3
    img = ""
    if fotos and fotos.get("retrato") and d.get("imagen", "foto") != "firma":
        img = f'<img src="{L.data_uri(fotos["retrato"]["ruta_3x4"])}" style="width:100%;height:100%;object-fit:cover">'
    else:
        img = f'<div style="position:absolute;inset:0;display:grid;place-items:center;background:{c["profundo"]}">{firma_svg(d.get("firma", "horizonte"), c["acento"])}</div>'
    css = f"""
:root{{--ft:'{ft}',system-ui,sans-serif;--fx:'{fx}',system-ui,sans-serif}}
*{{box-sizing:border-box}}body{{margin:0;font-family:var(--fx)}}
.p{{width:1920px;height:1080px;background:{c['fondo']};color:{c['texto']};padding:36px;display:grid;gap:16px;
grid-template-columns:repeat(12,minmax(0,1fr));grid-template-rows:repeat(6,minmax(0,1fr));
grid-template-areas:"L L L L L P P P I I I I" "L L L L L P P P I I I I" "L L L L L T T T I I I I" "A A A A S S S S I I I I" "A A A A S S S S Q Q Q Q" "A A A A S S S S Q Q Q Q"}}
.t{{border-radius:{r}px;position:relative;overflow:hidden;padding:28px}}
.pill{{position:absolute;left:22px;top:20px;font:700 19px var(--fx);letter-spacing:.06em;text-transform:uppercase;background:rgba(255,255,255,.9);color:#12141A;padding:6px 16px;border-radius:99px;z-index:3}}
.L{{grid-area:L;background:{c['primario']};color:{sobre_p};display:flex;align-items:center;justify-content:center}}
.P{{grid-area:P;background:#fff;display:flex;flex-direction:column;justify-content:flex-end}}
.P h2{{margin:0;font:800 46px/1.05 var(--ft);letter-spacing:-.03em}}.P p{{margin:10px 0 0;font:500 24px/1.3 var(--fx);color:#3D4452}}
.T{{grid-area:T;background:{c['profundo']};color:{L.legible(c['profundo'])};display:flex;align-items:flex-end;gap:24px;padding:62px 28px 16px}}
.T .aa{{font:800 74px/1 var(--ft);letter-spacing:-.05em}}.T div span{{display:block;font:600 24px/1.3 var(--fx)}}
.A{{grid-area:A;background:#fff}}.sw{{position:absolute;left:24px;right:24px;top:68px;bottom:24px;display:grid;grid-template-rows:repeat(5,minmax(0,1fr));gap:10px}}
.sw div{{border-radius:{max(r - 8, 8)}px;padding:0 18px;display:flex;justify-content:space-between;align-items:center;font:700 22px var(--fx)}}
.S{{grid-area:S;background:{c['acento']};color:{L.legible(c['acento'])}}}
.S .tarjeta{{position:absolute;left:30px;top:80px;width:360px;height:210px;background:{c['primario']};color:{sobre_p};border-radius:{max(r - 10, 6)}px;padding:22px;box-shadow:0 14px 30px rgba(0,0,0,.25)}}
.S .tarjeta b{{display:block;font:800 36px/1.2 var(--ft);letter-spacing:-.03em;margin-bottom:10px}}.S .tarjeta span{{display:block;font:500 20px/1.3 var(--fx)}}
.S .post{{position:absolute;right:30px;top:60px;width:230px;height:290px;background:{c['profundo']};color:{L.legible(c['profundo'])};border-radius:{max(r - 10, 6)}px;padding:20px;display:flex;flex-direction:column;justify-content:flex-end;transform:rotate(3deg);box-shadow:0 14px 30px rgba(0,0,0,.25)}}
.S .post i{{display:block;width:44px;height:5px;background:{c['acento']};margin-bottom:12px}}.S .post b{{font:700 28px/1.1 var(--ft);letter-spacing:-.03em}}
.S .estilo{{position:absolute;left:30px;bottom:26px;right:30px;font:600 23px/1.3 var(--fx)}}
.I{{grid-area:I;padding:0;background:{c['profundo']}}}
.Q{{grid-area:Q;background:{c['texto']};color:{L.legible(c['texto'])};display:flex;flex-direction:column;justify-content:flex-end}}
.Q b{{font:800 34px/1.1 var(--ft);letter-spacing:-.03em}}.Q span{{font:500 22px/1.3 var(--fx);opacity:.9;margin-top:6px}}
"""
    return f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · dirección {idx}</title>{fuente}<style>{css}</style>
<div class="p"><div class="t L"><span class="pill">Dirección {idx}</span>{logo_en(c['primario'])}</div>
<div class="t P"><span class="pill">Idea</span><h2>{L.esc(d['nombre'])}</h2><p>{L.esc(d.get('idea', ''))}</p></div>
<div class="t T"><span class="pill">Tipografía</span><div class="aa">Aa</div><div><span>{L.esc(ft)} · títulos</span><span>{L.esc(fx)} · texto</span></div></div>
<div class="t A"><span class="pill">Color</span><div class="sw">{sw}</div></div>
<div class="t S"><span class="pill">Aplicaciones</span><div class="tarjeta"><b>{L.esc(nombre)}</b><span>{L.esc(d.get('frase', ''))}</span></div>
<div class="post"><i></i><b>{L.esc(d.get('frase', nombre))}</b></div><div class="estilo">{L.esc(d.get('estilo_imagen', ''))}</div></div>
<div class="t I"><span class="pill">{'Fotografía' if fotos and fotos.get('retrato') and d.get('imagen', 'foto') != 'firma' else 'Gráfico firma'}</span>{img}</div>
<div class="t Q"><span class="pill">Voz</span><b>{L.esc(d.get('frase', ''))}</b><span>{'Acento sin contraste suficiente para texto: solo detalles grandes' if aviso_acento else 'Acento apto para titulares grandes'}</span></div></div></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("marca")
    ap.add_argument("direcciones")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--fotos")
    a = ap.parse_args()
    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    lg = L.logos(m, base)
    ds = json.load(open(a.direcciones, encoding="utf-8"))
    if not 2 <= len(ds) <= 3:
        sys.exit("direcciones.json necesita de 2 a 3 direcciones")
    for i, d in enumerate(ds, 1):
        faltan = [k for k in ("primario", "profundo", "acento", "fondo", "texto") if k not in d.get("colores", {})]
        if faltan:
            sys.exit(f"dirección {i}: faltan colores {faltan}")
    pals = {tuple(sorted(d["colores"].items())) for d in ds}
    tipos = {(d.get("tipografia", {}).get("titulos"), d.get("firma")) for d in ds}
    if len(pals) < len(ds) or len(tipos) < len(ds):
        print("  aviso las direcciones se parecen: cambia la paleta, la tipografía de títulos o el gráfico firma para que sean opciones de verdad")
    fotos = L.elegir_fotos(a.fotos) if a.fotos else {}
    os.makedirs(a.salida, exist_ok=True)
    for i, d in enumerate(ds, 1):
        h = os.path.join(a.salida, f"direccion-{i}.html")
        open(h, "w", encoding="utf-8").write(tablero(m, lg, d, i, fotos))
        r = subprocess.run([sys.executable, CRITICO, h, "--ancho", "1920", "--alto", "1080", "--png", h.replace(".html", ".png")], capture_output=True, text=True)
        errs = [x.strip() for x in r.stdout.splitlines() if x.strip().startswith("ERROR")]
        print(f"direccion-{i}: {d['nombre']} → {h.replace('.html', '.png')}" + ("" if r.returncode == 2 else f"  ({len(errs)} error(es) del crítico)"))
        for x in errs[:3]:
            print("   ", x)
    print("Siguiente: mirar los tableros, elegir con un diálogo, comprobar el contraste con contraste.py y pasar lo elegido a marca.json.")


if __name__ == "__main__":
    main()
