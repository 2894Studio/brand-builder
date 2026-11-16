#!/usr/bin/env python3
"""Hace que un logo con texto vivo se vea IGUAL en cualquier sitio.

Un logo SVG que carga su fuente con @import de Google Fonts sale en Georgia o en otra fuente de reserva
cuando se usa dentro de <img>, en el manual o sin conexión. Y si usa una clase CSS compartida (.nombre),
dos logos pegados en la misma página se pisan entre sí. Esta herramienta arregla las dos cosas:

  1. Incrusta la fuente dentro del SVG (@font-face con datos base64), recortada a los glifos del logo si
     está instalada la librería `fonttools` (pip install fonttools); si no, incrusta la fuente completa.
  2. Pasa las reglas de clase a atributos `style` en cada elemento y quita la clase.

Uso:
  python3 incrustar_fuente.py logo/*.svg --google Newsreader
  python3 incrustar_fuente.py logo/*.svg --fuente Newsreader.ttf [--peso 400] [--salida DIR]

Por defecto sobrescribe cada SVG y guarda una copia `.bak`. Antes de publicar, comprueba la licencia de la
fuente (las de Google Fonts son OFL y permiten incrustar). Solo librería estándar; fonttools es opcional.
"""
import argparse
import base64
import os
import re
import shutil
import sys
import urllib.request


def descargar_google(familia, peso):
    url = "https://fonts.googleapis.com/css2?family=%s:wght@%d&display=swap" % (familia.replace(" ", "+"), peso)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})          # sin UA devuelve woff2
    css = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    m = re.search(r"url\((https://[^)]+\.ttf)\)", css)
    if not m:
        raise SystemExit("Google Fonts no devolvió un .ttf para «%s» (peso %d). Descárgala y usa --fuente." % (familia, peso))
    return urllib.request.urlopen(m.group(1), timeout=60).read()


def recortar(datos, texto):
    """Recorta la fuente a los glifos del logo conservando ligaduras y kerning. Devuelve (bytes, recortada)."""
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError:
        return datos, False
    import io
    op = subset.Options()
    op.layout_features = ["liga", "clig", "kern", "calt", "ccmp", "locl", "mark", "mkmk"]
    op.name_IDs = ["*"]
    op.notdef_outline = True
    f = TTFont(io.BytesIO(datos))
    s = subset.Subsetter(op)
    s.populate(text=texto)
    s.subset(f)
    out = io.BytesIO()
    f.save(out)
    return out.getvalue(), True


def procesar(ruta, datos_fuente, peso, salida):
    svg = open(ruta, encoding="utf-8").read()
    if "data:font/ttf;base64" in svg:
        print(f"  {os.path.basename(ruta)}: ya tiene la fuente incrustada, no se toca")
        return
    # reglas de clase dentro de <style>
    reglas = {}
    for nombre, decl in re.findall(r"\.([\w-]+)\s*\{([^}]*)\}", svg):
        reglas[nombre] = " ".join(decl.split())
    fam = None
    for decl in reglas.values():
        mf = re.search(r"font-family:\s*['\"]?([^,'\";]+)", decl)
        if mf:
            fam = mf.group(1).strip()
            break
    if not fam:
        raise SystemExit(f"{ruta}: no encuentro font-family en las reglas CSS; revisa el SVG.")
    texto = "".join(re.findall(r"<text[^>]*>([^<]*)</text>", svg))
    texto = re.sub(r"&amp;", "&", texto)
    datos, recortada = recortar(datos_fuente, texto + "fi fl ")
    b64 = base64.b64encode(datos).decode("ascii")
    face = ("@font-face { font-family: '%s'; font-weight: %d; src: url(data:font/ttf;base64,%s) format('truetype'); }"
            % (fam, peso, b64))

    # 1) clases -> style en línea
    def a_inline(m):
        etiqueta = m.group(0)
        cl = re.search(r'\sclass="([^"]+)"', etiqueta)
        if not cl:
            return etiqueta
        estilos = [reglas[c] for c in cl.group(1).split() if c in reglas]
        if not estilos:
            return etiqueta
        etiqueta = etiqueta.replace(cl.group(0), "")
        union = " ".join(estilos)
        ya = re.search(r'\sstyle="([^"]*)"', etiqueta)
        if ya:
            return etiqueta.replace(ya.group(0), ' style="%s %s"' % (union, ya.group(1)))
        return etiqueta[:-1] + ' style="%s">' % union if not etiqueta.endswith("/>") else etiqueta[:-2] + ' style="%s"/>' % union

    svg = re.sub(r"<(?!/)[a-zA-Z][^>]*>", a_inline, svg)
    # 2) el <style> solo conserva el @font-face (sin @import ni clases)
    svg = re.sub(r"<style>.*?</style>", "<style>\n    %s\n  </style>" % face, svg, count=1, flags=re.S)
    dest = os.path.join(salida, os.path.basename(ruta)) if salida else ruta
    if not salida:
        shutil.copy(ruta, ruta + ".bak")
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(svg)
    print(f"  ok {os.path.basename(dest)}  {len(svg) // 1024} KB  ({'fuente recortada' if recortada else 'fuente COMPLETA: instala fonttools para recortarla'})")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", nargs="+")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--fuente", help="archivo .ttf de la fuente")
    g.add_argument("--google", help="nombre de la familia en Google Fonts, p. ej. Newsreader")
    ap.add_argument("--peso", type=int, default=400)
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    try:
        datos = open(a.fuente, "rb").read() if a.fuente else descargar_google(a.google, a.peso)
    except OSError as ex:
        print(f"No se puede obtener la fuente: {ex}", file=sys.stderr)
        return 2
    for r in a.svg:
        procesar(r, datos, a.peso, a.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
