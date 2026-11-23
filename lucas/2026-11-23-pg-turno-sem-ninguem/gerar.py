#!/usr/bin/env python3
"""@lucasgiordane · 23/11/2026 · Modelo 3 CURIOSIDADE: "A P&G já tem fábricas que trabalham turnos inteiros sem ninguém dentro".
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
/* página 1: fábrica no escuro */
.night{position:absolute;inset:0;overflow:hidden}
.moon{position:absolute;right:60px;top:58px;width:70px;height:70px;border-radius:50%;background:#F4F1EA;box-shadow:inset -18px -6px 0 0 #101013}
.st{position:absolute;width:3px;height:3px;border-radius:50%;background:#F5F5F5;opacity:.5}
.fab{position:absolute;left:40px;right:40px;bottom:120px;height:250px}
.fab .bd{position:absolute;left:0;right:0;bottom:0;height:170px;background:#1E2025;border:3px solid #F4F1EA;border-radius:6px 6px 0 0;box-sizing:border-box}
.fab .sh{position:absolute;bottom:167px;width:150px;height:80px;background:#1E2025;border:3px solid #F4F1EA;border-bottom:0;box-sizing:border-box;clip-path:polygon(0 100%,0 0,100% 100%)}
.fab .ch{position:absolute;bottom:167px;width:34px;height:110px;background:#1E2025;border:3px solid #F4F1EA;border-bottom:0;box-sizing:border-box}
.fab .wd{position:absolute;top:36px;width:70px;height:46px;border-radius:4px;background:#2A2D33;border:2px solid #3C4149;box-sizing:border-box}
.belt{position:absolute;left:0;right:0;bottom:22px;height:14px;background:#3C4149;border-radius:7px}
.bx{position:absolute;bottom:36px;width:44px;height:38px;background:#DDA94F;border-radius:4px;border:2px solid #101013;box-sizing:border-box}
.clk{position:absolute;left:40px;top:44px;background:#F4F1EA;color:#101013;border-radius:12px;padding:12px 18px;display:flex;flex-direction:column;gap:2px}
.clk small{font-family:'IBM Plex Mono',monospace;font-size:17px;color:#3C4149;letter-spacing:.04em}
.clk b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:40px}
.zero{position:absolute;left:40px;top:150px;background:#DDA94F;color:#101013;border-radius:10px;padding:10px 16px;font-family:Manrope,sans-serif;font-weight:800;font-size:24px}
.tagbx{position:absolute;right:26px;bottom:24px;background:#F4F1EA;color:#101013;border-radius:10px;padding:12px 18px;display:flex;flex-direction:column;gap:4px}
.tagbx b{font-family:Manrope,sans-serif;font-weight:800;font-size:24px}
.tagbx span{font-family:'IBM Plex Mono',monospace;font-size:17px;color:#3C4149}
/* página 2: as 24 horas */
.dia{padding:30px 44px 0;display:flex;flex-direction:column;gap:22px}
.tn{display:flex;align-items:center;gap:18px}
.tn .hr{flex:none;width:170px;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:26px;color:#F5F5F5}
.tn .bar{flex:1;height:96px;border-radius:12px;background:#F4F1EA;color:#101013;display:flex;align-items:center;gap:14px;padding:0 22px;box-sizing:border-box;transform-origin:left center}
.tn .bar b{font-family:Manrope,sans-serif;font-weight:800;font-size:28px}
.tn .bar span{font-size:22px;color:#3C4149}
.tn .ppl{display:flex;gap:6px;margin-left:auto}
.tn .ppl i{width:22px;height:22px;border-radius:50%;background:#101013;display:block}
.tn.g .bar{background:#DDA94F}
.tn.g .bar span{color:#101013}
.nota{margin:30px 44px 0;font-size:25px;line-height:1.38;color:#F5F5F5;background:#2A2416;border:1px solid #A6752D;border-radius:12px;padding:16px 20px}
.nota b{color:#DDA94F}
/* página 3: 15 fábricas */
.grid{padding:40px 44px 0;display:grid;grid-template-columns:repeat(5,1fr);gap:22px 14px}
.fb{height:56px;border-radius:8px;background:#F4F1EA;position:relative;display:flex;align-items:flex-end;justify-content:center}
.fb::before{content:'';position:absolute;left:12px;top:-14px;width:28px;height:18px;background:#F4F1EA;clip-path:polygon(0 100%,0 0,100% 100%)}
.fb::after{content:'';position:absolute;left:42px;top:-14px;width:28px;height:18px;background:#F4F1EA;clip-path:polygon(0 100%,0 0,100% 100%)}
.fb i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:18px;color:#101013;margin-bottom:8px}
.fb.nx{background:transparent;border:3px dashed #DDA94F;box-sizing:border-box}
.fb.nx::before,.fb.nx::after{display:none}
.fb.nx i{color:#DDA94F}
.trz{padding:26px 44px 0;display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}
.trz div{background:#1E2025;padding:16px;border:2px solid #DDA94F;border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:6px}
.trz small{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:16px;color:#DDA94F;letter-spacing:.06em}
.trz b{font-family:Manrope,sans-serif;font-weight:800;font-size:25px;color:#F5F5F5;line-height:1.2}
/* página 4: a IA antes do turno */
.flx{padding:30px 40px 0;display:flex;align-items:stretch;gap:0}
.st4{flex:1;background:#F4F1EA;color:#101013;border-radius:12px;padding:16px 14px;display:flex;flex-direction:column;gap:6px;text-align:center}
.st4 small{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:16px;color:#A6752D}
.st4 b{font-family:Manrope,sans-serif;font-weight:800;font-size:24px;line-height:1.2}
.st4.g{background:#DDA94F}
.st4.g small{color:#101013}
.arw{flex:none;width:44px;display:flex;align-items:center;justify-content:center;color:#DDA94F;font-size:36px;font-weight:700}
.cmp{padding:34px 40px 0;display:flex;flex-direction:column;gap:26px}
.cp .lb{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px}
.cp .lb span{font-size:25px;color:#F5F5F5}
.cp .lb b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:38px;color:#F4F1EA}
.cp .tr{height:58px;border-radius:10px;background:#2A2D33;overflow:hidden}
.cp .tr i{display:block;height:100%;border-radius:10px;background:#F4F1EA;transform-origin:left center}
.cp.g .lb b{color:#DDA94F}
.cp.g .tr i{background:#DDA94F}
/* página 5: metas */
.mt{padding:44px 40px 0;display:flex;flex-direction:column;gap:16px}
.mt div{display:flex;align-items:center;gap:22px;background:#F4F1EA;color:#101013;border-radius:12px;padding:18px 22px}
.mt b{flex:none;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:36px;min-width:290px}
.mt span{font-size:23px;line-height:1.3;color:#1E2025}
.mt div.rd{border-left:10px solid #EF4444}
.mt div.rd b{color:#B91C1C}
.selo{position:absolute;top:20px;left:26px;background:#DDA94F;color:#101013;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:18px;letter-spacing:.08em;border-radius:4px;padding:4px 10px;z-index:5}
.fab .bd{overflow:hidden}
@keyframes esteira{from{transform:translateX(0)}to{transform:translateX(980px)}}
@keyframes rise2{from{opacity:0;transform:translateY(120px)}to{opacity:1;transform:none}}
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
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:scale(1)}}
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
def FT(t='P&G (dia do investidor, 19/11), via NYT/PYMNTS · 22/11/2026'):
    return f'<span class="fonte" style="z-index:5">Fonte: {t}</span>'
EST = [(6, 12), (18, 30), (31, 8), (44, 22), (57, 14), (70, 6), (83, 30), (93, 16), (12, 40), (38, 36), (64, 34), (50, 4)]
def stars():
    return ''.join(f'<i class="st" style="left:{x}%;top:{y}%"></i>' for x, y in EST)

PAGS = []
# 1 · capa: a fábrica de madrugada, luzes apagadas, a esteira andando sozinha
janelas = ''.join(f'<span class="wd" style="left:{40 + 100 * k}px"></span>' for k in range(8))
caixas = ''.join(f'<span class="bx" style="left:-60px;animation:esteira 5.2s {round(-k * 0.87, 2)}s infinite linear"></span>' for k in range(6))
fab = (f'<div class="fab" {A("rise2", 1.0, .2)}>'
       '<span class="sh" style="left:30px"></span><span class="sh" style="left:180px"></span><span class="sh" style="left:330px"></span>'
       '<span class="ch" style="right:120px;height:120px"></span><span class="ch" style="right:60px;height:90px"></span>'
       f'<div class="bd">{janelas}<span class="belt"></span>{caixas}</div></div>')
cena1 = (f'<div class="night">{stars()}<span class="moon" {A("fade", .8, .1)}></span>{fab}'
         f'<div class="clk" {A("inL", .5, 1.2)}><small>exemplo de turno</small><b class="hora">22:00 → 06:00</b></div>'
         f'<div class="zero" {A("pop", .5, 2.2)}>0 pessoas na linha</div>'
         f'<div class="tagbx" {A("inUp", .6, 3.2)}><b>+15 fábricas</b><span>P&amp;G · nov/2026</span></div></div>')
PAGS.append((6.0, page('1/6', 'CURIOSIDADE', TB('A P&amp;G já tem fábricas que trabalham <em>turnos inteiros sem ninguém dentro.</em>') + TP('A dona de Gillette, Pampers e Ariel contou o plano aos investidores. Te conto ↓'),
                       IL + cena1, 'Arraste →')))
# 2 · o que é um "turno no escuro"
tns = [('06h–14h', '', 'Turno da manhã', 'gente na linha', 3),
       ('14h–22h', '', 'Turno da tarde', 'gente na linha', 3),
       ('horas seguidas', 'g', 'Turno sem gente', 'só as máquinas', 0)]
def ppl(n): return '<span class="ppl">' + '<i></i>' * n + '</span>' if n else ''
dia = ''.join(f'<div class="tn {c}" {A("fade", .3, .4 + 1.0 * i)}><span class="hr">{h}</span><div class="bar" style="animation:grow .7s {.5 + 1.0 * i}s both cubic-bezier(.2,.8,.2,1)"><b>{t}</b><span>{s}</span>{ppl(n)}</div></div>' for i, (h, c, t, s, n) in enumerate(tns))
PAGS.append((6.0, page('2/6', None, TB('1. O que é um <em>"turno no escuro".</em>') + TP('As linhas de produção rodam <b>horas seguidas sem nenhuma pessoa mexendo</b>. O New York Times chama de "dark shift".'),
                       IL + f'<div class="dia">{dia}</div><p class="nota" {A("inUp", .6, 3.6)}>As pessoas não somem da fábrica: <b>elas param de ficar presas à máquina.</b></p>' + FT(), 'Arraste →')))
# 3 · mais de 15 fábricas + robôs fora da linha
fbs = ''.join(f'<div class="fb" {A("pop", .35, .4 + .14 * k)}><i>{k + 1:02d}</i></div>' for k in range(15))
fbs += f'<div class="fb nx" {A("pop", .4, 2.7)}><i>+2027</i></div>'
trio = [('DOCAS', 'Robôs carregando'), ('ARMAZÉNS', 'Robôs movendo estoque'), ('ESTRADA', 'Caminhão autônomo em teste')]
tr = ''.join(f'<div {A("inUp", .5, 3.3 + .5 * i)}><small>{a}</small><b>{b}</b></div>' for i, (a, b) in enumerate(trio))
PAGS.append((6.0, page('3/6', None, TB('2. Já são <em>mais de 15 fábricas</em> no mundo.') + TP('E a P&amp;G quer mais no ano fiscal de 2027. A automação já saiu da linha e chegou nas docas, no estoque e na estrada.'),
                       IL + f'<div class="grid">{fbs}</div><div class="trz">{tr}</div>' + FT(), 'Arraste →')))
# 4 · a IA prepara o turno
fl = [('', 'DADOS', 'Produção do dia'), ('g', 'IA', 'Analisa tudo'), ('', 'EQUIPE', 'Chega com o plano')]
flx = ''
for i, (c, a, b) in enumerate(fl):
    if i: flx += f'<span class="arw" {A("fade", .3, .6 + .9 * i - .3)}>→</span>'
    flx += f'<div class="st4 {c}" {A("pop", .5, .6 + .9 * i)}><small>{a}</small><b>{b}</b></div>'
cmp = (f'<div class="cmp"><div class="cp" {A("fade", .3, 3.2)}><div class="lb"><span>Antes</span><b>horas</b></div><div class="tr"><i style="width:100%;animation:grow .8s 3.4s both"></i></div></div>'
       f'<div class="cp g" {A("fade", .3, 4.3)}><div class="lb"><span>Com a IA</span><b>5 min</b></div><div class="tr"><i style="width:6%;animation:grow .4s 4.5s both"></i></div></div></div>')
PAGS.append((6.5, page('4/6', None, TB('3. A IA <em>prepara o turno</em> antes de ele começar.') + TP('Na fábrica de Mechelen, na Bélgica, a IA lê os dados de produção antes de cada turno. Segundo a P&amp;G, uma tarefa de horas caiu para 5 minutos.'),
                       f'<div class="flx">{flx}</div>{cmp}' + FT('Luc Reynaert, P&G, via Tech Times · 23/11/2026'), 'Arraste →')))
# 5 · as metas (e o lado das pessoas)
mts = [('', 'até US$ 10 bi', 'de economia, entre 2027 e 2030'),
       ('', 'até 20%', 'mais produtividade nas fábricas'),
       ('rd', '20% a 30%', 'menos gente em suprimentos até 2030, terceirizados incluídos')]
mt = ''.join(f'<div class="{c}" {A("inL", .55, .7 + 1.0 * i)}><b>{a}</b><span>{b}</span></div>' for i, (c, a, b) in enumerate(mts))
PAGS.append((6.0, page('5/6', None, TB('4. O plano: <em>muito dinheiro e menos gente.</em>') + TP('Tudo isso é meta, não resultado. E inclui um corte grande na equipe que cuida da produção e da entrega.'),
                       '<span class="selo">META</span>' + f'<div class="mt">{mt}</div>' + FT('P&G via Tech Times (23/11) e PYMNTS (22/11)'), 'Arraste: falta uma pergunta →')))
# 6 · CTA
cm = (f'<div class="ctaw"><div class="kw" {A("pop", .6, .4)}><span class="kwl">comente</span><b class="tw">DIAGNÓSTICO</b></div>'
      f'<div class="cm" {A("inUp", .6, 2.0)}><i class="avg"></i><div><b>seguidor</b><span class="ty">DIAGNÓSTICO</span></div><em {A("pop", .4, 2.6)}>♥</em></div>'
      f'<div class="cm me" {A("inUp", .6, 3.1)}><img src="{AV}" alt=""><div><b>lucasgiordane</b><span>Te chamei no direct! 📩</span></div></div>'
      f'<div class="dm" {A("inUp", .6, 4.2)}><small>direct · lucasgiordane</small><span>Oi! Me conta: qual é o seu negócio e o que mais trava hoje?</span></div></div>')
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
