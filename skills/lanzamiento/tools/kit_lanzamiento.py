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
  "post1": {"recurso": "compuesto|expresivo_gigante|expresivo_precio|cifra|pasos|manifiesto|foto|pantalla|telefono|comparativa|mapa|html", "args": {"titular": "…", "ventana": "…", "tema": "claro"}},
  "post2": {"recurso": "…", "args": {…}},
  "notas": ["lo que es de ejemplo o queda a mano, una frase cada una"],
  (en post1 y post2, opcional pero esperado: "intencion": {"mensaje": "una sola idea", "gancho": "lo que hace parar el scroll", "prueba": "el hecho que lo sostiene", "llamada": "qué se espera que haga quien lo ve"})
}
En "args" cada clave es una opción del generador (guiones bajos = guiones: tarjeta_izq → --tarjeta-izq); true = opción sin valor.
Los argumentos de cada recurso están en la cabecera de su script (post_compuesto.py para «compuesto»: composición a medida con args.spec; post_tipografico.py para cifra, pasos y manifiesto; post_expresivo.py para expresivo_gigante y expresivo_precio; post_foto.py, post_pantalla.py, post_telefono.py, post_comparativa.py, post_mapa.py).
Si la marca es visual (fotografía, gastronomía, moda, viajes, interiorismo…) y no hay fotos, añade `"sin_fotos": "motivo"` al brief solo si se decide a propósito.
Sale con 1 si algún generador falla o la puerta de entrega se cierra; imprime qué corregir en el brief y se repite.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CRITICO = os.path.join(RAIZ, "skills", "gusto", "tools", "critico_render.py")
PUERTA = os.path.join(RAIZ, "skills", "entrega", "tools", "verificar_entrega.py")
GEN = {"compuesto": "post_compuesto.py", "expresivo_gigante": "post_expresivo.py", "expresivo_precio": "post_expresivo.py", "cifra": "post_tipografico.py", "pasos": "post_tipografico.py", "manifiesto": "post_tipografico.py", "foto": "post_foto.py", "telefono": "post_telefono.py", "pantalla": "post_pantalla.py", "comparativa": "post_comparativa.py", "mapa": "post_mapa.py"}
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
    return subprocess.run([sys.executable] + cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


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

    # arquetipos: los dos posts no pueden ser de la misma familia, y la interfaz (móvil, ventana) solo para productos digitales
    fam = {"telefono": "ui", "pantalla": "ui", "comparativa": "datos", "mapa": "mapa", "foto": "foto", "compuesto": "compuesto", "expresivo_gigante": "expresivo:gigante", "expresivo_precio": "expresivo:precio", "cifra": "tipografico:cifra", "pasos": "tipografico:pasos", "manifiesto": "tipografico:manifiesto"}
    r1, r2 = b.get("post1", {}).get("recurso", ""), b.get("post2", {}).get("recurso", "")
    # con gusto entrenado que tiene reglas de composición para posts, los dos posts se diseñan a medida (post_compuesto.py o html propio)
    if gusto and os.path.exists(gusto) and not b.get("plantillas_ok"):
        try:
            sys.path.insert(0, os.path.join(AQUI, "..", "..", "gusto", "tools"))
            import gusto_lib as GL
            comp = [x for x in GL.reglas_numeradas(GL.cargar(gusto)) if x["dimension"] == "composicion" and "post" in (x["aplica_en"] or []) and not x["prohibe"]]
        except Exception:  # noqa: BLE001
            comp = []
        plant = [n for n, rr in (("post1", r1), ("post2", r2)) if rr not in ("compuesto", "html")]
        if comp and plant:
            print(f"FALLO tu gusto tiene reglas de composición para posts ({', '.join(x['id'] for x in comp[:5])}…): {' y '.join(plant)} debe ser «compuesto» (composición a medida, ver skills/lanzamiento/references/composicion-a-medida.md). Si de verdad no procede, añade \"plantillas_ok\": \"motivo\" al brief.")
            return 1
    if r1 in fam and r1 == r2 and r1 != "compuesto" or (r1 in fam and r2 in fam and fam[r1] == fam[r2] and fam[r1] != "compuesto"):
        print(f"FALLO los dos posts son del mismo arquetipo ({fam[r1]}): {r1} y {r2}. Cambia uno (python3 {os.path.join(AQUI, 'proponer_posts.py')} {marca} propone combinaciones distintas)")
        return 1
    if "ui" in (fam.get(r1), fam.get(r2)) and not b.get("ui_ok"):
        try:
            mj = json.load(open(marca, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            mj = {}
        txt = " ".join(str(mj.get(k, "")) for k in ("categoria", "publico")).lower()
        if not re.search(r"software|\bapp\b|aplicaci|plataforma|saas|\bweb\b|digital|programaci|c[oó]digo|desarrollo|tecnolog|ciberseg|fintech|datos", txt):
            print("FALLO la interfaz de móvil o de escritorio solo encaja con productos digitales y esta marca no lo es. Elige otro recurso (cifra, pasos, manifiesto, foto…) o, si de verdad el producto tiene interfaz, añade \"ui_ok\": \"motivo\" al brief.")
            return 1

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
        if GEN[rec] == "post_tipografico.py":
            cmd += ["--modo", rec]
        elif GEN[rec] == "post_compuesto.py":
            spec = ruta(base, a_spec) if (a_spec := dict(p.get("args", {})).pop("spec", None)) else ""
            if not spec or not os.path.exists(spec):
                print(f"{nombre}: FALLO el recurso «compuesto» necesita args.spec con la ruta de la composición (JSON; ver post_compuesto.py --ejemplo)")
                mal += 1
                continue
            copia = os.path.join(carpeta, f"composicion-{nombre.split('-')[1]}.json")
            if os.path.abspath(spec) != os.path.abspath(copia):
                open(copia, "w", encoding="utf-8").write(open(spec, encoding="utf-8").read())
            cmd += ["--spec", copia]
        elif GEN[rec] == "post_expresivo.py":
            cmd += ["--modo", rec.split("_", 1)[1]]
        a = dict(p.get("args", {}))
        a.pop("spec", None)
        if fotos and os.path.isdir(fotos) and rec in ("telefono", "mapa", "foto", "compuesto") and "fotos" not in a and "foto" not in a:
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

    # LEEME: se reescribe en cada ejecución desde el brief y los créditos de las fotos (nunca se queda el de una versión anterior)
    leeme = os.path.join(carpeta, "LEEME.md")
    notas = list(b.get("notas", []) or [])
    if fotos and os.path.exists(os.path.join(fotos, "manifiesto.json")):
        try:
            for reg in json.load(open(os.path.join(fotos, "manifiesto.json"), encoding="utf-8")):
                if str(reg.get("origen")) == "ia":
                    notas.append(f"La foto {reg['archivo']} es una imagen generada con IA: no es una persona ni un equipo reales.")
        except Exception:  # noqa: BLE001
            pass
    if b.get("sin_fotos"):
        notas.append(f"Sin fotos por decisión explícita: {b['sin_fotos']}")
    usa = ", ".join(f"{n} ({'foto' if (b.get(k) or {}).get('recurso') == 'foto' else (b.get(k) or {}).get('recurso', '')})".replace(" ()", "") for n, k in (("post-1-que-es", "post1"), ("post-2-atributo", "post2")))
    with open(leeme, "w", encoding="utf-8") as fh:
        fh.write("# Kit de lanzamiento\n\nPiezas (HTML editable y PNG): logo/, bento, " + usa + ".\n\n## Qué es de ejemplo o queda a mano\n\n")
        for x in notas or ["(rellena: qué es real, qué es de ejemplo y qué queda por hacer a mano)"]:
            fh.write(f"- {x}\n")
        for n, k in (("post-1-que-es", "post1"), ("post-2-atributo", "post2")):
            it = (b.get(k) or {}).get("intencion") or {}
            if it:
                fh.write(f"\n## Intención de {n}\n\n")
                for campo in ("mensaje", "gancho", "prueba", "llamada"):
                    if it.get(campo):
                        fh.write(f"- **{campo.capitalize()}:** {it[campo]}\n")

    # contraste con las referencias (si el gusto tiene decisiones)
    if gusto and os.path.exists(gusto):
        cr = os.path.join(RAIZ, "skills", "gusto", "tools", "contacto_referencias.py")
        r = run([cr, "--gusto", gusto, "--referencias", os.path.join(os.path.dirname(gusto), "referencias"), "--piezas", carpeta, "--salida", carpeta])
        if r.returncode == 0 and "contacto-gusto.png" in r.stdout:
            print("\nREFERENCIAS: mira " + os.path.join(carpeta, "contacto-gusto.png") + " (referencias | piezas) y rellena " + os.path.join(carpeta, "revision-gusto.md") + " regla por regla; corrige lo que no cumpla y vuelve a ejecutar.")

    # puerta
    cmd = [PUERTA, carpeta, "--marca", marca] + (["--gusto", gusto] if gusto and os.path.exists(gusto) else []) + (["--kits", ruta(base, b["kits"])] if b.get("kits") else [])
    r = run(cmd)
    print("\n" + r.stdout.strip())
    return 1 if (mal or r.returncode) else 0


if __name__ == "__main__":
    sys.exit(main())
