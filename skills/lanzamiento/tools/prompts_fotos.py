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
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402

CANVA_RATIO = {"4:3": "LANDSCAPE_4_3", "3:4": "PORTRAIT_3_4", "1:1": "SQUARE_1_1", "4:5": "PORTRAIT_4_5"}
TIPOS = [
    ("equipo-1", "4:3 (horizontal)", "equipo", "Un grupo de 3 a 5 personas diversas, en su contexto real de trabajo, interactuando de forma natural (hablando, mirando una pantalla o un material), no posando mirando a cámara."),
    ("retrato-1", "3:4 (vertical)", "retrato", "Retrato de una sola persona en su entorno de trabajo, a media distancia, mirada natural, luz lateral suave, fondo con profundidad y desenfoque realista."),
    ("producto-1", "1:1 (cuadrado)", "producto", "Detalle del producto o servicio en uso, en primer plano, manos o contexto humano parcial, composición limpia con aire alrededor."),
    ("objeto-1", "4:5 (vertical)", "objeto", "Un objeto característico del producto o del servicio, con un accesorio que dé personalidad, sobre un fondo liso de un solo color saturado, fotografía de estudio con luz dura y sombra nítida, vista cenital ligeramente inclinada, composición minimalista con aire alrededor."),
    ("local-1", "4:3 (horizontal)", "escena", "El lugar o el entorno donde ocurre el servicio, plano general con orientación clara y sin personas en primer plano."),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("marca")
    ap.add_argument("--salida", default="lanzamiento/prompts-fotos.md")
    ap.add_argument("--proveedor", choices=["auto", "canva", "flora", "higgsfield", "magnific", "spaces", "gemini", "flow", "todos"], default="auto", help="adapta las instrucciones a la herramienta; auto lee trabajo/*/proveedor-imagen.json (ver proveedor_imagen.py) y, si no hay, usa todos")
    for _, _, clave, _ in TIPOS:
        ap.add_argument("--" + clave)
    a = ap.parse_args()
    if a.proveedor == "auto":
        import glob
        enc = sorted(glob.glob(os.path.join("trabajo", "*", "proveedor-imagen.json")), key=os.path.getmtime)
        prov = ""
        if enc:
            try:
                prov = json.load(open(enc[-1], encoding="utf-8")).get("proveedor", "")
            except Exception:  # noqa: BLE001
                prov = ""
        a.proveedor = prov if prov in ("canva", "flora", "higgsfield", "magnific", "spaces", "gemini", "flow") else "todos"
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
        if clave == "objeto":
            prompt = f"{sujeto} Fondo liso de color {c['nombres']['acento']} ({c['acento']}). Contexto de marca: {cat}. Formato {formato}. Sin ningún texto, sin logotipos, sin marcas de agua. Alta resolución."
        else:
            prompt = f"{sujeto} {contexto} Estilo: {base_estilo}. Paleta: {paleta}. Formato {formato}. {comun}"
        bloques.append((archivo, formato, prompt))
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    with open(a.salida, "w", encoding="utf-8") as fh:
        if a.proveedor == "canva":
            donde = ("Usa cada prompt con `generate-image` del conector de **Canva** y la proporción (`aspectRatio`) indicada en cada bloque. "
                     "Cada generación gasta créditos de Canva: genera 1 por prompt y solo repite si hace falta (tope: 8 por kit).")
        elif a.proveedor == "flora":
            donde = ("Usa cada prompt con `flora_create_generations` (FLORA, `type` image, `add_to_canvas` false si no quieres ensuciar un proyecto) y el `aspect_ratio` indicado en cada bloque. "
                     "**Antes, pide el presupuesto con `quote: true` y dile a la persona el coste en USD.** Modelos probados: `t2i-elote-gateway` (Nano Banana 2.1, ~0,05 USD, acepta `aspect_ratio`), "
                     "`t2i-gpt-image-2-6-sunburst` (GPT Image, ~0,055 USD, el que mejor clava colores planos saturados) y, más barato, `t2i-seedream-5-5-t2i` (~0,024 USD, falló por proveedor caído en la prueba). "
                     "La imagen sale en `outputs[].url`: se descarga directamente con `curl` (sin exportar nada).")
        elif a.proveedor == "gemini" and os.environ.get("GEMINI_API_KEY"):
            donde = ("Hay clave de la API de Gemini: genera cada imagen con `python3 skills/lanzamiento/tools/generar_gemini.py generar \"<prompt>\" --como <archivo> --aspecto <formato>` "
                     "(guarda la imagen y anota los créditos). Ojo: la API de imágenes de Gemini exige facturación activada (el nivel gratuito tiene límite 0).")
        elif a.proveedor in ("higgsfield", "magnific", "spaces"):
            nom = {"higgsfield": "Higgsfield", "magnific": "Magnific", "spaces": "Spaces"}[a.proveedor]
            donde = (f"Usa cada prompt en **{nom}**: con su conector MCP si lo tienes instalado (mira sus herramientas de imagen y pide el coste antes de generar) o pegándolo a mano en su web. "
                     f"Guarda cada imagen en `fotos/` con el nombre indicado. **Receta no verificada con {nom} en este plugin:** el primer uso dirá qué ajustar. "
                     + ("Magnific es sobre todo para **mejorar** (ampliar y dar detalle) una foto que ya tienes: pasa por él la foto elegida, no sustituye a un generador. " if a.proveedor == "magnific" else ""))
        elif a.proveedor in ("gemini", "flow"):
            donde = ("Pega cada prompt en **" + ("Gemini** (crear imágenes)" if a.proveedor == "gemini" else "Google Flow** (modo imagen)") +
                     ". Si la herramienta tiene selector de formato, elígelo; si no, el formato ya va dentro del prompt. "
                     "Genera 2 o 3 variantes y quédate con la mejor. Revisa tu cuota gratuita: cambia según el plan.")
        else:
            donde = ("Pega cada prompt en **Gemini**, en **Google Flow** (modo imagen) o úsalo con `generate-image` del conector de **Canva** o `flora_create_generations` de **FLORA** "
                     "(con la proporción indicada). Revisa la cuota o los créditos de cada herramienta: cambian según el plan.")
        fh.write(f"# Prompts de fotos · {nombre}\n\n" + donde + "\n\n"
                 "**Antes de usarlas:** son personas y lugares sintéticos. No se presentan como tu equipo, tus clientes ni tu local reales. "
                 + ("" if a.proveedor == "canva" else "Google suele añadir una marca invisible a lo que genera; no la quites. " if a.proveedor in ("gemini", "flow", "todos") else "") + "Se anotan con origen `ia` en `fotos/creditos.md` "
                 "(con `tools/registrar_foto.py`, o a mano: `| equipo-1.png | ia | Canva, Gemini o Flow (generada) | n/a | n/a |`). Si no te convence la persona, repite: no la retoques para que parezca otra.\n\n"
                 "Mira bien la imagen antes de aceptarla: manos, dientes, texto fantasma en pantallas o carteles, simetrías raras.\n\n")
        for archivo, formato, prompt in bloques:
            ratio = CANVA_RATIO.get(formato.split()[0], "")
            extra = (f" Proporción para Canva: `{ratio}`." if a.proveedor in ("canva", "todos") and ratio else "") + \
                    (f" `aspect_ratio` para FLORA: `{formato.split()[0]}`." if a.proveedor in ("flora", "todos") else "")
            fh.write(f"## {archivo} · {formato}\n\nGuárdala como `fotos/{archivo}.png`.{extra}\n\n```\n{prompt}\n```\n\n")
        fh.write("## Si el resultado sale genérico\n\nCambia el **sujeto**, no la paleta: más concreto (qué hace la persona, con qué objeto, en qué lugar exacto) "
                 "y cita un atributo de tus referencias en `gusto.json` (encuadre, luz, distancia). Repite como máximo 2 veces por prompt.\n")
    print(f"ok {a.salida} ({len(bloques)} prompts)")
    print("Siguiente: genera las imágenes, guárdalas en fotos/, añade su fila a creditos.md con origen ia y pasa preparar_fotos.py")


if __name__ == "__main__":
    main()
