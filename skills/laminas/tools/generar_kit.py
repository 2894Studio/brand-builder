#!/usr/bin/env python3
"""marca.json (+ kit.json) -> manual de marca como láminas SVG, index.html navegable y PDF opcional.

Uso:  python3 generar_kit.py marca.json [--kit kit.json] [--salida DIR]
Sin kit.json, las láminas de contenido salen con textos «pendiente» y se avisa.
Con `rsvg-convert` instalado se genera además manual-de-marca.pdf. No hace falta para nada más.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_laminas import *  # noqa: F401,F403,E402
import lib_laminas as L  # noqa: E402
import marca_lib as m  # noqa: E402

PEND = "Pendiente de redactar"


def kit_get(kit, ruta, defecto=None):
    n = kit
    for k in ruta.split("."):
        if not isinstance(n, dict) or k not in n:
            return defecto
        n = n[k]
    return n


class Generador:
    def __init__(self, marca, kit, salida, salida_logos_base=None):
        self.est = L.Estilo(marca)
        self.marca, self.kit, self.salida = marca, kit, salida
        # versión -> ruta relativa al SVG de la lámina; el fichero se copia a <salida>/logo/
        self.logos = {}
        for l in marca.get("brandKit", {}).get("logo", []):
            if not isinstance(l, dict):
                continue
            real = os.path.join(salida_logos_base, l["archivo"]) if salida_logos_base else l["archivo"]
            if os.path.isfile(real):
                self.logos[l["version"]] = "../logo/" + os.path.basename(l["archivo"])
            else:
                self.est.aviso(f"el logo «{l['version']}» apunta a {l['archivo']}, que no existe")
        self.laminas = []          # [(nombre_archivo, titulo, svg)]
        self.n = 0                 # numeración de láminas de contenido
        self.total = 12 if kit.get("mockups") else 11   # contenido numerado; portada y divisores no cuentan

    def pend(self, valor, que):
        if valor:
            return valor
        self.est.aviso(f"falta en kit.json: {que}")
        return PEND

    # ---- esqueletos de lámina ----
    def _add(self, slug, titulo, cuerpo, fondo=None):
        self.laminas.append((f"{len(self.laminas) + 1:02d}-{slug}.svg", titulo,
                             L.svg(cuerpo, fondo or self.est.base, titulo)))

    def portada(self):
        e = self.est
        c = [L.rect(0, 0, L.W, L.H, e.ink), L.rect(L.x(10), 0, L.COL * 3 + L.GUT * 2, L.H, e.brand, op=0.9)]
        c.append(L.logo(e, L.MARGIN_X, 300, 900, 240, "invertida", e.base, self.logos, self.salida, ancla="start"))
        c.append(L.firma_filete(e, L.MARGIN_X, 620, e.acento))
        c.append(L.t(e, "Manual de marca", L.MARGIN_X, 668, 34, e.base))
        c.append(L.t(e, self.marca["categoria"], L.MARGIN_X, 726, 24, e.neutro))
        c.append(L.t(e, "v" + str(self.marca.get("brandKit", {}).get("version", "1.0.0")),
                     L.MARGIN_X, L.Y_FOOT, 20, e.neutro))
        self._add("portada", "Portada", "".join(c), e.ink)

    def divisor(self, num, titulo):
        e = self.est
        c = [L.rect(0, 0, L.W, L.H, e.brand)]
        c.append(L.t(e, f"{num:02d}", L.MARGIN_X, 330, 160, e.sobre_marca, "bold", lh=1.0, rol="titulos"))
        c.append(L.firma_filete(e, L.MARGIN_X, 560, e.sobre_marca))
        ls = L.envolver(titulo, 72, span(1, 4)[1], "bold")[:2]
        c.append(L.t(e, ls, L.MARGIN_X, 600, 72, e.sobre_marca, "bold", lh=1.1, rol="titulos"))
        self._add(f"divisor-{L.m.slug(titulo)}", f"Divisor: {titulo}", "".join(c), e.brand)

    def contenido(self, kicker, titulo, lead, cuerpo, visual, slug):
        """Arquetipo C: texto en tramo 1–5, zona visual en 6–12."""
        e = self.est
        self.n += 1
        tx, tw = span(1, 5)
        c = [L.t(e, kicker.upper(), tx, L.Y_KICKER, 20, e.brand, "bold", espaciado=3)]
        tl = L.envolver(titulo, 72, tw, "bold")
        if len(tl) > L.TITULO_MAX_LINEAS:
            e.aviso(f"el título «{titulo}» ocupa {len(tl)} líneas; acórtalo a 2 (la banda es fija)")
            tl = tl[:L.TITULO_MAX_LINEAS]
        c.append(L.t(e, tl, tx, L.Y_TITLE, 72, e.ink, "bold", lh=1.1, rol="titulos"))
        c.append(L.firma_filete(e, tx))
        y_cuerpo = L.Y_BODY
        if lead:
            s, nl = L.bloque(e, lead, tx, L.Y_LEAD, 34, tw, 2, lh=1.35, que="entradilla")
            c.append(s)
            # el cuerpo arranca siempre 24 px por debajo de la entradilla, nunca encima
            y_cuerpo = max(L.Y_BODY, int(L.Y_LEAD + 34 * 1.35 * nl + 24))
        if cuerpo:
            s, _ = L.bloque(e, cuerpo, tx, y_cuerpo, 28, tw, L.CUERPO_MAX_LINEAS, lh=1.5)
            c.append(s)
        c.append(visual)
        c.append(L.pie(e, self.n, self.total))
        self._add(slug, titulo, "".join(c))

    def fichas(self, kicker, titulo, lead, items, slug, dibujar):
        """Arquetipo E: 3–5 fichas desde y=470."""
        e = self.est
        self.n += 1
        k = max(3, min(5, len(items)))
        cw = {3: 544, 4: 402, 5: 316}[k]
        paso = cw + L.GUT
        c = [L.t(e, kicker.upper(), L.MARGIN_X, L.Y_KICKER, 20, e.brand, "bold", espaciado=3)]
        tl = L.envolver(titulo, 72, span(1, 12)[1] // 2, "bold")[:2]
        c.append(L.t(e, tl, L.MARGIN_X, L.Y_TITLE, 72, e.ink, "bold", lh=1.1, rol="titulos"))
        c.append(L.firma_filete(e))
        s, _ = L.bloque(e, lead, L.MARGIN_X, L.Y_LEAD, 34, span(1, 12)[1], 1, lh=1.35, que="entradilla")
        c.append(s)
        for i, it in enumerate(items[:5]):
            c.append(dibujar(it, L.MARGIN_X + i * paso, L.Y_BODY, cw))
        c.append(L.pie(e, self.n, self.total))
        self._add(slug, titulo, "".join(c))

    def especimen(self, titulo, reglas, slug, etiqueta):
        """Arquetipo D: imagen a sangre y panel opaco con todo el texto."""
        e = self.est
        self.n += 1
        c = [L.foto(e, 760, 0, L.W - 760, L.H, etiqueta, rx=0), L.rect(0, 0, 760, L.H, e.base)]   # la imagen real irá a sangre bajo el panel
        tl = L.envolver(titulo, 72, 520, "bold")[:2]
        c.append(L.t(e, tl, L.MARGIN_X, L.Y_TITLE, 72, e.ink, "bold", lh=1.1, rol="titulos"))
        c.append(L.firma_filete(e))
        y = L.Y_LEAD + 40
        for i, r in enumerate(reglas[:5]):
            s, nl = L.bloque(e, f"{i + 1}. {r}", L.MARGIN_X, y, 26, 520, 3, lh=1.4, que="regla")
            c.append(s)
            y += int(26 * 1.4 * nl) + 22
        c.append(L.pie(e, self.n, self.total, xr=640))      # dentro del panel, nunca sobre la imagen
        self._add(slug, titulo, "".join(c))

    # ---- láminas concretas ----
    def la_marca(self):
        e, k = self.est, self.kit
        valores = k.get("valores") or []
        if not valores:
            self.pend(None, "valores (3–4, cada uno con una frase)")
            valores = [{"nombre": "Valor", "frase": PEND}] * 3
        vx, vw = span(6, 12)
        vis, y = [], L.Y_VIS_TOP
        alto = (L.Y_VIS_BOT - L.Y_VIS_TOP - 24 * (len(valores[:4]) - 1)) // len(valores[:4])
        for v in valores[:4]:
            vis.append(L.rect(vx, y, vw, alto, e.base, rx=e.firma["radio"], stroke=e.neutro))
            vis.append(L.t(e, v.get("nombre", ""), vx + 28, y + 22, 28, e.brand, "bold", rol="titulos"))
            s, _ = L.bloque(e, v.get("frase", ""), vx + 28, y + 66, 24, vw - 56, 2, lh=1.4, que="valor")
            vis.append(s)
            y += alto + 24
        pub = self.marca.get("publico") or self.pend(None, "«publico» en marca.json")
        cuerpo = f"Para {pub}."
        self.contenido("La marca", "Qué prometemos", self.pend(k.get("promesa"), "promesa"), cuerpo,
                       "".join(vis), "la-marca")

    def logo_principal(self):
        e = self.est
        vx, vw = span(6, 12)
        vis = [L.rect(vx, L.Y_VIS_TOP, vw, 548, e.base, rx=e.firma["radio"], stroke=e.neutro),
               L.logo(e, vx + 140, L.Y_VIS_TOP + 100, vw - 280, 348, "principal", e.ink, self.logos, self.salida)]
        reglas = ("Área de respeto: la altura de la inicial.\nTamaño mínimo: 25 mm en impreso, 96 px en pantalla.\n"
                  "Una sola tinta: marca, tinta o base.\nNunca rotado, estirado ni con sombra.")
        self.contenido("Identidad", "Logo", "La marca principal, con aire.", reglas, "".join(vis), "logo")

    def versiones(self):
        e = self.est
        v = [("Principal", "principal", e.base, e.ink), ("Invertida", "invertida", e.brand, e.sobre_marca),
             ("Monocroma", "monocroma", e.base, e.ink), ("Símbolo", "simbolo", e.base, e.brand)]

        def ficha(it, xx, yy, cw):
            nombre, clave, fondo, tinta = it
            return (L.rect(xx, yy, cw, 300, fondo, rx=e.firma["radio"], stroke=e.neutro)
                    + L.logo(e, xx + 20, yy + 40, cw - 40, 220, clave, tinta, self.logos, self.salida)
                    + L.t(e, nombre, xx, yy + 320, 28, e.ink, "bold", rol="titulos"))
        self.fichas("Identidad", "Versiones", "Cuatro versiones, mismos archivos en todas partes.", v,
                    "versiones", ficha)

    def paleta(self):
        e = self.est
        n = m.nombres_color(self.marca)
        items = [("Base", e.base, n.get("fondo", ""), "fondo"), ("Tinta", e.ink, n.get("texto", ""), "texto"),
                 ("Marca", e.brand, n.get("primario", ""), "primario")]
        if "acento" in m.paleta(self.marca):
            items.append(("Acento", e.acento, n.get("acento", ""), "acento: máximo el 10 %"))
        if "neutro" in m.paleta(self.marca):
            items.append(("Neutro", e.neutro, n.get("neutro", ""), "bordes y superficies"))

        def ficha(it, xx, yy, cw):
            rol, hx, nom, papel = it
            r = m.contraste(hx, e.base)
            return (L.rect(xx, yy, cw, 300, hx, rx=e.firma["radio"], stroke=e.neutro)
                    + L.t(e, f"{rol} · {nom}", xx, yy + 320, 26, e.ink, "bold", rol="titulos")
                    + L.t(e, hx.upper(), xx, yy + 360, 22, e.brand, "bold")
                    + L.t(e, papel, xx, yy + 394, 20, e.muted)
                    + L.t(e, f"{r:.1f}:1 sobre la base · {m.veredicto(r)}", xx, yy + 424, 18, e.muted))
        self.fichas("Identidad", "Paleta", "Cinco colores, cada uno con un papel.", items, "paleta", ficha)

    def tipografia(self):
        e = self.est
        tp = self.marca.get("tipografia", {})
        vx, vw = span(6, 12)
        ft, fx = e.f_tit, e.f_txt
        vis = [L.t(e, "Aa", vx, L.Y_VIS_TOP, 240, e.brand, "bold", lh=1.0, rol="titulos"),
               L.t(e, f"{ft} · títulos", vx, 650, 28, e.ink, "bold", rol="titulos"),
               L.t(e, f"{fx} · texto", vx, 696, 28, e.ink, rol="texto")]
        muestra = f"{self.est.nombre} cuida de lo que usas cada día. Dos familias, una jerarquía."
        s, _ = L.bloque(e, muestra, vx, 760, 28, vw, 3, lh=1.5, que="muestra")
        vis.append(s)
        lic = " y ".join(f"{tp.get(k, {}).get('familia', '?')}: {tp.get(k, {}).get('licencia', 'licencia por comprobar')}"
                         for k in ("titulos", "texto"))
        cuerpo = "Escala: 120 / 72 / 34 / 28 / 22 / 20 px.\nTítulos en negrita, texto en regular.\nLicencia: " + lic
        self.contenido("Sistema", "Tipografía", "Dos familias y una jerarquía clara.", cuerpo, "".join(vis), "tipografia")

    def voz(self):
        e, k = self.est, self.kit
        rasgos = kit_get(k, "voz.rasgos") or []
        if not rasgos:
            self.pend(None, "voz.rasgos (3, con asi_si y asi_no)")
            rasgos = [{"rasgo": "Rasgo", "asi_si": PEND, "asi_no": PEND}] * 3
        vx, vw = span(6, 12)
        vis, y = [], L.Y_VIS_TOP
        for r in rasgos[:3]:
            vis.append(L.t(e, r.get("rasgo", ""), vx, y, 28, e.brand, "bold", rol="titulos"))
            s, _ = L.bloque(e, "Así sí: " + r.get("asi_si", ""), vx, y + 44, 22, vw, 2, lh=1.4, que="así sí")
            s2, _ = L.bloque(e, "Así no: " + r.get("asi_no", ""), vx, y + 44 + 66, 22, vw, 2, e.muted, lh=1.4, que="así no")
            vis += [s, s2]
            y += 188
        cuerpo = f"Tono: {self.marca['tono']}.\nNo decimos: " + ", ".join(self.marca["palabrasProhibidas"][:4]) + "."
        self.contenido("Sistema", "Voz", "Comportamiento, no adjetivos.", cuerpo, "".join(vis), "voz")

    def elementos(self):
        e = self.est
        els = self.kit.get("elementos") or []
        if not els:
            self.pend(None, "elementos (texturas, iconos o recursos propios)")
            els = [{"nombre": "Elemento", "uso": PEND}] * 3

        def ficha(it, xx, yy, cw):
            s, _ = L.bloque(e, it.get("uso", ""), xx, yy + 352, 22, cw, 2, e.muted, lh=1.4, que="uso del elemento")
            return (L.foto(e, xx, yy, cw, 300, "recurso pendiente")
                    + L.t(e, it.get("nombre", ""), xx, yy + 316, 26, e.ink, "bold", rol="titulos") + s)
        self.fichas("Sistema", "Elementos", "Recursos propios que se repiten con disciplina.", els, "elementos", ficha)

    def fotografia(self):
        e, k = self.est, self.kit
        vx, vw = span(6, 12)
        mitad = (vw - L.GUT) // 2
        vis = [L.foto(e, vx, L.Y_VIS_TOP, mitad, 440, "sí"), L.foto(e, vx + mitad + L.GUT, L.Y_VIS_TOP, mitad, 440, "no")]
        si = self.pend(kit_get(k, "fotografia.si"), "fotografia.si")
        no = self.pend(kit_get(k, "fotografia.no"), "fotografia.no")
        for xx, tx, col in ((vx, "Sí: " + si, e.ink), (vx + mitad + L.GUT, "No: " + no, e.muted)):
            s, _ = L.bloque(e, tx, xx, L.Y_VIS_TOP + 460, 22, mitad, 3, col, lh=1.4, que="pie de foto")
            vis.append(s)
        self.contenido("Sistema", "Fotografía", "Qué sí y qué no.", self.marca["visual"]["estilo"],
                       "".join(vis), "fotografia")

    def usos(self):
        reglas = self.kit.get("usos") or ["Sobre superficies curvas, el logo va plano y centrado.",
                                          "Sobre tela, solo la versión monocroma.",
                                          "Sobre envase, respeta el área de respeto en todos los lados."]
        self.especimen("Usos sobre superficie", reglas, "usos", "superficie · pendiente")

    def aplicacion(self, clave, kicker, titulo, slug):
        e = self.est
        d = self.kit.get(clave) or {}
        vx, vw = span(6, 12)
        vis = L.foto(e, vx, L.Y_VIS_TOP, vw, 548, "aplicación pendiente")
        self.contenido(kicker, d.get("titulo") or titulo, d.get("lead") or self.pend(None, clave),
                       d.get("descripcion", ""), vis, slug)

    def mockup(self):
        self.especimen("Mockup", ["Escena generada: el producto va en blanco y el logo se superpone plano, sin perspectiva.",
                                  "Es una aproximación para presentar, no una maqueta de imprenta."], "mockup",
                       "escena generada · pendiente")

    # ---- orden ----
    def generar(self):
        self.portada()
        self.divisor(1, "La marca")
        self.la_marca()
        self.divisor(2, "Identidad")
        self.logo_principal()
        self.versiones()
        self.paleta()
        self.divisor(3, "Sistema")
        self.tipografia()
        self.voz()
        self.elementos()
        self.fotografia()
        self.usos()
        self.divisor(4, "Aplicaciones")
        self.aplicacion("aplicacion_principal", "Aplicaciones", "Aplicación principal", "aplicacion-principal")
        self.aplicacion("aplicacion_secundaria", "Aplicaciones", "Aplicación secundaria", "aplicacion-secundaria")
        if self.kit.get("mockups"):
            self.mockup()
        assert self.n == self.total, f"numeración incoherente: {self.n} láminas de contenido, esperaba {self.total}"


def index_html(g):
    e = g.est
    fams = {e.f_tit, e.f_txt}
    q = "&".join("family=" + f.replace(" ", "+") + ":wght@400;500;700" for f in sorted(fams))
    cuerpo = []
    for nombre, titulo, s in g.laminas:
        inline = s.replace('href="../', 'href="')        # en el index las rutas son relativas a su carpeta
        cuerpo.append(f'<section id="{nombre[:-4]}"><h2>{esc(titulo)}</h2>{inline}</section>')
    return f"""<!doctype html>
<html lang="{esc(g.marca['idioma'][:2])}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Manual de marca · {esc(g.marca['nombre'])}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{q}&display=swap">
<style>
body{{margin:0;background:#111;color:#eee;font-family:system-ui,sans-serif}}
header{{padding:24px 32px;position:sticky;top:0;background:#111;z-index:2;border-bottom:1px solid #333}}
main{{max-width:1100px;margin:0 auto;padding:24px 16px}}
section{{margin:0 0 40px}} h2{{font-size:14px;font-weight:500;color:#999;margin:0 0 8px}}
svg{{width:100%;height:auto;display:block;box-shadow:0 2px 24px #0008}}
</style></head><body>
<header><strong>{esc(g.marca['nombre'])}</strong> · manual de marca · {len(g.laminas)} láminas</header>
<main>{''.join(cuerpo)}</main></body></html>
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--kit")
    ap.add_argument("--salida")
    a = ap.parse_args(argv)
    try:
        marca = m.cargar(a.marca)
        kit = json.load(open(a.kit, encoding="utf-8")) if a.kit else {}
    except (OSError, json.JSONDecodeError) as ex:
        print(f"No se puede leer la entrada: {ex}", file=sys.stderr)
        return 2
    if not m.informe(a.marca, marca):
        print("marca.json no es válido; corrígelo antes de generar el kit.", file=sys.stderr)
        return 1
    salida = a.salida or os.path.join(os.path.dirname(os.path.abspath(a.marca)), "kit")
    os.makedirs(os.path.join(salida, "laminas"), exist_ok=True)

    base_logo = os.path.dirname(os.path.abspath(a.marca))
    g = Generador(marca, kit, salida, salida_logos_base=base_logo)   # rutas de logo relativas a marca.json
    g.generar()
    # copiar los logos a <salida>/logo/ para que el kit funcione aunque se mueva la carpeta
    for l in marca.get("brandKit", {}).get("logo", []):
        src = os.path.join(base_logo, l["archivo"])
        if os.path.isfile(src):
            os.makedirs(os.path.join(salida, "logo"), exist_ok=True)
            shutil.copy(src, os.path.join(salida, "logo", os.path.basename(l["archivo"])))

    for nombre, _, s in g.laminas:
        with open(os.path.join(salida, "laminas", nombre), "w", encoding="utf-8") as f:
            f.write(s)
    with open(os.path.join(salida, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html(g))
    print(f"ok {len(g.laminas)} láminas en {os.path.join(salida, 'laminas')}")
    print(f"ok {os.path.join(salida, 'index.html')}")

    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        pdf = os.path.join(salida, "manual-de-marca.pdf")
        ins = [os.path.join(salida, "laminas", n) for n, _, _ in g.laminas]
        r = subprocess.run([rsvg, "-f", "pdf", "-o", pdf] + ins, capture_output=True, text=True)
        print("ok " + pdf if r.returncode == 0 else "aviso: no se pudo crear el PDF: " + r.stderr.strip()[:120])
    else:
        print("aviso: sin rsvg-convert no se genera el PDF (abre index.html e imprime a PDF desde el navegador)")

    if g.est.avisos:
        print("\nAvisos del kit:", file=sys.stderr)
        for av in g.est.avisos:
            print("  -", av, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
