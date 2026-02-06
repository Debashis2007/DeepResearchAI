"""
Deep Research AI - Main Entry Point

A comprehensive AI-powered research system that combines web search,
reasoning, verification, and citation to deliver accurate, well-sourced
research results.
"""

import asyncio
import argparse
import json
import sys
from typing import Any

from .config import Config, LLMConfig, SearchConfig, ResearchConfig
from .orchestrator import ResearchOrchestrator, research
from .models import OutputFormat, CitationStyle
from .modules.output_generation import AudienceType


def create_config(
    llm_provider: str = "openai",
    llm_model: str | None = None,
    search_provider: str = "brave",
    openai_api_key: str | None = None,
    anthropic_api_key: str | None = None,
    search_api_key: str | None = None
) -> Config:
    """
    Create a configuration object.
    
    Args:
        llm_provider: LLM provider ("openai" or "anthropic")
        llm_model: Model name (uses default for provider if not specified)
        search_provider: Search provider ("brave", "serper", or "tavily")
        openai_api_key: OpenAI API key
        anthropic_api_key: Anthropic API key
        search_api_key: Search API key
        
    Returns:
        Configured Config object
    """
    # Determine model based on provider
    if llm_model is None:
        llm_model = "gpt-4o" if llm_provider == "openai" else "claude-sonnet-4-20250514"
    
    llm_config = LLMConfig(
        provider=llm_provider,
        model=llm_model,
        openai_api_key=openai_api_key or "",
        anthropic_api_key=anthropic_api_key or ""
    )
    
    search_config = SearchConfig(
        provider=search_provider,
        api_key=search_api_key or ""
    )
    
    return Config(
        llm_config=llm_config,
        search_config=search_config
    )


async def run_research(
    query: str,
    config: Config | None = None,
    audience: str = "general",
    citation_style: str = "apa",
    output_format: str = "markdown",
    max_sources: int = 10,
    verify: bool = True
) -> dict[str, Any]:
    """
    Run a research query and return results.
    
    Args:
        query: The research query
        config: Configuration (uses defaults if not provided)
        audience: Target audience (general, professional, academic, technical)
        citation_style: Citation style (apa, mla, chicago, ieee, harvard)
        output_format: Output format (text, markdown, html, json)
        max_sources: Maximum number of sources to use
        verify: Whether to verify claims
        
    Returns:
        Dictionary containing research results
    """
    config = config or Config()
    orchestrator = ResearchOrchestrator(config)
    
    # Convert string parameters to enums
    audience_type = AudienceType(audience.lower())
    cit_style = CitationStyle(citation_style.upper())
    out_format = OutputFormat(output_format.lower())
    
    # Run research
    result = await orchestrator.research(
        query=query,
        audience=audience_type,
        citation_style=cit_style,
        output_format=out_format,
        max_sources=max_sources,
        verify_claims=verify
    )
    
    # Convert to dictionary
    return {
        "query": result.query,
        "answer": result.answer,
        "confidence": result.confidence,
        "sources": [
            {
                "title": s.title,
                "url": s.url,
                "credibility_score": s.credibility_score
            }
            for s in result.sources
        ],
        "verification_status": result.verification_status,
        "metadata": result.metadata
    }


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Deep Research AI - Comprehensive AI-powered research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "What is quantum computing?"
  %(prog)s "Compare Python and Rust" --audience professional
  %(prog)s "Latest AI developments" --max-sources 15 --no-verify
        """
    )
    
    parser.add_argument(
        "query",
        help="The research query to investigate"
    )
    
    parser.add_argument(
        "--llm-provider",
        choices=["openai", "anthropic"],
        default="openai",
        help="LLM provider to use (default: openai)"
    )
    
    parser.add_argument(
        "--llm-model",
        help="Specific model to use (default: provider's best model)"
    )
    
    parser.add_argument(
        "--search-provider",
        choices=["brave", "serper", "tavily"],
        default="brave",
        help="Search provider to use (default: brave)"
    )
    
    parser.add_argument(
        "--audience",
        choices=["general", "professional", "academic", "technical"],
        default="general",
        help="Target audience (default: general)"
    )
    
    parser.add_argument(
        "--citation-style",
        choices=["apa", "mla", "chicago", "ieee", "harvard"],
        default="apa",
        help="Citation style (default: apa)"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["text", "markdown", "html", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    
    parser.add_argument(
        "--max-sources",
        type=int,
        default=10,
        help="Maximum number of sources to use (default: 10)"
    )
    
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip claim verification"
    )
    
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON"
    )
    
    parser.add_argument(
        "--openai-api-key",
        help="OpenAI API key (or set OPENAI_API_KEY env var)"
    )
    
    parser.add_argument(
        "--anthropic-api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )
    
    parser.add_argument(
        "--search-api-key",
        help="Search API key (or set SEARCH_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Create configuration
    config = create_config(
        llm_provider=args.llm_provider,
        llm_model=args.llm_model,
        search_provider=args.search_provider,
        openai_api_key=args.openai_api_key,
        anthropic_api_key=args.anthropic_api_key,
        search_api_key=args.search_api_key
    )
    
    # Run research
    print(f"🔍 Researching: {args.query}\n")
    
    try:
        result = asyncio.run(run_research(
            query=args.query,
            config=config,
            audience=args.audience,
            citation_style=args.citation_style,
            output_format=args.output_format,
            max_sources=args.max_sources,
            verify=not args.no_verify
        ))
        
        if args.json_output:
            print(json.dumps(result, indent=2))
        else:
            print_result(result)
            
    except Exception as e:
        print(f"❌ Research failed: {e}", file=sys.stderr)
        sys.exit(1)


def print_result(result: dict) -> None:
    """Print research result in a readable format."""
    print("=" * 60)
    print("📚 RESEARCH RESULTS")
    print("=" * 60)
    print()
    
    print(f"📋 Query: {result['query']}")
    print(f"🎯 Confidence: {result['confidence']:.1%}")
    print(f"✅ Verification: {result['verification_status']}")
    print()
    
    print("📝 Answer:")
    print("-" * 40)
    print(result['answer'])
    print()
    
    print(f"📚 Sources ({len(result['sources'])}):")
    print("-" * 40)
    for i, source in enumerate(result['sources'], 1):
        print(f"{i}. {source['title']}")
        print(f"   URL: {source['url']}")
        print(f"   Credibility: {source['credibility_score']:.1%}")
    print()
    
    print("=" * 60)


if __name__ == "__main__":
    main()
