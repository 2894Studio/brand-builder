#!/usr/bin/env python3
"""marca.json -> brand.json de motion-architect (https://github.com/Hainrixz/motion-architect).

Uso:
  python3 exportar_motion.py marca.json --salida motion-architect/studio/brand.json
  python3 exportar_motion.py marca.json --salida studio/brand.json --studio motion-architect/studio
Opciones:
  --tagline TEXTO   claim corto que sale bajo el nombre (por defecto, la categoría)
  --studio RUTA     carpeta studio/ de motion-architect: comprueba si las fuentes existen en Remotion
  --forzar          sobrescribe un brand.json existente (antes guarda brand.json.bak)

Esquema de destino (verificado en el repo): name, tagline, colors{background, surface, text, muted,
accent, accent2}, fonts{display, body}, radius, style.
IMPORTANTE: en motion-architect la fuente real es la de los imports de src/brand/brand.ts; `fonts` del
JSON es solo informativo. Este script imprime las líneas exactas que hay que cambiar en brand.ts.
"""
import argparse
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marca_lib as m  # noqa: E402


def modulo_fuente(familia):
    """'Space Grotesk' -> 'SpaceGrotesk' (convención de @remotion/google-fonts)."""
    return re.sub(r"[^A-Za-z0-9]", "", familia)


def primera_frase(texto, maximo=140):
    f = re.split(r"(?<=[.;])\s", texto.strip())[0].rstrip(".;, ")
    if len(f) <= maximo:
        return f
    return f[: maximo - 1].rsplit(" ", 1)[0].rstrip(" ,;") + "…"      # corta en palabra, no a mitad


def construir(marca, tagline=None):
    p = m.paleta(marca)
    avisos = []
    fondo, texto, primario = p["fondo"], p["texto"], p["primario"]
    acento = p.get("acento")

    # accent: el color que lleva texto resaltado y fondo de píldoras -> debe leerse sobre el fondo.
    # Por eso es el primario (de la marca), y el acento (verde, etc.) pasa a accent2.
    accent, accent2 = primario, (acento or m.mezclar(primario, fondo, 0.35))
    r = m.contraste(accent, fondo)
    if r < 4.5:
        avisos.append(f"accent ({accent}) sobre el fondo da {r:.2f}:1; motion-architect lo usa en texto resaltado "
                      "(mínimo 4,5:1). Úsalo solo en formas o cambia el color primario.")
    if acento and m.contraste(acento, fondo) < 4.5:
        avisos.append(f"accent2 ({acento}) da {m.contraste(acento, fondo):.2f}:1 sobre el fondo: no lo uses en texto.")

    muted = m.mezclar(texto, fondo, 0.38)
    if m.contraste(muted, fondo) < 4.5:
        muted = texto
    if "neutro" in p:
        avisos.append(f"el neutro de la marca ({p['neutro']}) no tiene hueco en brand.json; "
                      "surface se calcula como un 6 % de tinta sobre el fondo.")

    tp = marca.get("tipografia", {})
    display = tp.get("titulos", {}).get("familia")
    body = tp.get("texto", {}).get("familia")
    if not display or not body:
        avisos.append("sin «tipografia» en marca.json: se deja la fuente por defecto de motion-architect.")
        display, body = display or "Bricolage Grotesque", body or "Geist"

    brand = {
        "name": marca["nombre"],
        "tagline": tagline or marca["categoria"],
        "colors": {
            "background": fondo,
            "surface": m.mezclar(fondo, texto, 0.06),
            "text": texto,
            "muted": muted,
            "accent": accent,
            "accent2": accent2,
        },
        "fonts": {"display": display, "body": body},
        "radius": m.FIRMAS[m.territorio(marca)]["radio"],
        "style": primera_frase(marca["visual"]["estilo"]),
    }
    return brand, avisos


def lineas_brand_ts(marca):
    tp = marca.get("tipografia", {})
    out = []
    for rol, var, defecto in (("titulos", "loadDisplay", [500, 700]), ("texto", "loadBody", [400, 500])):
        fam = tp.get(rol, {}).get("familia")
        if not fam:
            continue
        pesos = ", ".join(f'"{x}"' for x in tp[rol].get("pesos", defecto))
        out.append(f'import {{ loadFont as {var} }} from "@remotion/google-fonts/{modulo_fuente(fam)}";')
        out.append(f'const {"display" if var == "loadDisplay" else "body"} = {var}("normal", '
                   f'{{ weights: [{pesos}], subsets: ["latin"] }});')
    return out


def comprobar_fuentes(marca, studio):
    res = []
    base = os.path.join(studio, "node_modules", "@remotion", "google-fonts", "dist", "esm")
    if not os.path.isdir(base):
        return ["no se puede comprobar las fuentes: falta studio/node_modules (ejecuta ./install.sh de motion-architect)"]
    for rol in ("titulos", "texto"):
        fam = marca.get("tipografia", {}).get(rol, {}).get("familia")
        if fam:
            ok = os.path.isfile(os.path.join(base, modulo_fuente(fam) + ".mjs"))
            res.append(f"{fam}: {'disponible en @remotion/google-fonts' if ok else 'NO está en @remotion/google-fonts; usa una fuente propia (.woff2) o elige otra'}")
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--salida", default="brand.json")
    ap.add_argument("--tagline")
    ap.add_argument("--studio")
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args(argv)
    try:
        marca = m.cargar(a.marca)
    except (OSError, json.JSONDecodeError) as ex:
        print(f"No se puede leer {a.marca}: {ex}", file=sys.stderr)
        return 2
    if not m.informe(a.marca, marca):
        print("marca.json no es válido; corrígelo antes de exportar.", file=sys.stderr)
        return 1

    brand, avisos = construir(marca, a.tagline)
    if os.path.exists(a.salida):
        if not a.forzar:
            print(f"{a.salida} ya existe y no se sobrescribe sin --forzar (guardaría una copia en {a.salida}.bak).",
                  file=sys.stderr)
            return 1
        shutil.copy(a.salida, a.salida + ".bak")
        print(f"copia de seguridad: {a.salida}.bak")
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    with open(a.salida, "w", encoding="utf-8") as f:
        json.dump(brand, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("ok", a.salida)

    print("\nFALTA UN PASO MANUAL: la fuente real es la de los imports de studio/src/brand/brand.ts.")
    print("Sustituye las líneas de loadFont por estas:\n")
    for ln in lineas_brand_ts(marca):
        print("  " + ln)
    if a.studio:
        print()
        for ln in comprobar_fuentes(marca, a.studio):
            print("  -", ln)
    else:
        print("\n  (pasa --studio RUTA para comprobar que Remotion tiene esas fuentes)")
    if avisos:
        print("\nAvisos:", file=sys.stderr)
        for av in avisos:
            print("  -", av, file=sys.stderr)
    print("\nEl logo no se exporta: ponlo en studio/public/brand/logo.svg (motion-architect lo usa con staticFile).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
