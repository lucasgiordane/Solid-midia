# Post-card do @lucasgiordane

- `solid26.css`: folha de estilo da identidade 2026 (inclui o formato post-card, classe `.pc`).
- `modelos.py`: gera as capas dos 5 modelos aprovados em 21/11/2026 (É OFICIAL, Na prática por setor, Curiosidade, Faz a conta, Raio-X) e a página final de CTA.
- `anima2.py`: gera o carrossel animado de teste (6 páginas em MP4 1080x1350, 30 fps) com Playwright + ffmpeg.

Uso: `python3 -I <script> <saida> solid26.css <pasta-blobs> ~/fontes/node_modules/@fontsource`
A pasta de blobs precisa ter `a0000000000000000000000000000004.jpg` (copie `lucas-avatar.jpg`: recorte do Retrato Corporativo, enquadramento igual ao perfil do Instagram) e `a0000000000000000000000000000001.svg` (copie `simbolo-dourado.svg`).
Fontes: `npm install @fontsource/manrope @fontsource/inter @fontsource/ibm-plex-mono`.
**Capa do vídeo (decisão do Lucas em 25/11/2026):** no MP4 da página 1, o primeiro quadro é a página pronta (todos os elementos no lugar) e só depois a animação começa. O Instagram usa o primeiro quadro como capa no perfil; sem isso a caixa aparece vazia no grid. Todos os geradores já fazem isso; mantenha em geradores novos.

Guia completo: `claude/modelos-post-card-lucas.md` no projeto Solid Business.
