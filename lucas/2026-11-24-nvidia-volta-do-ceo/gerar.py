#!/usr/bin/env python3
"""@lucasgiordane · 24/11/2026 · Modelo 1 É OFICIAL: "A Nvidia tirou o CEO e trouxe de volta 11 dias depois".
Uso: python3 -I gerar.py <saida> <solid26.css> <blobs> <fontes> png|mp4 [páginas, ex.: 1,4]
Fontes: comunicado da Nvidia no 8-K da SEC (23/11/2026); fechamento da ação: The Nation (Dow Jones Market Data), 23/11/2026."""
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
.pc .av{width:116px;height:116px;border:0}
.pc .nm b{font-size:44px;letter-spacing:-0.01em}
.pc .nm span{font-size:32px;color:#5B6070}
.pc .pg{top:110px}
.pc .tx{margin-top:24px;gap:22px;flex:1;justify-content:center}
.pc .tp{font-size:36px;line-height:1.36;color:#1E2025}
.pc .tp b{color:#101013}
.pc .tb{font-size:46px}
/* caixa do vídeo com o mesmo tamanho e a mesma posição em todas as páginas (decisão do Lucas em 25/11/2026) */
.pc .mi{flex:none;height:660px;min-height:0;margin-top:24px;padding:0}
.fonte{position:absolute;left:26px;bottom:18px;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#A5A8AE}
.il-l{position:absolute;right:20px;top:18px;font-family:'IBM Plex Mono',monospace;font-size:16px;letter-spacing:.12em;color:#101013;background:#DDA94F;border-radius:4px;padding:4px 10px}
.wrap{position:absolute;inset:0;padding:44px 44px 56px;display:flex;flex-direction:column;justify-content:center;gap:22px}
/* capa: cartão da notícia */
.news{background:#F4F1EA;color:#101013;border-radius:14px;padding:24px 28px;display:flex;flex-direction:column;gap:10px;border-left:10px solid #DDA94F}
.news small{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:19px;color:#A6752D;letter-spacing:.05em}
.news b{font-family:Manrope,sans-serif;font-weight:800;font-size:33px;line-height:1.2}
.news span{font-size:21px;color:#3C4149;line-height:1.3}
.bign{display:flex;align-items:center;gap:26px;padding:4px 4px 0}
.bign b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:108px;color:#DDA94F;line-height:1}
.bign span{font-size:25px;line-height:1.3;color:#F5F5F5}
.bign span em{font-style:normal;color:#DDA94F;font-weight:600}
/* linha do tempo */
.tl{display:flex;flex-direction:column;gap:18px;position:relative}
.tl .lnv{position:absolute;left:35px;top:30px;bottom:30px;width:4px;background:#A6752D;transform-origin:top center}
.ev{display:flex;gap:22px;align-items:center;position:relative}
.ev .dt{flex:none;width:74px;height:74px;border-radius:50%;background:#1E2025;border:4px solid #DDA94F;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:20px;color:#DDA94F;box-sizing:border-box}
.ev .dt.ok{background:#DDA94F;color:#101013}
.ev .cd{flex:1;background:#F4F1EA;border-radius:12px;padding:14px 20px;color:#101013}
.ev .cd b{display:block;font-family:Manrope,sans-serif;font-weight:800;font-size:27px}
.ev .cd span{display:block;font-size:20px;color:#3C4149;margin-top:4px;line-height:1.3}
.cnt{align-self:flex-start;margin-left:96px;background:#DDA94F;color:#101013;border-radius:10px;padding:10px 18px;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:24px}
/* barras */
.br .lb{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}
.br .lb span{font-size:26px;color:#F5F5F5}
.br .lb b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:42px;color:#F4F1EA}
.br .tr{height:66px;border-radius:10px;background:#2A2D33;overflow:hidden}
.br .tr i{display:block;height:100%;border-radius:10px;background:#F4F1EA;transform-origin:left center}
.br.g .lb b{color:#DDA94F}
.br.g .tr i{background:#DDA94F}
.chips{display:flex;gap:14px}
.chip{flex:1;background:#F4F1EA;color:#101013;border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;gap:4px}
.chip b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:36px;color:#101013}
.chip span{font-size:19px;color:#3C4149;line-height:1.3}
.chip.g{background:#DDA94F}
.chip.g span{color:#101013}
/* cartões do que muda */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.card{background:#F4F1EA;color:#101013;border-radius:12px;padding:20px 20px 22px;display:flex;flex-direction:column;gap:10px;border-top:8px solid #DDA94F}
.card i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:18px;color:#A6752D;letter-spacing:.06em}
.card b{font-family:Manrope,sans-serif;font-weight:800;font-size:26px;line-height:1.22}
.card span{font-size:19px;color:#3C4149;line-height:1.3}
/* checklist do seu negócio */
.q{display:flex;gap:18px;align-items:center;background:#F4F1EA;color:#101013;border-radius:12px;padding:15px 20px}
.q .bx i{font-style:normal}
.q .bx{flex:none;width:44px;height:44px;border-radius:8px;border:4px solid #101013;box-sizing:border-box;display:flex;align-items:center;justify-content:center;font-family:Manrope,sans-serif;font-weight:800;font-size:30px;color:#EF4444;line-height:1}
.q b{display:block;font-family:Manrope,sans-serif;font-weight:800;font-size:26px;line-height:1.22}
.q div{line-height:1.2}
.q span{display:block;font-size:19px;color:#3C4149;margin-top:2px}
.cap{font-size:24px;line-height:1.32;color:#F5F5F5;background:#2A2416;border:1px solid #A6752D;border-radius:12px;padding:16px 20px}
.cap b{color:#DDA94F}
/* CTA */
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
@keyframes inL{from{opacity:0;transform:translateX(-50px)}to{opacity:1;transform:none}}
@keyframes inR{from{opacity:0;transform:translateX(50px)}to{opacity:1;transform:none}}
@keyframes inUp{from{opacity:0;transform:translateY(36px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes growY{from{transform:scaleY(0)}to{transform:scaleY(1)}}
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
F8K = '<span class="fonte">Fonte: comunicado da Nvidia (8-K, SEC) · 23/11/2026</span>'
FAC = '<span class="fonte">Fonte: Dow Jones Market Data, via The Nation · 23/11/2026</span>'

PAGS = []
# 1 · capa: cartão da notícia + número grande
capa = (f'<div class="wrap"><div class="news" {A("inUp", .6, .3)}><small>NVIDIA · COMUNICADO OFICIAL · 23/11/2026</small>'
        f'<b>Conselho reconduz Jensen Huang como presidente e CEO</b><span>Decisão unânime, com efeito imediato.</span></div>'
        f'<div class="bign"><b {A("pop", .6, 1.4)}>+31%</b><span {A("fade", .6, 2.0)}>foi quanto a ação subiu no mesmo dia: <em>cerca de US$ 952 bilhões</em> a mais em valor de mercado.</span></div></div>'
        f'<span class="fonte">Fontes: Nvidia (8-K) e Dow Jones Market Data, via The Nation · 23/11/2026</span>')
PAGS.append((6.0, page('1/6', 'É OFICIAL', TB('A Nvidia perdeu o CEO. <em>11 dias depois, trouxe de volta.</em>') + TP('E a gigante dos chips de IA ganhou quase um trilhão de dólares num dia. Te conto ↓'),
                       capa, 'Arraste →')))
# 2 · linha do tempo
evs = [('12/11', '', 'Nvidia anuncia a saída de Huang', 'Depois de 33 anos no comando. A CFO, Colette Kress, vira CEO interina.'),
       ('20/11', '', 'Ação fecha a US$ 125,53', 'Fim de uma semana de forte queda.'),
       ('23/11', 'ok', 'Conselho vota pela volta', 'Por unanimidade, com efeito imediato.')]
tl = ''.join(f'<div class="ev" {A("inL", .55, .6 + 1.1 * i)}><span class="dt {c}">{d}</span><div class="cd"><b>{t}</b><span>{s}</span></div></div>' for i, (d, c, t, s) in enumerate(evs))
PAGS.append((6.0, page('2/6', None, TB('1. Tudo aconteceu <em>em 11 dias.</em>') + TP('A gigante dos chips de IA ficou sem o cofundador e voltou atrás.'),
                       f'<div class="wrap"><div class="tl"><span class="lnv" {A("growY", 2.4, .4, "linear")}></span>{tl}</div><span class="cnt" {A("pop", .5, 4.0)}>11 dias</span></div>'
                       '<span class="fonte">Fontes: Nvidia (8-K) e The Nation · 12 a 23/11/2026</span>', 'Arraste →')))
# 3 · o mercado
barras = (f'<div class="wrap"><div class="br" {A("fade", .4, .3)}><div class="lb"><span>Fechamento em 20/11</span><b>US$ 125,53</b></div><div class="tr"><i style="width:76%;animation:grow .8s .6s both"></i></div></div>'
          f'<div class="br g" {A("fade", .4, 1.6)}><div class="lb"><span>Fechamento em 23/11</span><b>US$ 165,05</b></div><div class="tr"><i style="width:100%;animation:grow 1.2s 1.9s both cubic-bezier(.2,.8,.2,1)"></i></div></div>'
          f'<div class="chips"><div class="chip g" {A("pop", .5, 3.3)}><b>+31,48%</b><span>maior alta num dia desde maio de 2003</span></div>'
          f'<div class="chip" {A("pop", .5, 3.9)}><b>US$ 952 bi</b><span>a mais em valor de mercado, num dia</span></div></div></div>' + FAC)
PAGS.append((6.0, page('3/6', None, TB('2. O mercado respondeu <em>no mesmo dia.</em>') + TP('Uma decisão do conselho valeu quase um trilhão de dólares em poucas horas.'),
                       barras, 'Arraste →')))
# 4 · o que muda
cards = [('VOLTA', 'Huang reassume', 'Presidente, CEO e membro do conselho.'),
         ('CFO', 'Kress volta ao cargo', 'Deixa de ser CEO interina e segue como diretora financeira.'),
         ('CONTINUA', 'A investigação segue', 'Comitê só de conselheiros independentes, com advogados de fora.'),
         ('NOVO', 'Mais controle', 'Comitê de segurança nacional e exportação e um diretor de compliance.')]
cd = ''.join(f'<div class="card" {A("pop", .5, .5 + .7 * i)}><i>{a}</i><b>{b}</b><span>{c}</span></div>' for i, (a, b, c) in enumerate(cards))
PAGS.append((6.0, page('4/6', None, TB('3. O que muda <em>a partir de agora.</em>') + TP('A volta veio com condições, segundo o próprio comunicado da Nvidia.'),
                       f'<div class="wrap"><div class="grid">{cd}</div></div>' + F8K, 'Arraste →')))
# 5 · e no seu negócio
qs = [('Quem aprova os pagamentos?', 'Se só você aprova, o caixa para.'),
      ('Quem atende o cliente grande?', 'Se só você conhece, ele vai embora.'),
      ('Onde estão as senhas e contratos?', 'Se só você sabe, ninguém acha.'),
      ('Quem decide o preço?', 'Se está só na sua cabeça, cada um cobra um valor.')]
ql = ''.join(f'<div class="q" {A("inL", .5, .5 + .8 * i)}><span class="bx"><i {A("pop", .3, .9 + .8 * i)}>?</i></span><div><b>{a}</b><span>{b}</span></div></div>' for i, (a, b) in enumerate(qs))
PAGS.append((6.5, page('5/6', None, TB('4. A lição serve <em>para qualquer empresa.</em>') + TP('Quando tudo depende de uma pessoa, a empresa inteira balança junto. Faz o teste:'),
                       IL + f'<div class="wrap" style="padding:58px 44px 52px;gap:14px">{ql}<p class="cap" {A("inUp", .5, 4.2)}>Se você sumisse 11 dias, <b>quantas dessas teriam resposta?</b></p></div>', 'Arraste: falta uma pergunta →')))
# 6 · CTA
cm = (f'<div class="ctaw"><div class="kw" {A("pop", .6, .4)}><span class="kwl">comente</span><b class="tw">DIAGNÓSTICO</b></div>'
      f'<div class="cm" {A("inUp", .6, 2.0)}><i class="avg"></i><div><b>seguidor</b><span class="ty">DIAGNÓSTICO</span></div><em {A("pop", .4, 2.6)}>♥</em></div>'
      f'<div class="cm me" {A("inUp", .6, 3.1)}><img src="{AV}" alt=""><div><b>lucasgiordane</b><span>Te chamei no direct! 📩</span></div></div>'
      f'<div class="dm" {A("inUp", .6, 4.2)}><small>direct · lucasgiordane</small><span>Oi! Me conta: qual é o seu negócio e o que mais trava hoje?</span></div></div>')
PAGS.append((7.0, page('6/6', 'SUA VEZ', TB('Se você ficasse 11 dias fora, <em>sua empresa aguentava?</em>') + TP('<b>Comenta DIAGNÓSTICO</b> que eu te chamo no direct e a gente olha o seu caso. E salva para não perder.'),
                       cm, 'Comenta DIAGNÓSTICO ↓')))

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pgw = br.new_page(viewport={'width': 1080, 'height': 1350})
    for i, (dur, body) in enumerate(PAGS, 1):
        if SO and i not in SO: continue
        pgw.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{"".join(faces)}{CSS}html,body{{margin:0;width:1080px;height:1350px;overflow:hidden}}</style></head><body>{body}</body></html>')
        pgw.evaluate('document.fonts.ready')
        if MODO == 'medir':
            print(i, pgw.evaluate("[document.querySelector('.mi').offsetHeight, Math.round(document.querySelector('.tx').getBoundingClientRect().bottom)]"))
            continue
        if MODO == 'png':
            pgw.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {dur * 1000 - 1}; }})')
            pgw.screenshot(path=os.path.join(OUT, f'slide-{i:02d}.png'))
            continue
        fr = os.path.join(OUT, f'f{i}'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
        n = int(FPS * dur)
        for f in range(n):
            # capa: na página 1 o primeiro quadro é a página pronta, para o Instagram usar como capa no perfil
            t = dur * 1000 - 1 if (i == 1 and f == 0) else f * 1000 / FPS
            pgw.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {t}; }})')
            pgw.screenshot(path=os.path.join(fr, f'{f:04d}.png'))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(fr, '%04d.png'),
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', os.path.join(OUT, f'slide-{i:02d}.mp4')], check=True)
        shutil.rmtree(fr)
    br.close()
print('ok')
