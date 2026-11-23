#!/usr/bin/env python3
"""Estilos de animação da caixa de mídia do post-card do @lucasgiordane (teste de 23/11/2026).
Mesma página (capa do carrossel P&G "turno sem ninguém"), com a caixa preta animada em 4 estilos:
  glow   · Traço neon: o desenho se faz sozinho em linhas douradas que brilham
  giz    · Quadro de giz: traço de giz branco, anotações à mão, círculo dourado
  pixel  · Pixel art: blocos, fonte 8 bits, movimento em passos
  hq     · Quadrinho: contorno grosso, retícula, balão e onomatopeia
Texto de cima, cabeçalho e rodapé não mudam (padrão dos 5 modelos). Cores da identidade 2026; nunca tom sobre tom.
Uso: python3 -I estilos-animacao.py <saida> <solid26.css> <blobs> <fontes> png|mp4 [estilos, ex.: glow,giz]"""
import os, sys, base64, glob, subprocess, shutil
from playwright.sync_api import sync_playwright
OUT, CSSF, BLOBS, FONTES, MODO = sys.argv[1:6]
SO = sys.argv[6].split(',') if len(sys.argv) > 6 else None
os.makedirs(OUT, exist_ok=True)
FPS, DUR = 30, 6.5

def b64(p): return base64.b64encode(open(p, 'rb').read()).decode()
faces = []
for fam, pat, ws in [('Manrope', 'manrope/files/manrope-latin-{w}-normal.woff2', [500, 600, 700, 800]),
                     ('Inter', 'inter/files/inter-latin-{w}-normal.woff2', [400, 500, 600, 700]),
                     ('IBM Plex Mono', 'ibm-plex-mono/files/ibm-plex-mono-latin-{w}-normal.woff2', [400, 500, 600]),
                     ('Caveat', 'caveat/files/caveat-latin-{w}-normal.woff2', [600, 700]),
                     ('Press Start 2P', 'press-start-2p/files/press-start-2p-latin-{w}-normal.woff2', [400]),
                     ('Bangers', 'bangers/files/bangers-latin-{w}-normal.woff2', [400])]:
    for w in ws:
        faces.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64(os.path.join(FONTES, pat.format(w=w)))}) format('woff2');}}")
AV = 'data:image/jpeg;base64,' + b64(glob.glob(os.path.join(BLOBS, 'a0000000000000000000000000000004.*'))[0])

CSS = open(CSSF).read() + """
.pc .av{width:116px;height:116px;border:0}
.pc .nm b{font-size:44px;letter-spacing:-0.01em}
.pc .nm span{font-size:32px;color:#5B6070}
.pc .pg{top:110px}
.pc .tx{margin-top:36px;gap:22px}
.pc .tp{font-size:38px;line-height:1.36;color:#1E2025}
.pc .tb{font-size:46px}
.pc .mi{margin-top:36px;padding:0}
.estilo{position:absolute;left:26px;bottom:20px;font-family:'IBM Plex Mono',monospace;font-size:17px;letter-spacing:.06em;z-index:6}
.il-l{z-index:6}
svg.cena{position:absolute;inset:0;width:100%;height:100%}
@keyframes draw{from{stroke-dashoffset:var(--L)}to{stroke-dashoffset:0}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{0%{opacity:0;transform:scale(.5)}70%{opacity:1;transform:scale(1.1)}100%{opacity:1;transform:scale(1)}}
@keyframes esteira{from{transform:translateX(0)}to{transform:translateX(840px)}}
@keyframes flick{0%,100%{opacity:1}45%{opacity:.82}50%{opacity:.55}55%{opacity:.9}}
@keyframes twk{0%,49%{opacity:1}50%,100%{opacity:.15}}
@keyframes shake{0%,100%{transform:rotate(-4deg) scale(1)}50%{transform:rotate(3deg) scale(1.06)}}
@keyframes inUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:none}}

/* ---------- GLOW · traço neon ---------- */
.glow{background:#0A0A0C}
.glow .ln{fill:none;stroke:#DDA94F;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 6px #DDA94F) drop-shadow(0 0 16px rgba(221,169,79,.6))}
.glow .ln2{fill:none;stroke:#F4F1EA;stroke-width:3;stroke-linecap:round;filter:drop-shadow(0 0 6px rgba(244,241,234,.8))}
.glow .gt{position:absolute;font-family:'IBM Plex Mono',monospace;font-weight:600;color:#F4F1EA;text-shadow:0 0 10px rgba(244,241,234,.8)}
.glow .gt.g{color:#DDA94F;text-shadow:0 0 12px #DDA94F,0 0 28px rgba(221,169,79,.6)}
.glow .estilo{color:#DDA94F}
/* ---------- GIZ · quadro de giz ---------- */
.giz{background:#1E2025;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:6px 6px}
.giz .ln{fill:none;stroke:#F4F1EA;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;filter:url(#chalk);opacity:.92}
.giz .lng{fill:none;stroke:#DDA94F;stroke-width:6;stroke-linecap:round;filter:url(#chalk)}
.giz .hw{position:absolute;font-family:Caveat,cursive;font-weight:700;color:#F4F1EA;line-height:1}
.giz .hw.g{color:#DDA94F}
.giz .estilo{color:#A5A8AE}
/* ---------- PIXEL ---------- */
.pixel{background:#101013;image-rendering:pixelated}
.pixel .px{position:absolute;font-family:'Press Start 2P',monospace;color:#F4F1EA;line-height:1.5}
.pixel .px.g{color:#101013;background:#DDA94F;padding:12px 14px;box-shadow:6px 6px 0 #A6752D}
.pixel .estilo{color:#DDA94F;font-family:'Press Start 2P',monospace;font-size:12px}
/* ---------- HQ · quadrinho ---------- */
.hq{background:#F4F1EA;background-image:radial-gradient(#D9D2C1 2.2px,transparent 2.4px);background-size:16px 16px}
.hq .ln{stroke:#101013;stroke-width:7;stroke-linejoin:round;stroke-linecap:round}
.hq .bl{position:absolute;background:#FFFFFF;border:5px solid #101013;border-radius:50%;padding:26px 34px;font-family:Bangers,cursive;font-size:44px;letter-spacing:.03em;color:#101013;text-align:center;line-height:1.05}
.hq .bl::after{content:'';position:absolute;left:70px;bottom:-22px;border:18px solid transparent;border-top:30px solid #101013;border-bottom:0}
.hq .bum{position:absolute;font-family:Bangers,cursive;font-size:84px;color:#DDA94F;-webkit-text-stroke:4px #101013;letter-spacing:.04em}
.hq .zz{position:absolute;font-family:Bangers,cursive;font-size:48px;color:#101013}
.hq .estilo{color:#101013;font-weight:600}
.hq .il-l{color:#3C4149}
"""
def A(name, dur, delay, ease='cubic-bezier(.2,.8,.2,1)'):
    return f'style="animation:{name} {dur}s {delay}s both {ease}"'
def page(texto, media, rodape='Arraste →'):
    return f'''<div class="pc">
<div class="au2"><img class="av" src="{AV}" alt=""><div class="nm"><b>Lucas Giordane</b><span>@lucasgiordane</span></div></div>
<span class="pg">1/6</span>
<div class="tx"><span class="tg">CURIOSIDADE</span>{texto}</div>
<div class="mi">{media}</div>
<div class="lg"><span>{rodape}</span><i>SOLID BUSINESS</i></div>
</div>'''
TXT = ('<p class="tb">A P&amp;G já tem fábricas que trabalham <em>turnos inteiros sem ninguém dentro.</em></p>'
       '<p class="tp">A dona de Gillette, Pampers e Ariel contou o plano aos investidores. Te conto ↓</p>')
IL = '<span class="il-l">ILUSTRAÇÃO</span>'

# geometria da fábrica (caixa de 920 x 680)
TELHADO = 'M60 360 L60 270 L210 360 L210 270 L360 360 L360 270 L510 360'
PREDIO = 'M60 360 L860 360 L860 580 L60 580 Z'
CHAMINE = 'M690 360 L690 240 L726 240 L726 360 M760 360 L760 280 L796 280 L796 360'
ESTEIRA = 'M90 540 L830 540'
JANELAS = [(100 + 92 * k, 390, 62, 44) for k in range(8)]
def path(d, cls, delay, dur, L=2400):
    return f'<path class="{cls}" d="{d}" style="--L:{L};stroke-dasharray:{L};animation:draw {dur}s {delay}s both ease-in-out"/>'
def jan(cls, d0):
    return ''.join(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4" style="--L:220;stroke-dasharray:220;animation:draw .35s {d0 + .1 * k:.2f}s both"/>' for k, (x, y, w, h) in enumerate(JANELAS))

def glow():
    caixas = ''.join(f'<rect class="ln" x="70" y="498" width="40" height="34" rx="3" style="animation:esteira 4.6s {-k * .92:.2f}s infinite linear, fade .3s 2.6s both"/>' for k in range(5))
    svg = (f'<svg class="cena" viewBox="0 0 920 680"><clipPath id="cl"><rect x="64" y="364" width="792" height="212"/></clipPath>'
           + path(PREDIO, 'ln', .3, 1.2) + path(TELHADO, 'ln', 1.0, .9) + path(CHAMINE, 'ln', 1.4, .8) + jan('ln2', 1.8)
           + path(ESTEIRA, 'ln2', 2.3, .5, 760) + f'<g clip-path="url(#cl)">{caixas}</g>'
           + '<circle cx="820" cy="110" r="38" class="ln2" style="--L:240;stroke-dasharray:240;animation:draw .8s .2s both"/></svg>')
    txt = (f'<div class="gt" style="left:44px;top:60px;font-size:20px;letter-spacing:.08em;animation:fade .5s 2.8s both">EXEMPLO DE TURNO</div>'
           f'<div class="gt" style="left:44px;top:92px;font-size:54px;animation:fade .5s 3.0s both, flick 2.2s 3.6s infinite">22:00 → 06:00</div>'
           f'<div class="gt g" style="left:44px;top:172px;font-size:40px;font-family:Manrope,sans-serif;font-weight:800;animation:pop .6s 3.6s both">0 pessoas na linha</div>')
    return f'<div class="glow" style="position:absolute;inset:0">{svg}{txt}{IL}<span class="estilo">ESTILO · TRAÇO NEON</span></div>'

def giz():
    caixas = ''.join(f'<rect class="ln" x="70" y="496" width="42" height="36" style="animation:esteira 4.6s {-k * .92:.2f}s infinite linear, fade .3s 2.6s both"/>' for k in range(5))
    filt = ('<filter id="chalk"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" result="n"/>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>')
    svg = (f'<svg class="cena" viewBox="0 0 920 680">{filt}<clipPath id="cl"><rect x="64" y="364" width="792" height="212"/></clipPath>'
           + path(PREDIO, 'ln', .3, 1.3) + path(TELHADO, 'ln', 1.1, .9) + path(CHAMINE, 'ln', 1.5, .8) + jan('ln', 1.9)
           + path(ESTEIRA, 'ln', 2.4, .5, 760) + f'<g clip-path="url(#cl)">{caixas}</g>'
           # círculo dourado em volta do "0 pessoas" e seta até a fábrica
           + path('M30 190 C 30 140, 470 140, 470 190 C 470 245, 30 245, 34 186', 'lng', 4.0, .8, 1100)
           + path('M480 210 C 560 230, 600 260, 600 330 M582 310 L600 334 L622 312', 'lng', 4.6, .6, 300) + '</svg>')
    txt = (f'<div class="hw" style="left:46px;top:50px;font-size:44px;animation:fade .6s 2.9s both">turno das 22h às 6h <span style="font-size:30px">(exemplo)</span></div>'
           f'<div class="hw g" style="left:62px;top:160px;font-size:66px;animation:fade .6s 3.5s both">0 pessoas na linha!</div>')
    return f'<div class="giz" style="position:absolute;inset:0">{svg}{txt}{IL}<span class="estilo">ESTILO · QUADRO DE GIZ</span></div>'

def pixel():
    P = 10  # tamanho do "pixel"
    def bloco(x, y, w, h, cor, extra=''):
        return f'<i style="position:absolute;left:{x * P}px;top:{y * P}px;width:{w * P}px;height:{h * P}px;background:{cor};{extra}"></i>'
    cena = ''
    cena += bloco(6, 36, 80, 22, '#F4F1EA', 'animation:fade .01s .4s both')            # prédio (contorno)
    cena += bloco(7, 37, 78, 20, '#1E2025', 'animation:fade .01s .4s both')
    for k, x0 in enumerate([6, 21, 36]):                                                # telhado em degraus
        for s in range(9):
            cena += bloco(x0 + s * 1.5, 27 + s, 1.5, 9 - s, '#F4F1EA', f'animation:fade .01s {.7 + .25 * k:.2f}s both')
    cena += bloco(69, 24, 4, 12, '#F4F1EA', 'animation:fade .01s 1.5s both') + bloco(76, 28, 4, 8, '#F4F1EA', 'animation:fade .01s 1.6s both')
    for k in range(8):
        cena += bloco(10 + 9.5 * k, 39, 6, 4, '#3C4149', f'animation:fade .01s {1.8 + .1 * k:.2f}s both')
    cena += bloco(9, 53, 74, 1, '#A5A8AE', 'animation:fade .01s 2.6s both')
    cx = ''.join(f'<i style="position:absolute;left:{9 * P}px;top:{49 * P}px;width:{4 * P}px;height:{4 * P}px;background:#DDA94F;box-shadow:inset -10px -10px 0 #A6752D;animation:esteira 4.6s {-k * .92:.2f}s infinite steps(42), fade .01s 2.7s both"></i>' for k in range(5))
    cena += f'<div style="position:absolute;left:{7 * P}px;top:{37 * P}px;width:{78 * P}px;height:{20 * P}px;overflow:hidden"><div style="position:absolute;left:-{7 * P}px;top:-{37 * P}px">{cx}</div></div>'
    lua = bloco(80, 6, 6, 6, '#F4F1EA', 'animation:fade .01s .2s both') + bloco(82, 5, 4, 5, '#101013', 'animation:fade .01s .2s both')
    est = ''.join(bloco(x, y, 1, 1, '#F4F1EA', f'animation:twk 1.2s {d}s infinite steps(1)') for x, y, d in [(20, 4, 0), (34, 10, .4), (50, 3, .8), (62, 14, .2), (71, 8, .6), (44, 18, 1.0)])
    txt = (f'<div class="px" style="left:44px;top:60px;font-size:16px;animation:fade .01s 2.9s both">EXEMPLO DE TURNO</div>'
           f'<div class="px" style="left:44px;top:96px;font-size:34px;animation:fade .01s 3.1s both">22:00 - 06:00</div>'
           f'<div class="px g" style="left:44px;top:164px;font-size:22px;animation:pop .4s 3.6s both steps(4)">0 PESSOAS NA LINHA</div>')
    return f'<div class="pixel" style="position:absolute;inset:0">{lua}{est}{cena}{txt}{IL}<span class="estilo">ESTILO · PIXEL ART</span></div>'

def hq():
    caixas = ''.join(f'<rect x="70" y="494" width="44" height="38" fill="#DDA94F" stroke="#101013" stroke-width="5" style="animation:esteira 4.6s {-k * .92:.2f}s infinite linear"/>' for k in range(5))
    svg = (f'<svg class="cena" viewBox="0 0 920 680" style="animation:pop .6s .2s both"><clipPath id="cl"><rect x="64" y="364" width="792" height="212"/></clipPath>'
           f'<path class="ln" d="{TELHADO} L510 360 Z" fill="#3C4149"/><path class="ln" d="M210 360 L210 270 L360 360 Z M360 360 L360 270 L510 360 Z" fill="#3C4149"/>'
           f'<path class="ln" d="M690 360 L690 240 L726 240 L726 360 Z M760 360 L760 280 L796 280 L796 360 Z" fill="#1E2025"/>'
           f'<path class="ln" d="{PREDIO}" fill="#1E2025"/>'
           + ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#101013" stroke="#F4F1EA" stroke-width="3"/>' for x, y, w, h in JANELAS)
           + f'<line x1="90" y1="540" x2="830" y2="540" stroke="#A5A8AE" stroke-width="10" stroke-linecap="round"/><g clip-path="url(#cl)">{caixas}</g></svg>')
    txt = (f'<div class="bl" style="left:40px;top:40px;animation:pop .5s 1.4s both">22H ÀS 6H (EXEMPLO):<br>0 PESSOAS NA LINHA!</div>'
           f'<div class="bum" style="right:50px;top:200px;animation:pop .4s 2.6s both, shake .5s 3.0s 4 both">CLANK!</div>'
           f'<div class="zz" style="left:600px;top:120px;animation:fade .4s 3.4s both, shake .9s 3.8s 3">Z z z</div>')
    return f'<div class="hq" style="position:absolute;inset:0">{svg}{txt}{IL}<span class="estilo">ESTILO · QUADRINHO</span></div>'

ESTILOS = [('glow', glow), ('giz', giz), ('pixel', pixel), ('hq', hq)]
with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={'width': 1080, 'height': 1350})
    for nome, fn in ESTILOS:
        if SO and nome not in SO: continue
        body = page(TXT, fn())
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{"".join(faces)}{CSS}html,body{{margin:0;width:1080px;height:1350px;overflow:hidden}}</style></head><body>{body}</body></html>')
        pg.evaluate('document.fonts.ready')
        if MODO == 'png':
            pg.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {DUR * 1000 - 1}; }})')
            pg.screenshot(path=os.path.join(OUT, f'estilo-{nome}.png'))
            continue
        fr = os.path.join(OUT, f'f-{nome}'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
        for f in range(int(FPS * DUR)):
            pg.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {f * 1000 / FPS}; }})')
            pg.screenshot(path=os.path.join(fr, f'{f:04d}.png'))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(fr, '%04d.png'),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', os.path.join(OUT, f'estilo-{nome}.mp4')], check=True)
        shutil.rmtree(fr)
    br.close()
print('ok')
