#!/usr/bin/env python3
"""Exporta artboards .dc.html do canvas da Solid para PNG.

Uso:
  python3 ferramentas/exportar-pecas.py <pasta-project-do-canvas> <pasta-saida> <arq1.dc.html> [arq2 ...]
       [--blobs <pasta com <id>.svg/png dos /_blob/<id>>] [--fontes <node_modules/@fontsource>]

- Lê o solid.css da pasta do canvas e embute as fontes da marca (Montserrat, Source Sans 3, IBM Plex Mono)
  a partir dos pacotes @fontsource (npm install @fontsource/montserrat @fontsource/source-sans-3 @fontsource/ibm-plex-mono).
- Troca cada /_blob/<id> pelo arquivo local <id>.* da pasta --blobs.
- Tamanho de cada peça vem do $preview do próprio arquivo (1080x1350 feed, 1080x1920 story/reels).
- Código de saída 2 = fonte ou imagem faltando (não use os PNGs nesse caso).
"""
import sys, os, re, json, glob, base64, argparse
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument('proj'); ap.add_argument('out'); ap.add_argument('files', nargs='+')
ap.add_argument('--blobs', default=None)
ap.add_argument('--fontes', default=os.path.expanduser('~/fontes/node_modules/@fontsource'))
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)

FONTES = [('Montserrat', 'montserrat/files/montserrat-latin-{w}-normal.woff2', [500, 600, 700, 800, 900]),
          ('Source Sans 3', 'source-sans-3/files/source-sans-3-latin-{w}-normal.woff2', [400, 600]),
          ('IBM Plex Mono', 'ibm-plex-mono/files/ibm-plex-mono-latin-{w}-normal.woff2', [400, 600])]
faces, erro = [], False
for fam, pat, ws in FONTES:
    for w in ws:
        f = os.path.join(a.fontes, pat.format(w=w))
        if not os.path.exists(f):
            print('FONTE FALTANDO:', f); erro = True; continue
        b64 = base64.b64encode(open(f, 'rb').read()).decode()
        faces.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
# itálico do Source Sans 3 (usado em .ob)
fi = os.path.join(a.fontes, 'source-sans-3/files/source-sans-3-latin-400-italic.woff2')
if os.path.exists(fi):
    faces.append("@font-face{font-family:'Source Sans 3';font-weight:400;font-style:italic;src:url(data:font/woff2;base64,%s) format('woff2');}" % base64.b64encode(open(fi, 'rb').read()).decode())
css = open(os.path.join(a.proj, 'solid.css')).read()

def blob_uri(m):
    global erro
    bid = m.group(1)
    cand = glob.glob(os.path.join(a.blobs or '', bid + '.*')) if a.blobs else []
    if not cand:
        print('IMAGEM FALTANDO: /_blob/' + bid); erro = True; return m.group(0)
    ext = cand[0].rsplit('.', 1)[1].lower()
    mime = {'svg': 'image/svg+xml', 'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'webp': 'image/webp'}[ext]
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(cand[0], 'rb').read()).decode())

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for name in a.files:
        src = open(os.path.join(a.proj, name)).read()
        body = re.search(r'<x-dc>(.*)</x-dc>', src, re.S).group(1)
        body = re.sub(r'<helmet>.*?</helmet>', '', body, flags=re.S)
        body = re.sub(r'/_blob/([0-9a-f]{32})', blob_uri, body)
        prev = json.loads(re.search(r"data-props='(.*?)'", src, re.S).group(1)).get('$preview', {'width': 1080, 'height': 1350})
        W, H = prev['width'], prev['height']
        html = f'<!doctype html><html><head><meta charset="utf-8"><style>{"".join(faces)}{css}html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{body}</body></html>'
        pg = br.new_page(viewport={'width': W, 'height': H})
        pg.set_content(html)
        ok = pg.evaluate("""(async()=>{const fs=['800 40px Montserrat','400 20px "Source Sans 3"','600 20px "IBM Plex Mono"'];
          await Promise.all(fs.map(f=>document.fonts.load(f))); await document.fonts.ready; return fs.every(f=>document.fonts.check(f));})()""")
        if not ok:
            print('FONTE NÃO CARREGOU em', name); erro = True
        # aviso de texto estourando a área da peça
        over = pg.evaluate("(()=>{const s=document.querySelector('.sl');const md=s&&s.querySelector('.md');return md?Math.round(md.scrollHeight-md.clientHeight):0})()")
        if over > 4:
            print(f'AVISO: conteúdo passa {over}px da área central em', name)
        out = os.path.join(a.out, re.sub(r'\.dc\.html$', '.png', os.path.basename(name)))
        pg.screenshot(path=out, clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        pg.close()
    br.close()
sys.exit(2 if erro else 0)
