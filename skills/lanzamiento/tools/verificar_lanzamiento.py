#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Autotest de la skill lanzamiento: librería de color, bento, andamio de posts y exportador de logos.
Lo que necesita navegador (revisión con el crítico) se marca SALTADO si falta Playwright.

Uso:  python3 verificar_lanzamiento.py
"""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import lib_lanzamiento as L  # noqa: E402

RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
PULSO = os.path.join(RAIZ, "evals", "fixtures", "pulso", "marca.json")
CRITICO = os.path.join(RAIZ, "skills", "gusto", "tools", "critico_render.py")
fallos, saltados = [], []


def ok(c, msg):
    print(("  ok     " if c else "  FALLO  ") + msg)
    if not c:
        fallos.append(msg)


def py(*a):
    return subprocess.run([sys.executable, *a], capture_output=True, text=True)


# 1. color
ok(L.legible("#FFFFFF") != "#FFFFFF", "sobre fondo blanco el texto no es blanco")
ok(L.legible("#0A1F6B") == "#FFFFFF", "sobre azul profundo el texto es blanco")
ok(L.luminancia(L.oscurecer("#2B63F0", 0.5)) < L.luminancia("#2B63F0"), "oscurecer baja la luminancia")
ok(L.contraste("#000000", "#FFFFFF") > 20, "contraste negro/blanco ≈ 21")

# 2. marca mínima y escape
m_min = {"nombre": "Mínima", "visual": {"colores": [{"nombre": "x", "hex": "#336699", "rol": "primario"}]}}
c = L.colores(m_min)
ok(c["primario"] == "#336699" and c["profundo"] and c["neutro"], "marca mínima: colores derivados sin fallar")
ok(L.fuentes(m_min)["titulos"] == "Inter", "marca sin tipografía: fuente por defecto")
ok(L.enlace_google_fonts(m_min) == "", "sin «Google Fonts» no hay enlace a Google")
g = L.enlace_google_fonts({"tipografia": {"titulos": {"familia": "Space Grotesk", "pesos": [500, 700], "fuente": "Google Fonts"}, "texto": {"familia": "IBM Plex Sans", "pesos": [400], "fuente": "Google Fonts"}}})
ok("Space+Grotesk" in g and "IBM+Plex+Sans" in g and "500;700" in g, "enlace a Google Fonts con familias y pesos")

with tempfile.TemporaryDirectory() as d:
    # 3. bento con la marca de ejemplo
    salida = os.path.join(d, "bento.html")
    r = py(os.path.join(AQUI, "bento.py"), PULSO, "--salida", salida, "--lema", "<b>x</b> & más", "--prueba", "Servicio|1 revisión al mes")
    h = open(salida, encoding="utf-8").read() if os.path.exists(salida) else ""
    ok(r.returncode == 0 and "PULSO" in h, "bento.py genera el HTML con el nombre")
    ok("#2F4BD8" in h, "el bento usa el color primario de marca.json")
    ok("&lt;b&gt;x&lt;/b&gt;" in h and "<b>x</b>" not in h, "el texto del lema se escapa")
    ok("Foto real" in h, "sin fotos: marcador visible, no inventado")
    ok("Territorio" in h and "Tecnológico" in h, "sin gusto.json: muestra el territorio con su tilde")
    # con gusto.json
    gj = os.path.join(d, "gusto.json")
    json.dump({"tonos": {"serio": 50, "divertido": 20, "tecnologico": 30}}, open(gj, "w"))
    py(os.path.join(AQUI, "bento.py"), PULSO, "--salida", salida, "--gusto", gj)
    h2 = open(salida, encoding="utf-8").read()
    ok("Proporción" in h2 and ">50<" in h2, "con gusto.json: muestra la proporción de tonos")

    # 4. logos reales: se incrustan como data URI
    svg = os.path.join(d, "invertida.svg")
    open(svg, "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60"><rect width="200" height="60" fill="#fff"/></svg>')
    mm = json.load(open(PULSO, encoding="utf-8"))
    mm["brandKit"]["logo"] = [{"version": "invertida", "archivo": "invertida.svg"}]
    mp = os.path.join(d, "marca.json")
    json.dump(mm, open(mp, "w"))
    py(os.path.join(AQUI, "bento.py"), mp, "--salida", salida)
    ok("data:image/svg+xml;base64," in open(salida, encoding="utf-8").read(), "el logo se incrusta en el bento (no depende de rutas)")

    # 5. marca mínima no rompe
    mmn = os.path.join(d, "min.json")
    json.dump(m_min, open(mmn, "w"))
    r = py(os.path.join(AQUI, "bento.py"), mmn, "--salida", os.path.join(d, "b2.html"))
    ok(r.returncode == 0, "bento.py con una marca mínima no falla")

    # 6. andamio de posts
    for tipo in ("que-es", "atributo"):
        p = os.path.join(d, f"{tipo}.html")
        r = py(os.path.join(AQUI, "post_base.py"), PULSO, "--tipo", tipo, "--salida", p, "--titular", "Prueba")
        t = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        ok(r.returncode == 0 and 'class="p campo"' in t and "RECURSO VISUAL" in t and "1080px" in t, f"post_base.py ({tipo}) genera el andamio")

    # 7. exportar logos
    r = py(os.path.join(AQUI, "exportar_logos.py"), PULSO, "--salida", os.path.join(d, "logo"))
    ok(r.returncode == 2 and "ningún logo" in r.stdout, "exportar_logos: sin logos en disco, lo dice y sale con 2")
    r = py(os.path.join(AQUI, "exportar_logos.py"), mp, "--salida", os.path.join(d, "logo"), "--ancho", "400")
    if r.returncode == 2 and "No hay rsvg-convert" in r.stdout:
        saltados.append("exportación PNG (falta Chromium/rsvg)")
        print("  SALTADO exportación PNG: falta Chromium o rsvg-convert")
    else:
        png = os.path.join(d, "logo", "invertida.png")
        ok(r.returncode == 0 and os.path.exists(png), "exportar_logos crea el PNG")

    # 7b. fotos
    try:
        from PIL import Image
        fd = os.path.join(d, "fotos"); os.makedirs(fd)
        Image.new("RGB", (1600, 1200), (90, 120, 200)).save(os.path.join(fd, "equipo-1.jpg"))
        Image.new("RGB", (600, 800), (200, 120, 90)).save(os.path.join(fd, "retrato-1.jpg"))
        sal = os.path.join(d, "salida")
        r = py(os.path.join(AQUI, "preparar_fotos.py"), fd, "--salida", sal)
        ok(r.returncode == 1 and "falta su fila" in r.stdout, "preparar_fotos: sin créditos da error y no sigue")
        py(os.path.join(AQUI, "preparar_fotos.py"), fd, "--crear-creditos")
        ct = open(os.path.join(fd, "creditos.md"), encoding="utf-8").read()
        ct = ct.replace("| equipo-1.jpg |  |  |  |  |", "| equipo-1.jpg | ia | Canva | n/a |  |").replace("| retrato-1.jpg |  |  |  |  |", "| retrato-1.jpg | banco |  |  |  |")
        open(os.path.join(fd, "creditos.md"), "w", encoding="utf-8").write(ct)
        r = py(os.path.join(AQUI, "preparar_fotos.py"), fd, "--salida", sal)
        ok(r.returncode == 1 and "sin autor o sin licencia" in r.stdout, "preparar_fotos: origen banco sin licencia da error")
        ct = ct.replace("| retrato-1.jpg | banco |  |  |  |", "| retrato-1.jpg | banco | Ana Pérez, unsplash.com/x | Unsplash License | n/a |")
        open(os.path.join(fd, "creditos.md"), "w", encoding="utf-8").write(ct)
        r = py(os.path.join(AQUI, "preparar_fotos.py"), fd, "--salida", sal)
        man = json.load(open(os.path.join(sal, "manifiesto.json"), encoding="utf-8"))
        ok(r.returncode == 0 and len(man) == 2, "preparar_fotos: con créditos completos termina bien")
        ok(any("baja resolución" in v for x in man for v in x["avisos"]), "avisa de la foto de baja resolución (600×800)")
        ok(os.path.exists(os.path.join(sal, "equipo-1-3x4.jpg")) and Image.open(os.path.join(sal, "equipo-1-4x3.jpg")).size[0] * 3 == Image.open(os.path.join(sal, "equipo-1-4x3.jpg")).size[1] * 4, "recortes 3:4 y 4:3 con la proporción exacta")
        ok(man[0]["pie"] == "Imagen generada con IA" and man[1]["pie"] is None, "las fotos de origen ia quedan marcadas en el manifiesto")
        bt = os.path.join(d, "bento-f.html")
        py(os.path.join(AQUI, "bento.py"), PULSO, "--salida", bt, "--fotos", sal)
        h = open(bt, encoding="utf-8").read()
        ok("data:image/jpeg;base64," in h and "Foto real" not in h.split('class="t F"')[1].split("</div>")[0], "el bento usa las fotos de la carpeta")
        ok("Imagen generada con IA" not in h, "por defecto NO se escribe «Imagen generada con IA» sobre el bento")
        py(os.path.join(AQUI, "bento.py"), PULSO, "--salida", bt, "--fotos", sal, "--declarar-ia")
        ok("Imagen generada con IA" in open(bt, encoding="utf-8").read(), "con --declarar-ia sí se escribe")
        pt = os.path.join(d, "post-f.html")
        py(os.path.join(AQUI, "post_base.py"), PULSO, "--tipo", "que-es", "--salida", pt, "--fotos", sal)
        t2 = open(pt, encoding="utf-8").read()
        ok("FOTOS DISPONIBLES" in t2 and "Imagen generada con IA" not in t2, "post_base lista las fotos y por defecto no declara IA")
        ok('class="pie-ejemplo"' not in t2, "post_base no pone pie por defecto")
        py(os.path.join(AQUI, "post_base.py"), PULSO, "--tipo", "que-es", "--salida", pt, "--pie", "Mi pie")
        ok("Mi pie" in open(pt, encoding="utf-8").read(), "con --pie sí lo pone")
    except ImportError:
        saltados.append("fotos (falta Pillow)")
        print("  SALTADO fotos: falta Pillow")

    # 7c. generadores de posts
    try:
        r = py(os.path.join(AQUI, "post_telefono.py"), PULSO, "--salida", os.path.join(d, "t.html"), "--titular", "Mantenimiento <b>sin cita</b>",
               "--filas", "Revisión|Cada mes;Ajuste|Frenos y cambios;Recogida|En tu portal", "--estado", "Incluido", "--boton", "Pedir", "--tarjeta-izq", "Plan|1 al mes", "--cifra", "3|servicios")
        t = open(os.path.join(d, "t.html"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "t.html")) else ""
        ok(r.returncode == 0 and 'class="telefono"' in t and "<b>sin cita</b>" in t, "post_telefono genera el post con el titular en negrita")
        ok("Foto real" not in t and "Imagen generada" not in t, "post_telefono: sin fotos no deja marcadores ni etiquetas")
        ok(t.count('class="fila"') == 3, "post_telefono: una fila por cada dato")
        ok(L.contraste(L.suave("#14181F", "#C8CDD6"), "#FFFFFF") >= 4.6, "el gris suave derivado contrasta ≥ 4,6:1")
        ok("&lt;script&gt;" in (py(os.path.join(AQUI, "post_telefono.py"), PULSO, "--salida", os.path.join(d, "t2.html"), "--titular", "x", "--filas", "<script>|y"), open(os.path.join(d, "t2.html"), encoding="utf-8").read())[1], "post_telefono escapa el texto de las filas")
        rc = py(CRITICO, os.path.join(d, "t.html"), "--marca", PULSO)
        if rc.returncode != 2:
            ok(rc.returncode == 0, "post_telefono pasa el crítico sin errores")
    except Exception as e:  # noqa: BLE001
        ok(False, f"post_telefono falló: {e}")
    r = subprocess.run(["node", "-e", "require.resolve('d3-geo')"], capture_output=True, text=True)
    if r.returncode != 0 and not os.path.isdir(os.path.join(os.getcwd(), "node_modules", "d3-geo")):
        saltados.append("post_mapa (faltan los paquetes npm de mapa en esta carpeta)")
        print("  SALTADO post_mapa: faltan los paquetes npm (npm i world-atlas topojson-client d3-geo)")
    else:
        pm = os.path.join(d, "m.html")
        r = py(os.path.join(AQUI, "post_mapa.py"), PULSO, "--salida", pm, "--titular", "Ciclistas <b>cerca de ti</b>", "--centro", "Madrid|-3.70,40.42",
               "--bbox", "-10.5,35.3,7,46.8", "--radio", "200", "--puntos", "Toledo|-4.02,39.86;Segovia|-4.12,40.95;Barcelona|2.17,41.39", "--destacada", "Ana|Mecánica|Toledo")
        t = open(pm, encoding="utf-8").read() if os.path.exists(pm) else ""
        ok(r.returncode == 0 and "A 68 km de ti" in t, "post_mapa calcula la distancia real (Madrid–Toledo 68 km)")
        ok("Barcelona" in r.stdout and "fuera del radio" in r.stdout, "post_mapa avisa de la ciudad fuera del radio")
        r = py(os.path.join(AQUI, "post_mapa.py"), PULSO, "--salida", pm, "--titular", "x", "--centro", "Madrid|-3.70,40.42", "--bbox", "-10.5,35.3,7,46.8", "--puntos", "Toledo|-4.02,39.86", "--destacada", "Ana|M|Segovia")
        ok(r.returncode == 1, "post_mapa rechaza una destacada que no está entre los puntos")

    # 7b. generadores nuevos: comparativa, pantalla, tema claro, bento sin fotos
    pc = os.path.join(d, "c.html")
    r = py(os.path.join(AQUI, "post_comparativa.py"), PULSO, "--salida", pc, "--titular", "x", "--ellos", "Otro|9 €|a;b", "--nosotros", "Tú|3 €|c;d")
    ok(r.returncode != 0 and not os.path.exists(pc), "post_comparativa rechaza un competidor sin --fuente")
    r = py(os.path.join(AQUI, "post_comparativa.py"), PULSO, "--salida", pc, "--titular", "Menos <b>coste</b>", "--ellos", "Otro|9 €|a;b", "--nosotros", "Tú|3 €|c;d", "--ejemplo", "--tema", "claro")
    t = open(pc, encoding="utf-8").read() if os.path.exists(pc) else ""
    ok(r.returncode == 0 and "Dato de ejemplo" in t, "post_comparativa --ejemplo marca el dato como de ejemplo")
    pp = os.path.join(d, "p.html")
    r = py(os.path.join(AQUI, "post_pantalla.py"), PULSO, "--salida", pp, "--titular", "Todo <b>a mano</b>", "--ventana", "pulso.app|Panel", "--menu", "Inicio;Rutas", "--cifra", "10 €|al mes", "--codigo", "const a = 1;run(a);", "--tema", "claro")
    ok(r.returncode == 0 and "const a = 1" in open(pp, encoding="utf-8").read(), "post_pantalla genera la ventana con código")
    bd = os.path.join(d, "bd.html")
    r = py(os.path.join(AQUI, "bento.py"), PULSO, "--salida", bd, "--datos", "Precio|10 €/mes;Grupos|5", "--puntos", "Uno;Dos")
    t = open(bd, encoding="utf-8").read() if os.path.exists(bd) else ""
    ok("Foto real" not in t and "10 €/mes" in t and "Dos" in t, "bento sin fotos: --datos y --puntos sustituyen los marcadores")

    be = os.path.join(d, "be.html")
    r = py(os.path.join(AQUI, "bento.py"), PULSO, "--salida", be, "--variante", "educativa")
    ok(r.returncode != 0, "bento educativo exige --ruta con el recorrido")
    r = py(os.path.join(AQUI, "bento.py"), PULSO, "--salida", be, "--variante", "educativa", "--ruta", "Uno;Dos;Tres")
    ok(r.returncode == 0 and "Recorrido" in open(be, encoding="utf-8").read(), "bento educativo: el recorrido es una tarjeta")
    r = py(os.path.join(AQUI, "bento.py"), PULSO, "--salida", os.path.join(d, "bp.html"), "--variante", "producto")
    ok(r.returncode != 0, "bento de producto exige foto")
    ra = py(os.path.join(AQUI, "variedad.py"), be, bd)
    ok("PARECIDA" in ra.stdout or "ok" in ra.stdout, "variedad.py compara estructuras")

    # 7c. buscar_fotos.py contra un servidor Pexels falso (sin red ni clave reales)
    import http.server
    import io
    import threading

    class _H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *x):
            pass

        def do_GET(self):
            from PIL import Image
            def jpg(w, h):
                b = io.BytesIO()
                Image.new("RGB", (w, h), "#789").save(b, "JPEG")
                return b.getvalue()
            P = "http://127.0.0.1:%d" % self.server.server_port
            foto = {"id": 42, "photographer": "Ana", "photographer_url": "https://www.pexels.com/@ana", "url": "https://www.pexels.com/photo/42/", "alt": "Equipo",
                    "src": {"medium": P + "/m.jpg", "large2x": P + "/l.jpg", "original": P + "/l.jpg"}}
            if self.path.startswith("/v1") and self.headers.get("Authorization") != "K":
                self.send_response(401); self.end_headers(); return
            body = (json.dumps({"photos": [foto]}) if self.path.startswith("/v1/search") else json.dumps(foto)).encode() if self.path.startswith("/v1") else jpg(350, 233) if self.path == "/m.jpg" else jpg(1880, 1253)
            self.send_response(200); self.end_headers(); self.wfile.write(body)
    try:
        import PIL  # noqa: F401
        srv = http.server.HTTPServer(("127.0.0.1", 0), _H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        env = dict(os.environ, PEXELS_API_BASE="http://127.0.0.1:%d/v1" % srv.server_port, PEXELS_API_KEY="K")
        carp = os.path.join(d, "fotos-px")
        BF = os.path.join(AQUI, "buscar_fotos.py")
        sin = subprocess.run([sys.executable, BF, "buscar", "x", "--carpeta", carp], capture_output=True, text=True, env={**env, "PEXELS_API_KEY": ""})
        ok(sin.returncode != 0 and "gratis" in (sin.stdout + sin.stderr).lower(), "buscar_fotos sin clave explica cómo conseguirla (gratis)")
        r1 = subprocess.run([sys.executable, BF, "buscar", "equipo", "--carpeta", carp], capture_output=True, text=True, env=env)
        ok(r1.returncode == 0 and os.path.exists(os.path.join(carp, "_candidatas", "pexels-42.jpg")), "buscar_fotos deja miniaturas candidatas")
        r2 = subprocess.run([sys.executable, BF, "elegir", "42", "--como", "equipo-1", "--carpeta", carp], capture_output=True, text=True, env=env)
        cred = open(os.path.join(carp, "creditos.md"), encoding="utf-8").read() if os.path.exists(os.path.join(carp, "creditos.md")) else ""
        ok(r2.returncode == 0 and "| equipo-1.jpg | banco |" in cred and "Pexels License" in cred, "buscar_fotos elegir descarga y rellena creditos.md")
        r3 = py(os.path.join(AQUI, "preparar_fotos.py"), carp, "--salida", os.path.join(d, "fotos-out"))
        ok(r3.returncode == 0, "preparar_fotos acepta la foto descargada con su fila")
        srv.shutdown()
    except ImportError:
        saltados.append("buscar_fotos (falta Pillow)")

    pf = os.path.join(d, "pf.md")
    r = py(os.path.join(AQUI, "prompts_fotos.py"), PULSO, "--salida", pf, "--equipo", "mecánicos revisando una bici")
    tx = open(pf, encoding="utf-8").read() if os.path.exists(pf) else ""
    ok(r.returncode == 0 and tx.count("```") == 8 and "sin ningún texto" in tx and "#2F4BD8" in tx and "Mecánicos revisando una bici." in tx, "prompts_fotos: 4 prompts con paleta, sin texto y con el sujeto pedido")

    rc = py(os.path.join(AQUI, "prompts_fotos.py"), PULSO, "--salida", pf, "--proveedor", "canva")
    ok(rc.returncode == 0 and "LANDSCAPE_4_3" in open(pf, encoding="utf-8").read() and "PORTRAIT_3_4" in open(pf, encoding="utf-8").read(), "prompts_fotos --proveedor canva indica la proporción de Canva")
    fr = os.path.join(d, "fr")
    os.makedirs(fr)
    try:
        from PIL import Image
        Image.new("RGB", (1500, 1100), "#789").save(os.path.join(fr, "equipo-1.png"))
        r = py(os.path.join(AQUI, "registrar_foto.py"), os.path.join(fr, "equipo-1.png"), "--origen", "ia", "--fuente", "Canva (generada)")
        ok(r.returncode == 0 and "| equipo-1.png | ia | Canva (generada) |" in open(os.path.join(fr, "creditos.md"), encoding="utf-8").read(), "registrar_foto anota una foto de IA")
        r = py(os.path.join(AQUI, "registrar_foto.py"), os.path.join(fr, "equipo-1.png"), "--origen", "propia")
        ok(r.returncode != 0, "registrar_foto exige permiso para una foto propia con personas")
    except ImportError:
        saltados.append("registrar_foto (falta Pillow)")

    # 8. el crítico acepta el bento
    r = py(CRITICO, salida, "--ancho", "1920", "--alto", "1080")
    if r.returncode == 2:
        saltados.append("revisión con el crítico (falta Playwright)")
        print("  SALTADO crítico: falta Playwright")
    else:
        ok(r.returncode == 0, "el bento pasa el crítico sin errores (1920×1080)")

print()
if saltados:
    print("SALTADO:", "; ".join(saltados))
print("TODO OK" if not fallos else f"{len(fallos)} FALLO(S)")
sys.exit(1 if fallos else 0)
