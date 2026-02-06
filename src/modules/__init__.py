"""
Modules for Deep Research AI.
"""

from .query_understanding import query_understanding, QueryUnderstanding
from .web_search import web_search, WebSearch
from .reasoning_engine import reasoning_engine, ReasoningEngine
from .verification import verification, Verification
from .citation import citation_manager, CitationManager
from .output_generation import output_generator, OutputGenerator, SummaryLength, AudienceType
from .error_handling import (
    error_handler,
    ErrorHandler,
    ErrorSeverity,
    ComponentType,
    ErrorContext,
    ResearchError,
    QueryError,
    SearchError,
    ReasoningError,
    VerificationError,
    CitationError,
    LLMError,
    RateLimitError,
)

__all__ = [
    # Query Understanding
    "query_understanding",
    "QueryUnderstanding",
    
    # Web Search
    "web_search",
    "WebSearch",
    
    # Reasoning Engine
    "reasoning_engine",
    "ReasoningEngine",
    
    # Verification
    "verification",
    "Verification",
    
    # Citation
    "citation_manager",
    "CitationManager",
    
    # Output Generation
    "output_generator",
    "OutputGenerator",
    "SummaryLength",
    "AudienceType",
    
    # Error Handling
    "error_handler",
    "ErrorHandler",
    "ErrorSeverity",
    "ComponentType",
    "ErrorContext",
    "ResearchError",
    "QueryError",
    "SearchError",
    "ReasoningError",
    "VerificationError",
    "CitationError",
    "LLMError",
    "RateLimitError",
]
