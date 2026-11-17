#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Prueba de punta a punta del plugin: un agente barato recorre el flujo y se mide el resultado con la puerta de entrega.

Uso:  python3 evals/e2e/ejecutar.py evals/e2e/escenarios/escuela_codigo.json [--gusto-zip referencias-etiquetadas.zip]
        [--modelo claude-haiku-5-5] [--max-usd 2.5] [--max-turnos 14] [--salida carpeta] [--credenciales ~/.claude/.credentials.json]
        python3 evals/e2e/ejecutar.py --todos
Qué hace: instala el plugin desde esta carpeta en una configuración aislada (no toca la tuya), importa el gusto si se da, abre una sesión de
`claude -p` con el mensaje del escenario y contesta a sus preguntas con las respuestas del escenario hasta que la puerta de entrega se abre,
se agotan los turnos o se pasa el presupuesto. Después mide: puerta de entrega, huellas de plantilla, arquetipos de los posts, variedad,
piezas dibujadas a mano y revisión contra el gusto. Escribe informe.md y informe.json en la salida.
**Gasta tokens de tu cuenta** (con Haiku, del orden de 1 a 2 USD por escenario): el tope --max-usd corta la ejecución.
"""
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):      # Windows: con la salida en una tubería Python usaría cp1252 y se rompería con «→», «≈», etc.
    try:
        _flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
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


def sh(cmd, cwd=None, env=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)


def respuesta(esc, texto):
    t = (texto or "").lower()
    for r in esc.get("respuestas", []):
        if any(k in t for k in r["cuando"]):
            return r["responde"]
    return esc["respuesta_por_defecto"]


def medir(proy):
    """Mide lo que dejó el agente. Devuelve un diccionario."""
    res = {"brief": {}, "lanzamiento": None, "puerta": None, "fallos": [], "tells": [], "arquetipos": {}, "svg_a_mano": False, "revision_gusto": None, "piezas": []}
    est = sorted(glob.glob(os.path.join(proy, "trabajo", "*", "estrategia.md")), key=os.path.getmtime)
    if est:
        r0 = sh([sys.executable, os.path.join(RAIZ, "skills", "estrategia", "tools", "verificar_brief.py"), est[-1]])
        res["brief"] = {"estrategia": os.path.relpath(est[-1], proy), "verificador": "CORRECTO" if r0.returncode == 0 else "INCOMPLETO", "fallos": [l.strip()[:160] for l in r0.stdout.splitlines() if l.strip().startswith("FALLO")],
                        "brief_logo": bool(glob.glob(os.path.join(os.path.dirname(est[-1]), "brief-logo.md"))), "prompts_logo": bool(glob.glob(os.path.join(os.path.dirname(est[-1]), "prompts-logo.md")))}
    lz = sorted(glob.glob(os.path.join(proy, "trabajo", "*", "lanzamiento")), key=os.path.getmtime)
    if not lz:
        return res
    d = lz[-1]
    res["lanzamiento"] = os.path.relpath(d, proy)
    res["piezas"] = sorted(os.path.basename(x) for x in glob.glob(os.path.join(d, "*")) if os.path.basename(x).startswith(("bento", "post-")))
    res["svg_a_mano"] = any(x.endswith(".svg") for x in res["piezas"]) and not any(x.endswith(".html") for x in res["piezas"])
    marca = os.path.join(proy, "marca.json")
    gusto = os.path.join(proy, "gusto.json")
    cmd = [sys.executable, os.path.join(RAIZ, "skills", "entrega", "tools", "verificar_entrega.py"), d] + (["--marca", marca] if os.path.exists(marca) else []) + (["--gusto", gusto] if os.path.exists(gusto) else [])
    r = sh(cmd, cwd=proy)
    res["puerta"] = "ABIERTA" if "PUERTA DE ENTREGA: ABIERTA" in r.stdout else "CERRADA"
    res["fallos"] = [l.strip()[:200] for l in r.stdout.splitlines() if l.strip().startswith("FALLO")]
    for n in ("post-1-que-es", "post-2-atributo"):
        h = os.path.join(d, n + ".html")
        if os.path.exists(h):
            t = open(h, encoding="utf-8").read()
            m = re.search(r'<meta name="arquetipo" content="([^"]+)"', t)
            res["arquetipos"][n] = m.group(1) if m else "propio(html)"
            c = sh([sys.executable, os.path.join(RAIZ, "skills", "gusto", "tools", "critico_render.py"), h, "--ancho", "1080", "--alto", "1440"] + (["--marca", marca] if os.path.exists(marca) else []), cwd=proy)
            res["tells"] += [f"{n}: " + l.split("anti-plantilla:")[1].strip()[:90] for l in c.stdout.splitlines() if "anti-plantilla:" in l]
    rev = os.path.join(d, "revision-gusto.md")
    if os.path.exists(rev):
        txt = open(rev, encoding="utf-8").read()
        res["revision_gusto"] = {"reglas": txt.count("\n- R"), "pendientes": txt.count("(pendiente)")}
    return res


def ejecutar(esc_ruta, a):
    esc = json.load(open(esc_ruta, encoding="utf-8"))
    base = os.path.join(a.salida, os.path.splitext(os.path.basename(esc_ruta))[0])
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
            sys.exit("No se pudo instalar el plugin en la configuración aislada: " + (r.stdout + r.stderr)[-300:])
    if a.gusto_zip:
        r = sh([sys.executable, "-I", os.path.join(RAIZ, "skills", "gusto", "tools", "importar_etiquetado.py"), os.path.abspath(a.gusto_zip), "--gusto", "gusto.json", "--referencias", "referencias"], cwd=proy)
        print("gusto:", (r.stdout.strip().splitlines() or ["?"])[0])
    gasto, sid, turnos, msg, log = 0.0, None, 0, esc["mensaje_inicial"], []
    t0 = time.time()
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
        log.append({"turno": turnos, "coste": round(float(d.get("total_cost_usd") or 0), 4), "agente": texto[:2500 if turnos <= 2 else 600], "agente_completo": texto, "preguntas": texto.count("?"),
                    "visual": sorted({m.group(0).lower() for m in re.finditer(r"#[0-9a-f]{6}\b|\blogo\w*|\bpaleta\b|\btipograf\w*|\bprompt\w*", texto, re.I)}), "respuesta": ""})
        print(f"  turno {turnos}: {gasto:.2f} USD")
        if glob.glob(os.path.join(proy, "trabajo", "*", "lanzamiento", ".puerta-ok")) or glob.glob(os.path.join(proy, "trabajo", "*", "prompts-logo.md")):
            break
        est_ = sorted(glob.glob(os.path.join(proy, "trabajo", "*", "estrategia.md")), key=os.path.getmtime)
        if esc.get("termina_con_brief") and est_ and sh([sys.executable, os.path.join(RAIZ, "skills", "estrategia", "tools", "verificar_brief.py"), est_[-1]]).returncode == 0:
            break
        por_turno = esc.get("por_turno") or []
        if turnos - 1 < len(por_turno) and not any(k in texto.lower() for k in ("tres vías", "vía a")) or (turnos == 1 and not por_turno):
            msg = por_turno[turnos - 1] if por_turno else esc["respuesta_por_defecto"]      # rondas de la persona, en orden
        else:
            msg = respuesta(esc, texto)
        log[-1]["respuesta"] = msg[:300]
    m = medir(proy)
    inf = {"escenario": esc["nombre"], "modelo": a.modelo, "turnos": turnos, "coste_usd": round(gasto, 3), "minutos": round((time.time() - t0) / 60, 1), "gusto": bool(a.gusto_zip), "medidas": m, "turnos_log": log}
    json.dump(inf, open(os.path.join(base, "informe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    b = m.get("brief") or {}
    L = [f"# {esc['nombre']}", "",
         "- Rondas: " + ", ".join(f"turno {t['turno']}: {t.get('preguntas', 0)} «?»" + (f" · visual: {', '.join(t['visual'])}" if t.get('visual') else "") for t in log),
         f"- Brief estratégico: {b.get('verificador', 'no creado')}" + ("".join(f"\n  - {x}" for x in b.get("fallos", []))) + f" · brief-logo.md: {'sí' if b.get('brief_logo') else 'no'} · prompts-logo.md: {'sí' if b.get('prompts_logo') else 'no'}", f"- Modelo: {a.modelo} · turnos: {turnos} · coste: {gasto:.2f} USD · {inf['minutos']} min · gusto entrenado: {'sí' if a.gusto_zip else 'no'}",
         f"- Puerta de entrega: **{m['puerta']}**" if m["puerta"] else "- No llegó a crear `lanzamiento/`", f"- Piezas: {', '.join(m['piezas']) or '—'}",
         f"- Arquetipos: {m['arquetipos'] or '—'}", f"- Piezas dibujadas a mano (solo SVG): {'sí' if m['svg_a_mano'] else 'no'}",
         f"- Huellas de plantilla: {len(m['tells'])}" + ("".join(f"\n  - {t}" for t in m["tells"])),
         f"- Revisión contra el gusto: {m['revision_gusto'] or 'no hecha'}"]
    if m["fallos"]:
        L.append("- Fallos de la puerta:" + "".join(f"\n  - {x}" for x in m["fallos"]))
    open(os.path.join(base, "informe.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))
    print("Informe:", os.path.join(base, "informe.md"))
    return inf


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("escenario", nargs="?")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--gusto-zip")
    ap.add_argument("--modelo", default="claude-haiku-5-5")
    ap.add_argument("--max-usd", type=float, default=2.5)
    ap.add_argument("--max-turnos", type=int, default=14)
    ap.add_argument("--salida", default=os.path.join(tempfile.gettempdir(), "brand-kit-e2e"))
    ap.add_argument("--credenciales", default="~/.claude/.credentials.json")
    a = ap.parse_args()
    esc = sorted(glob.glob(os.path.join(AQUI, "escenarios", "*.json"))) if a.todos else ([a.escenario] if a.escenario else [])
    if not esc:
        ap.error("indica un escenario o --todos")
    for e in esc:
        print(f"== {e}")
        ejecutar(e, a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
