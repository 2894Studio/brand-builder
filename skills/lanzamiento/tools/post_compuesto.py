#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Post a medida: el agente DISEÑA la composición (qué elementos, dónde, de qué tamaño) y el script la dibuja con la paleta y las fuentes de la marca.

Uso:  python3 post_compuesto.py marca.json --spec composicion-post-1.json --salida lanzamiento/post-1-que-es.html [--fotos lanzamiento/fotos] [--lienzo post|cuadrado|historia]
      python3 post_compuesto.py --ejemplo                (imprime una especificación de ejemplo)

La especificación es un JSON; las coordenadas son píxeles del lienzo (post 1080×1440, cuadrado 1080×1080, historia 1080×1920):
{
  "concepto": {"referencias": ["R19", "R23"], "decisiones": "tres líneas: qué se toma de esas referencias y cómo se traduce aquí"},
  "fondo": {"color": "primario"}   o   {"degradado": ["primario", "profundo"], "angulo": 160},
  "elementos": [
    {"tipo": "texto", "texto": "Frase con <b>palabra clave</b>", "x": 70, "y": 150, "ancho": 640, "tam": 104, "peso": 800, "color": "texto", "familia": "titulos", "interlineado": 1.02, "tracking": -0.03, "alinear": "izq"},
    {"tipo": "palabra", "texto": "luz", "x": 600, "y": -60, "tam": 640, "color": "fondo", "giro": 90, "opacidad": 1},     (palabra enorme recortada por el borde)
    {"tipo": "forma", "forma": "circulo|rect|semicirculo|pastilla|triangulo", "x": 0, "y": 0, "w": 300, "h": 300, "color": "acento", "giro": 0, "radio": 24},
    {"tipo": "firma", "patron": "horizonte|puntos|diagonal|ondas", "x": 70, "y": 900, "w": 420, "h": 300, "color": "acento", "opacidad": 0.9},
    {"tipo": "foto", "cual": "retrato|equipo|producto|local", "x": 70, "y": 700, "w": 560, "h": 560, "marco": "sello|redondeado|recto|circulo", "giro": -4},
    {"tipo": "insignia", "x": 470, "y": 60, "d": 210, "giro": -12, "color": "fondo"},        (insignia festoneada con el símbolo del logo)
    {"tipo": "cifra", "valor": "5", "unidad": "alumnos por grupo", "x": 70, "y": 300, "tam": 440, "color": "acento"},
    {"tipo": "simbolo", "x": 560, "y": 700, "w": 700, "giro": -10, "opacidad": 1},                 (el símbolo del logo a gran tamaño, puede salirse del lienzo; sobre fondo oscuro usa «simbolo_invertido» si el logo lo tiene; "tema": "oscuro|claro" lo fuerza)
    {"tipo": "linea", "x": 70, "y": 120, "w": 60, "grosor": 5, "color": "acento"},
    {"tipo": "logo", "x": 70, "y": 1310, "h": 62}
  ]
}
Colores: primario, profundo, acento, fondo, texto, neutro, blanco o un #hex. Los elementos se pintan en el orden de la lista (el último queda encima).
Sin `concepto.referencias` el script se niega: cada composición cita las reglas de gusto (R1…Rn de gusto.py reglas) que traduce.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402
import post_expresivo as X  # noqa: E402

GRAFICOS = ("forma", "firma", "foto", "insignia", "simbolo", "palabra")
LIENZOS = {"post": (1080, 1440), "cuadrado": (1080, 1080), "historia": (1080, 1920)}
EJEMPLO = {
    "concepto": {"referencias": ["R19", "R23"], "decisiones": "Directo y minimalista con un color llamativo y una imagen principal (R19, R23): palabra gigante recortada y una foto con marco."},
    "fondo": {"color": "primario"},
    "elementos": [
        {"tipo": "palabra", "texto": "luz", "x": 560, "y": -40, "tam": 700, "color": "fondo", "giro": 90},
        {"tipo": "linea", "x": 70, "y": 140, "w": 60, "grosor": 5, "color": "acento"},
        {"tipo": "texto", "texto": "Titular con <b>palabra clave</b>", "x": 70, "y": 170, "ancho": 470, "tam": 92, "peso": 300, "color": "blanco"},
        {"tipo": "foto", "cual": "retrato", "x": 70, "y": 700, "w": 560, "h": 560, "marco": "sello", "giro": -4},
        {"tipo": "logo", "x": 70, "y": 1330, "h": 58}
    ],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca", nargs="?")
    ap.add_argument("--spec")
    ap.add_argument("--salida")
    ap.add_argument("--fotos")
    ap.add_argument("--lienzo", choices=list(LIENZOS), default="post")
    ap.add_argument("--ejemplo", action="store_true")
    a = ap.parse_args()
    if a.ejemplo:
        print(json.dumps(EJEMPLO, ensure_ascii=False, indent=1))
        return 0
    if not (a.marca and a.spec and a.salida):
        ap.error("hacen falta marca.json, --spec y --salida (o --ejemplo)")
    spec = json.load(open(a.spec, encoding="utf-8"))
    refs = (spec.get("concepto") or {}).get("referencias") or []
    if not refs or not (spec["concepto"].get("decisiones") or "").strip():
        sys.exit("La composición necesita «concepto»: {\"referencias\": [\"R19\", …], \"decisiones\": \"qué se toma de ellas y cómo se traduce aquí\"} (reglas de gusto.py reglas)")
    if not any(e.get("tipo") in GRAFICOS for e in spec.get("elementos", [])):
        sys.exit("La composición es solo texto. Añade al menos un elemento gráfico (" + ", ".join(GRAFICOS) + "): una forma, la firma, una foto, el símbolo del logo a gran tamaño, una insignia o una palabra gigante recortada. Un post sin nada gráfico es una plantilla con otro nombre.")
    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c = L.colores(m)
    lg = L.logos(m, base)
    nombre = m.get("nombre", "Marca")
    W, H = LIENZOS[a.lienzo]
    fotos = L.elegir_fotos(a.fotos) if a.fotos else {}
    paleta = {"primario": c["primario"], "profundo": c["profundo"], "acento": c["acento"], "fondo": c["fondo"], "texto": c["texto"], "neutro": c["neutro"], "blanco": "#FFFFFF"}

    def col(v, defecto="texto"):
        v = v or defecto
        if v is None:
            return paleta["texto"]
        return paleta.get(v, v if str(v).startswith("#") else paleta.get(defecto, paleta["texto"]))

    fam = lambda f: "var(--f-titulos)" if f != "texto" else "var(--f-texto)"  # noqa: E731
    fo = spec.get("fondo", {"color": "fondo"})
    fondo_css = (f"linear-gradient({fo.get('angulo', 160)}deg,{col(fo['degradado'][0])},{col(fo['degradado'][1])})" if fo.get("degradado") else col(fo.get("color"), "fondo"))
    partes, avisos, css_extra = [], [], ""
    base_bg = col((fo.get("degradado") or [fo.get("color", "fondo")])[0], "fondo")
    auto_fg = L.legible(base_bg)      # color de texto por defecto: el que contrasta con el fondo
    simbolo = f'<img src="{L.data_uri(lg["simbolo"])}" alt="" style="width:62%;height:62%;object-fit:contain">' if "simbolo" in lg else ""
    for i, e in enumerate(spec.get("elementos", [])):
        t = e.get("tipo")
        x, y = e.get("x", 0), e.get("y", 0)
        giro = f"transform:rotate({e.get('giro', 0)}deg);" if e.get("giro") else ""
        if t == "texto":
            al = {"izq": "left", "centro": "center", "der": "right"}.get(e.get("alinear", "izq"), "left")
            partes.append(f'<div class="t" style="left:{x}px;top:{y}px;width:{e.get("ancho", 600)}px;font:{e.get("peso", 700)} {e.get("tam", 80)}px/{e.get("interlineado", 1.05)} {fam(e.get("familia", "titulos"))};'
                          f'letter-spacing:{e.get("tracking", -0.03)}em;color:{col(e.get("color"), None) if e.get("color") else auto_fg};text-align:{al};{"text-transform:uppercase;" if e.get("mayusculas") else ""}{giro}">{L.con_negrita(e.get("texto", ""))}</div>')
        elif t == "palabra":
            partes.append(f'<div class="g" data-bleed="1" data-decorativo="1" aria-hidden="true" style="left:{x}px;top:{y}px;font:900 {e.get("tam", 600)}px/.8 var(--f-titulos);color:{col(e.get("color"), "fondo")};opacity:{e.get("opacidad", 1)};'
                          f'{"writing-mode:vertical-rl;transform:rotate(180deg);" if e.get("giro") == 90 else giro}">{L.esc(e.get("texto", nombre))}</div>')
        elif t == "forma":
            w_, h_, k = e.get("w", 200), e.get("h", 200), e.get("forma", "rect")
            est = {"circulo": "border-radius:50%;", "pastilla": "border-radius:999px;", "rect": f"border-radius:{e.get('radio', 0)}px;", "semicirculo": f"border-radius:{w_}px {w_}px 0 0;", "triangulo": "clip-path:polygon(50% 0,100% 100%,0 100%);"}.get(k, "")
            borde = f"border:{e['borde']}px solid {col(e.get('color_borde', e.get('color')))};background:transparent;" if e.get("borde") else f"background:{col(e.get('color'), 'acento')};"
            partes.append(f'<div class="f" data-decorativo="1" style="left:{x}px;top:{y}px;width:{w_}px;height:{h_}px;{est}{borde}{giro}opacity:{e.get("opacidad", 1)}"></div>')
        elif t == "firma":
            w_, h_ = e.get("w", 420), e.get("h", 300)
            svg = L.firma_svg(e.get("patron", "horizonte"), col(e.get("color"), "acento"), w_, h_)
            partes.append(f'<div class="f" data-decorativo="1" style="left:{x}px;top:{y}px;opacity:{e.get("opacidad", 1)};{giro}">{svg}</div>')
        elif t == "foto":
            ruta = None
            if e.get("archivo") and os.path.exists(e["archivo"]):
                ruta = e["archivo"]
            elif e.get("cual") in fotos:
                w_, h_ = e.get("w", 500), e.get("h", 500)
                clave = "ruta_3x4" if h_ > w_ * 1.1 else ("ruta_4x3" if w_ > h_ * 1.1 else "ruta_1x1")
                ruta = fotos[e["cual"]].get(clave)
            if not ruta or not os.path.exists(ruta):
                avisos.append(f"elemento {i + 1} (foto): no hay foto «{e.get('cual', e.get('archivo'))}»; se omite")
                continue
            w_, h_, marco = e.get("w", 500), e.get("h", 500), e.get("marco", "redondeado")
            if marco == "sello":
                partes.append(f'<div class="s" style="left:{x}px;top:{y}px;width:{w_}px;height:{h_}px;{giro}clip-path:path(\'{X.sello_path(w_, h_)}\');background:{col(e.get("color_marco"), "acento")}">'
                              f'<div style="position:absolute;inset:20px;background:url({L.data_uri(ruta)}) center/cover"></div></div>')
            else:
                rad = {"circulo": "50%", "recto": "0", "redondeado": f"{e.get('radio', 28)}px"}.get(marco, "28px")
                partes.append(f'<div class="s" style="left:{x}px;top:{y}px;width:{w_}px;height:{h_}px;border-radius:{rad};overflow:hidden;{giro}background:url({L.data_uri(ruta)}) center/cover"></div>')
        elif t == "simbolo":
            if "simbolo" not in lg:
                sys.exit(f"elemento {i + 1} (simbolo): el logo no tiene versión «simbolo». Genera uno con skills/identidad/tools/simbolo_geometrico.py (o pídelo en el paso de identidad) y regístralo en marca.json → brandKit.logo.")
            w_ = e.get("w", 600)
            oscuro_ = (e.get("tema") == "oscuro") or (e.get("tema") is None and L.luminancia(base_bg) < 0.25)
            clave = "simbolo_invertido" if oscuro_ and "simbolo_invertido" in lg else "simbolo"
            if oscuro_ and clave == "simbolo":
                avisos.append(f"elemento {i + 1} (simbolo): fondo oscuro y el logo no tiene «simbolo_invertido»; el símbolo puede perderse (registra simbolo_invertido en brandKit.logo)")
            partes.append(f'<div class="f" data-decorativo="1" data-bleed="1" style="left:{x}px;top:{y}px;width:{w_}px;height:{e.get("h", w_)}px;opacity:{e.get("opacidad", 1)};{giro}">'
                          f'<img src="{L.data_uri(lg[clave])}" alt="" style="width:100%;height:100%;object-fit:contain"></div>')
        elif t == "insignia":
            d = e.get("d", 200)
            contenido = simbolo or ""
            if not contenido:
                avisos.append(f"elemento {i + 1} (insignia): el logo no tiene versión «simbolo»; la insignia va sin contenido (no se usa una inicial)")
            partes.append(f'<div class="s" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;{giro}clip-path:path(\'{X.sello_circular(d / 2)}\');background:{col(e.get("color"), "fondo")};display:grid;place-items:center;box-shadow:inset 0 0 0 10px {col(e.get("color_borde"), "acento")}">{contenido}</div>')
        elif t == "cifra":
            partes.append(f'<div class="t" style="left:{x}px;top:{y}px;font:800 {e.get("tam", 400)}px/.86 var(--f-titulos);letter-spacing:-.07em;color:{col(e.get("color"), "acento")}">{L.esc(e.get("valor", ""))}</div>')
            if e.get("unidad"):
                partes.append(f'<div class="t" style="left:{x}px;top:{y + int(e.get("tam", 400) * 0.95)}px;width:{e.get("ancho_unidad", 800)}px;font:600 {e.get("tam_unidad", 60)}px/1.1 var(--f-titulos);letter-spacing:-.03em;color:{col(e.get("color_unidad"), None) if e.get("color_unidad") else auto_fg}">{L.esc(e["unidad"])}</div>')
        elif t == "linea":
            partes.append(f'<div class="f" data-decorativo="1" style="left:{x}px;top:{y}px;width:{e.get("w", 60)}px;height:{e.get("grosor", 4)}px;background:{col(e.get("color"), "acento")}"></div>')
        elif t == "estrellas":
            partes.append(f'<div class="f" data-decorativo="1" style="left:{x}px;top:{y}px">{X.estrellas(col(e.get("color"), "acento"))}</div>')
        elif t == "logo":
            var = e.get("variante", "auto")
            fb = col(fo.get("color") or (fo.get("degradado") or ["fondo"])[0], "fondo")
            oscuro = L.luminancia(fb) < 0.3
            clave = var if var in lg else ("invertida" if oscuro and "invertida" in lg else "principal")
            if clave in lg:
                partes.append(f'<img class="f" src="{L.data_uri(lg[clave])}" alt="{L.esc(nombre)}" style="left:{x}px;top:{y}px;height:{e.get("h", 60)}px">')
            else:
                partes.append(f'<div class="t" style="left:{x}px;top:{y}px;font:700 {e.get("h", 60)}px var(--f-titulos);letter-spacing:-.03em;color:{L.legible(fb)}">{L.esc(nombre)}</div>')
        else:
            avisos.append(f"elemento {i + 1}: tipo «{t}» desconocido; se omite")
    css = L.css_variables(m) + f"""
.p{{width:{W}px;height:{H}px;position:relative;overflow:hidden;background:{fondo_css}}}
.t,.g,.f,.s{{position:absolute;margin:0}}.t b{{font-weight:800}}.g{{white-space:nowrap}}
"""
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · composición a medida</title>
<meta name="arquetipo" content="compuesto">
<!-- concepto: {L.esc(', '.join(refs))} · {L.esc(spec['concepto']['decisiones'])} -->
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css}</style>
<div class="p">{''.join(partes)}</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    open(a.salida, "w", encoding="utf-8").write(doc)
    print(f"ok {a.salida}  ({len(partes)} elementos, lienzo {W}×{H})")
    for av in avisos:
        print("  aviso", av)
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--ancho", W, "--alto", H, "--marca", a.marca)
    return 0


if __name__ == "__main__":
    sys.exit(main())
