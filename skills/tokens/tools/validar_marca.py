#!/usr/bin/env python3
"""Valida un marca.json: contrato de creative-architect + extensiones de brand-kit-builder.

Uso:  python3 validar_marca.py marca.json
Salida: 0 si es válido (aunque haya avisos), 1 si hay errores, 2 si no se puede leer.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marca_lib as m  # noqa: E402


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        marca = m.cargar(argv[1])
    except (OSError, json.JSONDecodeError) as ex:
        print(f"No se puede leer {argv[1]}: {ex}", file=sys.stderr)
        return 2
    ok = m.informe(argv[1], marca)
    print(("válido: " if ok else "NO válido: ") + argv[1])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
