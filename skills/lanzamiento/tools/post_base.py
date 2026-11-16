#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Crea el andamio HTML de un post (1080×1440) con los colores, fuentes y logo de la marca y los componentes comunes.

Uso:  python3 post_base.py marca.json --tipo que-es|atributo --salida lanzamiento/post-1.html [--titular "Frase"] [--apoyo "Frase"]

No diseña el post: deja la estructura (campo de color, titular, hueco para el recurso visual y logo; sin pie salvo --pie) y los
componentes CSS listos (.cristal, .foto, .rotulo, .telefono, .pantalla). El recurso visual lo eliges y lo construyes tú con
`references/recursos-visuales.md`. Después: critico_render.py sobre el resultado.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402

TIPOS = {"que-es": "Qué es la marca", "atributo": "Su principal atributo"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--tipo", choices=list(TIPOS), required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--titular", default="")
    ap.add_argument("--apoyo", default="")
    ap.add_argument("--fotos", help="carpeta lanzamiento/fotos (salida de preparar_fotos.py)")
    ap.add_argument("--declarar-ia", action="store_true", help="el pie dice «Imagen generada con IA» si hay fotos de origen ia (por defecto no)")
    ap.add_argument("--pie", default="", help="texto del pie (por defecto no hay pie)")
    a = ap.parse_args()
    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    if "invertida" in lg:
        logo = f'<img class="logo" src="{L.data_uri(lg["invertida"])}" alt="{L.esc(nombre)}">'
    else:
        logo = f'<div class="logo-texto">{L.esc(nombre)}</div>'
    titular = L.esc(a.titular) or "TITULAR: una frase, la mitad en peso ligero y la clave en <b>negrita</b>"
    apoyo = L.esc(a.apoyo)
    elegidas = L.elegir_fotos(a.fotos) if a.fotos else {}
    ia = a.declarar_ia and any(v.get("pie") for v in elegidas.values())
    pie = " · ".join(x for x in ["Imagen generada con IA" if ia else "", a.pie] if x)
    lista = "".join(f"\n    {t}: {os.path.relpath(v['ruta_3x4'], os.path.dirname(os.path.abspath(a.salida)))} (3:4) · {os.path.relpath(v['ruta_4x3'], os.path.dirname(os.path.abspath(a.salida)))} (4:3) · {os.path.relpath(v['ruta_1x1'], os.path.dirname(os.path.abspath(a.salida)))} (1:1)" for t, v in elegidas.items())
    nota_fotos = f"<!-- FOTOS DISPONIBLES (úsalas en el recurso visual con <div class=\"foto\"><img src=\"…\"></div>):{lista}\n  -->" if elegidas else "<!-- Sin fotos: usa un recurso que se sostenga solo (mapa, interfaz, cifra) o marcadores visibles. -->"
    css = L.css_variables(m) + """
.p{width:1080px;height:1440px;position:relative;overflow:hidden;color:var(--sobre-primario)}
.titular{position:absolute;left:70px;right:70px;font-size:100px}
.apoyo{position:absolute;left:70px;right:70px;font-size:34px;font-weight:400;opacity:.92;margin:0}
.logo{position:absolute;left:70px;bottom:70px;height:66px}.logo-texto{position:absolute;left:70px;bottom:70px;font:700 56px var(--f-titulos);letter-spacing:-.03em}
.visual{position:absolute;inset:0}
"""
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · {TIPOS[a.tipo]}</title>
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}</style>
<div class="p campo">
  {nota_fotos}
  <!-- 1) TITULAR (mitad ligero, palabra clave en negrita). Arriba por defecto; si el recurso visual lo pide, abajo. -->
  <h1 class="titular" style="top:90px">{titular}</h1>
  {'<p class="apoyo" style="top:300px">' + apoyo + '</p>' if apoyo else ''}
  <!-- 2) RECURSO VISUAL ({TIPOS[a.tipo]}): ver references/recursos-visuales.md. Colócalo dentro de .visual. -->
  <div class="visual">
    <!-- AQUÍ: teléfono con interfaz / mapa de puntos / cifra con fuente / persona con rol ... -->
  </div>
  <!-- 3) LOGO. Sin pie por defecto: no añadas rótulos ni textos sobre las fotos que no se hayan pedido. -->
  {logo}
  {'<div class="pie-ejemplo">' + L.esc(pie) + '</div>' if pie else ''}
</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}  (tipo: {TIPOS[a.tipo]})")
    if "invertida" not in lg:
        print("  aviso sin logo «invertida»: el pie lleva el nombre en texto")
    print("Siguiente: construir el recurso visual y pasar skills/gusto/tools/critico_render.py", a.salida, "--marca", a.marca)


if __name__ == "__main__":
    main()
