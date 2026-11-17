#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Hook de parada: no deja dar por terminado un kit de lanzamiento que no pasó la puerta de entrega.

Si en trabajo/*/lanzamiento/ hay piezas (bento o posts) y no existe un `.puerta-ok` más reciente que ellas, bloquea la parada una vez
y le dice al agente que use kit_lanzamiento.py. Si el agente ya fue obligado a seguir (stop_hook_active), deja parar para no entrar en
bucle: la entrega tendrá que decir con honestidad que la puerta no se pasó. Solo actúa en Claude Code; no toca nada fuera de lanzamiento/.
"""
import glob
import json
import os
import sys


def _rel(ruta, base=None):
    """os.path.relpath que no falla entre unidades distintas de Windows (devuelve la ruta absoluta)."""
    try:
        return os.path.relpath(ruta, base) if base else os.path.relpath(ruta)
    except ValueError:
        return os.path.abspath(ruta)

try:
    ent = json.load(sys.stdin)
except Exception:  # noqa: BLE001
    ent = {}
cwd = ent.get("cwd") or os.getcwd()
dirs = sorted(glob.glob(os.path.join(cwd, "trabajo", "*", "lanzamiento")), key=os.path.getmtime)
if not dirs or ent.get("stop_hook_active"):
    sys.exit(0)
d = dirs[-1]
piezas = [p for p in glob.glob(os.path.join(d, "*")) if os.path.basename(p).startswith(("bento", "post-")) and os.path.isfile(p)]
if not piezas:
    sys.exit(0)
marca = os.path.join(d, ".puerta-ok")
if os.path.exists(marca) and os.path.getmtime(marca) >= max(os.path.getmtime(p) for p in piezas):
    sys.exit(0)
raiz = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
solo_svg = not any(p.endswith(".html") for p in piezas)
motivo = (
    f"El kit de {_rel(d, cwd)} no ha pasado la puerta de entrega, así que no está terminado. "
    + ("Las piezas son SVG o PNG sueltos y no vienen de los generadores del plugin: no se dibujan a mano. " if solo_svg else "")
    + "Escribe lanzamiento/brief.json (formato en la cabecera de skills/lanzamiento/tools/kit_lanzamiento.py) y ejecuta "
    + f"python3 \"{raiz}/skills/lanzamiento/tools/kit_lanzamiento.py\" <ruta del brief>. "
    + "Corrige lo que marque el crítico y la puerta y repite (máximo 2 vueltas por pieza). Si de verdad no se puede pasar, "
    + "dilo en el mensaje final con el motivo en lugar de decir «terminado»."
)
print(json.dumps({"decision": "block", "reason": motivo}, ensure_ascii=False))
