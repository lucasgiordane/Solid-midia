#!/usr/bin/env python3
"""Post-card animado v2 (carrossel de segunda, 5 páginas em MP4 1080x1350).
Uso: python3 -I anima2.py <saida> <solid26.css> <blobs> <fontes> [páginas, ex.: 1,4]"""
import os, sys, base64, glob, subprocess, shutil
from playwright.sync_api import sync_playwright
OUT, CSSF, BLOBS, FONTES = sys.argv[1:5]
SO = [int(x) for x in sys.argv[5].split(',')] if len(sys.argv) > 5 else None
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
SIM = 'data:image/svg+xml;base64,' + b64(glob.glob(os.path.join(BLOBS, 'a0000000000000000000000000000001.*'))[0])

CSS = open(CSSF).read() + """
.pc .mi{padding:40px 36px;justify-content:center}
/* fluxo: blocos marfim, texto preto, setas douradas */
.mv .flw{gap:6px;align-items:stretch}
.mv .nd{background:#F4F1EA;border:0;min-height:150px;border-radius:14px;position:relative;padding:12px 4px}
.mv .nd b{color:#101013;font-size:19px;letter-spacing:-0.01em;line-height:1.15}
.mv .nd small{color:#3C4149;font-size:14px;font-weight:500}
.mv .nd.on{background:#DDA94F}
.mv .ar{align-self:center;width:18px;height:4px;background:#DDA94F;border-radius:2px;flex-shrink:0;transform-origin:left center;position:relative}
.mv .ar::after{content:"";position:absolute;right:-2px;top:-6px;border-left:9px solid #DDA94F;border-top:8px solid transparent;border-bottom:8px solid transparent}
.mv .flw-cap{font-size:30px;color:#F5F5F5;margin-top:30px}.mv .flw-cap b{color:#DDA94F}
.mv.small .nd{min-height:108px}
.strike{position:absolute;left:8%;right:8%;top:50%;height:4px;background:#F59E0B;transform-origin:left center}
/* página 1: 4 blocos do mesmo tamanho */
.g4{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:170px;gap:18px}
.g4 div{background:#F4F1EA;border-radius:14px;display:flex;align-items:center;gap:20px;padding:0 28px}
.g4 div b{flex:none;width:64px;height:64px;border-radius:12px;background:#101013;color:#DDA94F;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:34px}
.g4 div span{font-family:Manrope,sans-serif;font-weight:700;font-size:30px;line-height:1.2;color:#101013}
/* página 4: agente */
.ag{margin-top:26px;background:#1E2025;border:1px solid #3C4149;border-radius:14px;padding:22px 26px}
.ag .h{display:flex;align-items:center;justify-content:space-between;padding-bottom:14px;border-bottom:1px solid #3C4149;margin-bottom:6px}
.ag .h b{font-family:Manrope,sans-serif;font-weight:700;font-size:26px;color:#F5F5F5}
.ag .st{display:inline-flex;align-items:center;gap:8px;font-family:'IBM Plex Mono',monospace;font-size:17px;color:#A78BFA;border:1.5px solid #A78BFA;border-radius:6px;padding:4px 10px}
.ag .st i{width:10px;height:10px;border-radius:50%;background:#A78BFA;display:block}
.ag .r{display:flex;align-items:center;gap:16px;padding:13px 0;border-bottom:1px solid #2A2D33}
.ag .r:last-child{border-bottom:0}
.ag .r span{font-size:24px;color:#F5F5F5;flex:1}
.ag .r em{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#22C55E;border:1.5px solid #22C55E;border-radius:6px;padding:3px 8px}
.ag .r .n{flex:none;width:34px;height:34px;border-radius:50%;background:#DDA94F;color:#101013;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:18px}
.sel{position:absolute;left:-6px;right:-6px;top:-6px;bottom:-6px;border:3px solid #DDA94F;border-radius:18px}
.tagsel{position:absolute;left:50%;bottom:-40px;transform:translateX(-50%);white-space:nowrap;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#DDA94F}
/* página 5: painel */
.db{background:#F4F1EA;border-radius:14px;padding:24px 26px;color:#101013}
.db .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}
.db .top b{font-family:Manrope,sans-serif;font-weight:800;font-size:25px}
.db .top span{font-family:'IBM Plex Mono',monospace;font-size:16px;color:#3C4149}
.db .ks{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.db .k{background:#FFFFFF;border:1px solid #E2DCCF;border-radius:12px;padding:16px 16px 14px}
.db .k small{display:block;font-size:17px;color:#3C4149;line-height:1.25;min-height:44px}
.db .k .v{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:44px;letter-spacing:-0.03em;margin-top:6px}
.db .k .ant{font-family:'IBM Plex Mono',monospace;font-size:16px;color:#3C4149;margin-top:4px}
.db .k .d{display:inline-block;margin-top:10px;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:16px;color:#FFFFFF;background:#15803D;border-radius:5px;padding:3px 8px}
.db .ch{margin-top:18px;background:#FFFFFF;border:1px solid #E2DCCF;border-radius:12px;padding:16px 18px 10px}
.db .ch small{font-size:17px;color:#3C4149}
.db .bars{display:flex;align-items:flex-end;gap:14px;height:150px;margin-top:10px;position:relative}
.db .bars div{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:6px}
.db .bars i{display:block;width:100%;border-radius:5px 5px 0 0;background:#3C4149;transform-origin:bottom}
.db .bars i.g{background:#DDA94F}
.db .bars span{font-family:'IBM Plex Mono',monospace;font-size:13px;color:#3C4149}
.db .bars .mk{position:absolute;top:-4px;bottom:22px;width:0;border-left:2px dashed #A6752D}
.db .bars .mkt{position:absolute;top:-6px;font-family:'IBM Plex Mono',monospace;font-size:14px;color:#A6752D;background:#FFFFFF;padding:0 4px}
/* página 6: CTA */
.cws{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.cw{background:#F4F1EA;border-radius:14px;padding:20px 22px;display:flex;flex-direction:column;gap:6px}
.cw b{font-family:Manrope,sans-serif;font-weight:800;font-size:34px;color:#101013}
.cw small{font-size:20px;color:#3C4149}
.cm{margin-top:22px;display:flex;align-items:center;gap:16px;background:#1E2025;border:1px solid #3C4149;border-radius:14px;padding:14px 18px}
.cm img{width:52px;height:52px;border-radius:50%;object-fit:cover}
.cm div{display:flex;flex-direction:column;gap:2px;flex:1}
.cm b{font-family:Inter,sans-serif;font-weight:600;font-size:19px;color:#A5A8AE}
.cm span{font-size:24px;color:#F5F5F5}
.cm .ty{font-family:'IBM Plex Mono',monospace;font-weight:600;color:#DDA94F;font-size:28px}
.cm .ty i{font-style:normal;color:#F5F5F5}
.cm em{font-style:normal;color:#EF4444;font-size:28px}
.cm.me{margin-top:12px;margin-left:60px}
.cm .avg{flex:none;width:52px;height:52px;border-radius:50%;background:#3C4149;display:block}
.kw{display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:8px}
.kwl{font-family:Inter,sans-serif;font-weight:600;font-size:22px;letter-spacing:.24em;color:#A5A8AE;text-transform:uppercase}
.tw{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:72px;color:#DDA94F;letter-spacing:.02em;white-space:nowrap;overflow:hidden;border-right:5px solid #DDA94F;animation:type 1.1s .7s steps(11) both, caret .6s 1.8s 3 both}
@keyframes type{from{width:0}to{width:11.6ch}}
@keyframes caret{50%{border-color:transparent}}
.dm{margin-top:14px;margin-left:60px;background:#2A2416;border:1px solid #A6752D;border-radius:14px 14px 4px 14px;padding:14px 18px;display:flex;flex-direction:column;gap:4px}
.dm small{font-family:'IBM Plex Mono',monospace;font-size:15px;color:#DDA94F}
.dm span{font-size:23px;color:#F5F5F5;line-height:1.35}
/* animações */
@keyframes inL{from{opacity:0;transform:translateX(-50px)}to{opacity:1;transform:none}}
@keyframes inUp{from{opacity:0;transform:translateY(36px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes growY{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{0%{opacity:0;transform:scale(.7)}70%{opacity:1;transform:scale(1.05)}100%{opacity:1;transform:scale(1)}}
@keyframes flip{0%{opacity:0;transform:perspective(800px) rotateX(-80deg) translateY(20px)}100%{opacity:1;transform:none}}
@keyframes shake{0%,100%{transform:none}20%{transform:translateX(-8px)}40%{transform:translateX(8px)}60%{transform:translateX(-6px)}80%{transform:translateX(6px)}}
@keyframes vanish{from{opacity:1;max-width:300px}to{opacity:0;max-width:0;padding-left:0;padding-right:0;margin:0 -6px}}
@keyframes goldfill{from{background:#F4F1EA}to{background:#DDA94F}}
@keyframes blink{0%,100%{opacity:0}30%,70%{opacity:1}}
"""
def A(name, dur, delay, ease='cubic-bezier(.2,.8,.2,1)'):
    return f'style="animation:{name} {dur}s {delay}s both {ease}"'
def page(pg, tag, texto, media, rodape, cls=''):
    tg = f'<span class="tg">{tag}</span>' if tag else ''
    return f'''<div class="pc mv {cls}">
<div class="au2"><img class="av" src="{AV}" alt=""><div class="nm"><b>Lucas Giordane <img src="{SIM}" alt=""></b><span>@lucasgiordane</span></div></div>
<span class="pg">{pg}</span>
<div class="tx">{tg}{texto}</div>
<div class="mi">{media}</div>
<div class="lg"><span>{rodape}</span><i>SOLID BUSINESS</i></div>
</div>'''
TP = lambda x: f'<p class="tp">{x}</p>'
TB = lambda x: f'<p class="tb">{x}</p>'
IL = '<span class="il-l">ILUSTRAÇÃO</span>'
EX = '<span class="il-l">EXEMPLO</span>'
SEIS = [('Pedido', 'WhatsApp'), ('Planilha extra', 'cópia do pedido'), ('Orçamento', 'manual'), ('Pagamento', 'Pix ou cartão'), ('Produção', 'equipe'), ('Entrega', 'cliente')]
CINCO = [SEIS[0]] + SEIS[2:]

def fluxo(nos, nd_attr, ar_attr):
    h = []
    for k, (t, s) in enumerate(nos):
        if k: h.append(f'<span class="ar" {ar_attr(k)}></span>')
        h.append(f'<div class="nd" {nd_attr(k)}><b>{t}</b><small>{s}</small></div>')
    return '<div class="flw">' + ''.join(h) + '</div>'

PAGS = []
# 1 · os 4 passos entram um por vez, do mesmo tamanho
itens = ['Desenhe o caminho', 'Corte o que sobra', 'Automatize o que se repete', 'Meça com um número']
g = ''.join(f'<div {A("flip", .6, .5 + .9 * i)}><b>{i + 1}</b><span>{t}</span></div>' for i, t in enumerate(itens))
PAGS.append((6.0, page('1/6', 'NA PRÁTICA', TP('Quase todo dono de negócio começa a IA pelo lado errado: <b>pela ferramenta.</b>') + TB('A ordem que funciona tem 4 passos. ↓'),
                       IL + f'<div class="g4">{g}</div>', 'Arraste →')))
# 2 · o caminho como ele é hoje, com a planilha extra, entra bloco por bloco
f2 = fluxo(SEIS, lambda k: A('inL', .5, .4 + .55 * k), lambda k: A('grow', .3, .25 + .55 * k))
PAGS.append((6.0, page('2/6', None, TB('1. Desenhe o caminho do pedido à entrega, <em>como ele é hoje.</em>') + TP('Se só existe na sua cabeça, nenhuma ferramenta consegue seguir.'),
                       IL + f2 + f'<p class="flw-cap" {A("inUp", .6, 4.0)}>Seis passos. <b>Agora dá para enxergar.</b></p>', 'Primeiro o processo, depois a IA')))
# 3 · começa com os mesmos seis; a planilha treme, é riscada e sai
def nd3(k):
    return 'style="animation:shake .5s 0.9s both, vanish .7s 2.3s both cubic-bezier(.2,.8,.2,1)"' if k == 1 else ''
def ar3(k):
    return 'style="animation:vanish .7s 2.3s both cubic-bezier(.2,.8,.2,1)"' if k == 1 else ''
f3 = fluxo(SEIS, nd3, ar3).replace('<small>cópia do pedido</small>', f'<small>cópia do pedido</small><span class="strike" {A("grow", .4, 1.6)}></span>')
PAGS.append((6.0, page('3/6', None, TB('2. Corte o que ninguém usa <em>antes</em> de automatizar.') + TP('A planilha que copia o pedido só existe porque sempre existiu.'),
                       IL + f3 + f'<p class="flw-cap" {A("inUp", .6, 3.2)}>Cinco passos. <b>Automatizar desperdício só o deixa mais rápido.</b></p>', 'Primeiro o processo, depois a IA')))
# 4 · escolhe o passo que se repete e mostra o agente trabalhando
def nd4(k):
    if k == 1:
        return 'style="animation:goldfill .5s 1.6s both"'
    return ''
f4 = fluxo(CINCO, nd4, lambda k: '')
f4 = f4.replace('<small>manual</small>', f'<small>se repete todo dia</small><span class="sel" {A("pop", .5, 1.2)}></span>', 1)
passos = [('Recebe o pedido no WhatsApp', 2.8), ('Pergunta quantidade, cidade e prazo', 3.6), ('Calcula pela sua tabela de preços', 4.4), ('Monta a proposta e manda para você aprovar', 5.2)]
rows = ''.join(f'<div class="r" {A("inL", .5, t)}><span class="n">{i + 1}</span><span>{s}</span><em {A("pop", .4, t + .5)}>feito</em></div>' for i, (s, t) in enumerate(passos))
ag = f'<div class="ag" {A("inUp", .6, 2.2)}><div class="h"><b>Agente de orçamento</b><span class="st"><i></i>IA ativa</span></div>{rows}</div>'
PAGS.append((8.0, page('4/6', None, TB('3. Escolha o passo que <em>se repete todo dia</em> e entregue para um agente.') + TP('Você só aprova. O resto ele faz.'),
                       IL + f4 + ag, 'Primeiro o processo, depois a IA', 'small')))
# 5 · painel comparativo antes x depois
ks = [('Tempo até a primeira resposta', '5 min', 'antes: 4 h', '▼ 98%'), ('Orçamentos respondidos no mesmo dia', '100%', 'antes: 52%', '▲ 48 p.p.'), ('Orçamentos que viraram venda', '27%', 'antes: 18%', '▲ 9 p.p.')]
kh = ''.join(f'<div class="k" {A("inUp", .5, .5 + .5 * i)}><small>{a}</small><div class="v">{v}</div><div class="ant">{an}</div><span class="d" {A("pop", .4, 1.1 + .5 * i)}>{d}</span></div>' for i, (a, v, an, d) in enumerate(ks))
alturas = [92, 88, 95, 90, 30, 12, 8, 6]
bars = ''.join(f'<div><i class="{"g" if k >= 4 else ""}" style="height:{h}%;animation:growY .45s {2.2 + .18 * k}s both cubic-bezier(.2,.8,.2,1)"></i><span>S{k + 1}</span></div>' for k, h in enumerate(alturas))
bars += f'<span class="mk" style="left:calc(50% - 7px);animation:fade .4s 3.3s both"></span><span class="mkt" style="left:calc(50% + 2px);animation:fade .4s 3.3s both">automação ligada</span>'
db = (f'<div class="db" {A("fade", .4, .2)}><div class="top"><b>Painel · Orçamentos</b><span>antes × 30 dias depois · exemplo</span></div>'
      f'<div class="ks">{kh}</div><div class="ch" {A("inUp", .5, 1.9)}><small>Tempo até a primeira resposta, por semana</small><div class="bars">{bars}</div></div></div>')
PAGS.append((7.0, page('5/6', None, TB('4. Meça antes e depois, <em>com números.</em>') + TP('Se não melhorou, ajuste antes de seguir. Se melhorou, vai para o próximo processo.'),
                       db, 'Arraste: falta uma pergunta para você →')))
# 6 · CTA: comentar uma palavra
cm = (f'<div class="kw" {A("pop", .6, .4)}><span class="kwl">comente</span><b class="tw">DIAGNÓSTICO</b></div>'
      f'<div class="cm" {A("inUp", .6, 2.0)}><i class="avg"></i><div><b>seguidor</b><span class="ty">DIAGNÓSTICO</span></div><em {A("pop", .4, 2.6)}>♥</em></div>'
      f'<div class="cm me" {A("inUp", .6, 3.1)}><img src="{AV}" alt=""><div><b>lucasgiordane</b><span>Te chamei no direct! 📩</span></div></div>'
      f'<div class="dm" {A("inUp", .6, 4.2)}><small>direct · lucasgiordane</small><span>Oi! Me conta: qual é o seu negócio e o que mais trava hoje? Eu olho com você.</span></div>')
PAGS.append((7.0, page('6/6', 'SUA VEZ', TB('Quer saber por onde começar no seu negócio?') + TP('<b>Comenta DIAGNÓSTICO</b> que eu te chamo no direct.'),
                       cm, 'Comenta DIAGNÓSTICO ↓')))

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pgw = br.new_page(viewport={'width': 1080, 'height': 1350})
    for i, (dur, body) in enumerate(PAGS, 1):
        if SO and i not in SO: continue
        pgw.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{"".join(faces)}{CSS}html,body{{margin:0;width:1080px;height:1350px;overflow:hidden}}</style></head><body>{body}</body></html>')
        pgw.evaluate('document.fonts.ready')
        fr = os.path.join(OUT, f'f{i}'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
        n = int(FPS * dur)
        for f in range(n):
            pgw.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {f * 1000 / FPS}; }})')
            pgw.screenshot(path=os.path.join(fr, f'{f:04d}.png'))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(fr, '%04d.png'),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', os.path.join(OUT, f'slide-{i:02d}.mp4')], check=True)
    br.close()
print('ok')
