#!/usr/bin/env python3
# Copyright (c) 2026 2894 Studio · MIT
"""Genera el bento de la marca (tablero 1920×1080 con logo, símbolo, color, tipografía, voz, fotografía y proporción) en HTML.

Uso:  python3 bento.py marca.json --salida lanzamiento/bento.html [opciones]
  --gusto gusto.json         usa la proporción de tonos; sin él, enseña el territorio
  --lema "frase"             la frase de la tarjeta «Voz» (por defecto, la categoría de marca.json)
  --prueba "Título|Valor"    la tarjeta de prueba, p. ej. "Equipo propuesto|4 perfiles" (dato real o de ejemplo)
  --foto-equipo ruta         fotografía de varias personas; sin ella, marcador visible «Foto real»
  --foto-persona ruta        retrato; sin él, marcador visible
  --fotos DIR                carpeta lanzamiento/fotos (salida de preparar_fotos.py): coge equipo* y retrato*
  --declarar-ia              escribe «Imagen generada con IA» sobre las fotos de origen ia (por defecto NO se escribe)
  --persona "Nombre|Rol"     rótulo del retrato (por defecto, marcador «Nombre y apellido»)
  --datos "Etiqueta|Valor;..."  sin foto de equipo: la tarjeta «Fotografía» pasa a «Datos» con hasta 3 cifras reales (p. ej. "Precio|10 €/mes;Grupos|5 alumnos")
  --puntos "a;b;c"           sin retrato: la tarjeta «Personas» pasa a «Incluye» con hasta 4 puntos reales del producto
  --variante generica|educativa|producto   distribución del tablero según la marca (por defecto, generica)
  --ruta "Paso 1;Paso 2;…"   variante educativa: el recorrido o temario (3 a 5 pasos reales); ocupa la tarjeta más grande
  --plano                    la tarjeta del logo va en color liso (por defecto lleva degradado con luz)
Lo que no se aporta queda como **marcador visible**, nunca inventado. Luego se revisa con gusto/tools/critico_render.py.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_lanzamiento as L  # noqa: E402


def mosaico_logo(m, base, c, f, degradado):
    lg = L.logos(m, base)
    nombre = L.esc(m.get("nombre", "Marca"))
    luz = L.aclarar(c["primario"], 0.35)
    bg = f"radial-gradient(700px 500px at 20% 92%,{luz} 0%,rgba(255,255,255,0) 60%),var(--campo)" if degradado else c["primario"]
    sobre = L.legible(c["primario"])
    if "invertida" in lg:
        img = f'<img src="{L.data_uri(lg["invertida"])}" style="width:68%;max-height:64%">'
    elif "principal" in lg and L.luminancia(c["primario"]) > 0.5:
        img = f'<img src="{L.data_uri(lg["principal"])}" style="width:68%;max-height:64%">'
    else:
        img = f'<div style="font-family:var(--f-titulos);font-weight:700;font-size:110px;letter-spacing:-.04em;color:{sobre}">{nombre}</div>'
    return f'<div class="t L" style="background:{bg};color:{sobre}"><span class="pill">Logo</span>{img}</div>'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("marca")
    ap.add_argument("--salida", default="bento.html")
    ap.add_argument("--gusto")
    ap.add_argument("--lema")
    ap.add_argument("--prueba")
    ap.add_argument("--foto-equipo")
    ap.add_argument("--foto-persona")
    ap.add_argument("--fotos")
    ap.add_argument("--declarar-ia", action="store_true")
    ap.add_argument("--persona")
    ap.add_argument("--plano", action="store_true")
    ap.add_argument("--variante", choices=["generica", "educativa", "producto"], default="generica")
    ap.add_argument("--ruta")
    ap.add_argument("--datos")
    ap.add_argument("--puntos")
    a = ap.parse_args()

    m = L.cargar_marca(a.marca)
    base = os.path.dirname(os.path.abspath(a.marca))
    c, f = L.colores(m), L.fuentes(m)
    nombre = m.get("nombre", "Marca")
    lg = L.logos(m, base)
    lema = a.lema or m.get("categoria", "")
    prueba_t, prueba_v = (a.prueba.split("|", 1) + [""])[:2] if a.prueba else (m.get("categoria", "Qué es"), "")
    persona_n, persona_r = (a.persona.split("|", 1) + ["Rol · Ciudad"])[:2] if a.persona else ("Nombre y apellido", "Rol · Ciudad")

    # símbolo
    if "simbolo" in lg:
        simbolo = f'<img src="{L.data_uri(lg["simbolo"])}" style="width:150px">'
    else:
        simbolo = f'<div style="width:150px;height:150px;border-radius:34px;background:{c["primario"]};color:{L.legible(c["primario"])};display:grid;place-items:center;font:700 84px var(--f-titulos)">{L.esc(nombre[:1].upper())}</div>'

    elegidas = L.elegir_fotos(a.fotos) if a.fotos else {}
    if "equipo" in elegidas and not a.foto_equipo:
        a.foto_equipo = elegidas["equipo"]["ruta_4x3"]
    if "retrato" in elegidas and not a.foto_persona:
        a.foto_persona = elegidas["retrato"]["ruta_3x4"]
    pie_ia = {k: (v.get("pie") if a.declarar_ia else None) for k, v in elegidas.items()}

    def foto(ruta, pos, ia=False, alto_nota=14):
        if ruta and os.path.exists(ruta):
            nota = f'<div class="nota-ia" style="bottom:{alto_nota}px">Imagen generada con IA</div>' if ia else ""
            return f'<img src="{L.data_uri(ruta)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos}">{nota}'
        return '<div class="ph">Foto real<br>(sustituir por una propia)</div>'

    # alternativas sin foto: datos y puntos reales (nunca inventados) en lugar del marcador
    tarjeta_f = f'<span class="pill">Fotografía</span>{foto(a.foto_equipo, "50% 40%", bool(pie_ia.get("equipo")))}'
    if not (a.foto_equipo and os.path.exists(a.foto_equipo)) and a.datos:
        fil = [d.split("|", 1) + [""] for d in a.datos.split(";") if d.strip()][:2 if a.variante == "educativa" else 3]
        celdas = "".join(f'<div><small>{L.esc(x[0].strip())}</small><b>{L.esc(x[1].strip())}</b></div>' for x in fil)
        tarjeta_f = f'<span class="pill">Datos</span><div class="dat">{celdas}</div>'
        a.foto_equipo = "datos"
    tarjeta_p = f'<span class="pill">Personas</span>{foto(a.foto_persona, "50% 14%", bool(pie_ia.get("retrato")), 96)}<div class="rot"><b>{L.esc(persona_n)}</b>{L.esc(persona_r)}</div>'
    if not (a.foto_persona and os.path.exists(a.foto_persona)) and a.puntos:
        pts = [x.strip() for x in a.puntos.split(";") if x.strip()][:4]
        lis = "".join(f"<li>{L.esc(x)}</li>" for x in pts)
        tarjeta_p = f'<span class="pill">Incluye</span><ul class="pts">{lis}</ul>'
        a.foto_persona = "puntos"

    # color
    sw = []
    for clave, rol in (("primario", "Primario"), ("profundo", "Profundo"), ("acento", "Acento"), ("neutro", "Neutro"), ("fondo", "Fondo")):
        h = c[clave]
        borde = "border:2px solid #D5D9E0;" if L.luminancia(h) > 0.85 else ""
        sw.append(f'<div style="background:{h};color:{L.legible(h)};{borde}">{L.esc(c["nombres"][clave])}<br>{h}</div>')

    # proporción o territorio
    if a.gusto and os.path.exists(a.gusto):
        import json
        t = json.load(open(a.gusto, encoding="utf-8")).get("tonos", {})
        nom = {"serio": "Serio", "divertido": "Divertido", "tecnologico": "Tecnológico"}
        filas = "".join(f'<div><div class="n"><span>{nom.get(k, k)}</span><span>{v}</span></div><div class="bar"><i style="width:{v}%"></i></div></div>'
                        for k, v in sorted(t.items(), key=lambda kv: -kv[1]))
        mosaico_m = f'<div class="t M campo"><span class="pill">Proporción</span><div class="pr">{filas}</div></div>'
    else:
        terr = m.get("brandKit", {}).get("territorio", "")
        nombres_t = {"artesanal": "Artesanal", "editorial": "Editorial", "tecnologico": "Tecnológico", "natural": "Natural", "cercano": "Cercano"}
        mosaico_m = f'<div class="t M campo"><span class="pill">Territorio</span><div class="terr">{L.esc(nombres_t.get(terr, terr.capitalize()) or "—")}</div></div>'

    areas = {
        "generica": '"L L L L L F F F C C I I" "L L L L L F F F C C I I" "L L L L L F F F V V V V" "K K K K K T T T P P M M" "K K K K K T T T P P M M" "K K K K K T T T P P M M"',
        "educativa": '"L L L L L R R R R I I I" "L L L L L R R R R C C C" "L L L L L R R R R C C C" "K K K K T T T V V V V V" "K K K K T T T F F F P P" "K K K K T T T M M M P P"',
        "producto": '"F F F F F F L L L L I I" "F F F F F F L L L L C C" "F F F F F F L L L L C C" "P P P P V V V V V V V V" "P P P P K K K K K T T T" "P P P P M M M M M T T T"',
    }[a.variante]
    css_var = {
        "generica": "",
        "educativa": ".dat{flex-direction:row;gap:20px;top:72px;bottom:18px;align-items:flex-end;justify-content:flex-start}.dat div{flex:1}.dat b{font-size:36px}.dat small{font-size:19px;margin-bottom:4px}"
                     ".sw div{font-size:19px;padding:10px;word-break:break-word}.V{padding:20px 30px}.V h2{font-size:28px;line-height:1.15}.terr{font-size:30px}.pr{gap:12px;font-size:19px}.M{padding:20px 30px}.M .pill{display:none}.pr .n{margin-bottom:4px}.bar{height:10px}",
        "producto": ".sw div{font-size:19px;padding:10px;word-break:break-word}.I img,.I div{max-width:90px;max-height:90px}.T .aa{font-size:110px;margin-bottom:12px}.T{padding:26px}.V h2{font-size:34px}.M{padding:20px 30px}.pr{gap:12px;font-size:19px}.pr .n{margin-bottom:4px}.bar{height:10px}.M .pill{display:none}.terr{font-size:34px}",
    }[a.variante]
    if a.variante == "producto" and not (a.foto_equipo and os.path.exists(a.foto_equipo)):
        sys.exit("--variante producto necesita --foto-equipo (o --fotos con equipo*): la fotografía es la tarjeta protagonista. Sin foto, usa la variante generica o educativa.")
    tarjeta_r = ""
    if a.variante == "educativa":
        pasos = [x.strip() for x in (a.ruta or "").split(";") if x.strip()][:5]
        if len(pasos) < 3:
            sys.exit("--variante educativa necesita --ruta con 3 a 5 pasos reales del recorrido (p. ej. \"Fundamentos;Frontend;Backend;Proyecto final\")")
        lis = "".join(f'<li><span>{i + 1:02d}</span>{L.esc(x)}</li>' for i, x in enumerate(pasos))
        tarjeta_r = f'<div class="t R"><span class="pill">Recorrido</span><ol class="ruta">{lis}</ol></div>'

    pesos = "/".join(str(p) for p in f["pesos_texto"])
    css = L.css_variables(m) + """
.p{width:1920px;height:1080px;background:#E4E8F0;padding:36px;display:grid;gap:16px;
grid-template-columns:repeat(12,minmax(0,1fr));grid-template-rows:minmax(0,1fr) minmax(0,1fr) minmax(0,1.35fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1fr);
grid-template-areas:AREAS}
.t{border-radius:30px;position:relative;overflow:hidden;padding:34px}
.pill{position:absolute;left:24px;top:22px;font-size:19px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;background:rgba(255,255,255,.88);color:#12141A;padding:6px 16px;border-radius:99px;z-index:3}
.L{grid-area:L;display:flex;align-items:center;justify-content:center}.F{grid-area:F;background:var(--neutro)}
.ph{position:absolute;inset:60px 24px 24px;border:2px dashed var(--profundo);border-radius:20px;display:grid;place-items:center;text-align:center;color:var(--profundo);font-size:24px;line-height:1.4}
.C{grid-area:C;display:flex;flex-direction:column;justify-content:flex-end}.C small{font-size:22px}.C b{font-size:54px;font-weight:600;letter-spacing:-.03em;line-height:1.05}
.I{grid-area:I;background:#fff;display:flex;align-items:center;justify-content:center}
.V{grid-area:V;background:#fff;display:flex;flex-direction:column;justify-content:flex-end;padding-bottom:26px}.V h2{margin:0;font:400 40px/1.12 var(--f-titulos);letter-spacing:-.03em}
.K{grid-area:K;background:#fff}.sw{position:absolute;left:24px;right:24px;top:72px;bottom:24px;display:grid;grid-template-columns:minmax(0,1.6fr) repeat(4,minmax(0,1fr));gap:10px}
.sw div{border-radius:20px;padding:14px;font-size:19px;font-weight:600;display:flex;flex-direction:column;justify-content:flex-end;line-height:1.3;overflow:hidden}
.T{grid-area:T;background:var(--profundo);color:var(--sobre-profundo);display:flex;flex-direction:column;justify-content:flex-end}
.T .aa{font:400 190px/.8 var(--f-titulos);letter-spacing:-.05em;margin-bottom:34px}.T p{margin:0;font-size:22px;line-height:1.4;opacity:.92}
.P{grid-area:P;background:var(--neutro)}.rot{position:absolute;left:14px;right:14px;bottom:14px;border-radius:20px;background:rgba(10,20,60,.72);padding:10px 14px;color:#fff;font-size:20px;line-height:1.25;z-index:2}.rot b{display:block;font-size:23px;font-weight:600}
.M{grid-area:M;display:flex;flex-direction:column;justify-content:flex-end}.pr{display:grid;gap:22px;font-size:21px;font-weight:600}.pr .n{display:flex;justify-content:space-between;margin-bottom:8px}
.bar{height:14px;border-radius:99px;background:rgba(255,255,255,.28);overflow:hidden}.bar i{display:block;height:100%;background:#fff}.terr{font:600 44px/1.1 var(--f-titulos);letter-spacing:-.02em}
.nota-ia{position:absolute;left:14px;bottom:14px;background:rgba(10,20,60,.72);color:#fff;font-size:19px;padding:6px 14px;border-radius:99px;z-index:2}
.dat{position:absolute;left:30px;right:30px;top:76px;bottom:26px;display:flex;flex-direction:column;justify-content:space-around;color:var(--profundo)}
.dat small{display:block;font-size:20px;line-height:1.3;margin-bottom:8px;font-weight:600;opacity:.8}.dat b{font:600 54px/1.05 var(--f-titulos);letter-spacing:-.03em}
.pts{list-style:none;margin:0;position:absolute;left:24px;right:24px;top:74px;bottom:22px;display:flex;flex-direction:column;justify-content:space-around;padding:0;font-size:21px;font-weight:600;line-height:1.25;color:var(--profundo)}
.pts li{padding-left:34px;position:relative}.pts li:before{content:"";position:absolute;left:0;top:.3em;width:18px;height:18px;border-radius:50%;background:var(--primario)}
.R{grid-area:R;background:#fff}.ruta{list-style:none;margin:0;padding:0;position:absolute;left:34px;right:34px;top:84px;bottom:30px;display:flex;flex-direction:column;justify-content:space-between;color:var(--profundo)}
.ruta li{font:600 38px/1.15 var(--f-titulos);letter-spacing:-.02em;border-top:2px solid var(--neutro);padding-top:16px;display:flex;gap:22px;align-items:baseline}.ruta li span{font:600 22px var(--f-texto);color:var(--primario);min-width:42px}
.campo{background:linear-gradient(160deg,var(--primario),var(--profundo));color:var(--sobre-primario)}
:root{--campo:linear-gradient(160deg,var(--primario),var(--profundo))}
"""
    doc = f"""<!doctype html><html lang="es"><meta charset="utf-8"><title>{L.esc(nombre)} · bento de marca</title>
{L.enlace_google_fonts(m)}<style>{L.COMPONENTES_CSS}{css.replace("AREAS", areas)}{css_var}</style><div class="p">
{mosaico_logo(m, base, c, f, not a.plano)}
<div class="t F">{tarjeta_f}</div>
<div class="t C campo"><span class="pill">Prueba</span><small>{L.esc(prueba_t)}</small><b>{L.esc(prueba_v)}</b></div>
{tarjeta_r}<div class="t I"><span class="pill">Símbolo</span>{simbolo}</div>
<div class="t V"><span class="pill">Voz</span><h2>{L.esc(lema)}</h2></div>
<div class="t K"><span class="pill">Color</span><div class="sw">{''.join(sw)}</div></div>
<div class="t T"><span class="pill">Tipografía</span><div class="aa">Aa</div><p>{L.esc(f["titulos"])}, titulares<br>{L.esc(f["texto"])} {pesos}, texto</p></div>
<div class="t P">{tarjeta_p}</div>
{mosaico_m}
</div></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    with open(a.salida, "w", encoding="utf-8") as fh:
        fh.write(doc)
    avisos = []
    if "invertida" not in lg and L.luminancia(c["primario"]) <= 0.5:
        avisos.append("sin logo «invertida»: la tarjeta de logo muestra el nombre en texto")
    if "simbolo" not in lg:
        avisos.append("sin logo «simbolo»: se usa la inicial")
    if not a.foto_equipo:
        avisos.append("sin foto de equipo: marcador visible (usa --datos \"Etiqueta|Valor;...\" con cifras reales para sustituirlo)")
    if not a.foto_persona:
        avisos.append("sin retrato: marcador visible (usa --puntos \"a;b;c\" con lo que incluye el producto para sustituirlo)")
    print(f"ok {a.salida}")
    for x in avisos:
        print("  aviso", x)
    print("Siguiente: python3 skills/gusto/tools/critico_render.py", a.salida, "--ancho 1920 --alto 1080 --marca", a.marca)


if __name__ == "__main__":
    main()
