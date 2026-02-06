"""
Configuration settings for Deep Research AI.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class LLMConfig:
    """LLM provider configuration."""
    provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    
    # Fallback configuration
    fallback_provider: str = "anthropic"
    fallback_model: str = "claude-3-sonnet-20240229"
    fallback_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))


@dataclass
class SearchConfig:
    """Web search configuration."""
    provider: str = "tavily"
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("TAVILY_API_KEY"))
    max_results: int = 10
    timeout_seconds: int = 30
    
    # Fallback search
    fallback_provider: str = "serper"
    fallback_api_key: Optional[str] = field(default_factory=lambda: os.getenv("SERPER_API_KEY"))


@dataclass
class ResearchConfig:
    """Research operation configuration."""
    # Timeouts
    max_research_time_seconds: int = 120
    quick_research_time_seconds: int = 30
    
    # Sources
    max_sources: int = 15
    min_sources_for_verification: int = 2
    
    # Verification
    min_confidence_threshold: float = 0.5
    require_cross_reference: bool = True
    
    # Output
    default_output_format: str = "markdown"
    include_confidence_scores: bool = True
    include_sources: bool = True


@dataclass
class Config:
    """Main application configuration."""
    llm: LLMConfig = field(default_factory=LLMConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    research: ResearchConfig = field(default_factory=ResearchConfig)
    
    # Application settings
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))


# Global config instance
config = Config()
