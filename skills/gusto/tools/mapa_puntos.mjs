#!/usr/bin/env node
// Copyright (c) 2026 2894 Studio · MIT
// Genera los puntos de un mapa de puntos (halftone) a partir de la geografía real, como JSON.
//
// Instalación (una vez, en una carpeta de trabajo):  npm i world-atlas topojson-client d3-geo
// Uso:  node mapa_puntos.mjs --bbox -10.5,35.3,7,46.8 --centro -3.70,40.42 [--ancho 1000 --alto 880 --paso 12] > puntos.json
//   --bbox   lonMin,latMin,lonMax,latMax de la zona a encuadrar
//   --centro lon,lat del punto de referencia (la persona, una ciudad)
//   --puntos "lon,lat;lon,lat"  ciudades a proyectar (salen en «puntos»: [[x,y],…], en el mismo orden)
// Salida: {W,H,kmPx,centro:[x,y],dots:[[x,y]...],puntos:[[x,y]...]}; kmPx = píxeles por kilómetro, para dibujar un radio real
// (un anillo de 200 km = 200*kmPx). Proyección cónica conforme, malla hexagonal desplazada, costa de 50 m.
// El encuadre se hace con MultiPoint: un Polygon con el sentido de giro contrario deja la proyección degenerada.
import fs from 'fs';
import {createRequire} from 'module';
import {pathToFileURL} from 'url';
// Los paquetes se buscan en la carpeta desde la que se ejecuta (donde hiciste npm i), no junto a este script.
const req = createRequire(process.cwd() + '/_.js');
const cargar = async (p) => { try { return await import(pathToFileURL(req.resolve(p)).href); } catch { console.error(`Falta el paquete ${p}. Instálalo en esta carpeta:  npm i world-atlas topojson-client d3-geo`); process.exit(2); } };
const {feature} = await cargar('topojson-client');
const {geoConicConformal, geoContains, geoDistance} = await cargar('d3-geo');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const [x0, y0, x1, y1] = arg('bbox', '-10.5,35.3,7,46.8').split(',').map(Number);
const [cx, cy] = arg('centro', '-3.70,40.42').split(',').map(Number);
const W = +arg('ancho', 1000), H = +arg('alto', 880), sp = +arg('paso', 12);
const topo = JSON.parse(fs.readFileSync(req.resolve('world-atlas/land-50m.json')));
const land = feature(topo, topo.objects.land);
const xm = (x0 + x1) / 2, ym = (y0 + y1) / 2;
const box = {type: 'MultiPoint', coordinates: [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, ym], [x1, ym], [xm, y0], [xm, y1]]};
const proj = geoConicConformal().parallels([y0 + (y1 - y0) * 0.25, y0 + (y1 - y0) * 0.75]).fitExtent([[0, 0], [W, H]], box);
const a = [cx, cy], b = [cx, cy + 1];
const kmPx = Math.hypot(...proj(a).map((v, i) => v - proj(b)[i])) / (geoDistance(a, b) * 6371);
const dots = [];
for (let row = 0, y = 6; y < H; y += sp * 0.866, row++)
  for (let x = (row % 2 ? sp / 2 : 0) + 6; x < W; x += sp) {
    const ll = proj.invert([x, y]);
    if (ll && geoContains(land, ll)) dots.push([Math.round(x * 10) / 10, Math.round(y * 10) / 10]);
  }
const puntos = arg('puntos', '').split(';').filter(Boolean).map(s => proj(s.split(',').map(Number)).map(v => Math.round(v * 10) / 10));
console.log(JSON.stringify({W, H, kmPx, centro: proj(a).map(v => Math.round(v * 10) / 10), dots, puntos}));
