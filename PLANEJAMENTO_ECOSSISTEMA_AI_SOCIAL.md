# ECOSSISTEMA AI SOCIAL MEDIA - Planejamento Completo

> **Projeto:** AgenteSocial - Assessoria Completa de Redes Sociais com IA
> **Data:** 15/02/2026
> **Status:** Planejamento

---

## 1. PESQUISA DE MERCADO

### 1.1 Produtos Existentes (Referência)

| Plataforma | Foco Principal | Destaques | Limitacao |
|-----------|---------------|-----------|-----------|
| **Predis.ai** | Criacao de conteudo visual | Posts, carroseis, videos, analise de concorrentes, hashtags | Sem podcast, sem multi-agente |
| **Lately.ai** | Repurposing de conteudo | Memoria de padroes, aprende com analytics, repropoe conteudo | Sem criacao visual, sem podcast |
| **FeedHive** | Scheduling inteligente | Predicao de viralidade, sugestoes de melhoria pre-publicacao | Sem analise profunda, sem PDF |
| **Ocoya** | Copywriting + scheduling | 50+ templates, multi-plataforma, design AI | Sem agentes, sem memoria |
| **ContentStudio** | Ecossistema completo | Descoberta de conteudo viral, automacoes, analytics, PDF | Sem multi-agente IA |
| **Jasper AI** | Marketing suite | Brand voice memory, campanhas multi-canal, arte IA | Caro, sem podcast dedicado |
| **Castmagic** | Podcast para conteudo | Transcricao, gera posts/newsletters/show notes de podcasts | So podcast, sem social |
| **Sprout Social** | Enterprise social | Listening social, CRM, relatorios PDF, email | Sem IA generativa avancada |
| **Taplio** | LinkedIn growth | Banco de posts virais, analise de padroes, lead gen | So LinkedIn |
| **Opus Clip** | Video clipping | Corte automatico, score de viralidade, legendas | So video |

### 1.2 Projetos Open Source (GitHub)

| Projeto | Framework | Descricao |
|---------|-----------|-----------|
| `alejandro-ao/crewai-instagram-example` | CrewAI | Multi-agente para Instagram (Market Researcher + Copy Writer) |
| `bhancockio/instagram-llama3-crewai` | CrewAI + Llama3 | Automacao de posts Instagram com agentes |
| `crewAIInc/crewAI-examples` | CrewAI | Exemplos oficiais incluindo Instagram Post |
| `falakrana/crewai-content-generator` | CrewAI | Gerador de conteudo com historico (gatherer + thinker + writer) |
| `ashishpatel26/500-AI-Agents-Projects` | Multi | 500 projetos de agentes IA, incluindo social media |

### 1.3 Gap no Mercado

**NENHUM produto atual cobre 100% do que voce descreveu.** A maioria cobre 4-6 de 9 funcionalidades. O sistema que voce viu provavelmente era um projeto custom com CrewAI/LangGraph demonstrado em YouTube ou conferencia.

**Nossa oportunidade:** Criar o PRIMEIRO ecossistema completo com TODOS os 9 pilares integrados.

---

## 2. OS 9 PILARES DO ECOSSISTEMA

```
+==================================================================================+
|                        ECOSSISTEMA AI SOCIAL MEDIA                               |
+==================================================================================+
|                                                                                  |
|  [1] ANALISE        [2] VIRAL          [3] CONTEUDO       [4] PODCAST           |
|  Perfis e Redes     Trends & Hash      Posts/Stories      Roteiros/Scripts       |
|                                                                                  |
|  [5] AUTOMACAO      [6] RELATORIOS     [7] MEMORIA        [8] EMAIL             |
|  Workflows          PDF/Analytics      Aprendizado        Notificacoes           |
|                                                                                  |
|  [9] ASSESSORIA COMPLETA - Orquestracao de todos os pilares                     |
|                                                                                  |
+==================================================================================+
```

### Pilar 1: Analise de Redes Sociais
- Analise de perfis Instagram (bio, feed, engagement rate, crescimento)
- Analise de canais YouTube (videos, views, inscricoes, retention)
- Analise de perfis TikTok, LinkedIn, Twitter/X
- Benchmarking de concorrentes
- Audiencia e demografia
- Melhores horarios de postagem

### Pilar 2: Deteccao de Conteudo Viral
- Monitoramento de posts virais por nicho
- Analise de hashtags trending
- Deteccao de termos e temas em alta
- Score de viralidade para conteudo
- Analise de formatos que performam melhor
- Referencia cruzada entre plataformas

### Pilar 3: Criacao de Conteudo
- Posts para Instagram (feed, carrossel, single image)
- Stories Instagram (sequencias, CTAs, polls)
- Reels/Shorts (roteiros + descricoes)
- Threads e tweets
- Posts LinkedIn
- Legendas otimizadas com hashtags
- Sugestoes de imagem/design (prompts para geracao)

### Pilar 4: Podcast & Video
- Roteiros completos para podcasts
- Show notes automaticas
- Clipping de momentos virais
- Transcricao e resumo
- Repurposing: podcast -> posts, stories, threads
- Sugestoes de temas baseadas em trends

### Pilar 5: Automacoes
- Calendario editorial automatico
- Scheduling de posts
- Workflows de aprovacao
- Triggers baseados em eventos (novo trend, data comemorativa)
- Respostas automaticas a comentarios
- Republishing de conteudo evergreen

### Pilar 6: Relatorios & Analytics
- Dashboard de metricas em tempo real
- Relatorios PDF automaticos (semanal/mensal)
- Analise de performance por tipo de conteudo
- ROI de conteudo
- Comparativo com periodos anteriores
- Exportacao CSV/Excel

### Pilar 7: Sistema de Memoria
- Aprendizado do tom de voz da marca
- Historico de conteudos que performaram bem
- Padroes de engajamento por tipo de post
- Preferencias do usuario
- Base de conhecimento do nicho (RAG)
- Documentos/PDFs da marca como contexto

### Pilar 8: Comunicacao & Email
- Emails automaticos com relatorios
- Notificacoes de trends relevantes
- Alertas de performance (viral post, queda de engagement)
- Newsletter com insights semanais
- Resumo diario para o gestor
- Integracoes WhatsApp/Telegram

### Pilar 9: Assessoria Estrategica
- Planejamento mensal de conteudo
- Analise SWOT do perfil
- Recomendacoes personalizadas
- Consultoria de crescimento baseada em dados
- Plano de acao com prioridades
- Review e otimizacao continua

---

## 3. ARQUITETURA DOS AGENTES IA

### 3.1 Diagrama da Equipe de Agentes

```
                    +========================+
                    |   MASTER ORCHESTRATOR   |
                    |   (Supervisor Agent)    |
                    |   GPT-4.1-mini / Claude |
                    +========================+
                              |
          +-------------------+-------------------+
          |                   |                   |
    +============+     +============+      +============+
    |  RESEARCH  |     |  CREATIVE  |      | STRATEGIC  |
    |   SQUAD    |     |   SQUAD    |      |   SQUAD    |
    +============+     +============+      +============+
    |            |     |            |      |            |
    v            v     v            v      v            v

+--------+  +--------+  +--------+  +--------+  +--------+  +--------+
| Social | | Viral  | | Content | |Podcast | |Strategy| |Report |
|Analyst | |Tracker | | Writer | |Creator | |Advisor | |  Gen  |
+--------+  +--------+  +--------+  +--------+  +--------+  +--------+

+--------+  +--------+  +--------+  +--------+  +--------+  +--------+
|  SEO   | |Hashtag | | Visual | | Video  | |Calendar| | Email |
|Analyst | |Hunter  | |Designer| |Scripter| |Planner | |Sender |
+--------+  +--------+  +--------+  +--------+  +--------+  +--------+

                    +========================+
                    |    MEMORY AGENT        |
                    | (Transversal - RAG)    |
                    | ChromaDB / Pinecone    |
                    +========================+
```

### 3.2 Definicao de Cada Agente

#### MASTER ORCHESTRATOR (Agente Principal)
```yaml
nome: Master Orchestrator
modelo: GPT-4.1-mini ou Claude Sonnet
papel: Supervisor e orquestrador de todos os agentes
responsabilidades:
  - Receber requests do usuario
  - Delegar para o agente correto
  - Coordenar workflows multi-agente
  - Consolidar resultados
  - Manter contexto da conversa
modo: Supervisor (determine_input_for_members=True)
```

#### RESEARCH SQUAD (Esquadrao de Pesquisa)

**1. Social Media Analyst**
```yaml
nome: Social Analyst
modelo: GPT-4.1-nano
papel: Analista de perfis e metricas de redes sociais
ferramentas:
  - Instagram Graph API (perfil, posts, stories, insights)
  - YouTube Data API v3 (canal, videos, analytics)
  - TikTok API (perfil, videos, engagement)
  - Twitter/X API v2 (perfil, tweets, analytics)
  - LinkedIn API (company pages, posts)
  - Apify scrapers (quando API nao disponivel)
outputs:
  - Relatorio de perfil completo
  - Metricas de engagement
  - Benchmarking competitivo
  - Analise de audiencia
```

**2. Viral Content Tracker**
```yaml
nome: Viral Tracker
modelo: GPT-4.1-nano
papel: Detector de conteudo viral e tendencias
ferramentas:
  - Google Trends API
  - Instagram Explore scraper
  - TikTok Trending scraper
  - Twitter/X Trending Topics
  - Reddit API (subreddits do nicho)
  - YouTube Trending
  - NewsAPI (noticias do nicho)
outputs:
  - Lista de conteudos virais do nicho
  - Trends emergentes
  - Formatos em alta
  - Timing de trends
```

**3. Hashtag & SEO Analyst**
```yaml
nome: Hashtag Hunter
modelo: GPT-4.1-nano
papel: Pesquisa e otimizacao de hashtags e SEO social
ferramentas:
  - Hashtag API (volume, competicao, related)
  - Instagram hashtag search
  - YouTube keyword tool
  - TikTok keyword insights
  - Google Search Console API
outputs:
  - Sets de hashtags otimizados por post
  - Keywords para YouTube SEO
  - Estrategia de SEO social
  - Trending hashtags do nicho
```

#### CREATIVE SQUAD (Esquadrao Criativo)

**4. Content Writer**
```yaml
nome: Content Writer
modelo: GPT-4.1-mini (precisa de qualidade superior)
papel: Criacao de textos e legendas para redes sociais
ferramentas:
  - Memory Agent (tom de voz, historico)
  - Template library (formatos de post)
  - Emoji optimizer
  - CTA generator
  - Hook generator (primeiras linhas)
outputs:
  - Legendas Instagram (feed, carrossel, reels)
  - Stories copy (sequencias)
  - Threads Twitter/X
  - Posts LinkedIn
  - Descricoes YouTube
  - Scripts de Reels/Shorts
```

**5. Visual Designer Agent**
```yaml
nome: Visual Designer
modelo: GPT-4.1-nano + DALL-E 3 / Midjourney API
papel: Sugestoes visuais e geracao de prompts de design
ferramentas:
  - DALL-E 3 API (geracao de imagens)
  - Canva API (templates)
  - Color palette generator
  - Brand kit manager
  - Image analysis (para analise de feed)
outputs:
  - Prompts de imagem otimizados
  - Sugestoes de layout para carrossel
  - Paleta de cores da marca
  - Feed preview (grid visual)
  - Thumbnails sugeridas
```

**6. Podcast & Video Creator**
```yaml
nome: Podcast Creator
modelo: GPT-4.1-mini
papel: Roteiros de podcast e video, repurposing
ferramentas:
  - Whisper API (transcricao)
  - YouTube Transcript API
  - Podcast RSS parser
  - Audio analysis
  - Memory Agent (temas anteriores)
outputs:
  - Roteiros de podcast completos
  - Show notes
  - Timestamps e capitulos
  - Clips sugeridos para reels
  - Repurposing: audio -> posts/threads/stories
  - Sugestoes de convidados
```

**7. Video Script Writer**
```yaml
nome: Video Scripter
modelo: GPT-4.1-nano
papel: Roteiros para Reels, Shorts, TikTok e YouTube
ferramentas:
  - Hook database (ganchos que funcionam)
  - Trend analysis (formatos em alta)
  - Template de roteiros (por formato)
  - CTA library
outputs:
  - Roteiros de Reels (15s, 30s, 60s, 90s)
  - Roteiros de Shorts
  - Scripts de YouTube (estrutura completa)
  - Storyboards textuais
```

#### STRATEGIC SQUAD (Esquadrao Estrategico)

**8. Strategy Advisor**
```yaml
nome: Strategy Advisor
modelo: GPT-4.1-mini
papel: Consultoria estrategica de redes sociais
ferramentas:
  - Memory Agent (historico completo do cliente)
  - Analytics data (performance passada)
  - Market research tools
  - Competitor analysis data
outputs:
  - Planejamento mensal de conteudo
  - Analise SWOT do perfil
  - Recomendacoes de crescimento
  - Plano de acao priorizado
  - Review de estrategia
```

**9. Calendar Planner**
```yaml
nome: Calendar Planner
modelo: GPT-4.1-nano
papel: Planejamento e scheduling de conteudo
ferramentas:
  - Best time to post API
  - Google Calendar API
  - Holiday/event database (datas comemorativas)
  - Content recycling engine
outputs:
  - Calendario editorial semanal/mensal
  - Scheduling otimizado por plataforma
  - Datas comemorativas relevantes
  - Plano de frequencia de posts
```

**10. Report Generator**
```yaml
nome: Report Gen
modelo: GPT-4.1-nano
papel: Geracao de relatorios e dashboards
ferramentas:
  - ReportLab / WeasyPrint (PDF generation)
  - Recharts / Chart.js (graficos)
  - Data aggregation tools
  - Email service (SendGrid/Resend)
outputs:
  - Relatorio PDF semanal
  - Relatorio PDF mensal
  - Dashboard interativo
  - Email com resumo
  - Exportacao CSV/Excel
```

**11. Email & Notification Agent**
```yaml
nome: Email Agent
modelo: GPT-4.1-nano
papel: Envio de emails, notificacoes e alertas
ferramentas:
  - SendGrid / Resend API
  - WhatsApp Business API (UAZAPI)
  - Telegram Bot API
  - Push notification service
  - Template engine (emails HTML)
outputs:
  - Emails de relatorio automatico
  - Alertas de trends
  - Notificacoes de performance
  - Newsletter semanal
  - Mensagens WhatsApp/Telegram
```

#### TRANSVERSAL AGENT (Agente Transversal)

**12. Memory Agent (RAG)**
```yaml
nome: Memory Agent
modelo: Embedding model (text-embedding-3-small)
papel: Memoria de longo prazo, aprendizado e contexto
ferramentas:
  - ChromaDB / Pinecone (vector store)
  - Document loader (PDF, DOCX, TXT)
  - Conversation memory
  - Pattern analyzer
  - Brand voice extractor
funcionalidades:
  - Armazena tom de voz da marca
  - Aprende padroes de conteudo que funcionam
  - Mantem historico de posts e performance
  - Indexa documentos da marca (manual, brand book, PDFs)
  - Fornece contexto para todos os outros agentes
  - Evolui com o tempo (melhora recomendacoes)
```

### 3.3 Fluxo de Comunicacao entre Agentes

```
USUARIO
  |
  v
[Master Orchestrator] ---> Identifica intencao
  |
  |--- "Analise meu Instagram" --> Social Analyst + Memory Agent
  |
  |--- "Crie posts para semana" --> Content Writer + Hashtag Hunter
  |                                  + Visual Designer + Calendar Planner
  |
  |--- "Trends do meu nicho" --> Viral Tracker + Hashtag Hunter
  |
  |--- "Roteiro de podcast" --> Podcast Creator + Memory Agent
  |
  |--- "Relatorio mensal" --> Report Generator + Social Analyst
  |                            + Email Agent
  |
  |--- "Plano estrategico" --> Strategy Advisor + Social Analyst
  |                             + Viral Tracker + Calendar Planner
  |
  v
[Memory Agent] <--- Todos os agentes alimentam a memoria
```

---

## 4. STACK TECNOLOGICO

### 4.1 Backend (Agentes IA)

```yaml
Framework de Agentes: Agno (Python) - Supervisor mode
  - Motivo: Ja temos experiencia com NEXMA (Agent Master v2.1)
  - Alternativa: CrewAI ou LangGraph

Modelos IA:
  - Master: OpenAIResponses(id="gpt-4.1-mini") ou Claude Sonnet
  - Especialistas: OpenAIResponses(id="gpt-4.1-nano")
  - Embeddings: text-embedding-3-small
  - Imagens: DALL-E 3 API
  - Transcricao: Whisper API

API Framework: FastAPI (Python)
  - Endpoints REST para cada funcionalidade
  - WebSocket para chat em tempo real
  - Background tasks com Celery/Redis

Vector Database: ChromaDB (local) ou Pinecone (cloud)
  - Memoria de longo prazo
  - RAG para documentos da marca
  - Historico de conteudos

Cache & Queue: Redis
  - Cache de resultados de API
  - Fila de tarefas assincronas
  - Rate limiting

Database: Supabase (PostgreSQL)
  - Dados do usuario e perfis
  - Historico de conteudos gerados
  - Metricas e analytics
  - Configuracoes e preferencias
```

### 4.2 Frontend

```yaml
Framework: Next.js 16 (React 19)
  - App Router
  - Server Components
  - Streaming SSR

UI Library: shadcn/ui + Tailwind CSS 4
  - Components prontos e customizaveis
  - Design system consistente

Charts: Recharts
  - Graficos de performance
  - Dashboards interativos

Estado: Zustand ou TanStack Query
  - Gerenciamento de estado leve
  - Cache de dados do servidor

Real-time: WebSocket / Server-Sent Events
  - Chat com agentes em tempo real
  - Notificacoes push
  - Status de geracao de conteudo
```

### 4.3 Infraestrutura

```yaml
Deploy Backend: Railway
  - FastAPI + Agentes IA
  - Workers Celery
  - Redis

Deploy Frontend: Vercel
  - Next.js
  - Edge functions
  - CDN global

Database: Supabase
  - PostgreSQL managed
  - Auth (login/signup)
  - Storage (imagens, PDFs, audio)
  - Realtime subscriptions

Monitoramento: Sentry + Posthog
  - Error tracking
  - Analytics de uso
  - Feature flags
```

### 4.4 APIs Externas Necessarias

```yaml
Redes Sociais:
  - Instagram Graph API (Meta Business Suite)
  - YouTube Data API v3
  - Twitter/X API v2
  - TikTok API for Business
  - LinkedIn API

Trends & Search:
  - Google Trends API (pytrends)
  - NewsAPI
  - Reddit API (PRAW)

IA & ML:
  - OpenAI API (GPT-4.1, DALL-E 3, Whisper, Embeddings)
  - Anthropic API (Claude - opcional)

Email & Comunicacao:
  - SendGrid ou Resend
  - UAZAPI (WhatsApp)
  - Telegram Bot API

Outros:
  - Apify (web scraping quando API nao existe)
  - Canva API (design templates)
  - Google Calendar API
```

---

## 5. ESTRUTURA DO PROJETO

```
AgenteSocial/
|
|-- backend/                          # FastAPI + Agentes IA
|   |-- app/
|   |   |-- main.py                   # FastAPI app entry
|   |   |-- config.py                 # Settings e env vars
|   |   |-- dependencies.py           # Dependency injection
|   |   |
|   |   |-- agents/                   # Definicao dos agentes
|   |   |   |-- master.py             # Master Orchestrator
|   |   |   |-- social_analyst.py     # Social Media Analyst
|   |   |   |-- viral_tracker.py      # Viral Content Tracker
|   |   |   |-- hashtag_hunter.py     # Hashtag & SEO Analyst
|   |   |   |-- content_writer.py     # Content Writer
|   |   |   |-- visual_designer.py    # Visual Designer
|   |   |   |-- podcast_creator.py    # Podcast & Video Creator
|   |   |   |-- video_scripter.py     # Video Script Writer
|   |   |   |-- strategy_advisor.py   # Strategy Advisor
|   |   |   |-- calendar_planner.py   # Calendar Planner
|   |   |   |-- report_generator.py   # Report Generator
|   |   |   |-- email_agent.py        # Email & Notifications
|   |   |   |-- memory_agent.py       # Memory Agent (RAG)
|   |   |   |-- team.py               # Team configuration (Supervisor)
|   |   |
|   |   |-- tools/                    # Ferramentas dos agentes
|   |   |   |-- instagram_tools.py    # Instagram Graph API
|   |   |   |-- youtube_tools.py      # YouTube Data API
|   |   |   |-- tiktok_tools.py       # TikTok API
|   |   |   |-- twitter_tools.py      # Twitter/X API
|   |   |   |-- linkedin_tools.py     # LinkedIn API
|   |   |   |-- trends_tools.py       # Google Trends, NewsAPI
|   |   |   |-- hashtag_tools.py      # Hashtag research
|   |   |   |-- scraping_tools.py     # Apify / web scraping
|   |   |   |-- image_tools.py        # DALL-E, Canva
|   |   |   |-- audio_tools.py        # Whisper, podcast tools
|   |   |   |-- pdf_tools.py          # PDF generation
|   |   |   |-- email_tools.py        # SendGrid/Resend
|   |   |   |-- whatsapp_tools.py     # UAZAPI integration
|   |   |   |-- calendar_tools.py     # Google Calendar
|   |   |   |-- memory_tools.py       # ChromaDB operations
|   |   |   |-- supabase_tools.py     # Database operations
|   |   |
|   |   |-- api/                      # Endpoints REST
|   |   |   |-- v1/
|   |   |   |   |-- chat.py           # Chat com agentes (WebSocket)
|   |   |   |   |-- analysis.py       # Endpoints de analise
|   |   |   |   |-- content.py        # Endpoints de conteudo
|   |   |   |   |-- podcast.py        # Endpoints de podcast
|   |   |   |   |-- reports.py        # Endpoints de relatorios
|   |   |   |   |-- calendar.py       # Endpoints de calendario
|   |   |   |   |-- settings.py       # Config do usuario
|   |   |   |   |-- webhooks.py       # Webhooks de redes sociais
|   |   |
|   |   |-- services/                 # Logica de negocio
|   |   |   |-- analysis_service.py
|   |   |   |-- content_service.py
|   |   |   |-- scheduling_service.py
|   |   |   |-- report_service.py
|   |   |   |-- notification_service.py
|   |   |   |-- memory_service.py
|   |   |
|   |   |-- models/                   # Pydantic models
|   |   |   |-- user.py
|   |   |   |-- profile.py
|   |   |   |-- content.py
|   |   |   |-- report.py
|   |   |   |-- schedule.py
|   |   |
|   |   |-- database/                 # Database layer
|   |   |   |-- supabase_client.py
|   |   |   |-- migrations/
|   |
|   |-- tests/
|   |-- requirements.txt
|   |-- Dockerfile
|   |-- railway.toml
|
|-- frontend/                         # Next.js App
|   |-- src/
|   |   |-- app/
|   |   |   |-- (auth)/               # Login/Register
|   |   |   |-- (dashboard)/          # Dashboard principal
|   |   |   |   |-- page.tsx          # Home dashboard
|   |   |   |   |-- analytics/        # Metricas e graficos
|   |   |   |   |-- content/          # Criacao de conteudo
|   |   |   |   |   |-- posts/        # Posts Instagram/Social
|   |   |   |   |   |-- stories/      # Stories
|   |   |   |   |   |-- reels/        # Reels/Shorts scripts
|   |   |   |   |   |-- podcast/      # Podcast roteiros
|   |   |   |   |-- calendar/         # Calendario editorial
|   |   |   |   |-- reports/          # Relatorios PDF
|   |   |   |   |-- strategy/         # Planejamento estrategico
|   |   |   |   |-- profiles/         # Analise de perfis
|   |   |   |   |-- trends/           # Trends e virais
|   |   |   |   |-- memory/           # Docs da marca (upload)
|   |   |   |   |-- settings/         # Configuracoes
|   |   |   |-- chat/                 # Chat com agentes IA
|   |   |
|   |   |-- components/
|   |   |   |-- ui/                   # shadcn components
|   |   |   |-- charts/              # Graficos Recharts
|   |   |   |-- content/             # Content creation components
|   |   |   |-- calendar/            # Calendar components
|   |   |   |-- chat/                # Chat interface
|   |   |   |-- reports/             # Report components
|   |   |
|   |   |-- lib/
|   |   |   |-- supabase/            # Supabase client
|   |   |   |-- api/                 # API client
|   |   |   |-- hooks/               # Custom React hooks
|   |   |   |-- utils/               # Utilities
|   |
|   |-- package.json
|   |-- next.config.ts
|   |-- tailwind.config.ts
|
|-- database/                         # Supabase migrations
|   |-- migrations/
|   |   |-- 001_initial_schema.sql
|   |   |-- 002_content_tables.sql
|   |   |-- 003_analytics_tables.sql
|   |   |-- 004_scheduling_tables.sql
|   |   |-- 005_memory_tables.sql
|   |-- seeds/
|
|-- docs/                             # Documentacao
|   |-- architecture/
|   |-- api/
|   |-- guides/
|
|-- .env.example
|-- docker-compose.yml
|-- README.md
```

---

## 6. SCHEMA DO BANCO DE DADOS (Supabase)

### 6.1 Tabelas Principais

```sql
-- Usuarios e organizacoes
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  avatar_url TEXT,
  plan TEXT DEFAULT 'free', -- free, pro, agency
  organization_id UUID,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Perfis de redes sociais conectados
CREATE TABLE social_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  platform TEXT NOT NULL, -- instagram, youtube, tiktok, twitter, linkedin
  platform_id TEXT NOT NULL, -- ID na plataforma
  username TEXT,
  display_name TEXT,
  followers_count INTEGER,
  access_token TEXT, -- encrypted
  refresh_token TEXT, -- encrypted
  token_expires_at TIMESTAMPTZ,
  last_synced_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Conteudos gerados
CREATE TABLE generated_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  profile_id UUID REFERENCES social_profiles(id),
  type TEXT NOT NULL, -- post, story, reel, thread, podcast_script, carousel
  platform TEXT NOT NULL,
  title TEXT,
  body TEXT NOT NULL, -- conteudo principal
  hashtags TEXT[], -- array de hashtags
  media_urls TEXT[], -- URLs de imagens/videos
  media_prompts TEXT[], -- prompts de geracao de imagem
  status TEXT DEFAULT 'draft', -- draft, approved, scheduled, published
  scheduled_for TIMESTAMPTZ,
  published_at TIMESTAMPTZ,
  performance JSONB, -- likes, comments, shares, views
  agent_used TEXT, -- qual agente gerou
  generation_params JSONB, -- parametros usados
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Calendario editorial
CREATE TABLE content_calendar (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  content_id UUID REFERENCES generated_content(id),
  scheduled_date DATE NOT NULL,
  scheduled_time TIME,
  platform TEXT NOT NULL,
  content_type TEXT NOT NULL,
  status TEXT DEFAULT 'planned', -- planned, created, approved, published
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Trends e conteudo viral detectado
CREATE TABLE viral_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  platform TEXT NOT NULL,
  content_url TEXT,
  author TEXT,
  description TEXT,
  engagement_score NUMERIC,
  virality_score NUMERIC, -- 0-100
  hashtags TEXT[],
  keywords TEXT[],
  content_type TEXT, -- post, reel, video, thread
  detected_at TIMESTAMPTZ DEFAULT now(),
  niches TEXT[], -- nichos relevantes
  metadata JSONB DEFAULT '{}'
);

-- Hashtags pesquisadas e catalogadas
CREATE TABLE hashtag_research (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  hashtag TEXT NOT NULL,
  platform TEXT NOT NULL,
  volume INTEGER, -- volume de uso
  competition TEXT, -- low, medium, high
  related_hashtags TEXT[],
  trend_direction TEXT, -- up, stable, down
  niche TEXT,
  last_researched_at TIMESTAMPTZ DEFAULT now()
);

-- Podcasts e episodios
CREATE TABLE podcast_episodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  title TEXT NOT NULL,
  description TEXT,
  script TEXT, -- roteiro completo
  show_notes TEXT, -- notas do episodio
  topics TEXT[], -- topicos abordados
  audio_url TEXT, -- URL do audio original
  transcription TEXT, -- transcricao completa
  duration_seconds INTEGER,
  clips JSONB, -- [{start, end, title, description}]
  repurposed_content UUID[], -- IDs de conteudos gerados
  status TEXT DEFAULT 'draft', -- draft, recorded, edited, published
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Relatorios gerados
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  type TEXT NOT NULL, -- weekly, monthly, quarterly, custom
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,
  data JSONB NOT NULL, -- dados do relatorio
  pdf_url TEXT, -- URL do PDF gerado
  sent_to TEXT[], -- emails para quem foi enviado
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Analytics snapshots
CREATE TABLE analytics_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id UUID REFERENCES social_profiles(id),
  snapshot_date DATE NOT NULL,
  followers INTEGER,
  following INTEGER,
  posts_count INTEGER,
  engagement_rate NUMERIC,
  avg_likes NUMERIC,
  avg_comments NUMERIC,
  avg_shares NUMERIC,
  avg_views NUMERIC,
  top_performing_content JSONB,
  demographics JSONB,
  best_posting_times JSONB,
  metadata JSONB DEFAULT '{}'
);

-- Memoria e documentos da marca
CREATE TABLE brand_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  name TEXT NOT NULL,
  type TEXT, -- brand_book, manual, reference, pdf
  content TEXT, -- conteudo extraido
  file_url TEXT, -- URL do arquivo original
  embedding_ids TEXT[], -- IDs dos embeddings no vector store
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Configuracoes de automacao
CREATE TABLE automation_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  name TEXT NOT NULL,
  trigger_type TEXT NOT NULL, -- schedule, event, trend_detected, date
  trigger_config JSONB NOT NULL,
  action_type TEXT NOT NULL, -- generate_content, send_report, send_email, notify
  action_config JSONB NOT NULL,
  is_active BOOLEAN DEFAULT true,
  last_triggered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Notificacoes e emails enviados
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  channel TEXT NOT NULL, -- email, whatsapp, telegram, push, in_app
  type TEXT NOT NULL, -- report, alert, trend, summary
  subject TEXT,
  body TEXT,
  sent_at TIMESTAMPTZ,
  read_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}'
);

-- Conversas com agentes (chat)
CREATE TABLE agent_conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  title TEXT,
  agent_type TEXT, -- master, social_analyst, content_writer, etc.
  messages JSONB DEFAULT '[]', -- [{role, content, timestamp}]
  context JSONB DEFAULT '{}', -- contexto da conversa
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

---

## 7. ROADMAP DE DESENVOLVIMENTO

### Fase 0: Setup & Fundacao (Semana 1-2)
```
[ ] Criar repositorio e estrutura do projeto
[ ] Configurar backend FastAPI com Agno
[ ] Configurar frontend Next.js com shadcn/ui
[ ] Configurar Supabase (auth, database, storage)
[ ] Configurar Redis
[ ] Criar schema inicial do banco
[ ] Setup de deploy (Railway + Vercel)
[ ] Configurar .env e variaveis de ambiente
```

### Fase 1: Core Agents (Semana 3-5)
```
[ ] Implementar Master Orchestrator (Supervisor)
[ ] Implementar Memory Agent (ChromaDB + RAG)
[ ] Implementar Content Writer (posts, legendas)
[ ] Implementar chat interface (frontend)
[ ] Criar tools basicas (supabase, memory)
[ ] Testar fluxo completo: usuario -> chat -> conteudo gerado
```

### Fase 2: Social Analysis (Semana 6-8)
```
[ ] Implementar Social Media Analyst
[ ] Integrar Instagram Graph API
[ ] Integrar YouTube Data API
[ ] Implementar dashboard de analytics
[ ] Criar pagina de analise de perfis
[ ] Implementar analytics snapshots automaticos
```

### Fase 3: Viral & Trends (Semana 9-10)
```
[ ] Implementar Viral Content Tracker
[ ] Implementar Hashtag Hunter
[ ] Integrar Google Trends
[ ] Criar pagina de trends
[ ] Implementar score de viralidade
[ ] Feed de conteudo viral do nicho
```

### Fase 4: Content Creation Completo (Semana 11-13)
```
[ ] Implementar Visual Designer Agent
[ ] Implementar Video Script Writer
[ ] Criar interface de criacao por tipo (post, story, reel, carrossel)
[ ] Implementar templates de conteudo
[ ] Gerador de carrosseis
[ ] Previsualizacao de posts
```

### Fase 5: Podcast & Video (Semana 14-16)
```
[ ] Implementar Podcast Creator Agent
[ ] Integrar Whisper para transcricao
[ ] Gerador de roteiros de podcast
[ ] Repurposing: podcast -> posts
[ ] Clipping de momentos virais
[ ] Show notes automaticas
```

### Fase 6: Calendario & Automacoes (Semana 17-19)
```
[ ] Implementar Calendar Planner Agent
[ ] Implementar Strategy Advisor
[ ] Criar interface de calendario editorial
[ ] Drag-and-drop de conteudos
[ ] Automacoes baseadas em regras
[ ] Scheduling de posts
```

### Fase 7: Relatorios & Email (Semana 20-22)
```
[ ] Implementar Report Generator
[ ] Implementar Email Agent
[ ] Geracao de PDF automatica
[ ] Dashboard de metricas avancado
[ ] Emails automaticos semanais/mensais
[ ] Notificacoes WhatsApp/Telegram
```

### Fase 8: Polish & Launch (Semana 23-26)
```
[ ] Onboarding flow completo
[ ] Landing page
[ ] Planos e pricing (Stripe)
[ ] Otimizacao de performance
[ ] Testes E2E
[ ] Security audit
[ ] Documentacao
[ ] Beta launch
```

---

## 8. EQUIPE DE DESENVOLVIMENTO (HUMANOS)

### Opcao A: Equipe Enxuta (3-4 pessoas)
```
1. Full-Stack Dev (voce) - Backend Python + Frontend Next.js
2. AI/ML Engineer - Especialista em agentes, prompts, RAG
3. Designer UI/UX - Interface, landing page, brand
4. (Opcional) DevOps - Infra, CI/CD, monitoramento
```

### Opcao B: Solo + IA (voce + Claude/Cursor)
```
1. Voce - Arquiteto + Dev principal
2. Claude Code - Pair programming, code generation
3. Cursor/Windsurf - IDE assistida por IA
4. Freelancers pontuais - Design, videos de marketing
```

### Opcao C: Squad Completa (6-8 pessoas)
```
1. Tech Lead / Arquiteto
2. Backend Developer (Python/FastAPI)
3. Frontend Developer (Next.js/React)
4. AI Engineer (Agentes, RAG, Prompts)
5. Designer UI/UX
6. Product Manager
7. QA Engineer
8. DevOps Engineer
```

---

## 9. ESTIMATIVAS DE CUSTO MENSAL (Producao)

```yaml
Infraestrutura:
  Railway (backend): $20-50/mes
  Vercel (frontend): $20/mes (Pro)
  Supabase (database): $25/mes (Pro)
  Redis: $10-20/mes
  Total Infra: ~$75-115/mes

APIs de IA:
  OpenAI (GPT-4.1 + DALL-E + Whisper): $50-200/mes (depende do uso)
  Embeddings: $5-20/mes
  Total IA: ~$55-220/mes

APIs Externas:
  SendGrid/Resend: $0-20/mes
  Apify (scraping): $49/mes
  NewsAPI: $0-449/mes
  Total APIs: ~$49-489/mes

TOTAL ESTIMADO: $179-824/mes
(Escala conforme usuarios ativos)
```

---

## 10. MODELO DE NEGOCIO SUGERIDO

```yaml
Free (Gratis):
  - 1 perfil social
  - 10 conteudos/mes
  - Chat com agentes (limitado)
  - Analytics basico

Pro ($29/mes):
  - 5 perfis sociais
  - 100 conteudos/mes
  - Todos os agentes
  - Relatorios PDF
  - Calendario editorial
  - Email semanal

Agency ($79/mes):
  - 20 perfis sociais
  - Conteudos ilimitados
  - Todos os agentes
  - Relatorios personalizados
  - Automacoes avancadas
  - API access
  - Podcast tools
  - Suporte prioritario
  - White label (add-on)
```

---

## 11. DIFERENCIAIS COMPETITIVOS

1. **Multi-Agente Real** - Nao e uma IA generica, sao 12 agentes especializados
2. **Memoria Evolutiva** - O sistema aprende e melhora com o tempo
3. **Podcast Integrado** - Unico com roteiros + repurposing nativo
4. **Assessoria Completa** - Substitui uma agencia de social media inteira
5. **Open Architecture** - Pode integrar com qualquer ferramenta via API
6. **Relatorios Pro** - PDF automatico de qualidade profissional
7. **Multi-Plataforma** - Instagram, YouTube, TikTok, Twitter, LinkedIn
8. **Preco Acessivel** - Fracao do custo de uma agencia real

---

## 12. CODIGO DOS AGENTES (Agno Framework)

### 12.1 Master Orchestrator - team.py

```python
# backend/app/agents/team.py
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team
from agno.storage.postgres import PostgresDb

from app.agents.social_analyst import social_analyst
from app.agents.viral_tracker import viral_tracker
from app.agents.hashtag_hunter import hashtag_hunter
from app.agents.content_writer import content_writer
from app.agents.visual_designer import visual_designer
from app.agents.podcast_creator import podcast_creator
from app.agents.video_scripter import video_scripter
from app.agents.strategy_advisor import strategy_advisor
from app.agents.calendar_planner import calendar_planner
from app.agents.report_generator import report_generator
from app.agents.email_agent import email_agent
from app.config import settings

# Database para memoria persistente
db = PostgresDb(
    table_name="agent_sessions",
    db_url=settings.DATABASE_URL,
)

# Time principal - Supervisor mode
social_media_team = Team(
    name="SocialMediaMaster",
    model=OpenAIResponses(id="gpt-4.1-mini"),
    mode="supervisor",
    agents=[
        social_analyst,
        viral_tracker,
        hashtag_hunter,
        content_writer,
        visual_designer,
        podcast_creator,
        video_scripter,
        strategy_advisor,
        calendar_planner,
        report_generator,
        email_agent,
    ],
    instructions=[
        "Voce e o orquestrador de uma agencia completa de social media com IA.",
        "Analise o pedido do usuario e delegue para o agente especialista correto.",
        "Para tarefas complexas, coordene multiplos agentes em sequencia.",
        "Sempre consulte o contexto do usuario (marca, nicho, tom de voz) antes de delegar.",
        "Responda SEMPRE em portugues brasileiro.",
        "Ao final, sintetize os resultados de todos os agentes em uma resposta coesa.",
        "",
        "REGRAS DE DELEGACAO:",
        "- Analise de perfil/metricas -> Social Analyst",
        "- Trends e virais -> Viral Tracker",
        "- Hashtags e SEO -> Hashtag Hunter",
        "- Textos e legendas -> Content Writer",
        "- Imagens e design -> Visual Designer",
        "- Podcast e audio -> Podcast Creator",
        "- Roteiros de video -> Video Scripter",
        "- Estrategia e planejamento -> Strategy Advisor",
        "- Calendario editorial -> Calendar Planner",
        "- Relatorios PDF -> Report Generator",
        "- Emails e notificacoes -> Email Agent",
        "",
        "WORKFLOWS MULTI-AGENTE:",
        "- 'Crie posts para semana' -> Content Writer + Hashtag Hunter + Calendar Planner",
        "- 'Analise meu perfil' -> Social Analyst + Strategy Advisor",
        "- 'Relatorio mensal' -> Social Analyst + Report Generator + Email Agent",
        "- 'Plano estrategico' -> Social Analyst + Viral Tracker + Strategy Advisor",
    ],
    determine_input_for_members=True,
    show_members_responses=True,
    enable_agentic_memory=True,
    markdown=True,
    storage=db,
)
```

### 12.2 Social Media Analyst

```python
# backend/app/agents/social_analyst.py
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from app.tools.instagram_tools import (
    get_instagram_profile,
    get_instagram_insights,
    get_instagram_media,
    get_instagram_stories_insights,
)
from app.tools.youtube_tools import (
    analyze_youtube_channel,
    get_youtube_video_stats,
    get_youtube_analytics,
)
from app.tools.supabase_tools import (
    save_analytics_snapshot,
    get_historical_analytics,
)

social_analyst = Agent(
    name="SocialAnalyst",
    model=OpenAIResponses(id="gpt-4.1-nano"),
    role="Analista de redes sociais especializado em metricas e performance",
    instructions=[
        "Voce analisa perfis de redes sociais e fornece insights acionaveis.",
        "Sempre apresente dados concretos: numeros, porcentagens, comparativos.",
        "Calcule engagement rate: (likes + comments + shares) / followers * 100",
        "Compare com benchmarks do nicho quando possivel.",
        "Identifique os melhores horarios de postagem baseado nos dados.",
        "Analise os top 10 posts por engagement e identifique padroes.",
        "Responda SEMPRE em portugues brasileiro.",
        "",
        "FORMATO DE RELATORIO:",
        "1. Resumo executivo (3 linhas)",
        "2. Metricas principais (followers, engagement, reach)",
        "3. Top posts e padroes identificados",
        "4. Melhores horarios de postagem",
        "5. Recomendacoes (3-5 acoes concretas)",
    ],
    tools=[
        get_instagram_profile,
        get_instagram_insights,
        get_instagram_media,
        get_instagram_stories_insights,
        analyze_youtube_channel,
        get_youtube_video_stats,
        get_youtube_analytics,
        save_analytics_snapshot,
        get_historical_analytics,
    ],
    markdown=True,
)
```

### 12.3 Viral Content Tracker

```python
# backend/app/agents/viral_tracker.py
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from app.tools.trends_tools import (
    get_google_trends,
    get_trending_topics,
    get_news_by_topic,
)
from app.tools.scraping_tools import (
    scrape_instagram_explore,
    scrape_tiktok_trending,
    scrape_youtube_trending,
)
from app.tools.supabase_tools import (
    save_viral_content,
    get_saved_virals,
)

viral_tracker = Agent(
    name="ViralTracker",
    model=OpenAIResponses(id="gpt-4.1-nano"),
    role="Detector de conteudo viral e tendencias emergentes",
    instructions=[
        "Voce e especialista em detectar conteudo viral e tendencias.",
        "Monitore trends em todas as plataformas e faca cruzamento.",
        "Classifique cada trend com um score de viralidade (0-100).",
        "Identifique o TIMING: trend nascendo, no pico, ou morrendo.",
        "Analise o FORMATO: qual tipo de conteudo esta viralizando.",
        "Responda SEMPRE em portugues brasileiro.",
        "",
        "SCORE DE VIRALIDADE:",
        "- Velocidade de engajamento (likes/hora) = 40%",
        "- Taxa de compartilhamento (shares/impressions) = 30%",
        "- Taxa de salvamento (saves/reach) = 30%",
        "",
        "FORMATO DE RELATORIO:",
        "1. Top 5 trends do momento (com score)",
        "2. Trends emergentes (< 48h)",
        "3. Formatos em alta (reel, carrossel, etc)",
        "4. Hashtags trending",
        "5. Oportunidades de conteudo para o nicho do usuario",
    ],
    tools=[
        get_google_trends,
        get_trending_topics,
        get_news_by_topic,
        scrape_instagram_explore,
        scrape_tiktok_trending,
        scrape_youtube_trending,
        save_viral_content,
        get_saved_virals,
    ],
    markdown=True,
)
```

### 12.4 Content Writer

```python
# backend/app/agents/content_writer.py
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from app.tools.memory_tools import (
    get_brand_voice,
    get_similar_high_performers,
    get_content_templates,
)
from app.tools.hashtag_tools import get_optimized_hashtags
from app.tools.supabase_tools import save_generated_content

content_writer = Agent(
    name="ContentWriter",
    model=OpenAIResponses(id="gpt-4.1-mini"),  # Mini para qualidade
    role="Copywriter especialista em redes sociais",
    instructions=[
        "Voce e um copywriter expert em redes sociais.",
        "SEMPRE consulte o tom de voz da marca antes de escrever.",
        "SEMPRE busque conteudos similares que performaram bem (RAG).",
        "Responda SEMPRE em portugues brasileiro.",
        "",
        "REGRAS POR PLATAFORMA:",
        "",
        "INSTAGRAM FEED:",
        "- Primeira linha e o GANCHO (hook) - mais importante",
        "- Maximo 2200 caracteres, ideal 150-300",
        "- CTA claro no final",
        "- 20-30 hashtags relevantes (nos comentarios)",
        "- Use emojis com moderacao",
        "",
        "INSTAGRAM STORIES:",
        "- Texto curto e direto (max 100 caracteres por slide)",
        "- Sequencia de 3-7 slides",
        "- Inclua enquetes, perguntas, CTAs interativos",
        "- Urgencia e escassez quando apropriado",
        "",
        "INSTAGRAM CARROSSEL:",
        "- Slide 1: Hook forte (titulo impactante)",
        "- Slides 2-9: Conteudo de valor (1 ideia por slide)",
        "- Slide final: CTA + resumo",
        "- Texto curto em cada slide (max 50 palavras)",
        "",
        "REELS/SHORTS:",
        "- Gancho nos primeiros 3 segundos",
        "- Roteiro com timestamps [0s], [3s], [10s]...",
        "- CTA verbal e visual",
        "- Descricao otimizada com keywords",
        "",
        "LINKEDIN:",
        "- Tom profissional mas acessivel",
        "- Primeira linha e gancho (aparece no preview)",
        "- Use line breaks para facilitar leitura",
        "- 1300-1500 caracteres ideal",
        "- 3-5 hashtags relevantes",
        "",
        "TWITTER/X:",
        "- Max 280 caracteres",
        "- Thread se precisar de mais espaco",
        "- Gancho forte no primeiro tweet",
        "- Hashtags limitadas (1-2)",
    ],
    tools=[
        get_brand_voice,
        get_similar_high_performers,
        get_content_templates,
        get_optimized_hashtags,
        save_generated_content,
    ],
    markdown=True,
)
```

### 12.5 Podcast Creator

```python
# backend/app/agents/podcast_creator.py
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from app.tools.audio_tools import (
    transcribe_audio,
    analyze_podcast_feed,
    extract_clips,
)
from app.tools.memory_tools import (
    get_brand_voice,
    get_past_episodes,
)
from app.tools.supabase_tools import save_podcast_episode

podcast_creator = Agent(
    name="PodcastCreator",
    model=OpenAIResponses(id="gpt-4.1-mini"),
    role="Especialista em podcast e repurposing de audio",
    instructions=[
        "Voce cria roteiros de podcast e faz repurposing de episodios.",
        "Responda SEMPRE em portugues brasileiro.",
        "",
        "PARA ROTEIROS DE PODCAST:",
        "- Estrutura: Intro (2min) + Desenvolvimento (15-25min) + Conclusao (3min)",
        "- Intro: gancho, apresentacao do tema, o que o ouvinte vai aprender",
        "- Desenvolvimento: 3-5 blocos tematicos com transicoes",
        "- Conclusao: resumo, CTA, preview proximo episodio",
        "- Inclua MARCADORES DE TEMPO estimados",
        "- Sugira PERGUNTAS para entrevistas",
        "- Sugira MOMENTOS DE CORTE para reels/shorts",
        "",
        "PARA REPURPOSING (audio -> conteudo):",
        "- Transcreva o episodio",
        "- Extraia 5-10 QUOTES impactantes para posts",
        "- Identifique momentos VIRAIS para clips (30-60s)",
        "- Gere SHOW NOTES completas",
        "- Crie THREAD resumo para Twitter",
        "- Gere CARROSSEL com insights principais",
        "- Sugira NEWSLETTER baseada no episodio",
        "",
        "FORMATO DO ROTEIRO:",
        "```",
        "EPISODIO: [Titulo]",
        "DURACAO: [estimada]",
        "TEMA: [tema central]",
        "",
        "[00:00] INTRO",
        "- Gancho: ...",
        "- Apresentacao: ...",
        "",
        "[02:00] BLOCO 1: [subtema]",
        "- Ponto principal: ...",
        "- Exemplo/historia: ...",
        "- Transicao: ...",
        "",
        "[MOMENTO DE CORTE - REEL] [timestamp]",
        "- Quote: '...'",
        "```",
    ],
    tools=[
        transcribe_audio,
        analyze_podcast_feed,
        extract_clips,
        get_brand_voice,
        get_past_episodes,
        save_podcast_episode,
    ],
    markdown=True,
)
```

### 12.6 Strategy Advisor

```python
# backend/app/agents/strategy_advisor.py
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

from app.tools.supabase_tools import (
    get_historical_analytics,
    get_content_performance,
    get_competitor_data,
)
from app.tools.memory_tools import (
    get_brand_voice,
    get_performance_patterns,
    get_audience_insights,
)

strategy_advisor = Agent(
    name="StrategyAdvisor",
    model=OpenAIResponses(id="gpt-4.1-mini"),
    role="Consultor estrategico de redes sociais",
    instructions=[
        "Voce e um consultor estrategico senior de redes sociais.",
        "Base TODAS as recomendacoes em DADOS, nunca em achismo.",
        "Responda SEMPRE em portugues brasileiro.",
        "",
        "ANALISE SWOT DO PERFIL:",
        "- Forcas: o que esta funcionando bem (dados)",
        "- Fraquezas: onde esta perdendo oportunidades",
        "- Oportunidades: trends, gaps, nichos inexplorados",
        "- Ameacas: concorrentes, mudancas de algoritmo",
        "",
        "PLANEJAMENTO MENSAL:",
        "- Semana 1: Tema/pilar A (educativo)",
        "- Semana 2: Tema/pilar B (entretenimento)",
        "- Semana 3: Tema/pilar C (inspiracional)",
        "- Semana 4: Tema/pilar D (promocional)",
        "- Mix de formatos: 40% carrossel, 30% reel, 20% single, 10% stories",
        "",
        "RECOMENDACOES DEVEM SER:",
        "1. Especificas (nao generico)",
        "2. Mensuraveis (com KPIs claros)",
        "3. Acionaveis (passos concretos)",
        "4. Baseadas em dados (numeros reais)",
        "5. Com prazo (quando implementar)",
    ],
    tools=[
        get_historical_analytics,
        get_content_performance,
        get_competitor_data,
        get_brand_voice,
        get_performance_patterns,
        get_audience_insights,
    ],
    markdown=True,
)
```

---

## 13. CODIGO DAS FERRAMENTAS (Tools)

### 13.1 Instagram Tools

```python
# backend/app/tools/instagram_tools.py
import requests
from agno.tools import tool
from app.config import settings


@tool
def get_instagram_profile(account_id: str) -> dict:
    """Busca dados do perfil Instagram Business.

    Args:
        account_id: ID da conta Instagram Business

    Returns:
        dict com dados do perfil (nome, bio, followers, media_count)
    """
    url = f"https://graph.facebook.com/v19.0/{account_id}"
    params = {
        "fields": "id,name,username,biography,followers_count,"
                  "follows_count,media_count,profile_picture_url,website",
        "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


@tool
def get_instagram_insights(
    account_id: str,
    metric: str = "impressions,reach,profile_views,follower_count",
    period: str = "day"
) -> dict:
    """Busca insights/metricas da conta Instagram.

    Args:
        account_id: ID da conta Instagram Business
        metric: Metricas separadas por virgula (impressions,reach,profile_views,follower_count)
        period: Periodo (day, week, days_28, month, lifetime)

    Returns:
        dict com metricas do periodo
    """
    url = f"https://graph.facebook.com/v19.0/{account_id}/insights"
    params = {
        "metric": metric,
        "period": period,
        "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


@tool
def get_instagram_media(account_id: str, limit: int = 25) -> dict:
    """Busca posts recentes do Instagram com metricas.

    Args:
        account_id: ID da conta Instagram Business
        limit: Quantidade de posts (max 100)

    Returns:
        dict com lista de posts e suas metricas
    """
    url = f"https://graph.facebook.com/v19.0/{account_id}/media"
    params = {
        "fields": "id,caption,media_type,media_url,thumbnail_url,"
                  "timestamp,like_count,comments_count,permalink",
        "limit": min(limit, 100),
        "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Calcular engagement para cada post
    for post in data.get("data", []):
        likes = post.get("like_count", 0)
        comments = post.get("comments_count", 0)
        post["engagement"] = likes + comments

    # Ordenar por engagement
    data["data"] = sorted(
        data.get("data", []),
        key=lambda x: x.get("engagement", 0),
        reverse=True,
    )

    return data


@tool
def get_instagram_stories_insights(account_id: str) -> dict:
    """Busca insights dos stories do Instagram.

    Args:
        account_id: ID da conta Instagram Business

    Returns:
        dict com metricas dos stories (impressions, reach, replies, exits)
    """
    url = f"https://graph.facebook.com/v19.0/{account_id}/stories"
    params = {
        "fields": "id,media_type,media_url,timestamp",
        "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    stories = response.json()

    # Buscar insights para cada story
    for story in stories.get("data", []):
        insights_url = f"https://graph.facebook.com/v19.0/{story['id']}/insights"
        insights_params = {
            "metric": "impressions,reach,replies,taps_forward,taps_back,exits",
            "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
        }
        ins_response = requests.get(insights_url, params=insights_params, timeout=30)
        if ins_response.ok:
            story["insights"] = ins_response.json()

    return stories
```

### 13.2 YouTube Tools

```python
# backend/app/tools/youtube_tools.py
from googleapiclient.discovery import build
from agno.tools import tool
from app.config import settings


def _get_youtube_client():
    return build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)


@tool
def analyze_youtube_channel(channel_id: str) -> dict:
    """Analisa um canal do YouTube com metricas completas.

    Args:
        channel_id: ID do canal YouTube (ex: UCxxxxxx)

    Returns:
        dict com estatisticas do canal, videos recentes e metricas
    """
    youtube = _get_youtube_client()

    # Dados do canal
    channel = youtube.channels().list(
        part="statistics,snippet,contentDetails,brandingSettings",
        id=channel_id,
    ).execute()

    if not channel.get("items"):
        return {"error": f"Canal {channel_id} nao encontrado"}

    channel_data = channel["items"][0]
    uploads_playlist = channel_data["contentDetails"]["relatedPlaylists"]["uploads"]

    # Videos recentes (ultimos 50)
    playlist_items = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads_playlist,
        maxResults=50,
    ).execute()

    video_ids = [
        item["contentDetails"]["videoId"]
        for item in playlist_items.get("items", [])
    ]

    # Estatisticas dos videos
    videos = youtube.videos().list(
        part="statistics,contentDetails,snippet",
        id=",".join(video_ids[:50]),
    ).execute()

    # Calcular metricas agregadas
    total_views = 0
    total_likes = 0
    total_comments = 0
    for video in videos.get("items", []):
        stats = video.get("statistics", {})
        total_views += int(stats.get("viewCount", 0))
        total_likes += int(stats.get("likeCount", 0))
        total_comments += int(stats.get("commentCount", 0))

    video_count = len(videos.get("items", []))

    return {
        "channel": {
            "title": channel_data["snippet"]["title"],
            "description": channel_data["snippet"]["description"][:500],
            "subscribers": int(channel_data["statistics"].get("subscriberCount", 0)),
            "total_views": int(channel_data["statistics"].get("viewCount", 0)),
            "video_count": int(channel_data["statistics"].get("videoCount", 0)),
        },
        "recent_videos_stats": {
            "analyzed": video_count,
            "avg_views": total_views // max(video_count, 1),
            "avg_likes": total_likes // max(video_count, 1),
            "avg_comments": total_comments // max(video_count, 1),
            "engagement_rate": round(
                (total_likes + total_comments) / max(total_views, 1) * 100, 2
            ),
        },
        "top_videos": sorted(
            [
                {
                    "title": v["snippet"]["title"],
                    "views": int(v["statistics"].get("viewCount", 0)),
                    "likes": int(v["statistics"].get("likeCount", 0)),
                    "comments": int(v["statistics"].get("commentCount", 0)),
                    "published_at": v["snippet"]["publishedAt"],
                }
                for v in videos.get("items", [])
            ],
            key=lambda x: x["views"],
            reverse=True,
        )[:10],
    }


@tool
def get_youtube_video_stats(video_id: str) -> dict:
    """Busca estatisticas detalhadas de um video do YouTube.

    Args:
        video_id: ID do video YouTube

    Returns:
        dict com views, likes, comments, duracao, tags
    """
    youtube = _get_youtube_client()

    video = youtube.videos().list(
        part="statistics,contentDetails,snippet,topicDetails",
        id=video_id,
    ).execute()

    if not video.get("items"):
        return {"error": f"Video {video_id} nao encontrado"}

    item = video["items"][0]

    return {
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"][:1000],
        "published_at": item["snippet"]["publishedAt"],
        "tags": item["snippet"].get("tags", []),
        "duration": item["contentDetails"]["duration"],
        "views": int(item["statistics"].get("viewCount", 0)),
        "likes": int(item["statistics"].get("likeCount", 0)),
        "comments": int(item["statistics"].get("commentCount", 0)),
        "favorites": int(item["statistics"].get("favoriteCount", 0)),
    }
```

### 13.3 Trends & Viral Detection Tools

```python
# backend/app/tools/trends_tools.py
from pytrends.request import TrendReq
from agno.tools import tool
import requests
from app.config import settings


@tool
def get_google_trends(
    keywords: list[str],
    timeframe: str = "now 7-d",
    geo: str = "BR",
) -> dict:
    """Busca tendencias do Google Trends para palavras-chave.

    Args:
        keywords: Lista de ate 5 palavras-chave para pesquisar
        timeframe: Periodo (now 1-H, now 4-H, now 1-d, now 7-d, today 1-m, today 3-m)
        geo: Pais (BR=Brasil, US=EUA, vazio=global)

    Returns:
        dict com interesse ao longo do tempo e termos relacionados
    """
    pytrends = TrendReq(hl="pt-BR", tz=180)
    pytrends.build_payload(keywords[:5], timeframe=timeframe, geo=geo)

    # Interesse ao longo do tempo
    interest_over_time = pytrends.interest_over_time()

    # Termos relacionados
    related_queries = pytrends.related_queries()

    # Trending searches
    trending = pytrends.trending_searches(pn="brazil")

    result = {
        "keywords": keywords,
        "geo": geo,
        "timeframe": timeframe,
        "interest_over_time": {},
        "related_queries": {},
        "trending_now": trending.head(20).values.tolist() if not trending.empty else [],
    }

    if not interest_over_time.empty:
        for kw in keywords[:5]:
            if kw in interest_over_time.columns:
                values = interest_over_time[kw].tolist()
                result["interest_over_time"][kw] = {
                    "current": values[-1] if values else 0,
                    "peak": max(values) if values else 0,
                    "avg": sum(values) / len(values) if values else 0,
                    "trend": "up" if len(values) > 1 and values[-1] > values[0] else "down",
                }

    for kw in keywords[:5]:
        if kw in related_queries:
            top = related_queries[kw].get("top")
            rising = related_queries[kw].get("rising")
            result["related_queries"][kw] = {
                "top": top.head(10).to_dict("records") if top is not None and not top.empty else [],
                "rising": rising.head(10).to_dict("records") if rising is not None and not rising.empty else [],
            }

    return result


@tool
def get_news_by_topic(topic: str, language: str = "pt") -> dict:
    """Busca noticias recentes sobre um topico via NewsAPI.

    Args:
        topic: Topico para pesquisar
        language: Idioma (pt=portugues, en=ingles)

    Returns:
        dict com lista de noticias recentes
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "language": language,
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": settings.NEWS_API_KEY,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    return {
        "total_results": data.get("totalResults", 0),
        "articles": [
            {
                "title": article["title"],
                "description": article.get("description", ""),
                "source": article["source"]["name"],
                "url": article["url"],
                "published_at": article["publishedAt"],
            }
            for article in data.get("articles", [])[:20]
        ],
    }
```

### 13.4 Audio & Podcast Tools

```python
# backend/app/tools/audio_tools.py
import feedparser
import tempfile
import requests
from openai import OpenAI
from agno.tools import tool
from app.config import settings


@tool
def transcribe_audio(audio_url: str) -> dict:
    """Transcreve audio usando Whisper API (podcast, video, etc).

    Args:
        audio_url: URL do arquivo de audio (mp3, wav, m4a)

    Returns:
        dict com transcricao completa e segmentos com timestamps
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Download do audio
    response = requests.get(audio_url, timeout=120, stream=True)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        for chunk in response.iter_content(chunk_size=8192):
            tmp.write(chunk)
        tmp_path = tmp.name

    # Transcricao com timestamps
    with open(tmp_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            language="pt",
        )

    return {
        "text": transcript.text,
        "duration": transcript.duration,
        "language": transcript.language,
        "segments": [
            {
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
            }
            for seg in (transcript.segments or [])
        ],
    }


@tool
def analyze_podcast_feed(rss_url: str) -> dict:
    """Analisa feed RSS de um podcast para insights de conteudo.

    Args:
        rss_url: URL do feed RSS do podcast

    Returns:
        dict com nome, episodios recentes, topicos e frequencia
    """
    feed = feedparser.parse(rss_url)

    episodes = []
    for entry in feed.entries[:20]:
        audio_url = None
        for link in entry.get("links", []):
            if "audio" in link.get("type", ""):
                audio_url = link.href
                break

        episodes.append({
            "title": entry.get("title", ""),
            "description": entry.get("summary", "")[:500],
            "published": entry.get("published", ""),
            "duration": entry.get("itunes_duration", ""),
            "audio_url": audio_url,
        })

    return {
        "podcast_name": feed.feed.get("title", ""),
        "description": feed.feed.get("subtitle", feed.feed.get("summary", ""))[:500],
        "total_episodes": len(feed.entries),
        "recent_episodes": episodes,
        "categories": [
            tag.get("term", "") for tag in feed.feed.get("tags", [])
        ],
    }


@tool
def extract_clips(
    transcription_segments: list[dict],
    min_duration: int = 15,
    max_duration: int = 90,
) -> list[dict]:
    """Identifica momentos de corte para reels/shorts a partir de transcricao.

    Args:
        transcription_segments: Lista de segmentos com {start, end, text}
        min_duration: Duracao minima do clip em segundos
        max_duration: Duracao maxima do clip em segundos

    Returns:
        Lista de clips sugeridos com timestamps e texto
    """
    clips = []
    current_clip = {"start": 0, "end": 0, "text": "", "segments": []}

    for seg in transcription_segments:
        # Detectar frases impactantes (criterios simples)
        text = seg.get("text", "").strip()
        is_impactful = (
            any(word in text.lower() for word in [
                "importante", "segredo", "dica", "nunca", "sempre",
                "incrivel", "transformou", "mudou", "principal",
                "essencial", "critico", "revelacao", "verdade",
            ])
            or text.endswith("!")
            or text.endswith("?")
        )

        if is_impactful:
            # Criar clip ao redor do momento impactante
            clip_start = max(0, seg["start"] - 5)
            clip_end = min(seg["end"] + 30, seg["end"] + max_duration)

            # Coletar texto dos segmentos no range
            clip_text = " ".join(
                s["text"]
                for s in transcription_segments
                if s["start"] >= clip_start and s["end"] <= clip_end
            )

            duration = clip_end - clip_start
            if min_duration <= duration <= max_duration:
                clips.append({
                    "start_seconds": round(clip_start, 1),
                    "end_seconds": round(clip_end, 1),
                    "duration_seconds": round(duration, 1),
                    "text": clip_text[:500],
                    "hook": text[:100],
                    "timestamp_display": f"{int(clip_start//60)}:{int(clip_start%60):02d}",
                })

    # Retornar top 10 clips mais impactantes
    return clips[:10]
```

### 13.5 Memory Tools (RAG)

```python
# backend/app/tools/memory_tools.py
from openai import OpenAI
from agno.tools import tool
from app.config import settings
from app.database.supabase_client import supabase


async def _generate_embedding(text: str) -> list[float]:
    """Gera embedding para um texto usando OpenAI."""
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


@tool
def get_brand_voice(user_id: str) -> dict:
    """Busca o tom de voz e diretrizes da marca do usuario.

    Args:
        user_id: ID do usuario

    Returns:
        dict com tom de voz, vocabulario, exemplos e persona
    """
    result = supabase.table("brand_voice") \
        .select("*") \
        .eq("organization_id", user_id) \
        .execute()

    if not result.data:
        return {
            "message": "Nenhum brand voice configurado. "
                       "Recomendo configurar para conteudos mais consistentes.",
            "defaults": {
                "tone": "profissional mas acessivel",
                "emoji_use": "moderado",
                "language": "portugues brasileiro",
            }
        }

    return result.data[0]


@tool
def get_similar_high_performers(
    content_brief: str,
    user_id: str,
    top_k: int = 5,
    min_score: float = 0.6,
) -> list[dict]:
    """Busca conteudos similares que performaram bem (RAG via pgvector).

    Args:
        content_brief: Descricao/tema do conteudo a ser criado
        user_id: ID do usuario
        top_k: Quantidade de resultados (default 5)
        min_score: Score minimo de performance (0-1)

    Returns:
        Lista de conteudos similares com alta performance
    """
    import asyncio
    embedding = asyncio.get_event_loop().run_until_complete(
        _generate_embedding(content_brief)
    )

    # Busca por similaridade vetorial no Supabase (pgvector)
    result = supabase.rpc("match_content", {
        "query_embedding": embedding,
        "match_threshold": 0.7,
        "match_count": top_k,
        "min_performance_score": min_score,
        "filter_user_id": user_id,
    }).execute()

    return [
        {
            "content": item["content"][:300],
            "platform": item["platform"],
            "content_type": item["content_type"],
            "performance_score": item["performance_score"],
            "similarity": round(item["similarity"], 3),
            "hashtags": item.get("hashtags", []),
        }
        for item in (result.data or [])
    ]


@tool
def save_to_memory(
    user_id: str,
    content: str,
    platform: str,
    content_type: str,
    hashtags: list[str] = None,
) -> dict:
    """Salva conteudo na memoria de longo prazo com embedding.

    Args:
        user_id: ID do usuario
        content: Texto do conteudo
        platform: Plataforma (instagram, youtube, etc)
        content_type: Tipo (post, reel, story, carousel, etc)
        hashtags: Lista de hashtags usadas

    Returns:
        dict com confirmacao e ID do registro
    """
    import asyncio
    embedding = asyncio.get_event_loop().run_until_complete(
        _generate_embedding(content)
    )

    result = supabase.table("content_history").insert({
        "organization_id": user_id,
        "content": content,
        "platform": platform,
        "content_type": content_type,
        "hashtags": hashtags or [],
        "embedding": embedding,
        "performance_score": 0,  # Atualizado depois via webhook
    }).execute()

    return {"saved": True, "id": result.data[0]["id"] if result.data else None}
```

---

## 14. SISTEMA DE MEMORIA - 3 CAMADAS

### 14.1 Arquitetura de Memoria

```
+================================================================+
|                    ARQUITETURA DE MEMORIA                       |
+================================================================+
|                                                                |
|  CAMADA 1: Working Memory (Curto Prazo)                       |
|  +----------------------------------------------------------+ |
|  | - Contexto da conversa atual                              | |
|  | - Estado do pipeline de conteudo em andamento             | |
|  | - Rascunhos e revisoes em progresso                       | |
|  | - Storage: In-memory (Agno context / LangGraph state)     | |
|  | - TTL: Duracao da sessao                                  | |
|  +----------------------------------------------------------+ |
|                                                                |
|  CAMADA 2: Episodic Memory (Medio Prazo)                      |
|  +----------------------------------------------------------+ |
|  | - Conteudos publicados e performance de cada um           | |
|  | - Interacoes recentes com audiencia                       | |
|  | - Correcoes de brand voice feitas pelo usuario            | |
|  | - Conteudos que funcionaram/falharam (com motivos)        | |
|  | - Storage: Supabase PostgreSQL (tabelas relacionais)      | |
|  | - TTL: 90 dias (rotacao automatica)                       | |
|  +----------------------------------------------------------+ |
|                                                                |
|  CAMADA 3: Semantic Memory (Longo Prazo - RAG)                |
|  +----------------------------------------------------------+ |
|  | - Brand identity e guidelines (vector embeddings)         | |
|  | - Perfis de audiencia/persona                             | |
|  | - Padroes de performance (o que funciona)                 | |
|  | - Conhecimento do nicho e industria                       | |
|  | - Historico de analise competitiva                        | |
|  | - Documentos da marca (PDFs, brand books)                 | |
|  | - Storage: pgvector no Supabase + RAG retrieval           | |
|  | - TTL: Permanente (com atualizacao)                       | |
|  +----------------------------------------------------------+ |
|                                                                |
+================================================================+
```

### 14.2 Schema pgvector para Memoria Semantica

```sql
-- Habilitar extensao pgvector no Supabase
CREATE EXTENSION IF NOT EXISTS vector;

-- Historico de conteudo com embeddings para RAG
CREATE TABLE content_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    content TEXT NOT NULL,
    platform TEXT NOT NULL,
    content_type TEXT NOT NULL,
    hashtags TEXT[],
    keywords TEXT[],
    published_at TIMESTAMPTZ,
    embedding vector(1536),  -- text-embedding-3-small

    -- Metricas de performance (atualizadas via webhook/cron)
    impressions INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    engagement_rate NUMERIC(5,4) DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    performance_score NUMERIC(3,2) DEFAULT 0,  -- 0.00 a 1.00

    -- Metadados de aprendizado
    content_pillar TEXT,     -- educativo, entretenimento, inspiracional, promocional
    tone TEXT,               -- tom usado
    visual_style TEXT,       -- estilo visual
    cta_type TEXT,           -- tipo de CTA usado
    hook_text TEXT,          -- primeira linha/gancho

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indice para busca vetorial (HNSW - rapido)
CREATE INDEX ON content_history
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Tom de voz da marca
CREATE TABLE brand_voice (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    platform TEXT,           -- NULL = todas plataformas
    tone_guidelines TEXT,
    vocabulary_positive TEXT[],   -- Palavras para usar
    vocabulary_negative TEXT[],   -- Palavras para evitar
    example_posts JSONB,         -- Exemplos bons
    audience_persona JSONB,      -- Persona do publico
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Rastreamento de concorrentes
CREATE TABLE competitor_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL,
    competitor_name TEXT NOT NULL,
    platform TEXT NOT NULL,
    handle TEXT,
    follower_count INTEGER,
    avg_engagement_rate NUMERIC(5,4),
    content_frequency TEXT,
    top_content_themes TEXT[],
    last_analyzed_at TIMESTAMPTZ,
    analysis_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Funcao de busca por similaridade vetorial
CREATE OR REPLACE FUNCTION match_content(
    query_embedding vector(1536),
    match_threshold FLOAT,
    match_count INT,
    min_performance_score FLOAT DEFAULT 0,
    filter_user_id UUID DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    platform TEXT,
    content_type TEXT,
    hashtags TEXT[],
    performance_score NUMERIC,
    similarity FLOAT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        ch.id,
        ch.content,
        ch.platform,
        ch.content_type,
        ch.hashtags,
        ch.performance_score,
        1 - (ch.embedding <=> query_embedding) AS similarity
    FROM content_history ch
    WHERE
        1 - (ch.embedding <=> query_embedding) > match_threshold
        AND ch.performance_score >= min_performance_score
        AND (filter_user_id IS NULL OR ch.organization_id = filter_user_id)
    ORDER BY ch.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

### 14.3 Learning Loop (Aprendizado Continuo)

```python
# backend/app/services/learning_service.py
from app.database.supabase_client import supabase
from app.tools.memory_tools import _generate_embedding


class ContentLearningEngine:
    """Motor de aprendizado que melhora recomendacoes com o tempo."""

    async def record_published_content(
        self,
        user_id: str,
        content: str,
        platform: str,
        content_type: str,
        hashtags: list[str] = None,
    ) -> str:
        """Registra conteudo publicado com embedding para futuro RAG."""
        embedding = await _generate_embedding(content)

        result = supabase.table("content_history").insert({
            "organization_id": user_id,
            "content": content,
            "platform": platform,
            "content_type": content_type,
            "hashtags": hashtags or [],
            "embedding": embedding,
            "published_at": "now()",
        }).execute()

        return result.data[0]["id"] if result.data else None

    async def update_performance(
        self,
        content_id: str,
        metrics: dict,
    ) -> None:
        """Atualiza metricas de performance (chamado via webhook/cron)."""
        # Calcular score normalizado (0-1)
        engagement = (
            metrics.get("likes", 0)
            + metrics.get("comments", 0) * 3
            + metrics.get("shares", 0) * 5
            + metrics.get("saves", 0) * 2
        )
        reach = max(metrics.get("reach", 1), 1)
        score = min(engagement / reach, 1.0)

        supabase.table("content_history").update({
            "impressions": metrics.get("impressions", 0),
            "reach": metrics.get("reach", 0),
            "engagement_rate": metrics.get("engagement_rate", 0),
            "likes": metrics.get("likes", 0),
            "comments": metrics.get("comments", 0),
            "shares": metrics.get("shares", 0),
            "saves": metrics.get("saves", 0),
            "performance_score": round(score, 2),
            "updated_at": "now()",
        }).eq("id", content_id).execute()

    async def generate_insights(
        self,
        user_id: str,
        days: int = 30,
    ) -> dict:
        """Gera insights de performance baseado no historico."""
        from datetime import datetime, timedelta

        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

        result = supabase.table("content_history") \
            .select("*") \
            .eq("organization_id", user_id) \
            .gte("published_at", cutoff) \
            .order("performance_score", desc=True) \
            .execute()

        data = result.data or []
        if not data:
            return {"message": "Sem dados suficientes para gerar insights"}

        # Analise por tipo de conteudo
        type_performance = {}
        for item in data:
            ct = item["content_type"]
            if ct not in type_performance:
                type_performance[ct] = {"count": 0, "total_score": 0}
            type_performance[ct]["count"] += 1
            type_performance[ct]["total_score"] += float(item["performance_score"])

        for ct in type_performance:
            type_performance[ct]["avg_score"] = round(
                type_performance[ct]["total_score"] / type_performance[ct]["count"], 2
            )

        # Top hashtags
        all_hashtags = {}
        for item in data:
            for tag in (item.get("hashtags") or []):
                if tag not in all_hashtags:
                    all_hashtags[tag] = {"count": 0, "total_score": 0}
                all_hashtags[tag]["count"] += 1
                all_hashtags[tag]["total_score"] += float(item["performance_score"])

        top_hashtags = sorted(
            [
                {"hashtag": tag, "uses": info["count"],
                 "avg_score": round(info["total_score"] / info["count"], 2)}
                for tag, info in all_hashtags.items()
            ],
            key=lambda x: x["avg_score"],
            reverse=True,
        )[:20]

        return {
            "period_days": days,
            "total_posts": len(data),
            "avg_performance_score": round(
                sum(float(d["performance_score"]) for d in data) / len(data), 2
            ),
            "best_content_types": sorted(
                type_performance.items(),
                key=lambda x: x[1]["avg_score"],
                reverse=True,
            ),
            "top_hashtags": top_hashtags,
            "top_3_posts": [
                {
                    "content": item["content"][:200],
                    "platform": item["platform"],
                    "type": item["content_type"],
                    "score": float(item["performance_score"]),
                }
                for item in data[:3]
            ],
        }
```

---

## 15. ALGORITMO DE DETECCAO VIRAL

```python
# backend/app/services/viral_detection.py

class ViralContentDetector:
    """Detecta conteudo potencialmente viral baseado em velocidade de engajamento."""

    def calculate_virality_score(
        self,
        metrics: dict,
        hours_since_publish: float,
    ) -> float:
        """
        Calcula score de viralidade (0-100).

        Componentes:
        - Velocidade de engajamento (likes+comments+shares por hora) = 40%
        - Taxa de compartilhamento (shares/impressions) = 30%
        - Taxa de salvamento (saves/reach) = 30%
        """
        if hours_since_publish <= 0:
            return 0.0

        likes = metrics.get("likes", 0)
        comments = metrics.get("comments", 0)
        shares = metrics.get("shares", 0)
        saves = metrics.get("saves", 0)
        impressions = max(metrics.get("impressions", 1), 1)
        reach = max(metrics.get("reach", 1), 1)

        # Velocidade de engajamento ponderada
        engagement_velocity = (
            likes
            + comments * 3      # Comentarios valem 3x (indicam debate)
            + shares * 5        # Shares valem 5x (amplificacao organica)
            + saves * 2         # Saves valem 2x (conteudo de referencia)
        ) / hours_since_publish

        # Taxa de compartilhamento (indicador de viralidade organica)
        share_rate = shares / impressions * 100

        # Taxa de salvamento (indicador de qualidade)
        save_rate = saves / reach * 100

        # Score final ponderado
        score = (
            engagement_velocity * 0.4
            + share_rate * 0.3
            + save_rate * 0.3
        )

        return min(round(score, 1), 100.0)

    def classify_trend_stage(
        self,
        data_points: list[dict],
    ) -> str:
        """
        Classifica o estagio de um trend.

        Args:
            data_points: [{timestamp, volume}] ordenados por tempo

        Returns:
            'emerging' | 'growing' | 'peak' | 'declining' | 'dead'
        """
        if len(data_points) < 3:
            return "emerging"

        volumes = [dp["volume"] for dp in data_points]
        recent = volumes[-3:]
        older = volumes[:-3] if len(volumes) > 3 else volumes[:1]

        avg_recent = sum(recent) / len(recent)
        avg_older = sum(older) / len(older) if older else 0
        max_volume = max(volumes)

        if avg_recent > avg_older * 2:
            return "growing"
        elif avg_recent >= max_volume * 0.8:
            return "peak"
        elif avg_recent < avg_older * 0.5:
            return "declining"
        elif avg_recent < avg_older * 0.1:
            return "dead"
        else:
            return "emerging"

    def predict_content_performance(
        self,
        similar_content_scores: list[float],
        posting_hour: int,
        content_type: str,
        hashtag_count: int,
    ) -> dict:
        """
        Prediz performance baseado em padroes historicos.

        Returns:
            dict com predicted_score, confidence e sugestoes
        """
        # Score base: media dos conteudos similares
        base_score = (
            sum(similar_content_scores) / len(similar_content_scores)
            if similar_content_scores
            else 0.5
        )

        # Ajustes baseados em padroes conhecidos
        adjustments = 0.0

        # Melhor horario (picos: 8-9h, 12-13h, 18-20h)
        peak_hours = {8: 0.1, 9: 0.1, 12: 0.05, 13: 0.05, 18: 0.1, 19: 0.15, 20: 0.1}
        adjustments += peak_hours.get(posting_hour, -0.05)

        # Tipo de conteudo (carrosseis e reels performam melhor)
        type_boost = {
            "carousel": 0.15,
            "reel": 0.1,
            "video": 0.05,
            "post": 0.0,
            "story": -0.05,
        }
        adjustments += type_boost.get(content_type, 0.0)

        # Hashtags (sweet spot: 20-30)
        if 20 <= hashtag_count <= 30:
            adjustments += 0.05
        elif hashtag_count < 5 or hashtag_count > 30:
            adjustments -= 0.05

        predicted = min(max(base_score + adjustments, 0.0), 1.0)
        confidence = min(len(similar_content_scores) / 10, 1.0)

        suggestions = []
        if posting_hour not in peak_hours:
            suggestions.append(f"Considere postar entre 18h-20h (horario atual: {posting_hour}h)")
        if content_type == "post":
            suggestions.append("Carrosseis e Reels tendem a ter 15-20% mais engagement")
        if hashtag_count < 15:
            suggestions.append(f"Aumente para 20-30 hashtags (atual: {hashtag_count})")

        return {
            "predicted_score": round(predicted, 2),
            "confidence": round(confidence, 2),
            "suggestions": suggestions,
        }
```

---

## 16. PIPELINE DE AUTOMACAO

### 16.1 Schedule Diario

```python
# backend/app/services/automation_scheduler.py
# Configuracao Celery Beat para tarefas automaticas

CELERY_BEAT_SCHEDULE = {
    # === MANHA: Pesquisa e Planejamento ===

    "trend_scan_daily": {
        "task": "app.tasks.trend_scan",
        "schedule": crontab(hour=6, minute=0),  # 06:00
        "description": "Viral Tracker escaneia trends do dia",
    },
    "competitor_check": {
        "task": "app.tasks.competitor_check",
        "schedule": crontab(hour=7, minute=0),  # 07:00
        "description": "Social Analyst checa posts dos concorrentes (24h)",
    },
    "content_planning": {
        "task": "app.tasks.daily_content_plan",
        "schedule": crontab(hour=8, minute=0),  # 08:00
        "description": "Calendar Planner atualiza plano dos proximos 3 dias",
    },

    # === MEIO DIA: Sincronizacao ===

    "instagram_sync": {
        "task": "app.tasks.sync_instagram_metrics",
        "schedule": crontab(hour="*/4"),  # A cada 4 horas
        "description": "Sincronizar metricas Instagram",
    },
    "youtube_sync": {
        "task": "app.tasks.sync_youtube_metrics",
        "schedule": crontab(hour="*/6"),  # A cada 6 horas
        "description": "Sincronizar metricas YouTube",
    },

    # === TARDE: Analise ===

    "performance_daily_check": {
        "task": "app.tasks.daily_performance",
        "schedule": crontab(hour=18, minute=0),  # 18:00
        "description": "Analytics Agent puxa metricas do dia",
    },

    # === NOITE: Aprendizado ===

    "learning_update": {
        "task": "app.tasks.learning_loop",
        "schedule": crontab(hour=22, minute=0),  # 22:00
        "description": "Learning Engine atualiza scores e memoria",
    },

    # === SEMANAL ===

    "weekly_report": {
        "task": "app.tasks.weekly_report",
        "schedule": crontab(hour=10, minute=0, day_of_week=0),  # Domingo 10:00
        "description": "Report Generator cria relatorio semanal + envia email",
    },
    "newsletter_prep": {
        "task": "app.tasks.prepare_newsletter",
        "schedule": crontab(hour=14, minute=0, day_of_week=5),  # Sexta 14:00
        "description": "Email Agent prepara newsletter semanal",
    },
    "weekly_strategy_review": {
        "task": "app.tasks.strategy_review",
        "schedule": crontab(hour=9, minute=0, day_of_week=1),  # Segunda 09:00
        "description": "Strategy Advisor revisa estrategia da semana",
    },

    # === MENSAL ===

    "monthly_report": {
        "task": "app.tasks.monthly_report",
        "schedule": crontab(hour=10, minute=0, day_of_month=1),  # Dia 1, 10:00
        "description": "Report Generator cria relatorio mensal completo + PDF",
    },
    "competitor_deep_analysis": {
        "task": "app.tasks.monthly_competitor_analysis",
        "schedule": crontab(hour=8, minute=0, day_of_month=1),  # Dia 1, 08:00
        "description": "Social Analyst faz analise profunda dos concorrentes",
    },
}
```

### 16.2 Fluxo Visual do Pipeline Diario

```
06:00  TREND SCAN
  |--- Viral Tracker escaneia Google Trends, Instagram, TikTok, YouTube
  |--- Output: trend_report + top_hashtags
  v
07:00  COMPETITOR CHECK
  |--- Social Analyst analisa posts dos ultimos 24h dos concorrentes
  |--- Output: competitor_insights
  v
08:00  CONTENT PLANNING
  |--- Calendar Planner recebe trend_report + competitor_insights
  |--- Atualiza calendario dos proximos 3 dias
  |--- Output: content_briefs (rascunhos prontos para criacao)
  v
09:00-17:00  CRIACAO & APROVACAO (sob demanda do usuario)
  |--- Content Writer gera conteudos a partir dos briefs
  |--- Visual Designer sugere imagens/prompts
  |--- Usuario aprova via dashboard
  v
A cada 4h  SYNC METRICAS
  |--- Puxa metricas atualizadas do Instagram/YouTube
  |--- Atualiza analytics_snapshots
  v
18:00  PERFORMANCE CHECK
  |--- Analytics Agent analisa metricas do dia
  |--- Identifica top/bottom performers
  |--- Output: daily_performance_report
  v
22:00  LEARNING UPDATE
  |--- Learning Engine recalcula performance_scores
  |--- Atualiza embeddings de conteudos novos
  |--- Alimenta memoria de longo prazo (pgvector)
  |--- Output: updated_memory + optimization_suggestions
```

### 16.3 Fluxo Semanal

```
SEGUNDA 09:00  STRATEGY REVIEW
  |--- Strategy Advisor revisa performance da semana anterior
  |--- Ajusta pilares de conteudo e mix de formatos
  |--- Output: weekly_strategy_update

SEXTA 14:00  NEWSLETTER PREP
  |--- Email Agent agrega melhores conteudos da semana
  |--- Podcast Creator sugere clips do episodio (se houver)
  |--- Output: newsletter_draft (para aprovacao)

DOMINGO 10:00  WEEKLY REPORT
  |--- Report Generator compila metricas da semana
  |--- Gera PDF com graficos e insights
  |--- Email Agent envia para stakeholders
  |--- Output: weekly_report.pdf + email_sent
```

---

## 17. API ENDPOINTS (FastAPI)

```python
# backend/app/api/v1/chat.py
from fastapi import APIRouter, WebSocket, Depends
from app.agents.team import social_media_team
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1")


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    """Chat em tempo real com os agentes via WebSocket."""
    await websocket.accept()
    user = await get_current_user(websocket)

    try:
        while True:
            # Receber mensagem do usuario
            message = await websocket.receive_text()

            # Enviar para o time de agentes
            response = social_media_team.run(
                message=message,
                user_id=user.id,
                stream=True,
            )

            # Stream da resposta
            async for chunk in response:
                await websocket.send_json({
                    "type": "chunk",
                    "content": chunk.content,
                    "agent": chunk.agent_name,
                })

            await websocket.send_json({"type": "done"})

    except Exception:
        await websocket.close()


# backend/app/api/v1/content.py
@router.post("/content/generate")
async def generate_content(
    request: ContentGenerateRequest,
    user=Depends(get_current_user),
):
    """Gera conteudo para uma plataforma especifica."""
    prompt = (
        f"Crie um {request.content_type} para {request.platform} "
        f"sobre o tema: {request.topic}. "
        f"Tom: {request.tone or 'padrao da marca'}. "
        f"Inclua hashtags otimizadas."
    )

    result = social_media_team.run(
        message=prompt,
        user_id=str(user.id),
    )

    return {"content": result.content, "agent_used": result.agent_name}


# backend/app/api/v1/analysis.py
@router.get("/analysis/profile/{platform}/{profile_id}")
async def analyze_profile(
    platform: str,
    profile_id: str,
    user=Depends(get_current_user),
):
    """Analisa perfil de rede social."""
    prompt = f"Analise completa do perfil {platform} ID: {profile_id}"

    result = social_media_team.run(
        message=prompt,
        user_id=str(user.id),
    )

    return {"analysis": result.content}


# backend/app/api/v1/reports.py
@router.post("/reports/generate")
async def generate_report(
    request: ReportGenerateRequest,
    user=Depends(get_current_user),
):
    """Gera relatorio PDF do periodo."""
    prompt = (
        f"Gere relatorio {request.type} do periodo "
        f"{request.period_start} a {request.period_end}. "
        f"Inclua metricas, graficos e recomendacoes."
    )

    result = social_media_team.run(
        message=prompt,
        user_id=str(user.id),
    )

    return {
        "report": result.content,
        "pdf_url": result.metadata.get("pdf_url"),
    }
```

---

## REFERENCIAS

- [Top 10 AI Agents for Social Media 2026](https://noimosai.com/en/blog/top-10-ai-agents-for-social-media-to-explode-your-brand-growth-in-2026)
- [How AI Agents Transform Social Media Marketing](https://www.admove.ai/blog/ai-agents-for-social-media-marketing)
- [12 Best AI Agents for Social Media Management](https://www.ema.co/additional-blogs/addition-blogs/best-social-media-ai-agents)
- [CrewAI Instagram Example](https://github.com/alejandro-ao/crewai-instagram-example)
- [CrewAI Examples (Official)](https://github.com/crewAIInc/crewAI-examples)
- [500 AI Agents Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects)
- [How to Automate Instagram Strategy with CrewAI](https://alejandro-ao.com/how-to-automate-instagram-strategy-with-crewai/)
- [Predis.ai vs Ocoya](https://predis.ai/resources/predis-ai-vs-ocoya/)
- [Sprinklr AI Social Media Content Creation](https://www.sprinklr.com/blog/ai-social-media-content-creation/)
- [FeedHive](https://www.feedhive.com/)
- [Ocoya](https://www.ocoya.com/)
- [Lately.ai](https://www.lately.ai/)
- [Relevance AI Agent Templates](https://relevanceai.com/agent-templates-tasks/social-media-management-ai-agents)
- [Lyzr AI Agents for Social Media](https://www.lyzr.ai/blog/ai-agents-for-social-media/)
- [10 Best CrewAI Projects 2026](https://www.projectpro.io/article/crew-ai-projects-ideas-and-examples/1117)
