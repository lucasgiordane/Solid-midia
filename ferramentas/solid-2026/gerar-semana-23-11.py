#!/usr/bin/env python3
# Gera as peças da semana 23 a 29/11 no padrão do canvas Solid · Instagram
import os, sys, shutil
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SG = '<span class="sb">SOLID BUSINESS</span>'
SIMB = {'n': 'a0000000000000000000000000000001', 's': 'a0000000000000000000000000000001', 'p': 'a0000000000000000000000000000002'}
def simb(cls):
    k = 'n' if 'n' in cls.split() else ('s' if 's' in cls.split() else 'p')
    return f'<img class="simb" src="/_blob/{SIMB[k]}" alt="Símbolo Solid Business">'
DG = '<svg class="dg" aria-hidden="true" viewBox="0 0 420 440"><line x1="360" y1="440" x2="420" y2="336.1"></line><line x1="280" y1="440" x2="420" y2="197.5"></line><line x1="200" y1="440" x2="420" y2="58.9"></line></svg>'
AT = '<span class="at">@solidbusiness_</span>'
HEAD = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
<link rel="stylesheet" href="solid26.css">
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=IBM+Plex+Mono:wght@400;500;600&amp;display=swap">
<style>body{{margin:0}}</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1080,"height":{h}}}}}'>
class Component extends DCLogic {{ renderVals() {{ return {{}}; }} }}
</script>
</body>
</html>
'''
FILES = []
def w(name, title, body, h=1350):
    open(os.path.join(OUT, name), 'w').write(HEAD.format(title=title, body=body, h=h))
    FILES.append(name)

def T(a, b=None, st=''):
    s = f' style="{st}"' if st else ''
    return f'<h1 class="t"{s}>{a}' + (f' <span class="a">{b}</span>' if b else '') + '</h1>'
def P(x, st=''):
    s = f' style="{st}"' if st else ''
    return f'<p class="p"{s}>{x}</p>'
def X(*items):  # cartões com ✕
    return ''.join(f'<div class="cd row"><span class="num">✕</span><span class="ct">{i}</span></div>' for i in items)
def N(*items):  # cartões numerados
    return '<div class="col" style="gap: 14px;">' + ''.join(f'<div class="cd row"><span class="num">{k+1:02d}</span><span class="ct">{i}</span></div>' for k, i in enumerate(items)) + '</div>'
def STEPS(*items):
    return '<div class="steps">' + ''.join(f'<div class="r"><i>{k+1}</i><div class="col" style="gap: 6px;"><span class="ct">{a}</span><span class="cs">{b}</span></div></div>' for k, (a, b) in enumerate(items)) + '</div>'
CTA = lambda x: f'<span class="cta">{x}</span>'
DV = '<div class="dv"></div>'
STK = lambda x: f'<div class="stk">{x}</div>'

def sl(name, title, cls, lb, pg, inner, nx=None, ent=None, gap=28, foot=None):
    e = f'<div class="ent {ent}"></div>\n' if ent else ''
    pgs = f'<span class="pg">{pg}</span>' if pg else ''
    if foot is None:
        foot = SG + (f'<span class="nx">{nx}</span>' if nx else AT)
    body = f'''<div class="sl {cls}">
{DG}
{e}<div class="hd"><div class="hdl">{simb(cls)}</div>{pgs}</div>
<div class="md" style="gap: {gap}px;">
<span class="lb">{lb}</span>
{inner}
</div>
<div class="ft">{foot}</div>
</div>'''
    w(name, title, body)

def reel(name, title, cls, lb, pg, inner, nx=None, gap=48):
    foot = SG + (f'<span class="nx">{nx}</span>' if nx else AT)
    body = f'''<div class="sl r {cls}">
{DG}
<div class="hd"><div class="hdl">{simb(cls)}</div>{f'<span class="pg">{pg}</span>' if pg else ''}</div>
<div class="md" style="gap: {gap}px;">
<span class="lb">{lb}</span>
{inner}
</div>
<div class="ft">{foot}</div>
</div>'''
    w(name, title, body, 1920)

def story(name, title, cls, lb, inner):
    body = f'''<div class="sl r st {cls}">
{DG}
<div class="hd"><div class="hdl">{simb(cls)}</div></div>
<div class="md" style="gap: 40px;">
<span class="lb">{lb}</span>
{inner}
</div>
<div class="ft">{SG}{AT}</div>
</div>'''
    w(name, title, body, 1920)

FR_FOOT = f'<span class="nx" style="font-weight: 600; font-size: 24px;">Envia para quem precisa ler isso</span>{AT}'

# ---------- SEGUNDA 23/11 ----------
D = 's23-seg'
sl(f'{D}-c1.dc.html', 'Seg · 1 Capa', 'n fio', 'Automação · IA', '01/06',
   T('O que quase todo mundo entende errado', 'sobre IA no negócio.', 'margin-bottom: 24px;') + P('Não é a ferramenta. <b>Arrasta.</b>'), 'O erro')
sl(f'{D}-c2.dc.html', 'Seg · 2 O erro', 'n fio', 'O erro', '02/06',
   T('Comprar a ferramenta', 'antes de olhar o processo.', 'margin-bottom: 24px;') + X('Assina 3 ferramentas e usa uma', 'Ninguém sabe quem faz o quê', 'A IA repete a bagunça, só que mais rápido'), 'O custo', gap=20)
sl(f'{D}-c3.dc.html', 'Seg · 3 O custo', 'n fio', 'O custo', '03/06',
   T('Automatizar bagunça', 'só acelera a bagunça.', 'margin-bottom: 16px;') + P('Se o pedido chega pelo WhatsApp, vai para o caderno e some no meio do caminho, a IA não resolve.') + P('<b>Ela só faz o erro chegar mais rápido.</b>'), 'A ordem certa')
sl(f'{D}-c4.dc.html', 'Seg · 4 A ordem certa', 'fio', 'A ordem certa', '04/06',
   T('Primeiro o processo.', 'Depois a IA.', 'margin-bottom: 8px;') + STEPS(('Desenhe', 'Do pedido à entrega, passo a passo.'), ('Corte', 'O que ninguém usa sai antes de automatizar.'), ('Automatize', 'Só o passo que se repete toda semana.'), ('Meça', 'Um número para saber se melhorou.')), 'A virada', gap=24)
sl(f'{D}-c5.dc.html', 'Seg · 5 Virada', 'fio', 'A virada', '05/06',
   T('IA boa é a que', 'você nem percebe.', 'margin-bottom: 16px;') + P('O cliente recebe a resposta na hora, o pedido não se perde e você ganha tempo para pensar no negócio.') + P('<b>Isso vem do processo, não da ferramenta.</b>'), 'Sua vez')
sl(f'{D}-c6.dc.html', 'Seg · 6 CTA', 's fio', 'Sua vez', '06/06',
   T('Qual processo', 'você automatizaria primeiro?', 'font-size: 84px;') + DV + P('Comenta aqui. Se não souber por onde começar, eu te ajudo a olhar.') + CTA('Salva para olhar com a equipe'), gap=44)
sl(f'{D}-f1.dc.html', 'Seg · Frase', 'n', 'Frase do dia', '01/02',
   '<span class="qm">“</span>\n<p class="q">Automação não é coisa de empresa grande. É coisa de quem valoriza o próprio tempo.</p>\n<div class="col" style="gap: 10px;"><span class="au">Solid Business</span></div>', 'No seu negócio', ent='p', gap=36)
sl(f'{D}-f2.dc.html', 'Seg · Aplicação', '', 'No seu negócio', '02/02',
   T('Quanto vale', 'uma hora sua?') + P('Uma hora por dia copiando pedido, conferindo pagamento ou respondendo a mesma pergunta passa de 20 horas por mês.') + DV + P('<b>Tempo que podia ir para vender, cuidar do cliente ou descansar.</b>'), gap=40, foot=FR_FOOT)

# ---------- TERÇA 24/11 ----------
D = 's23-ter'
def CHK(items, cor=None):
    st = f' style="border-color: {cor};"' if cor else ''
    return '<div class="col" style="gap: 30px;">' + ''.join(f'<div class="row"><span class="chk"{st}></span><span class="ct">{i}</span></div>' for i in items) + '</div>'
sl(f'{D}-c1.dc.html', 'Ter · 1 Capa', '', 'Teste rápido', '01/06',
   T('Como saber se a sua empresa', 'está pronta para automatizar.', 'margin-bottom: 24px;') + P('6 sinais. <b>Conte quantos você marca.</b>'), 'Os sinais', ent='n')
sl(f'{D}-c2.dc.html', 'Ter · 2 Sinais 1 a 3', 'n', 'Sinais 1 a 3', '02/06',
   T('Marque os que', 'acontecem aí.', 'margin-bottom: 16px;') + CHK(['Você responde a mesma pergunta várias vezes por dia', 'Pedido ou orçamento já se perdeu no WhatsApp', 'Você confere pagamento um por um no extrato']), 'Mais 3', ent='p')
sl(f'{D}-c3.dc.html', 'Ter · 3 Sinais 4 a 6', '', 'Sinais 4 a 6', '03/06',
   T('Continue', 'contando.', 'margin-bottom: 16px;') + CHK(['A planilha só existe na cabeça de uma pessoa', 'Você cobra cliente atrasado de memória', 'Tirar 3 dias de folga trava a empresa']), 'O resultado', ent='s')
def FAIXA(a, b):
    return f'<div class="cd row"><span class="num" style="width: 130px;">{a}</span><span class="ct">{b}</span></div>'
sl(f'{D}-c4.dc.html', 'Ter · 4 Resultado', 's', 'O resultado', '04/06',
   T('Quantos', 'você marcou?', 'margin-bottom: 16px;') + '<div class="col" style="gap: 14px;">' + FAIXA('0–1', 'Siga como está e refaça o teste em 3 meses') + FAIXA('2–3', 'Escolha 1 processo e escreva o passo a passo') + FAIXA('4–6', 'Organize o processo antes de qualquer ferramenta. Depois, automatize') + '</div>', 'A virada', ent='p', gap=20)
sl(f'{D}-c5.dc.html', 'Ter · 5 Virada', '', 'A virada', '05/06',
   T('Cada sinal é', 'uma hora sua indo embora.', 'margin-bottom: 16px;') + P('Não é falta de ferramenta.') + P('<b>É o mesmo trabalho feito à mão, toda semana.</b>'), 'Sua vez', ent='n')
sl(f'{D}-c6.dc.html', 'Ter · 6 CTA', 'n', 'Sua vez', '06/06',
   T('Comenta o seu número', 'de 0 a 6.', 'font-size: 84px;') + DV + P('Eu te digo por onde começar no seu caso.') + CTA('Salva e refaz daqui a 1 mês'), gap=44)
sl(f'{D}-r1.dc.html', 'Ter · Trajetória 1', '', 'Projeto Solid · ReparoFit', '01/03',
   T('Você nunca viu chamado de manutenção', 'feito assim.', 'margin-bottom: 24px;') + P('Academias, condomínios, hotéis e clubes. <b>Um aviso que não pode se perder.</b>'), 'Como funciona', gap=28)
sl(f'{D}-r2.dc.html', 'Ter · Trajetória 2', '', 'Como funciona', '02/03',
   T('O aviso não se perde', 'no caminho.', 'margin-bottom: 8px;') + STEPS(('Placa com QR em cada equipamento', 'Fica no próprio aparelho.'), ('Quem vê o problema escaneia', 'Conta o que aconteceu e manda uma foto.'), ('O chamado vai para a gestão', 'E de lá para o técnico.'), ('Você acompanha cada etapa', 'Aberto, em atendimento, resolvido.')), 'A lição', gap=24)
sl(f'{D}-r3.dc.html', 'Ter · Trajetória 3', 'n', 'A lição', '03/03',
   T('Antes do sistema,', 'o caminho do aviso.', 'margin-bottom: 16px;') + P('Por trás do QR existe um processo desenhado: quem vê, quem recebe, quem resolve.') + P('<b>Primeiro o processo, depois a tecnologia.</b>') + P('reparofit.com.br', 'font-family: \'IBM Plex Mono\', monospace; color: #DDA94F;'))

# ---------- QUARTA 25/11 ----------
D = 's23-qua'
sl(f'{D}-m1.dc.html', 'Qua · 1 Capa', 'n', 'Mito × verdade', '01/04',
   T('O mito nº 1 sobre IA', 'que você ainda acredita.', 'margin-bottom: 24px;') + P('Muito dono de negócio pensa assim. <b>Arrasta.</b>'), 'O mito', gap=36)
sl(f'{D}-m2.dc.html', 'Qua · 2 Mito', 'n', 'Mito', '02/04',
   '<span class="tag" style="font-size: 28px; padding: 10px 20px;">MITO</span>' + T('“A IA vai substituir', 'o meu funcionário.”', 'margin-bottom: 8px;') + P('Aí uns compram tudo com medo de ficar para trás. Outros não testam nada com medo de errar.'), 'A verdade', gap=32)
sl(f'{D}-m3.dc.html', 'Qua · 3 Verdade', 'n', 'Verdade', '03/04',
   '<span class="tag b" style="font-size: 28px; padding: 10px 20px;">VERDADE</span>' + T('A IA tira a tarefa,', 'não a pessoa.', 'margin-bottom: 8px;') + STEPS(('Sai: copiar, conferir, repetir', 'O trabalho repetido que cansa a equipe.'), ('Fica: atender, decidir, resolver', 'O que precisa de gente.'), ('Muda: o tempo de cada um', 'Sobra hora para o que traz cliente.')), 'O que fazer', gap=24)
sl(f'{D}-m4.dc.html', 'Qua · 4 O que fazer', 'n', 'O que fazer', '04/04',
   T('Liste 3 tarefas', 'que se repetem toda semana.', 'margin-bottom: 8px;') + P('É por elas que a automação começa. <b>As pessoas ficam; a tarefa repetida, não.</b>') + CTA('Comenta: qual você tiraria primeiro?'), gap=40)
reel(f'{D}-v1.dc.html', 'Qua · Reels 1', 'n', 'Faz a conta', '1/5',
     T('Quanto custa', 'uma tarefa repetitiva?') + P('Faz a conta comigo.'), 'Veja até o fim')
reel(f'{D}-v2.dc.html', 'Qua · Reels 2', '', 'O exemplo', '2/5',
     T('30 minutos', 'por dia.') + P('Conferir pagamento, copiar pedido, responder a mesma pergunta.'), 'A conta')
reel(f'{D}-v3.dc.html', 'Qua · Reels 3', '', 'A conta', '3/5',
     '<div class="col" style="gap: 20px;"><div class="tile"><span class="cs">30 min × 22 dias</span><span class="v">11 h/mês</span></div><div class="tile bl"><span class="cs">11 h × 12 meses</span><span class="v">132 h/ano</span></div></div>' + P('<b>Mais de 3 semanas de trabalho de 40 horas.</b>'), 'A virada')
reel(f'{D}-v4.dc.html', 'Qua · Reels 4', 's', 'A virada', '4/5',
     T('E isso é', 'uma tarefa só.') + P('Quantas assim existem no seu negócio?'), 'Sua vez')
reel(f'{D}-v5.dc.html', 'Qua · Reels 5', 'n', 'Sua vez', '5/5',
     T('Anote as tarefas', 'que se repetem.') + P('Comente DIAGNÓSTICO que eu te ajudo a ver qual automatizar primeiro.') + CTA('Comente DIAGNÓSTICO'))

# ---------- QUINTA 26/11 ----------
D = 's23-qui'
sl(f'{D}-c1.dc.html', 'Qui · 1 Capa', 'n', 'Automação · por onde começar', '01/06',
   T('A maneira mais fácil de', 'começar a automatizar.', 'margin-bottom: 24px;') + P('Sem sistema caro. <b>Três números 1.</b>'), 'O problema')
sl(f'{D}-c2.dc.html', 'Qui · 2 Problema', 'n', 'O problema', '02/06',
   T('Querer automatizar', 'tudo de uma vez.', 'margin-bottom: 24px;') + X('Muita ferramenta, nenhuma em uso', 'A equipe não sabe o que mudou', 'Ninguém sabe dizer se melhorou'), 'A regra', gap=20)
def TILE(v, a, b):
    return f'<div class="tile"><span class="v">{v}</span><span class="ct">{a}</span><span class="cs">{b}</span></div>'
sl(f'{D}-c3.dc.html', 'Qui · 3 A regra', 'n', 'A regra 1 · 1 · 1', '03/06',
   T('1&nbsp;processo. 1&nbsp;automação.', '1&nbsp;indicador.', 'margin-bottom: 16px;') + '<div class="g3">' + TILE('1', 'processo', 'o que mais se repete') + TILE('1', 'automação', 'só no passo mais chato') + TILE('1', 'indicador', 'para saber se melhorou') + '</div>', 'Um exemplo')
sl(f'{D}-c4.dc.html', 'Qui · 4 Exemplo', 'n', 'Exemplo', '04/06',
   T('Orçamento', 'pelo WhatsApp.', 'margin-bottom: 8px;') + STEPS(('Processo', 'Do pedido de orçamento ao envio da proposta.'), ('Automação', 'Resposta na hora, com as perguntas do orçamento.'), ('Indicador', 'Tempo até a primeira resposta.')), 'Depois de 30 dias', gap=24)
sl(f'{D}-c5.dc.html', 'Qui · 5 Virada', 'n', 'Depois de 30 dias', '05/06',
   T('Melhorou?', 'Aí sim, o próximo.', 'margin-bottom: 16px;') + P('Se o indicador melhorou, escolha o próximo processo. Se não, ajuste antes de seguir.') + P('<b>Comece pequeno, meça e só depois escale.</b>'), 'Sua vez')
sl(f'{D}-c6.dc.html', 'Qui · 6 CTA', 'n', 'Sua vez', '06/06',
   T('Qual seria', 'o seu 1&nbsp;·&nbsp;1&nbsp;·&nbsp;1?', 'font-size: 84px;') + DV + P('Escreve nos comentários: processo, automação e indicador. Eu comento o seu.') + CTA('Salva para fazer esta semana'), gap=44)
sl(f'{D}-d1.dc.html', 'Qui · Dado', 'n', 'Dado da semana', '01/02',
   '<span class="big">9&nbsp;horas</span>' + T('por semana com burocracia financeira:', 'a média do dono de pequeno negócio.', 'font-size: 64px;') + P('No varejo, <b>11 horas.</b>') + '<span class="src">Fonte: estudo “Tempo é dinheiro”, Nu Empresas e Bridge Research, com 1.200 donos de pequenos negócios ouvidos em julho de 2026. Divulgado pela Mercado&amp;Consumo (15/10/2026).</span>', 'No seu negócio', gap=32)
sl(f'{D}-d2.dc.html', 'Qui · No seu negócio', '', 'No seu negócio', '02/02',
   T('Quase tudo isso', 'se repete toda semana.', 'font-size: 80px;') + P('Notas fiscais, entradas e saídas, conferir recebimentos.') + P('Mesmo assim, entre quem usa IA, só <b>30%</b> usam em tarefas financeiras ou administrativas. Para textos, <b>68%</b>.') + '<span class="src">Fonte: Nu Empresas e Bridge Research, via Mercado&amp;Consumo.</span>' + CTA('Comece pelo que mais se repete'), gap=32)

# ---------- SEXTA 27/11 ----------
D = 's23-sex'
sl(f'{D}-o1.dc.html', 'Sex · 1 Gancho', '', 'Opinião do Lucas', '01/03',
   T('Se eu fosse automatizar uma coisa só,', 'começaria pelo WhatsApp.', 'margin-bottom: 24px;') + P('Hoje é Black Friday. <b>E é por lá que o cliente chama.</b>'), '3 motivos', gap=36)
sl(f'{D}-o2.dc.html', 'Sex · 2 Motivos', '', 'Por quê', '02/03',
   T('3 motivos.', None, 'margin-bottom: 8px;') + STEPS(('É onde o cliente chega', 'Pedido, dúvida e orçamento caem no mesmo lugar.'), ('Demora custa venda', 'Quem espera demais pergunta para outro.'), ('Nada fica registrado', 'Sem registro, não dá para chamar o cliente de volta.')), 'O primeiro passo', gap=24)
sl(f'{D}-o3.dc.html', 'Sex · 3 Primeiro passo', 'n', 'O primeiro passo', '03/03',
   T('Resposta na hora', 'e registro de quem chamou.', 'margin-bottom: 16px;') + P('Não precisa de robô que conversa sozinho. Uma mensagem de boas-vindas com as perguntas certas e uma lista de quem chamou já mudam a semana.') + P('<b>E você, começaria por onde? Comenta aqui.</b>'))
sl(f'{D}-f1.dc.html', 'Sex · Frase', 'n', 'Frase do dia', '01/02',
   '<span class="qm">“</span>\n<p class="q">Eficiência é fazer as coisas direito; eficácia é fazer as coisas certas.</p>\n<div class="col" style="gap: 10px;"><span class="au">Peter Drucker</span><span class="ob">O Gestor Eficaz (1967)</span></div>', 'No seu negócio', gap=36)
sl(f'{D}-f2.dc.html', 'Sex · Aplicação', 'n', 'No seu negócio', '02/02',
   T('Automatizar a tarefa errada', 'é eficiência sem eficácia.') + P('Antes de deixar um processo mais rápido, pergunte se ele precisa existir.') + DV + P('<b>Primeiro o certo. Depois o rápido.</b>'), gap=40, foot=FR_FOOT)

# ---------- SÁBADO 28/11 ----------
D = 's23-sab'
sl(f'{D}-c1.dc.html', 'Sáb · 1 Capa', 'n fio', 'Diagnóstico Solid', '01/05',
   T('Ninguém te prepara para esta parte:', 'a operação do dia a dia.', 'margin-bottom: 24px;') + P('Abrir é uma coisa. Fazer rodar toda semana é outra.'), 'O problema')
sl(f'{D}-c2.dc.html', 'Sáb · 2 Problema', 'n fio', 'O problema', '02/05',
   T('Tudo passa', 'pelo dono.', 'margin-bottom: 24px;') + X('Cada pedido depende de você para andar', 'O mesmo trabalho é feito à mão toda semana', 'Só você sabe o passo a passo'), 'As 4 perguntas', gap=20)
sl(f'{D}-c3.dc.html', 'Sáb · 3 As 4 perguntas', 'fio', 'Faceta Operação · 4 perguntas', '03/05',
   T('O que a gente olha', 'antes de automatizar.', 'margin-bottom: 8px;') + N('O passo a passo do pedido à entrega está escrito?', 'Quais tarefas se repetem toda semana?', 'Onde o trabalho para esperando alguém?', 'Se você sumir 3 dias, o que trava?'), 'O veredito')
sl(f'{D}-c4.dc.html', 'Sáb · 4 Veredito', 'fio', 'O veredito', '04/05',
   T('No fim,', 'um próximo passo.', 'margin-bottom: 16px;') + P('Você sai sabendo qual processo organizar primeiro e o que dá para automatizar nele.') + P('<b>Sem empurrar ferramenta.</b>'), 'Como participar')
sl(f'{D}-c5.dc.html', 'Sáb · 5 CTA', 's fio', 'É gratuito', '05/05',
   T('30 minutos,', '5 vagas por semana.', 'font-size: 88px;') + DV + P('Comente DIAGNÓSTICO ou mande a palavra no direct.') + CTA('Comente DIAGNÓSTICO'), gap=44)
reel(f'{D}-v1.dc.html', 'Sáb · Reels capa', 'n', 'Reels', None,
     T('Você não precisa de ferramenta cara', 'para começar a automatizar.') + P('Assista até o fim.'))

# ---------- DOMINGO 29/11 ----------
D = 's23-dom'
sl(f'{D}-r1.dc.html', 'Dom · 1 Gancho', 'n', 'Ritual de domingo', '01/02',
   T('A maneira mais fácil de descobrir', 'o que automatizar.', 'margin-bottom: 24px;') + P('15 minutos com o caderno. <b>Arrasta.</b>'), 'Os 3 passos', ent='p', gap=36)
sl(f'{D}-r2.dc.html', 'Dom · 2 Passos + CTA', '', 'Os 3 passos', '02/02',
   STEPS(('Liste o que você repetiu na semana', 'Tudo que fez mais de 2 vezes.'), ('Anote o tempo de cada um', 'Mesmo que seja no chute.'), ('Circule o que mais toma tempo', 'É a sua candidata número 1.')) + CTA('Comente RITUAL e receba o guia'), gap=40)
sl(f'{D}-slot.dc.html', 'Dom · Trajetória (aguardando)', '', 'Trajetória', None,
   '<div class="slot">' + T('Aguardando', 'material do Lucas.', 'font-size: 72px;') + P('O que você viveu ou aprendeu nesta semana com a Solid, com uma foto sua. Sem material, o post sai da grade.') + '</div>')

# ---------- STORIES ----------
S = [
 ('seg', [('n', 'Bom dia', T('Você comprou a ferramenta', 'antes do processo?') + P('Ao meio-dia, a ordem certa no feed.')),
          ('', 'Hoje no feed', T('Primeiro o processo.', 'Depois a IA.') + P('Toque para ver o carrossel.') + STK('COMPARTILHE O CARROSSEL AQUI')),
          ('s', 'Hoje à noite', T('Quanto vale', 'uma hora sua?') + P('A frase das 19h30 já está no feed.'))]),
 ('ter', [('', 'Bom dia', T('Quantos destes', 'acontecem aí?') + P('Ao meio-dia, o teste dos 6 sinais.')),
          ('n', 'Teste rápido', T('Você marcou', 'quantos sinais?') + STK('FIGURINHA ENQUETE: 0 a 1 / 2 a 3 / 4 a 6')),
          ('s', 'No feed', T('Do aviso perdido', 'ao chamado com QR.') + P('O ReparoFit está no feed.'))]),
 ('qua', [('n', 'Mito ou verdade?', T('A IA vai substituir', 'o seu funcionário?') + STK('FIGURINHA ENQUETE: Mito / Verdade')),
          ('', 'A resposta', T('Mito ou verdade?', 'Está no feed.') + STK('COMPARTILHE O POST AQUI')),
          ('s', 'Faz a conta', T('30 minutos por dia', 'viram 132 horas no ano.') + P('Veja a conta no Reels.'))]),
 ('qui', [('', 'Bom dia', T('1&nbsp;processo. 1&nbsp;automação.', '1&nbsp;indicador.') + P('Ao meio-dia, por onde começar.')),
          ('n', 'Me conta', T('Qual tarefa você', 'tiraria do seu dia?') + STK('FIGURINHA CAIXINHA')),
          ('s', 'Dado da semana', '<span class="big">9 h</span>' + T('por semana', 'com burocracia financeira.') + P('Nu Empresas e Bridge Research. Detalhes no feed.'))]),
 ('sex', [('n', 'Black Friday', T('Hoje o cliente', 'chama no WhatsApp.') + P('Responda rápido e anote quem chamou.')),
          ('', 'Enquete', T('Por onde você', 'começaria a automatizar?') + STK('FIGURINHA ENQUETE: WhatsApp / Cobrança / Notas')),
          ('s', 'Antes de dormir', T('Hoje, anote', 'quem comprou.') + P('É a lista para chamar de volta em dezembro.'))]),
 ('sab', [('n', 'Bom dia', T('Se você sumir 3 dias,', 'o que trava?') + P('Às 10h, a faceta Operação no feed.')),
          ('', 'Diagnóstico Solid', T('Quer olhar a sua operação', 'comigo?') + P('Gratuito, 30 minutos.') + STK('FIGURINHA MENSAGEM: DIAGNÓSTICO')),
          ('s', 'Ainda dá tempo', T('5 vagas por semana', 'para o Diagnóstico.') + P('Gratuito, 30 minutos. Mande DIAGNÓSTICO no direct.'))]),
 ('dom', [('n', 'Ritual de domingo', T('15 minutos', 'com o caderno.') + P('Ao meio-dia, o ritual no feed.')),
          ('', 'Me conta', T('Qual tarefa você mais', 'repetiu nesta semana?') + STK('FIGURINHA CAIXINHA')),
          ('s', 'Guia grátis', T('Comente RITUAL', 'no post de hoje.') + P('Eu te mando o guia completo no direct.'))]),
]
HORAS = ['8h30', '13h', '20h']
for dia, ss in S:
    for k, (c, lb, inner) in enumerate(ss):
        story(f's23-{dia}-s{k+1}.dc.html', f'{dia.capitalize()} · Story {k+1} · {HORAS[k]}', c, lb, inner)

print(len(FILES))
open(os.path.join(OUT, '_lista.txt'), 'w').write('\n'.join(FILES))
