#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Escribe prompts listos para pegar en Gemini o en Google Flow y generar las fotos de la marca.

Uso:  python3 prompts_fotos.py marca.json [--salida lanzamiento/prompts-fotos.md]
        [--equipo "profesores y alumnos en una clase en directo"] [--retrato "una profesora de programación"]
        [--producto "portátil con el editor de código abierto"] [--escena "aula con pantallas"]
Cada prompt sale de marca.json (categoría, público, estilo fotográfico, colores). Sin texto, sin logos.
Las imágenes generadas se guardan como fotos/<nombre>.png, se anotan en creditos.md con origen «ia» y NUNCA
se presentan como el equipo o los clientes reales de una empresa.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402

TIPOS = [
    ("equipo-1", "4:3 (horizontal)", "equipo", "Un grupo de 3 a 5 personas diversas, en su contexto real de trabajo, interactuando de forma natural (hablando, mirando una pantalla o un material), no posando mirando a cámara."),
    ("retrato-1", "3:4 (vertical)", "retrato", "Retrato de una sola persona en su entorno de trabajo, a media distancia, mirada natural, luz lateral suave, fondo con profundidad y desenfoque realista."),
    ("producto-1", "1:1 (cuadrado)", "producto", "Detalle del producto o servicio en uso, en primer plano, manos o contexto humano parcial, composición limpia con aire alrededor."),
    ("local-1", "4:3 (horizontal)", "escena", "El lugar o el entorno donde ocurre el servicio, plano general con orientación clara y sin personas en primer plano."),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("marca")
    ap.add_argument("--salida", default="lanzamiento/prompts-fotos.md")
    for _, _, clave, _ in TIPOS:
        ap.add_argument("--" + clave)
    a = ap.parse_args()
    m = L.cargar_marca(a.marca)
    c = L.colores(m)
    nombre = m.get("nombre", "la marca")
    cat = m.get("categoria", "")
    pub = m.get("publico", "")
    estilo = m.get("visual", {}).get("estilo", "")
    if not estilo:
        print("aviso: marca.json no tiene visual.estilo; los prompts saldrán con un estilo fotográfico genérico. Define uno en identidad.")
    paleta = f"tonos dominantes {c['nombres']['primario']} ({c['primario']}) y {c['nombres']['neutro']} ({c['neutro']}), con un solo toque de {c['nombres']['acento']} ({c['acento']})"
    base_estilo = estilo or "fotografía documental con luz natural, color sobrio, grano fino"
    comun = ("Fotografía realista, sin ningún texto, sin logotipos, sin marcas de agua, sin rótulos legibles. "
             "Personas con rasgos naturales, manos y dedos anatómicamente correctos, sin deformaciones. Alta resolución.")
    bloques = []
    for archivo, formato, clave, defecto in TIPOS:
        sujeto = (getattr(a, clave) or defecto).strip()
        sujeto = sujeto[:1].upper() + sujeto[1:]
        if not sujeto.endswith("."):
            sujeto += "."
        contexto = f"Contexto de marca: {cat}." + (f" Para {pub.rstrip('.')}." if pub else "")
        prompt = f"{sujeto} {contexto} Estilo: {base_estilo}. Paleta: {paleta}. Formato {formato}. {comun}"
        bloques.append((archivo, formato, prompt))
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    with open(a.salida, "w", encoding="utf-8") as fh:
        fh.write(f"# Prompts de fotos · {nombre}\n\n"
                 "Pega cada prompt en **Gemini** (crear imágenes) o en **Google Flow** (modo imagen). Si la herramienta tiene selector de formato, "
                 "elígelo; si no, el formato ya va dentro del prompt. Genera 2 o 3 variantes por prompt y quédate con la mejor. "
                 "Revisa tu cuota gratuita en cada herramienta: cambia según el plan.\n\n"
                 "**Antes de usarlas:** son personas y lugares sintéticos. No se presentan como tu equipo, tus clientes ni tu local reales. "
                 "Google suele añadir una marca invisible a lo que genera; no la quites. Se anotan con origen `ia` en `fotos/creditos.md` "
                 "(`| equipo-1.png | ia | Gemini (generada) | n/a | n/a |`). Si no te convence la persona, repite: no la retoques para que parezca otra.\n\n"
                 "Mira bien la imagen antes de aceptarla: manos, dientes, texto fantasma en pantallas o carteles, simetrías raras.\n\n")
        for archivo, formato, prompt in bloques:
            fh.write(f"## {archivo} · {formato}\n\nGuárdala como `fotos/{archivo}.png`.\n\n```\n{prompt}\n```\n\n")
        fh.write("## Si el resultado sale genérico\n\nCambia el **sujeto**, no la paleta: más concreto (qué hace la persona, con qué objeto, en qué lugar exacto) "
                 "y cita un atributo de tus referencias en `gusto.json` (encuadre, luz, distancia). Repite como máximo 2 veces por prompt.\n")
    print(f"ok {a.salida} ({len(bloques)} prompts)")
    print("Siguiente: genera las imágenes, guárdalas en fotos/, añade su fila a creditos.md con origen ia y pasa preparar_fotos.py")


if __name__ == "__main__":
    main()
