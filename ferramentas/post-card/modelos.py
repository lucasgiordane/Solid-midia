#!/usr/bin/env python3
"""5 modelos de post-card do @lucasgiordane (capa + 1 página interna em alguns) e a página final de CTA."""
import os, sys, base64, glob
from playwright.sync_api import sync_playwright
OUT, CSSF, BLOBS, FONTES = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
def b64(p): return base64.b64encode(open(p, 'rb').read()).decode()
faces = []
for fam, pat, ws in [('Manrope', 'manrope/files/manrope-latin-{w}-normal.woff2', [500, 600, 700, 800]),
                     ('Inter', 'inter/files/inter-latin-{w}-normal.woff2', [400, 500, 600, 700]),
                     ('IBM Plex Mono', 'ibm-plex-mono/files/ibm-plex-mono-latin-{w}-normal.woff2', [400, 500, 600])]:
    for w in ws:
        faces.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64(os.path.join(FONTES, pat.format(w=w)))}) format('woff2');}}")
AV = 'data:image/jpeg;base64,' + b64(glob.glob(os.path.join(BLOBS, 'a0000000000000000000000000000004.*'))[0])
CSS = open(CSSF).read() + """
/* cabeçalho no estilo do modelo de referência: nome grande, @ abaixo, sem selo */
.pc .av{width:116px;height:116px;border:0}
.pc .nm b{font-size:44px;letter-spacing:-0.01em}
.pc .nm span{font-size:32px;color:#5B6070}
.pc .tx{margin-top:40px}
.pc .tp{font-size:43px;line-height:1.36;color:#101013}
.pc .tb{font-size:46px}
.pc .mi{padding:30px 32px}
.pc .cr{margin-top:12px;font-size:22px;color:#5B6070}
.k{font-family:'IBM Plex Mono',monospace}
/* 1 · notícia */
.nw{background:#FFFFFF;border-radius:12px;padding:26px 28px;color:#101013;display:flex;flex-direction:column;gap:14px}
.nw .src{display:flex;align-items:center;gap:12px;font-size:20px;color:#3C4149}
.nw .src i{width:34px;height:34px;border-radius:8px;background:#1351B4;display:block}
.nw h4{margin:0;font-family:Manrope,sans-serif;font-weight:800;font-size:34px;line-height:1.2;color:#1351B4}
.nw p{margin:0;font-size:22px;color:#3C4149;line-height:1.4}
.nw .ln{height:1px;background:#E2DCCF}
.nw small{font-size:18px;color:#5B6070}
/* 2 · agentes por setor */
.ag4{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.ag4 div{background:#1E2025;border:1px solid #3C4149;border-radius:14px;padding:20px;display:flex;flex-direction:column;gap:10px}
.ag4 div i{width:56px;height:56px;border-radius:12px;background:#DDA94F;display:flex;align-items:center;justify-content:center;font-style:normal;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:26px;color:#101013}
.ag4 div b{font-family:Manrope,sans-serif;font-weight:700;font-size:27px;color:#F5F5F5}
.ag4 div small{font-size:19px;color:#A5A8AE;line-height:1.3}
.dash{background:#F4F1EA;border-radius:12px;padding:20px 22px;color:#101013}
.dash .t{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.dash .t b{font-family:Manrope,sans-serif;font-weight:800;font-size:24px}
.dash .t span{font-family:'IBM Plex Mono',monospace;font-size:16px;color:#6D28D9;border:1.5px solid #A78BFA;border-radius:6px;padding:3px 8px}
.dash .kp{display:flex;gap:14px;margin-bottom:14px}
.dash .kp div{flex:1;background:#FFFFFF;border:1px solid #E2DCCF;border-radius:10px;padding:12px 14px}
.dash .kp small{display:block;font-size:16px;color:#3C4149}
.dash .kp b{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:40px}
.dash .row{display:grid;grid-template-columns:1fr 150px 120px;align-items:center;padding:10px 4px;border-bottom:1px solid #E2DCCF;font-size:20px}
.ok{font-family:'IBM Plex Mono',monospace;font-size:15px;color:#FFFFFF;background:#15803D;border-radius:5px;padding:3px 8px;justify-self:start}
.wt{font-family:'IBM Plex Mono',monospace;font-size:15px;color:#101013;background:#F59E0B;border-radius:5px;padding:3px 8px;justify-self:start}
/* 3 · vídeo de terceiro com crédito */
.vd{position:relative;height:100%;min-height:440px;border-radius:12px;background:linear-gradient(135deg,#1E2025,#3C4149);display:flex;align-items:center;justify-content:center;overflow:hidden}
.vd .pl{width:110px;height:110px;border-radius:50%;background:rgba(245,245,245,.92);display:flex;align-items:center;justify-content:center}
.vd .pl:after{content:"";border-left:36px solid #101013;border-top:22px solid transparent;border-bottom:22px solid transparent;margin-left:10px}
.vd .bar{position:absolute;left:24px;right:24px;bottom:22px;height:6px;border-radius:3px;background:#5B6070}
.vd .bar i{display:block;width:38%;height:100%;border-radius:3px;background:#DDA94F}
.vd .lab{position:absolute;top:20px;left:22px;font-family:'IBM Plex Mono',monospace;font-size:18px;color:#F5F5F5;background:rgba(16,16,19,.7);border-radius:6px;padding:6px 10px}
/* 4 · faz a conta */
.fn{display:flex;flex-direction:column;gap:14px}
.fn .r{display:grid;grid-template-columns:230px 1fr 110px;align-items:center;gap:16px}
.fn .r span{font-size:23px;color:#F5F5F5}
.fn .r div{height:54px;border-radius:8px;background:#2A2D33;overflow:hidden}
.fn .r div i{display:block;height:100%;background:#DDA94F;border-radius:8px}
.fn .r div i.l{background:#5B6070}
.fn .r b{font-family:'IBM Plex Mono',monospace;font-size:32px;color:#DDA94F;text-align:right}
.fn .gp{margin-top:8px;display:flex;align-items:center;gap:14px;font-size:24px;color:#F5F5F5;background:#2A2416;border:1px solid #A6752D;border-radius:12px;padding:14px 18px}
.fn .gp b{font-family:'IBM Plex Mono',monospace;font-size:36px;color:#DDA94F}
/* 5 · raio-x do processo */
.lanes{display:flex;flex-direction:column;gap:10px}
.lane{display:grid;grid-template-columns:150px 1fr;gap:12px;align-items:center}
.lane > span{font-family:Inter,sans-serif;font-weight:600;font-size:17px;letter-spacing:.12em;color:#A5A8AE;text-transform:uppercase}
.lane .st{display:flex;gap:10px;align-items:center}
.lane .st div{background:#F4F1EA;border-radius:10px;padding:12px 12px;font-family:Manrope,sans-serif;font-weight:700;font-size:19px;color:#101013;white-space:nowrap}
.lane .st div.gg{background:#FEE2E2;outline:3px solid #EF4444}
.lane .st i{color:#DDA94F;font-style:normal;font-size:24px}
.lane .st em{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:16px;color:#FCA5A5}
.gl{margin-top:14px;display:flex;align-items:center;gap:12px;font-size:22px;color:#F5F5F5}
.gl b{font-family:'IBM Plex Mono',monospace;color:#FCA5A5}
.mvv{gap:8px}.mvv .nd{background:#F4F1EA;border:0;min-height:160px;border-radius:14px}.mvv .nd b{color:#101013;font-size:23px}.mvv .nd small{color:#3C4149;font-size:16px}.mvv .nd.on{background:#DDA94F}
.mvv .ar{color:#DDA94F;font-size:30px}
.pc .flw-cap{font-size:28px;color:#F5F5F5;margin-top:28px}.pc .flw-cap b{color:#DDA94F}
/* CTA */
.cl{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr 1fr;gap:8px;height:100%;min-height:380px}
.cl div{border-radius:8px;background:#1E2025;border:1px solid #3C4149;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:44px;color:#DDA94F}
.cl div.w{background:#F4F1EA;color:#A6752D}
"""
def page(tag, texto, media, cred=''):
    tg = f'<span class="tg">{tag}</span>' if tag else ''
    cr = f'<div class="cr">{cred}</div>' if cred else ''
    return f'''<div class="pc">
<div class="au2"><img class="av" src="{AV}" alt=""><div class="nm"><b>Lucas Giordane</b><span>@lucasgiordane</span></div></div>
<div class="tx">{tg}{texto}</div>
<div class="mi">{media}</div>{cr}
</div>'''
TP = lambda x: f'<p class="tp">{x}</p>'
TB = lambda x: f'<p class="tb">{x}</p>'
IL = '<span class="il-l">ILUSTRAÇÃO</span>'
EX = '<span class="il-l">EXEMPLO</span>'
P = {}
# MODELO 1 · É OFICIAL (notícia → impacto no negócio)
P['m1-capa'] = page('É OFICIAL', TP('A Receita Federal liberou o código da calculadora dos novos impostos da Reforma Tributária.') + TB('O que muda no seu negócio, em 3 pontos ↓'),
    '<div class="nw"><div class="src"><i></i>Agência Gov · 16/11/2026</div><h4>Receita abre código-fonte para empresas usarem no cálculo de tributos de consumo</h4><div class="ln"></div><p>Primeira vez que a Receita publica um software no GitHub: a Calculadora de Tributos, que segue as regras da CBS.</p><small>Fonte oficial · link na legenda</small></div>',
    'Fonte: Agência Gov (16/11/2026)')
P['m1-interna'] = page(None, TB('1. O sistema que emite a sua nota pode calcular o imposto <em>do mesmo jeito que a Receita.</em>') + TP('Pergunte ao seu fornecedor de sistema quando ele vai usar a calculadora oficial.'),
    IL + '<div class="flw mvv"><div class="nd"><b>Venda</b><small>no caixa</small></div><span class="ar">→</span><div class="nd on"><b>Calculadora</b><small>código da Receita</small></div><span class="ar">→</span><div class="nd"><b>Nota fiscal</b><small>com CBS e IBS</small></div><span class="ar">→</span><div class="nd"><b>Contador</b><small>confere</small></div></div><p class="flw-cap">Menos erro de cálculo, <b>menos retrabalho com o contador.</b></p>')
# MODELO 2 · SE EU TIVESSE (agentes por setor)
P['m2-capa'] = page('NA PRÁTICA', TP('Se eu tivesse uma oficina mecânica hoje,') + TB('estes são os 4 agentes de IA que eu colocaria para trabalhar ↓'),
    IL + '<div class="ag4"><div><i>01</i><b>Orçamento</b><small>monta pelo relato e pela tabela de peças</small></div><div><i>02</i><b>Peças</b><small>cota 3 fornecedores e avisa o mais barato</small></div><div><i>03</i><b>Revisão</b><small>chama o cliente 6 meses depois</small></div><div><i>04</i><b>Cobrança</b><small>lembra antes do vencimento</small></div></div>')
P['m2-interna'] = page(None, TB('3. Agente de revisão: chama o cliente <em>6 meses depois</em> do serviço.') + TP('No exemplo, 38 clientes avisados no mês e 14 carros de volta na oficina, sem ninguém pegar o telefone.'),
    EX + '<div class="dash"><div class="t"><b>Revisões · novembro</b><span>● Agente · IA</span></div><div class="kp"><div><small>avisados</small><b>38</b></div><div><small>agendaram</small><b>14</b></div><div><small>retorno estimado</small><b>R$ 9.800</b></div></div><div class="row"><span>Gol 2018 · troca de óleo</span><span class="k">há 6 meses</span><span class="ok">agendou</span></div><div class="row"><span>HB20 2021 · freios</span><span class="k">há 6 meses</span><span class="wt">aguarda</span></div><div class="row"><span>Onix 2020 · revisão</span><span class="k">há 7 meses</span><span class="ok">agendou</span></div></div>')
# MODELO 3 · CURIOSIDADE (vídeo de terceiro com crédito)
P['m3-capa'] = page('CURIOSIDADE', TP('Tem gente montando em uma tarde sistemas que levavam meses para ficar prontos.') + TB('Separei 5 que servem para pequeno negócio ↓'),
    '<div class="vd"><span class="lab">vídeo · 0:38</span><div class="pl"></div><div class="bar"><i></i></div></div>',
    '🎥 crédito: @perfil-de-origem (sempre com permissão ou de fonte oficial)')
# MODELO 4 · FAZ A CONTA (gráfico que se monta)
P['m4-capa'] = page('FAZ A CONTA', TP('Quanto custa deixar um orçamento esperando 4 horas por resposta?') + TB('Fiz a conta com 100 orçamentos ↓'),
    EX + '<div class="fn"><div class="r"><span>Pedidos de orçamento</span><div><i style="width:100%"></i></div><b>100</b></div><div class="r"><span>Respondidos em 5 min</span><div><i style="width:27%"></i></div><b>27</b></div><div class="r"><span>Respondidos em 4 h</span><div><i class="l" style="width:18%"></i></div><b>18</b></div><div class="gp">Diferença no mês: <b>+9 vendas</b> só por responder antes</div></div>')
# MODELO 5 · RAIO-X (fluxo real com gargalo)
P['m5-capa'] = page('RAIO-X', TP('Mapeei o caminho de um pedido numa loja de material de construção.') + TB('O gargalo não estava onde o dono achava ↓'),
    IL + '<div class="lanes"><div class="lane"><span>Vendas</span><div class="st"><div>Pedido</div><i>→</i><div>Orçamento</div><i>→</i><div>Aprovação</div></div></div><div class="lane"><span>Financeiro</span><div class="st"><div class="gg">Confere Pix</div><em>espera 2 dias</em></div></div><div class="lane"><span>Estoque</span><div class="st"><div>Separa</div><i>→</i><div>Carrega</div></div></div><div class="lane"><span>Entrega</span><div class="st"><div>Rota</div><i>→</i><div>Cliente</div></div></div></div><p class="gl">Gargalo: <b>conferência manual do Pix</b> (situação de exemplo)</p>')
# CTA final (igual em todos)
P['cta'] = page('SUA VEZ', TB('Qual desses você colocaria primeiro no seu negócio?') + TP('<b>Comenta DIAGNÓSTICO</b> que eu te chamo no direct e a gente olha o seu caso. E salva para não perder.'),
    '<div class="cl"><div>01</div><div class="w">02</div><div>03</div><div class="w">04</div><div>05</div><div class="w">↓</div></div>',
    'Colagem das imagens do carrossel, como no modelo de referência')
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1350})
    for k, body in P.items():
        pg.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{"".join(faces)}{CSS}html,body{{margin:0}}</style></head><body>{body}</body></html>')
        pg.evaluate('document.fonts.ready'); pg.screenshot(path=os.path.join(OUT, f'{k}.png'))
    br.close()
print('ok')
