# Formato oficial do Orceu Radar

Guia de formato das notícias do Orceu Radar. A automação diária consulta este arquivo antes de escrever cada `.md`.

## Formato aceito

Cada notícia vai em `noticias/{slug}.md` (nome do arquivo = slug, sem data).

```markdown
---
title: "Como ler o custo do m² do Sinapi antes de fechar o orçamento da obra"
meta_title: "Custo do m² do Sinapi: como ler antes do orçamento"
subtitle: "O índice mensal do IBGE e da Caixa ajuda a calibrar o orçamento."
resumo: "O Sinapi publica todo mês o custo médio do m² por estado. É referência, não preço pronto."
slug: "como-ler-o-custo-do-m2-do-sinapi"
categoria: "mercado-e-economia"
estado: ""
autor: "Equipe de Redação Orceu"
date: "2026-10-14"
tempo_leitura: 3
imagem: ""
imagem_alt: "Capa da editoria Mercado & Economia"
imagem_credito: "Foto: Nome/Agência"
fonte: "IBGE/Sinapi"
fonte_url: "https://www.ibge.gov.br/..."
tags: ["custo da construção", "sinapi"]
cta_produto: "copiloto"
---

Parágrafo de abertura com **negrito** quando precisar.

## Subtítulo

- item de lista
- outro item

### O que isso representa para o setor

Parágrafo final, que vira o destaque de fechamento da matéria.
```

## Campos

| Campo | Obrigatório | Regra |
|---|---|---|
| title | sim | título completo (H1) |
| meta_title | sim | até 70 caracteres |
| subtitle | sim | linha fina |
| resumo | sim | bloco "Em resumo" |
| slug | sim | minúsculas, números e hífens; igual ao nome do arquivo |
| categoria | sim | gestao-e-obras, mercado-e-economia ou inovacao-e-ia |
| date | sim | AAAA-MM-DD; define a ordem |
| tempo_leitura | sim | minutos, de 1 a 60 |
| fonte | sim | nome mostrado na linha "Fonte:" |
| fonte_url | sim | link válido |
| cta_produto | sim | copiloto, treinamentos, comunidade ou hub |
| seção final | sim | "### O que isso representa para o setor", com texto |
| estado | não | sigla da UF (ex.: SP) ou vazio |
| autor | não | padrão "Equipe de Redação Orceu" |
| imagem | não | URL direta da foto da Agência Brasil; vazio usa a capa da categoria (o sync baixa e ajusta) |
| imagem_alt | não | padrão: o título |
| imagem_credito | não | preencher sempre que houver imagem |
| tags | não | lista entre colchetes |

## Regras editoriais fixas

- Evitar pautas políticas em votação ou disputa (PECs, projetos polêmicos, partidos). Preferir índices, crédito, normas técnicas, tecnologia e mercado.
- Usar a data de publicação da fonte e só notícias das últimas 48h.
