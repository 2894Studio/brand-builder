#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Propone tres combinaciones de posts (qué es + atributo) de arquetipos distintos para que la persona elija.

Uso:  python3 proponer_posts.py marca.json [--fotos lanzamiento/fotos] [--gusto gusto.json] [--semilla texto]
Cada combinación usa dos arquetipos diferentes y dice qué hay que aportar. Las tres combinaciones no repiten el arquetipo del post 1.
El orden depende de la categoría y de lo que haya (fotos, datos, producto digital); los empates los rompe el nombre de la marca,
así dos marcas parecidas no acaban con el mismo par. Muestra las tres con un diálogo y deja elegir; no elijas tú por defecto la interfaz.
"""
import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DESC = {
    "pasos": ("pasos", "Pasos numerados (un verbo y su consecuencia)", "3 o 4 pasos reales de cómo funciona o qué se hace"),
    "manifiesto": ("manifiesto", "Frase enorme de la voz de la marca, con la inicial a sangre", "una frase del manifiesto de estrategia.md (≤ 12 palabras)"),
    "expresivo_gigante": ("expresivo_gigante", "Campaña expresiva: palabra gigante recortada, foto en marco de sello e insignia", "1 foto con personalidad y una palabra clave de la marca"),
    "expresivo_precio": ("expresivo_precio", "Campaña expresiva con precio enorme (decimales en superíndice) y beneficios", "un precio real (o de ejemplo marcado) y 3 beneficios; 1 foto"),
    "cifra": ("cifra", "Un número gigante con su explicación", "una cifra real propia (plazas, años, precio) o de terceros con fuente"),
    "foto": ("foto", "Foto a sangre con bloque opaco y notas sobre la foto", "1 foto buena (propia, de banco o generada) en fotos/"),
    "pantalla": ("pantalla", "Ventana de escritorio con la interfaz del producto", "solo si el producto tiene interfaz: 3 filas reales"),
    "telefono": ("telefono", "Móvil con la interfaz de la app", "solo si es una app móvil: 3 filas reales"),
    "comparativa": ("comparativa", "Ellos / nosotros", "dato del competidor con fuente y fecha (si no, no se hace)"),
    "mapa": ("mapa", "Mapa de puntos con la zona", "centro, ciudades y una persona destacada reales (necesita Node)"),
}
FAM = {"pantalla": "ui", "telefono": "ui"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("marca")
    ap.add_argument("--fotos")
    ap.add_argument("--gusto")
    ap.add_argument("--semilla", default="")
    a = ap.parse_args()
    m = json.load(open(a.marca, encoding="utf-8"))
    txt = " ".join(str(m.get(k, "")) for k in ("categoria", "publico", "nombre")).lower()
    hay_fotos = bool(a.fotos and os.path.exists(os.path.join(a.fotos, "manifiesto.json")))
    digital = bool(re.search(r"software|\bapp\b|aplicaci|plataforma|saas|\bweb\b|digital|programaci|c[oó]digo|desarrollo|tecnolog|ciberseg|fintech|datos", txt))
    app = bool(re.search(r"\bapp\b|aplicaci", txt))
    visual = bool(re.search(r"fotograf|ilustraci|moda\b|gastronom|restaurante|viaje|arquitect|interiorism|joyer|cosm[eé]t|floristeri|tatuaj", txt))
    local = bool(re.search(r"cerca|zona|barrio|a domicilio|reparto|tienda|taller", txt))
    precio = bool(re.search(r"precio|cuota|suscripci|tarifa|barat|ahorr|gratis", txt))
    h = int(hashlib.sha1((m.get("nombre", "") + a.semilla).encode()).hexdigest(), 16)

    def rota(xs, k):
        if not xs:
            return xs
        k = (h >> k) % len(xs)
        return xs[k:] + xs[:k]
    # tres direcciones: mostrar el producto, contarlo con tipografía, probarlo con un dato
    divertido = False
    if a.gusto and os.path.exists(a.gusto):
        try:
            tn = json.load(open(a.gusto, encoding="utf-8")).get("tonos", {}) or {}
            divertido = bool(tn) and max(tn, key=tn.get) == "divertido"
        except Exception:  # noqa: BLE001
            pass
    divertido = divertido or bool(re.search(r"viaj|ocio|fiesta|evento|divertid|jugueter|helader|festival", txt))
    d_mostrar = (["expresivo_gigante"] if divertido else []) + (["foto"] if (hay_fotos or visual) else []) + (["pantalla"] if digital else []) + (["telefono"] if app else []) + (["mapa"] if local else [])
    d_tipo = ["manifiesto", "pasos"]
    d_dato = (["expresivo_precio"] if (divertido and precio) else []) + ["cifra"] + (["comparativa"] if (digital or precio) else []) + (["mapa"] if local and "mapa" not in d_mostrar else [])
    d_mostrar, d_tipo, d_dato = rota(d_mostrar, 3), rota(d_tipo, 7), rota(d_dato, 11)
    if not d_mostrar:
        d_mostrar = ["foto"]
    m1, t1, a1 = d_mostrar[0], d_tipo[0], d_dato[0]
    m2 = d_mostrar[1] if len(d_mostrar) > 1 else m1
    t2 = d_tipo[1] if len(d_tipo) > 1 else t1
    a2 = d_dato[1] if len(d_dato) > 1 else a1
    # post 1 «qué es»: mostrar o contar; post 2 «atributo»: dato, mostrar o contar; siempre arquetipos de familia distinta
    candidatos = [(m1, a1), (t1, m2 if FAM.get(m2, m2) != FAM.get(t1, t1) else a1), (t2, a2 if FAM.get(a2, a2) != FAM.get(t2, t2) else a1)]
    if h % 2:   # alterna el orden de las dos primeras según la marca
        candidatos[0], candidatos[1] = candidatos[1], candidatos[0]
    combos, vistos = [], set()
    for x, y in candidatos:
        if FAM.get(x, x) == FAM.get(y, y) or (x, y) in vistos:
            continue
        vistos.add((x, y)); combos.append((x, y))
    sin_foto = " (¡necesita fotos! sin ellas, genera algunas con prompts_fotos.py)" if (visual and not hay_fotos) else ""
    temas = [("oscuro", "claro"), ("claro", "oscuro"), ("oscuro", "oscuro")]
    print(f"Propuestas para {m.get('nombre', 'la marca')} (categoría: {m.get('categoria', '—')[:70]})\n")
    for i, (x, y) in enumerate(combos, 1):
        print(f"{'ABC'[i - 1]}) Post 1 «qué es»: {DESC[x][1]}  ·  Post 2 «atributo»: {DESC[y][1]}")
        print(f"   necesita → post 1: {DESC[x][2]}; post 2: {DESC[y][2]}" + (sin_foto if "foto" in (x, y) else ""))
        print(f"   tema sugerido: post 1 {temas[i - 1][0]}, post 2 {temas[i - 1][1]} (que no sean iguales)\n")
    print("Nota: la interfaz (móvil, ventana) solo se propone si el producto es digital; los dos posts siempre son de arquetipos distintos.")
    print("Siguiente: que la persona elija con un diálogo y escribir lanzamiento/brief.json con esos dos recursos (ver kit_lanzamiento.py).")


if __name__ == "__main__":
    main()
