#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Posts «divertidos y expresivos» (campaña): colores planos y saturados, palabra gigante recortada, foto con marco de sello de
correos, insignia con el símbolo, estrellas y líneas de matasellos. Pensado para marcas con personalidad (viajes, ocio, comida, eventos).

Uso:  python3 post_expresivo.py marca.json --modo gigante|precio --salida lanzamiento/post-1-que-es.html --foto ruta.jpg [opciones]

  --modo gigante   titular a la izquierda, foto en marco de sello abajo, insignia y una palabra enorme recortada en el borde
        --titular "La luz de Sevilla te <b>espera</b>"  --palabra "luz"  [--kicker "Curso de 4 semanas"]
  --modo precio    fondo oscuro con destino/producto, precio enorme con decimales en superíndice, píldora y beneficios
        --destino "Sevilla" --precio "99|90|€" [--etiqueta "Curso de 4 semanas"] [--hashtag "#TuVista"]
        --beneficios "4 semanas;Grupo de 8;Salidas por la calle" [--ejemplo] [--titular "…"]
  --foto ruta      foto o imagen del producto (usa fotos/ ya preparadas: lanzamiento/fotos/*-3x4.jpg); sin foto el marco queda en color
  --ejemplo        el precio es de ejemplo: se escribe «Precio de ejemplo» en la pieza (nada inventado se presenta como real)
Colores: el primario es el campo; el acento, los detalles y la palabra clave; el color profundo o la tinta, el bloque oscuro.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402


def sello_path(w, h, r=8, paso=30):
    """Contorno de sello de correos: rectángulo con muescas semicirculares hacia dentro en los cuatro bordes."""
    nx, ny = max(2, round(w / paso)), max(2, round(h / paso))
    px, py = w / nx, h / ny
    d = ["M0 0"]
    for i in range(nx):                      # borde superior, de izquierda a derecha
        cx = (i + .5) * px
        d.append(f"L{cx - r:.1f} 0 A{r} {r} 0 0 0 {cx + r:.1f} 0")
    d.append(f"L{w} 0")
    for i in range(ny):                      # borde derecho, de arriba abajo
        cy = (i + .5) * py
        d.append(f"L{w} {cy - r:.1f} A{r} {r} 0 0 0 {w} {cy + r:.1f}")
    d.append(f"L{w} {h}")
    for i in range(nx):                      # borde inferior, de derecha a izquierda
        cx = w - (i + .5) * px
        d.append(f"L{cx + r:.1f} {h} A{r} {r} 0 0 0 {cx - r:.1f} {h}")
    d.append(f"L0 {h}")
    for i in range(ny):                      # borde izquierdo, de abajo arriba
        cy = h - (i + .5) * py
        d.append(f"L0 {cy + r:.1f} A{r} {r} 0 0 0 0 {cy - r:.1f}")
    d.append("Z")
    return " ".join(d)


def sello_circular(R, n=16):
    """Contorno de insignia festoneada (círculo con n bultos)."""
    pts = [(R + R * math.cos(2 * math.pi * i / n), R + R * math.sin(2 * math.pi * i / n)) for i in range(n)]
    b = R * math.sin(math.pi / n) * 1.08
    d = [f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"]
    for i in range(1, n + 1):
        x, y = pts[i % n]
        d.append(f"A{b:.1f} {b:.1f} 0 0 1 {x:.1f} {y:.1f}")
    return " ".join(d) + " Z"


def estrellas(color, n=5, s=30):
    def estrella(cx, cy, r):
        p = []
        for k in range(10):
            ang = -math.pi / 2 + k * math.pi / 5
            rr = r if k % 2 == 0 else r * .42
            p.append(f"{cx + rr * math.cos(ang):.1f},{cy + rr * math.sin(ang):.1f}")
        return f'<polygon points="{" ".join(p)}" fill="{color}"/>'
    return f'<svg width="{n * s + 20}" height="{s + 8}" viewBox="0 0 {n * s + 20} {s + 8}" aria-hidden="true">' + "".join(
        estrella(s / 2 + i * s + 6, s / 2 + 4, (s / 2 - 1) * (1.2 if i == n // 2 else 1)) for i in range(n)) + "</svg>"


def matasellos(color, w=300):
    ondas = "".join(f'<path d="M0 {10 + k * 16} q{w / 8} -9 {w / 4} 0 t{w / 4} 0 t{w / 4} 0 t{w / 4} 0" fill="none" stroke="{color}" stroke-width="2"/>' for k in range(4))
    return f'<svg width="{w}" height="72" viewBox="0 0 {w} 72" aria-hidden="true">{ondas}</svg>'


def flecha(color):
    return f'<svg width="30" height="22" viewBox="0 0 30 22" aria-hidden="true"><path d="M2 11h24M17 3l9 8-9 8" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("marca")
    ap.add_argument("--modo", choices=["gigante", "precio"], required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--foto")
    ap.add_argument("--titular", default="")
    ap.add_argument("--palabra", default="")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--destino", default="")
    ap.add_argument("--precio", default="")
    ap.add_argument("--etiqueta", default="")
    ap.add_argument("--hashtag", default="")
    ap.add_argument("--beneficios", default="")
    ap.add_argument("--ejemplo", action="store_true")
    ap.add_argument("--pie", default="")
    a = ap.parse_args()

    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    prim, acento, oscuro = c["primario"], c["acento"], c["texto"]
    sobre_prim = L.legible(prim)
    ac_prim = acento if L.contraste(acento, prim) >= 3 else sobre_prim      # acento para texto sobre el campo primario
    ac_osc = acento if L.contraste(acento, oscuro) >= 3 else "#FFFFFF"      # acento para texto sobre el bloque oscuro
    foto = a.foto if a.foto and os.path.exists(a.foto) else None
    uri = L.data_uri(foto) if foto else ""
    simbolo = f'<img src="{L.data_uri(lg["simbolo"])}" alt="" style="width:62%;height:62%;object-fit:contain">' if "simbolo" in lg else \
        f'<span style="font:800 78px var(--f-titulos);color:{prim}">{L.esc(nombre[:1].upper())}</span>'
    css = L.css_variables(m) + f"""
.p{{width:1080px;height:1440px;position:relative;overflow:hidden}}
.sello{{position:absolute;background:{acento};filter:drop-shadow(0 14px 24px rgba(0,0,0,.25))}}
.sello .in{{position:absolute;inset:20px;background:#ddd center/cover no-repeat}}
.ins{{position:absolute;width:210px;height:210px;transform:rotate(-12deg);filter:drop-shadow(0 10px 18px rgba(0,0,0,.25))}}
.ins>div{{width:100%;height:100%;background:{c['fondo']};display:grid;place-items:center;box-shadow:inset 0 0 0 10px {acento}}}
.dash{{width:60px;height:5px;background:{acento};margin-bottom:26px}}
.tit{{margin:0;font:300 84px/1.04 var(--f-titulos);letter-spacing:-.035em}}.tit b{{font-weight:800;color:{ac_prim if a.modo == 'gigante' else ac_osc}}}
.kick{{font:700 26px var(--f-texto);letter-spacing:.1em;text-transform:uppercase;margin-bottom:22px}}
.logo{{position:absolute;left:70px;bottom:62px;height:62px;z-index:3}}.logo-texto{{position:absolute;left:70px;bottom:62px;font:700 52px var(--f-titulos);letter-spacing:-.03em;z-index:3}}
.ej{{position:absolute;right:70px;bottom:70px;font:600 20px var(--f-texto);z-index:3}}
"""
    logo_c = L.logo_html(m, lg, "oscuro", nombre)
    if a.modo == "gigante":
        palabra = (a.palabra or nombre).lower()
        W, H = 560, 560
        css += f"""
.p{{background:{prim};color:{sobre_prim}}}
.gig{{position:absolute;right:-60px;top:-30px;writing-mode:vertical-rl;transform:rotate(180deg);font:900 700px/.8 var(--f-titulos);letter-spacing:-.06em;color:{c['fondo']};white-space:nowrap}}
.txt{{position:absolute;left:70px;top:160px;width:500px}}
.sello.f{{left:70px;top:690px;width:{W}px;height:{H}px;transform:rotate(-4deg);clip-path:path('{sello_path(W, H)}')}}
.ins.i{{left:470px;top:60px}}
.est{{position:absolute;left:70px;top:70px}}
.mat{{position:absolute;left:640px;top:880px;opacity:.55}}
"""
        cuerpo = (f'<div class="est">{estrellas(acento)}</div><div class="gig" data-bleed="1" data-decorativo="1" aria-hidden="true">{L.esc(palabra)}</div>'
                  f'<div class="txt"><div class="dash"></div>' + (f'<div class="kick">{L.esc(a.kicker)}</div>' if a.kicker else "") +
                  f'<h1 class="tit">{L.con_negrita(a.titular)}</h1></div>'
                  f'<div class="sello f"><div class="in" style="background-image:url({uri})"></div></div>'
                  f'<div class="ins i" style="clip-path:path(\'{sello_circular(105)}\')"><div>{simbolo}</div></div>'
                  f'<div class="mat">{matasellos(L.legible(prim))}</div>' + logo_c)
    else:
        if "|" not in a.precio:
            sys.exit('--modo precio necesita --precio "entero|decimales|moneda" (p. ej. "99|90|€")')
        pe = (a.precio.split("|") + ["", ""])[:3]
        bens = [x.strip() for x in a.beneficios.split(";") if x.strip()][:4]
        W, H = 400, 470
        css += f"""
.p{{background:{oscuro};color:#FFFFFF}}
.hash{{position:absolute;left:70px;top:90px;font:500 40px var(--f-titulos);letter-spacing:-.02em}}
.dest{{position:absolute;left:70px;top:140px;font:800 170px/1 var(--f-titulos);letter-spacing:-.05em;color:{prim if L.contraste(prim, oscuro) >= 3 else ac_osc}}}
.pr{{position:absolute;left:70px;top:350px;display:flex;align-items:flex-start;gap:10px}}
.pr .mon{{font:700 54px var(--f-titulos);color:{ac_osc};margin-top:30px}}
.pr .ent{{font:800 330px/.9 var(--f-titulos);letter-spacing:-.07em}}
.pr .dec{{font:800 120px/1 var(--f-titulos);letter-spacing:-.04em;margin-top:34px}}
.pil{{position:absolute;left:70px;top:700px;border:3px solid {ac_osc};color:{ac_osc};border-radius:20px;padding:12px 30px;font:700 34px var(--f-texto)}}
.sello.f{{left:70px;top:820px;width:{W}px;height:{H}px;transform:rotate(-3deg);clip-path:path('{sello_path(W, H)}')}}
.ben{{position:absolute;left:520px;top:850px;width:490px}}.ben h3{{margin:0 0 22px;font:700 32px var(--f-texto)}}
.ben div{{display:flex;gap:16px;align-items:center;margin-bottom:20px;font:500 34px/1.15 var(--f-texto)}}
.ins.i{{left:790px;top:80px;width:190px;height:190px}}
"""
        ejem = '<div class="ej" style="color:#C9D0D9">Precio de ejemplo</div>' if a.ejemplo else ""
        cuerpo = ((f'<div class="hash">{L.esc(a.hashtag)}</div>' if a.hashtag else "") + f'<div class="dest">{L.esc(a.destino)}</div>'
                  f'<div class="pr"><span class="mon">{L.esc(pe[2])}</span><span class="ent">{L.esc(pe[0])}</span><span class="dec">,{L.esc(pe[1])}</span></div>' +
                  (f'<div class="pil">{L.esc(a.etiqueta)}</div>' if a.etiqueta else "") +
                  f'<div class="sello f"><div class="in" style="background-image:url({uri})"></div></div>'
                  f'<div class="ins i" style="clip-path:path(\'{sello_circular(95)}\')"><div>{simbolo}</div></div>' +
                  (f'<div class="ben"><h3>{L.esc(a.titular or "Incluye:")}</h3>' + "".join(f'<div>{flecha(ac_osc)}<span>{L.esc(b)}</span></div>' for b in bens) + "</div>" if bens else "") +
                  logo_c + ejem)
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · post expresivo</title>
<meta name="arquetipo" content="expresivo:{a.modo}">
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}</style>
<div class="p">{cuerpo}</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}")
    if not foto:
        print("  aviso sin foto: el marco del sello queda en gris; pasa --foto")
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--marca", a.marca)


if __name__ == "__main__":
    main()
