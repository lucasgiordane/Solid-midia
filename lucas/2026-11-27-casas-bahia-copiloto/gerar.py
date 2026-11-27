#!/usr/bin/env python3
"""@lucasgiordane · 27/11/2026 · Modelo 2 NA PRÁTICA: "Casas Bahia: o copiloto de IA dos vendedores (Bah.IA)".
Pedido do Lucas: usar vários estilos de animação da referência @yleintech ("10 Claude Animation styles"), um por página:
  1 Quadrinho (Comic Art) · 2 Flat Vector · 3 Traço neon (Glow Sketch) · 4 Pixel Art · 5 Quadro de giz (Chalkboard) · 6 CTA padrão.
Uso: python3 -I gerar.py <saida> <solid26.css> <blobs> <fontes> png|mp4|medir [páginas, ex.: 1,4]
Fontes: Baguete, 12/09/2025 (Bah.IA, Gemini, CI&T, CTO Filipe Jaske); NeoFeed, 11/08/2026 (CEO Renato Franklin, +40% produtividade)."""
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
.pc .tx{margin-top:24px;gap:22px;flex:1;justify-content:center}
.pc .tp{font-size:36px;line-height:1.36;color:#1E2025}
.pc .tp b{color:#101013}
.pc .tb{font-size:46px}
/* caixa do vídeo com o mesmo tamanho e a mesma posição em todas as páginas (decisão do Lucas em 25/11/2026) */
.pc .mi{flex:none;height:660px;min-height:0;margin-top:24px;padding:0}
.fonte{position:absolute;left:26px;bottom:16px;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#A5A8AE;z-index:6}
.il-l{position:absolute;right:20px;top:18px;font-family:'IBM Plex Mono',monospace;font-size:16px;letter-spacing:.12em;color:#101013;background:#DDA94F;border-radius:4px;padding:4px 10px;z-index:6}
.sty{position:absolute;right:20px;bottom:14px;font-family:'IBM Plex Mono',monospace;font-size:15px;letter-spacing:.08em;z-index:6}
.cena{position:absolute;inset:0}
svg.sv{position:absolute;inset:0;width:100%;height:100%}
@keyframes draw{from{stroke-dashoffset:var(--L)}to{stroke-dashoffset:0}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{0%{opacity:0;transform:scale(.5)}70%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:scale(1)}}
@keyframes inL{from{opacity:0;transform:translateX(-60px)}to{opacity:1;transform:none}}
@keyframes inR{from{opacity:0;transform:translateX(60px)}to{opacity:1;transform:none}}
@keyframes inUp{from{opacity:0;transform:translateY(36px)}to{opacity:1;transform:none}}
@keyframes shake{0%,100%{transform:rotate(-4deg) scale(1)}50%{transform:rotate(3deg) scale(1.06)}}
@keyframes flick{0%,100%{opacity:1}45%{opacity:.8}50%{opacity:.55}55%{opacity:.9}}
@keyframes twk{0%,49%{opacity:1}50%,100%{opacity:.15}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes typ{from{width:0}to{width:var(--W)}}

/* ---------- 1 · QUADRINHO ---------- */
.hq{background:#F4F1EA;background-image:radial-gradient(#D9D2C1 2.2px,transparent 2.4px);background-size:16px 16px}
.hq .qd{position:absolute;background:#FFFFFF;border:6px solid #101013;box-shadow:10px 10px 0 #101013;overflow:hidden}
.hq .bl{position:absolute;background:#FFFFFF;border:5px solid #101013;border-radius:28px;padding:16px 22px;font-family:Bangers,cursive;font-size:38px;letter-spacing:.03em;color:#101013;text-align:center;line-height:1.05;z-index:3}
.hq .bl.t::after{content:'';position:absolute;left:60px;bottom:-26px;border:16px solid transparent;border-top:26px solid #101013;border-bottom:0}
.hq .bl.tr::after{content:'';position:absolute;right:60px;bottom:-26px;border:16px solid transparent;border-top:26px solid #101013;border-bottom:0}
.hq .bum{position:absolute;font-family:Bangers,cursive;font-size:78px;color:#DDA94F;-webkit-text-stroke:4px #101013;letter-spacing:.04em;z-index:4}
.hq .cap{position:absolute;left:0;top:0;background:#DDA94F;border-right:5px solid #101013;border-bottom:5px solid #101013;font-family:Bangers,cursive;font-size:30px;letter-spacing:.04em;padding:6px 14px;color:#101013}
.hq .sty{color:#101013;font-weight:600}
.hq .fonte{color:#3C4149}
/* ---------- 2 · FLAT VECTOR ---------- */
.flat{background:#1E2025}
.flat .ph{position:absolute;left:60px;top:120px;width:250px;height:440px;border-radius:36px;background:#F4F1EA}
.flat .ph .scr{position:absolute;left:16px;right:16px;top:40px;bottom:40px;border-radius:18px;background:#101013;overflow:hidden}
.flat .ph .cpf{position:absolute;left:16px;right:16px;top:60px;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#A5A8AE}
.flat .ph .in{position:absolute;left:16px;top:88px;height:48px;border-radius:10px;background:#F4F1EA;color:#101013;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:21px;line-height:48px;padding-left:12px;overflow:hidden;white-space:nowrap}
.flat .ph .bt{position:absolute;left:16px;right:16px;top:156px;height:52px;border-radius:10px;background:#DDA94F;color:#101013;font-family:Manrope,sans-serif;font-weight:800;font-size:22px;text-align:center;line-height:52px}
.flat .src{position:absolute;left:400px;width:470px;height:104px;border-radius:18px;background:#F4F1EA;color:#101013;display:flex;align-items:center;gap:20px;padding:0 24px;box-sizing:border-box}
.flat .src i{flex:none;width:64px;height:64px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:34px}
.flat .src b{display:block;font-family:Manrope,sans-serif;font-weight:800;font-size:28px}
.flat .src span{display:block;font-size:20px;color:#3C4149;margin-top:2px}
.flat .ln{position:absolute;height:6px;background:#DDA94F;border-radius:3px;transform-origin:left center}
.flat .sty{color:#A5A8AE}
/* ---------- 3 · TRAÇO NEON ---------- */
.glow{background:#0A0A0C}
.glow .ln{fill:none;stroke:#DDA94F;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 6px #DDA94F) drop-shadow(0 0 16px rgba(221,169,79,.6))}
.glow .ln2{fill:none;stroke:#F4F1EA;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 6px rgba(244,241,234,.8))}
.glow .gt{position:absolute;font-family:Manrope,sans-serif;font-weight:800;color:#F4F1EA;text-shadow:0 0 10px rgba(244,241,234,.6)}
.glow .gs{position:absolute;font-family:Inter,sans-serif;font-weight:500;color:#D9D4C7}
.glow .gn{position:absolute;font-family:'IBM Plex Mono',monospace;font-weight:600;color:#DDA94F;text-shadow:0 0 12px #DDA94F,0 0 28px rgba(221,169,79,.6)}
.glow .sty{color:#DDA94F}
/* ---------- 4 · PIXEL ---------- */
.pixel{background:#101013}
.pixel .px{position:absolute;font-family:'Press Start 2P',monospace;color:#F4F1EA;line-height:1.5}
.pixel .bx{position:absolute;left:44px;right:44px;height:150px;background:#1E2025;border:6px solid #F4F1EA;box-shadow:8px 8px 0 #3C4149;box-sizing:border-box}
.pixel .bx.g{border-color:#DDA94F;box-shadow:8px 8px 0 #A6752D}
.pixel .bx .n{position:absolute;left:26px;top:44px;font-family:'Press Start 2P',monospace;font-size:34px;color:#DDA94F}
.pixel .bx .d{position:absolute;left:330px;right:20px;top:26px;font-family:Inter,sans-serif;font-weight:600;font-size:24px;color:#F4F1EA;line-height:1.3}
.pixel .bx .d small{display:block;font-weight:500;font-size:18px;color:#A5A8AE;margin-top:6px}
.pixel .sty{color:#DDA94F;font-family:'Press Start 2P',monospace;font-size:11px}
/* ---------- 5 · QUADRO DE GIZ ---------- */
.giz{background:#1E2025;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:6px 6px}
.giz .ln{fill:none;stroke:#F4F1EA;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;filter:url(#chalk);opacity:.92}
.giz .lng{fill:none;stroke:#DDA94F;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;filter:url(#chalk)}
.giz .hw{position:absolute;font-family:Caveat,cursive;font-weight:700;color:#F4F1EA;line-height:1.05}
.giz .hw.g{color:#DDA94F}
.giz .sty{color:#A5A8AE}
/* ---------- 6 · CTA ---------- */
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
EX = '<span class="il-l">EXEMPLO</span>'
FB = '<span class="fonte">Fonte: Baguete, 12/09/2025 · NeoFeed, 11/08/2026</span>'
def path(d, cls, delay, dur, L=2400):
    return f'<path class="{cls}" d="{d}" style="--L:{L};stroke-dasharray:{L};animation:draw {dur}s {delay}s both ease-in-out"/>'
PAGS = []

# ---------- 1 · capa em QUADRINHO: cliente, vendedor, a IA "sopra" a venda ----------
def pessoa(x, y, cor, s=1.0):
    # boneco simples de HQ: cabeça, corpo, contorno grosso
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-60 210 C-60 120,60 120,60 210 Z" fill="{cor}" stroke="#101013" stroke-width="7" stroke-linejoin="round"/>'
            f'<circle cx="0" cy="62" r="52" fill="#F4F1EA" stroke="#101013" stroke-width="7"/>'
            f'<circle cx="-18" cy="58" r="6" fill="#101013"/><circle cx="18" cy="58" r="6" fill="#101013"/>'
            f'<path d="M-16 86 Q0 98 16 86" fill="none" stroke="#101013" stroke-width="5" stroke-linecap="round"/></g>')
q1 = (f'<div class="qd" style="left:34px;top:62px;width:410px;height:520px;animation:pop .5s .2s both">'
      f'<svg class="sv" viewBox="0 0 410 540">{pessoa(205, 300, "#3C4149", 1.05)}'
      f'<rect x="60" y="500" width="290" height="40" fill="#A5A8AE" stroke="#101013" stroke-width="6"/></svg>'
      f'<span class="cap">A CLIENTE</span></div>'
      f'<div class="bl t" style="left:60px;top:140px;width:330px;animation:pop .45s 1.0s both">QUERO UMA GELADEIRA… MAS O DINHEIRO TÁ CURTO!</div>')
q2 = (f'<div class="qd" style="left:476px;top:62px;width:410px;height:520px;animation:pop .5s .6s both">'
      f'<svg class="sv" viewBox="0 0 410 540">{pessoa(150, 300, "#DDA94F", 1.05)}'
      f'<rect x="232" y="356" width="104" height="170" rx="16" fill="#101013" stroke="#101013" stroke-width="6"/>'
      f'<rect x="244" y="372" width="80" height="120" rx="8" fill="#DDA94F" style="animation:flick 1s 2.6s 4"/>'
      f'<text x="284" y="440" text-anchor="middle" font-family="Bangers" font-size="34" fill="#101013">IA</text></svg>'
      f'<span class="cap">O VENDEDOR</span></div>'
      f'<div class="bl tr" style="left:500px;top:140px;width:360px;font-size:34px;animation:pop .45s 2.0s both">"DIGITA O CPF DELA: A IA ME DIZ O QUE CABE NO BOLSO."</div>'
      f'<div class="bum" style="left:690px;top:290px;animation:pop .4s 2.8s both, shake .5s 3.2s 4 both">BIP!</div>')
PAGS.append((6.5, page('1/6', 'NA PRÁTICA', TB('A Casas Bahia pôs uma IA para soprar a venda no ouvido de <em>mais de 10 mil vendedores.</em>') + TP('Chama Bah.IA. Te mostro como funciona ↓'),
    f'<div class="hq cena">{q1}{q2}{IL}{FB}<span class="sty">ESTILO · QUADRINHO</span></div>', 'Arraste →')))

# ---------- 2 · FLAT VECTOR: CPF → 3 fontes de dados ----------
ICO = lambda c: [f'<svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><circle cx="20" cy="13" r="7"/><path d="M6 36 C6 24 34 24 34 36"/></svg>',
                  f'<svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"><circle cx="17" cy="17" r="11"/><path d="M25 25 L36 36"/></svg>',
                  f'<svg width="40" height="40" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6 H9 L13 27 H32 L36 12 H11"/><circle cx="15" cy="34" r="2.5"/><circle cx="30" cy="34" r="2.5"/></svg>']
srcs = [(ICO('#DDA94F')[0], 'Perfil', 'quem é o cliente'), (ICO('#DDA94F')[1], 'Navegação', 'o que ele olhou no site'), (ICO('#101013')[2], 'Compras', 'o que já levou antes')]
fl = (f'<div class="ph" {A("inL", .6, .2)}><div class="scr"></div><span class="cpf">CPF DO CLIENTE</span>'
      f'<span class="in" style="--W:186px;animation:typ 1s .9s both steps(14)">123.456.789-00</span>'
      f'<span class="bt" {A("pop", .4, 2.0)}>Consultar</span></div>')
for k, (ic, t, s) in enumerate(srcs):
    y = 130 + 150 * k
    d = 2.5 + .55 * k
    fl += f'<span class="ln" style="left:316px;top:{y + 49}px;width:80px;animation:grow .35s {d - .3:.2f}s both"></span>'
    fl += f'<div class="src" style="top:{y}px;animation:inR .5s {d:.2f}s both cubic-bezier(.2,.8,.2,1)"><i style="background:{"#DDA94F" if k == 2 else "#101013"}">{ic}</i><div><b>{t}</b><span>{s}</span></div></div>'
PAGS.append((6.0, page('2/6', None, TB('1. O vendedor digita o CPF. <em>A IA lê o histórico do cliente.</em>') + TP('Perfil, o que ele olhou no site e o que já comprou.'),
    f'<div class="flat cena">{fl}{IL}{FB}<span class="sty">ESTILO · FLAT VECTOR</span></div>', 'Arraste →')))

# ---------- 3 · TRAÇO NEON: a tela que volta para o vendedor ----------
tela = 'M300 30 L620 30 Q650 30 650 60 L650 570 Q650 600 620 600 L300 600 Q270 600 270 570 L270 60 Q270 30 300 30 Z'
cards = [(96, 'Cabe no bolso', 'geladeira X em 12x, perto do limite dela'), (256, 'Como abordar', 'ela olhou 3 modelos de 2 portas'), (416, 'Compare com', 'o modelo que ela salvou no site')]
gl = f'<svg class="sv" viewBox="0 0 920 660">' + path(tela, 'ln', .2, 1.3, 2000)
gl += '<path class="ln2" d="M420 60 L500 60" style="--L:80;stroke-dasharray:80;animation:draw .3s 1.4s both"/>'
for k, (y, t, s) in enumerate(cards):
    gl += f'<rect class="ln2" x="296" y="{y}" width="328" height="140" rx="16" style="--L:940;stroke-dasharray:940;animation:draw .6s {1.6 + .7 * k:.2f}s both ease-in-out"/>'
gl += '</svg>'
for k, (y, t, s) in enumerate(cards):
    d = 2.0 + .7 * k
    gl += f'<div class="gn" style="left:318px;top:{y + 18}px;font-size:22px;animation:fade .4s {d:.2f}s both">0{k + 1}</div>'
    gl += f'<div class="gt" style="left:318px;top:{y + 48}px;width:290px;font-size:27px;line-height:1.15;animation:fade .4s {d + .1:.2f}s both">{t}</div>'
    gl += f'<div class="gs" style="left:318px;top:{y + 84}px;width:290px;font-size:19px;line-height:1.25;animation:fade .4s {d + .2:.2f}s both">{s}</div>'
gl += '<div class="gn" style="left:40px;top:250px;font-size:30px;width:210px;line-height:1.3;animation:fade .5s 4.2s both, flick 2s 4.8s infinite">em<br>segundos</div>'
gl += '<div class="gn" style="left:690px;top:250px;font-size:30px;width:210px;line-height:1.3;animation:fade .5s 4.5s both">no<br>WhatsApp</div>'
PAGS.append((6.5, page('3/6', None, TB('2. A IA sugere <em>o que oferecer e como falar.</em>') + TP('Produto certo para o bolso e o perfil, abordagem e comparação.'),
    f'<div class="glow cena">{gl}{EX}{FB}<span class="sty">ESTILO · TRAÇO NEON</span></div>', 'Arraste →')))

# ---------- 4 · PIXEL ART: o que a empresa diz que mudou ----------
nums = [('10 MIL+', 'vendedores usam o copiloto', 'Casas Bahia (CTO e CEO)', ''),
        ('+40%', 'de produtividade nas lojas físicas', 'CEO Renato Franklin, ao NeoFeed (ago/2026)', 'g'),
        ('+50%', 'de conversão nas vendas pelo WhatsApp', 'CTO Filipe Jaske, à Baguete (set/2025) · canal todo', '')]
px = ''
for k, (n, d, s, c) in enumerate(nums):
    t0 = .4 + 1.1 * k
    px += (f'<div class="bx {c}" style="top:{70 + 176 * k}px;animation:pop .45s {t0:.2f}s both steps(4)">'
           f'<span class="n" style="animation:fade .01s {t0 + .4:.2f}s both">{n}</span>'
           f'<div class="d" style="animation:fade .01s {t0 + .6:.2f}s both">{d}<small>{s}</small></div></div>')
px += ''.join(f'<i style="position:absolute;left:{x}px;top:{y}px;width:10px;height:10px;background:#DDA94F;animation:twk 1.2s {dl}s infinite steps(1)"></i>' for x, y, dl in [(120, 26, 0), (420, 34, .4), (700, 22, .8), (860, 40, .2)])
PAGS.append((6.5, page('4/6', None, TB('3. O que a Casas Bahia <em>diz que mudou.</em>') + TP('Números da própria empresa, sem auditoria de fora.'),
    f'<div class="pixel cena">{px}{FB}<span class="sty">ESTILO · PIXEL ART</span></div>', 'Arraste →')))

# ---------- 5 · QUADRO DE GIZ: no seu negócio ----------
filt = ('<filter id="chalk"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>')
passos = [('1.', 'Cadastre quem compra', '(nome e WhatsApp)'), ('2.', 'Anote o que levou e quando', '(planilha já serve)'), ('3.', 'Aí a IA sugere a próxima venda', '')]
gz = f'<svg class="sv" viewBox="0 0 920 660">{filt}'
gz += path('M60 108 L560 108', 'ln', .9, .5, 520)
for k in range(3):
    y = 210 + 130 * k
    gz += f'<rect class="ln" x="60" y="{y - 34}" width="46" height="46" style="--L:200;stroke-dasharray:200;animation:draw .35s {1.4 + 1.0 * k:.2f}s both"/>'
    if k < 2:
        gz += path(f'M68 {y - 12} L82 {y + 4} L106 {y - 40}', 'lng', 1.9 + 1.0 * k, .3, 90)
# círculo dourado no passo 3 e seta
gz += path('M118 455 C 118 398, 870 398, 870 455 C 870 514, 118 514, 124 450', 'lng', 4.6, .8, 1700)
gz += '</svg>'
gz += '<div class="hw" style="left:60px;top:40px;font-size:56px;animation:fade .6s .3s both">E no seu negócio?</div>'
for k, (n, t, s) in enumerate(passos):
    y = 210 + 130 * k
    gz += f'<div class="hw {"g" if k == 2 else ""}" style="left:130px;top:{y - 44}px;font-size:{50 if k < 2 else 52}px;animation:fade .5s {1.5 + 1.0 * k:.2f}s both">{t} <span style="font-size:34px;color:#A5A8AE">{s}</span></div>'
gz += '<div class="hw" style="left:60px;top:560px;font-size:40px;animation:fade .6s 5.2s both">sem histórico, nenhuma IA adivinha nada.</div>'
PAGS.append((7.0, page('5/6', None, TB('4. No seu negócio, o começo é <em>anotar quem compra o quê.</em>') + TP('A IA da Casas Bahia só funciona porque o histórico existe.'),
    f'<div class="giz cena">{gz}{EX}<span class="sty">ESTILO · QUADRO DE GIZ</span></div>', 'Arraste →')))

# ---------- 6 · CTA ----------
cm = (f'<div class="ctaw"><div class="kw" {A("pop", .6, .4)}><span class="kwl">comente</span><b class="tw">DIAGNÓSTICO</b></div>'
      f'<div class="cm" {A("inUp", .6, 2.0)}><i class="avg"></i><div><b>seguidor</b><span class="ty">DIAGNÓSTICO</span></div><em {A("pop", .4, 2.6)}>♥</em></div>'
      f'<div class="cm me" {A("inUp", .6, 3.1)}><img src="{AV}" alt=""><div><b>lucasgiordane</b><span>Te chamei no direct! 📩</span></div></div>'
      f'<div class="dm" {A("inUp", .6, 4.2)}><small>direct · lucasgiordane</small><span>Oi! Me conta: qual é o seu negócio e o que mais trava hoje?</span></div></div>')
PAGS.append((7.0, page('6/6', 'SUA VEZ', TB('Seu vendedor sabe o que o cliente <em>já comprou</em> antes de atender?') + TP('<b>Comenta DIAGNÓSTICO</b> que eu te chamo no direct e a gente olha o seu caso. E salva para não perder.'),
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
