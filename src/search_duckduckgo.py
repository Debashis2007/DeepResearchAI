"""
Free web search using DuckDuckGo for Deep Research AI.

No API key required - perfect for Hugging Face deployment.
"""

import asyncio
from dataclasses import dataclass
from typing import Any

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


@dataclass
class SearchResult:
    """Search result from DuckDuckGo."""
    title: str
    url: str
    snippet: str
    domain: str


class DuckDuckGoSearch:
    """
    Free web search using DuckDuckGo.
    
    No API key required.
    """
    
    def __init__(self, max_results: int = 10) -> None:
        """
        Initialize DuckDuckGo search.
        
        Args:
            max_results: Maximum results per search
        """
        if not DDGS_AVAILABLE:
            raise ImportError(
                "duckduckgo-search not installed. "
                "Install with: pip install duckduckgo-search"
            )
        
        self.max_results = max_results
        self.ddgs = DDGS()
    
    async def search(
        self,
        query: str,
        max_results: int | None = None
    ) -> list[SearchResult]:
        """
        Search the web using DuckDuckGo.
        
        Args:
            query: Search query
            max_results: Override default max results
            
        Returns:
            List of SearchResult objects
        """
        max_results = max_results or self.max_results
        
        # Run sync search in executor
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: list(self.ddgs.text(query, max_results=max_results))
        )
        
        search_results = []
        for r in results:
            # Extract domain from URL
            url = r.get("href", r.get("link", ""))
            domain = self._extract_domain(url)
            
            search_results.append(SearchResult(
                title=r.get("title", ""),
                url=url,
                snippet=r.get("body", r.get("snippet", "")),
                domain=domain
            ))
        
        return search_results
    
    async def search_news(
        self,
        query: str,
        max_results: int | None = None
    ) -> list[SearchResult]:
        """
        Search news using DuckDuckGo.
        
        Args:
            query: Search query
            max_results: Override default max results
            
        Returns:
            List of SearchResult objects
        """
        max_results = max_results or self.max_results
        
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: list(self.ddgs.news(query, max_results=max_results))
        )
        
        search_results = []
        for r in results:
            url = r.get("url", r.get("link", ""))
            domain = self._extract_domain(url)
            
            search_results.append(SearchResult(
                title=r.get("title", ""),
                url=url,
                snippet=r.get("body", r.get("excerpt", "")),
                domain=domain
            ))
        
        return search_results
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc.replace("www.", "")
        except Exception:
            return ""


async def search_web(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """
    Convenience function for web search.
    
    Args:
        query: Search query
        max_results: Maximum results
        
    Returns:
        List of result dictionaries
    """
    searcher = DuckDuckGoSearch(max_results=max_results)
    results = await searcher.search(query)
    
    return [
        {
            "title": r.title,
            "url": r.url,
            "snippet": r.snippet,
            "domain": r.domain
        }
        for r in results
    ]
