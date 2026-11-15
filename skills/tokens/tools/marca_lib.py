#!/usr/bin/env python3
"""Núcleo común de brand-kit-builder: lectura y validación de marca.json,
contraste WCAG, léxico prohibido y firma gráfica por territorio.

Solo librería estándar. Lo importan tokens/, laminas/ e identidad/.
El contrato de marca.json es el de creative-architect (Hainrixz) más extensiones
opcionales (tipografia, publico, competidores, brandKit) que sus oficios ignoran.
"""
import json
import re
import sys
import unicodedata

ROLES = ("primario", "fondo", "acento", "texto")          # roles del contrato
ROLES_OBLIGATORIOS = ("primario", "fondo", "texto")
TERRITORIOS = ("artesanal", "editorial", "tecnologico", "natural", "cercano")

# Firma gráfica por territorio (ver laminas/references/sistema-laminas.md, sección 5)
FIRMAS = {
    "artesanal":    {"filete": "trazo",   "numeracion": "romana",     "radio": 0,  "recorte": "cuadrado"},
    "editorial":    {"filete": "linea",   "numeracion": "guiones",    "radio": 0,  "recorte": "alto"},
    "tecnologico":  {"filete": "barra",   "numeracion": "mono",       "radio": 4,  "recorte": "esquina4"},
    "natural":      {"filete": "onda",    "numeracion": "circulo",    "radio": 24, "recorte": "esquina24"},
    "cercano":      {"filete": "bloque",  "numeracion": "margen",     "radio": 16, "recorte": "redondo"},
}

# Léxico prohibido (identidad/references/lexico-prohibido.md)
LEXICO = [
    "sinergia", "ecosistema", "tapiz", "universo", "viaje", "propuesta de valor",
    "solución integral", "solucion integral", "apuesta",
    "elevar", "potenciar", "revolucionar", "transformar", "empoderar", "impulsar",
    "innovador", "innovadora", "disruptivo", "disruptiva", "único", "única", "excepcional",
    "premium", "a medida", "de vanguardia",
]
ESTRUCTURAS = [
    (r"\bno es solo\b.{0,60}\bes\b", "«No es solo X, es Y»"),
    (r"\ben un mundo donde\b", "«En un mundo donde…»"),
    (r"\bdonde\b.{1,40}\bse encuentra[n]? con\b", "«Donde X se encuentra con Y»"),
]


def _norm(s):
    return unicodedata.normalize("NFC", s).lower()


def hallar_lexico(texto):
    """Devuelve la lista de términos o estructuras prohibidas presentes en `texto`."""
    t = _norm(texto)
    hits = [w for w in LEXICO if re.search(r"(?<!\w)%s(?!\w)" % re.escape(w), t)]
    hits += [nombre for pat, nombre in ESTRUCTURAS if re.search(pat, t)]
    return sorted(set(hits))


def _strings(obj, ruta=""):
    if isinstance(obj, str):
        yield ruta, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _strings(v, f"{ruta}.{k}" if ruta else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _strings(v, f"{ruta}[{i}]")


# ---------- color ----------
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def luminancia(hx):
    c = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def veredicto(ratio):
    if ratio >= 4.5:
        return "texto normal"
    if ratio >= 3:
        return "solo texto grande o UI"
    return "no para texto"


def mezclar(a, b, t):
    """Mezcla a→b en proporción t (0..1) y devuelve hex."""
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * t) for x, y in zip(ca, cb))


def mejor_sobre(fondo, candidatos):
    """El candidato con más contraste sobre `fondo`."""
    return max(candidatos, key=lambda c: contraste(c, fondo))


# ---------- marca.json ----------
def cargar(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def paleta(marca):
    """{'primario': '#..', 'fondo': .., 'texto': .., 'acento': .., 'neutro': ..}
    El neutro no existe en el contrato: vive en brandKit.neutro."""
    p = {}
    for c in marca.get("visual", {}).get("colores", []):
        if isinstance(c, dict) and c.get("rol") in ROLES:
            p[c["rol"]] = c["hex"].upper()
    n = marca.get("brandKit", {}).get("neutro")
    if isinstance(n, dict) and isinstance(n.get("hex"), str):
        p["neutro"] = n["hex"].upper()
    return p


def nombres_color(marca):
    n = {c["rol"]: c.get("nombre", c["rol"]) for c in marca.get("visual", {}).get("colores", [])
         if isinstance(c, dict) and "rol" in c}
    nn = marca.get("brandKit", {}).get("neutro", {})
    if isinstance(nn, dict) and "nombre" in nn:
        n["neutro"] = nn["nombre"]
    return n


def territorio(marca):
    return marca.get("brandKit", {}).get("territorio", "editorial")


def validar(marca):
    """Devuelve (errores, avisos). Un error impide generar; un aviso se muestra."""
    e, a = [], []
    if not isinstance(marca, dict):
        return ["marca.json debe ser un objeto JSON"], a

    for k in ("nombre", "categoria", "tono", "idioma"):
        if not isinstance(marca.get(k), str) or not marca[k].strip():
            e.append(f"falta «{k}» (texto no vacío)")
    if isinstance(marca.get("idioma"), str) and not re.match(r"^[a-z]{2}(-[A-Z]{2})?$", marca["idioma"]):
        e.append("«idioma» debe tener la forma es o es-ES")

    pp = marca.get("palabrasProhibidas")
    if not isinstance(pp, list) or not all(isinstance(x, str) for x in pp):
        e.append("«palabrasProhibidas» debe ser una lista de textos")
    elif not pp:
        a.append("«palabrasProhibidas» está vacía: es la lista más operativa de la voz")

    vis = marca.get("visual")
    if not isinstance(vis, dict):
        e.append("falta el objeto «visual»")
        vis = {}
    if not isinstance(vis.get("estilo"), str) or len(vis.get("estilo", "").strip()) < 20:
        e.append("«visual.estilo» debe describir la técnica (luz, grano, paleta, encuadre), mínimo 20 caracteres")

    cols = vis.get("colores")
    roles_vistos = []
    if not isinstance(cols, list) or not cols:
        e.append("«visual.colores» debe ser una lista con al menos primario, fondo y texto")
        cols = []
    for i, c in enumerate(cols):
        if not isinstance(c, dict):
            e.append(f"visual.colores[{i}] debe ser un objeto")
            continue
        if not c.get("nombre"):
            e.append(f"visual.colores[{i}] sin «nombre»")
        if not isinstance(c.get("hex"), str) or not HEX.match(c["hex"]):
            e.append(f"visual.colores[{i}].hex «{c.get('hex')}» no es #RRGGBB")
        if c.get("rol") not in ROLES:
            e.append(f"visual.colores[{i}].rol «{c.get('rol')}» no es uno de {', '.join(ROLES)}")
        else:
            roles_vistos.append(c["rol"])
    for r in ROLES_OBLIGATORIOS:
        if r not in roles_vistos:
            e.append(f"falta un color con rol «{r}»")
    for r in set(roles_vistos):
        if roles_vistos.count(r) > 1:
            e.append(f"el rol «{r}» aparece {roles_vistos.count(r)} veces (uno por rol)")
    if "acento" not in roles_vistos:
        a.append("no hay color de acento: el kit funcionará, pero sin un 10 % que dirija la mirada")

    bk = marca.get("brandKit")
    if bk is not None:
        if not isinstance(bk, dict):
            e.append("«brandKit» debe ser un objeto")
        else:
            if "territorio" in bk and bk["territorio"] not in TERRITORIOS:
                e.append(f"brandKit.territorio «{bk['territorio']}» no es uno de {', '.join(TERRITORIOS)}")
            n = bk.get("neutro")
            if n is not None and (not isinstance(n, dict) or not HEX.match(str(n.get("hex", "")))):
                e.append("brandKit.neutro debe ser {nombre, hex #RRGGBB}")
    else:
        a.append("sin «brandKit.territorio» se usa «editorial» como firma gráfica")

    tp = marca.get("tipografia")
    if tp is not None:
        if not isinstance(tp, dict):
            e.append("«tipografia» debe ser un objeto con titulos y texto")
        else:
            for k in ("titulos", "texto"):
                if not isinstance(tp.get(k), dict) or not tp[k].get("familia"):
                    e.append(f"tipografia.{k}.familia es obligatoria")
            extra = [k for k in tp if k not in ("titulos", "texto")]
            if extra:
                e.append(f"máximo 2 tipografías (titulos y texto); sobra: {', '.join(extra)}")

    # contraste: lo que se declara texto tiene que poder leerse
    p = paleta(marca)
    if "texto" in p and "fondo" in p and HEX.match(p["texto"]) and HEX.match(p["fondo"]):
        r = contraste(p["texto"], p["fondo"])
        if r < 4.5:
            e.append(f"el texto ({p['texto']}) sobre el fondo ({p['fondo']}) da {r:.2f}:1; mínimo 4,5:1")
        if "acento" in p and HEX.match(p["acento"]):
            ra = contraste(p["acento"], p["fondo"])
            if ra < 4.5:
                a.append(f"el acento {p['acento']} sobre el fondo da {ra:.2f}:1 ({veredicto(ra)}): "
                         "úsalo en filetes, iconos grandes o fondos, no en texto pequeño")

    # léxico prohibido en lo que escribe la marca (no en palabrasProhibidas, que las lista a propósito)
    for ruta, s in _strings({k: v for k, v in marca.items() if k != "palabrasProhibidas"}):
        hits = hallar_lexico(s)
        if hits:
            a.append(f"léxico prohibido en {ruta}: {', '.join(hits)}")
    return e, a


def informe(ruta, marca):
    e, a = validar(marca)
    for x in e:
        print(f"  ERROR  {x}", file=sys.stderr)
    for x in a:
        print(f"  aviso  {x}", file=sys.stderr)
    return not e


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "marca"
