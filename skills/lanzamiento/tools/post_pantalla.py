#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Post «qué es la marca» con una ventana de escritorio (web, plataforma, panel) en vez de un teléfono (1080×1440).

Para productos web, plataformas, formación o servicios donde el móvil no es el soporte principal. Opcionalmente muestra un
bloque de código (`--codigo`) para marcas técnicas. Lo que sale en la ventana es del cliente: datos reales o plausibles,
anotados en el LEEME.md.

Uso:  python3 post_pantalla.py marca.json --salida lanzamiento/post-1-que-es.html --titular "Formación <b>Full Stack</b>, en grupos de 5." \\
        --ventana "fullstacker.com|Tu cohorte" --menu "Inicio;Clases;Proyectos;Equipo" --activo 2 --cifra "10 €|al mes" \\
        --filas "Frontend|React y Tailwind;Backend|Node y APIs" --estado "En vivo" --tarjeta "Grupos|5 alumnos" [--tema claro|oscuro]
      o con código:  --codigo "const grupo = 5;;await clase.empezar(grupo);"   (cada línea separada por «;», máximo 7)
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--titular", required=True)
    ap.add_argument("--ventana", default="tu-marca.com|Panel")
    ap.add_argument("--menu", default="Inicio;Proyectos;Equipo")
    ap.add_argument("--activo", type=int, default=1, help="posición (desde 1) del elemento de menú activo")
    ap.add_argument("--cifra", default="")
    ap.add_argument("--filas", default="")
    ap.add_argument("--estado", default="")
    ap.add_argument("--codigo", default="")
    ap.add_argument("--tarjeta", default="")
    ap.add_argument("--tema", choices=["oscuro", "claro"], default="oscuro")
    ap.add_argument("--pie", default="")
    a = ap.parse_args()
    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    dom, titulo = (a.ventana.split("|") + [""])[:2]
    menu = [x.strip() for x in a.menu.split(";") if x.strip()][:5]
    filas = [(x.split("|") + [""])[:2] for x in a.filas.split(";") if x.strip()][:3]
    cif = (a.cifra.split("|") + [""])[:2] if a.cifra else None
    avisos = []
    if a.estado and len(a.estado) > 14:
        avisos.append(f"el estado «{a.estado}» es largo: usa 14 caracteres o menos")
    lineas = [x for x in a.codigo.split(";") if x.strip()][:7] if a.codigo else []
    for ln in lineas:
        if len(ln) > 38:
            avisos.append(f"la línea de código «{ln[:20]}…» tiene {len(ln)} caracteres: se saldría de la ventana (máximo 38)")
    avatar = L.base_avatar(c["primario"])
    # alto de la ventana según el contenido, y todo el bloque (ventana + titular) centrado en la pieza
    contenido = 62 + 60 + 56 + (100 if cif else 10) + ((len(lineas) * 36 + 56) if lineas else len(filas) * 92) + 50
    alto = max(560, min(760, contenido))
    sup = max(110, (1190 - (alto + 80 + 190)) // 2 + 90)
    menu_html = "".join(f'<div class="mi{" on" if i + 1 == a.activo else ""}">{L.esc(x)}</div>' for i, x in enumerate(menu))
    if lineas:
        cuerpo = '<div class="codigo">' + "".join(f'<div><i>{i + 1}</i>{L.esc(ln)}</div>' for i, ln in enumerate(lineas)) + "</div>"
    else:
        cuerpo = "".join(
            f'<div class="fila"><div class="av">{L.esc(L.iniciales(r))}</div><div><b>{L.esc(r)}</b><span>{L.esc(d)}</span></div>'
            + (f'<span class="chip">{L.esc(a.estado)}</span>' if a.estado else "") + "</div>" for r, d in filas)
    ct, cf = c["texto"], c["fondo"]
    tarjeta = ""
    if a.tarjeta:
        t1, t2 = (a.tarjeta.split("|") + [""])[:2]
        tarjeta = f'<div class="cristal" style="right:30px;top:{sup - 56}px;width:300px;background:{ct};border-color:{ct};color:{cf}"><small>{L.esc(t1)}</small><b>{L.esc(t2)}</b></div>'
    logo = L.logo_html(m, lg, a.tema, nombre)
    css = L.css_variables(m) + L.css_luz(m) + """
.p{width:1080px;height:1440px;position:relative;overflow:hidden}
.titular{position:absolute;left:70px;right:70px;top:TTOPpx;font-size:84px}
.ventana{position:absolute;left:70px;top:WTOPpx;width:940px;height:WALTOpx;border-radius:30px;background:#fff;color:#12141A;box-shadow:0 40px 90px rgba(5,15,70,.45);overflow:hidden}
.barra{height:62px;background:#EEF0F4;display:flex;align-items:center;gap:10px;padding:0 24px}.barra i{width:14px;height:14px;border-radius:50%;background:#C9CED8}
.barra span{margin-left:18px;background:#fff;border-radius:99px;padding:6px 20px;font-size:20px;color:#4A5160}
.cuerpo{display:grid;grid-template-columns:230px 1fr;height:calc(100% - 62px)}
.lateral{background:var(--neutro);padding:26px 18px;display:grid;gap:8px;align-content:start}
.mi{font-size:22px;padding:12px 16px;border-radius:14px;color:#2A3040}.mi.on{background:#fff;font-weight:600;color:var(--primario)}
.principal{padding:30px 34px;min-width:0}.tt{font:600 40px/1.1 var(--f-titulos);letter-spacing:-.02em;margin:0 0 6px}
.cf{display:flex;align-items:baseline;gap:12px;margin:12px 0 22px}.cf b{font:600 76px/1 var(--f-titulos);letter-spacing:-.04em;white-space:nowrap}.cf span{font-size:22px;color:var(--suave)}
.fila{display:flex;align-items:center;gap:16px;background:var(--neutro);border-radius:20px;padding:14px 16px;margin-bottom:12px}
.av{flex:none;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;font-weight:600;font-size:19px;color:#fff;background:linear-gradient(135deg,AVATAR,var(--profundo))}
.fila div b{display:block;font-size:22px;font-weight:600}.fila div span{font-size:19px;color:var(--suave)}
.chip{margin-left:auto;font-size:19px;font-weight:600;color:var(--primario);background:#fff;border-radius:99px;padding:6px 14px;white-space:nowrap}
.codigo{background:#0F1424;color:#E6EAF5;border-radius:20px;padding:22px 24px;font:22px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}.codigo i{display:inline-block;width:34px;color:#8A93AD;font-style:normal}
.logo{position:absolute;left:70px;bottom:70px;height:66px}.logo-texto{position:absolute;left:70px;bottom:70px;font:700 56px var(--f-titulos);letter-spacing:-.03em}
.cristal b{font-size:50px}
""".replace("AVATAR", avatar).replace("WTOP", str(sup)).replace("WALTO", str(alto)).replace("TTOP", str(sup + alto + 80))
    pie = a.pie
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · qué es la marca</title>
<meta name="arquetipo" content="ui">
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}{L.tema_css(m, a.tema)}</style>
<div class="p campo"><div class="ventana"><div class="barra"><i></i><i></i><i></i><span>{L.esc(dom)}</span></div>
<div class="cuerpo"><div class="lateral">{menu_html}</div><div class="principal"><p class="tt">{L.esc(titulo)}</p>
{('<div class="cf"><b>' + L.esc(cif[0]) + '</b><span>' + L.esc(cif[1]) + '</span></div>') if cif else ''}{cuerpo}</div></div></div>
{tarjeta}<h1 class="titular">{L.con_negrita(a.titular)}</h1>{logo}{('<div class="pie-ejemplo">' + L.esc(pie) + '</div>') if pie else ''}</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}")
    for x in avisos:
        print("  aviso", x)
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--marca", a.marca)
    return 0


if __name__ == "__main__":
    sys.exit(main())
