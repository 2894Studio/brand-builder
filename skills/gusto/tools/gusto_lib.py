# Copyright (c) 2026 2894 Studio · MIT
"""Utilidades compartidas de la skill gusto: carga/guardado de gusto.json y ajuste de la proporción de tonos."""
import json
import os

TONOS = ("serio", "divertido", "tecnologico")
VERSION = 1


def nuevo(producto="SaaS"):
    return {"version": VERSION, "producto": producto,
            "tonos": {"serio": 50, "divertido": 20, "tecnologico": 30},
            "referencias": [], "elecciones_ab": [], "reglas": []}


def cargar(ruta):
    if not os.path.exists(ruta):
        return nuevo()
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def guardar(g, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalizar(tonos):
    """Devuelve la proporción como enteros que suman 100."""
    total = sum(tonos.get(t, 0) for t in TONOS) or 1
    out = {t: round(tonos.get(t, 0) * 100 / total) for t in TONOS}
    resto = 100 - sum(out.values())
    mayor = max(out, key=out.get)
    out[mayor] += resto
    return out


def mover(tonos, hacia, puntos=10):
    """La persona eligió una variante cuyo tono dominante es «hacia»: sube ese tono y baja los demás a prorrata.
    Es una heurística transparente, no aprendizaje: cada elección mueve la proporción un máximo de «puntos»."""
    t = dict(tonos)
    otros = [x for x in TONOS if x != hacia]
    base = sum(t[x] for x in otros) or 1
    quitar = min(puntos, base)
    for x in otros:
        t[x] = t[x] - quitar * t[x] / base
    t[hacia] = t[hacia] + quitar
    return normalizar(t)


def reglas_numeradas(g):
    """Todas las decisiones de las referencias «sí» (y las «no» como prohibiciones) con un id R1…Rn estable por orden."""
    out = []
    for r in g.get("referencias", []):
        for d in r.get("decisiones", []) or []:
            if d.get("regla"):
                out.append({"id": f"R{len(out) + 1}", "dimension": d.get("dimension"), "regla": d["regla"], "aplica_en": d.get("aplica_en", []),
                            "origen": r.get("nombre"), "prohibe": r.get("tipo") == "no"})
    return out


def validar(g):
    errores = []
    if g.get("version") != VERSION:
        errores.append(f"version debe ser {VERSION}")
    tonos = g.get("tonos", {})
    if set(tonos) != set(TONOS):
        errores.append(f"tonos debe tener exactamente {', '.join(TONOS)}")
    elif sum(tonos.values()) != 100:
        errores.append(f"los tonos deben sumar 100 (suman {sum(tonos.values())})")
    tipos = {"si": 0, "no": 0, "otra": 0}
    for i, r in enumerate(g.get("referencias", [])):
        if not r.get("nombre"):
            errores.append(f"referencias[{i}] sin nombre")
        if r.get("tipo") not in tipos:
            errores.append(f"referencias[{i}] «tipo» debe ser si, no u otra")
        else:
            tipos[r["tipo"]] += 1
        if r.get("tono") and r["tono"] not in TONOS:
            errores.append(f"referencias[{i}] tono «{r['tono']}» no válido")
        if r.get("confirmado") and not r.get("nota_usuario"):
            errores.append(f"referencias[{i}] marcada como confirmada pero sin nota_usuario (qué te gusta)")
    DIM = ("nombre", "simbolo", "forma", "color", "tipografia", "imagen", "composicion", "firma", "voz")
    APLICA = ("logo", "post", "bento", "web")
    distintivas = set()
    for i, r in enumerate(g.get("referencias", [])):
        for j, d in enumerate(r.get("decisiones", []) or []):
            if d.get("dimension") not in DIM:
                errores.append(f"referencias[{i}].decisiones[{j}] «dimension» debe ser una de {', '.join(DIM)}")
            if not (d.get("regla") or "").strip():
                errores.append(f"referencias[{i}].decisiones[{j}] sin «regla»")
            for ap_ in d.get("aplica_en", []) or []:
                if ap_ not in APLICA:
                    errores.append(f"referencias[{i}].decisiones[{j}] «aplica_en» {ap_} no válido ({', '.join(APLICA)})")
            if r.get("tipo") == "si" and d.get("dimension") in ("nombre", "simbolo", "tipografia", "imagen", "composicion", "firma"):
                distintivas.add(d["dimension"])
    avisos = []
    refs_si = [r for r in g.get("referencias", []) if r.get("tipo") == "si"]
    if refs_si:
        sin_dec = [r.get("nombre") for r in refs_si if not r.get("decisiones")]
        if sin_dec:
            avisos.append("referencias «sí» sin decisiones transferables (qué copio y qué no, por dimensión): " + ", ".join(sin_dec) + ". Sin ellas la referencia solo elige un tono y las piezas salen genéricas")
        elif len(distintivas) < 2:
            avisos.append("las decisiones solo tocan forma o color (lo genérico): añade al menos 2 dimensiones de las distintivas (nombre, símbolo, tipografía, imagen, composición, firma)")
    if g.get("referencias"):
        if tipos["no"] == 0:
            avisos.append("ninguna referencia «no» (lo que NO quieres parecer): educa menos el gusto")
        sin_nota = [r["nombre"] for r in g["referencias"] if not r.get("nota_usuario")]
        if sin_nota:
            avisos.append("sin nota de la persona (qué le gusta): " + ", ".join(sin_nota))
        if len(g["referencias"]) < 6:
            avisos.append(f"hay {len(g['referencias'])} referencias; el método pide de 6 a 8")
    return errores, avisos
