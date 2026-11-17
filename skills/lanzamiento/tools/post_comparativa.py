#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Post «principal atributo» con una comparativa de dos columnas (precio, modelo, plazos…) (1080×1440).

IMPORTANTE: los datos de la otra columna (competencia, «lo de siempre») deben tener **fuente**. Una cifra inventada sobre un
competidor es una afirmación falsa y puede ser publicidad comparativa ilegal. Por eso el script exige `--fuente`; si de verdad
es solo un ejemplo para maquetar, usa `--ejemplo` y la pieza lo escribe junto al dato. No te inventes ni «aproximes» cifras.

Uso:  python3 post_comparativa.py marca.json --salida lanzamiento/post-2-atributo.html --titular "Aprender código <b>sin hipotecarte</b>." \\
        --ellos "Bootcamp tradicional|8.500 €|Horario rígido;40 alumnos por aula" --fuente "Web del bootcamp X, consultada el 12/11/2026" \\
        --nosotros "Fullstacker|10 € / mes|Grupos de 5 alumnos;A tu ritmo" [--insignia "Sin permanencia"] [--tema claro|oscuro]
Formato de cada columna: «Etiqueta|Dato principal|detalle;detalle» (hasta 3 detalles).
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402


def col(s):
    p = [x.strip() for x in s.split("|")]
    p += [""] * (3 - len(p))
    return p[0], p[1], [d.strip() for d in p[2].split(";") if d.strip()][:3]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--titular", required=True)
    ap.add_argument("--ellos", required=True)
    ap.add_argument("--nosotros", required=True)
    ap.add_argument("--fuente", default="")
    ap.add_argument("--ejemplo", action="store_true", help="los datos de «ellos» son de ejemplo (se escribe en la pieza)")
    ap.add_argument("--insignia", default="")
    ap.add_argument("--tema", choices=["oscuro", "claro"], default="oscuro")
    ap.add_argument("--pie", default="")
    a = ap.parse_args()
    if not a.fuente and not a.ejemplo:
        print("Falta --fuente: los datos de la otra columna necesitan una fuente comprobable (o --ejemplo si solo es un ejemplo).\n"
              "No inventes cifras de otras empresas: es una afirmación falsa y puede ser publicidad comparativa ilegal.")
        return 1
    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    e_t, e_v, e_d = col(a.ellos)
    n_t, n_v, n_d = col(a.nosotros)
    logo = L.logo_html(m, lg, a.tema, nombre)
    nota = ("Dato de ejemplo" if a.ejemplo and not a.fuente else "Fuente: " + a.fuente)
    insignia = f'<span class="insignia">{L.esc(a.insignia)}</span>' if a.insignia else ""
    lis = lambda ds: "".join(f"<li>{L.esc(d)}</li>" for d in ds)
    css = L.css_variables(m) + L.css_luz(m) + """
.p{width:1080px;height:1440px;position:relative;overflow:hidden}
.titular{position:absolute;left:70px;right:70px;top:84px;font-size:92px}
.col{position:absolute;left:70px;right:70px;border-radius:32px;padding:34px 40px}
.col .et{font-size:22px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;display:flex;justify-content:space-between;align-items:center}
.col .val{font:600 88px/1.05 var(--f-titulos);letter-spacing:-.04em;margin:14px 0 14px;white-space:nowrap}
.col ul{margin:0;padding:0;list-style:none;display:grid;gap:8px;font-size:26px}.col li:before{content:"–  "}
.ellos{top:520px;background:rgba(255,255,255,.10);border:1.5px solid rgba(255,255,255,.28);color:var(--sobre-primario)}
.nosotros{top:860px;background:#fff;color:#12141A;box-shadow:0 28px 70px rgba(8,25,110,.35)}
.nosotros .et{color:var(--primario)}.nosotros .val{color:var(--primario)}
.insignia{background:var(--acento);color:#12141A;border-radius:99px;padding:6px 16px;font-size:20px;letter-spacing:.04em}
.fuente{position:absolute;left:70px;right:70px;top:1262px;font-size:20px;opacity:.85}
.logo{position:absolute;left:70px;bottom:70px;height:66px}.logo-texto{position:absolute;left:70px;bottom:70px;font:700 56px var(--f-titulos);letter-spacing:-.03em}
"""
    claro = ""
    if a.tema == "claro":
        claro = (f".ellos{{background:{c['neutro']};border:1.5px solid {c['neutro']};color:{c['texto']}}}"
                 f".nosotros{{background:{c['profundo']};color:{L.legible(c['profundo'])};box-shadow:0 24px 60px rgba(20,30,60,.20)}}"
                 f".nosotros .et,.nosotros .val{{color:{L.legible(c['profundo'])}}}")
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · comparativa</title>
<meta name="arquetipo" content="datos">
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}{L.tema_css(m, a.tema)}{claro}</style>
<div class="p campo"><h1 class="titular">{L.con_negrita(a.titular)}</h1>
<div class="col ellos"><div class="et"><span>{L.esc(e_t)}</span></div><div class="val">{L.esc(e_v)}</div><ul>{lis(e_d)}</ul></div>
<div class="col nosotros"><div class="et"><span>{L.esc(n_t)}</span>{insignia}</div><div class="val">{L.esc(n_v)}</div><ul>{lis(n_d)}</ul></div>
<div class="fuente">{L.esc(nota)}</div>{logo}{('<div class="pie-ejemplo">' + L.esc(a.pie) + '</div>') if a.pie else ''}</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}")
    if a.ejemplo and not a.fuente:
        print("  aviso los datos de la otra columna están marcados «de ejemplo»: no los publiques como reales")
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--marca", a.marca)
    return 0


if __name__ == "__main__":
    sys.exit(main())
