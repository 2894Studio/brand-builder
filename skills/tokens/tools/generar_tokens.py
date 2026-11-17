#!/usr/bin/env python3
"""marca.json -> tokens de diseño para producto (W3C Design Tokens, CSS, Tailwind v3 y v4).

Uso:  python3 generar_tokens.py marca.json [--salida DIR]
Salida (en DIR, por defecto ./tokens junto a marca.json):
  tokens.json          W3C Design Tokens: primitivos + semánticos
  tokens.css           variables CSS (:root)
  tailwind.preset.js   preset para Tailwind v3
  tailwind-v4.css      bloque @theme para Tailwind v4
  contraste.md         tabla de pares texto/fondo con su ratio real
  ejemplo.html         botón, tarjeta y formulario con los tokens
Falla (exit 1) si un par obligatorio de texto no llega a 4,5:1.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import argparse
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marca_lib as m  # noqa: E402

# Escala web derivada de la escala de láminas (cuerpo 28 px de lámina <-> 1 rem), razón 1,25.
ESCALA = [("xs", 0.8), ("sm", 0.875), ("base", 1.0), ("lg", 1.25), ("xl", 1.563),
          ("2xl", 1.953), ("3xl", 2.441), ("4xl", 3.052), ("display", 3.815)]
# Espaciado de base 8; el medianil de 24 de la rejilla de láminas es space.6
ESPACIO = [("0", 0), ("1", 4), ("2", 8), ("3", 12), ("4", 16), ("5", 20), ("6", 24),
           ("8", 32), ("12", 48), ("16", 64), ("24", 96), ("32", 128)]
PESOS = {"regular": 400, "medium": 500, "bold": 700}
INTERLINEADO = {"display": 1.0, "heading": 1.1, "body": 1.5, "label": 1.4}
GENERICAS = ["system-ui", "-apple-system", "Segoe UI", "sans-serif"]


def tok(valor, tipo, desc=None):
    d = {"$value": valor, "$type": tipo}
    if desc:
        d["$description"] = desc
    return d


def construir(marca):
    p = m.paleta(marca)
    nom = m.nombres_color(marca)
    ink, base, brand = p["texto"], p["fondo"], p["primario"]
    acc = p.get("acento")
    neu = p.get("neutro")
    firma = m.FIRMAS[m.territorio(marca)]
    pares, problemas = [], []

    # derivados con contraste comprobado
    sobre_marca = m.mejor_sobre(brand, [base, ink])
    muted = m.mezclar(ink, base, 0.38)
    if m.contraste(muted, base) < 4.5:
        muted = ink                      # no inventamos un gris que no se lea
    sobre_acento = m.mejor_sobre(acc, [base, ink]) if acc else None

    def par(nombre, fg, bg, minimo, obligatorio=True):
        r = m.contraste(fg, bg)
        ok = r >= minimo
        pares.append((nombre, fg, bg, r, minimo, ok, obligatorio))
        if obligatorio and not ok:
            problemas.append(f"{nombre}: {r:.2f}:1 < {minimo}:1")

    par("text.default sobre surface.base", ink, base, 4.5)
    par("text.muted sobre surface.base", muted, base, 4.5)
    par("text.on-brand sobre surface.brand", sobre_marca, brand, 4.5)
    par("brand sobre surface.base (enlaces, botón secundario)", brand, base, 4.5, obligatorio=False)
    if acc:
        par("text.on-accent sobre accent", sobre_acento, acc, 4.5)
        par("accent sobre surface.base", acc, base, 4.5, obligatorio=False)
    if neu:
        par("border.default sobre surface.base (UI)", neu, base, 3.0, obligatorio=False)

    color = {
        "primitive": {
            "ink": tok(ink, "color", f"{nom.get('texto', 'tinta')} · rol texto"),
            "base": tok(base, "color", f"{nom.get('fondo', 'base')} · rol fondo"),
            "brand": tok(brand, "color", f"{nom.get('primario', 'marca')} · rol primario"),
        },
        "text": {
            "default": tok("{color.primitive.ink}", "color"),
            "muted": tok(muted, "color", "tinta atenuada, ≥ 4,5:1 sobre la base"),
            "on-brand": tok(sobre_marca, "color", "texto sobre surface.brand"),
        },
        "surface": {
            "base": tok("{color.primitive.base}", "color"),
            "brand": tok("{color.primitive.brand}", "color"),
        },
    }
    if acc:
        color["primitive"]["accent"] = tok(acc, "color", f"{nom.get('acento', 'acento')} · rol acento")
        color["accent"] = {
            "default": tok("{color.primitive.accent}", "color",
                           "máximo el 10 % de la superficie; no para texto pequeño si no llega a 4,5:1"),
            "on-accent": tok(sobre_acento, "color", "texto sobre accent"),
        }
        if m.contraste(acc, base) >= 4.5:
            color["text"]["accent"] = tok("{color.primitive.accent}", "color")
    if neu:
        color["primitive"]["neutral"] = tok(neu, "color", f"{nom.get('neutro', 'neutro')} · neutro de la marca")
        color["border"] = {"default": tok("{color.primitive.neutral}", "color", "bordes y superficies; no texto")}
        color["surface"]["subtle"] = tok("{color.primitive.neutral}", "color")

    tp = marca.get("tipografia", {})
    fh = tp.get("titulos", {}).get("familia", "system-ui")
    fb = tp.get("texto", {}).get("familia", "system-ui")
    tokens = {
        "$description": f"Tokens de {marca['nombre']} generados desde marca.json por brand-kit-builder",
        "color": color,
        "font": {
            "family": {
                "heading": tok([fh] + GENERICAS, "fontFamily"),
                "body": tok([fb] + GENERICAS, "fontFamily"),
            },
            "size": {k: tok(f"{v}rem", "dimension") for k, v in ESCALA},
            "weight": {k: tok(v, "fontWeight") for k, v in PESOS.items()},
            "lineHeight": {k: tok(v, "number") for k, v in INTERLINEADO.items()},
        },
        "space": {k: tok(f"{v}px", "dimension") for k, v in ESPACIO},
        "radius": {
            "sm": tok(f"{firma['radio'] // 2}px", "dimension"),
            "md": tok(f"{firma['radio']}px", "dimension",
                      f"del territorio «{m.territorio(marca)}»"),
            "pill": tok("9999px", "dimension"),
        },
    }
    return tokens, pares, problemas


def resolver(tokens, v):
    while isinstance(v, str) and v.startswith("{") and v.endswith("}"):
        nodo = tokens
        for k in v[1:-1].split("."):
            nodo = nodo[k]
        v = nodo["$value"]
    return v


def aplanar(tokens, prefijo=()):
    for k, v in tokens.items():
        if k.startswith("$"):
            continue
        if "$value" in v:
            yield prefijo + (k,), v
        else:
            yield from aplanar(v, prefijo + (k,))


def a_css(tokens):
    lineas = [":root {"]
    for ruta, t in aplanar(tokens):
        nombre = "--" + "-".join(ruta)
        val = t["$value"]
        if isinstance(val, str) and val.startswith("{"):
            val = "var(--" + val[1:-1].replace(".", "-") + ")"
        elif isinstance(val, list):
            val = ", ".join(f'"{x}"' if " " in x else x for x in val)
        lineas.append(f"  {nombre}: {val};")
    lineas.append("}")
    return "\n".join(lineas) + "\n"


def a_tailwind_v3(tokens, marca):
    def r(v):
        return resolver(tokens, v)
    c = tokens["color"]
    colores = {
        "ink": r(c["primitive"]["ink"]["$value"]),
        "base": r(c["primitive"]["base"]["$value"]),
        "brand": r(c["primitive"]["brand"]["$value"]),
    }
    if "accent" in c["primitive"]:
        colores["accent"] = r(c["primitive"]["accent"]["$value"])
    if "neutral" in c["primitive"]:
        colores["neutral"] = r(c["primitive"]["neutral"]["$value"])
    f = tokens["font"]
    cfg = {
        "theme": {"extend": {
            "colors": colores,
            "fontFamily": {"heading": f["family"]["heading"]["$value"], "body": f["family"]["body"]["$value"]},
            "fontSize": {k: v["$value"] for k, v in f["size"].items()},
            "borderRadius": {k: v["$value"] for k, v in tokens["radius"].items()},
            "spacing": {k: v["$value"] for k, v in tokens["space"].items()},
        }}
    }
    return (f"// Preset de Tailwind v3 para {marca['nombre']}. Generado desde marca.json.\n"
            f"// Uso: presets: [require('./tailwind.preset.js')] en tailwind.config.js\n"
            f"module.exports = {json.dumps(cfg, indent=2, ensure_ascii=False)};\n")


def a_tailwind_v4(tokens, marca):
    ls = [f"/* Tailwind v4 · {marca['nombre']} · generado desde marca.json */", "@theme {"]
    c = tokens["color"]["primitive"]
    for k, t in c.items():
        ls.append(f"  --color-{k}: {t['$value']};")
    f = tokens["font"]
    ls.append("  --font-heading: " + ", ".join(f'"{x}"' if " " in x else x for x in f["family"]["heading"]["$value"]) + ";")
    ls.append("  --font-body: " + ", ".join(f'"{x}"' if " " in x else x for x in f["family"]["body"]["$value"]) + ";")
    for k, t in f["size"].items():
        ls.append(f"  --text-{k}: {t['$value']};")
    for k, t in tokens["radius"].items():
        ls.append(f"  --radius-{k}: {t['$value']};")
    ls.append("}")
    return "\n".join(ls) + "\n"


def a_contraste(marca, pares):
    ls = [f"# Contraste de {marca['nombre']}", "",
          "Mínimos: 4,5:1 texto normal · 3:1 texto grande o UI. Los pares obligatorios hacen fallar la generación.", "",
          "| Par | Texto | Fondo | Ratio | Mínimo | Resultado |", "|---|---|---|---|---|---|"]
    for nombre, fg, bg, r, mn, ok, obl in pares:
        if ok:
            res = "✔"
        elif obl:
            res = "✘ ERROR"
        elif nombre.startswith("border"):
            res = "solo decorativo: no sirve de borde en campos de formulario"
        else:
            res = f"limitado: {m.veredicto(r)}"
        ls.append(f"| {nombre} | `{fg}` | `{bg}` | {r:.2f}:1 | {mn}:1 | {res} |")
    ls += ["", "Los pares con «limitado» o «solo decorativo» no son un error: indican para qué sí vale ese color "
           "(filetes, iconos grandes, fondos) y para qué no (texto pequeño)."]
    return "\n".join(ls) + "\n"


def a_ejemplo(tokens, marca, css):
    fh = tokens["font"]["family"]["heading"]["$value"][0]
    fb = tokens["font"]["family"]["body"]["$value"][0]
    fam = "&".join("family=" + x.replace(" ", "+") + ":wght@400;500;700" for x in {fh, fb})
    n = html.escape(marca["nombre"])
    tiene_acento = "accent" in tokens["color"]["primitive"]
    badge = ('<span class="badge">nuevo</span>' if tiene_acento else "")
    badge_css = ("""
.badge{display:inline-block;background:var(--color-accent-default);color:var(--color-accent-on-accent);
  font-size:var(--font-size-xs);font-weight:var(--font-weight-bold);padding:var(--space-1) var(--space-3);
  border-radius:var(--radius-pill)}""" if tiene_acento else "")
    return f"""<!doctype html>
<html lang="{html.escape(marca['idioma'][:2])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{n} · tokens en uso</title>
<!-- Las fuentes se cargan de Google Fonts si hay conexión; sin ella se usa la fuente del sistema. -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fam}&display=swap">
<style>
{css}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--color-surface-base);color:var(--color-text-default);
  font-family:var(--font-family-body);font-size:var(--font-size-base);line-height:var(--font-lineHeight-body)}}
h1,h2{{font-family:var(--font-family-heading);line-height:var(--font-lineHeight-heading);margin:0}}
h1{{font-size:var(--font-size-3xl)}} h2{{font-size:var(--font-size-xl)}}
header{{background:var(--color-surface-brand);color:var(--color-text-on-brand);padding:var(--space-6) var(--space-12)}}
main{{max-width:960px;margin:0 auto;padding:var(--space-12)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:var(--space-6);margin-top:var(--space-8)}}
.card{{background:var(--color-surface-base);border:1px solid var(--color-border-default);
  border-radius:var(--radius-md);padding:var(--space-6)}}
.card p{{color:var(--color-text-muted)}}
button{{font:inherit;font-weight:var(--font-weight-bold);border:2px solid var(--color-surface-brand);
  border-radius:var(--radius-md);padding:var(--space-3) var(--space-6);cursor:pointer}}
.primary{{background:var(--color-surface-brand);color:var(--color-text-on-brand)}}
.secondary{{background:transparent;color:var(--color-surface-brand)}}
button:focus-visible,input:focus-visible{{outline:3px solid var(--color-surface-brand);outline-offset:2px}}
label{{display:block;font-weight:var(--font-weight-medium);margin-bottom:var(--space-2)}}
input{{font:inherit;width:100%;padding:var(--space-3);border:1px solid var(--color-text-muted);
  border-radius:var(--radius-md);background:var(--color-surface-base);color:var(--color-text-default)}}{badge_css}
</style>
</head>
<body>
<header><strong style="font-family:var(--font-family-heading);font-size:var(--font-size-xl)">{n}</strong></header>
<main>
  <h1>Así se ve {n} en producto</h1>
  <p>Todo lo de esta página sale de <code>tokens.css</code>. Si cambia la marca, cambian los tokens y esto se actualiza solo.</p>
  <div class="grid">
    <section class="card"><h2>Tarjeta {badge}</h2>
      <p>Texto atenuado sobre la base, con contraste comprobado.</p>
      <button class="primary">Acción principal</button> <button class="secondary">Secundaria</button></section>
    <form class="card" onsubmit="return false"><h2>Formulario</h2>
      <label for="e">Correo</label><input id="e" type="email" placeholder="nombre@correo.com">
      <p></p><button class="primary">Enviar</button></form>
  </div>
</main>
</body>
</html>
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    try:
        marca = m.cargar(a.marca)
    except (OSError, json.JSONDecodeError) as ex:
        print(f"No se puede leer {a.marca}: {ex}", file=sys.stderr)
        return 2
    if not m.informe(a.marca, marca):
        print("marca.json no es válido; corrígelo antes de generar tokens.", file=sys.stderr)
        return 1
    salida = a.salida or os.path.join(os.path.dirname(os.path.abspath(a.marca)), "tokens")
    os.makedirs(salida, exist_ok=True)

    tokens, pares, problemas = construir(marca)
    css = a_css(tokens)
    archivos = {
        "tokens.json": json.dumps(tokens, indent=2, ensure_ascii=False) + "\n",
        "tokens.css": css,
        "tailwind.preset.js": a_tailwind_v3(tokens, marca),
        "tailwind-v4.css": a_tailwind_v4(tokens, marca),
        "contraste.md": a_contraste(marca, pares),
        "ejemplo.html": a_ejemplo(tokens, marca, css),
    }
    for nombre, contenido in archivos.items():
        with open(os.path.join(salida, nombre), "w", encoding="utf-8") as f:
            f.write(contenido)
        print("ok", os.path.join(salida, nombre))
    if problemas:
        print("\nPares de texto que no llegan al mínimo:", file=sys.stderr)
        for pr in problemas:
            print("  ERROR ", pr, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
