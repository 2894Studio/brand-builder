#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Autotest de la estrategia: el verificador del brief acepta un brief bueno y rechaza los malos, y las guías existen y se enlazan.

Uso:  python3 verificar_estrategia.py        Sale con 1 si algo falla.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: salida en tubería → cp1252
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
BRIEF = os.path.join(AQUI, "verificar_brief.py")
BUENO = os.path.join(RAIZ, "evals", "fixtures", "estrategia", "brief-bueno.md")
fallos = []


def ok(c, msg):
    print(("  ok     " if c else "  FALLO  ") + msg)
    if not c:
        fallos.append(msg)


def verificar(ruta):
    return subprocess.run([sys.executable, BRIEF, ruta], capture_output=True, text=True, encoding="utf-8", errors="replace").returncode


txt = open(BUENO, encoding="utf-8").read()
ok(verificar(BUENO) == 0, "acepta un brief completo (tensión, mapa, posicionamiento, «no es», tres vías, idea rectora, cosas por descubrir y palabras clave)")
cambios = {
    "sin idea rectora": txt.replace("## Idea rectora\nLa prueba técnica antes del contrato.", ""),
    "con posicionamiento sin fórmula": txt.replace("porque **cada perfil pasa por un reto de 90 minutos corregido por un ingeniero senior**", "con calidad"),
    "con la tensión de una sola mitad": txt.replace("pero las agencias solo les dan currículums sin prueba técnica", ""),
    "con solo dos alternativas en el mapa": txt.replace("| Los propios contactos del CTO | Alguien de confianza | Informal, de boca a boca, sin garantía |\n", ""),
    "con solo dos vías": txt[:txt.index("### Vía C")] + txt[txt.index("**Recomendada:**"):],
    "sin recomendar ninguna vía": txt.replace("**Recomendada:** la A, porque", "La A, porque"),
    "con un color en las vías": txt.replace("- **Sensación general:** sobria.", "- **Sensación general:** sobria, con un azul oscuro."),
    "con una tipografía en las vías": txt.replace("- **Sensación general:** cálida.", "- **Sensación general:** cálida, con tipografía redondeada."),
    "con un código de color en la idea rectora": txt.replace("La prueba técnica antes del contrato.", "La prueba técnica antes del contrato (#1B1A17)."),
    "con una idea rectora de relleno largo": txt.replace("La prueba técnica antes del contrato.", "Somos una compañía que existe para acompañar a todas las startups del mundo en el largo camino de encontrar a las personas adecuadas para sus proyectos."),
    "sin cosas por descubrir": txt[:txt.index("## Lo que aún no sabes")] + txt[txt.index("## Palabras clave"):],
    "sin palabras clave": txt[:txt.index("## Palabras clave")] + txt[txt.index("## Riesgos y pendientes"):],
    "con palabras clave sin rellenar": txt.replace("- `technical recruiting brand identity`\n- `startup hiring platform`\n- `rigorous no-nonsense branding`", "- `…`\n- `…`\n- `…`"),
    "con léxico prohibido": txt.replace("Seca, concreta y sin adornos.", "Una marca innovadora que quiere revolucionar y potenciar el sector con una solución integral."),
    "vacío": "# Brief\n\n## Situación\nUna marca innovadora.\n",
}
d = tempfile.mkdtemp()
for nombre, contenido in cambios.items():
    f = os.path.join(d, "malo.md")
    open(f, "w", encoding="utf-8").write(contenido)
    ok(verificar(f) == 1, f"rechaza un brief {nombre}")

# guías y enlaces
for ruta in ("skills/estrategia/SKILL.md", "skills/estrategia/references/entrevista.md", "skills/estrategia/references/vias.md", "skills/estrategia/references/brief-estrategico.md",
             "skills/estrategia/references/palabras-clave.md", "skills/estrategia/references/lexico-prohibido.md", "skills/brand-kit-builder/references/criterio-experto.md",
             "skills/brand-kit-builder/references/preguntas-interactivas.md"):
    ok(os.path.exists(os.path.join(RAIZ, ruta)), f"existe {ruta}")
sk = open(os.path.join(RAIZ, "skills", "estrategia", "SKILL.md"), encoding="utf-8").read()
ok("palabras-clave.md" in sk and "verificar_brief.py" in sk and "AskUserQuestion" in sk, "la skill enlaza las palabras clave, el verificador y el diálogo nativo")
ok("identidad" not in sk and "brief-logo" not in sk, "la skill no ofrece pasos que el plugin ya no tiene")
print()
print("TODO OK" if not fallos else f"{len(fallos)} FALLO(S)")
sys.exit(1 if fallos else 0)
