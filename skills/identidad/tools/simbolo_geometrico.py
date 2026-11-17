#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Símbolos geométricos para el logo, gratis y sin proveedor de imagen.

El agente ELIGE el tipo de construcción (y dice por qué); el script la dibuja con la paleta de la marca y deja
SVG listos: símbolo solo, logotipo con el nombre (principal, invertida, monocroma) y una hoja de comparación.

Uso:
  python3 simbolo_geometrico.py --nombre fullstacker --tinta "#0E1A2B" --acento "#E8B04B" --fondo "#F5F3EE" \\
        --tipos baldosa,bloques --fuente "Inter" --peso 800 --salida trabajo/…/logo-opciones
  python3 simbolo_geometrico.py --elegir a --salida trabajo/…/logo-opciones --destino trabajo/…/logo
  python3 simbolo_geometrico.py --tipos            (lista los tipos y cuándo usarlos)

Tipos: baldosa (cuatro celdas de cuartos de círculo, círculos y cuadrados), orbita (disco con satélite y mordisco),
pliegue (triángulo y medio disco que encajan), bloques (barras apiladas desplazadas), arcos (arcos concéntricos).
--variante N cambia el dibujo dentro del mismo tipo (por defecto sale del nombre, así dos marcas no coinciden).

El nombre va como texto vivo: ejecuta después skills/identidad/tools/incrustar_fuente.py sobre los SVG.
Un símbolo geométrico es un punto de partida honesto, no un logo premiado: si la marca merece un dibujo a mano, este script no lo sustituye.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: salida en tubería → cp1252
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import argparse
import hashlib
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile

TIPOS = {
    "baldosa": "Marcas con carácter lúdico, editorial o de formación: un mosaico Bauhaus de cuatro celdas. Funciona pequeño.",
    "orbita": "Marcas de red, comunidad, movimiento o conexión: un disco con un satélite y un mordisco.",
    "pliegue": "Marcas de dirección, transición o cambio (carrera, mudanza, método): dos piezas que encajan en diagonal.",
    "bloques": "Marcas de capas, procesos, plataformas o crecimiento (stack, programa, niveles): barras apiladas.",
    "arcos": "Marcas de acogida, horizonte, protección o servicio: arcos concéntricos.",
}


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lum(h):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (c(v) for v in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contraste(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _rng(nombre, tipo, variante):
    return random.Random(int(hashlib.md5(f"{nombre}|{tipo}|{variante}".encode("utf-8")).hexdigest()[:12], 16))


# --- construcciones: cada una devuelve SVG interior en una caja de 100×100; t = tinta, a = acento --------------------------------

def _cuarto(x, y, tam, rot, color):
    """Cuarto de círculo de radio `tam` en la celda (x, y); `rot` 0..3 elige la esquina del centro."""
    cx = [(x, y), (x + tam, y), (x + tam, y + tam), (x, y + tam)]
    ini = [(x + tam, y), (x + tam, y + tam), (x, y + tam), (x, y)]
    fin = [(x, y + tam), (x, y), (x + tam, y), (x + tam, y + tam)]
    c = cx[rot]
    s, e = ini[rot], fin[rot]
    return f'<path d="M{c[0]} {c[1]} L{s[0]} {s[1]} A{tam} {tam} 0 0 1 {e[0]} {e[1]} Z" fill="{color}"/>'


def baldosa(rng, t, a):
    k = 50
    pos = [(0, 0), (k, 0), (0, k), (k, k)]
    tipos = ["cuarto", "cuarto", "circulo", "cuadrado", "medio"]
    rng.shuffle(tipos)
    elegidos = tipos[:4]
    if "circulo" not in elegidos:
        elegidos[rng.randrange(4)] = "circulo"
    colores = [t, t, a, t]
    rng.shuffle(colores)
    out = []
    for (x, y), kind, col in zip(pos, elegidos, colores):
        if kind == "cuarto":
            # el centro del cuarto mira hacia el centro del símbolo para que las celdas conversen
            rot = {(0, 0): 2, (k, 0): 3, (0, k): 1, (k, k): 0}[(x, y)] if rng.random() < .6 else rng.randrange(4)
            out.append(_cuarto(x, y, k, rot, col))
        elif kind == "circulo":
            out.append(f'<circle cx="{x + k / 2}" cy="{y + k / 2}" r="{k / 2 - 1}" fill="{col}"/>')
        elif kind == "cuadrado":
            out.append(f'<rect x="{x}" y="{y}" width="{k}" height="{k}" fill="{col}"/>')
        else:
            if rng.random() < .5:
                out.append(f'<path d="M{x} {y + k} A{k / 2} {k / 2} 0 0 1 {x + k} {y + k} Z" fill="{col}"/>')
            else:
                out.append(f'<path d="M{x} {y} A{k / 2} {k / 2} 0 0 0 {x + k} {y} Z" fill="{col}"/>')
    return "".join(out)


def orbita(rng, t, a):
    ang = rng.choice([-45, 45, 135, -135]) * math.pi / 180
    cx, cy, R = 50, 50, 40
    sx, sy = cx + (R + 2) * math.cos(ang), cy + (R + 2) * math.sin(ang)
    mid = f"m{rng.randrange(10 ** 6)}"
    return (f'<defs><mask id="{mid}"><rect width="100" height="100" fill="#fff"/><circle cx="{sx:.1f}" cy="{sy:.1f}" r="21" fill="#000"/></mask></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{t}" mask="url(#{mid})"/>'
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="13" fill="{a}"/>')


def pliegue(rng, t, a):
    flip = rng.random() < .5
    tri = f'<path d="M0 0 L88 0 L0 88 Z" fill="{t}"/>'
    med = f'<path d="M100 0 A70.71 70.71 0 0 1 0 100 Z" fill="{a}" transform="translate(6 6) scale(.94)"/>'
    g = tri + med
    return f'<g transform="translate(100 0) scale(-1 1)">{g}</g>' if flip else g


def bloques(rng, t, a):
    anchos = [rng.choice([100, 86, 72]), rng.choice([66, 78, 58]), rng.choice([88, 74, 60])]
    desp = [0, rng.choice([0, 14, 22]), rng.choice([0, 10, 18])]
    acc = rng.randrange(3)
    out = []
    for i in range(3):
        y = 6 + i * 33
        w = min(anchos[i], 100 - desp[i])
        out.append(f'<rect x="{desp[i]}" y="{y}" width="{w}" height="25" rx="12.5" fill="{a if i == acc else t}"/>')
    return "".join(out)


def arcos(rng, t, a):
    cx, cy = 50, 84
    out = []
    cols = [t, a, t]
    if rng.random() < .5:
        cols = [a, t, t]
    for i, r in enumerate((43, 29, 15)):
        out.append(f'<path d="M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}" fill="none" stroke="{cols[i]}" stroke-width="9"/>')
    return "".join(out)


CONSTRUCCION = {"baldosa": baldosa, "orbita": orbita, "pliegue": pliegue, "bloques": bloques, "arcos": arcos}


def svg_simbolo(tipo, nombre, variante, t, a, lado=100):
    cuerpo = CONSTRUCCION[tipo](_rng(nombre, tipo, variante), t, a)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{lado}" height="{lado}" role="img" aria-label="{nombre}">{cuerpo}</svg>'


def svg_logotipo(tipo, nombre, variante, t, a, tinta_texto, fuente, peso, minusculas, mono=None):
    """Símbolo + nombre en horizontal. mono = un solo color para todo (versión monocroma)."""
    tt, aa = (mono, mono) if mono else (t, a)
    cuerpo = CONSTRUCCION[tipo](_rng(nombre, tipo, variante), tt, aa)
    txt = nombre.lower() if minusculas else nombre
    tam = 62
    ancho_txt = int(len(txt) * tam * 0.6) + 10
    W = 100 + 28 + ancho_txt
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 100" width="{W}" height="100" role="img" aria-label="{nombre}">'
            f'<g>{cuerpo}</g>'
            f'<text x="128" y="68" font-family="\'{fuente}\', sans-serif" font-weight="{peso}" font-size="{tam}" letter-spacing="-2" fill="{mono or tinta_texto}">{txt}</text></svg>')


def hoja(opciones, nombre, fondo, tinta, oscuro):
    celdas = []
    for letra, (tipo, var, d) in opciones.items():
        celdas.append(f'<section><h2>Opción {letra.upper()} · {tipo}</h2>'
                      f'<div class="p claro">{open(os.path.join(d, "principal.svg"), encoding="utf-8").read()}</div>'
                      f'<div class="p oscuro">{open(os.path.join(d, "invertida.svg"), encoding="utf-8").read()}</div>'
                      f'<div class="s"><span>{open(os.path.join(d, "simbolo.svg"), encoding="utf-8").read()}</span>'
                      f'<span class="m">{open(os.path.join(d, "simbolo.svg"), encoding="utf-8").read()}</span></div></section>')
    return (f'<!doctype html><meta charset="utf-8"><title>Símbolos · {nombre}</title><style>body{{margin:0;padding:48px;background:#e8e8ec;font:14px/1.4 system-ui;color:#222}}'
            f'main{{display:grid;grid-template-columns:1fr 1fr;gap:40px;max-width:1500px}}h2{{font:600 15px system-ui;margin:0 0 12px}}'
            f'.p{{padding:44px;border-radius:18px;margin-bottom:14px;display:flex;align-items:center;justify-content:center}}.p svg{{height:96px;width:auto}}'
            f'.claro{{background:{fondo}}}.oscuro{{background:{oscuro}}}.s{{display:flex;gap:18px;align-items:center}}.s svg{{width:120px;height:120px;background:{fondo};padding:20px;border-radius:18px}}'
            f'.m svg{{width:32px;height:32px;padding:6px}}</style><main>{"".join(celdas)}</main>')


RUNNER = r"""
const {chromium}=require('playwright');(async()=>{const [url,out]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:700}});
await p.goto(url);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:out,fullPage:true});await b.close()})().catch(e=>{console.error(e.message);process.exit(3)})
"""


def captura(html, png):
    node = shutil.which("node")
    if not node:
        return False
    d = tempfile.mkdtemp()
    run = os.path.join(d, "r.js")
    open(run, "w", encoding="utf-8").write(RUNNER)
    env = dict(os.environ)
    try:
        raiz = subprocess.run([shutil.which("npm") or "npm", "root", "-g"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20).stdout.strip()
        env["NODE_PATH"] = os.pathsep.join(filter(None, [env.get("NODE_PATH", ""), raiz, os.path.join(os.getcwd(), "node_modules")]))
    except Exception:  # noqa: BLE001
        pass
    r = subprocess.run([node, run, "file://" + os.path.abspath(html).replace("\\", "/"), png], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=120)
    return r.returncode == 0 and os.path.exists(png)


def generar(a):
    tipos = [x.strip() for x in a.tipos_elegidos.split(",") if x.strip()]
    for x in tipos:
        if x not in CONSTRUCCION:
            sys.exit(f"tipo desconocido «{x}». Opciones: {', '.join(CONSTRUCCION)}")
    if len(tipos) != 2 or tipos[0] == tipos[1]:
        sys.exit("Elige exactamente dos tipos distintos (las dos propuestas de logo se diferencian en el tipo de marca, no en el acabado).")
    t, ac, fondo = a.tinta, a.acento, a.fondo
    if _contraste(t, fondo) < 4.5:
        sys.exit(f"La tinta {t} no contrasta con el fondo {fondo} (mínimo 4,5:1). Elige otra tinta.")
    claro = "#F5F3EE" if _lum(fondo) > .5 else fondo
    oscuro = a.oscuro or t
    ac_osc = ac if _contraste(ac, oscuro) >= 3 else claro
    os.makedirs(a.salida, exist_ok=True)
    opciones = {}
    for letra, tipo in zip("ab", tipos):
        d = os.path.join(a.salida, f"opcion-{letra}")
        os.makedirs(d, exist_ok=True)
        var = a.variante
        put = lambda n, s: open(os.path.join(d, n), "w", encoding="utf-8").write(s)  # noqa: E731
        put("simbolo.svg", svg_simbolo(tipo, a.nombre, var, t, ac))
        put("simbolo-invertido.svg", svg_simbolo(tipo, a.nombre, var, claro, ac_osc))
        put("principal.svg", svg_logotipo(tipo, a.nombre, var, t, ac, t, a.fuente, a.peso, a.minusculas))
        put("invertida.svg", svg_logotipo(tipo, a.nombre, var, claro, ac_osc, claro, a.fuente, a.peso, a.minusculas))
        put("monocroma.svg", svg_logotipo(tipo, a.nombre, var, t, t, t, a.fuente, a.peso, a.minusculas, mono=t))
        opciones[letra] = (tipo, var, d)
        print(f"opción {letra.upper()}: {tipo} → {d}")
    hp = os.path.join(a.salida, "comparar.html")
    open(hp, "w", encoding="utf-8").write(hoja(opciones, a.nombre, fondo, t, oscuro))
    print(f"hoja de comparación: {hp}")
    png = os.path.join(a.salida, "comparar.png")
    if captura(hp, png):
        print(f"imagen: {png} (ábrela y mírala antes de presentarla)")
    else:
        print("(sin Node + Playwright no hay imagen: abre comparar.html en un navegador para verlo)")
    print("Siguiente: enseña las dos opciones a la vez, recomienda una en dos líneas y deja elegir; luego --elegir a|b y incrustar_fuente.py.")


def elegir(a):
    d = os.path.join(a.salida, f"opcion-{a.elegir}")
    if not os.path.isdir(d):
        sys.exit(f"No existe {d}. Ejecuta primero la generación.")
    dest = a.destino or os.path.join(os.path.dirname(os.path.abspath(a.salida)), "logo")
    os.makedirs(dest, exist_ok=True)
    for n in ("principal", "invertida", "monocroma", "simbolo", "simbolo-invertido"):
        shutil.copyfile(os.path.join(d, n + ".svg"), os.path.join(dest, n + ".svg"))
    print(f"copiados a {dest}: principal, invertida, monocroma, simbolo, simbolo-invertido.")
    print('Regístralos en marca.json → brandKit.logo: [{"version": "principal", "archivo": "logo/principal.svg"}, {"version": "invertida", …}, {"version": "monocroma", …}, {"version": "simbolo", "archivo": "logo/simbolo.svg"}, {"version": "simbolo_invertido", "archivo": "logo/simbolo-invertido.svg"}]  (el símbolo invertido es el que se ve sobre fondos oscuros)')
    print(f"Y ejecuta: python3 {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'incrustar_fuente.py')} {os.path.join(dest, '*.svg')} --google <Familia>")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nombre")
    ap.add_argument("--tinta")
    ap.add_argument("--acento")
    ap.add_argument("--fondo", default="#FFFFFF")
    ap.add_argument("--oscuro", help="fondo oscuro de la versión invertida (por defecto la tinta)")
    ap.add_argument("--fuente", default="Inter")
    ap.add_argument("--peso", type=int, default=700)
    ap.add_argument("--minusculas", action="store_true")
    ap.add_argument("--tipos", dest="tipos_elegidos", nargs="?", const="", default=None, help="dos tipos separados por coma; sin valor lista los tipos")
    ap.add_argument("--variante", type=int, default=0)
    ap.add_argument("--salida", default="logo-opciones")
    ap.add_argument("--elegir", choices=["a", "b"])
    ap.add_argument("--destino")
    a = ap.parse_args()
    if a.tipos_elegidos == "" and not a.nombre:
        for k, v in TIPOS.items():
            print(f"  {k:9} {v}")
        return 0
    if a.elegir:
        return elegir(a)
    if not (a.nombre and a.tinta and a.acento and a.tipos_elegidos):
        ap.error("hacen falta --nombre, --tinta, --acento y --tipos a,b (o --tipos solo para listarlos; --elegir a|b para quedarte con una)")
    generar(a)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
