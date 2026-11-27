#!/usr/bin/env python3
"""@lucasgiordane · 27/11/2026 · Modelo 2 NA PRÁTICA: "Casas Bahia: o copiloto de IA dos vendedores (Bah.IA)".
Pedido do Lucas: usar vários estilos de animação da referência @yleintech ("10 Claude Animation styles"), um por página:
  v2 (27/11): cada estilo com paleta própria dentro da caixa e animação fora do padrão (pedido do Lucas).
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

/* v2 (27/11, pedido do Lucas): cada estilo com a sua paleta própria dentro da caixa e animação fora do padrão.
   Cabeçalho, texto de cima e rodapé seguem a identidade 2026. Contraste alto em tudo, nunca tom sobre tom. */
@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 -5% 0 0)}}
@keyframes slamL{0%{opacity:0;transform:translate(-120px,40px) rotate(-14deg) scale(.7)}70%{opacity:1;transform:translate(8px,-4px) rotate(2deg) scale(1.03)}100%{opacity:1;transform:rotate(-1.5deg)}}
@keyframes slamR{0%{opacity:0;transform:translate(120px,40px) rotate(14deg) scale(.7)}70%{opacity:1;transform:translate(-8px,-4px) rotate(-2deg) scale(1.03)}100%{opacity:1;transform:rotate(1.5deg)}}
@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
@keyframes zoomin{0%,100%{transform:scale(1)}40%{transform:scale(1.06) rotate(-.6deg)}}
@keyframes buzz{0%,100%{transform:translate(0,0) rotate(0)}20%{transform:translate(-4px,1px) rotate(-3deg)}40%{transform:translate(4px,-1px) rotate(3deg)}60%{transform:translate(-3px,0) rotate(-2deg)}80%{transform:translate(3px,1px) rotate(2deg)}}
@keyframes wob{0%,100%{transform:rotate(-2deg)}50%{transform:rotate(2deg)}}
@keyframes bounceIn{0%{opacity:0;transform:translateY(-260px)}55%{opacity:1;transform:translateY(0)}72%{transform:translateY(-36px)}86%{transform:translateY(0)}93%{transform:translateY(-10px)}100%{opacity:1;transform:none}}
@keyframes press{0%,100%{transform:scale(1)}45%{transform:scale(.88)}}
@keyframes flipIn{from{opacity:0;transform:perspective(900px) rotateY(-95deg)}to{opacity:1;transform:perspective(900px) rotateY(0)}}
@keyframes float{0%,100%{transform:translate(0,0)}50%{transform:translate(14px,-18px)}}
@keyframes travel{0%{offset-distance:0%;opacity:0}10%{opacity:1}90%{opacity:1}100%{offset-distance:100%;opacity:0}}
@keyframes glitch{0%,100%{transform:none;opacity:1}20%{transform:translate(-6px,0) skewX(-8deg);opacity:.7}22%{transform:translate(5px,0);opacity:1}24%{transform:none}60%{opacity:1}62%{opacity:.3}64%{opacity:1}}
@keyframes scan{from{transform:translateY(-40px)}to{transform:translateY(600px)}}
@keyframes gridmove{from{background-position:0 0}to{background-position:0 60px}}
@keyframes neonOn{0%{opacity:0}10%{opacity:1}14%{opacity:.2}18%{opacity:1}30%{opacity:.4}34%,100%{opacity:1}}
@keyframes coin{0%{opacity:0;transform:translateY(0)}20%{opacity:1}100%{opacity:0;transform:translateY(-90px)}}
@keyframes fillB{from{width:0}to{width:var(--W)}}
@keyframes blinkS{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes dust{0%{opacity:.9;transform:translate(0,0)}100%{opacity:0;transform:translate(var(--dx),60px)}}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(-14px)}}

/* ---------- 1 · QUADRINHO (pop art) ---------- */
.hq{background:#FFD23F;overflow:hidden}
.hq .rays{position:absolute;left:50%;top:50%;width:1600px;height:1600px;margin:-800px 0 0 -800px;background:repeating-conic-gradient(#FFB627 0 8deg,#FFD23F 8deg 16deg);animation:spin 40s linear infinite}
.hq .dotsr{position:absolute;inset:0;background-image:radial-gradient(rgba(230,57,70,.28) 3px,transparent 3.4px);background-size:18px 18px}
.hq .zoom{position:absolute;inset:0;animation:zoomin 1.4s 3.0s both ease-in-out}
.hq .qd{position:absolute;border:7px solid #101013;box-shadow:12px 12px 0 #101013;overflow:hidden}
.hq .qd.a{background:#7FD1F5}
.hq .qd.b{background:#FF8FB1}
.hq .bl{position:absolute;background:#FFFFFF;border:5px solid #101013;border-radius:28px;padding:16px 22px;font-family:Bangers,cursive;font-size:38px;letter-spacing:.03em;color:#101013;text-align:center;line-height:1.05;z-index:3}
.hq .bl em{font-style:normal;color:#E63946}
.hq .bl.t::after{content:'';position:absolute;left:60px;bottom:-26px;border:16px solid transparent;border-top:26px solid #101013;border-bottom:0}
.hq .bl.tr::after{content:'';position:absolute;right:60px;bottom:-26px;border:16px solid transparent;border-top:26px solid #101013;border-bottom:0}
.hq .bum{position:absolute;font-family:Bangers,cursive;font-size:92px;color:#E63946;-webkit-text-stroke:5px #101013;letter-spacing:.04em;z-index:4;text-shadow:6px 6px 0 #FFFFFF}
.hq .star{position:absolute;z-index:3}
.hq .cap{position:absolute;left:0;top:0;background:#101013;font-family:Bangers,cursive;font-size:30px;letter-spacing:.04em;padding:6px 14px;color:#FFD23F}
.hq .sty,.hq .fonte{color:#101013;font-weight:600;background:#FFD23F;padding:2px 6px}
.hq .fonte{left:20px}
.hq .il-l{background:#101013;color:#FFD23F}
/* ---------- 2 · FLAT VECTOR (pastel e cor viva) ---------- */
.flat{background:#FFF1E0;overflow:hidden}
.flat .blob{position:absolute;border-radius:50%}
.flat .ph{position:absolute;left:60px;top:110px;width:250px;height:440px;border-radius:36px;background:#2B2D42;box-shadow:0 24px 0 rgba(43,45,66,.15)}
.flat .ph .scr{position:absolute;left:16px;right:16px;top:40px;bottom:40px;border-radius:18px;background:#FFFFFF;overflow:hidden}
.flat .ph .cpf{position:absolute;left:30px;right:16px;top:64px;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:16px;color:#4D7CFE}
.flat .ph .in{position:absolute;left:30px;top:92px;height:48px;border-radius:10px;background:#EEF2FF;color:#2B2D42;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:19px;line-height:48px;padding-left:10px;overflow:hidden;white-space:nowrap}
.flat .ph .bt{position:absolute;left:30px;right:30px;top:160px;height:52px;border-radius:26px;background:#FF6B6B;color:#FFFFFF;font-family:Manrope,sans-serif;font-weight:800;font-size:22px;text-align:center;line-height:52px}
.flat .ph .ok{position:absolute;left:30px;right:30px;top:240px;font-family:Manrope,sans-serif;font-weight:800;font-size:20px;color:#1FB5A9;text-align:center}
.flat .src{position:absolute;left:420px;width:450px;height:108px;border-radius:22px;color:#FFFFFF;display:flex;align-items:center;gap:20px;padding:0 24px;box-sizing:border-box;transform-origin:left center}
.flat .src i{flex:none;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.95);display:flex;align-items:center;justify-content:center}
.flat .src b{display:block;font-family:Manrope,sans-serif;font-weight:800;font-size:30px}
.flat .src span{display:block;font-size:21px;margin-top:2px;font-weight:500}
.flat .pk{position:absolute;left:0;top:0;width:22px;height:22px;border-radius:50%;margin:-11px 0 0 -11px}
.flat .sty,.flat .fonte{color:#2B2D42}
.flat .il-l{background:#2B2D42;color:#FFF1E0}
/* ---------- 3 · TRAÇO NEON (synthwave) ---------- */
.glow{background:linear-gradient(#0D0221 0%,#1A0638 62%,#2D0B57 100%);overflow:hidden}
.glow .floor{position:absolute;left:-200px;right:-200px;bottom:-40px;height:260px;transform:perspective(320px) rotateX(58deg);transform-origin:bottom center;background-image:linear-gradient(#FF2BD6 2px,transparent 2px),linear-gradient(90deg,#FF2BD6 2px,transparent 2px);background-size:60px 60px;opacity:.45;animation:gridmove 1.2s linear infinite}
.glow .sun{position:absolute;left:50%;top:300px;width:300px;height:300px;margin-left:-150px;border-radius:50%;background:linear-gradient(#FFE600,#FF2BD6);opacity:.22;filter:blur(2px)}
.glow .ph{fill:#0D0221;fill-opacity:.85;stroke:#00F0FF;stroke-width:5;stroke-linejoin:round;filter:drop-shadow(0 0 8px #00F0FF) drop-shadow(0 0 22px rgba(0,240,255,.6))}
.glow .cd{fill:none;stroke-width:4;filter:drop-shadow(0 0 8px currentColor)}
.glow .gt{position:absolute;font-family:Manrope,sans-serif;font-weight:800;color:#FFFFFF}
.glow .gs{position:absolute;font-family:Inter,sans-serif;font-weight:500;color:#E9E3FF}
.glow .gn{position:absolute;font-family:'IBM Plex Mono',monospace;font-weight:600}
.glow .scan{position:absolute;left:276px;width:368px;height:28px;background:linear-gradient(transparent,rgba(0,240,255,.55),transparent);top:30px}
.glow .side{position:absolute;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:30px;line-height:1.3;width:220px}
.glow .sty{color:#00F0FF}
.glow .fonte{color:#E9E3FF;background:rgba(13,2,33,.9);padding:2px 6px;left:20px}
.glow .il-l{background:#FFE600;color:#0D0221}
/* ---------- 4 · PIXEL ART (tela de jogo) ---------- */
.pixel{background:#5C94FC;overflow:hidden}
.pixel .px{position:absolute;font-family:'Press Start 2P',monospace;line-height:1.5}
.pixel .bx{position:absolute;left:40px;right:40px;height:142px;background:#101436;border:6px solid #FFFFFF;box-shadow:8px 8px 0 #101013;box-sizing:border-box}
.pixel .bx .n{position:absolute;left:24px;top:22px;font-family:'Press Start 2P',monospace;font-size:32px}
.pixel .bx .bar{position:absolute;left:24px;top:78px;width:260px;height:26px;background:#2A2F5E;border:4px solid #FFFFFF;box-sizing:content-box}
.pixel .bx .bar i{display:block;height:100%}
.pixel .bx .d{position:absolute;left:330px;right:20px;top:20px;font-family:Inter,sans-serif;font-weight:700;font-size:24px;color:#FFFFFF;line-height:1.3}
.pixel .bx .d small{display:block;font-weight:500;font-size:18px;color:#C7CEF5;margin-top:6px}
.pixel .lv{position:absolute;font-family:'Press Start 2P',monospace;font-size:14px;color:#101013;background:#FFE600;padding:6px 8px;border:3px solid #101013}
.pixel .ground{position:absolute;left:0;right:0;bottom:0;height:56px;background:repeating-linear-gradient(90deg,#C84C0C 0 46px,#8B2E00 46px 50px);border-top:8px solid #3AB54A}
.pixel .cl{position:absolute;width:120px;height:30px;background:#FFFFFF;box-shadow:30px -20px 0 #FFFFFF,60px 0 0 #FFFFFF}
.pixel .cn{position:absolute;width:20px;height:28px;background:#FFE600;border:4px solid #101013}
.pixel .sty{color:#FFFFFF;font-family:'Press Start 2P',monospace;font-size:11px;bottom:20px}
.pixel .fonte{color:#FFFFFF;bottom:20px}
/* ---------- 5 · QUADRO DE GIZ (lousa verde, giz colorido) ---------- */
.giz{background:#2F5D3A;background-image:radial-gradient(rgba(255,255,255,.06) 1px,transparent 1px),radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.08),transparent 60%);background-size:6px 6px,100% 100%;box-shadow:inset 0 0 0 16px #8B5A2B,inset 0 0 0 20px #5E3A17}
.giz .ln{fill:none;stroke:#FFFFFF;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;filter:url(#chalk);opacity:.92}
.giz .lny{fill:none;stroke:#FFE066;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;filter:url(#chalk)}
.giz .lnp{fill:none;stroke:#FF8FAB;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;filter:url(#chalk)}
.giz .hw{position:absolute;font-family:Caveat,cursive;font-weight:700;color:#FFFFFF;line-height:1.05;white-space:nowrap}
.giz .hw.y{color:#FFE066}
.giz .hw.p{color:#FF8FAB}
.giz .hw.b{color:#9ED8F5}
.giz .du{position:absolute;width:6px;height:6px;border-radius:50%;background:#FFFFFF}
.giz .sty{color:#D8E8DA;right:34px;bottom:28px}
.giz .il-l{background:#FFE066;color:#101013;right:34px;top:32px}
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

# ---------- 1 · capa em QUADRINHO pop art: cliente, vendedor, a IA "sopra" a venda ----------
def pessoa(x, y, cor, s=1.0):
    # boneco simples de HQ: cabeça, corpo, contorno grosso
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-60 210 C-60 120,60 120,60 210 Z" fill="{cor}" stroke="#101013" stroke-width="7" stroke-linejoin="round"/>'
            f'<circle cx="0" cy="62" r="52" fill="#FFE8D1" stroke="#101013" stroke-width="7"/>'
            f'<circle cx="-18" cy="58" r="6" fill="#101013"/><circle cx="18" cy="58" r="6" fill="#101013"/>'
            f'<path d="M-16 86 Q0 98 16 86" fill="none" stroke="#101013" stroke-width="5" stroke-linecap="round"/></g>')
def estrela(x, y, r, cor, d):
    import math
    pts = ' '.join(f'{x + (r if k % 2 == 0 else r * .5) * math.cos(math.pi * k / 8):.1f},{y + (r if k % 2 == 0 else r * .5) * math.sin(math.pi * k / 8):.1f}' for k in range(16))
    return f'<polygon points="{pts}" fill="{cor}" stroke="#101013" stroke-width="5" style="transform-origin:{x}px {y}px;animation:pop .4s {d}s both"/>'
q1 = (f'<div class="qd a" style="left:34px;top:62px;width:410px;height:520px;animation:slamL .6s .2s both">'
      f'<svg class="sv" viewBox="0 0 410 540">{pessoa(205, 300, "#E63946", 1.05)}'
      f'<path d="M150 330 L130 300 M260 330 L280 300 M205 318 L205 286" stroke="#101013" stroke-width="5" stroke-linecap="round" style="animation:fade .2s 1.2s both"/>'
      f'<rect x="60" y="500" width="290" height="40" fill="#FFFFFF" stroke="#101013" stroke-width="6"/></svg>'
      f'<span class="cap">A CLIENTE</span></div>'
      f'<div class="bl t" style="left:60px;top:140px;width:330px;animation:pop .45s 1.0s both, wob 1.6s 1.5s infinite ease-in-out">QUERO UMA GELADEIRA… MAS O DINHEIRO <em>TÁ CURTO!</em></div>')
q2 = (f'<div class="qd b" style="left:476px;top:62px;width:410px;height:520px;animation:slamR .6s .7s both">'
      f'<svg class="sv" viewBox="0 0 410 540">{pessoa(150, 300, "#1D4ED8", 1.05)}'
      f'<g style="transform-origin:284px 440px;animation:buzz .12s 2.6s 14 linear">'
      f'<rect x="232" y="356" width="104" height="170" rx="16" fill="#101013"/>'
      f'<rect x="244" y="372" width="80" height="120" rx="8" fill="#FFD23F"/>'
      f'<text x="284" y="446" text-anchor="middle" font-family="Bangers" font-size="40" fill="#E63946">IA</text></g>'
      f'<path d="M350 380 L378 368 M352 420 L384 420 M350 460 L378 472" stroke="#101013" stroke-width="6" stroke-linecap="round" style="animation:fade .1s 2.6s both, blinkS .24s 2.6s 7"/></svg>'
      f'<span class="cap">O VENDEDOR</span></div>'
      f'<div class="bl tr" style="left:500px;top:140px;width:360px;font-size:34px;animation:pop .45s 2.0s both">"DIGITA O CPF DELA: A IA ME DIZ O QUE <em>CABE NO BOLSO.</em>"</div>'
      f'<svg class="star" style="left:0;top:0;width:920px;height:660px;pointer-events:none" viewBox="0 0 920 660">{estrela(760, 336, 74, "#FFFFFF", 2.7)}</svg>'
      f'<div class="bum" style="left:676px;top:282px;animation:pop .4s 2.8s both, shake .5s 3.2s 4 both">BIP!</div>')
PAGS.append((6.5, page('1/6', 'NA PRÁTICA', TB('A Casas Bahia pôs uma IA para soprar a venda no ouvido de <em>mais de 10 mil vendedores.</em>') + TP('Chama Bah.IA. Te mostro como funciona ↓'),
    f'<div class="hq cena"><div class="rays"></div><div class="dotsr"></div><div class="zoom">{q1}{q2}</div>{IL}{FB}<span class="sty">ESTILO · QUADRINHO</span></div>', 'Arraste →')))

# ---------- 2 · FLAT VECTOR: CPF → 3 fontes de dados ----------
ICO = lambda c: [f'<svg width="38" height="38" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><circle cx="20" cy="13" r="7"/><path d="M6 36 C6 24 34 24 34 36"/></svg>',
                  f'<svg width="38" height="38" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round"><circle cx="17" cy="17" r="11"/><path d="M25 25 L36 36"/></svg>',
                  f'<svg width="38" height="38" viewBox="0 0 40 40" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6 H9 L13 27 H32 L36 12 H11"/><circle cx="15" cy="34" r="2.5"/><circle cx="30" cy="34" r="2.5"/></svg>']
CORES = ['#4D7CFE', '#1FB5A9', '#FF6B6B']
srcs = [('Perfil', 'quem é o cliente'), ('Navegação', 'o que ele olhou no site'), ('Compras', 'o que já levou antes')]
fl = ''.join(f'<span class="blob" style="left:{x}px;top:{y}px;width:{w}px;height:{w}px;background:{c};opacity:.22;animation:float {t}s {-t / 3:.1f}s infinite ease-in-out"></span>'
             for x, y, w, c, t in [(-60, 420, 260, '#FFC93C', 6), (700, -80, 240, '#4D7CFE', 7), (330, 520, 140, '#FF6B6B', 5), (820, 470, 120, '#1FB5A9', 6)])
fl += (f'<div class="ph" style="animation:bounceIn 1s .1s both"><div class="scr"></div><span class="cpf">CPF DO CLIENTE</span>'
       f'<span class="in" style="--W:180px;animation:typ 1s 1.0s both steps(14)">123.456.789-00</span>'
       f'<span class="bt" style="animation:fade .3s .8s both, press .35s 2.1s both">Consultar</span>'
       f'<span class="ok" style="animation:pop .4s 4.6s both">✓ histórico carregado</span></div>')
fl += '<svg class="sv" viewBox="0 0 920 660">'
for k in range(3):
    y = 120 + 150 * k + 54
    fl += f'<path d="M312 330 C 360 330, 360 {y}, 418 {y}" fill="none" stroke="{CORES[k]}" stroke-width="6" stroke-linecap="round" stroke-dasharray="4 14" style="animation:fade .3s {2.3 + .1 * k:.2f}s both"/>'
fl += '</svg>'
for k, (t, s) in enumerate(srcs):
    y = 120 + 150 * k
    d = 2.9 + .5 * k
    yy = y + 54
    for j in range(3):
        fl += f'<span class="pk" style="background:{CORES[k]};offset-path:path(\'M312 330 C 360 330, 360 {yy}, 418 {yy}\');animation:travel .7s {2.3 + .25 * j + .15 * k:.2f}s both linear"></span>'
    fl += f'<div class="src" style="top:{y}px;background:{CORES[k]};animation:flipIn .6s {d:.2f}s both cubic-bezier(.2,.8,.2,1)"><i>{ICO(CORES[k])[k]}</i><div><b>{t}</b><span>{s}</span></div></div>'
PAGS.append((6.0, page('2/6', None, TB('1. O vendedor digita o CPF. <em>A IA lê o histórico do cliente.</em>') + TP('Perfil, o que ele olhou no site e o que já comprou.'),
    f'<div class="flat cena">{fl}{IL}{FB}<span class="sty">ESTILO · FLAT VECTOR</span></div>', 'Arraste →')))

# ---------- 3 · TRAÇO NEON synthwave: a tela que volta para o vendedor ----------
tela = 'M300 30 L620 30 Q650 30 650 60 L650 570 Q650 600 620 600 L300 600 Q270 600 270 570 L270 60 Q270 30 300 30 Z'
NEON = ['#FF2BD6', '#FFE600', '#39FF14']
cards = [(96, 'Cabe no bolso', 'geladeira X em 12x, perto do limite dela'), (256, 'Como abordar', 'ela olhou 3 modelos de 2 portas'), (416, 'Compare com', 'o modelo que ela salvou no site')]
gl = '<div class="sun"></div><div class="floor"></div>'
gl += f'<svg class="sv" viewBox="0 0 920 660"><path class="ph" d="{tela}" style="--L:2000;stroke-dasharray:2000;animation:draw 1.2s .2s both ease-in-out"/>'
gl += '<path d="M420 60 L500 60" stroke="#00F0FF" stroke-width="4" stroke-linecap="round" style="animation:fade .2s 1.3s both"/>'
for k, (y, t, s) in enumerate(cards):
    gl += f'<rect class="cd" x="296" y="{y}" width="328" height="140" rx="16" stroke="{NEON[k]}" color="{NEON[k]}" style="--L:940;stroke-dasharray:940;animation:draw .6s {1.6 + .7 * k:.2f}s both ease-in-out, neonOn .8s {2.2 + .7 * k:.2f}s both"/>'
gl += '</svg>'
gl += '<div class="scan" style="animation:scan 1.4s 1.3s 2 linear both"></div>'
for k, (y, t, s) in enumerate(cards):
    d = 2.0 + .7 * k
    gl += f'<div class="gn" style="left:318px;top:{y + 18}px;font-size:22px;color:{NEON[k]};text-shadow:0 0 12px {NEON[k]};animation:fade .3s {d:.2f}s both">0{k + 1}</div>'
    gl += f'<div class="gt" style="left:318px;top:{y + 48}px;width:290px;font-size:27px;line-height:1.15;animation:wipe .5s {d + .1:.2f}s both, glitch 1.2s {d + .8:.2f}s 1">{t}</div>'
    gl += f'<div class="gs" style="left:318px;top:{y + 84}px;width:290px;font-size:19px;line-height:1.25;animation:wipe .6s {d + .3:.2f}s both">{s}</div>'
gl += '<div class="side" style="left:40px;top:230px;color:#00F0FF;text-shadow:0 0 14px #00F0FF;animation:neonOn 1s 4.2s both">em<br>segundos</div>'
gl += '<div class="side" style="left:690px;top:230px;color:#FF2BD6;text-shadow:0 0 14px #FF2BD6;animation:neonOn 1s 4.6s both">no<br>WhatsApp</div>'
PAGS.append((6.5, page('3/6', None, TB('2. A IA sugere <em>o que oferecer e como falar.</em>') + TP('Produto certo para o bolso e o perfil, abordagem e comparação.'),
    f'<div class="glow cena">{gl}{EX}{FB}<span class="sty">ESTILO · TRAÇO NEON</span></div>', 'Arraste →')))

# ---------- 4 · PIXEL ART tela de jogo: o que a empresa diz que mudou ----------
nums = [('10MIL+', 'vendedores usam o copiloto', 'Casas Bahia (CTO e CEO)', '#FFE600', 100, 'PLAYERS'),
        ('+40%', 'de produtividade nas lojas físicas', 'CEO Renato Franklin, ao NeoFeed (ago/2026)', '#3AB54A', 70, 'LEVEL UP!'),
        ('+50%', 'de conversão nas vendas pelo WhatsApp', 'CTO Filipe Jaske, à Baguete (set/2025) · canal todo', '#FF4D6D', 80, 'COMBO!')]
px = ''.join(f'<i class="cl" style="left:{x}px;top:{y}px;animation:float {t}s infinite ease-in-out"></i>' for x, y, t in [(90, 22, 7), (560, 34, 9)])
px += '<div class="ground"></div>'
for k, (n, d, s, c, w, lv) in enumerate(nums):
    t0 = .4 + 1.2 * k
    top = 52 + 160 * k
    px += (f'<div class="bx" style="top:{top}px;border-color:{c};animation:pop .45s {t0:.2f}s both steps(4)">'
           f'<span class="n" style="color:{c};animation:fade .01s {t0 + .3:.2f}s both, blinkS .2s {t0 + .3:.2f}s 3 steps(1)">{n}</span>'
           f'<span class="bar"><i style="--W:{w}%;background:{c};animation:fillB .9s {t0 + .4:.2f}s both steps(10)"></i></span>'
           f'<div class="d" style="animation:fade .01s {t0 + .7:.2f}s both">{d}<small>{s}</small></div></div>'
           f'<span class="lv" style="right:58px;top:{top - 14}px;animation:pop .3s {t0 + 1.0:.2f}s both steps(3)">{lv}</span>')
    px += ''.join(f'<i class="cn" style="left:{200 + 40 * j}px;top:{top + 20}px;animation:coin .6s {t0 + .9 + .12 * j:.2f}s both steps(6)"></i>' for j in range(3))
PAGS.append((6.5, page('4/6', None, TB('3. O que a Casas Bahia <em>diz que mudou.</em>') + TP('Números da própria empresa, sem auditoria de fora.'),
    f'<div class="pixel cena">{px}{FB}<span class="sty">ESTILO · PIXEL ART</span></div>', 'Arraste →')))

# ---------- 5 · QUADRO DE GIZ (lousa verde, giz colorido): no seu negócio ----------
filt = ('<filter id="chalk"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter>')
passos = [('Cadastre quem compra', '(nome e WhatsApp)', 'b'), ('Anote o que levou e quando', '(planilha já serve)', 'p'), ('Aí a IA sugere a próxima venda', '', 'y')]
gz = f'<svg class="sv" viewBox="0 0 920 660">{filt}'
gz += path('M62 114 L540 114', 'lny', 1.2, .5, 520)
for k in range(3):
    y = 220 + 120 * k
    gz += f'<rect class="ln" x="62" y="{y - 34}" width="46" height="46" style="--L:200;stroke-dasharray:200;animation:draw .35s {1.5 + 1.0 * k:.2f}s both"/>'
    if k < 2:
        gz += path(f'M70 {y - 12} L84 {y + 4} L108 {y - 40}', 'lny', 2.3 + 1.0 * k, .3, 90)
gz += path('M120 448 C 120 394, 870 394, 870 448 C 870 506, 120 506, 126 442', 'lnp', 4.3, .8, 1700)
gz += path('M890 560 C 860 520, 830 500, 790 498 M808 482 L788 498 L810 512', 'lnp', 5.1, .5, 300)
gz += '</svg>'
gz += '<div class="hw" style="left:62px;top:48px;font-size:58px;animation:wipe .9s .3s both steps(18)">E no seu negócio?</div>'
for k, (t, s, c) in enumerate(passos):
    y = 220 + 120 * k
    d = 1.6 + 1.0 * k
    gz += f'<div class="hw {c}" style="left:130px;top:{y - 46}px;font-size:{50 if k < 2 else 54}px;animation:wipe .8s {d:.2f}s both steps(16)">{t} <span style="font-size:34px;color:#D8E8DA">{s}</span></div>'
    gz += ''.join(f'<i class="du" style="left:{140 + 70 * j + 30 * k}px;top:{y + 4}px;--dx:{(-1) ** j * 12}px;animation:dust .8s {d + .1 * j:.2f}s both"></i>' for j in range(5))
gz += '<div class="hw" style="left:62px;top:552px;font-size:42px;animation:wipe 1s 5.4s both steps(20)">sem histórico, nenhuma IA adivinha nada.</div>'
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
