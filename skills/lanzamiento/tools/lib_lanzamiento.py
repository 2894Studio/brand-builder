# Copyright (c) 2026 2894 Studio · MIT
"""Utilidades compartidas del paso «lanzamiento»: lee marca.json y devuelve colores, fuentes y logos listos para maquetar."""
import base64
import html
import json
import os


def cargar_marca(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


# ---- color -----------------------------------------------------------------------------------
def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in rgb)


def luminancia(h):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = _rgb(h)
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = sorted([luminancia(a), luminancia(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def oscurecer(h, factor=0.55):
    return _hex([v * factor for v in _rgb(h)])


def aclarar(h, factor=0.85):
    return _hex([v + (255 - v) * factor for v in _rgb(h)])


def legible(fondo, claro="#FFFFFF", oscuro="#12141A"):
    """Texto que mejor se lee sobre «fondo»."""
    return claro if contraste(claro, fondo) >= contraste(oscuro, fondo) else oscuro


def colores(m):
    por_rol = {c["rol"]: c for c in m.get("visual", {}).get("colores", [])}
    kit = m.get("brandKit", {})
    prim = por_rol.get("primario", {}).get("hex", "#2B63F0")
    fondo = por_rol.get("fondo", {}).get("hex", "#F4F5F7")
    texto = por_rol.get("texto", {}).get("hex", "#12141A")
    acento = por_rol.get("acento", {}).get("hex", prim)
    neutro = kit.get("neutro", {}).get("hex") or aclarar(prim, 0.88)
    profundo = kit.get("profundo", {}).get("hex") or oscurecer(prim, 0.5)
    nombres = {
        "primario": por_rol.get("primario", {}).get("nombre", "Primario"),
        "fondo": por_rol.get("fondo", {}).get("nombre", "Fondo"),
        "acento": por_rol.get("acento", {}).get("nombre", "Acento"),
        "texto": por_rol.get("texto", {}).get("nombre", "Texto"),
        "neutro": kit.get("neutro", {}).get("nombre", "Neutro"),
        "profundo": kit.get("profundo", {}).get("nombre", "Profundo"),
    }
    return {"primario": prim, "fondo": fondo, "texto": texto, "acento": acento, "neutro": neutro, "profundo": profundo, "nombres": nombres}


# ---- tipografía --------------------------------------------------------------------------------
def fuentes(m):
    t = m.get("tipografia", {})
    tit = t.get("titulos", {}) or {}
    txt = t.get("texto", {}) or {}
    return {
        "titulos": tit.get("familia", "Inter"), "texto": txt.get("familia", tit.get("familia", "Inter")),
        "pesos_titulos": tit.get("pesos", [400, 700]), "pesos_texto": txt.get("pesos", [400, 600]),
        "google": "google" in (tit.get("fuente", "") + txt.get("fuente", "")).lower(),
    }


def enlace_google_fonts(m):
    """<link> a Google Fonts con las familias de la marca (solo si la marca dice que vienen de ahí). Vacío si no."""
    f = fuentes(m)
    if not f["google"]:
        return ""
    fams = {}
    for fam, pesos in ((f["titulos"], f["pesos_titulos"]), (f["texto"], f["pesos_texto"])):
        fams.setdefault(fam, set()).update(int(p) for p in pesos)
    q = "&".join("family=%s:wght@%s" % (fam.replace(" ", "+"), ";".join(str(p) for p in sorted(ps))) for fam, ps in fams.items())
    return f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{q}&display=swap">'


# ---- logos -------------------------------------------------------------------------------------
def logos(m, base):
    """{versión: ruta absoluta} de los logos que existen en disco."""
    out = {}
    for l in m.get("brandKit", {}).get("logo", []):
        ruta = l.get("archivo", "")
        p = ruta if os.path.isabs(ruta) else os.path.join(base, ruta)
        if os.path.exists(p):
            out[l.get("version", os.path.basename(p))] = p
    return out


def data_uri(ruta):
    ext = os.path.splitext(ruta)[1].lower()
    mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "application/octet-stream")
    with open(ruta, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def esc(t):
    return html.escape(str(t), quote=True)


# ---- CSS común -----------------------------------------------------------------------------------
def css_variables(m):
    c, f = colores(m), fuentes(m)
    return (":root{--primario:%(primario)s;--fondo:%(fondo)s;--texto:%(texto)s;--acento:%(acento)s;--neutro:%(neutro)s;--profundo:%(profundo)s;"
            "--sobre-primario:%(sp)s;--sobre-profundo:%(spf)s;--f-titulos:'%(ft)s',system-ui,sans-serif;--f-texto:'%(fx)s',system-ui,sans-serif}" % {
                **c, "sp": legible(c["primario"]), "spf": legible(c["profundo"]), "ft": f["titulos"], "fx": f["texto"]})


COMPONENTES_CSS = """
*{box-sizing:border-box}body{margin:0;font-family:var(--f-texto);color:var(--texto)}
.titular{font-family:var(--f-titulos);letter-spacing:-.035em;line-height:1.02;margin:0;font-weight:400}.titular b{font-weight:700}
.etiqueta{font-size:20px;font-weight:600;letter-spacing:.12em;text-transform:uppercase}
.campo{background:linear-gradient(170deg,var(--primario) 0%,var(--profundo) 100%);color:var(--sobre-primario)}
.cristal{position:absolute;border-radius:28px;background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.38);backdrop-filter:blur(14px);padding:20px 26px;box-shadow:0 18px 50px rgba(8,25,110,.28);color:#fff}
.cristal small{display:block;font-size:24px;font-weight:500}.cristal b{display:block;font-size:56px;font-weight:600;letter-spacing:-.03em;line-height:1.05;margin-top:4px}
.foto{position:absolute;border-radius:34px;overflow:hidden;border:2px solid rgba(255,255,255,.55);box-shadow:0 22px 60px rgba(5,15,70,.4)}.foto img{width:100%;height:100%;object-fit:cover;display:block}
.rotulo{position:absolute;border-radius:20px;background:rgba(10,20,60,.7);border:1.5px solid rgba(255,255,255,.4);padding:10px 16px;color:#fff;font-size:22px;line-height:1.25}.rotulo b{display:block;font-size:25px;font-weight:600}
.telefono{position:absolute;border-radius:72px;background:#07090F;padding:14px;box-shadow:0 40px 90px rgba(5,15,70,.5),inset 0 0 0 3px #232734}
.pantalla{width:100%;height:100%;border-radius:60px;background:#fff;color:var(--texto);overflow:hidden;position:relative;padding:22px 26px}
.pie-ejemplo{position:absolute;right:70px;bottom:84px;font-size:20px;color:rgba(255,255,255,.8);text-align:right;line-height:1.35}
"""


# ---- fotos (salida de preparar_fotos.py) -------------------------------------------------------
def elegir_fotos(carpeta):
    """{'equipo': {...}, 'retrato': {...}, ...} con las rutas de los recortes. Coge la primera foto de cada tipo."""
    ruta = os.path.join(carpeta, "manifiesto.json")
    if not os.path.exists(ruta):
        return {}
    out = {}
    for reg in json.load(open(ruta, encoding="utf-8")):
        stem = os.path.splitext(reg["archivo"])[0].lower()
        for tipo in ("equipo", "retrato", "producto", "local"):
            if stem.startswith(tipo) and tipo not in out:
                rec = reg.get("recortes", {})
                out[tipo] = {"archivo": reg["archivo"], "origen": reg.get("origen"), "pie": reg.get("pie"),
                             "ruta_3x4": os.path.join(carpeta, rec.get("3x4", "")), "ruta_4x3": os.path.join(carpeta, rec.get("4x3", "")),
                             "ruta_1x1": os.path.join(carpeta, rec.get("1x1", ""))}
    return out


# ---- utilidades de piezas ----------------------------------------------------------------------
def iniciales(texto):
    p = [w for w in str(texto).replace("/", " ").split() if w]
    return (p[0][0] + (p[1][0] if len(p) > 1 else p[0][1:2])).upper() if p else "?"


def base_avatar(prim):
    """Color de avatar sobre el que el texto blanco se lee (≥ 4,5:1): el primario, oscurecido si hace falta."""
    h = prim
    for f in (1.0, 0.85, 0.7, 0.55, 0.4):
        h = oscurecer(prim, f)
        if contraste("#FFFFFF", h) >= 4.5:
            return h
    return h


def con_negrita(texto):
    """Escapa el texto y deja pasar <b>…</b> (para la palabra clave del titular)."""
    t = esc(texto)
    return t.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")


def haversine_km(a, b):
    import math
    (lo1, la1), (lo2, la2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


CAMPO_LUZ = """
.campo{background:radial-gradient(900px 700px at 22% 62%,var(--luz) 0%,rgba(255,255,255,0) 60%),linear-gradient(170deg,var(--primario) 0%,var(--medio) 45%,var(--profundo) 100%);color:var(--sobre-primario)}
"""


def css_luz(m):
    c = colores(m)
    return ":root{--luz:%s;--medio:%s;--suave:%s}" % (aclarar(c["primario"], 0.35), oscurecer(c["primario"], 0.7), suave(c["texto"], c["neutro"])) + CAMPO_LUZ


def mezclar(h1, h2, t):
    a, b = _rgb(h1), _rgb(h2)
    return _hex([a[i] * (1 - t) + b[i] * t for i in range(3)])


def suave(texto, fondo):
    """Gris suave derivado del color de texto que sigue contrastando ≥ 4,6:1 con blanco y con «fondo» (para detalles y subtítulos)."""
    for t in (0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.1, 0.0):
        h = mezclar(texto, "#FFFFFF", t)
        if contraste(h, "#FFFFFF") >= 4.6 and contraste(h, fondo) >= 4.6:
            return h
    return texto


# ---- tema claro / oscuro --------------------------------------------------------------------------
def tema_css(m, tema):
    """Sobrescribe el campo, las tarjetas y los anillos para el tema claro (fondo de la marca, texto oscuro, tarjetas blancas)."""
    if tema != "claro":
        return ""
    c = colores(m)
    halo = mezclar(c["fondo"], c["primario"], 0.12)
    return (f".campo{{background:radial-gradient(900px 700px at 78% 6%,{halo} 0%,{c['fondo']} 72%);color:{c['texto']}}}"
            f".cristal{{background:#fff;border:1.5px solid {c['neutro']};color:{c['texto']};backdrop-filter:none;box-shadow:0 14px 36px rgba(20,30,60,.10)}}"
            f".anillo{{border-color:{c['neutro']}!important}}.desvanecido{{display:none}}.titular{{color:{c['texto']}}}"
            f".pie-ejemplo{{color:{suave(c['texto'], c['fondo'])}}}")


def logo_html(m, lg, tema, nombre):
    """El logo adecuado al tema: invertido sobre fondo oscuro, principal sobre claro. Si falta, el nombre en texto."""
    clave = "principal" if tema == "claro" else "invertida"
    if clave in lg:
        return f'<img class="logo" src="{data_uri(lg[clave])}" alt="{esc(nombre)}">'
    return f'<div class="logo-texto">{esc(nombre)}</div>'
