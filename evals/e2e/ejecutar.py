#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Prueba de punta a punta de la estrategia con un modelo real y una persona simulada.

Uso:  python3 evals/e2e/ejecutar.py evals/e2e/escenarios/estrategia_exploracion.json [--modelo claude-sonnet-5-5] [--max-usd 3] [--max-turnos 8] [--salida carpeta]
Instala el plugin en una configuración aislada, envía el primer mensaje y contesta cada ronda con las frases del escenario («por_turno»).
Mide por turno cuántos «?» hay y si se cuela lenguaje visual (logo, paleta, tipografía, hex, prompts), y al final pasa el verificador del brief.
Cuesta unos 1 USD con Sonnet. Necesita la CLI `claude` y credenciales (por defecto ~/.claude/.credentials.json).
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
BRIEF = os.path.join(RAIZ, "skills", "estrategia", "tools", "verificar_brief.py")
VISUAL = r"#[0-9a-f]{6}\b|\blogo\w*|\bpaleta\b|\btipograf\w*|\bprompt\w*"


def sh(cmd, cwd=None, env=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)


def brief_ok(proy):
    est = sorted(glob.glob(os.path.join(proy, "trabajo", "*", "estrategia.md")), key=os.path.getmtime)
    if not est:
        return None, None
    r = sh([sys.executable, BRIEF, est[-1]])
    return est[-1], r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("escenario")
    ap.add_argument("--modelo", default="claude-sonnet-5-5")
    ap.add_argument("--max-usd", type=float, default=3.0)
    ap.add_argument("--max-turnos", type=int, default=8)
    ap.add_argument("--salida", default=os.path.join(tempfile.gettempdir(), "brand-kit-e2e"))
    ap.add_argument("--credenciales", default="~/.claude/.credentials.json")
    a = ap.parse_args()
    esc = json.load(open(a.escenario, encoding="utf-8"))
    base = os.path.join(a.salida, os.path.splitext(os.path.basename(a.escenario))[0])
    shutil.rmtree(base, ignore_errors=True)
    proy, cfg = os.path.join(base, "proyecto"), os.path.join(base, "cfg")
    os.makedirs(proy)
    os.makedirs(cfg)
    cred = os.path.expanduser(a.credenciales)
    if os.path.exists(cred):
        shutil.copy(cred, os.path.join(cfg, ".credentials.json"))
    env = dict(os.environ, CLAUDE_CONFIG_DIR=cfg)
    for c in (["claude", "plugin", "marketplace", "add", RAIZ], ["claude", "plugin", "install", "brand-kit-builder@brand-kit-builder"]):
        r = sh(c, cwd=proy, env=env)
        if r.returncode != 0:
            sys.exit("No se pudo instalar el plugin: " + (r.stdout + r.stderr)[-300:])
    gasto, sid, turnos, msg, log, t0 = 0.0, None, 0, esc["mensaje_inicial"], [], time.time()
    por_turno = esc.get("por_turno") or []
    while turnos < a.max_turnos and gasto < a.max_usd:
        cmd = ["claude", "-p", "--model", a.modelo, "--output-format", "json", "--max-budget-usd", str(max(0.3, a.max_usd - gasto)), "--permission-mode", "bypassPermissions"]
        if sid:
            cmd += ["--resume", sid]
        r = sh(cmd + [msg], cwd=proy, env=env, timeout=1500)
        try:
            d = json.loads(r.stdout)
        except Exception:  # noqa: BLE001
            log.append({"turno": turnos + 1, "error": (r.stdout + r.stderr)[-300:]})
            break
        sid = d.get("session_id", sid)
        gasto += float(d.get("total_cost_usd") or 0)
        turnos += 1
        texto = d.get("result", "")
        log.append({"turno": turnos, "coste": round(float(d.get("total_cost_usd") or 0), 4), "agente": texto, "preguntas": texto.count("?"),
                    "visual": sorted({m.group(0).lower() for m in re.finditer(VISUAL, texto, re.I)})})
        print(f"  turno {turnos}: {gasto:.2f} USD")
        est, r0 = brief_ok(proy)
        if est and r0.returncode == 0 and glob.glob(os.path.join(os.path.dirname(est), "instrucciones-de-proyecto.md")):
            break
        msg = por_turno[turnos - 1] if turnos - 1 < len(por_turno) else esc["respuesta_final"]
        log[-1]["respuesta"] = msg[:300]
    est, r0 = brief_ok(proy)
    fallos = [l.strip()[:160] for l in (r0.stdout.splitlines() if r0 else []) if l.strip().startswith("FALLO")]
    t1 = (log[0].get("agente", "") if log else "")
    pide_nombre = "nombre" in t1.lower()
    nombre_en_lista = bool(re.search(r"(?m)^\s*\d+[.)]\s+.*nombre", t1, re.I))
    L = [f"# {esc['nombre']}", "", f"- Modelo: {a.modelo} · turnos: {turnos} · coste: {gasto:.2f} USD · {round((time.time() - t0) / 60, 1)} min",
         "- Rondas: " + ", ".join(f"turno {t['turno']}: {t.get('preguntas', 0)} «?»" + (f" · visual: {', '.join(t['visual'])}" if t.get("visual") else "") for t in log),
         f"- Nombre en la ronda 1: {'pregunta numerada' if nombre_en_lista else ('SUELTO fuera de la lista' if pide_nombre else 'no se pide (ya lo dio)')}",
         f"- Instrucciones de proyecto: {'sí' if (est and glob.glob(os.path.join(os.path.dirname(est), 'instrucciones-de-proyecto.md'))) else 'no creadas'}",
         f"- Brief estratégico: {'CORRECTO' if (r0 and r0.returncode == 0) else ('INCOMPLETO' if est else 'no creado')}" + "".join(f"\n  - {x}" for x in fallos)]
    open(os.path.join(base, "informe.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump({"escenario": esc["nombre"], "turnos": log, "brief": est}, open(os.path.join(base, "informe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(L))
    print("Informe:", os.path.join(base, "informe.md"))


if __name__ == "__main__":
    main()
