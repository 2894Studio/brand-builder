#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Posts tipográficos, sin fotos ni interfaces: tres composiciones editoriales distintas.

Uso:  python3 post_tipografico.py marca.json --modo cifra|pasos|manifiesto --salida lanzamiento/post-2-atributo.html --titular "…" [opciones]

  --modo cifra        un número gigante con su unidad, su explicación y su fuente
        --cifra "8|alumnos por grupo"  --apoyo "Cada foto tuya, corregida."  [--fuente "…" | --ejemplo]  [--kicker "Grupos reducidos"]
  --modo pasos        un titular y de 3 a 4 pasos numerados con hilo fino (un verbo y su consecuencia por paso)
        --pasos "Sales|con tu móvil por Sevilla;Disparas|con 4 trucos de luz;Recibes|corrección de cada foto"
  --modo manifiesto   una sola frase enorme con la palabra clave en el color de acento y la inicial de la marca a sangre
        --titular "La luz de las seis <b>no espera a nadie.</b>"
  --tema oscuro|claro  oscuro: fondo del color profundo de la marca; claro: fondo de la marca con un bloque de color abajo
  --pie "…"            texto pequeño opcional
Cifra con datos de terceros: lleva fuente o se marca --ejemplo. Una cifra propia de la marca (plazas, años, precio) no necesita fuente.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("marca")
    ap.add_argument("--modo", choices=["cifra", "pasos", "manifiesto"], required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--titular", default="")
    ap.add_argument("--cifra", default="")
    ap.add_argument("--apoyo", default="")
    ap.add_argument("--fuente", default="")
    ap.add_argument("--ejemplo", action="store_true")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--pasos", default="")
    ap.add_argument("--tema", choices=["oscuro", "claro"], default="oscuro")
    ap.add_argument("--pie", default="")
    a = ap.parse_args()

    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    oscuro = a.tema == "oscuro"
    fondo = c["profundo"] if oscuro else c["fondo"]
    texto = L.legible(c["profundo"]) if oscuro else c["texto"]
    acento = c["acento"] if L.contraste(c["acento"], fondo) >= 3 else (c["primario"] if L.contraste(c["primario"], fondo) >= 3 else texto)
    suave = L.suave(texto, fondo)
    logo = L.logo_html(m, lg, "oscuro" if oscuro else "claro", nombre)
    errores = []
    cuerpo = ""
    if a.modo == "cifra":
        if "|" not in a.cifra:
            sys.exit('--modo cifra necesita --cifra "valor|unidad" (p. ej. "8|alumnos por grupo")')
        n, u = a.cifra.split("|", 1)
        fuente = a.fuente or ("Dato de ejemplo" if a.ejemplo else "")
        cuerpo = (f'<div class="kick">{L.esc(a.kicker)}</div>' if a.kicker else "") + \
                 f'<div class="num">{L.esc(n)}</div><div class="uni">{L.esc(u)}</div><div class="hilo"></div>' \
                 f'<p class="apoyo">{L.con_negrita(a.apoyo or a.titular)}</p>' + (f'<div class="fte">{L.esc(fuente)}</div>' if fuente else "")
        if not fuente:
            print("  aviso cifra sin --fuente ni --ejemplo: vale si es un dato propio de la marca (plazas, precio, años); si es de terceros, cita la fuente")
    elif a.modo == "pasos":
        ps = [x.split("|", 1) + [""] for x in a.pasos.split(";") if x.strip()]
        if not 3 <= len(ps) <= 4:
            sys.exit('--modo pasos necesita de 3 a 4 pasos: --pasos "Verbo|consecuencia;Verbo|consecuencia;…"')
        filas = "".join(f'<li><span class="n">{i:02d}</span><div><b>{L.esc(p[0].strip())}</b><span>{L.esc(p[1].strip())}</span></div></li>' for i, p in enumerate(ps, 1))
        cuerpo = (f'<div class="kick">{L.esc(a.kicker)}</div>' if a.kicker else "") + f'<h1 class="tit">{L.con_negrita(a.titular)}</h1><ol class="pasos">{filas}</ol>'
    else:
        ini = nombre[:1].upper() if nombre.isupper() else nombre[:1].lower()
        cuerpo = f'<div class="glifo" data-bleed="1" data-decorativo="1" aria-hidden="true">{L.esc(ini)}</div><h1 class="grande">{L.con_negrita(a.titular)}</h1>'
        if not a.titular:
            sys.exit("--modo manifiesto necesita --titular con la frase")
    bloque_bg, bloque_fg = (c["primario"], L.legible(c["primario"]))
    css = L.css_variables(m) + f"""
.p{{width:1080px;height:1440px;position:relative;overflow:hidden;background:{fondo};color:{texto}}}
.cuerpo{{position:absolute;left:70px;right:70px;top:90px;bottom:{'210px' if oscuro else '400px'};display:flex;flex-direction:column;justify-content:{'flex-end' if a.modo == 'manifiesto' else 'center'}}}
.kick{{font:600 26px var(--f-texto);letter-spacing:.08em;text-transform:uppercase;color:{suave};margin-bottom:28px}}
.num{{font:800 560px/.84 var(--f-titulos);letter-spacing:-.07em;color:{acento};margin-top:20px}}
.uni{{font:600 64px/1.1 var(--f-titulos);letter-spacing:-.03em;margin-top:18px}}
.hilo{{height:3px;background:{suave};opacity:.5;margin:52px 0 40px;width:100%}}
.apoyo{{margin:0;font:500 50px/1.15 var(--f-titulos);letter-spacing:-.025em;max-width:860px}}.apoyo b{{font-weight:800}}
.fte{{margin-top:34px;font:500 22px var(--f-texto);color:{suave}}}
.tit{{margin:0 0 60px;font:700 96px/1.02 var(--f-titulos);letter-spacing:-.04em}}.tit b{{color:{acento}}}
.pasos{{list-style:none;margin:0;padding:0}}.pasos li{{display:flex;gap:34px;align-items:baseline;border-top:2px solid {suave};padding:46px 0}}
.pasos .n{{font:700 60px var(--f-titulos);color:{acento};min-width:92px;letter-spacing:-.03em}}
.pasos b{{display:block;font:700 64px/1.05 var(--f-titulos);letter-spacing:-.03em}}.pasos div span{{display:block;font:500 36px/1.25 var(--f-texto);color:{suave};margin-top:8px}}
.glifo{{position:absolute;right:-120px;bottom:-330px;font:800 1500px/1 var(--f-titulos);letter-spacing:-.08em;color:{L.mezclar(fondo, c['primario'], 0.28)}}}
.grande{{position:relative;margin:0;font:700 124px/1.0 var(--f-titulos);letter-spacing:-.05em;padding-top:0}}.grande b{{color:{acento}}}
.base{{position:absolute;left:0;right:0;bottom:0;height:{'210px' if oscuro else '300px'};background:{'transparent' if oscuro else bloque_bg}}}
.logo{{position:absolute;left:70px;bottom:{'70px' if oscuro else '110px'};height:62px;z-index:2}}.logo-texto{{position:absolute;left:70px;bottom:{'70px' if oscuro else '110px'};font:700 52px var(--f-titulos);letter-spacing:-.03em;color:{texto if oscuro else bloque_fg};z-index:2}}
.pie-ejemplo{{position:absolute;right:70px;bottom:{'78px' if oscuro else '118px'};font-size:20px;color:{suave if oscuro else bloque_fg};z-index:2}}
"""
    logo_final = L.logo_html(m, lg, "oscuro", nombre) if not oscuro else logo   # sobre el bloque de color va el logo invertido
    if not oscuro and "invertida" not in lg:
        logo_final = f'<div class="logo-texto">{L.esc(nombre)}</div>'
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · post tipográfico</title>
<meta name="arquetipo" content="tipografico:{a.modo}">
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}</style>
<div class="p"><div class="cuerpo">{cuerpo}</div><div class="base">{logo_final}{('<div class="pie-ejemplo">' + L.esc(a.pie) + '</div>') if a.pie else ''}</div></div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}")
    for e in errores:
        print("  aviso", e)
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--marca", a.marca)


if __name__ == "__main__":
    main()
