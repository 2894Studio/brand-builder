#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Post «qué es la marca» con un teléfono que enseña la interfaz del producto o servicio (1080×1440).

Composición: campo en degradado con luz, anillos redondeados, teléfono con lista de filas, tarjetas de cristal con una cifra,
fotos en tarjetas con borde de cristal (si las hay), desvanecido inferior, titular y logo. Es la composición del post que
mejor ha funcionado; lo que cambia de una marca a otra son los datos, no el diseño.

Uso:  python3 post_telefono.py marca.json --salida lanzamiento/post-1-que-es.html --titular "Equipos de IA <b>completos</b>, listos para trabajar." \\
        --pantalla "Contexto|Título de la pantalla" --cifra "4|perfiles · un solo equipo" \\
        --filas "Datos|Líder de datos;Modelos|Ingeniería de ML;Producto|Responsable;Gobierno|Riesgo y cumplimiento" \\
        --estado "Disponible" --boton "Presentar equipo" --tarjeta-izq "Equipo propuesto|4 perfiles" --tarjeta-der "Dedicación|100 %" \\
        [--fotos lanzamiento/fotos] [--persona "Marta|Líder de datos"] [--pie "texto"] [--declarar-ia]
Lo que la pantalla muestra es del cliente: pon datos reales o plausibles y anótalos en el LEEME.md. Sin fotos, las tarjetas de
foto no se dibujan (no deja marcadores). El texto de la pantalla mide 19 px o más. Revisa con critico_render.py.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402


def partir(s, n=2):
    p = [x.strip() for x in str(s).split("|")]
    return (p + [""] * n)[:n]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--titular", required=True)
    ap.add_argument("--pantalla", default="Propuesta|Equipo propuesto")
    ap.add_argument("--cifra", default="")
    ap.add_argument("--filas", required=True, help='"Rol|detalle;Rol|detalle" (de 3 a 5 filas)')
    ap.add_argument("--estado", default="")
    ap.add_argument("--boton", default="Ver más")
    ap.add_argument("--tarjeta-izq", default="")
    ap.add_argument("--tarjeta-der", default="")
    ap.add_argument("--fotos")
    ap.add_argument("--persona", default="")
    ap.add_argument("--pie", default="")
    ap.add_argument("--declarar-ia", action="store_true")
    ap.add_argument("--tema", choices=["oscuro", "claro"], default="oscuro", help="oscuro: degradado de la marca; claro: fondo de la marca con tarjetas blancas")
    a = ap.parse_args()

    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    ctx, titulo = partir(a.pantalla)
    cifra_n, cifra_t = partir(a.cifra)
    filas = [partir(x, 2) for x in a.filas.split(";") if x.strip()]
    avisos = []
    por_linea = 22 if a.estado else 30   # caracteres que caben por línea en el detalle de una fila
    def alto(f):
        return 40 + 26 * max(1, -(-len(f[1]) // por_linea))
    while len(filas) > 1 and sum(alto(f) + 12 for f in filas) > 430:
        avisos.append(f"la fila «{filas[-1][0]}» no cabe en el teléfono y se quita; acorta los detalles (≤ {por_linea} caracteres) o usa menos filas")
        filas.pop()
    for r, d in filas:
        if len(d) > por_linea * 2:
            avisos.append(f"el detalle de «{r}» tiene {len(d)} caracteres: se verá en 3 líneas o más")
    if a.estado and len(a.estado) > 14:
        avisos.append(f"el estado «{a.estado}» es largo ({len(a.estado)} caracteres) y puede salirse de la fila: usa 14 o menos")
    if len(cifra_n_t := a.cifra.split("|")[0]) > 5 if a.cifra else False:
        avisos.append(f"la cifra «{cifra_n_t}» es larga para el tamaño grande: usa 5 caracteres o menos")
    avatar = L.base_avatar(c["primario"])
    chip_fg = c["primario"] if L.contraste(c["primario"], c["neutro"]) >= 4.5 else c["texto"]
    elegidas = L.elegir_fotos(a.fotos) if a.fotos else {}
    declarar = a.declarar_ia and any(v.get("pie") for v in elegidas.values())

    def src(tipo, fmt):
        v = elegidas.get(tipo)
        r = v and v.get(f"ruta_{fmt}")
        return L.data_uri(r) if r and os.path.exists(r) else None

    retrato, equipo = src("retrato", "3x4"), src("equipo", "4x3")
    pn, pr = partir(a.persona) if a.persona else ("", "")

    filas_html = "".join(
        f'<div class="fila"><div class="av">{L.esc(L.iniciales(r))}</div><div><b>{L.esc(r)}</b><span>{L.esc(d)}</span></div>'
        + (f'<span class="chip">{L.esc(a.estado)}</span>' if a.estado else "") + "</div>" for r, d in filas)
    izq = partir(a.tarjeta_izq)
    der = partir(a.tarjeta_der)
    tarjetas = ""
    if a.tarjeta_izq:
        tarjetas += f'<div class="cristal" style="left:30px;top:215px;width:272px"><small>{L.esc(izq[0])}</small><b>{L.esc(izq[1])}</b></div>'
    if a.tarjeta_der:
        tarjetas += f'<div class="cristal" style="right:30px;top:430px;width:272px"><small>{L.esc(der[0])}</small><b>{L.esc(der[1])}</b></div>'
    fotos_html = ""
    if retrato:
        rot = f'<div class="rotulo" style="left:14px;right:14px;bottom:14px;padding:10px 14px"><b>{L.esc(pn)}</b>{L.esc(pr)}</div>' if pn else ""
        fotos_html += f'<div class="foto" style="left:40px;top:395px;width:290px;height:420px"><img src="{retrato}" style="object-position:50% 14%">{rot}</div>'
    if equipo:
        fotos_html += f'<div class="foto" style="left:792px;top:610px;width:252px;height:230px"><img src="{equipo}" style="object-position:50% 38%"></div>'
    logo = L.logo_html(m, lg, a.tema, nombre)
    pie = " · ".join(x for x in ["Imagen generada con IA" if declarar else "", a.pie] if x)
    css = L.css_variables(m) + L.css_luz(m) + """
.p{width:1080px;height:1440px;position:relative;overflow:hidden}
.anillo{position:absolute;left:50%;border:2px solid rgba(255,255,255,.22);border-radius:240px}
.telefono{left:50%;top:60px;width:470px;height:930px;margin-left:-235px}
.isla{position:absolute;left:50%;top:14px;width:130px;height:36px;margin-left:-65px;background:#07090F;border-radius:20px}
.hora{display:flex;justify-content:space-between;font-size:19px;font-weight:600;margin:0 6px 46px}
.ctx{font-size:20px;color:var(--suave);margin:0}.tit{font:600 38px/1.1 var(--f-titulos);letter-spacing:-.02em;margin:4px 0 2px}
.cifra{display:flex;flex-wrap:nowrap;align-items:baseline;gap:10px;margin:18px 0 20px}.cifra b{font:600 84px/1 var(--f-titulos);letter-spacing:-.04em;white-space:nowrap}.cifra span{font-size:22px;color:var(--suave)}
.fila{display:flex;align-items:center;gap:16px;background:var(--neutro);border-radius:22px;padding:14px 16px;margin-bottom:12px}
.av{flex:none;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;font-weight:600;font-size:19px;color:#fff;background:linear-gradient(135deg,AVATAR,var(--profundo))}
.fila div b{display:block;font-size:22px;font-weight:600}.fila div span{font-size:19px;color:var(--suave)}
.chip{margin-left:auto;font-size:19px;font-weight:600;color:CHIP;background:#fff;border-radius:99px;padding:6px 12px;white-space:nowrap}
.pantalla{display:flex;flex-direction:column}.boton{margin-top:auto;margin-bottom:8px;background:linear-gradient(135deg,var(--primario),var(--profundo));color:#fff;border-radius:24px;padding:20px;text-align:center;font-size:22px;font-weight:600}
.desvanecido{position:absolute;left:0;right:0;bottom:0;height:560px;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,var(--profundo) 100%);opacity:.95}
.titular{position:absolute;left:70px;right:70px;bottom:200px;font-size:84px}
.logo{position:absolute;left:70px;bottom:70px;height:66px}.logo-texto{position:absolute;left:70px;bottom:70px;font:700 56px var(--f-titulos);letter-spacing:-.03em}
.cristal b{font-size:50px}
""".replace("AVATAR", avatar).replace("CHIP", chip_fg)
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · qué es la marca</title>
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}{L.tema_css(m, a.tema)}</style>
<div class="p campo">
<div class="anillo" style="width:660px;height:1000px;margin-left:-330px;top:240px"></div><div class="anillo" style="width:800px;height:1100px;margin-left:-400px;top:190px;border-color:rgba(255,255,255,.12)"></div>
<div class="telefono"><div class="pantalla"><div class="isla"></div>
<div class="hora"><span>9:41</span><span aria-hidden="true">●●●</span></div>
<p class="ctx">{L.esc(ctx)}</p><p class="tit">{L.esc(titulo)}</p>
{('<div class="cifra"><b>' + L.esc(cifra_n) + '</b><span>' + L.esc(cifra_t) + '</span></div>') if cifra_n else '<div style="height:18px"></div>'}
{filas_html}
<div class="boton">{L.esc(a.boton)}</div></div></div>
{tarjetas}{fotos_html}
<div class="desvanecido"></div>
<h1 class="titular">{L.con_negrita(a.titular)}</h1>
{logo}
{('<div class="pie-ejemplo">' + L.esc(pie) + '</div>') if pie else ''}
</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}")
    if not (retrato or equipo):
        print("  aviso sin fotos: el post va sin tarjetas de foto (no se dejan marcadores)")
    for x in avisos:
        print("  aviso", x)
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--marca", a.marca)


if __name__ == "__main__":
    main()
