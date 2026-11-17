#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Abre el etiquetador de referencias en el navegador y guarda directamente en el proyecto (solo en tu ordenador, nada sale de él).

Uso:  python3 etiquetador.py [--carpeta .] [--puerto 8765] [--no-abrir]
Sirve etiquetador.html en http://127.0.0.1:PUERTO; el botón «Guardar en el proyecto» crea <carpeta>/referencias/ y actualiza <carpeta>/gusto.json
(mide las imágenes y guarda tus notas y decisiones). Sin este servidor, abre etiquetador.html a mano y usa «Descargar ZIP» + importar_etiquetado.py.
Solo escucha en 127.0.0.1. Ctrl+C para cerrar.
"""
import argparse
import http.server
import json
import os
import sys
import threading
import webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import importar_etiquetado as I  # noqa: E402

MAX = 120 * 1024 * 1024


def servidor(carpeta, puerto=8765):
    gusto = os.path.join(carpeta, "gusto.json")
    refs = os.path.join(carpeta, "referencias")

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, codigo, obj):
            b = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(codigo)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            if self.path.split("?")[0] == "/ping":
                return self._json(200, {"ok": True})
            if self.path.split("?")[0] in ("/", "/etiquetador.html"):
                b = open(os.path.join(AQUI, "etiquetador.html"), "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)
                return
            self.send_error(404)

        def do_POST(self):
            if self.path != "/guardar":
                return self._json(404, {"ok": False, "error": "ruta desconocida"})
            if (self.headers.get("Host", "").split(":")[0] not in ("127.0.0.1", "localhost")):
                return self._json(403, {"ok": False, "error": "solo local"})
            n = int(self.headers.get("Content-Length", 0))
            if n <= 0 or n > MAX:
                return self._json(413, {"ok": False, "error": "tamaño no admitido"})
            try:
                meta = json.loads(self.rfile.read(n).decode("utf-8"))
                msg, err, av = I.importar(meta, I.desde_dataurl, gusto, refs)
            except Exception as e:  # noqa: BLE001
                return self._json(400, {"ok": False, "error": str(e)[:200]})
            return self._json(200, {"ok": True, "mensaje": msg + (" · avisos: " + "; ".join(av) if av else "") + (" · ERRORES: " + "; ".join(err) if err else "")})

    return http.server.ThreadingHTTPServer(("127.0.0.1", puerto), H)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carpeta", default=".")
    ap.add_argument("--puerto", type=int, default=8765)
    ap.add_argument("--no-abrir", action="store_true")
    a = ap.parse_args()
    srv = servidor(os.path.abspath(a.carpeta), a.puerto)
    url = f"http://127.0.0.1:{srv.server_port}/"
    print(f"Etiquetador en {url}  (guarda en {os.path.abspath(a.carpeta)}). Ctrl+C para cerrar.")
    if not a.no_abrir:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
