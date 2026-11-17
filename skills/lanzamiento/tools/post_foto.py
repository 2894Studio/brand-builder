#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Post con la fotografía como protagonista: foto a sangre arriba y bloque opaco abajo con el titular (nunca texto sobre la imagen).

Uso:  python3 post_foto.py marca.json --salida lanzamiento/post-1-que-es.html --titular "Frase con <b>palabra clave</b>." \\
        --fotos lanzamiento/fotos [--cual retrato|equipo|producto|local] | --foto ruta.jpg \\
        [--tarjeta "Etiqueta|Valor"] [--notas "62,38|Gira el móvil dos grados;30,70|Baja la exposición"] [--tema claro|oscuro] [--pie "…"]
  --notas   hasta 3 anotaciones sobre la foto: «x,y» en % del ancho y alto de la foto y el texto; sale un punto numerado y una nota opaca
            (útil para enseñar corrección, detalle o proceso sobre la propia foto)
  --tema    oscuro: bloque inferior del color profundo de la marca; claro: bloque con el fondo de la marca
Sin foto no hay post: el script se niega (para eso están post_pantalla, post_telefono o post_comparativa).
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("marca")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--titular", required=True)
    ap.add_argument("--foto")
    ap.add_argument("--fotos")
    ap.add_argument("--cual", choices=["equipo", "retrato", "producto", "local"])
    ap.add_argument("--tarjeta", default="")
    ap.add_argument("--notas", default="")
    ap.add_argument("--tema", choices=["oscuro", "claro"], default="oscuro")
    ap.add_argument("--pie", default="")
    ap.add_argument("--declarar-ia", action="store_true")
    a = ap.parse_args()

    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    ruta, ia_pie = a.foto, None
    if not ruta and a.fotos:
        el = L.elegir_fotos(a.fotos)
        orden = [a.cual] if a.cual else ["retrato", "equipo", "producto", "local"]
        for t in orden:
            if t in el:
                ruta = el[t]["ruta_4x3"]
                ia_pie = el[t].get("pie") if a.declarar_ia else None
                break
    if not ruta or not os.path.exists(ruta):
        sys.exit("post_foto necesita una foto (--foto ruta o --fotos carpeta con la salida de preparar_fotos.py). Sin foto, usa otro recurso.")
    oscuro = a.tema == "oscuro"
    bloque_bg = "var(--profundo)" if oscuro else c["fondo"]
    bloque_fg = "var(--sobre-profundo)" if oscuro else c["texto"]
    logo = L.logo_html(m, lg, "oscuro" if oscuro else "claro", nombre)
    pie = " · ".join(x for x in [ia_pie or "", a.pie] if x)
    tarjeta = ""
    if a.tarjeta:
        t1, t2 = (a.tarjeta.split("|") + [""])[:2]
        tarjeta = f'<div class="tarj"><small>{L.esc(t1)}</small><b>{L.esc(t2)}</b></div>'
    notas = ""
    for i, n in enumerate([x for x in a.notas.split(";") if x.strip()][:3], 1):
        pos, _, txt = n.partition("|")
        try:
            x, y = [float(v) for v in pos.split(",")]
        except ValueError:
            sys.exit(f"--notas: «{pos}» no es x,y en % (p. ej. 62,38)")
        izq = x > 55
        notas += (f'<div class="pin" style="left:{x}%;top:{y}%"><i>{i}</i></div>'
                  f'<div class="nota" style="top:{y}%;{"right" if izq else "left"}:{(100 - x) + 5 if izq else x + 5}%">{L.esc(txt.strip())}</div>')
    css = L.css_variables(m) + f"""
.p{{width:1080px;height:1440px;position:relative;overflow:hidden;background:{bloque_bg};color:{bloque_fg}}}
.foto-grande{{position:absolute;left:0;top:0;width:1080px;height:880px}}.foto-grande img{{width:100%;height:100%;object-fit:cover;display:block}}
.bloque{{position:absolute;left:0;right:0;top:960px;bottom:0;padding:60px 70px 0}}
.titular{{margin:0;font:600 78px/1.04 var(--f-titulos);letter-spacing:-.035em;color:{bloque_fg}}}.titular b{{font-weight:800}}
.logo{{position:absolute;left:70px;bottom:62px;height:62px}}.logo-texto{{position:absolute;left:70px;bottom:62px;font:700 52px var(--f-titulos);letter-spacing:-.03em}}
.tarj{{position:absolute;right:56px;top:890px;background:#fff;color:#12141A;border-radius:26px;padding:20px 28px;box-shadow:0 18px 44px rgba(10,20,50,.22)}}
.tarj small{{display:block;font-size:22px;font-weight:600;color:#3D4452}}.tarj b{{display:block;font-size:50px;line-height:1.05;letter-spacing:-.03em;font-weight:700}}
.pin{{position:absolute;width:48px;height:48px;margin:-24px 0 0 -24px;border-radius:50%;background:var(--primario);color:{L.legible(c['primario'])};border:4px solid #fff;display:grid;place-items:center;box-shadow:0 8px 24px rgba(0,0,0,.3)}}
.pin i{{font:700 22px var(--f-texto);font-style:normal}}
.nota{{position:absolute;margin-top:-26px;background:#fff;color:#12141A;border-radius:18px;padding:12px 20px;font:600 24px/1.25 var(--f-texto);max-width:340px;box-shadow:0 10px 30px rgba(0,0,0,.25)}}
.pie-ejemplo{{position:absolute;right:70px;bottom:70px;font-size:20px;opacity:.8}}
"""
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · post con foto</title>
<meta name="arquetipo" content="foto">
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}</style>
<div class="p"><div class="foto-grande"><img src="{L.data_uri(ruta)}" alt="">{notas}</div>
<div class="bloque"><h1 class="titular">{L.con_negrita(a.titular)}</h1></div>
{tarjeta}{logo}{('<div class="pie-ejemplo">' + L.esc(pie) + '</div>') if pie else ''}</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}")
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--marca", a.marca)


if __name__ == "__main__":
    main()
