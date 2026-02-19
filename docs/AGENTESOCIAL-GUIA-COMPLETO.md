# AgenteSocial - Guia Completo do Sistema

> **Um ecossistema de IA para gestao completa de redes sociais**
> Versao 2.0 | Fevereiro 2026

---

## Indice

1. [O que e o AgenteSocial?](#1-o-que-e-o-agentesocial)
2. [Como Funciona — Visao Geral](#2-como-funciona--visao-geral)
3. [Os 11 Agentes de IA](#3-os-11-agentes-de-ia)
4. [Arquitetura de Sub-Times](#4-arquitetura-de-sub-times)
5. [Fluxo de uma Mensagem](#5-fluxo-de-uma-mensagem)
6. [Funcionalidades por Area](#6-funcionalidades-por-area)
7. [Plataformas Suportadas](#7-plataformas-suportadas)
8. [API — Todos os Endpoints](#8-api--todos-os-endpoints)
9. [Banco de Dados](#9-banco-de-dados)
10. [Sistema de Memoria](#10-sistema-de-memoria)
11. [Seguranca e Autenticacao](#11-seguranca-e-autenticacao)
12. [Tecnologias Utilizadas](#12-tecnologias-utilizadas)
13. [Como Instalar e Rodar](#13-como-instalar-e-rodar)

---

## 1. O que e o AgenteSocial?

O **AgenteSocial** e uma plataforma de inteligencia artificial que gerencia suas redes sociais de forma autonoma. Imagine ter uma **equipe completa de marketing digital** trabalhando 24/7 para voce — e essa equipe e composta por 11 agentes de IA especializados.

### O que ele faz por voce:

| Necessidade | O que o AgenteSocial resolve |
|---|---|
| "Preciso criar posts" | Cria textos, carrosseis, reels e stories personalizados |
| "Quero saber como meu perfil esta" | Analisa metricas, engajamento e crescimento |
| "O que esta bombando?" | Detecta tendencias virais e oportunidades |
| "Quais hashtags usar?" | Pesquisa e recomenda hashtags otimizadas |
| "Preciso de um roteiro de video" | Cria scripts para Reels, TikTok e YouTube |
| "Quero lancar um podcast" | Gera roteiros completos com show notes |
| "Quando devo postar?" | Planeja calendario editorial otimizado |
| "Como estou performando?" | Gera relatorios detalhados de performance |
| "Qual estrategia seguir?" | Recomenda estrategias por tier de seguidores |
| "Preciso de design" | Sugere layouts, cores e prompts para imagens IA |
| "Lembrar meu tom de voz" | Memoriza preferencias e mantem consistencia |

### Foco no Brasil

Todo o sistema e otimizado para o mercado brasileiro:
- Todos os agentes respondem em **portugues brasileiro**
- Horarios otimizados para **fuso de Brasilia**
- Datas sazonais brasileiras (Carnaval, Dia das Maes, Black Friday, etc.)
- Benchmarks de engajamento para o publico brasileiro

---

## 2. Como Funciona — Visao Geral

### Diagrama Geral do Sistema

```
+------------------------------------------------------------------+
|                        USUARIO / FRONTEND                         |
|              (App Web, Chat, Dashboard, Calendario)               |
+----------------------------------+-------------------------------+
                                   |
                         API REST + WebSocket
                                   |
+----------------------------------v-------------------------------+
|                         BACKEND (FastAPI)                         |
|                                                                   |
|  +--------------------+  +------------------+  +--------------+  |
|  |   API Endpoints    |  |  Autenticacao    |  |    Cache     |  |
|  |  /chat /content    |  |  JWT + API Key   |  |  In-Memory   |  |
|  |  /analysis /reports|  |  Supabase Auth   |  |  + Redis     |  |
|  |  /calendar /settings|  +------------------+  +--------------+  |
|  +--------+-----------+                                           |
|           |                                                       |
|  +--------v---------------------------------------------------+  |
|  |              TIME DE AGENTES IA (AGNO 2.5.2)               |  |
|  |                                                             |  |
|  |  +----------+  +----------+  +----------+  +----------+   |  |
|  |  | Content  |  | Analysis |  |  Media   |  |Operations|   |  |
|  |  | Factory  |  |  Squad   |  |Production|  |          |   |  |
|  |  | (3 IAs)  |  | (3 IAs)  |  | (2 IAs)  |  | (3 IAs) |   |  |
|  |  +----------+  +----------+  +----------+  +----------+   |  |
|  +-------------------------------------------------------------+  |
|           |                                                       |
|  +--------v---------------------------------------------------+  |
|  |                    FERRAMENTAS (Tools)                       |  |
|  |  Instagram API | YouTube API | Google Trends | Whisper      |  |
|  |  DuckDuckGo    | Supabase DB | Memory (pgvector)            |  |
|  +-------------------------------------------------------------+  |
+----------------------------------+-------------------------------+
                                   |
+----------------------------------v-------------------------------+
|                     BANCO DE DADOS (Supabase)                     |
|  PostgreSQL + pgvector + RLS + 20 tabelas                        |
+------------------------------------------------------------------+
```

### Em palavras simples:

1. **Voce envia uma mensagem** (ex: "Cria um post sobre marketing digital")
2. O **Roteador Principal** analisa e envia para o sub-time correto
3. O **Sub-Time** coordena seus agentes especialistas
4. Os agentes **usam ferramentas** (banco de dados, APIs, busca web)
5. A resposta volta **personalizada** com seu tom de voz e historico

---

## 3. Os 11 Agentes de IA

Cada agente e um especialista com instrucoes detalhadas, ferramentas proprias e um papel definido.

### Mapa Visual dos Agentes

```
                    +-------------------------+
                    |    MASTER ORCHESTRATOR   |
                    |    (Roteador Principal)  |
                    |    Modelo: GPT-4.1-mini  |
                    +------------+------------+
                                 |
            +--------------------+--------------------+
            |                    |                     |
   +--------v-------+  +--------v--------+  +---------v-------+
   |                 |  |                  |  |                 |
   v                 v  v                  v  v                 v

+-------+ +-------+ +-------+ +-------+ +-------+ +-------+
|Content| |Visual | |Hashtag| |Social | |Viral  | |Strategy|
|Writer | |Design.| |Hunter | |Analyst| |Tracker| |Advisor |
+-------+ +-------+ +-------+ +-------+ +-------+ +-------+

+-------+ +-------+ +-------+ +-------+ +-------+
|Podcast| |Video  | |Calendar| |Report | |Memory |
|Creator| |Script | |Planner | |Gener. | |Agent  |
+-------+ +-------+ +--------+ +-------+ +-------+
```

### Tabela Detalhada de Cada Agente

| # | Agente | O que faz | Ferramentas |
|---|--------|-----------|-------------|
| 1 | **Content Writer** | Cria posts, carrosseis, reels, stories, threads | Memoria, Banco de dados |
| 2 | **Visual Designer** | Sugere layouts, cores, tipografia, prompts DALL-E/Midjourney | Memoria, Banco de dados |
| 3 | **Hashtag Hunter** | Pesquisa e recomenda hashtags otimizadas por nicho | Instagram API, Google Trends, Banco de dados |
| 4 | **Social Analyst** | Analisa perfis, metricas, engajamento, benchmarks | Instagram, YouTube, Google Trends, DuckDuckGo |
| 5 | **Viral Tracker** | Detecta conteudo viral e tendencias cross-platform | Google Trends, Instagram, YouTube, DuckDuckGo |
| 6 | **Strategy Advisor** | Define estrategias de crescimento e monetizacao | Memoria, Banco de dados, DuckDuckGo |
| 7 | **Podcast Creator** | Cria roteiros de podcast, show notes, identifica clips | Whisper (transcricao), Banco de dados, Memoria |
| 8 | **Video Script Writer** | Cria roteiros para Reels, TikTok, YouTube | Memoria, Banco de dados |
| 9 | **Calendar Planner** | Planeja calendario editorial semanal/mensal | Banco de dados, Memoria |
| 10 | **Report Generator** | Gera relatorios de performance (WoW, MoM) | Banco de dados, Memoria |
| 11 | **Memory Agent** | Gerencia memoria de longo prazo e preferencias | Memoria semantica (pgvector), Banco de dados |

---

## 4. Arquitetura de Sub-Times

Os 11 agentes estao organizados em **4 sub-times especializados**. O time principal recebe a mensagem e **roteia** para o sub-time correto.

### Diagrama dos Sub-Times

```
+====================================================================+
||                   AGENTESOCIAL TEAM (Roteador)                   ||
||                     Modo: ROUTE (Roteamento)                     ||
||                     Modelo: GPT-4.1-mini                         ||
+====================================================================+
         |                |                |                |
         v                v                v                v
+----------------+ +----------------+ +----------------+ +----------------+
|   CONTENT      | |   ANALYSIS     | |    MEDIA       | |  OPERATIONS    |
|   FACTORY      | |   SQUAD        | |  PRODUCTION    | |                |
|                | |                | |                | |                |
| Modo:coordinate| | Modo:coordinate| | Modo:coordinate| | Modo:coordinate|
+----------------+ +----------------+ +----------------+ +----------------+
| - Content      | | - Social       | | - Podcast      | | - Calendar     |
|   Writer       | |   Analyst      | |   Creator      | |   Planner      |
| - Visual       | | - Viral        | | - Video Script | | - Report       |
|   Designer     | |   Tracker      | |   Writer       | |   Generator    |
| - Hashtag      | | - Strategy     | |                | | - Memory       |
|   Hunter       | |   Advisor      | |                | |   Agent        |
+----------------+ +----------------+ +----------------+ +----------------+
```

### Quando cada sub-time e acionado:

| Voce diz... | Sub-Time acionado |
|---|---|
| "Cria um post sobre fitness" | **Content Factory** |
| "Faz um carrossel de 7 slides" | **Content Factory** |
| "Sugere hashtags para moda" | **Content Factory** |
| "Analisa meu perfil do Instagram" | **Analysis Squad** |
| "O que esta viral hoje?" | **Analysis Squad** |
| "Qual estrategia para chegar a 10K?" | **Analysis Squad** |
| "Cria um roteiro de Reels" | **Media Production** |
| "Faz um script de podcast" | **Media Production** |
| "Planeja meu calendario da semana" | **Operations** |
| "Gera relatorio do mes" | **Operations** |
| "Quais sao minhas preferencias?" | **Operations** |

---

## 5. Fluxo de uma Mensagem

### Exemplo: "Cria um post sobre inteligencia artificial para Instagram"

```
USUARIO
  |
  |  "Cria um post sobre IA para Instagram"
  v
+----------------------------------------------------+
|  1. ROTEADOR PRINCIPAL                              |
|     Analisa: "criar post" = conteudo                |
|     Decisao: enviar para CONTENT FACTORY            |
+----------------------------------------------------+
  |
  v
+----------------------------------------------------+
|  2. CONTENT FACTORY (Coordenador)                   |
|     Delega para 3 agentes:                          |
+----------------------------------------------------+
  |              |                |
  v              v                v
+----------+ +----------+  +----------+
| CONTENT  | | VISUAL   |  | HASHTAG  |
| WRITER   | | DESIGNER |  | HUNTER   |
|          | |          |  |          |
| 1. Busca | | 1. Busca |  | 1. Busca |
|   brand  | |   cores  |  |   volume |
|   voice  | |   da     |  |   de     |
| 2. Busca | |   marca  |  |   cada   |
|   histor.| | 2. Sugere|  |   hashtag|
| 3. Cria  | |   layout |  | 2. Mix   |
|   post   | | 3. Gera  |  |   30/40/ |
|   com    | |   prompt |  |   30     |
|   hook,  | |   DALL-E |  | 3. Separa|
|   corpo, | |          |  |   alto/  |
|   CTA    | |          |  |   medio/ |
|          | |          |  |   nicho  |
+-----+----+ +----+-----+  +----+-----+
      |            |              |
      v            v              v
+----------------------------------------------------+
|  3. CONTENT FACTORY compila tudo em 1 resposta:     |
|                                                      |
|  ## Post Instagram — Inteligencia Artificial         |
|                                                      |
|  **HOOK:** "A IA ja esta mudando sua vida..."        |
|  **CORPO:** [3 paragrafos otimizados]                |
|  **CTA:** "Salve esse post e mande pra um amigo!" |
|  **HASHTAGS:** #IA #inteligenciaartificial ...       |
|  **VISUAL:** Prompt DALL-E pronto para usar          |
|  **DIMENSOES:** 1080x1350px (4:5)                    |
+----------------------------------------------------+
  |
  v
USUARIO recebe tudo pronto!
```

---

## 6. Funcionalidades por Area

### 6.1 Criacao de Conteudo

O Content Writer domina **5 formatos** de conteudo, cada um com template estruturado:

```
+-------------------------------------------------------------------+
|                    FORMATOS DE CONTEUDO                             |
+-------------------------------------------------------------------+
|                                                                     |
|  +-------------+  +-------------+  +-------------+                 |
|  |    POST     |  |  CARROSSEL  |  | REEL/TIKTOK |                 |
|  |             |  |             |  |             |                  |
|  | - Hook      |  | Slide 1:   |  | [0-2s] Hook |                 |
|  | - Corpo     |  |   Hook     |  | [2-8s] Prob.|                 |
|  | - CTA       |  | Slide 2-6: |  | [8-25s]     |                 |
|  | - Hashtags  |  |   Conteudo |  |   Solucao   |                 |
|  | - Visual    |  | Slide 7:   |  | [25-30s]    |                 |
|  |             |  |   CTA      |  |   CTA       |                 |
|  +-------------+  +-------------+  +-------------+                 |
|                                                                     |
|  +-------------+  +-------------+                                   |
|  |   STORY     |  |   THREAD   |                                   |
|  |             |  |  (Twitter) |                                   |
|  | Frame 1:   |  |             |                                   |
|  |  Abertura  |  | Tweet 1:   |                                   |
|  | Frame 2:   |  |   Hook     |                                   |
|  |  Enquete   |  | Tweet 2-6: |                                   |
|  | Frame 3:   |  |   Corpo    |                                   |
|  |  Conteudo  |  | Tweet 7:   |                                   |
|  | Frame 4:   |  |  Conclusao |                                   |
|  |  Prova     |  | Tweet 8:   |                                   |
|  | Frame 5:   |  |   CTA      |                                   |
|  |  CTA       |  |            |                                   |
|  +-------------+  +-------------+                                   |
+-------------------------------------------------------------------+
```

### 6.2 Analise e Metricas

```
+-------------------------------------------------------------------+
|                   ANALISE DE PERFIL                                 |
+-------------------------------------------------------------------+
|                                                                     |
|  1. TAXA DE ENGAJAMENTO                                            |
|     Formula: (likes + comments + shares + saves) / followers * 100 |
|                                                                     |
|     Benchmarks Instagram:                                           |
|     [===                    ] <1%  = Baixo                         |
|     [========               ] 1-3% = Medio                         |
|     [==============         ] 3-6% = Bom                           |
|     [====================== ] >6%  = Excelente                     |
|                                                                     |
|  2. SCORE DE VIRALIDADE (0-100)                                    |
|     +------------------------------------------+                   |
|     | Velocidade de engajamento    | 40% peso  |                   |
|     | Taxa de compartilhamento     | 30% peso  |                   |
|     | Taxa de salvamento           | 30% peso  |                   |
|     +------------------------------------------+                   |
|                                                                     |
|     0-30: Normal | 31-60: Acima da media                           |
|     61-80: VIRAL | 81-100: SUPER VIRAL                             |
|                                                                     |
|  3. DETECCAO DE TENDENCIAS                                         |
|     TikTok -> Instagram Reels: 3-7 dias de migracao               |
|     Twitter -> Todas: 24-48h de propagacao                         |
|     YouTube -> Shorts/Reels: clips curtos derivados                |
|     Google Trends -> Oportunidades de conteudo                     |
|                                                                     |
+-------------------------------------------------------------------+
```

### 6.3 Estrategia por Tier de Seguidores

```
+-------------------------------------------------------------------+
|               ESTRATEGIA POR TIER DE CRESCIMENTO                   |
+-------------------------------------------------------------------+
|                                                                     |
|  TIER 1: INICIANTE (0 — 1.000 seguidores)                         |
|  +---------------------------------------------------------------+ |
|  | Foco: Nicho ultra-especifico                                  | |
|  | Frequencia: 5-7x por semana                                   | |
|  | Estrategia: 100% conteudo de valor + networking ativo         | |
|  | Formato: Reels/TikTok obrigatorio                             | |
|  | Meta: 10-20% crescimento/mes                                  | |
|  +---------------------------------------------------------------+ |
|                                                                     |
|  TIER 2: CRESCIMENTO (1.000 — 10.000 seguidores)                  |
|  +---------------------------------------------------------------+ |
|  | Foco: Consistencia + qualidade                                | |
|  | Frequencia: 4-5x por semana                                   | |
|  | Estrategia: Series de conteudo + collabs                      | |
|  | Monetizacao: Parcerias, infoproduto basico                    | |
|  +---------------------------------------------------------------+ |
|                                                                     |
|  TIER 3: AUTORIDADE (10.000 — 100.000 seguidores)                 |
|  +---------------------------------------------------------------+ |
|  | Foco: Diversificacao de plataformas                           | |
|  | Frequencia: 3-5x por semana (alta qualidade)                  | |
|  | Estrategia: Cursos, mentorias, eventos                        | |
|  | Monetizacao: Parcerias pagas, receita recorrente              | |
|  +---------------------------------------------------------------+ |
|                                                                     |
|  TIER 4: INFLUENCIA (100.000+ seguidores)                          |
|  +---------------------------------------------------------------+ |
|  | Foco: Marca pessoal forte                                     | |
|  | Estrategia: Produtos proprios, licensing, equity              | |
|  | Monetizacao: Imperio de midia propria                         | |
|  +---------------------------------------------------------------+ |
|                                                                     |
+-------------------------------------------------------------------+
```

### 6.4 Mix de Hashtags

```
+-------------------------------------------------------------------+
|                   FORMULA DO MIX DE HASHTAGS                       |
+-------------------------------------------------------------------+
|                                                                     |
|  +------------------+                                              |
|  |  30% ALTO VOLUME |  > 500.000 posts                            |
|  |  (Alcance)       |  Ex: #marketingdigital #empreendedorismo    |
|  +------------------+                                              |
|                                                                     |
|  +------------------+                                              |
|  |  40% MEDIO VOLUME|  50.000 — 500.000 posts   <<<< SWEET SPOT  |
|  |  (Visibilidade)  |  Ex: #dicasdemarketing #crescimentoorganico |
|  +------------------+                                              |
|                                                                     |
|  +------------------+                                              |
|  |  30% NICHO       |  < 50.000 posts                             |
|  |  (Qualidade)     |  Ex: #marketingparamedicos #socialmedia2026 |
|  +------------------+                                              |
|                                                                     |
|  Quantidade por plataforma:                                        |
|  Instagram: 20-30 hashtags | TikTok: 3-5 | YouTube: 5-15          |
|  LinkedIn: 3-5             | Twitter: 0 no corpo                  |
+-------------------------------------------------------------------+
```

### 6.5 Calendario Editorial

```
+-------------------------------------------------------------------+
|                   CALENDARIO EDITORIAL SEMANAL                     |
+-------------------------------------------------------------------+
|                                                                     |
|  MIX DE CONTEUDO RECOMENDADO:                                      |
|                                                                     |
|  [================                         ] 40% Educativo         |
|  [============                             ] 30% Entretenimento    |
|  [========                                 ] 20% Vendas            |
|  [====                                     ] 10% Pessoal           |
|                                                                     |
|  MELHORES HORARIOS (Horario de Brasilia):                          |
|                                                                     |
|  Instagram:   11h-13h  e  18h-20h                                  |
|  YouTube:     14h-16h  (publicar para indexar)                     |
|  TikTok:      7h-9h, 12h-14h  e  19h-22h                          |
|  LinkedIn:    7h-9h  e  17h-18h  (dias uteis)                     |
|                                                                     |
|  FREQUENCIA IDEAL:                                                  |
|  Instagram: 4-5 posts + stories diarios + 3 reels/semana          |
|  YouTube:   1-2 videos + 2-3 shorts/semana                        |
|  TikTok:    1-3 videos/DIA                                        |
|  LinkedIn:  3-5 posts/semana (dias uteis)                          |
|                                                                     |
+-------------------------------------------------------------------+
```

### 6.6 Producao de Video e Podcast

```
+-------------------------------------------------------------------+
|                     ROTEIRO DE REELS/TIKTOK                        |
+-------------------------------------------------------------------+
|                                                                     |
|  [0-2s]  HOOK  <-- Critico! Determina 80% da retencao             |
|          VISUAL: Close-up + texto grande                           |
|          FALA: "PARA de fazer isso agora!"                         |
|          TEXTO EM TELA: Frase de 6 palavras                        |
|                                                                     |
|  [2-8s]  PROBLEMA / CONTEXTO                                      |
|          VISUAL: B-roll + transicao                                |
|          FALA: Apresentacao do problema                             |
|                                                                     |
|  [8-25s] SOLUCAO (2-3 pontos)                                     |
|          VISUAL: Demonstracao + texto overlay                      |
|          TRANSICAO: Corte seco entre pontos                        |
|                                                                     |
|  [25-30s] CTA FINAL                                               |
|          FALA: "Segue pra mais dicas!"                             |
|          TEXTO: @handle + CTA escrito                              |
|                                                                     |
|  + Audio sugerido + Hashtags + Legenda completa                    |
|                                                                     |
+-------------------------------------------------------------------+

+-------------------------------------------------------------------+
|                   ROTEIRO DE PODCAST (30 min)                      |
+-------------------------------------------------------------------+
|                                                                     |
|  [00:00] Intro / Vinheta                                           |
|  [00:30] Introducao do Tema (hook + contexto)                      |
|  [01:30] Bloco 1: Fundamento (conceitos base)                     |
|  [05:00] Bloco 2: Aprofundamento (3-5 pontos + storytelling)      |
|  [15:00] Bloco 3: Pratica (passo a passo + ferramentas)           |
|  [25:00] Bloco 4: Perguntas / Interacao                           |
|  [28:00] Encerramento + CTA (recap + proximo episodio)            |
|                                                                     |
|  + Show Notes com timestamps                                       |
|  + 3 clips sugeridos para Reels (30-60s cada)                     |
|  + Titulo SEO + Descricao + Tags                                   |
|                                                                     |
+-------------------------------------------------------------------+
```

---

## 7. Plataformas Suportadas

```
+-------------------------------------------------------------------+
|                    PLATAFORMAS SUPORTADAS                           |
+-------------------------------------------------------------------+
|                                                                     |
|  +------------+  Formatos: Post, Carrossel, Reels, Story          |
|  | INSTAGRAM  |  Hashtags: 20-30 | Dimensao: 1080x1350 (4:5)     |
|  +------------+  API: Graph API (perfil, media, insights)          |
|                                                                     |
|  +------------+  Formatos: Video, Shorts                           |
|  |  YOUTUBE   |  Tags: 5-15 | Thumbnail: 1280x720 (16:9)         |
|  +------------+  API: Data API v3 (canais, videos, trending)       |
|                                                                     |
|  +------------+  Formatos: Video curto (15-60s)                    |
|  |   TIKTOK   |  Hashtags: 3-5 | Dimensao: 1080x1920 (9:16)      |
|  +------------+  Sem API direta (conteudo via templates)           |
|                                                                     |
|  +------------+  Formatos: Post, Artigo, Carrossel                 |
|  |  LINKEDIN  |  Hashtags: 3-5 | Dimensao: 1200x627 (1.91:1)     |
|  +------------+  Tom: Profissional, dados e cases                  |
|                                                                     |
|  +------------+  Formatos: Thread (5-8 tweets)                     |
|  | TWITTER/X  |  Hashtags: 0 no corpo | Max: 280 chars/tweet      |
|  +------------+  Tom: Conciso, opinativo                           |
|                                                                     |
|  +------------+  Formatos: Post, Story                             |
|  |  FACEBOOK  |  Hashtags: moderados | Dimensao: 1200x630         |
|  +------------+  Tom: Conversacional, compartilhavel               |
|                                                                     |
|  +------------+  Formatos: Pin                                     |
|  | PINTEREST  |  Dimensao: 1000x1500 (2:3)                        |
|  +------------+  Foco: Visual, SEO                                 |
|                                                                     |
+-------------------------------------------------------------------+
```

---

## 8. API — Todos os Endpoints

A API do AgenteSocial e organizada em 7 areas:

### Mapa Completo de Endpoints

```
+-------------------------------------------------------------------+
|                      API DO AGENTESOCIAL                           |
|                    Base: /api/v1                                    |
+-------------------------------------------------------------------+
|                                                                     |
|  /chat                                                              |
|    POST /             Envia mensagem para o time de IA             |
|    GET  /conversations         Lista conversas do usuario          |
|    GET  /conversations/{id}/messages   Mensagens de uma conversa   |
|    WS   /ws           Chat em tempo real (WebSocket)               |
|                                                                     |
|  /content                                                           |
|    POST /generate             Gera conteudo com IA                 |
|    GET  /library              Lista conteudos criados              |
|    PUT  /{id}                 Edita conteudo                       |
|    DEL  /{id}                 Exclui conteudo                      |
|    POST /{id}/publish         Marca como publicado                 |
|    POST /{id}/schedule        Agenda publicacao                    |
|                                                                     |
|  /analysis                                                          |
|    POST /profile              Analisa perfil Instagram/YouTube     |
|    POST /trends               Busca tendencias Google Trends       |
|    GET  /viral                Lista conteudos virais (score>=70)   |
|    POST /competitor           Analise competitiva                  |
|    GET  /benchmarks/{platform} Benchmarks por plataforma           |
|                                                                     |
|  /reports                                                           |
|    POST /generate             Gera relatorio de performance        |
|    GET  /                     Lista relatorios                     |
|    GET  /{id}                 Detalhe de um relatorio              |
|    DEL  /{id}                 Exclui relatorio                     |
|                                                                     |
|  /calendar                                                          |
|    POST /events               Cria evento no calendario            |
|    GET  /events               Lista eventos (filtro mes/plataforma)|
|    PATCH /events/{id}         Atualiza evento                      |
|    DEL  /events/{id}          Exclui evento                        |
|    POST /generate-plan        Gera plano editorial com IA          |
|    GET  /automation-rules     Lista regras de automacao            |
|    POST /automation-rules     Cria regra de automacao              |
|                                                                     |
|  /settings                                                          |
|    POST /profiles             Conecta perfil social                |
|    GET  /profiles             Lista perfis conectados              |
|    DEL  /profiles/{id}        Remove perfil                        |
|    POST /brand-voice          Salva tom de voz da marca            |
|    GET  /brand-voice          Retorna tom de voz ativo             |
|                                                                     |
|  /webhooks                                                          |
|    POST /instagram            Webhook do Instagram                 |
|    GET  /instagram            Verificacao do webhook               |
|    POST /youtube              Webhook do YouTube                   |
|                                                                     |
|  /health                      Health check do servidor             |
|                                                                     |
+-------------------------------------------------------------------+
```

### Chat em Tempo Real (WebSocket)

```
+-------------------------------------------------------------------+
|                    WEBSOCKET: /api/v1/chat/ws                      |
+-------------------------------------------------------------------+
|                                                                     |
|  CLIENTE                           SERVIDOR                        |
|    |                                  |                             |
|    |-- {token: "jwt..."} ----------->|  Autenticacao               |
|    |<- {type: "authenticated"} ------|                              |
|    |                                  |                             |
|    |-- {message: "Cria post"} ------>|                              |
|    |<- {type: "typing", status: on} -|  Indicador "digitando..."   |
|    |                                  |  [IA processando...]        |
|    |<- {type: "typing", status: off} |                              |
|    |<- {type: "message",             |  Resposta completa          |
|    |    content: "## Post...",       |                              |
|    |    conversation_id: "abc123"}---|                              |
|    |                                  |                             |
+-------------------------------------------------------------------+
```

---

## 9. Banco de Dados

### Diagrama das Tabelas

```
+-------------------------------------------------------------------+
|                  BANCO DE DADOS — 20 TABELAS                       |
|                  PostgreSQL via Supabase                            |
+-------------------------------------------------------------------+

+---------------------------+     +---------------------------+
|  social_midia_profiles    |     | social_midia_brand_voice  |
|---------------------------|     |   _profiles               |
| id, user_id               |     |---------------------------|
| platform (instagram,etc)  |     | id, user_id               |
| handle (@usuario)         |     | name, tone                |
| followers_count           |     | vocabulary[], avoid_words[]|
| access_token (encrypted)  |     | target_audience           |
+---------------------------+     | is_active (1 por usuario) |
                                  +---------------------------+

+---------------------------+     +---------------------------+
| social_midia_content      |     | social_midia_content      |
|   _pieces                 |     |   _calendar               |
|---------------------------|     |---------------------------|
| id, user_id               |     | id, user_id               |
| content_type (post,reel..)| --> | content_id (FK)           |
| platform                  |     | title, platform           |
| title, body, caption      |     | scheduled_at              |
| hashtags[]                |     | published_at              |
| visual_suggestion         |     | status (scheduled,        |
| status (draft,published..)     |    published, cancelled)   |
| engagement_score          |     +---------------------------+
+---------------------------+

+---------------------------+     +---------------------------+
| social_midia_viral        |     | social_midia_hashtag      |
|   _content                |     |   _research               |
|---------------------------|     |---------------------------|
| id, platform              |     | id, user_id               |
| author_handle             |     | hashtag, platform         |
| likes, comments, shares   |     | volume, competition       |
| saves, views              |     | related_hashtags[]        |
| virality_score (0-100)    |     | trend_direction           |
| classification            |     | niche                     |
| niche, hashtags[]         |     +---------------------------+
+---------------------------+

+---------------------------+     +---------------------------+
| social_midia_analytics    |     | social_midia_reports      |
|   _snapshots              |     |---------------------------|
|---------------------------|     | id, user_id               |
| id, user_id, profile_id   |     | type (weekly,monthly,etc) |
| snapshot_date             |     | period_start, period_end  |
| followers, engagement_rate|     | data (JSONB)              |
| avg_likes, avg_comments   |     | pdf_url                   |
| top_performing_content    |     +---------------------------+
| demographics              |
| best_posting_times        |     +---------------------------+
+---------------------------+     | social_midia_competitor   |
                                  |   _tracking               |
+---------------------------+     |---------------------------|
| social_midia_podcast      |     | id, user_id               |
|   _episodes               |     | platform, handle, name    |
|---------------------------|     | followers_count           |
| id, user_id               |     | engagement_rate           |
| title, description        |     | top_content (JSONB)       |
| script, show_notes        |     | last_analyzed_at          |
| audio_url, transcription  |     +---------------------------+
| clips (JSONB)             |
| duration_seconds          |     +---------------------------+
+---------------------------+     | social_midia_agent        |
                                  |   _conversations          |
+---------------------------+     |---------------------------|
| social_midia_content      |     | id, user_id               |
|   _history                |     | agent_type                |
|---------------------------|     | messages (JSONB)          |
| id, user_id               |     | context (JSONB)           |
| content, content_type     |     +---------------------------+
| embedding (vector 1536)   |
| metadata (JSONB)          |     +---------------------------+
+---------------------------+     | social_midia_automation   |
                                  |   _rules                  |
+---------------------------+     |---------------------------|
| social_midia_notifications|     | name, trigger_type        |
|---------------------------|     | trigger_config (JSONB)    |
| id, user_id               |     | action_type               |
| channel, type             |     | action_config (JSONB)     |
| subject, body             |     | is_active                 |
| sent_at, read_at          |     +---------------------------+
+---------------------------+

+---------------------------+     +---------------------------+
| social_midia_brand        |     | AGNO: agentesocial        |
|   _documents              |     |   _sessions               |
|---------------------------|     |   _memories               |
| id, user_id               |     |   _team_sessions          |
| name, type, content       |     |---------------------------|
| file_url                  |     | Persistencia de memoria   |
| embedding_ids[]           |     | e sessoes dos agentes IA  |
+---------------------------+     +---------------------------+
```

### Seguranca do Banco (RLS)

Cada usuario so acessa seus proprios dados. Isso e garantido por **Row Level Security (RLS)**:

```
+-------------------------------------------------------------------+
|                    SEGURANCA POR LINHA (RLS)                       |
+-------------------------------------------------------------------+
|                                                                     |
|  Usuario A (user_id = "abc")    Usuario B (user_id = "xyz")       |
|                                                                     |
|  Vê SOMENTE:                   Ve SOMENTE:                        |
|  - Seus posts                  - Seus posts                        |
|  - Suas conversas              - Suas conversas                    |
|  - Seus relatorios             - Seus relatorios                   |
|  - Seu brand voice             - Seu brand voice                   |
|                                                                     |
|  NAO ve dados do Usuario B     NAO ve dados do Usuario A           |
|                                                                     |
|  Excecao: viral_content e publico (somente leitura)                |
|                                                                     |
+-------------------------------------------------------------------+
```

---

## 10. Sistema de Memoria

O AgenteSocial possui um sistema de memoria de 3 camadas que permite aos agentes "lembrar" do usuario:

```
+-------------------------------------------------------------------+
|                 SISTEMA DE MEMORIA (3 CAMADAS)                     |
+-------------------------------------------------------------------+
|                                                                     |
|  CAMADA 1: WORKING MEMORY (Sessao Atual)                          |
|  +---------------------------------------------------------------+ |
|  | Contexto da conversa atual                                    | |
|  | Ultimas 5 interacoes do agente                                | |
|  | Dura enquanto a sessao estiver ativa                          | |
|  +---------------------------------------------------------------+ |
|                                                                     |
|  CAMADA 2: EPISODIC MEMORY (90 dias — PostgreSQL)                  |
|  +---------------------------------------------------------------+ |
|  | Historico de conversas                                         | |
|  | Conteudos criados recentemente                                | |
|  | Metricas e analytics                                          | |
|  | Armazenado em tabelas do Supabase                             | |
|  +---------------------------------------------------------------+ |
|                                                                     |
|  CAMADA 3: SEMANTIC MEMORY (Permanente — pgvector)                 |
|  +---------------------------------------------------------------+ |
|  | Tom de voz da marca (brand voice)                             | |
|  | Preferencias do usuario                                       | |
|  | Padroes de sucesso aprendidos                                 | |
|  | Busca por SIMILARIDADE semantica (vetores 1536D)              | |
|  |                                                                | |
|  | Exemplo: "fitness" encontra "exercicio", "academia", "saude"  | |
|  +---------------------------------------------------------------+ |
|                                                                     |
+-------------------------------------------------------------------+

Como funciona a busca semantica:

  "Qual post sobre marketing teve mais engajamento?"
                    |
                    v
  +-------------------------------------------+
  | 1. Texto convertido em vetor (1536 dims)  |
  | 2. Busca por similaridade no pgvector     |
  | 3. Retorna os 10 mais similares           |
  | 4. Threshold: 0.7 (70% similaridade)      |
  +-------------------------------------------+
                    |
                    v
  Resultado: Posts sobre marketing ordenados por relevancia
```

---

## 11. Seguranca e Autenticacao

```
+-------------------------------------------------------------------+
|                       AUTENTICACAO                                  |
+-------------------------------------------------------------------+
|                                                                     |
|  METODO 1: JWT (Supabase Auth) — Para usuarios finais              |
|  +---------------------------------------------------------------+ |
|  | Header: Authorization: Bearer eyJhbG...                       | |
|  | Algoritmo: HS256                                              | |
|  | Claims: sub (user_id), email, role, exp                       | |
|  | Validado contra SUPABASE_JWT_SECRET                           | |
|  +---------------------------------------------------------------+ |
|                                                                     |
|  METODO 2: API Key — Para servico-a-servico                        |
|  +---------------------------------------------------------------+ |
|  | Header: X-API-Key: sua-chave-secreta                          | |
|  | Comparado com API_SECRET_KEY do .env                          | |
|  +---------------------------------------------------------------+ |
|                                                                     |
|  METODO 3: Modo Dev — Sem chaves configuradas                      |
|  +---------------------------------------------------------------+ |
|  | Retorna user_id: "dev-mode"                                   | |
|  | APENAS para desenvolvimento local                             | |
|  +---------------------------------------------------------------+ |
|                                                                     |
+-------------------------------------------------------------------+
```

---

## 12. Tecnologias Utilizadas

```
+-------------------------------------------------------------------+
|                    STACK TECNOLOGICO                                |
+-------------------------------------------------------------------+
|                                                                     |
|  BACKEND                                                            |
|  +-------------------+  +-------------------+                      |
|  | FastAPI 0.115.6   |  | Python 3.12       |                      |
|  | (Framework Web)   |  | (Linguagem)       |                      |
|  +-------------------+  +-------------------+                      |
|                                                                     |
|  IA / AGENTES                                                       |
|  +-------------------+  +-------------------+                      |
|  | AGNO 2.5.2        |  | OpenAI GPT-4.1    |                      |
|  | (Orquestracao)    |  | (mini + nano)     |                      |
|  +-------------------+  +-------------------+                      |
|  +-------------------+  +-------------------+                      |
|  | DuckDuckGo Search |  | Whisper API       |                      |
|  | (Busca Web)       |  | (Transcricao)     |                      |
|  +-------------------+  +-------------------+                      |
|                                                                     |
|  BANCO DE DADOS                                                     |
|  +-------------------+  +-------------------+                      |
|  | Supabase          |  | PostgreSQL        |                      |
|  | (BaaS + Auth)     |  | + pgvector        |                      |
|  +-------------------+  +-------------------+                      |
|                                                                     |
|  CACHE E FILAS                                                      |
|  +-------------------+  +-------------------+                      |
|  | Redis 5.2.1       |  | Celery 5.4.0      |                      |
|  | (Cache)           |  | (Task Queue)      |                      |
|  +-------------------+  +-------------------+                      |
|                                                                     |
|  INTEGRACOES                                                        |
|  +-------------------+  +-------------------+                      |
|  | Instagram Graph   |  | YouTube Data v3   |                      |
|  | API               |  | API               |                      |
|  +-------------------+  +-------------------+                      |
|  +-------------------+  +-------------------+                      |
|  | Google Trends     |  | Resend (Email)    |                      |
|  | (pytrends)        |  |                   |                      |
|  +-------------------+  +-------------------+                      |
|                                                                     |
+-------------------------------------------------------------------+
```

---

## 13. Como Instalar e Rodar

### Pre-requisitos

- Python 3.12+
- Conta no Supabase (gratuita)
- Chave da API OpenAI
- (Opcional) Redis, Instagram API, YouTube API

### Passo a Passo

```
1. CLONE O REPOSITORIO
   git clone <url-do-repo>
   cd AgenteSocial

2. CONFIGURE O AMBIENTE
   cp .env.example .env
   # Edite o .env com suas chaves:
   #   OPENAI_API_KEY=sk-...
   #   SUPABASE_URL=https://...
   #   SUPABASE_KEY=...
   #   SUPABASE_JWT_SECRET=...

3. CRIE O VIRTUAL ENVIRONMENT
   cd backend
   uv venv --python 3.12 .venv
   source .venv/bin/activate

4. INSTALE AS DEPENDENCIAS
   uv pip install -r requirements.txt

5. EXECUTE AS MIGRATIONS NO SUPABASE
   # No SQL Editor do Supabase, execute em ordem:
   #   001_initial_schema.sql
   #   002_memory_tables.sql
   #   003_rls_policies.sql
   #   004_rename_tables_social_midia.sql
   #   005_fix_vector_search.sql
   #   006_agno_memory_storage.sql

6. RODE O SERVIDOR
   uvicorn app.main:app --reload

7. ACESSE
   http://localhost:8000/docs    (Documentacao interativa)
   http://localhost:8000/health  (Health check)
```

### Verificacao Rapida

```bash
# Verificar versao do AGNO
python -c "import agno; print(agno.__version__)"
# Esperado: 2.5.2

# Verificar criacao do team
python -c "from app.agents.team import create_team; t = create_team(); print(f'{len(t.members)} sub-teams')"
# Esperado: 4 sub-teams

# Rodar testes
python -m pytest tests/ -v
```

---

## Resumo Visual Final

```
+===================================================================+
||                                                                   ||
||                      AGENTESOCIAL                                ||
||           Seu time de marketing digital com IA                   ||
||                                                                   ||
||  +---+  +---+  +---+  +---+  +---+  +---+  +---+  +---+       ||
||  | C |  | V |  | H |  | A |  | V |  | S |  | P |  | V |       ||
||  | o |  | i |  | a |  | n |  | i |  | t |  | o |  | i |       ||
||  | n |  | s |  | s |  | a |  | r |  | r |  | d |  | d |       ||
||  | t |  | u |  | h |  | l |  | a |  | a |  | c |  | e |       ||
||  | e |  | a |  | t |  | i |  | l |  | t |  | a |  | o |       ||
||  | u |  | l |  | a |  | s |  |   |  | e |  | s |  |   |       ||
||  | d |  |   |  | g |  | t |  | T |  | g |  | t |  | S |       ||
||  | o |  | D |  |   |  |   |  | r |  | y |  |   |  | c |       ||
||  |   |  | e |  | H |  |   |  | a |  |   |  | C |  | r |       ||
||  | W |  | s |  | u |  |   |  | c |  | A |  | r |  | i |       ||
||  | r |  | i |  | n |  |   |  | k |  | d |  | e |  | p |       ||
||  | i |  | g |  | t |  |   |  | e |  | v |  | a |  | t |       ||
||  | t |  | n |  | e |  |   |  | r |  | i |  | t |  |   |       ||
||  | e |  | e |  | r |  |   |  |   |  | s |  | o |  | W |       ||
||  | r |  | r |  |   |  |   |  |   |  | o |  | r |  | r |       ||
||  |   |  |   |  |   |  |   |  |   |  | r |  |   |  | i |       ||
||  +---+  +---+  +---+  +---+  +---+  +---+  +---+  +---+       ||
||                                                                   ||
||  +---+  +---+  +---+                                             ||
||  | C |  | R |  | M |    + Calendar Planner                      ||
||  | a |  | e |  | e |    + Report Generator                      ||
||  | l |  | p |  | m |    + Memory Agent                          ||
||  | e |  | o |  | o |                                             ||
||  | n |  | r |  | r |    = 11 agentes especializados             ||
||  | d |  | t |  | y |    = 4 sub-times coordenados               ||
||  | a |  |   |  |   |    = 7 plataformas suportadas              ||
||  | r |  | G |  | A |    = 20 tabelas no banco                   ||
||  |   |  | e |  | g |    = 40+ endpoints de API                  ||
||  +---+  | n |  | e |    = 100% em portugues BR                  ||
||         +---+  | n |                                             ||
||                | t |                                             ||
||                +---+                                             ||
||                                                                   ||
+===================================================================+
```

---

*Documento gerado em Fevereiro 2026 | AgenteSocial v2.0 com AGNO 2.5.2*
