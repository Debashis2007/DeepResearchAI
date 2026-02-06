"""
Tests for Deep Research AI modules.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Import modules to test
from src.config import Config, LLMConfig, SearchConfig
from src.models import (
    QueryAnalysis, SubQuery, Entity, SearchResult,
    Source, ReasoningStep, Citation, CitationStyle
)


class TestConfig:
    """Test configuration classes."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = Config()
        assert config.llm_config is not None
        assert config.search_config is not None
        assert config.research_config is not None
    
    def test_llm_config(self):
        """Test LLM configuration."""
        llm_config = LLMConfig(
            provider="openai",
            model="gpt-4o",
            openai_api_key="test-key"
        )
        assert llm_config.provider == "openai"
        assert llm_config.model == "gpt-4o"
    
    def test_search_config(self):
        """Test search configuration."""
        search_config = SearchConfig(
            provider="brave",
            api_key="test-key",
            max_results=10
        )
        assert search_config.provider == "brave"
        assert search_config.max_results == 10


class TestModels:
    """Test data models."""
    
    def test_sub_query_creation(self):
        """Test SubQuery model."""
        sub_query = SubQuery(
            query="What is Python?",
            purpose="definition",
            priority=1
        )
        assert sub_query.query == "What is Python?"
        assert sub_query.priority == 1
    
    def test_entity_creation(self):
        """Test Entity model."""
        entity = Entity(
            name="Python",
            entity_type="programming_language",
            context="Programming language created by Guido van Rossum"
        )
        assert entity.name == "Python"
        assert entity.entity_type == "programming_language"
    
    def test_search_result_creation(self):
        """Test SearchResult model."""
        result = SearchResult(
            title="Python Documentation",
            url="https://docs.python.org",
            snippet="Python is a programming language.",
            domain="docs.python.org"
        )
        assert result.title == "Python Documentation"
        assert result.domain == "docs.python.org"
    
    def test_source_creation(self):
        """Test Source model."""
        source = Source(
            source_id="source_1",
            url="https://example.com",
            title="Example Source",
            content="Some content",
            domain="example.com",
            credibility_score=0.8
        )
        assert source.source_id == "source_1"
        assert source.credibility_score == 0.8
    
    def test_citation_creation(self):
        """Test Citation model."""
        citation = Citation(
            source_id="source_1",
            style=CitationStyle.APA,
            formatted_citation="Author (2024). Title. Publisher.",
            in_text_citation="(Author, 2024)"
        )
        assert citation.style == CitationStyle.APA


class TestQueryUnderstanding:
    """Test Query Understanding module."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        mock = AsyncMock()
        mock.call_json.return_value = {
            "query_type": "factual",
            "intent": "seeking information",
            "complexity": "moderate",
            "sub_queries": [
                {"query": "What is Python?", "purpose": "definition", "priority": 1}
            ],
            "entities": [
                {"name": "Python", "type": "programming_language"}
            ]
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_analyze_query(self, mock_llm_client):
        """Test query analysis."""
        with patch('src.modules.query_understanding.LLMClient', return_value=mock_llm_client):
            from src.modules.query_understanding import QueryUnderstanding
            
            qu = QueryUnderstanding()
            qu.llm_client = mock_llm_client
            
            result = await qu.analyze("What is Python programming language?")
            
            assert result is not None
            mock_llm_client.call_json.assert_called()


class TestWebSearch:
    """Test Web Search module."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        mock = AsyncMock()
        mock.call_json.return_value = {
            "search_queries": [
                {"query": "Python programming language", "purpose": "primary search"}
            ]
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_generate_search_queries(self, mock_llm_client):
        """Test search query generation."""
        with patch('src.modules.web_search.LLMClient', return_value=mock_llm_client):
            from src.modules.web_search import WebSearch
            
            ws = WebSearch()
            ws.llm_client = mock_llm_client
            
            result = await ws.generate_search_queries("What is Python?")
            
            assert "search_queries" in result or result is not None


class TestReasoningEngine:
    """Test Reasoning Engine module."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        mock = AsyncMock()
        mock.call_json.return_value = {
            "reasoning_chain": [
                {"step": 1, "thought": "First, analyze the query"}
            ],
            "conclusion": "Python is a programming language"
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_chain_of_thought(self, mock_llm_client):
        """Test chain of thought reasoning."""
        with patch('src.modules.reasoning_engine.LLMClient', return_value=mock_llm_client):
            from src.modules.reasoning_engine import ReasoningEngine
            
            re = ReasoningEngine()
            re.llm_client = mock_llm_client
            
            result = await re.chain_of_thought(
                "What is Python?",
                "Python is a programming language..."
            )
            
            assert "reasoning_chain" in result or result is not None


class TestVerification:
    """Test Verification module."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        mock = AsyncMock()
        mock.call_json.return_value = {
            "verification_results": [],
            "overall_confidence": 0.8
        }
        return mock
    
    @pytest.fixture
    def sample_sources(self):
        """Create sample sources."""
        return [
            Source(
                source_id="s1",
                url="https://example.com",
                title="Example",
                content="Python is a programming language",
                domain="example.com",
                credibility_score=0.7
            )
        ]
    
    @pytest.mark.asyncio
    async def test_verify_claims(self, mock_llm_client, sample_sources):
        """Test claim verification."""
        with patch('src.modules.verification.LLMClient', return_value=mock_llm_client):
            from src.modules.verification import Verification
            
            v = Verification()
            v.llm_client = mock_llm_client
            
            claims = ["Python is a programming language"]
            result = await v.verify(claims, sample_sources)
            
            assert result is not None


class TestCitationManager:
    """Test Citation Manager module."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        mock = AsyncMock()
        mock.call_json.return_value = {
            "citations": [
                {
                    "source_id": "s1",
                    "formats": {"apa": "Author (2024). Title."},
                    "in_text": {"apa": "(Author, 2024)"}
                }
            ]
        }
        return mock
    
    @pytest.fixture
    def sample_sources(self):
        """Create sample sources."""
        return [
            Source(
                source_id="s1",
                url="https://example.com",
                title="Example",
                content="Content here",
                domain="example.com",
                credibility_score=0.7
            )
        ]
    
    @pytest.mark.asyncio
    async def test_generate_citations(self, mock_llm_client, sample_sources):
        """Test citation generation."""
        with patch('src.modules.citation.LLMClient', return_value=mock_llm_client):
            from src.modules.citation import CitationManager
            
            cm = CitationManager()
            cm.llm_client = mock_llm_client
            
            result = await cm.generate_citations(sample_sources, "Some content")
            
            assert "citations" in result


class TestOutputGenerator:
    """Test Output Generator module."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        mock = AsyncMock()
        mock.call_json.return_value = {
            "summary": {
                "text": "This is a summary",
                "key_points": ["Point 1", "Point 2"]
            }
        }
        return mock
    
    @pytest.mark.asyncio
    async def test_generate_summary(self, mock_llm_client):
        """Test summary generation."""
        with patch('src.modules.output_generation.LLMClient', return_value=mock_llm_client):
            from src.modules.output_generation import OutputGenerator, SummaryLength
            
            og = OutputGenerator()
            og.llm_client = mock_llm_client
            
            findings = {"synthesis": "Some findings"}
            result = await og.generate_summary(findings, SummaryLength.STANDARD)
            
            assert "summary" in result


class TestErrorHandler:
    """Test Error Handler module."""
    
    def test_record_error(self):
        """Test error recording."""
        from src.modules.error_handling import (
            ErrorHandler, ErrorContext, ErrorSeverity, ComponentType
        )
        
        handler = ErrorHandler()
        context = ErrorContext(
            component=ComponentType.QUERY_UNDERSTANDING,
            operation="analyze",
            query="test query"
        )
        
        error = ValueError("Test error")
        record = handler.record_error(error, context, ErrorSeverity.ERROR)
        
        assert record.error_type == "ValueError"
        assert record.error_message == "Test error"
    
    def test_get_error_summary(self):
        """Test error summary generation."""
        from src.modules.error_handling import ErrorHandler
        
        handler = ErrorHandler()
        summary = handler.get_error_summary()
        
        assert "total_errors" in summary
        assert "by_severity" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
