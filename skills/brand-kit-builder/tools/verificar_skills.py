#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Comprueba que todas las skills se pueden leer desde otras herramientas (Antigravity, Codex, Cline…), no solo desde Claude Code.

Claude Code tolera un YAML flojo; los lectores estrictos no. Un `description:` con «: » sin comillas hace que la skill
se SALTE en silencio (pasó: 5 de 10 skills). Esta prueba lo evita.

Comprueba en cada skills/*/SKILL.md: cabecera con `name` y `description`; `name` igual al nombre de la carpeta; `description` de
1 a 1024 caracteres; y que los enlaces de AGENTS.md existan; y que la cabecera se lea con un YAML estricto (PyYAML si está instalado; si no, que la descripción vaya
entre comillas o no lleve «: » ni « #»).

Uso:  python3 verificar_skills.py [carpeta_raiz_del_repo]      Sale con 1 si algo falla.
"""
import glob
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def main():
    raiz = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    fallos, n = [], 0
    for p in sorted(glob.glob(os.path.join(raiz, "skills", "*", "SKILL.md"))):
        n += 1
        carpeta = os.path.basename(os.path.dirname(p))
        m = re.match(r"^---\n(.*?)\n---\n", open(p, encoding="utf-8").read(), re.S)
        if not m:
            fallos.append(f"{carpeta}: no tiene cabecera ---")
            continue
        fm = m.group(1)
        if yaml:
            try:
                d = yaml.safe_load(fm)
            except yaml.YAMLError as e:
                fallos.append(f"{carpeta}: YAML no válido para un lector estricto ({str(e).splitlines()[0]})")
                continue
        else:
            d = {}
            for linea in fm.split("\n"):
                k, _, v = linea.partition(":")
                d[k.strip()] = v.strip()
            v = d.get("description", "")
            if v and not (v.startswith('"') and v.endswith('"')) and (": " in v or " #" in v):
                fallos.append(f"{carpeta}: «description» con «: » o « #» y sin comillas")
                continue
            d["description"] = v.strip('"')
        if not isinstance(d, dict) or not d.get("name") or not d.get("description"):
            fallos.append(f"{carpeta}: faltan name o description")
            continue
        if d["name"] != carpeta:
            fallos.append(f"{carpeta}: name «{d['name']}» no coincide con la carpeta")
        if not 1 <= len(str(d["description"])) <= 1024:
            fallos.append(f"{carpeta}: description de {len(str(d['description']))} caracteres (máximo 1024)")
    # AGENTS.md es un puntero: todos los archivos que enlaza deben existir
    ag = os.path.join(raiz, "AGENTS.md")
    if os.path.exists(ag):
        for ruta in re.findall(r"\]\(([^)#]+)\)", open(ag, encoding="utf-8").read()):
            if not ruta.startswith("http") and not os.path.exists(os.path.join(raiz, ruta)):
                fallos.append(f"AGENTS.md enlaza a «{ruta}», que no existe")
    for f in fallos:
        print("  FALLO ", f)
    print(f"{n} skill(s) revisadas con {'PyYAML (estricto)' if yaml else 'la comprobación básica (instala PyYAML para la estricta)'}")
    print("TODO OK" if not fallos else f"{len(fallos)} FALLO(S)")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
