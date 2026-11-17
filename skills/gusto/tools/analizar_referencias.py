#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Mide lo medible de una carpeta de imágenes de referencia y lo vuelca en gusto.json.

Uso:  python3 analizar_referencias.py CARPETA [--gusto gusto.json] [--tipo si|no|otra]

Mide: tamaño, colores dominantes, claro/oscuro, saturación, temperatura, aire (proporción de zonas lisas),
densidad de detalle y cuántos tonos distintos hay (si domina uno solo). NO mide ni inventa: el tono
(serio / divertido / tecnologico), la voz del texto y el tipo de imagen quedan en «interpretacion»
para que los complete el modelo viéndolas y los confirme la persona.
Necesita Pillow (pip install pillow). Sin Pillow lo dice y sale sin tocar nada.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import argparse
import colorsys
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gusto_lib as G  # noqa: E402

try:
    from PIL import Image, ImageFilter, ImageStat
except ImportError:  # pragma: no cover
    Image = None

EXT = (".png", ".jpg", ".jpeg", ".webp")


def hexa(rgb):
    return "#%02X%02X%02X" % tuple(rgb)


def medir(ruta):
    im = Image.open(ruta).convert("RGB")
    w0, h0 = im.size
    im.thumbnail((400, 400))
    w, h = im.size
    # colores dominantes (cuantización a 6)
    q = im.quantize(colors=6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:18]
    cuenta = sorted(q.getcolors(), reverse=True)
    total = float(w * h)
    dominantes = []
    for n, idx in cuenta:
        rgb = pal[idx * 3: idx * 3 + 3]
        dominantes.append({"hex": hexa(rgb), "pct": round(n / total * 100, 1)})
    # luminosidad y saturación medias
    hsv = im.convert("HSV")
    s_media = ImageStat.Stat(hsv).mean[1] / 255
    l_media = ImageStat.Stat(im.convert("L")).mean[0] / 255
    # tonos: ángulos de los píxeles saturados
    px = list(hsv.get_flattened_data() if hasattr(hsv, "get_flattened_data") else hsv.getdata())
    sat = [(hh, ss, vv) for hh, ss, vv in px if ss > 60 and vv > 60]
    huecos = [0] * 12
    for hh, _, _ in sat:
        huecos[int(hh / 256 * 12) % 12] += 1
    n_sat = sum(huecos)
    familias = sum(1 for c in huecos if n_sat and c / n_sat > 0.12)
    concentracion = round(max(huecos) / n_sat * 100) if n_sat else 0
    # temperatura
    cal = sum(1 for hh, _, _ in sat if hh < 256 * 70 / 360 or hh > 256 * 330 / 360)
    temp = "sin color dominante" if n_sat < total * 0.03 else ("cálida" if cal / n_sat > 0.55 else "fría")
    # aire: bloques 16x16 casi lisos
    g = im.convert("L")
    lisos = bloques = 0
    for y in range(0, h - 15, 16):
        for x in range(0, w - 15, 16):
            bloques += 1
            if ImageStat.Stat(g.crop((x, y, x + 16, y + 16))).stddev[0] < 6:
                lisos += 1
    aire = round(lisos / bloques * 100) if bloques else 0
    bordes = ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).mean[0]
    detalle = "alto" if bordes > 18 else ("medio" if bordes > 8 else "bajo")
    return {"ancho": w0, "alto": h0, "formato": "vertical" if h0 > w0 * 1.1 else ("horizontal" if w0 > h0 * 1.1 else "cuadrado"),
            "dominantes": dominantes, "luminosidad": "oscura" if l_media < 0.4 else ("clara" if l_media > 0.65 else "media"),
            "saturacion": "alta" if s_media > 0.5 else ("media" if s_media > 0.25 else "baja"),
            "temperatura": temp, "familias_de_tono": familias, "concentracion_tono_pct": concentracion,
            "aire_pct": aire, "detalle": detalle}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("carpeta")
    ap.add_argument("--gusto", default="gusto.json")
    ap.add_argument("--tipo", default="si", choices=["si", "no", "otra"], help="tipo asignado a las imágenes nuevas")
    a = ap.parse_args()
    if Image is None:
        print("Falta Pillow. Instálalo con:  pip install pillow   (o python3 -m pip install pillow)\nNo se ha cambiado nada.")
        return 2
    if not os.path.isdir(a.carpeta):
        print(f"No existe la carpeta {a.carpeta}")
        return 2
    g = G.cargar(a.gusto)
    ya = {r.get("archivo") for r in g["referencias"]}
    nuevas = 0
    for f in sorted(os.listdir(a.carpeta)):
        if not f.lower().endswith(EXT):
            continue
        ruta = os.path.join(a.carpeta, f)
        try:
            med = medir(ruta)
        except Exception as e:  # imagen corrupta
            print(f"  salto {f}: {e}")
            continue
        existente = next((r for r in g["referencias"] if r.get("archivo") == f), None)
        if existente:
            existente["medido"] = med
            continue
        g["referencias"].append({
            "nombre": os.path.splitext(f)[0], "archivo": f, "tipo": a.tipo,
            "medido": med,
            "interpretacion": {"tono": None, "imagen": None, "voz_del_texto": None, "forma": None, "nota": "pendiente: la rellena el modelo viendo la imagen"},
            "nota_usuario": "", "confirmado": False})
        nuevas += 1
        print(f"  {f}: {med['luminosidad']}, saturación {med['saturacion']}, temperatura {med['temperatura']}, "
              f"aire {med['aire_pct']}%, detalle {med['detalle']}, {med['familias_de_tono']} familia(s) de tono, "
              f"dominantes {', '.join(d['hex'] for d in med['dominantes'][:3])}")
    G.guardar(g, a.gusto)
    print(f"{nuevas} referencia(s) nueva(s); total {len(g['referencias'])} → {a.gusto}")
    print("Siguiente: ver cada imagen, rellenar «interpretacion» y pedir a la persona su nota (qué le gusta).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
