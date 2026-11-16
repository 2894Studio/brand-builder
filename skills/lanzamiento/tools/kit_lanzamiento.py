#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Monta el kit visual desde un brief.json: logo, bento y dos posts, con el crítico y la puerta de entrega.

Uso:  python3 kit_lanzamiento.py lanzamiento/brief.json
Quien dirige la marca solo decide y escribe el brief (copy, recurso, datos); el script ejecuta los generadores, captura los PNG,
pasa el crítico y la puerta. **No se dibujan los SVG a mano**: si ningún recurso encaja, `"recurso": "html"` con el archivo propio.

brief.json:
{
  "marca": "marca.json", "gusto": "gusto.json",              (rutas relativas al brief o absolutas)
  "carpeta": "trabajo/2026-11-16-marca-x/lanzamiento",       (donde salen las piezas)
  "kits": "trabajo",                                         (kits anteriores, para comprobar la variedad)
  "fotos": "lanzamiento/fotos",                              (opcional: salida de preparar_fotos.py)
  "bento": {"variante": "educativa", "lema": "…", "prueba": "Título|Valor", "ruta": "a;b;c", "datos": "E|V;E|V", "puntos": "a;b", "persona": "N|R"},
  "post1": {"recurso": "foto|pantalla|telefono|comparativa|mapa|html", "args": {"titular": "…", "ventana": "…", "tema": "claro"}},
  "post2": {"recurso": "…", "args": {…}},
  "notas": ["lo que es de ejemplo o queda a mano, una frase cada una"]
}
En "args" cada clave es una opción del generador (guiones bajos = guiones: tarjeta_izq → --tarjeta-izq); true = opción sin valor.
Los argumentos de cada recurso están en la cabecera de su script (post_foto.py, post_pantalla.py, post_telefono.py, post_comparativa.py, post_mapa.py).
Si la marca es visual (fotografía, gastronomía, moda, viajes, interiorismo…) y no hay fotos, añade `"sin_fotos": "motivo"` al brief solo si se decide a propósito.
Sale con 1 si algún generador falla o la puerta de entrega se cierra; imprime qué corregir en el brief y se repite.
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CRITICO = os.path.join(RAIZ, "skills", "gusto", "tools", "critico_render.py")
PUERTA = os.path.join(RAIZ, "skills", "entrega", "tools", "verificar_entrega.py")
GEN = {"foto": "post_foto.py", "telefono": "post_telefono.py", "pantalla": "post_pantalla.py", "comparativa": "post_comparativa.py", "mapa": "post_mapa.py"}
TAM = {"bento": (1920, 1080), "post-1-que-es": (1080, 1440), "post-2-atributo": (1080, 1440)}


def ruta(base, p):
    return p if not p or os.path.isabs(p) else os.path.normpath(os.path.join(base, p))


def flags(args):
    out = []
    for k, v in (args or {}).items():
        f = "--" + k.replace("_", "-")
        if v is True:
            out.append(f)
        elif v not in (False, None, ""):
            out += [f, str(v)]
    return out


def run(cmd):
    return subprocess.run([sys.executable] + cmd, capture_output=True, text=True)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    bp = os.path.abspath(sys.argv[1])
    base = os.path.dirname(bp)
    b = json.load(open(bp, encoding="utf-8"))
    marca = ruta(base, b.get("marca", "marca.json"))
    carpeta = ruta(base, b.get("carpeta", "."))
    os.makedirs(carpeta, exist_ok=True)
    gusto = ruta(base, b.get("gusto"))
    fotos = ruta(base, b.get("fotos"))
    mal = 0

    # logo
    lg = os.path.join(carpeta, "logo")
    r = run([os.path.join(AQUI, "exportar_logos.py"), marca, "--salida", lg])
    print("logo:", "ok" if r.returncode == 0 else "FALLO " + (r.stdout + r.stderr).strip()[-200:])
    mal += r.returncode != 0

    piezas = []
    # bento
    bn = b.get("bento", {})
    cmd = [os.path.join(AQUI, "bento.py"), marca, "--salida", os.path.join(carpeta, "bento.html")]
    if gusto and os.path.exists(gusto):
        cmd += ["--gusto", gusto]
    if fotos and os.path.isdir(fotos):
        cmd += ["--fotos", fotos]
    cmd += flags(bn)
    r = run(cmd)
    print("bento:", "ok" if r.returncode == 0 else "FALLO " + (r.stdout + r.stderr).strip()[-300:])
    if r.returncode == 0:
        piezas.append("bento")
        for l in r.stdout.splitlines():
            if l.strip().startswith("aviso"):
                print("   ", l.strip())
    mal += r.returncode != 0

    # posts
    for i, nombre in ((1, "post-1-que-es"), (2, "post-2-atributo")):
        p = b.get(f"post{i}", {})
        rec = p.get("recurso", "")
        salida = os.path.join(carpeta, nombre + ".html")
        if rec == "html":
            src = ruta(base, p.get("archivo", ""))
            if not os.path.exists(src):
                print(f"{nombre}: FALLO no existe {src}")
                mal += 1
                continue
            if os.path.abspath(src) != os.path.abspath(salida):
                open(salida, "w", encoding="utf-8").write(open(src, encoding="utf-8").read())
            print(f"{nombre}: html propio")
            piezas.append(nombre)
            continue
        if rec not in GEN:
            print(f"{nombre}: FALLO recurso «{rec}» desconocido (usa {', '.join(GEN)} o html)")
            mal += 1
            continue
        cmd = [os.path.join(AQUI, GEN[rec]), marca, "--salida", salida]
        a = dict(p.get("args", {}))
        if fotos and os.path.isdir(fotos) and rec in ("telefono", "mapa", "foto") and "fotos" not in a and "foto" not in a:
            a["fotos"] = fotos
        r = run(cmd + flags(a))
        print(f"{nombre}: {rec} " + ("ok" if r.returncode == 0 else "FALLO " + (r.stdout + r.stderr).strip()[-300:]))
        if r.returncode == 0:
            piezas.append(nombre)
            for l in r.stdout.splitlines():
                if l.strip().startswith("aviso"):
                    print("   ", l.strip())
        mal += r.returncode != 0

    # crítico + PNG
    for n in piezas:
        w, h = TAM[n]
        r = run([CRITICO, os.path.join(carpeta, n + ".html"), "--ancho", str(w), "--alto", str(h), "--marca", marca, "--png", os.path.join(carpeta, n + ".png")])
        if r.returncode == 2:
            print(f"{n}: el crítico no se pudo ejecutar (falta Playwright/Chromium): sin PNG ni revisión")
            mal += 1
            continue
        errs = [x.strip() for x in r.stdout.splitlines() if x.strip().startswith("ERROR")]
        print(f"{n}: crítico " + ("0 errores" if not errs else f"{len(errs)} error(es)"))
        for x in errs:
            print("    ", x)

    # LEEME
    leeme = os.path.join(carpeta, "LEEME.md")
    if not os.path.exists(leeme):
        with open(leeme, "w", encoding="utf-8") as fh:
            fh.write("# Kit de lanzamiento\n\nPiezas: logo/, bento, post-1-que-es, post-2-atributo (HTML editable y PNG).\n\n## Qué es de ejemplo o queda a mano\n\n")
            for x in b.get("notas", []) or ["(rellena: qué es real, qué es de ejemplo y qué queda por hacer a mano)"]:
                fh.write(f"- {x}\n")

    # puerta
    cmd = [PUERTA, carpeta, "--marca", marca] + (["--kits", ruta(base, b["kits"])] if b.get("kits") else [])
    r = run(cmd)
    print("\n" + r.stdout.strip())
    return 1 if (mal or r.returncode) else 0


if __name__ == "__main__":
    sys.exit(main())
