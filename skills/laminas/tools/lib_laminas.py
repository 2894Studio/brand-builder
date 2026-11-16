#!/usr/bin/env python3
"""Rejilla, escala tipográfica, firmas gráficas y primitivas SVG del sistema de láminas.
Lienzo 1920 × 1080. Reglas en laminas/references/sistema-laminas.md.
Solo librería estándar. Importa marca_lib desde skills/tokens/tools.
"""
import html
import os
import sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
_TOKENS = os.path.normpath(os.path.join(_AQUI, "..", "..", "tokens", "tools"))
if not os.path.isfile(os.path.join(_TOKENS, "marca_lib.py")):
    sys.exit("No encuentro skills/tokens/tools/marca_lib.py. Instala el plugin completo "
             "(las skills comparten el núcleo de marca.json).")
sys.path.insert(0, _TOKENS)
import marca_lib as m  # noqa: E402

W, H = 1920, 1080
MARGIN_X, MARGIN_Y = 120, 100
COL, GUT = 118, 24

Y_KICKER, Y_TITLE, Y_RULE, Y_LEAD, Y_BODY = 120, 160, 352, 384, 470
Y_VIS_TOP, Y_VIS_BOT = 352, 900
Y_FOOT = 946
TITULO_MAX_LINEAS, CUERPO_MAX_LINEAS = 2, 6


def x(n):
    """Inicio (x) de la columna n, 1-indexada."""
    return MARGIN_X + (n - 1) * (COL + GUT)


def span(a, b):
    """(x, ancho) del tramo de columnas a..b."""
    return x(a), (b - a + 1) * COL + (b - a) * GUT


assert x(12) + COL == W - MARGIN_X, "la columna 12 no cierra en el margen"
assert span(1, 12) == (120, 1680)
assert span(1, 5) == (120, 686)
assert span(6, 12) == (830, 970)
assert span(7, 12) == (972, 828)


def esc(s):
    return html.escape(str(s), quote=False)


class Estilo:
    """Todo lo que varía de una marca a otra: paleta, fuentes y firma gráfica."""

    def __init__(self, marca):
        self.marca = marca
        self.nombre = marca["nombre"]
        p = m.paleta(marca)
        self.base, self.ink, self.brand = p["fondo"], p["texto"], p["primario"]
        self.acento = p.get("acento", p["primario"])
        self.neutro = p.get("neutro") or m.mezclar(p["texto"], p["fondo"], 0.8)
        self.muted = m.mezclar(self.ink, self.base, 0.38)
        if m.contraste(self.muted, self.base) < 4.5:
            self.muted = self.ink
        self.sobre_marca = m.mejor_sobre(self.brand, [self.base, self.ink])
        self.territorio = m.territorio(marca)
        self.firma = m.FIRMAS[self.territorio]
        tp = marca.get("tipografia", {})
        self.f_tit = tp.get("titulos", {}).get("familia", "DejaVu Sans")
        self.f_txt = tp.get("texto", {}).get("familia", "DejaVu Sans")
        self.avisos = []

    def fam(self, rol):
        f = self.f_tit if rol == "titulos" else self.f_txt
        return f"'{f}', 'DejaVu Sans', Arial, sans-serif"

    def aviso(self, msg):
        if msg not in self.avisos:
            self.avisos.append(msg)


# ---------- texto ----------
def ancho_car(size, peso="normal"):
    return size * (0.60 if peso == "bold" else 0.55)


def envolver(txt, size, ancho, peso="normal"):
    """Parte `txt` en líneas que quepan en `ancho` px (estimación por caracteres)."""
    maxc = max(1, int(ancho / ancho_car(size, peso)))
    out = []
    for parrafo in str(txt).split("\n"):
        linea = ""
        for palabra in parrafo.split():
            prueba = (linea + " " + palabra).strip()
            if len(prueba) <= maxc:
                linea = prueba
            else:
                if linea:
                    out.append(linea)
                linea = palabra
        out.append(linea)
    return out


def t(est, lineas, xx, yy, size, fill=None, peso="normal", estilo="normal", anchor="start",
      lh=1.4, espaciado=0, rol="texto"):
    """Una o varias líneas de texto. `yy` es el borde superior de la primera línea."""
    if isinstance(lineas, str):
        lineas = lineas.split("\n")
    fill = fill or est.ink
    out = []
    for i, ln in enumerate(lineas):
        out.append(
            f'<text x="{xx}" y="{round(yy + size + i * size * lh, 1)}" font-family="{esc(est.fam(rol))}" '
            f'font-size="{size}" font-weight="{peso}" font-style="{estilo}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{espaciado}">{esc(ln)}</text>')
    return "".join(out)


def bloque(est, txt, xx, yy, size, ancho, maxl, fill=None, peso="normal", estilo="normal", lh=1.5,
           rol="texto", que="cuerpo"):
    """Texto envuelto con tope de líneas. Si se pasa, recorta y avisa (regla: lo que no quepa va al documento)."""
    ls = envolver(txt, size, ancho, peso)
    if len(ls) > maxl:
        est.aviso(f"{que} recortado de {len(ls)} a {maxl} líneas: «{str(txt)[:40]}…»")
        ls = ls[:maxl]
        ls[-1] = ls[-1].rstrip(" ,;:") + "…"
    return t(est, ls, xx, yy, size, fill, peso, estilo, lh=lh, rol=rol), len(ls)


def t_sangre(est, txt, xx, yy, size, fill, anchor="start", peso="bold", rol="titulos", op=1):
    """Texto DECORATIVO que se sale del lienzo (tipografía recortada a sangre). No lleva información:
    es aria-hidden y las comprobaciones de márgenes lo ignoran. `yy` es la línea base."""
    return (f'<text data-sangre="1" aria-hidden="true" x="{xx}" y="{yy}" font-family="{esc(est.fam(rol))}" '
            f'font-size="{size}" font-weight="{peso}" fill="{fill}" text-anchor="{anchor}" opacity="{op}">{esc(txt)}</text>')


def rect(xx, yy, w, h, fill, rx=0, op=1, stroke=None):
    s = f' stroke="{stroke}"' if stroke else ""
    return f'<rect x="{xx}" y="{yy}" width="{w}" height="{h}" fill="{fill}" rx="{rx}" opacity="{op}"{s}/>'


_pid = [0]


def foto(est, xx, yy, w, h, etiqueta="fotografía", rx=None):
    """Marcador de fotografía (no se genera imagen hasta que haya una real)."""
    _pid[0] += 1
    rx = est.firma["radio"] if rx is None else rx
    pid = f"p{_pid[0]}"
    return (f'<defs><pattern id="{pid}" width="18" height="18" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate(35)"><rect width="18" height="18" fill="{est.neutro}"/>'
            f'<rect width="7" height="18" fill="{m.mezclar(est.neutro, est.ink, 0.12)}"/></pattern></defs>'
            f'<rect x="{xx}" y="{yy}" width="{w}" height="{h}" fill="url(#{pid})" rx="{rx}"/>'
            + rect(xx + 16, yy + h - 56, min(w - 32, 28 + len(etiqueta) * 12), 40, est.base, rx=2)
            + t(est, etiqueta, xx + 28, yy + h - 48, 20, est.muted))


def svg(cuerpo, fondo, titulo=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(titulo)}">'
            f'{rect(0, 0, W, H, fondo)}{cuerpo}</svg>')


# ---------- firma gráfica ----------
def firma_filete(est, xx=MARGIN_X, yy=Y_RULE, color=None):
    c = color or est.brand
    tipo = est.firma["filete"]
    if tipo == "barra":
        return rect(xx, yy, 72, 4, c)
    if tipo == "linea":
        return rect(xx, yy, span(1, 5)[1], 1, c)
    if tipo == "trazo":
        d = f"M{xx} {yy + 6} C{xx + 30} {yy - 2}, {xx + 60} {yy + 10}, {xx + 120} {yy + 3}"
        return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round"/>'
    if tipo == "onda":
        d = f"M{xx} {yy + 6} q15 -12 30 0 t30 0 t30 0 t30 0"
        return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"/>'
    return rect(xx, yy - 4, 120, 14, c)          # bloque


ROMANOS = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV"]


def numeracion(est, n, total, fill=None, xr=None):
    fill = fill or est.ink
    tipo = est.firma["numeracion"]
    xr = xr or (x(12) + COL)
    if tipo == "romana":
        txt = ROMANOS[n] if n < len(ROMANOS) else str(n)
    elif tipo == "guiones":
        txt = f"–{n:02d}–"
    elif tipo == "mono":
        txt = f"{n:02d} / {total:02d}"
    elif tipo == "circulo":
        return (f'<circle cx="{xr - 16}" cy="{Y_FOOT + 12}" r="22" fill="none" stroke="{fill}" stroke-width="2"/>'
                + t(est, f"{n}", xr - 16, Y_FOOT + 1, 20, fill, anchor="middle"))
    else:  # margen
        return t(est, f"{n:02d}", xr, 100, 64, est.brand, "bold", anchor="end", rol="titulos")
    return t(est, txt, xr, Y_FOOT, 20, fill, anchor="end")


def pie(est, n, total, fill=None, xr=None):
    fill = fill or est.ink
    return t(est, est.nombre, MARGIN_X, Y_FOOT, 20, fill, espaciado=2, rol="titulos") + numeracion(est, n, total, fill, xr)


# ---------- logo ----------
def logo(est, xx, yy, w, h, version="principal", fill=None, archivos=None, base_dir=None, ancla="middle"):
    """Coloca el archivo de logo si hay uno para esa versión; si no, un logotipo provisional.
    `archivos` ya viene filtrado a ficheros que existen (lo hace generar_kit)."""
    archivos = archivos or {}
    arch = archivos.get(version)
    if arch:
        return (f'<image x="{xx}" y="{yy}" width="{w}" height="{h}" href="{esc(arch)}" '
                f'preserveAspectRatio="xMidYMid meet"/>')
    est.aviso("logotipo PROVISIONAL (solo el nombre en tipografía): falta el archivo del logo aprobado")
    # mayúsculas en negrita miden ~0.78 × el cuerpo; se deja un 10 % de aire a cada lado
    size = int(min(h * 0.62, w * 0.9 / (max(1, len(est.nombre)) * 0.78)))
    cy = yy + (h - size) / 2
    px = xx + w / 2 if ancla == "middle" else xx
    return t(est, est.nombre, px, cy, size, fill or est.ink, "bold", anchor=ancla,
             espaciado=-2, rol="titulos", lh=1.0)
