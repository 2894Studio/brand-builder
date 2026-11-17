#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Genera una imagen con la API de Gemini (clave de Google AI Studio), la guarda en fotos/ y anota sus créditos (origen ia).

Uso:  export GEMINI_API_KEY=tu_clave            (la clave se pide en aistudio.google.com/apikey; PowerShell: $env:GEMINI_API_KEY="tu_clave")
      python3 generar_gemini.py modelos                                      → lista los modelos que declaran generar imágenes
      python3 generar_gemini.py generar "prompt" --como equipo-1 --aspecto 4:3 [--tamano 2K] [--modelo ID] [--carpeta fotos]
Los prompts salen de prompts_fotos.py. El modelo por defecto es el primero de la lista que declara imagen (o GEMINI_IMAGE_MODEL); los nombres
de modelo cambian con el tiempo: si uno falla, ejecuta «modelos» y elige otro. **La clave es gratis, pero el nivel gratuito tiene límite 0 para imágenes (verificado el 2026-11-17): hace falta activar la facturación en AI Studio.**
No se pega la clave en el chat ni en archivos: solo variable de entorno. Receta **no verificada con la API real** en este plugin (probada con un servidor simulado).
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta")
AQUI = os.path.dirname(os.path.abspath(__file__))


def clave():
    k = os.environ.get("GEMINI_API_KEY")
    if not k:
        sys.exit("Falta GEMINI_API_KEY. Conseguir la clave es gratis (pero generar imágenes por API exige activar la facturación en AI Studio): entra en aistudio.google.com/apikey con tu cuenta de Google, crea una clave y ejecuta\n"
                 "  export GEMINI_API_KEY=tu_clave        (PowerShell: $env:GEMINI_API_KEY=\"tu_clave\")\n"
                 "Sin clave puedes pegar los prompts a mano en Gemini (gemini.google.com) y guardar la imagen en fotos/ (prompts_fotos.py --proveedor gemini).")
    return k


def llamar(ruta, k, cuerpo=None):
    req = urllib.request.Request(BASE + ruta, data=json.dumps(cuerpo).encode() if cuerpo is not None else None,
                                 headers={"x-goog-api-key": k, "Content-Type": "application/json", "User-Agent": "brand-kit-builder/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detalle = ""
        try:
            detalle = json.load(e).get("error", {}).get("message", "")
        except Exception:  # noqa: BLE001
            pass
        if e.code in (400, 403) and "API key" in detalle:
            sys.exit("Google rechazó la clave: revisa GEMINI_API_KEY.")
        if e.code == 429:
            if "limit: 0" in detalle and "Free Tier" in detalle:
                sys.exit("Google: tu clave está en el nivel GRATUITO, que tiene límite 0 para generar imágenes (verificado el 2026-11-17 con una clave real). "
                         "La clave funciona, pero la generación de imágenes con la API exige activar la facturación en Google AI Studio (pago por uso). "
                         "Sin facturación, usa Gemini en la web (gemini.google.com) o Google Flow pegando los prompts de prompts_fotos.py, o Canva.")
            sys.exit("Google: cuota agotada (429). Espera un rato o usa otro proveedor. Detalle: " + detalle[:240])
        sys.exit(f"Google respondió {e.code}: {detalle[:200]}")
    except urllib.error.URLError as e:
        sys.exit(f"No se pudo conectar con la API de Gemini ({e.reason}).")


def modelos(k):
    d = llamar("/models?pageSize=200", k)
    out = [m["name"].split("/")[-1] for m in d.get("models", []) if "image" in m["name"].lower() and "generateContent" in m.get("supportedGenerationMethods", [])]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("modelos")
    g = sub.add_parser("generar")
    g.add_argument("prompt")
    g.add_argument("--como", required=True, help="nombre del archivo: equipo-1, retrato-1, objeto-1…")
    g.add_argument("--aspecto", default="", help="1:1, 4:3, 3:4, 4:5, 16:9, 9:16…")
    g.add_argument("--tamano", default="", help="1K, 2K o 4K si el modelo lo admite (para llegar a ≥ 1080 px de lado corto)")
    g.add_argument("--modelo", default=os.environ.get("GEMINI_IMAGE_MODEL", ""))
    g.add_argument("--carpeta", default="fotos")
    g.add_argument("--reemplazar", action="store_true")
    a = ap.parse_args()
    k = clave()
    if a.cmd == "modelos":
        ms = modelos(k)
        print("\n".join(ms) if ms else "(la API no declara modelos con imagen para esta clave)")
        return 0
    ms = [] if a.modelo else modelos(k)
    pref = ("gemini-3.1-flash-image", "gemini-3-pro-image", "gemini-2.5-flash-image")
    modelo = a.modelo or next((p for p in pref if p in ms), "") or next(iter(ms), "")
    if not modelo:
        sys.exit("No hay un modelo de imagen disponible para esta clave: ejecuta «modelos» o define GEMINI_IMAGE_MODEL.")
    cfg = {"responseModalities": ["IMAGE"]}
    if a.aspecto or a.tamano:
        cfg["imageConfig"] = {k: v for k, v in (("aspectRatio", a.aspecto), ("imageSize", a.tamano)) if v}
    d = llamar(f"/models/{modelo}:generateContent", k, {"contents": [{"parts": [{"text": a.prompt}]}], "generationConfig": cfg})
    datos = None
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            ib = p.get("inlineData") or p.get("inline_data")
            if ib and ib.get("data"):
                datos = base64.b64decode(ib["data"])
    if not datos:
        motivo = (d.get("promptFeedback", {}) or {}).get("blockReason", "")
        sys.exit("La API no devolvió ninguna imagen" + (f" (bloqueada: {motivo})" if motivo else "") + ". Cambia el prompt o el modelo.")
    os.makedirs(a.carpeta, exist_ok=True)
    nombre = a.como if os.path.splitext(a.como)[1] else a.como + ".png"
    destino = os.path.join(a.carpeta, nombre)
    if os.path.exists(destino) and not a.reemplazar:
        sys.exit(f"{destino} ya existe; usa --reemplazar o elige otro nombre.")
    open(destino, "wb").write(datos)
    r = subprocess.run([sys.executable, os.path.join(AQUI, "registrar_foto.py"), destino, "--origen", "ia", "--fuente", f"Gemini API ({modelo}, generada)"], capture_output=True, text=True)
    print(f"ok {destino} (modelo {modelo})")
    print(r.stdout.strip() or r.stderr.strip())
    print("Mira la imagen antes de aceptarla (manos, texto fantasma). Siguiente: preparar_fotos.py fotos --salida lanzamiento/fotos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
