#!/usr/bin/env python3
"""@lucasgiordane · 26/11/2026 · Reels (1080x1920) "58 empresas, IA e emprego", versão em vídeo do carrossel.
Uso: python3 -I gerar-reels.py <saida> <blobs> <fontes> [png]
Sem áudio: a música entra pelo app/Edits. Primeiro quadro = cena 1 pronta (capa do Reels no perfil).
Área segura: conteúdo entre y=260 e y=1500 (topo e rodapé ficam sob a interface do Instagram).
Fontes: Anthropic, "Working with AI" (23/11/2026); Anthropic, "Labor market impacts of AI" (mar/2026, atual. 13/11/2026), ranking via CBS News."""
import os, sys, base64, glob, subprocess, shutil
from playwright.sync_api import sync_playwright
OUT, BLOBS, FONTES = sys.argv[1:4]
SOPNG = len(sys.argv) > 4 and sys.argv[4] == 'png'
os.makedirs(OUT, exist_ok=True)
FPS = 30

def b64(p): return base64.b64encode(open(p, 'rb').read()).decode()
faces = []
for fam, pat, ws in [('Manrope', 'manrope/files/manrope-latin-{w}-normal.woff2', [600, 700, 800]),
                     ('Inter', 'inter/files/inter-latin-{w}-normal.woff2', [400, 500, 600, 700]),
                     ('IBM Plex Mono', 'ibm-plex-mono/files/ibm-plex-mono-latin-{w}-normal.woff2', [500, 600])]:
    for w in ws:
        faces.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64(os.path.join(FONTES, pat.format(w=w)))}) format('woff2');}}")
AV = 'data:image/jpeg;base64,' + b64(glob.glob(os.path.join(BLOBS, 'a0000000000000000000000000000004.*'))[0])

CSS = """
body{background:#101013}
.rl{width:1080px;height:1920px;box-sizing:border-box;position:relative;overflow:hidden;background:#101013;color:#F5F5F5;font-family:Inter,sans-serif}
.rl:before{content:'';position:absolute;right:-120px;top:-60px;width:520px;height:520px;background:repeating-linear-gradient(60deg,transparent 0 38px,rgba(221,169,79,.10) 38px 40px)}
.hd{position:absolute;left:80px;top:250px;display:flex;align-items:center;gap:18px}
.hd img{width:84px;height:84px;border-radius:50%;object-fit:cover;border:3px solid #DDA94F}
.hd b{display:block;font-family:Manrope,sans-serif;font-weight:800;font-size:34px}
.hd span{font-size:26px;color:#A5A8AE}
.ct{position:absolute;left:80px;right:80px;top:400px;bottom:520px;display:flex;flex-direction:column;justify-content:center;gap:40px}
.tg{align-self:flex-start;font-weight:700;font-size:28px;letter-spacing:.18em;color:#101013;background:#DDA94F;border-radius:4px;padding:8px 16px}
.tt{margin:0;font-family:Manrope,sans-serif;font-weight:800;font-size:76px;line-height:1.12}
.tt em{font-style:normal;color:#DDA94F}
.st{margin:0;font-size:42px;line-height:1.35;color:#D9DBDF}
.fonte{position:absolute;left:80px;right:80px;bottom:440px;font-family:'IBM Plex Mono',monospace;font-size:22px;color:#7C808A}
.lg{position:absolute;left:80px;bottom:380px;font-weight:600;letter-spacing:.24em;font-size:22px;color:#5B6070}
.dots{display:grid;grid-template-columns:repeat(10,1fr);gap:14px;width:720px}
.dots i{display:block;aspect-ratio:1;border-radius:50%;background:#3C4149}
.dots i.on{background:#EF4444;box-shadow:0 0 0 7px rgba(239,68,68,.25)}
.big{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:260px;line-height:.9;color:#DDA94F}
.thirds{display:flex;gap:18px}
.thirds div{flex:1;height:300px;border-radius:16px;background:#F4F1EA;color:#101013;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px;text-align:center;padding:0 12px}
.thirds div.g{background:#DDA94F}
.thirds b{font-family:Manrope,sans-serif;font-weight:800;font-size:38px;line-height:1.1}
.thirds span{font-size:24px}
.quote{background:#F4F1EA;color:#101013;border-radius:18px;padding:44px 44px;font-family:Manrope,sans-serif;font-weight:800;font-size:64px;line-height:1.15;border-left:14px solid #DDA94F}
.quote small{display:block;margin-top:20px;font-family:Inter,sans-serif;font-weight:500;font-size:28px;color:#3C4149}
.cb{display:flex;flex-direction:column;gap:12px}
.cb .cl{display:flex;justify-content:space-between;align-items:baseline;gap:20px}
.cb .cl span{font-size:36px;line-height:1.2}
.cb .cl b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:64px;color:#F4F1EA}
.cb .tr{height:44px;border-radius:10px;background:#2A2D33;overflow:hidden}
.cb .tr i{display:block;height:100%;border-radius:10px;background:#F4F1EA;transform-origin:left center}
.cb.g .cl b{color:#DDA94F}
.cb.g .tr i{background:#DDA94F}
.kw{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:110px;color:#DDA94F;white-space:nowrap;overflow:hidden;border-right:6px solid #DDA94F;animation:type 1.1s 1.2s steps(11) both, caret .6s 2.3s 3 both;align-self:flex-start}
@keyframes type{from{width:0}to{width:11.6ch}}
@keyframes caret{50%{border-color:transparent}}
.dm{background:#2A2416;border:1px solid #A6752D;border-radius:18px;padding:26px 30px;font-size:36px;line-height:1.35}
.dm small{display:block;font-family:'IBM Plex Mono',monospace;font-size:22px;color:#DDA94F;margin-bottom:6px}
@keyframes inL{from{opacity:0;transform:translateX(-60px)}to{opacity:1;transform:none}}
@keyframes inUp{from{opacity:0;transform:translateY(50px)}to{opacity:1;transform:none}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:scale(1)}}
"""
def A(name, dur, delay): return f'style="animation:{name} {dur}s {delay}s both cubic-bezier(.2,.8,.2,1)"'
HD = f'<div class="hd"><img src="{AV}" alt=""><div><b>Lucas Giordane</b><span>@lucasgiordane</span></div></div>'
FWA = '<span class="fonte">Fonte: Anthropic, "Working with AI" · 23/11/2026 · 58 empresas clientes, EUA</span>'
FLM = '<span class="fonte">Fonte: Anthropic, "Labor market impacts of AI" (mar/2026, atual. 13/11), via CBS News</span>'
def cena(conteudo, fonte=''):
    return f'<div class="rl">{HD}<div class="ct">{conteudo}</div>{fonte}<span class="lg">SOLID BUSINESS</span></div>'

C = []
# 1 · gancho (também é a capa)
dots = ''.join(f'<i class="{"on" if k in (23, 46) else ""}" style="animation:{"pop" if k in (23, 46) else "fade"} .4s {(2.2 + (.4 if k == 46 else 0)) if k in (23, 46) else .8 + k * .02:.2f}s both"></i>' for k in range(58))
C.append((4.5, cena(f'<span class="tg" {A("pop", .4, .1)}>IA E EMPREGO</span><p class="tt" {A("inUp", .5, .2)}>A Anthropic foi a 58 empresas. <em>Quase ninguém foi demitido pela IA.</em></p><div class="dots">{dots}</div>', FWA)))
# 2 · 2 de 58
C.append((4.0, cena(f'<div class="big" {A("pop", .5, .2)}>2/58</div><p class="tt" style="font-size:64px" {A("inUp", .5, .8)}>empresas tiveram um cargo <em>eliminado pela IA</em>, com demissão.</p>', FWA)))
# 3 · 2 de cada 3
th = ''.join(f'<div class="{"g" if k < 2 else ""}" {A("pop", .45, 1.0 + .35 * k)}><b>{"contrata<br>menos" if k < 2 else "o resto"}</b><span>{"por causa da IA" if k < 2 else "sem queda"}</span></div>' for k in range(3))
C.append((4.5, cena(f'<p class="tt" {A("inUp", .5, .2)}>Mas em <em>2 de cada 3</em>, a contratação caiu.</p><div class="thirds">{th}</div><p class="st" {A("fade", .5, 2.4)}>A vaga não abre. Quem sai não é reposto.</p>', FWA)))
# 4 · frase
C.append((4.5, cena(f'<div class="quote" {A("inUp", .6, .2)}>"A gente pode não estar demitindo, mas não está contratando."<small>Entrevistado anônimo do estudo</small></div>', FWA)))
# 5 · quem sente
cnt = [('Cortaram terceirizados', 9, 'g'), ('Tiraram quem recusou usar IA', 5, 'g'), ('Contrataram mais (IA e TI)', 10, '')]
bs = ''.join(f'<div class="cb {c}" {A("fade", .4, .7 + .7 * i)}><div class="cl"><span>{n}</span><b>{v}</b></div><div class="tr"><i style="width:{v * 10}%;animation:grow .7s {.9 + .7 * i}s both cubic-bezier(.2,.8,.2,1)"></i></div></div>' for i, (n, v, c) in enumerate(cnt))
C.append((5.0, cena(f'<p class="tt" {A("inUp", .5, .2)}>Quem mais sente: <em>o terceirizado</em> e quem recusa a IA.</p>{bs}', FWA.replace('58 empresas clientes, EUA', 'nº de empresas, de 58'))))
# 6 · profissões
rk = [('Programador', 75, 'g'), ('Atendimento ao cliente', 70, ''), ('Digitação de dados', 67, '')]
rl = ''.join(f'<div class="cb {c}" {A("fade", .4, .7 + .6 * i)}><div class="cl"><span>{n}</span><b>{v}%</b></div><div class="tr"><i style="width:{v}%;animation:grow .7s {.9 + .6 * i}s both cubic-bezier(.2,.8,.2,1)"></i></div></div>' for i, (n, v, c) in enumerate(rk))
C.append((5.0, cena(f'<p class="tt" {A("inUp", .5, .2)}>Onde a IA já faz <em>mais tarefas</em>:</p>{rl}<p class="st" {A("fade", .5, 3.0)}>Perto de zero: cozinheiro, mecânico, bartender.</p>', FLM)))
# 7 · CTA
C.append((5.5, cena(f'<p class="tt" {A("inUp", .5, .2)}>Na sua empresa, a próxima vaga vai ser <em>de gente ou de IA?</em></p><span class="st" {A("fade", .4, .9)}>Comenta</span><b class="kw">DIAGNÓSTICO</b><div class="dm" {A("inUp", .5, 3.0)}><small>direct · lucasgiordane</small>Te chamo no direct e a gente olha o seu caso.</div>', '<span class="fonte">Amostra: empresas clientes da Anthropic nos EUA, não o mercado todo.</span>')))

fr = os.path.join(OUT, 'quadros-reels'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
n = 0
with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    for i, (dur, body) in enumerate(C, 1):
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{"".join(faces)}{CSS}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden}}</style></head><body>{body}</body></html>')
        pg.evaluate('document.fonts.ready')
        if SOPNG:
            pg.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {dur * 1000 - 1}; }})')
            pg.screenshot(path=os.path.join(OUT, f'reels-cena-{i:02d}.png'))
            continue
        for f in range(int(FPS * dur)):
            t = dur * 1000 - 1 if (i == 1 and f == 0) else f * 1000 / FPS   # capa: 1º quadro = cena 1 pronta
            pg.evaluate(f'document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {t}; }})')
            pg.screenshot(path=os.path.join(fr, f'{n:05d}.png')); n += 1
    br.close()
if not SOPNG:
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(fr, '%05d.png'),
                    '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', os.path.join(OUT, 'reels.mp4')], check=True)
shutil.rmtree(fr)
print('ok', n / FPS, 's')
