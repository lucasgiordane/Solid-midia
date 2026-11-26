#!/usr/bin/env python3
"""@lucasgiordane · 26/11/2026 · Modelo 4 FAZ A CONTA: "58 empresas, IA e emprego".
Uso: python3 -I gerar.py <saida> <solid26.css> <blobs> <fontes> png|mp4|medir [páginas, ex.: 1,4]
Fontes: Anthropic, "Working with AI" (23/11/2026); Anthropic, "Labor market impacts of AI" (05/03/2026, atualizado em 13/11/2026), ranking via CBS News."""
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

CSS += """
.dots{display:grid;grid-template-columns:repeat(15,1fr);gap:12px;padding:0 6px}
.dots i{display:block;aspect-ratio:1;border-radius:50%;background:#3C4149}
.dots i.on{background:#EF4444;box-shadow:0 0 0 5px rgba(239,68,68,.25)}
.lgd2{display:flex;gap:22px;flex-wrap:wrap;font-size:22px;color:#F5F5F5}
.lgd2 span{display:flex;align-items:center;gap:10px}
.lgd2 i{width:22px;height:22px;border-radius:50%;display:block}
.thirds{display:flex;gap:14px}
.thirds div{flex:1;height:150px;border-radius:12px;background:#F4F1EA;color:#101013;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:6px;text-align:center;padding:0 10px}
.thirds div.g{background:#DDA94F}
.thirds b{font-family:Manrope,sans-serif;font-weight:800;font-size:30px}
.thirds span{font-size:19px;line-height:1.25}
.quote{background:#F4F1EA;color:#101013;border-radius:14px;padding:26px 30px;font-family:Manrope,sans-serif;font-weight:800;font-size:36px;line-height:1.25;position:relative;border-left:10px solid #DDA94F}
.quote small{display:block;margin-top:12px;font-family:Inter,sans-serif;font-weight:500;font-size:19px;color:#3C4149}
.rk{display:flex;flex-direction:column;gap:12px}
.rk .r{display:grid;grid-template-columns:330px 1fr 92px;align-items:center;gap:16px}
.rk .r span{font-size:23px;color:#F5F5F5;line-height:1.15}
.rk .r .tr{height:40px;border-radius:8px;background:#2A2D33;overflow:hidden}
.rk .r .tr i{display:block;height:100%;border-radius:8px;background:#F4F1EA;transform-origin:left center}
.rk .r.g .tr i{background:#DDA94F}
.rk .r b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:32px;color:#F4F1EA;text-align:right}
.rk .r.g b{color:#DDA94F}
.cb{display:flex;flex-direction:column;gap:8px}
.cb .cl{display:flex;justify-content:space-between;align-items:baseline;gap:20px}
.cb .cl span{font-size:24px;color:#F5F5F5;line-height:1.2}
.cb .cl b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:38px;color:#F4F1EA}
.cb .ct{height:30px;border-radius:8px;background:#2A2D33;overflow:hidden}
.cb .ct i{display:block;height:100%;border-radius:8px;background:#F4F1EA;transform-origin:left center}
.cb.g .cl b{color:#DDA94F}
.cb.g .ct i{background:#DDA94F}
.zero{font-size:22px;line-height:1.35;color:#F5F5F5;border-top:1px solid #3C4149;padding-top:14px}
.zero b{color:#DDA94F}
"""
FWA = '<span class="fonte">Fonte: Anthropic, "Working with AI" · 23/11/2026 · 58 empresas clientes, EUA</span>'
FLM = '<span class="fonte">Fonte: Anthropic, "Labor market impacts of AI" (mar/2026, atual. 13/11), via CBS News</span>'
PAGS = []

# 1 · capa: cartão da notícia + 58 pontos, 2 acendem
dots = ''.join(f'<i class="{"on" if k in (22, 41) else ""}" style="animation:{"pop" if k in (22, 41) else "fade"} .4s {(2.6 + (0.5 if k == 41 else 0)) if k in (22, 41) else 0.9 + k * 0.022:.2f}s both"></i>' for k in range(58))
PAGS.append((6.0, page('1/6', 'FAZ A CONTA', TB('A Anthropic foi a 58 empresas ver o que a IA fez com os empregos. <em>Fiz a conta.</em>') + TP('Quase ninguém foi demitido pela IA. O efeito está em outro lugar ↓'),
    f'<div class="wrap" style="gap:26px"><div class="news" {A("inUp", .6, .2)}><small>ANTHROPIC · ESTUDO · 23/11/2026</small><b>Working with AI</b><span>66 entrevistas em 58 empresas clientes da Anthropic, nos EUA</span></div>'
    f'<div class="dots">{dots}</div><div class="lgd2" {A("fade", .5, 3.5)}><span><i style="background:#EF4444"></i>demitiram porque a IA eliminou o cargo</span></div></div>' + FWA, 'Arraste →')))

# 2 · só 2 em 58; 2 em cada 3 contratam menos
th = ''.join(f'<div class="{"g" if k < 2 else ""}" {A("pop", .5, 2.0 + .5 * k)}><b>{"contrata menos" if k < 2 else "o resto"}</b><span>{"por causa da IA" if k < 2 else "sem queda relatada"}</span></div>' for k in range(3))
PAGS.append((6.0, page('2/6', None, TB('1. Só <em>2 de 58</em> empresas demitiram porque a IA eliminou um cargo.') + TP('Mas em 2 de cada 3, a contratação caiu.'),
    f'<div class="wrap" style="gap:28px"><div class="bign" {A("inL", .6, .3)}><b>2/58</b><span>empresas tiveram um cargo<br><em>eliminado pela IA</em>, com demissão</span></div>'
    f'<div class="thirds">{th}</div></div>' + FWA, 'Arraste →')))

# 3 · a vaga que não abre
fl3 = [('1', '', 'Alguém sai da empresa'), ('2', '', 'A vaga não é reposta'), ('3', '', 'A equipe que ficou, com IA, absorve o trabalho')]
f3 = ''
for k, (n, c, t) in enumerate(fl3):
    if k: f3 += f'<span class="ar" {A("fade", .3, 1.6 + .8 * k - .3)}></span>'
    f3 += f'<div class="nd {c}" {A("inL", .5, 1.6 + .8 * k)}><i>{n}</i><b>{t}</b></div>'
PAGS.append((6.5, page('3/6', None, TB('2. O efeito é a vaga <em>que não abre.</em>') + TP('Um terço da queda é não repor quem saiu. O resto: vaga que nem chegou a abrir.'),
    f'<div class="wrap" style="gap:24px"><div class="quote" {A("inUp", .6, .3)}>"A gente pode não estar demitindo, mas não está contratando."<small>Entrevistado anônimo do estudo</small></div><div class="flow">{f3}</div></div>' + FWA, 'Arraste →')))

# 4 · o que aconteceu nas 58
cnt = [('Contrataram mais: gente para implantar IA e TI', 10, ''), ('Cortaram terceirizados', 9, 'g'), ('Tiraram quem se recusou a usar IA', 5, 'g'), ('Demitiram porque a IA eliminou o cargo', 2, '')]
bs = ''.join(f'<div class="cb {c}" {A("fade", .4, .3 + .8 * i)}><div class="cl"><span>{n}</span><b>{v}</b></div><div class="ct"><i style="width:{v / 10 * 100:.0f}%;animation:grow .8s {.5 + .8 * i}s both cubic-bezier(.2,.8,.2,1)"></i></div></div>' for i, (n, v, c) in enumerate(cnt))
PAGS.append((6.5, page('4/6', None, TB('3. Quem mais sente: <em>o terceirizado e quem recusa a IA.</em>') + TP('Programação, atendimento, jurídico e retaguarda, muitos fora do país.'),
    f'<div class="wrap" style="gap:18px;padding-bottom:64px">{bs}<p class="cap" style="font-size:22px" {A("inUp", .5, 3.8)}>Uma fintech trocou o atendimento terceirizado por agentes de IA. <b>Amostra: clientes da Anthropic nos EUA, não o mercado todo.</b></p></div>' + FWA.replace('58 empresas clientes, EUA', 'nº de empresas, de 58'), 'Arraste →')))

# 5 · profissões mais expostas
rk = [('Programador', 75), ('Atendimento ao cliente', 70), ('Digitação de dados', 67), ('Prontuário médico', 67), ('Pesquisa de mercado e marketing', 65), ('Vendedor', 63), ('Analista financeiro', 57)]
rl = ''.join(f'<div class="r {"g" if i == 0 else ""}" {A("fade", .3, .3 + .45 * i)}><span>{n}</span><div class="tr"><i style="width:{v}%;animation:grow .7s {.4 + .45 * i}s both cubic-bezier(.2,.8,.2,1)"></i></div><b>{v}%</b></div>' for i, (n, v) in enumerate(rk))
PAGS.append((6.5, page('5/6', None, TB('4. Onde a IA já faz <em>mais tarefas</em> hoje.') + TP('% das tarefas da profissão que já aparecem no uso real do Claude.'),
    f'<div class="wrap" style="gap:18px"><div class="rk">{rl}</div><p class="zero" {A("fade", .5, 4.0)}>Perto de zero: <b>cozinheiro, mecânico de moto, bartender, salva-vidas.</b></p></div>' + FLM, 'Arraste →')))

# 6 · CTA
cm = (f'<div class="ctaw"><div class="kw" {A("pop", .6, .4)}><span class="kwl">comente</span><b class="tw">DIAGNÓSTICO</b></div>'
      f'<div class="cm" {A("inUp", .6, 2.0)}><i class="avg"></i><div><b>seguidor</b><span class="ty">DIAGNÓSTICO</span></div><em {A("pop", .4, 2.6)}>♥</em></div>'
      f'<div class="cm me" {A("inUp", .6, 3.1)}><img src="{AV}" alt=""><div><b>lucasgiordane</b><span>Te chamei no direct! 📩</span></div></div>'
      f'<div class="dm" {A("inUp", .6, 4.2)}><small>direct · lucasgiordane</small><span>Oi! Me conta: qual é o seu negócio e o que mais trava hoje?</span></div></div>')
PAGS.append((7.0, page('6/6', 'SUA VEZ', TB('Na sua empresa, a próxima vaga vai ser <em>de gente ou de IA?</em>') + TP('<b>Comenta DIAGNÓSTICO</b> que eu te chamo no direct e a gente olha o seu caso. E salva para não perder.'),
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
