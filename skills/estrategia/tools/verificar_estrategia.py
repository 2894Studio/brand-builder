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
    "sin la sección de qué buscar y qué evitar": txt[:txt.index("## Qué buscar")] + txt[txt.index("## Riesgos y pendientes"):],
    "con solo dos cosas que evitar": txt.replace("- Exceso de ornamento, porque la marca promete sencillez.\n", ""),
    "con una cosa que buscar sin «porque»": txt.replace("- Un tono sobrio con un toque humano, porque el riesgo de la vía es sonar frío.", "- Un tono sobrio con un toque humano."),
    "con un color concreto en qué buscar": txt.replace("- Composiciones con mucho aire y pocos elementos,", "- Composiciones con fondo azul y pocos elementos,"),
    "con un código hex en qué evitar": txt.replace("- Exceso de ornamento, porque", "- Exceso de ornamento (#FF0000), porque"),
    "sin las cuatro fuerzas": txt.replace("- **Lo que le da miedo (ansiedad):** que otra agencia más le haga perder tiempo y dinero.\n", ""),
    "con una sola frase literal del cliente": txt.replace(", «me mandan CVs con todas las palabras de moda»", ""),
    "sin palabras que evitar": txt.replace("**Palabras que evitar:** talento de primer nivel, capital humano.", ""),
    "sin a quién no sirve": txt.replace("**A quién no sirve:** a quien contrata en volumen y no puede esperar una prueba.", ""),
    "con una sola objeción": txt.replace("- «Cobráis comisión y no sé qué recibo» → se entrega la corrección escrita de cada candidato.\n", ""),
    "vacío": "# Brief\n\n## Situación\nUna marca innovadora.\n",
}
d = tempfile.mkdtemp()
idea = (txt.replace("Cribo es una agencia pequeña", "Cribo será una agencia pequeña").replace("Lleva seis meses y trabaja sobre todo por recomendación.", "Todavía no ha vendido nada: es una idea en etapa cero.")
        .replace("- Frases literales: «no sé si este perfil sabe hacer lo que dice», «me mandan CVs con todas las palabras de moda».", "- Frases literales (*Supuesto*, aún sin conversaciones): «no sé si este perfil sabe hacer lo que dice», «me mandan CVs con todas las palabras de moda»."))
f0 = os.path.join(d, "idea.md")
open(f0, "w", encoding="utf-8").write(idea)
ok(verificar(f0) == 0, "acepta un brief de una idea sin clientes (frases literales marcadas como Supuesto)")
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
ok("pregunta numerada propia" in sk and "dentro de la lista numerada" in sk, "la skill exige que el nombre y toda pregunta vayan dentro de la lista numerada")
ok("marketingskills" in sk, "la skill propone marketingskills como único siguiente paso")
print()
print("TODO OK" if not fallos else f"{len(fallos)} FALLO(S)")
sys.exit(1 if fallos else 0)
