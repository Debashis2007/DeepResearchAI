"""
Deep Research AI

A comprehensive AI-powered research system that combines web search,
reasoning, verification, and citation to deliver accurate, well-sourced
research results.

Usage:
    from src import research, ResearchOrchestrator, Config
    
    # Quick research
    result = await research("What is quantum computing?")
    
    # Advanced usage
    config = Config()
    orchestrator = ResearchOrchestrator(config)
    result = await orchestrator.research(
        query="Compare Python and Rust",
        audience=AudienceType.PROFESSIONAL,
        max_sources=15
    )
"""

from .config import Config, LLMConfig, SearchConfig, ResearchConfig
from .models import (
    Entity,
    SubQuery,
    QueryAnalysis,
    SearchResult,
    ContentExtraction,
    Source,
    ReasoningStep,
    VerificationResult,
    Citation,
    ResearchResult,
    OutputFormat,
    CitationStyle,
)
from .llm_client import LLMClient
from .orchestrator import ResearchOrchestrator, research, ResearchSession, ResearchProgress
from .main import run_research, create_config

# Module imports
from .modules.query_understanding import QueryUnderstanding
from .modules.web_search import WebSearch
from .modules.reasoning_engine import ReasoningEngine
from .modules.verification import Verification
from .modules.citation import CitationManager
from .modules.output_generation import OutputGenerator, SummaryLength, AudienceType
from .modules.error_handling import (
    ErrorHandler,
    ErrorSeverity,
    ComponentType,
    ResearchError,
    QueryError,
    SearchError,
    ReasoningError,
    VerificationError,
    CitationError,
    LLMError,
    RateLimitError,
)

__version__ = "1.0.0"
__author__ = "Deep Research AI Team"

__all__ = [
    # Main API
    "research",
    "run_research",
    "create_config",
    "ResearchOrchestrator",
    
    # Configuration
    "Config",
    "LLMConfig",
    "SearchConfig",
    "ResearchConfig",
    
    # Models
    "Entity",
    "SubQuery",
    "QueryAnalysis",
    "SearchResult",
    "ContentExtraction",
    "Source",
    "ReasoningStep",
    "VerificationResult",
    "Citation",
    "ResearchResult",
    "OutputFormat",
    "CitationStyle",
    
    # Clients
    "LLMClient",
    
    # Modules
    "QueryUnderstanding",
    "WebSearch",
    "ReasoningEngine",
    "Verification",
    "CitationManager",
    "OutputGenerator",
    "ErrorHandler",
    
    # Enums
    "SummaryLength",
    "AudienceType",
    "ErrorSeverity",
    "ComponentType",
    
    # Exceptions
    "ResearchError",
    "QueryError",
    "SearchError",
    "ReasoningError",
    "VerificationError",
    "CitationError",
    "LLMError",
    "RateLimitError",
    
    # Session management
    "ResearchSession",
    "ResearchProgress",
]
