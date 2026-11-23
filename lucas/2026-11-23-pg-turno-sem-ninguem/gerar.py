#!/usr/bin/env python3
"""@lucasgiordane · 23/11/2026 · Modelo 3 CURIOSIDADE: "A P&G já tem fábricas que trabalham turnos inteiros sem ninguém dentro".
Estilo de animação: QUADRINHO (aprovado pelo Lucas em 23/11/2026; teste dos 4 estilos em ferramentas/post-card/estilos-animacao.py).
Uso: python3 -I gerar.py <saida> <solid26.css> <blobs> <fontes> png|mp4 [páginas, ex.: 1,4]
Fontes: P&G no dia do investidor (19/11/2026), via New York Times/PYMNTS (22/11/2026) e Tech Times UK (23/11/2026)."""
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
                     ('IBM Plex Mono', 'ibm-plex-mono/files/ibm-plex-mono-latin-{w}-normal.woff2', [400, 500, 600]),
                     ('Bangers', 'bangers/files/bangers-latin-{w}-normal.woff2', [400])]:
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
/* caixa de mídia em quadrinho: papel marfim com retícula e contorno grosso */
.pc .mi{margin-top:36px;padding:0;background:#F4F1EA;background-image:radial-gradient(#D9D2C1 2.2px,transparent 2.4px);background-size:16px 16px;border:6px solid #101013;color:#101013}
.il-l{color:#3C4149;z-index:6}
.fonte{position:absolute;left:24px;bottom:16px;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#3C4149;z-index:6}
.bg{font-family:Bangers,cursive;letter-spacing:.03em;font-weight:400}
.qd{background:#FFFFFF;border:5px solid #101013;border-radius:10px;box-shadow:7px 7px 0 #101013}
.qd.g{background:#DDA94F}
.qd.k{background:#1E2025;color:#F5F5F5}
.qd.r{background:#FFFFFF;border-color:#B91C1C;box-shadow:7px 7px 0 #B91C1C}
.leg{position:absolute;background:#DDA94F;border:4px solid #101013;padding:10px 16px;font-family:Inter,sans-serif;font-weight:700;font-size:22px;color:#101013;line-height:1.3}
.bl{position:absolute;background:#FFFFFF;border:5px solid #101013;border-radius:50%;padding:26px 34px;font-family:Bangers,cursive;font-size:42px;letter-spacing:.03em;color:#101013;text-align:center;line-height:1.05}
.bl::after{content:'';position:absolute;left:70px;bottom:-22px;border:18px solid transparent;border-top:30px solid #101013;border-bottom:0}
.bum{position:absolute;font-family:Bangers,cursive;color:#DDA94F;-webkit-text-stroke:4px #101013;paint-order:stroke fill;letter-spacing:.04em;white-space:nowrap}
.zz{position:absolute;font-family:Bangers,cursive;font-size:48px;color:#101013}
svg.cena{position:absolute;inset:0;width:100%;height:100%}
svg.cena .ln{stroke:#101013;stroke-width:7;stroke-linejoin:round;stroke-linecap:round}
/* página 2: tira de 3 quadros */
.tira{padding:96px 40px 0;display:flex;flex-direction:column;gap:20px}
.tq{display:flex;align-items:center;gap:20px;padding:16px 22px;transform-origin:left center}
.tq .hr{flex:none;width:200px;font-family:Bangers,cursive;font-size:40px;letter-spacing:.03em}
.tq .t{display:flex;flex-direction:column;gap:2px}
.tq .t b{font-family:Manrope,sans-serif;font-weight:800;font-size:28px}
.tq .t span{font-size:21px;color:#3C4149}
.tq.g .t span{color:#101013}
.tq .ppl{display:flex;gap:8px;margin-left:auto}
.tq .ppl i{width:26px;height:26px;border-radius:50%;background:#101013;border:3px solid #101013;display:block}
/* página 3: fábricas */
.grid{padding:44px 40px 0;display:grid;grid-template-columns:repeat(5,1fr);gap:22px 16px}
.fb{height:54px;border-radius:6px;background:#1E2025;border:4px solid #101013;position:relative;display:flex;align-items:flex-end;justify-content:center;box-shadow:4px 4px 0 #101013}
.fb::before,.fb::after{content:'';position:absolute;top:-20px;width:30px;height:18px;background:#101013;clip-path:polygon(0 100%,0 0,100% 100%)}
.fb::before{left:8px}.fb::after{left:40px}
.fb i{font-style:normal;font-family:Bangers,cursive;font-size:24px;color:#DDA94F;margin-bottom:4px;letter-spacing:.04em}
.fb.nx{background:#FFFFFF;border-style:dashed}
.fb.nx::before,.fb.nx::after{display:none}
.fb.nx i{color:#101013}
.trz{padding:30px 40px 0;display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px}
.trz div{padding:14px 16px;display:flex;flex-direction:column;gap:4px}
.trz small{font-family:Bangers,cursive;font-size:26px;letter-spacing:.05em;color:#A6752D}
.trz b{font-family:Manrope,sans-serif;font-weight:800;font-size:24px;line-height:1.2}
/* página 4: fluxo + comparação */
.flx{padding:46px 34px 0;display:flex;align-items:stretch}
.st4{flex:1;padding:14px 10px;display:flex;flex-direction:column;gap:6px;text-align:center}
.st4 small{font-family:Bangers,cursive;font-size:26px;letter-spacing:.05em}
.st4 b{font-family:Manrope,sans-serif;font-weight:800;font-size:22px;line-height:1.2}
.arw{flex:none;width:46px;display:flex;align-items:center;justify-content:center;font-family:Bangers,cursive;font-size:48px}
.cmp{padding:40px 40px 0;display:flex;flex-direction:column;gap:22px}
.cp .lb{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}
.cp .lb span{font-family:Bangers,cursive;font-size:32px;letter-spacing:.04em}
.cp .lb b{font-family:Bangers,cursive;font-size:50px;letter-spacing:.04em}
.cp .tr{height:52px;border:5px solid #101013;border-radius:8px;background:#FFFFFF;overflow:hidden}
.cp .tr i{display:block;height:100%;background:#3C4149;transform-origin:left center}
.cp.g .tr i{background:#DDA94F;border-right:5px solid #101013}
/* página 5: metas */
.mt{padding:66px 40px 0;display:flex;flex-direction:column;gap:20px}
.mt div{display:flex;align-items:center;gap:20px;padding:14px 20px}
.mt b{flex:none;font-family:Bangers,cursive;font-size:50px;letter-spacing:.03em;min-width:270px}
.mt span{font-size:23px;line-height:1.3;font-weight:600}
.mt div.r b{color:#B91C1C}
.selo{position:absolute;top:18px;left:22px;background:#DDA94F;border:4px solid #101013;font-family:Bangers,cursive;font-size:28px;letter-spacing:.08em;padding:2px 14px;z-index:6;transform:rotate(-4deg)}
/* página 6: CTA em balões */
.ctaw{position:absolute;inset:0}
.kw{position:absolute;left:0;right:0;top:34px;display:flex;flex-direction:column;align-items:center;gap:0}
.kwl{font-family:Bangers,cursive;font-size:34px;letter-spacing:.12em}
.tw{font-family:Bangers,cursive;font-size:104px;letter-spacing:.04em;color:#DDA94F;-webkit-text-stroke:5px #101013;paint-order:stroke fill;white-space:nowrap;overflow:hidden;animation:type 1.1s .7s steps(11) both}
@keyframes type{from{width:0}to{width:6.2em}}
.cb{position:absolute;padding:14px 20px;display:flex;align-items:center;gap:14px}
.cb img,.cb .avg{flex:none;width:54px;height:54px;border-radius:50%;object-fit:cover;border:3px solid #101013;background:#A5A8AE;box-sizing:border-box}
.cb div{display:flex;flex-direction:column;gap:2px}
.cb small{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:17px;color:#3C4149}
.cb span{font-size:24px;font-weight:600;line-height:1.3}
.cb .ty{font-family:Bangers,cursive;font-size:36px;letter-spacing:.04em;color:#A6752D;font-weight:400}
/* animações */
@keyframes inL{from{opacity:0;transform:translateX(-60px)}to{opacity:1;transform:none}}
@keyframes inR{from{opacity:0;transform:translateX(60px)}to{opacity:1;transform:none}}
@keyframes inUp{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{0%{opacity:0;transform:scale(.4)}70%{opacity:1;transform:scale(1.12)}100%{opacity:1;transform:scale(1)}}
@keyframes popr{0%{opacity:0;transform:scale(.4) rotate(-12deg)}70%{opacity:1;transform:scale(1.15) rotate(4deg)}100%{opacity:1;transform:scale(1) rotate(-4deg)}}
@keyframes shake{0%,100%{transform:rotate(-4deg) scale(1)}50%{transform:rotate(3deg) scale(1.06)}}
@keyframes esteira{from{transform:translateX(0)}to{transform:translateX(840px)}}
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
IL = '<span class="il-l">ILUSTRAÇÃO</span>'
def FT(t='P&G (dia do investidor, 19/11), via NYT/PYMNTS · 22/11/2026'):
    return f'<span class="fonte">Fonte: {t}</span>'
def burst(txt, x, y, size, delay, rot=-4):
    return f'<div class="bum" style="left:{x}px;top:{y}px;font-size:{size}px;animation:popr .45s {delay}s both, shake .5s {delay + .5:.2f}s 3 both">{txt}</div>'

PAGS = []
# 1 · capa: a fábrica em quadrinho, a esteira andando sozinha, balão e CLANK
TELHADO = 'M60 360 L60 270 L210 360 Z M210 360 L210 270 L360 360 Z M360 360 L360 270 L510 360 Z'
JANELAS = [(100 + 92 * k, 390, 62, 44) for k in range(8)]
caixas = ''.join(f'<rect x="70" y="494" width="44" height="38" fill="#DDA94F" stroke="#101013" stroke-width="5" style="animation:esteira 4.6s {-k * .92:.2f}s infinite linear"/>' for k in range(5))
fab = (f'<svg class="cena" viewBox="0 0 908 672" style="animation:pop .6s .2s both;transform-origin:50% 70%"><clipPath id="cl"><rect x="64" y="364" width="792" height="212"/></clipPath>'
       f'<path class="ln" d="{TELHADO}" fill="#3C4149"/>'
       '<path class="ln" d="M690 360 L690 240 L726 240 L726 360 Z M760 360 L760 280 L796 280 L796 360 Z" fill="#1E2025"/>'
       '<path class="ln" d="M60 360 L860 360 L860 580 L60 580 Z" fill="#1E2025"/>'
       + ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#101013" stroke="#F4F1EA" stroke-width="3"/>' for x, y, w, h in JANELAS)
       + f'<line x1="90" y1="540" x2="830" y2="540" stroke="#A5A8AE" stroke-width="10" stroke-linecap="round"/><g clip-path="url(#cl)">{caixas}</g></svg>')
cena1 = (fab + f'<div class="bl" style="left:36px;top:36px;animation:pop .5s 1.4s both">22H ÀS 6H (EXEMPLO):<br>0 PESSOAS NA LINHA!</div>'
         + burst('CLANK!', 650, 180, 84, 2.6)
         + f'<div class="zz" style="left:560px;top:100px;animation:fade .4s 3.4s both, shake .9s 3.8s 3">Z z z</div>')
PAGS.append((6.0, page('1/6', 'CURIOSIDADE', TB('A P&amp;G já tem fábricas que trabalham <em>turnos inteiros sem ninguém dentro.</em>') + TP('A dona de Gillette, Pampers e Ariel contou o plano aos investidores. Te conto ↓'),
                       IL + cena1, 'Arraste →')))
# 2 · tira de 3 quadros: manhã, tarde, turno sem gente
def ppl(n): return '<span class="ppl">' + '<i></i>' * n + '</span>' if n else ''
tns = [('06H–14H', '', 'Turno da manhã', 'gente na linha', 3),
       ('14H–22H', '', 'Turno da tarde', 'gente na linha', 3),
       ('HORAS SEGUIDAS', 'g', 'Turno sem gente', 'só as máquinas', 0)]
tira = ''.join(f'<div class="tq qd {c}" {A("inL", .5, .4 + 1.0 * i)}><span class="hr">{h}</span><div class="t"><b>{t}</b><span>{s}</span></div>{ppl(n)}</div>' for i, (h, c, t, s, n) in enumerate(tns))
PAGS.append((6.0, page('2/6', None, TB('1. O que é um <em>"turno no escuro".</em>') + TP('As linhas de produção rodam <b>horas seguidas sem nenhuma pessoa mexendo</b>. O New York Times chama de "dark shift".'),
                       IL + f'<div class="tira">{tira}</div>' + burst('VRRRUM!', 330, 14, 56, 2.9)
                       + f'<div class="leg" style="left:40px;right:40px;bottom:58px;animation:inUp .6s 3.6s both">As pessoas não somem da fábrica: elas param de ficar presas à máquina.</div>' + FT(), 'Arraste →')))
# 3 · mais de 15 fábricas + robôs fora da linha
fbs = ''.join(f'<div class="fb" {A("pop", .35, .4 + .13 * k)}><i>{k + 1:02d}</i></div>' for k in range(15))
fbs += f'<div class="fb nx" {A("pop", .4, 2.5)}><i>+2027</i></div>'
trio = [('DOCAS', 'Robôs carregando'), ('ARMAZÉNS', 'Robôs movendo estoque'), ('ESTRADA', 'Caminhão autônomo em teste')]
tr = ''.join(f'<div class="qd" {A("inUp", .5, 3.2 + .5 * i)}><small>{a}</small><b>{b}</b></div>' for i, (a, b) in enumerate(trio))
PAGS.append((6.0, page('3/6', None, TB('2. Já são <em>mais de 15 fábricas</em> no mundo.') + TP('E a P&amp;G quer mais no ano fiscal de 2027. A automação já saiu da linha e chegou nas docas, no estoque e na estrada.'),
                       IL + f'<div class="grid">{fbs}</div><div class="trz">{tr}</div>' + burst('15+!', 250, 392, 72, 2.8) + FT(), 'Arraste →')))
# 4 · a IA prepara o turno
fl = [('', 'DADOS', 'Produção do dia'), ('g', 'IA', 'Analisa tudo'), ('', 'EQUIPE', 'Chega com o plano')]
flx = ''
for i, (c, a, b) in enumerate(fl):
    if i: flx += f'<span class="arw" {A("fade", .3, .3 + .9 * i)}>➜</span>'
    flx += f'<div class="st4 qd {c}" {A("pop", .5, .6 + .9 * i)}><small>{a}</small><b>{b}</b></div>'
cmp = (f'<div class="cmp"><div class="cp" {A("fade", .3, 3.2)}><div class="lb"><span>ANTES</span><b>HORAS</b></div><div class="tr"><i style="width:100%;animation:grow .8s 3.4s both"></i></div></div>'
       f'<div class="cp g" {A("fade", .3, 4.3)}><div class="lb"><span>COM A IA</span><b style="color:#A6752D">5 MIN</b></div><div class="tr"><i style="width:7%;animation:grow .4s 4.5s both"></i></div></div></div>')
PAGS.append((6.5, page('4/6', None, TB('3. A IA <em>prepara o turno</em> antes de ele começar.') + TP('Na fábrica de Mechelen, na Bélgica, a IA lê os dados de produção antes de cada turno. Segundo a P&amp;G, uma tarefa de horas caiu para 5 minutos.'),
                       f'<div class="flx">{flx}</div>{cmp}' + burst('ZAP!', 400, 452, 60, 4.9) + FT('Luc Reynaert, P&G, via Tech Times · 23/11/2026'), 'Arraste →')))
# 5 · as metas (e o lado das pessoas)
mts = [('', 'ATÉ US$ 10 BI', 'de economia, entre 2027 e 2030'),
       ('', 'ATÉ 20%', 'mais produtividade nas fábricas'),
       ('r', '20% A 30%', 'menos gente em suprimentos até 2030, terceirizados incluídos')]
mt = ''.join(f'<div class="qd {c}" {A("inL", .55, .7 + 1.0 * i)}><b>{a}</b><span>{b}</span></div>' for i, (c, a, b) in enumerate(mts))
PAGS.append((6.0, page('5/6', None, TB('4. O plano: <em>muito dinheiro e menos gente.</em>') + TP('Tudo isso é meta, não resultado. E inclui um corte grande na equipe que cuida da produção e da entrega.'),
                       f'<span class="selo" {A("popr", .45, .2)}>META</span>' + f'<div class="mt">{mt}</div>' + FT('P&G via Tech Times (23/11) e PYMNTS (22/11)'), 'Arraste: falta uma pergunta →')))
# 6 · CTA em balões
cm = (f'<div class="ctaw"><div class="kw" {A("pop", .6, .3)}><span class="kwl">COMENTE</span><b class="tw">DIAGNÓSTICO</b></div>'
      f'<div class="cb qd" style="left:40px;right:120px;top:250px;animation:inL .5s 2.0s both"><i class="avg"></i><div><small>seguidor</small><span class="ty">DIAGNÓSTICO!</span></div></div>'
      f'<div class="cb qd g" style="left:120px;right:40px;top:378px;animation:inR .5s 3.0s both"><img src="{AV}" alt=""><div><small style="color:#101013">lucasgiordane</small><span>Te chamei no direct! 📩</span></div></div>'
      f'<div class="cb qd" style="left:40px;right:40px;top:506px;animation:inUp .5s 4.0s both"><div><small>direct · lucasgiordane</small><span>Oi! Me conta: qual é o seu negócio e o que mais trava hoje?</span></div></div>'
      '</div>')
PAGS.append((7.0, page('6/6', 'SUA VEZ', TB('Que tarefa da sua empresa <em>podia rodar sozinha de madrugada?</em>') + TP('O orçamento, a cobrança, o relatório do dia. <b>Comenta DIAGNÓSTICO</b> que eu te chamo no direct. E salva para não perder.'),
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
