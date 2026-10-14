# Automação diária do Orceu Radar

Leia este arquivo e o FORMATO.md inteiros antes de qualquer etapa. Repositório: arthurdantxs/radar-noticias.
Se o repositório não estiver clonado na sessão, use a ferramenta add_repo (owner arthurdantxs, repo radar-noticias, access push), clone e registre o diretório.
Fuso: America/Araguaina (UTC-3, igual a Brasília). "Hoje" é a data local.
Commits terminam com as duas linhas:
Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: <link da sessão atual>

## Visão geral do dia

1. 06:10 Buscar e redigir: escolhe 2 notícias, escreve os 2 .md em `rascunhos/AAAA-MM-DD/` (NÃO em noticias/), valida e faz push.
2. 06:55 Publicar: revalida, move os 2 .md para `noticias/`, faz push, monta os 2 posts no Canva, publica o post 1 no Instagram, envia o resumo ao Arthur.
3. 07:30 (GitHub Action Sync Radar, não é com você) copia noticias/ para o site e a Cloudflare publica.
4. 20:30 Exporta o post 2 do Canva e publica no Instagram.

Estado do dia: `rascunhos/AAAA-MM-DD/estado.json` com slugs, links do Canva, ids de design, legendas e status do Instagram de cada post. Atualize e faça push a cada etapa. Cada execução lê esse arquivo para saber o que já foi feito e NUNCA repete uma etapa concluída (principalmente publicação no Instagram).

## 1. Escolha das notícias

- Exatamente 2 notícias de CONSTRUÇÃO CIVIL: obras, custo da construção, materiais, mão de obra, habitação e crédito para construtoras, normas técnicas, produtividade, tecnologia na obra, índices do setor. Macroeconomia só entra se o texto ligar direto ao setor.
- Fontes preferidas: IBGE, FGV, CBIC, Caixa, ministérios, Agência Brasil, Sinduscon, Abrainc, Secovi. Verifique a data de publicação abrindo a página da fonte (confirme o ANO).
- Janela: últimos 7 dias, prefira as mais recentes. Use a data de publicação da fonte no campo date.
- Não pode: vagas, anúncio de evento, notícia sobre concorrente, pauta política em votação ou disputa (PEC, projeto polêmico, partido).
- Não repita: confira noticias/, rascunhos/ e os fonte_url já usados. Slug nunca pode existir.
- Se achar menos de 2 que passem em todos os critérios, produza só as que passam e avise no resumo. Nunca afrouxe os critérios nem invente. Se achar 0, não publique nada e avise.
- Fatos só do que a fonte diz. Reescreva com palavras próprias, sem copiar trechos longos.

## 2. Redação (regras de marca)

- Sem travessão (— ou –), em nenhum lugar. Sem a construção "não é X, é Y". Nunca cite concorrentes. Diga "tecnologia" e não "software". Sem linguagem de coach ou guru. Tom de mentor: direto, prático, respeitoso.
- Estrutura do .md: siga o FORMATO.md. Campos obrigatórios completos. Seção final obrigatória "### O que isso representa para o setor" com texto prático.
- title completo, meta_title até 70 caracteres, subtitle linha fina, resumo até 170 caracteres, tempo_leitura 2 a 4.
- categoria: gestao-e-obras, mercado-e-economia ou inovacao-e-ia. cta_produto: copiloto, treinamentos, comunidade ou hub (escolha o que combina com o tema).
- Foto: Agência Brasil (CC BY). Abra uma matéria da Agência Brasil com foto adequada de construção (WebFetch, pegue o og:image e o crédito). Campo imagem = URL direta da foto (formato imagens.ebc.com.br ... 1170x700 ... ). imagem_alt descritivo. imagem_credito sempre preenchido no formato "Foto: Nome/Agência Brasil". Sem foto adequada: imagem "" (o site usa a capa da categoria) e, só no Canva, use uma das fotos de reserva abaixo.
- O shell não consegue baixar de imagens.ebc.com.br (proxy bloqueia). Não tente contornar. O Canva importa pela URL com a ferramenta upload-asset-from-url.
- Fotos de reserva para o Canva (Agência Brasil):
  - Fernando Frazão, trabalhador com tijolos: https://imagens.ebc.com.br/OSOPDe0MuQggIUzWubjyzAtTSsM=/1170x700/smart/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/construcao_civil_2306219897.jpg?itok=1BMVp9Ny
  - Marcello Casal Jr, obras no Setor Noroeste: https://imagens.ebc.com.br/KNMhaR1OHcAKsBuEm6XKHoHWj-o=/1170x700/smart/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/obras_construcao_noreste_mcajr_abr2807221048.jpg?itok=ROAcD-ja
- Validação obrigatória antes de qualquer push de .md:
  `python3 automacao/validar_noticia.py arquivo.md [outros.md] --hoje AAAA-MM-DD` (precisa de PyYAML; pip install --break-system-packages pyyaml se faltar). Exit 1 = corrigir antes. Arquivo inválido derruba o deploy do dia.
- Além do validador, releia cada .md procurando travessão, "não é X, é Y", "software" e menção a concorrente.

## 3. Canva (modelo DAHX_tSwhAU)

Para cada notícia, nome do design "Radar · DD/MM · tema" (tema curto, uma ou duas palavras).
1. copy-design do DAHX_tSwhAU (guarde design_id e o link que ele devolver).
2. read-design com open_transaction true e fields design_content + thumbnails. Confirme os locator ids pelo conteúdo lido (esperados, prefixo da página PBl0NHDsQlwKLPr4-):
   - foto: LBHJCTgK0F9k8BCF (update_fill)
   - pergunta (texto cinza na pílula): LBGLybSgnPtKPD7y
   - pílula branca: LB8jzZphVpcrS9Xk
   - título: LBkHNZCqfvQkFZYJ
   - resumo: LBnHpJY14FqQtm5M
3. upload-asset-from-url da foto (guarde o asset id) e então edit-design (page_index 1, finalize keep_open) com:
   - update_title do design
   - update_fill da foto com asset_id e alt_text
   - replace_text da pergunta (pergunta-gancho curta, ideal até 42 caracteres), do título (até 55 caracteres, cabe em 2 linhas) e do resumo (o mesmo resumo do .md, até 170)
   - o modelo NÃO tem campo de crédito: add_text com page_id PBl0NHDsQlwKLPr4, top 782, left 67.6, width 944 e o texto do crédito; depois format_text color #d9d9d9, font_size 17. Se o add_text já existir (cópia reaproveitada), use replace_text no elemento.
   - AJUSTE DA PÍLULA (obrigatório): a pílula tem largura fixa e deixa espaço vazio com texto curto. Calcule caracteres = tamanho da pergunta. largura_pilula = caracteres x 11.4 + 23 (máximo 542). largura_caixa_texto = largura_pilula - 10. Use resize_element na pílula (width largura_pilula, height 34.3, preserve_aspect_ratio false) e no texto da pergunta (somente width). Exemplo: 38 caracteres, pílula 456, caixa 446.
4. Olhe a thumbnail devolvida. Confira: pergunta em UMA linha dentro da pílula sem sobra grande à direita (se quebrou em 2 linhas, aumente 10 a 15 px; se sobrou muito, diminua), título em até 2 linhas sem encostar no resumo, resumo em até 3 linhas, crédito legível sob a foto, foto sem corte estranho. Corrija e confira de novo.
5. edit-design com finalize commit.

## 4. Instagram (conector Windsor, perfil Orceu orceu.ai, conta id 17841472904257078)

- Exporte o design do Canva em JPG (export-design, type jpg, quality 95, export_quality pro) IMEDIATAMENTE antes de publicar. O link expira em cerca de 5 horas.
- Carregue mcp__Windsor_ai__execute_action via ToolSearch, confira o schema com list_actions (connector instagram) e publique com create_image_post (image_url = link do export, caption = legenda).
- Publique UMA vez. Se a resposta vier ambígua ou com erro, verifique se o post saiu (get_data do conector instagram) antes de tentar de novo. Registre o resultado no estado.json.
- Legenda (até 2200 caracteres), no formato exato:
  1. Pergunta do post (a mesma do Canva) na primeira linha.
  2. Parágrafo 1: o fato principal com números, usando # em palavras-chave dentro do texto.
  3. Parágrafo 2: o detalhe que importa para quem constrói.
  4. Parágrafo 3: o que fazer, no tom de mentor.
  5. Linha final: "Matéria completa no Radar: radar.orceu.com" (NÃO escreva "link na bio", o perfil não tem o link).
  6. Hashtags finais, 3 a 5, sempre em minúscula, sempre incluindo #construçãocivil e #orceu.
  Mesmas regras de marca (sem travessão, sem "não é X, é Y", sem concorrentes, "tecnologia" e não "software").
- Post 1 = primeira notícia, publicado na etapa 06:55. Post 2 = segunda notícia, publicado às 20:30.

## 5. Resumo final (etapa 06:55)

Mensagem curta, em português informal e sem travessões, com: os 2 links do Canva, os 2 links das notícias no Radar (https://radar.orceu.com/noticia/SLUG/, entram no ar depois do sync das 07:30 e do deploy), status do post 1 no Instagram, e qualquer problema ou critério que não foi atendido. Envie também com a ferramenta de notificação, se existir.
