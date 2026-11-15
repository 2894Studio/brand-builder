#!/usr/bin/env python3
"""Contraste WCAG entre colores, con el veredicto que importa en una marca.

Uso:
  python3 contraste.py "#00C27A" "#F3F4F6"          un par (primero el color del texto, luego el fondo)
  python3 contraste.py --base "#F3F4F6" "#2F4BD8" "#00C27A" "#14181F"   varios colores sobre una base
"""
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "..", "..", "tokens", "tools")))
import marca_lib as m  # noqa: E402


def main(a):
    if len(a) == 2 and a[0] != "--base":
        pares = [(a[0], a[1])]
    elif len(a) >= 3 and a[0] == "--base":
        pares = [(c, a[1]) for c in a[2:]]
    else:
        print(__doc__)
        return 2
    for fg, bg in pares:
        if not (m.HEX.match(fg) and m.HEX.match(bg)):
            print(f"hex no válido: {fg} / {bg} (usa #RRGGBB)")
            return 2
        r = m.contraste(fg, bg)
        print(f"{fg.upper()} sobre {bg.upper()}  {r:5.2f}:1  {m.veredicto(r)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
