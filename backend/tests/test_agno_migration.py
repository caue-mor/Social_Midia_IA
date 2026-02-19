"""Testes da migracao AGNO 1.4.5 -> 2.5.2.

Valida:
- Criacao de team sem DATABASE_URL (degradacao graciosa)
- Sub-teams com membros corretos
- Memory config retorna None sem DB
- Flags store_history_messages ativas nos agentes
- Tools customizadas continuam funcionando
"""

import pytest
from unittest.mock import patch


class TestMemoryConfigGracefulDegradation:
    """Testa que memory_config degrada graciosamente sem DATABASE_URL."""

    def test_create_db_returns_none_without_db(self):
        from app.agents.memory_config import create_db
        result = create_db()
        assert result is None

    def test_create_db_with_custom_tables_returns_none_without_db(self):
        from app.agents.memory_config import create_db
        result = create_db(
            session_table="custom_sessions",
            memory_table="custom_memories",
        )
        assert result is None

    def test_create_memory_manager_returns_none_without_db(self):
        from app.agents.memory_config import create_memory_manager
        result = create_memory_manager()
        assert result is None


class TestTeamCreationWithoutDatabase:
    """Testa que o team principal cria sem Postgres."""

    def test_team_creation_without_database(self):
        from app.agents.team import create_team
        team = create_team()
        assert team is not None
        assert team.name == "AgenteSocial Team"
        assert len(team.members) == 4

    def test_team_has_instructions(self):
        from app.agents.team import create_team
        team = create_team()
        # AGNO 2.5.2 usa instructions para roteamento (sem param mode)
        assert team.instructions is not None
        assert len(team.instructions) > 0


class TestSubTeamContentFactory:
    """Testa o sub-team Content Factory."""

    def test_content_factory_creation(self):
        from app.agents.teams.content_factory import create_content_factory
        team = create_content_factory()
        assert team is not None
        assert team.name == "Content Factory"
        assert len(team.members) == 3

    def test_content_factory_member_names(self):
        from app.agents.teams.content_factory import create_content_factory
        team = create_content_factory()
        names = {m.name for m in team.members}
        assert "Content Writer" in names
        assert "Visual Designer" in names
        assert "Hashtag Hunter" in names


class TestSubTeamAnalysisSquad:
    """Testa o sub-team Analysis Squad."""

    def test_analysis_squad_creation(self):
        from app.agents.teams.analysis_squad import create_analysis_squad
        team = create_analysis_squad()
        assert team is not None
        assert team.name == "Analysis Squad"
        assert len(team.members) == 3

    def test_analysis_squad_member_names(self):
        from app.agents.teams.analysis_squad import create_analysis_squad
        team = create_analysis_squad()
        names = {m.name for m in team.members}
        assert "Social Media Analyst" in names
        assert "Viral Content Tracker" in names
        assert "Strategy Advisor" in names


class TestSubTeamMediaProduction:
    """Testa o sub-team Media Production."""

    def test_media_production_creation(self):
        from app.agents.teams.media_production import create_media_production
        team = create_media_production()
        assert team is not None
        assert team.name == "Media Production"
        assert len(team.members) == 2

    def test_media_production_member_names(self):
        from app.agents.teams.media_production import create_media_production
        team = create_media_production()
        names = {m.name for m in team.members}
        assert "Podcast Creator" in names
        assert "Video Script Writer" in names


class TestSubTeamOperations:
    """Testa o sub-team Operations."""

    def test_operations_creation(self):
        from app.agents.teams.operations import create_operations_team
        team = create_operations_team()
        assert team is not None
        assert team.name == "Operations"
        assert len(team.members) == 3

    def test_operations_member_names(self):
        from app.agents.teams.operations import create_operations_team
        team = create_operations_team()
        names = {m.name for m in team.members}
        assert "Calendar Planner" in names
        assert "Report Generator" in names
        assert "Memory Agent" in names


class TestAgentHistoryFlags:
    """Testa que todos os agentes tem store_history_messages e add_history_to_context ativos."""

    @pytest.mark.parametrize("creator_module,creator_name", [
        ("app.agents.master_orchestrator", "create_master_agent"),
        ("app.agents.social_analyst", "create_social_analyst"),
        ("app.agents.content_writer", "create_content_writer"),
        ("app.agents.viral_tracker", "create_viral_tracker"),
        ("app.agents.hashtag_hunter", "create_hashtag_hunter"),
        ("app.agents.podcast_creator", "create_podcast_creator"),
        ("app.agents.video_script_writer", "create_video_script_writer"),
        ("app.agents.calendar_planner", "create_calendar_planner"),
        ("app.agents.report_generator", "create_report_generator"),
        ("app.agents.strategy_advisor", "create_strategy_advisor"),
        ("app.agents.visual_designer", "create_visual_designer"),
        ("app.agents.memory_agent", "create_memory_agent"),
    ])
    def test_agent_has_store_history_messages(self, creator_module, creator_name):
        import importlib
        module = importlib.import_module(creator_module)
        creator = getattr(module, creator_name)
        agent = creator()
        assert agent.store_history_messages is True
        assert agent.add_history_to_context is True
        assert agent.num_history_runs == 5


class TestCustomToolsCompatibility:
    """Testa que tools customizadas (@tool) continuam funcionando."""

    def test_instagram_tools_importable(self):
        from app.tools.instagram_tools import get_instagram_tools
        tools = get_instagram_tools()
        assert len(tools) > 0

    def test_youtube_tools_importable(self):
        from app.tools.youtube_tools import get_youtube_tools
        tools = get_youtube_tools()
        assert len(tools) > 0

    def test_trends_tools_importable(self):
        from app.tools.trends_tools import get_trends_tools
        tools = get_trends_tools()
        assert len(tools) > 0

    def test_memory_tools_importable(self):
        from app.tools.memory_tools import get_memory_tools
        tools = get_memory_tools()
        assert len(tools) > 0

    def test_supabase_tools_importable(self):
        from app.tools.supabase_tools import get_supabase_tools
        tools = get_supabase_tools()
        assert len(tools) > 0

    def test_audio_tools_importable(self):
        from app.tools.audio_tools import get_audio_tools
        tools = get_audio_tools()
        assert len(tools) > 0

    def test_image_tools_importable(self):
        from app.tools.image_tools import get_image_tools
        tools = get_image_tools()
        assert len(tools) > 0

    def test_books_tools_importable(self):
        from app.tools.books_tools import get_books_tools
        tools = get_books_tools()
        assert len(tools) > 0

    def test_publishing_tools_importable(self):
        from app.tools.publishing_tools import get_publishing_tools
        tools = get_publishing_tools()
        assert len(tools) > 0
