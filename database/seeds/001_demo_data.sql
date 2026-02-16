-- AgenteSocial - Demo Seed Data
-- Insere dados de demonstracao para desenvolvimento e testes
-- IMPORTANTE: Execute apenas em ambiente de desenvolvimento
-- Requer um usuario autenticado no Supabase Auth

-- ============================================
-- Funcao auxiliar para inserir com user_id dinamico
-- ============================================
-- Uso: SELECT seed_demo_data('seu-user-uuid-aqui');

CREATE OR REPLACE FUNCTION seed_demo_data(demo_user_id UUID)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN

-- ============================================
-- Perfis sociais
-- ============================================
INSERT INTO social_midia_profiles (user_id, platform, handle, followers_count, is_active, metadata)
VALUES
  (demo_user_id, 'instagram', '@agentesocial_demo', 15420, true, '{"bio": "IA para Redes Sociais"}'),
  (demo_user_id, 'youtube', 'AgenteSocial Channel', 3200, true, '{"subscribers": 3200}'),
  (demo_user_id, 'linkedin', 'agentesocial', 1850, true, '{}'),
  (demo_user_id, 'tiktok', '@agentesocial', 8700, false, '{}')
ON CONFLICT DO NOTHING;

-- ============================================
-- Brand Voice
-- ============================================
INSERT INTO social_midia_brand_voice_profiles (user_id, name, tone, vocabulary, avoid_words, examples, personality, target_audience, is_active)
VALUES (
  demo_user_id,
  'Tom Padrao AgenteSocial',
  'Profissional mas acessivel, usa analogias do dia a dia para explicar conceitos de IA e marketing digital',
  ARRAY['inteligencia artificial', 'automacao', 'engajamento', 'estrategia', 'resultados', 'crescimento'],
  ARRAY['basicamente', 'literalmente', 'tipo assim', 'na real'],
  ARRAY['Automatize sua presenca digital com IA e foque no que importa: criar conexoes reais.', 'Dados nao mentem: seu proximo post viral pode ser planejado com inteligencia.'],
  'Inovador, confiavel e pratico. Transforma complexidade em simplicidade.',
  'Empreendedores digitais, social media managers e criadores de conteudo no Brasil',
  true
)
ON CONFLICT DO NOTHING;

-- ============================================
-- Conteudos de exemplo
-- ============================================
INSERT INTO social_midia_content_pieces (user_id, content_type, platform, title, body, caption, hashtags, visual_suggestion, tone, status, engagement_score, posted_day)
VALUES
  (demo_user_id, 'post', 'instagram', 'IA no Marketing Digital',
   'A inteligencia artificial esta revolucionando a forma como criamos conteudo para redes sociais. Nao se trata de substituir a criatividade humana, mas de potencializa-la.',
   'A IA veio para ficar e quem nao se adaptar vai ficar para tras. Voce ja usa IA no seu dia a dia?',
   ARRAY['#MarketingDigital', '#InteligenciaArtificial', '#IA', '#RedesSociais', '#Inovacao'],
   'Imagem com fundo gradiente azul/roxo, icone de cerebro + engrenagem, texto em branco',
   'educativo', 'published', 85.5, 'tuesday'),

  (demo_user_id, 'carrossel', 'instagram', '5 Dicas para Engajamento',
   'Slide 1: 5 formas de aumentar seu engajamento HOJE\nSlide 2: 1. Perguntas nos Stories\nSlide 3: 2. Conteudo salvavel (dicas e tutoriais)\nSlide 4: 3. Reels com trending audio\nSlide 5: 4. Responda TODOS os comentarios\nSlide 6: 5. Poste nos horarios certos\nSlide 7: Salve para lembrar!',
   'Qual dessas dicas voce ja aplica? Comenta aqui!',
   ARRAY['#Engajamento', '#DicasInstagram', '#SocialMedia', '#MarketingDigital'],
   'Carrossel com design clean, cores vibrantes, numeracao grande',
   'casual', 'published', 92.3, 'thursday'),

  (demo_user_id, 'reel', 'instagram', 'Como a IA cria posts',
   'Hook (0-2s): Voce sabia que a IA pode criar seu proximo post viral?\nCorpo (2-25s): Veja como funciona em 3 passos simples...\n1. Defina seu tom de voz\n2. Escolha o tipo de conteudo\n3. Deixe a IA trabalhar\nCTA (25-30s): Teste gratis no link da bio!',
   'IA criando conteudo em tempo real',
   ARRAY['#Reels', '#IA', '#MarketingDigital', '#Automacao'],
   'Video screen recording mostrando a ferramenta, transicoes rapidas, texto overlay',
   'casual', 'draft', 0, NULL),

  (demo_user_id, 'post', 'linkedin', 'O Futuro do Social Media Manager',
   'O papel do Social Media Manager esta evoluindo rapidamente. Com ferramentas de IA cada vez mais sofisticadas, o profissional que se destaca nao e aquele que posta mais, mas aquele que pensa estrategicamente.\n\nA IA cuida do operacional. Voce cuida da estrategia.\n\nIsso nao e ameaca. E oportunidade.',
   NULL,
   ARRAY['#SocialMedia', '#FuturoDoTrabalho', '#IA', '#LinkedIn'],
   NULL,
   'formal', 'scheduled', 0, 'wednesday')
ON CONFLICT DO NOTHING;

-- ============================================
-- Eventos do calendario
-- ============================================
INSERT INTO social_midia_content_calendar (user_id, title, platform, scheduled_at, status, notes)
VALUES
  (demo_user_id, 'Post IA no Marketing', 'instagram', NOW() + INTERVAL '1 day', 'scheduled', 'Post educativo sobre IA'),
  (demo_user_id, 'Carrossel Engajamento', 'instagram', NOW() + INTERVAL '3 days', 'scheduled', 'Carrossel com 5 dicas'),
  (demo_user_id, 'Video YouTube', 'youtube', NOW() + INTERVAL '5 days', 'scheduled', 'Tutorial completo'),
  (demo_user_id, 'Post LinkedIn', 'linkedin', NOW() + INTERVAL '2 days', 'scheduled', 'Artigo sobre futuro do SMM')
ON CONFLICT DO NOTHING;

-- ============================================
-- Hashtag Research
-- ============================================
INSERT INTO social_midia_hashtag_research (user_id, hashtag, platform, volume, competition, related_hashtags, trend_direction, niche)
VALUES
  (demo_user_id, '#MarketingDigital', 'instagram', 45000000, 'high', ARRAY['#Marketing', '#Digital', '#SocialMedia'], 'stable', 'marketing'),
  (demo_user_id, '#InteligenciaArtificial', 'instagram', 12000000, 'medium', ARRAY['#IA', '#AI', '#MachineLearning'], 'up', 'tecnologia'),
  (demo_user_id, '#Empreendedorismo', 'instagram', 35000000, 'high', ARRAY['#Negocios', '#Startup', '#Sucesso'], 'stable', 'negocios')
ON CONFLICT DO NOTHING;

-- ============================================
-- Viral Content (publico)
-- ============================================
INSERT INTO social_midia_viral_content (platform, author_handle, content_text, virality_score, classification, niche, hashtags, metadata)
VALUES
  ('instagram', '@marketingbr', 'Thread sobre como crescer no Instagram em 2026', 87.5, 'viral', 'marketing',
   ARRAY['#Instagram', '#Crescimento', '#Marketing'], '{"likes": 45000, "shares": 12000}'),
  ('tiktok', '@techbrasil', 'ChatGPT escrevendo um post inteiro em 10 segundos', 95.2, 'super_viral', 'tecnologia',
   ARRAY['#ChatGPT', '#IA', '#Tech'], '{"views": 2500000, "likes": 350000}'),
  ('youtube', '@socialmedia_tips', '10 ferramentas de IA para Social Media em 2026', 72.1, 'viral', 'marketing',
   ARRAY['#IA', '#SocialMedia', '#Ferramentas'], '{"views": 180000, "likes": 8500}')
ON CONFLICT DO NOTHING;

-- ============================================
-- Analytics Snapshot de exemplo
-- ============================================
INSERT INTO social_midia_analytics_snapshots (profile_id, snapshot_date, followers, following, posts_count, engagement_rate, avg_likes, avg_comments, best_posting_times)
SELECT
  sp.id,
  CURRENT_DATE - INTERVAL '1 day',
  15420, 890, 245, 4.7, 680, 42,
  '{"monday": ["09:00", "18:00"], "wednesday": ["12:00", "19:00"], "friday": ["10:00", "17:00"]}'::jsonb
FROM social_midia_profiles sp
WHERE sp.user_id = demo_user_id AND sp.platform = 'instagram'
LIMIT 1
ON CONFLICT DO NOTHING;

RAISE NOTICE 'Demo data inserted for user %', demo_user_id;

END;
$$;

-- ============================================
-- INSTRUCOES DE USO:
-- ============================================
-- 1. Crie um usuario no Supabase Auth
-- 2. Copie o UUID do usuario
-- 3. Execute: SELECT seed_demo_data('seu-uuid-aqui');
-- 4. Verifique: SELECT * FROM social_midia_profiles;
