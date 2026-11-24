#!/usr/bin/env python3
"""@lucasgiordane · 24/11/2026 · Modelo 5 RAIO-X: "Black Friday: o caminho de um golpe".
Uso: python3 -I gerar.py <saida> <solid26.css> <blobs> <fontes> png|mp4 [páginas, ex.: 1,4]
Fontes: relatório BioCatch "Tendências de Fraude Bancária Digital no Brasil 2026", via TI Inside (23/11/2026); alertas do Procon-MG e da Senacon, via ISTOÉ (23/11/2026)."""
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
.pc .tx{margin-top:36px;gap:22px}
.pc .tp{font-size:36px;line-height:1.36;color:#1E2025}
.pc .tp b{color:#101013}
.pc .tb{font-size:46px}
.pc .mi{margin-top:34px;padding:0}
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
.q{display:flex;gap:18px;align-items:center;background:#F4F1EA;color:#101013;border-radius:12px;padding:16px 20px}
.q .bx i{font-style:normal}
.q .bx{flex:none;width:44px;height:44px;border-radius:8px;border:4px solid #101013;box-sizing:border-box;display:flex;align-items:center;justify-content:center;font-family:Manrope,sans-serif;font-weight:800;font-size:30px;color:#EF4444;line-height:1}
.q b{font-family:Manrope,sans-serif;font-weight:800;font-size:27px;line-height:1.25}
.q span{display:block;font-size:19px;color:#3C4149;margin-top:2px}
.cap{font-size:25px;line-height:1.35;color:#F5F5F5;background:#2A2416;border:1px solid #A6752D;border-radius:12px;padding:16px 20px}
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

CSS += """
.flow{display:flex;flex-direction:column;align-items:stretch;gap:0}
.nd{display:flex;align-items:center;gap:18px;background:#F4F1EA;color:#101013;border-radius:12px;padding:14px 20px}
.nd i{font-style:normal;flex:none;width:46px;height:46px;border-radius:50%;background:#101013;color:#DDA94F;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:22px}
.nd b{font-family:Manrope,sans-serif;font-weight:800;font-size:26px;line-height:1.2}
.nd.red{background:#FDECEC;border:4px solid #EF4444}
.nd.red i{background:#EF4444;color:#F5F5F5}
.ar{align-self:center;width:4px;height:26px;background:#DDA94F;position:relative;margin:4px 0 10px}
.ar:after{content:'';position:absolute;left:-8px;bottom:-10px;border:10px solid transparent;border-top:12px solid #DDA94F;border-bottom:0}
.brk{align-self:flex-end;margin-top:10px;background:#EF4444;color:#F5F5F5;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:20px;letter-spacing:.08em;border-radius:6px;padding:6px 12px}
.ph{display:flex;justify-content:center;gap:26px}
.ph span{width:120px;height:206px;border-radius:18px;border:5px solid #5B6070;box-sizing:border-box;position:relative;display:block}
.ph span:after{content:'';position:absolute;left:38px;right:38px;bottom:12px;height:5px;border-radius:3px;background:#5B6070}
.ph span.on{border-color:#DDA94F;background:#2A2416}
.ph span.on:after{background:#DDA94F}
.ph span.on b{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);font-family:Manrope,sans-serif;font-weight:800;font-size:20px;line-height:1.2;color:#DDA94F;text-align:center}
.ring{position:absolute;inset:-14px;border-radius:26px;border:4px solid #DDA94F;opacity:0}
@keyframes ring{0%{opacity:.9;transform:scale(.9)}100%{opacity:0;transform:scale(1.25)}}
.hr{position:relative;height:84px;border-radius:10px;background:#2A2D33}
.hr .s{position:absolute;top:0;bottom:0;border-radius:10px;transform-origin:left center}
.ticks{display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;font-size:22px;color:#A5A8AE;margin-top:10px}
.lgd{display:flex;gap:16px;flex-wrap:wrap}
.lgd span{display:flex;align-items:center;gap:10px;font-size:22px;color:#F5F5F5}
.lgd span i{width:26px;height:26px;border-radius:6px;display:block}
"""
FBC = '<span class="fonte">Fonte: relatório BioCatch (bancos clientes no Brasil), via TI Inside · 23/11/2026</span>'
DIC = '<span class="il-l" style="z-index:5">DICAS</span>'
PAGS = []
# 1 · capa: o caminho do golpe
nds = [('1', '', 'Anúncio com preço bom demais'), ('2', '', 'Site que imita uma loja conhecida'), ('3', '', 'Pagamento por Pix'), ('!', 'red', 'A "central do banco" liga no meio da compra')]
fl = ''
for k, (n, c, t) in enumerate(nds):
    if k: fl += f'<span class="ar" {A("fade", .3, .5 + .9 * k - .3)}></span>'
    fl += f'<div class="nd {c}" {A("inL", .5, .5 + .9 * k)}><i>{n}</i><b>{t}</b></div>'
fl += f'<span class="brk" {A("pop", .5, 3.9)}>PONTO DE QUEBRA: VOCÊ NO TELEFONE</span>'
PAGS.append((6.0, page('1/6', 'RAIO-X', TB('Black Friday é sexta. Mapeei o caminho de um golpe. <em>O ponto fraco não é o banco.</em>') + TP('É a ligação no meio da compra. Te mostro ↓'),
                       IL + f'<div class="wrap" style="padding-top:60px"><div class="flow">{fl}</div></div>', 'Arraste →')))
# 2 · os 3 golpes mais comuns
gl = [('Loja falsa', 37.8, 'g'), ('Falsa central de atendimento', 22.5, ''), ('Falso advogado', 11.2, '')]
bs = ''.join(f'<div class="br {c}" {A("fade", .4, .3 + 1.0 * i)}><div class="lb"><span>{n}</span><b>{str(v).replace(".", ",")}%</b></div><div class="tr"><i style="width:{v / 37.8 * 100:.1f}%;animation:grow .9s {.6 + 1.0 * i}s both cubic-bezier(.2,.8,.2,1)"></i></div></div>' for i, (n, v, c) in enumerate(gl))
PAGS.append((6.0, page('2/6', None, TB('1. Os 3 golpes mais comuns no Brasil. <em>Loja falsa lidera.</em>') + TP('Juntos, somam mais de 7 em cada 10 golpes registrados.'),
                       f'<div class="wrap">{bs}<p class="cap" {A("inUp", .5, 3.6)}>Período: 2º semestre de 2025 e 1º de 2026. <b>Dado de uma empresa de segurança, a partir dos bancos clientes dela.</b></p></div>' + FBC, 'Arraste →')))
# 3 · 1 em cada 5: no telefone
phs = ''.join(f'<span class="{"on" if k == 2 else ""}" {A("pop", .4, .3 + .3 * k)}>' + ('<b>EM<br>LIGAÇÃO</b><i class="ring" style="animation:ring 1.2s 2.0s 3 both"></i>' if k == 2 else '') + '</span>' for k in range(5))
PAGS.append((6.0, page('3/6', None, TB('2. Em 1 de cada 5 tentativas, <em>a vítima está no telefone.</em>') + TP('Falando com o golpista enquanto mexe no app do banco.'),
                       f'<div class="wrap"><div class="ph">{phs}</div><div class="chips"><div class="chip g" {A("pop", .5, 3.0)}><b>+88%</b><span>ligações ativas detectadas durante o uso do banco</span></div>'
                       f'<div class="chip" {A("pop", .5, 3.6)}><b>3x</b><span>mais longa: a sessão do golpe dura o triplo da normal</span></div></div></div>' + FBC, 'Arraste →')))
# 4 · horário
hr = (f'<div><div class="hr"><span class="s" style="left:37.5%;width:33.3%;background:#DDA94F;animation:grow .9s .6s both"></span>'
      f'<span class="s" style="left:58.3%;width:12.5%;background:#EF4444;animation:grow .6s 1.8s both"></span></div>'
      f'<div class="ticks"><span>0h</span><span>6h</span><span>12h</span><span>18h</span><span>24h</span></div></div>'
      f'<div class="lgd" {A("fade", .5, 2.6)}><span><i style="background:#DDA94F"></i>9h às 17h: 90% das tentativas</span><span><i style="background:#EF4444"></i>14h às 17h: pico</span></div>'
      f'<p class="cap" {A("inUp", .5, 3.6)}>Justo quando você está no trabalho, <b>com pressa e sem tempo de conferir.</b></p>')
PAGS.append((6.0, page('4/6', None, TB('3. Não é de madrugada. <em>É em horário comercial.</em>') + TP('Nove em cada dez tentativas acontecem entre 9h e 17h. O pico é à tarde.'),
                       f'<div class="wrap">{hr}</div>' + FBC, 'Arraste →')))
# 5 · checklist
qs = [('Preço bom demais?', 'Desconfie antes de clicar.'),
      ('O site é mesmo o da loja?', 'Confira o endereço e o CNPJ.'),
      ('Pix para pessoa física?', 'Pare e confira de novo.'),
      ('"O banco" ligou pedindo para mover dinheiro?', 'Desligue e ligue você no número oficial.')]
ql = ''.join(f'<div class="q" {A("inL", .5, .5 + .8 * i)}><span class="bx"><i {A("pop", .3, .9 + .8 * i)}>✓</i></span><div><b>{a}</b><span>{b}</span></div></div>' for i, (a, b) in enumerate(qs))
PAGS.append((6.5, page('5/6', None, TB('4. Antes de pagar: <em>10 segundos de conferência.</em>') + TP('O Procon alerta para golpes com IA, com Pix e com lojas falsas nesta Black Friday.'),
                       DIC + f'<div class="wrap" style="padding-top:62px;gap:16px">{ql}</div><span class="fonte">Alerta: Procon-MG e MP-MG, via ISTOÉ · 23/11/2026</span>', 'Arraste: falta uma pergunta →')))
# 6 · CTA
cm = (f'<div class="ctaw"><div class="kw" {A("pop", .6, .4)}><span class="kwl">comente</span><b class="tw">DIAGNÓSTICO</b></div>'
      f'<div class="cm" {A("inUp", .6, 2.0)}><i class="avg"></i><div><b>seguidor</b><span class="ty">DIAGNÓSTICO</span></div><em {A("pop", .4, 2.6)}>♥</em></div>'
      f'<div class="cm me" {A("inUp", .6, 3.1)}><img src="{AV}" alt=""><div><b>lucasgiordane</b><span>Te chamei no direct! 📩</span></div></div>'
      f'<div class="dm" {A("inUp", .6, 4.2)}><small>direct · lucasgiordane</small><span>Oi! Me conta: qual é o seu negócio e o que mais trava hoje?</span></div></div>')
PAGS.append((7.0, page('6/6', 'SUA VEZ', TB('Seu cliente sabe confirmar que <em>é mesmo a sua empresa</em> falando com ele?') + TP('<b>Comenta DIAGNÓSTICO</b> que eu te chamo no direct e a gente olha o seu caso. E salva para não perder.'),
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
