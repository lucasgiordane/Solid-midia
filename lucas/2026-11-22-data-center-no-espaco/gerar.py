#!/usr/bin/env python3
"""@lucasgiordane · 22/11/2026 · Modelo 3 CURIOSIDADE: "O Google vai colocar data center de IA no espaço".
Uso: python3 -I gerar.py <saida> <solid26.css> <blobs> <fontes> png|mp4 [páginas, ex.: 1,4]
Fonte de todos os fatos: The Next Web, 19/11/2026 (anúncio do Google no blog, mesmo dia)."""
import os, sys, base64, glob, subprocess, shutil
from playwright.sync_api import sync_playwright
OUT, CSSF, BLOBS, FONTES, MODO = sys.argv[1:6]
SO = [int(x) for x in sys.argv[6].split(',')] if len(sys.argv) > 6 else None
os.makedirs(OUT, exist_ok=True)
FPS = 30

def b64(p): return base64.b64encode(open(p, 'rb').read()).decode()
faces = []
for fam, pat, ws in [('Manrope', 'manrope/files/manrope-latin-{w}-normal.woff2', [500, 600, 700, 800]),
                     ('Inter', 'inter/files/inter-latin-{w}-normal.woff2', [400, 500, 600, 700]),
                     ('IBM Plex Mono', 'ibm-plex-mono/files/ibm-plex-mono-latin-{w}-normal.woff2', [400, 500, 600])]:
    for w in ws:
        faces.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64(os.path.join(FONTES, pat.format(w=w)))}) format('woff2');}}")
AV = 'data:image/jpeg;base64,' + b64(glob.glob(os.path.join(BLOBS, 'a0000000000000000000000000000004.*'))[0])

CSS = open(CSSF).read() + """
/* cabeçalho igual ao dos modelos aprovados: foto, nome grande, @ embaixo, sem selo */
.pc .av{width:116px;height:116px;border:0}
.pc .nm b{font-size:44px;letter-spacing:-0.01em}
.pc .nm span{font-size:32px;color:#5B6070}
.pc .pg{top:110px}
.pc .tx{margin-top:36px;gap:22px}
.pc .tp{font-size:38px;line-height:1.36;color:#1E2025}
.pc .tp b{color:#101013}
.pc .tb{font-size:46px}
.pc .mi{margin-top:36px;padding:0}
.fonte{position:absolute;left:26px;bottom:18px;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#A5A8AE}
/* cena do espaço */
.sky{position:absolute;inset:0;overflow:hidden}
.st{position:absolute;width:3px;height:3px;border-radius:50%;background:#F5F5F5;opacity:.55}
.sun{position:absolute;left:46px;top:40px;width:86px;height:86px;border-radius:50%;background:#DDA94F;box-shadow:0 0 0 14px rgba(221,169,79,.18),0 0 0 30px rgba(221,169,79,.08)}
.earth{position:absolute;left:-15%;width:130%;top:72%;height:900px;border-radius:50%;background:#1E2025;border:4px solid #F4F1EA;box-sizing:border-box}
.orb{position:absolute;left:-6%;right:-6%;top:30%;height:62%;border-radius:50%;border:3px dashed #A6752D}
.sat{position:absolute;display:flex;align-items:center;gap:0}
.sat .pn{width:74px;height:42px;background:#DDA94F;border-radius:3px;background-image:linear-gradient(90deg,transparent 47%,#101013 47%,#101013 53%,transparent 53%),linear-gradient(0deg,transparent 46%,#101013 46%,#101013 54%,transparent 54%)}
.sat .bd{width:44px;height:52px;background:#F4F1EA;border-radius:6px;display:flex;align-items:center;justify-content:center;font-family:Manrope,sans-serif;font-weight:800;font-size:13px;letter-spacing:0;color:#101013}
.sat .rd{width:10px;height:4px;background:#F4F1EA}
.lz{position:absolute;height:4px;background:#DDA94F;transform-origin:left center;border-radius:2px;box-shadow:0 0 10px rgba(221,169,79,.7)}
.tagbx{position:absolute;right:26px;bottom:24px;background:#F4F1EA;color:#101013;border-radius:10px;padding:14px 18px;display:flex;flex-direction:column;gap:4px}
.tagbx b{font-family:Manrope,sans-serif;font-weight:800;font-size:26px}
.tagbx span{font-family:'IBM Plex Mono',monospace;font-size:18px;color:#3C4149}
/* página 2: satélite grande com chamadas */
.big{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
.big .sat{position:relative}
.big .pn{width:170px;height:96px}
.big .bd{width:104px;height:120px;font-family:Manrope,sans-serif;font-weight:800;font-size:30px;letter-spacing:0;border-radius:10px}
.big .rd{width:22px;height:8px}
.call{position:absolute;background:#F4F1EA;color:#101013;border-radius:12px;padding:14px 18px;display:flex;flex-direction:column;gap:4px;max-width:300px}
.call b{font-family:Manrope,sans-serif;font-weight:800;font-size:27px}
.call span{font-size:20px;color:#3C4149;line-height:1.3}
.call.g{background:#DDA94F}
.call.g span{color:#101013}
.ln{position:absolute;height:3px;background:#DDA94F;transform-origin:left center}
/* página 3: barras */
.bars{padding:56px 48px 0;display:flex;flex-direction:column;gap:40px}
.br .lb{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}
.br .lb span{font-size:28px;color:#F5F5F5}
.br .lb b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:44px;color:#F4F1EA}
.br .tr{height:70px;border-radius:10px;background:#2A2D33;overflow:hidden}
.br .tr i{display:block;height:100%;border-radius:10px;background:#F4F1EA;transform-origin:left center}
.br.g .lb b{color:#DDA94F}
.br.g .tr i{background:#DDA94F}
.cap{margin:44px 48px 0;font-size:28px;line-height:1.35;color:#F5F5F5;background:#2A2416;border:1px solid #A6752D;border-radius:12px;padding:18px 22px}
.cap b{color:#DDA94F}
/* página 4: linha do tempo */
.tl{padding:44px 48px 0;display:flex;flex-direction:column;gap:22px;position:relative}
.tl .lnv{position:absolute;left:83px;top:70px;bottom:40px;width:4px;background:#A6752D;transform-origin:top center}
.ev{display:flex;gap:26px;align-items:flex-start;position:relative}
.ev .dt{flex:none;width:74px;height:74px;border-radius:50%;background:#1E2025;border:4px solid #DDA94F;display:flex;align-items:center;justify-content:center;font-size:30px;color:#DDA94F;font-weight:700;box-sizing:border-box}
.ev .dt.ok{background:#DDA94F;color:#101013}
.ev .cd{flex:1;background:#F4F1EA;border-radius:12px;padding:16px 20px;color:#101013}
.ev .cd small{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:19px;color:#A6752D;letter-spacing:.04em}
.ev .cd b{display:block;font-family:Manrope,sans-serif;font-weight:800;font-size:28px;margin-top:4px}
.ev .cd span{display:block;font-size:20px;color:#3C4149;margin-top:4px;line-height:1.3}
/* página 5: riscos */
.rk{padding:40px 40px 0;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.rk div{background:#F4F1EA;border-radius:12px;padding:20px 20px 22px;color:#101013;display:flex;flex-direction:column;gap:10px;border-left:8px solid #EF4444}
.rk div i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:18px;color:#B91C1C;letter-spacing:.06em}
.rk div b{font-family:Manrope,sans-serif;font-weight:800;font-size:26px;line-height:1.22}
.rk div span{font-size:19px;color:#3C4149;line-height:1.3}
/* página 6: CTA (mesmo padrão do teste animado de 21/11) */
.ctaw{padding:36px 40px 0}
.kw{display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:8px}
.kwl{font-family:Inter,sans-serif;font-weight:600;font-size:22px;letter-spacing:.24em;color:#A5A8AE;text-transform:uppercase}
.tw{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:72px;color:#DDA94F;letter-spacing:.02em;white-space:nowrap;overflow:hidden;border-right:5px solid #DDA94F;animation:type 1.1s .7s steps(11) both, caret .6s 1.8s 3 both}
@keyframes type{from{width:0}to{width:11.6ch}}
@keyframes caret{50%{border-color:transparent}}
.cm{margin-top:22px;display:flex;align-items:center;gap:16px;background:#1E2025;border:1px solid #3C4149;border-radius:14px;padding:14px 18px}
.cm img{width:52px;height:52px;border-radius:50%;object-fit:cover}
.cm div{display:flex;flex-direction:column;gap:2px;flex:1}
.cm b{font-family:Inter,sans-serif;font-weight:600;font-size:19px;color:#A5A8AE}
.cm span{font-size:24px;color:#F5F5F5}
.cm .ty{font-family:'IBM Plex Mono',monospace;font-weight:600;color:#DDA94F;font-size:28px}
.cm em{font-style:normal;color:#EF4444;font-size:28px}
.cm.me{margin-top:12px;margin-left:60px}
.cm .avg{flex:none;width:52px;height:52px;border-radius:50%;background:#3C4149;display:block}
.dm{margin-top:14px;margin-left:60px;background:#2A2416;border:1px solid #A6752D;border-radius:14px 14px 4px 14px;padding:14px 18px;display:flex;flex-direction:column;gap:4px}
.dm small{font-family:'IBM Plex Mono',monospace;font-size:15px;color:#DDA94F}
.dm span{font-size:23px;color:#F5F5F5;line-height:1.35}
/* animações */
@keyframes inL{from{opacity:0;transform:translateX(-50px)}to{opacity:1;transform:none}}
@keyframes inR{from{opacity:0;transform:translateX(50px)}to{opacity:1;transform:none}}
@keyframes inUp{from{opacity:0;transform:translateY(36px)}to{opacity:1;transform:none}}
@keyframes rise{from{transform:translateY(260px)}to{transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes growY{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:scale(1)}}
@keyframes popbig{0%{opacity:0;transform:translate(-50%,-50%) scale(.5)}100%{opacity:1;transform:translate(-50%,-50%) scale(1)}}
@keyframes glow{0%,100%{box-shadow:0 0 0 14px rgba(221,169,79,.18),0 0 0 30px rgba(221,169,79,.08)}50%{box-shadow:0 0 0 22px rgba(221,169,79,.24),0 0 0 44px rgba(221,169,79,.1)}}
@keyframes twk{0%,100%{opacity:.25}50%{opacity:.9}}
"""
def A(name, dur, delay, ease='cubic-bezier(.2,.8,.2,1)'):
    return f'style="animation:{name} {dur}s {delay}s both {ease}"'
def page(pg, tag, texto, media, rodape):
    tg = f'<span class="tg">{tag}</span>' if tag else ''
    return f'''<div class="pc">
<div class="au2"><img class="av" src="{AV}" alt=""><div class="nm"><b>Lucas Giordane</b><span>@lucasgiordane</span></div></div>
<span class="pg">{pg}</span>
<div class="tx">{tg}{texto}</div>
<div class="mi">{media}</div>
<div class="lg"><span>{rodape}</span><i>SOLID BUSINESS</i></div>
</div>'''
TP = lambda x: f'<p class="tp">{x}</p>'
TB = lambda x: f'<p class="tb">{x}</p>'
IL = '<span class="il-l" style="z-index:5">ILUSTRAÇÃO</span>'
FT = '<span class="fonte" style="z-index:5">Fonte: Google, via The Next Web · 19/11/2026</span>'
EST = [(6, 12), (18, 40), (31, 8), (44, 30), (57, 16), (70, 6), (83, 34), (93, 14), (12, 58), (38, 52), (64, 48), (88, 60), (24, 26), (76, 22), (50, 4)]
def stars(tw=True):
    return ''.join(f'<i class="st" style="left:{x}%;top:{y}%;{"animation:twk 2.4s " + str(round(k * .17, 2)) + "s infinite both" if tw else ""}"></i>' for k, (x, y) in enumerate(EST))
def sat(label='TPU'):
    return f'<div class="sat"><div class="pn"></div><div class="rd"></div><div class="bd">{label}</div><div class="rd"></div><div class="pn"></div></div>'

PAGS = []
# 1 · capa: o céu, a órbita e os satélites entrando um por vez, ligados por laser
sats = [(14, 40, 1.4), (41, 25, 1.9), (68, 34, 2.4)]
s1 = ''.join(f'<div style="position:absolute;left:{x}%;top:{y}%"><div {A("pop", .6, t)}>{sat()}</div></div>' for x, y, t in sats)
def laser(x, y, w, ang, t):
    return f'<span style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:4px;transform:rotate({ang}deg);transform-origin:left center"><span class="lz" style="left:0;top:0;width:100%;animation:grow .5s {t}s both"></span></span>'
lz = laser(235, 318, 271, -23.9, 3.0) + laser(483, 208, 258, 14.8, 3.4)
cena1 = (f'<div class="sky">{stars()}<span class="sun" style="animation:fade .8s .1s both, glow 2.4s 1s infinite"></span>'
         f'<div class="orb" {A("fade", .8, .9)}></div><div class="earth" {A("rise", 1.0, .2)}></div>{lz}{s1}'
         f'<div class="tagbx" {A("inUp", .6, 4.0)}><b>Project Suncatcher</b><span>Google · lançamento em 2029</span></div></div>')
PAGS.append((6.0, page('1/6', 'CURIOSIDADE', TB('O Google vai colocar <em>data center de inteligência artificial</em> no espaço.') + TP('Já tem até foguete contratado. Te conto ↓'),
                       IL + cena1, 'Arraste →')))
# 2 · o satélite por dentro
big = f'<div class="big" style="animation:popbig .8s .3s both cubic-bezier(.2,.8,.2,1)">{sat("TPU")}</div>'
calls = ('<svg style="position:absolute;inset:0;width:100%;height:100%" viewBox="0 0 920 702"><g stroke="#DDA94F" stroke-width="4" stroke-linecap="round">'
         f'<line x1="250" y1="161" x2="250" y2="303" {A("fade", .4, 1.9)}/><line x1="640" y1="187" x2="480" y2="291" {A("fade", .4, 2.8)}/><line x1="460" y1="411" x2="460" y2="517" {A("fade", .4, 3.7)}/></g></svg>'
         f'<div class="call" style="left:28px;top:66px" {A("inL", .5, 1.5)}><b>Painel solar</b><span>a energia vem direto do sol</span></div>'
         f'<div class="call g" style="right:28px;top:66px" {A("inR", .5, 2.4)}><b>Chips de IA (TPU)</b><span>cerca de um rack de data center em cada satélite</span></div>'
         f'<div style="position:absolute;left:0;right:0;bottom:64px;display:flex;justify-content:center"><div class="call" style="position:relative" {A("inUp", .5, 3.3)}><b>Laser</b><span>para conversar com os satélites vizinhos</span></div></div>')
PAGS.append((6.0, page('2/6', None, TB('1. Cada satélite é <em>um pedaço de data center.</em>') + TP('Ele leva os chips de IA do próprio Google, as TPUs: cerca de um rack inteiro de servidores por satélite.'),
                       IL + f'<div class="sky">{stars(False)}</div>' + big + calls + FT, 'Arraste →')))
# 3 · por que no espaço: até 8x mais energia
barras = (f'<div class="bars"><div class="br" {A("fade", .4, .3)}><div class="lb"><span>Painel solar na Terra</span><b>1x</b></div><div class="tr"><i style="width:12.5%;animation:grow .6s .6s both"></i></div></div>'
          f'<div class="br g" {A("fade", .4, 1.4)}><div class="lb"><span>Mesmo painel em órbita</span><b>até 8x</b></div><div class="tr"><i style="width:100%;animation:grow 1.4s 1.7s both cubic-bezier(.2,.8,.2,1)"></i></div></div></div>'
          f'<p class="cap" {A("inUp", .6, 3.6)}>Os data centers de IA já pesam nas redes elétricas. <b>Energia virou o gargalo da IA.</b></p>')
PAGS.append((6.0, page('3/6', None, TB('2. Por que no espaço? <em>Sol quase o tempo todo.</em>') + TP('Numa órbita que acompanha o sol, o painel quase nunca fica no escuro. Segundo o Google, gera até 8 vezes mais energia.'),
                       barras + FT, 'Arraste →')))
# 4 · linha do tempo
evs = [('✓', 'ok', 'OUT/2026', 'Protótipo já está em órbita', 'Feito com a Planet. Rodou o Gemma 4, um modelo de IA do Google, e mandou de volta um haicai.'),
       ('2', '', '2027', 'Dois satélites ligados', 'Primeiro teste conversando entre si por laser.'),
       ('3', '', '1º TRI/2029', 'Lançamento no New Glenn', 'Foguete da Blue Origin, de Jeff Bezos. Valor do contrato não divulgado.')]
tl = ''.join(f'<div class="ev" {A("inL", .55, .8 + 1.1 * i)}><span class="dt {c}">{n}</span><div class="cd"><small>{d}</small><b>{t}</b><span>{s}</span></div></div>' for i, (n, c, d, t, s) in enumerate(evs))
PAGS.append((6.5, page('4/6', None, TB('3. Isso <em>já começou.</em>') + TP('Tem protótipo lá em cima e o Google já marcou o lançamento grande.'),
                       f'<div class="tl"><span class="lnv" {A("growY", 2.6, .5, "linear")}></span>{tl}</div>' + FT, 'Arraste →')))
# 5 · os riscos
rks = [('RISCO 1', 'Sem ar para esfriar os chips', 'No espaço, o calor não sai do jeito que sai aqui.'),
       ('RISCO 2', 'Voo em formação apertada', 'Os satélites precisam ficar perto para falar por laser.'),
       ('RISCO 3', 'Foguete parado', 'O New Glenn explodiu num teste em maio. Volta prevista para janeiro.'),
       ('RISCO 4', 'Até a SpaceX duvida', 'Avisou que data center em órbita pode nunca funcionar.')]
rk = ''.join(f'<div {A("pop", .5, .6 + .7 * i)}><i>{a}</i><b>{b}</b><span>{c}</span></div>' for i, (a, b, c) in enumerate(rks))
PAGS.append((6.0, page('5/6', None, TB('4. Mas ainda <em>pode não dar certo.</em>') + TP('O próprio mercado aponta pelo menos 4 problemas sem solução hoje.'),
                       f'<div class="rk">{rk}</div>' + FT, 'Arraste: falta uma pergunta →')))
# 6 · CTA DIAGNÓSTICO
cm = (f'<div class="ctaw"><div class="kw" {A("pop", .6, .4)}><span class="kwl">comente</span><b class="tw">DIAGNÓSTICO</b></div>'
      f'<div class="cm" {A("inUp", .6, 2.0)}><i class="avg"></i><div><b>seguidor</b><span class="ty">DIAGNÓSTICO</span></div><em {A("pop", .4, 2.6)}>♥</em></div>'
      f'<div class="cm me" {A("inUp", .6, 3.1)}><img src="{AV}" alt=""><div><b>lucasgiordane</b><span>Te chamei no direct! 📩</span></div></div>'
      f'<div class="dm" {A("inUp", .6, 4.2)}><small>direct · lucasgiordane</small><span>Oi! Me conta: qual é o seu negócio e o que mais trava hoje?</span></div></div>')
PAGS.append((7.0, page('6/6', 'SUA VEZ', TB('A IA gasta tanta energia que já foi buscar sol <em>fora do planeta.</em>') + TP('E aqui na Terra, onde ela já cabe no seu negócio? <b>Comenta DIAGNÓSTICO</b> que eu te chamo no direct. E salva para não perder.'),
                       cm, 'Comenta DIAGNÓSTICO ↓')))

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pgw = br.new_page(viewport={'width': 1080, 'height': 1350})
    for i, (dur, body) in enumerate(PAGS, 1):
        if SO and i not in SO: continue
        pgw.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{"".join(faces)}{CSS}html,body{{margin:0;width:1080px;height:1350px;overflow:hidden}}</style></head><body>{body}</body></html>')
        pgw.evaluate('document.fonts.ready')
        if MODO == 'png':
            pgw.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {dur * 1000 - 1}; }})')
            pgw.screenshot(path=os.path.join(OUT, f'slide-{i:02d}.png'))
            continue
        fr = os.path.join(OUT, f'f{i}'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
        n = int(FPS * dur)
        for f in range(n):
            pgw.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {f * 1000 / FPS}; }})')
            pgw.screenshot(path=os.path.join(fr, f'{f:04d}.png'))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(fr, '%04d.png'),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', os.path.join(OUT, f'slide-{i:02d}.mp4')], check=True)
        shutil.rmtree(fr)
    br.close()
print('ok')
