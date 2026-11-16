#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Busca fotos de Pexels (gratis), las descarga a fotos/ y rellena fotos/creditos.md.

Hace falta una clave gratuita de la API de Pexels (se pide en pexels.com/api, con una cuenta gratuita).
Se guarda en la variable de entorno PEXELS_API_KEY. Es **opcional**: sin clave se descargan las fotos a mano
(ver references/fotos.md) y se rellena creditos.md a mano.

Uso:
  python3 buscar_fotos.py buscar "equipo de oficina trabajando" --n 8 --orientacion landscape [--carpeta fotos]
      → guarda miniaturas en fotos/_candidatas/ (para mirarlas) y lista id, autor y descripción.
  python3 buscar_fotos.py elegir 1234567 --como equipo-1 [--carpeta fotos]
      → descarga la foto como fotos/equipo-1.jpg y añade su fila a fotos/creditos.md
        (origen banco, autor con enlace, licencia «Pexels License»).
Después: python3 preparar_fotos.py fotos --salida lanzamiento/fotos

Reglas de Pexels que se respetan: la foto se descarga y se acredita al autor con enlace. No se sugiere que una
persona que sale en la foto respalda la marca ni se presenta como el equipo o los clientes reales.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("PEXELS_API_BASE", "https://api.pexels.com/v1")
UA = "brand-kit-builder/1.0 (plugin educativo)"


def clave(a):
    k = getattr(a, "clave", None) or os.environ.get("PEXELS_API_KEY")
    if not k:
        sys.exit("Falta la clave de Pexels. Es gratis: crea una cuenta en pexels.com/api, copia tu clave y ejecuta\n"
                 "  export PEXELS_API_KEY=tu_clave        (en Windows PowerShell: $env:PEXELS_API_KEY=\"tu_clave\")\n"
                 "Sin clave también puedes descargar las fotos a mano de pexels.com y rellenar fotos/creditos.md "
                 "(skills/lanzamiento/references/fotos.md).")
    return k


def api(ruta, k, params=None):
    url = BASE + ruta + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": k, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            sys.exit("Pexels rechazó la clave (401/403): revisa PEXELS_API_KEY.")
        if e.code == 429:
            sys.exit("Pexels: demasiadas consultas por hora (límite del plan gratuito). Espera un rato o descarga a mano.")
        sys.exit(f"Pexels respondió con error {e.code}.")
    except urllib.error.URLError as e:
        sys.exit(f"No se pudo conectar con Pexels ({e.reason}). Si estás sin red, descarga las fotos a mano.")


def bajar(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r, open(destino, "wb") as fh:
        fh.write(r.read())


def limpio(s):
    return " ".join(str(s or "").replace("|", "/").split())


def buscar(a):
    k = clave(a)
    p = {"query": a.consulta, "per_page": max(1, min(a.n, 30)), "locale": "es-ES"}
    if a.orientacion:
        p["orientation"] = a.orientacion
    datos = api("/search", k, p)
    fotos = datos.get("photos", [])
    if not fotos:
        print("Sin resultados. Prueba con otras palabras (en inglés suele dar más).")
        return 1
    cand = os.path.join(a.carpeta, "_candidatas")
    os.makedirs(cand, exist_ok=True)
    for f in fotos:
        try:
            bajar(f["src"]["medium"], os.path.join(cand, f"pexels-{f['id']}.jpg"))
        except Exception as e:  # noqa: BLE001
            print(f"  aviso: no se pudo bajar la miniatura de {f['id']}: {e}")
        print(f"{f['id']:>10}  {limpio(f.get('photographer')):<26} {limpio(f.get('alt'))[:70]}")
    json.dump(fotos, open(os.path.join(cand, "candidatas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nMiniaturas en {cand}/pexels-<id>.jpg. Mira las que encajan y elige con:\n"
          f"  python3 {os.path.basename(sys.argv[0])} elegir <id> --como equipo-1 --carpeta {a.carpeta}")
    print("Recuerda: una persona de banco no se presenta como tu equipo ni como tus clientes.")
    return 0


def fila(archivo, autor, licencia):
    return f"| {archivo} | banco | {autor} | {licencia} | n/a |\n"


def elegir(a):
    k = clave(a)
    f = api(f"/photos/{int(a.id)}", k)
    nombre = a.como if os.path.splitext(a.como)[1] else a.como + ".jpg"
    destino = os.path.join(a.carpeta, nombre)
    os.makedirs(a.carpeta, exist_ok=True)
    if os.path.exists(destino) and not a.reemplazar:
        sys.exit(f"{destino} ya existe; usa --reemplazar o elige otro nombre con --como.")
    try:
        bajar(f["src"].get("large2x") or f["src"]["original"], destino)
    except Exception as ex:  # noqa: BLE001
        sys.exit(f"No se pudo descargar la foto ({ex}). Descárgala a mano de {f.get('url', 'pexels.com')} y rellena creditos.md.")
    autor = f"{limpio(f.get('photographer'))} ({f.get('photographer_url', '')}), {f.get('url', '')}"
    ruta = os.path.join(a.carpeta, "creditos.md")
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write("# Créditos de las fotos\n\nUna fila por foto. origen = propia, banco o ia.\n\n"
                     "| archivo | origen | autor o fuente | licencia | permiso de las personas |\n|---|---|---|---|---|\n")
    lineas = open(ruta, encoding="utf-8").read().splitlines(keepends=True)
    lineas = [x for x in lineas if not x.lstrip("| ").startswith(nombre + " ")]   # reemplaza la fila del mismo archivo
    if lineas and not lineas[-1].endswith("\n"):
        lineas[-1] += "\n"
    lineas.append(fila(nombre, autor, "Pexels License"))
    open(ruta, "w", encoding="utf-8").write("".join(lineas))
    print(f"ok {destino}\nok fila añadida a {ruta}: foto de {limpio(f.get('photographer'))} en Pexels")
    print("Ahora: python3 skills/lanzamiento/tools/preparar_fotos.py", a.carpeta, "--salida lanzamiento/fotos")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("buscar")
    b.add_argument("consulta")
    b.add_argument("--n", type=int, default=8)
    b.add_argument("--orientacion", choices=["landscape", "portrait", "square"])
    e = sub.add_parser("elegir")
    e.add_argument("id")
    e.add_argument("--como", required=True, help="nombre del archivo, p. ej. equipo-1 o retrato-1")
    e.add_argument("--reemplazar", action="store_true")
    for s in (b, e):
        s.add_argument("--carpeta", default="fotos")
        s.add_argument("--clave", help="mejor usa la variable PEXELS_API_KEY")
    a = ap.parse_args()
    sys.exit(buscar(a) if a.cmd == "buscar" else elegir(a))


if __name__ == "__main__":
    main()
