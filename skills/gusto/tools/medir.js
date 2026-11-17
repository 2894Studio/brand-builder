// Mide una pieza HTML ya renderizada. Se ejecuta dentro de la página (page.evaluate) y devuelve datos, sin juzgar.
(opts) => {
  const W = innerWidth, H = innerHeight;
  const out = {W, H, textos: [], colores: [], fuentes: [], lineas: []};
  const parseColor = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const fondoEfectivo = (el) => {
    let capas = [];
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return {opaco: false, motivo: 'imagen o degradado'};
      const c = parseColor(cs.backgroundColor);
      if (c && c.a > 0) { capas.push(c); if (c.a >= 0.99) break; }
    }
    if (!capas.length) return {r: 255, g: 255, b: 255, a: 1, opaco: true};
    let base = capas[capas.length - 1].a >= 0.99 ? capas.pop() : {r: 255, g: 255, b: 255, a: 1};
    while (capas.length) { const t = capas.pop(); base = {r: t.r * t.a + base.r * (1 - t.a), g: t.g * t.a + base.g * (1 - t.a), b: t.b * t.a + base.b * (1 - t.a), a: 1}; }
    return {...base, opaco: true};
  };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const hoja = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const vistos = new Set();
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const t = n.textContent.replace(/\s+/g, ' ').trim();
    if (!t) continue;
    const el = n.parentElement; if (!el || vistos.has(el)) continue;
    if (['SCRIPT', 'STYLE', 'TITLE'].includes(el.tagName)) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    vistos.add(el);
    const range = document.createRange(); range.selectNodeContents(el);
    const rr = range.getBoundingClientRect();
    if (rr.width === 0 || rr.height === 0) continue;
    // La caja del Range incluye el espacio de la fuente aunque el line-height sea menor (titulares gigantes con
    // line-height < 1). Para elementos de bloque se recorta a la caja del propio elemento: así no hay falsos solapes.
    // ¿Algún contenedor con overflow oculto corta el texto? (se sale de la caja del contenedor)
    let recorte = null;
    for (let a = el.parentElement; a && a !== document.body && a !== document.documentElement; a = a.parentElement) {
      const o = getComputedStyle(a);
      if (!/(hidden|clip|auto|scroll)/.test(o.overflow + o.overflowX + o.overflowY)) continue;
      const ar = a.getBoundingClientRect();
      if (ar.width >= innerWidth - 1 && ar.height >= innerHeight - 1) continue; // el propio lienzo: ya se comprueba aparte
      if (rr.bottom > ar.bottom + 2 || rr.right > ar.right + 2 || rr.top < ar.top - 2 || rr.left < ar.left - 2) { recorte = (a.className && String(a.className).split(' ')[0]) || a.tagName.toLowerCase(); break; }
    }
    let r = {left: rr.left, top: rr.top, right: rr.right, bottom: rr.bottom, width: rr.width, height: rr.height};
    if (cs.display !== 'inline') { const e = el.getBoundingClientRect(); if (e.height > 0) { r.top = Math.max(rr.top, e.top); r.bottom = Math.min(rr.bottom, e.bottom); r.height = Math.max(r.bottom - r.top, 1); } }
    const bleed = !!el.closest('[data-bleed]'); const deco = !!el.closest('[data-decorativo]');
    const fg = parseColor(cs.color), bg = fondoEfectivo(el);
    let contraste = null;
    if (fg && bg.opaco) { const f = fg.a < 1 ? {r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a)} : fg; contraste = Math.round(ratio(f, bg) * 100) / 100; }
    // lo que hay DEBAJO del texto: una forma opaca (círculo, bloque) que no es su ancestro también es su fondo; se mide el peor punto
    if (fg && !el.closest('[data-decorativo]')) {
      try {
        const rg2 = document.createRange(); rg2.selectNodeContents(el);
        const cajas = Array.from(rg2.getClientRects()).filter(q => q.width > 2 && q.height > 2).slice(0, 8);
        for (const q of cajas) for (const fx of [0.08, 0.5, 0.92]) {
          const px = q.left + q.width * fx, py = q.top + q.height * 0.5;
          if (px < 0 || py < 0 || px >= W || py >= H) continue;
          const pila = document.elementsFromPoint(px, py);
          let idx = -1; pila.forEach((s, i) => { if (el.contains(s)) idx = i; });
          for (let k = idx + 1; k < pila.length; k++) {
            const sc = getComputedStyle(pila[k]);
            const esAncestro = pila[k].contains(el);          // el fondo de los ancestros ya está medido arriba: solo cuentan las formas que NO lo son
            if (sc.backgroundImage && sc.backgroundImage !== 'none') break;
            const c = parseColor(sc.backgroundColor);
            if (esAncestro) { if (c && c.a >= 0.99) break; continue; }
            if (c && c.a >= 0.99) { const f = fg.a < 1 ? {r: fg.r * fg.a + c.r * (1 - fg.a), g: fg.g * fg.a + c.g * (1 - fg.a), b: fg.b * fg.a + c.b * (1 - fg.a)} : fg; const rt = Math.round(ratio(f, c) * 100) / 100; if (contraste === null || rt < contraste) contraste = rt; break; }
          }
        }
      } catch (e) { /* sin medición extra */ }
    }
    const size = parseFloat(cs.fontSize), peso = parseInt(cs.fontWeight) || 400;
    // líneas por palabra
    const partidas = []; const palabras = []; const rg = document.createRange();
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let tn = tw.nextNode(); tn; tn = tw.nextNode()) {
      const re = /\S+/g; let m;
      while ((m = re.exec(tn.textContent))) { rg.setStart(tn, m.index); rg.setEnd(tn, m.index + m[0].length); const q = rg.getBoundingClientRect(); const qr = Array.from(rg.getClientRects()); if (m[0].length >= 3 && !/[-\/–—]/.test(m[0]) && new Set(qr.map(z => Math.round(z.top / (size * 0.5)))).size > 1) partidas.push(m[0]); if (q.width) palabras.push({w: m[0], top: Math.round(q.top), left: q.left, right: q.right}); }
    }
    const lineas = []; palabras.forEach(p => { const l = lineas.find(l => Math.abs(l.top - p.top) < size * 0.5); l ? l.ps.push(p) : lineas.push({top: p.top, ps: [p]}); });
    out.textos.push({texto: t.slice(0, 60), tag: el.tagName.toLowerCase(), x: r.left, y: r.top, w: r.width, h: r.height, size, peso, contraste, fondoNoMedible: !bg.opaco ? bg.motivo : null, bleed, deco, recorte, partidas,
      fuente: cs.fontFamily, fgRgb: fg ? [Math.round(fg.r), Math.round(fg.g), Math.round(fg.b)] : null, bgRgb: bg.opaco ? [Math.round(bg.r), Math.round(bg.g), Math.round(bg.b)] : null, lineas: lineas.length, ultima: lineas.length ? lineas[lineas.length - 1].ps.map(p => p.w) : [], color: cs.color, _el: el});
  }
  // solapes entre cajas de texto (no anidadas)
  out.solapes = [];
  const T = out.textos;
  for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++) {
    const a = T[i], b = T[j];
    if (a._el.contains(b._el) || b._el.contains(a._el) || a.deco || b.deco) continue;
    const ix = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x), iy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    if (ix > 2 && iy > 2) out.solapes.push({a: a.texto, b: b.texto, ix: Math.round(ix), iy: Math.round(iy)});
  }
  // colores usados (texto, fondos y trazos/rellenos de SVG)
  const col = new Map();
  const sumar = (c, donde) => { const p = parseColor(c); if (!p || p.a === 0) return; const k = [Math.round(p.r), Math.round(p.g), Math.round(p.b)].join(','); col.set(k, (col.get(k) || 0) + 1); };
  document.querySelectorAll('body, body *').forEach(el => { const cs = getComputedStyle(el); sumar(cs.backgroundColor); if (el.childNodes && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) sumar(cs.color); if (el instanceof SVGElement) { if (cs.fill !== 'none') sumar(cs.fill); if (cs.stroke !== 'none') sumar(cs.stroke); } if (parseFloat(cs.borderTopWidth) > 0) sumar(cs.borderTopColor); });
  out.colores = [...col.entries()].map(([k, n]) => ({rgb: k.split(',').map(Number), usos: n}));
  // fuentes
  out.fuentesCargadas = [...document.fonts].map(f => ({familia: f.family.replace(/["']/g, ''), estado: f.status}));
  out.fuentesUsadas = [...new Set(T.map(t => t.fuente.split(',')[0].replace(/["']/g, '').trim()))];
  const cv = document.createElement('canvas').getContext('2d');
  const ancho = (fam, base) => { cv.font = '72px ' + (fam ? '"' + fam + '", ' : '') + base; return cv.measureText('mmmmmmmmmmlliWQ@ñ').width; };
  const existe = (f) => /^(sans-serif|serif|monospace|system-ui|ui-sans-serif|ui-serif|ui-monospace|ui-rounded|cursive|fantasy)$/.test(f) || ancho(f, 'monospace') !== ancho(null, 'monospace') || ancho(f, 'serif') !== ancho(null, 'serif');
  out.fuentesDisponibles = out.fuentesUsadas.map(f => ({familia: f, ok: existe(f)}));
  out.tamanos = T.map(t => t.size);
  out.caracteres = T.reduce((s, t) => s + t.texto.length, 0);
  // huellas de plantilla (anti-patrones): degradados y tarjetas anidadas
  const degradados = [], tarjetas = new Set();
  document.querySelectorAll('body, body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.backgroundImage && cs.backgroundImage.includes('gradient')) degradados.push([...cs.backgroundImage.matchAll(/rgba?\(([^)]+)\)/g)].map(m => m[1].split(',').slice(0, 3).map(s => parseFloat(s))));
    const rad = parseFloat(cs.borderTopLeftRadius) || 0, b = el.getBoundingClientRect();
    const fondo = parseColor(cs.backgroundColor), conCaja = (fondo && fondo.a >= 0.5) || (cs.boxShadow && cs.boxShadow !== 'none') || (parseFloat(cs.borderTopWidth) > 0 && parseColor(cs.borderTopColor) && parseColor(cs.borderTopColor).a > 0);
    if (rad >= 12 && conCaja && b.width >= 120 && b.height >= 80 && b.width < innerWidth - 2) tarjetas.add(el);
  });
  let profundidad = 0;
  tarjetas.forEach(el => { let d = 1; for (let a = el.parentElement; a; a = a.parentElement) if (tarjetas.has(a)) d++; profundidad = Math.max(profundidad, d); });
  out.huellas = {degradados, tarjetasAnidadas: profundidad};
  out.textos = T.map(({_el, ...r}) => r);
  return out;
}
