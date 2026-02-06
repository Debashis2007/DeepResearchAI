"""
Web search with multiple backends for Deep Research AI.

Primary: DuckDuckGo (free, no API)
Fallback: Wikipedia API (always works)
"""

import asyncio
import urllib.parse
from dataclasses import dataclass
import httpx


@dataclass
class SearchResult:
    """Search result."""
    title: str
    url: str
    snippet: str
    domain: str


class MultiSearch:
    """
    Multi-backend web search.
    
    Tries DuckDuckGo first, falls back to Wikipedia.
    """
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
        self._ddgs = None
        self._ddgs_error = None
        
        # Try to import DDGS
        try:
            from duckduckgo_search import DDGS
            self._ddgs = DDGS()
        except Exception as e:
            self._ddgs_error = str(e)
    
    async def search(self, query: str, max_results: int = None) -> list[SearchResult]:
        """Search with fallback."""
        max_results = max_results or self.max_results
        results = []
        
        # Try DuckDuckGo first
        if self._ddgs:
            try:
                results = await self._search_ddg(query, max_results)
                if results:
                    return results
            except Exception as e:
                print(f"DuckDuckGo search failed: {e}")
        
        # Fallback to Wikipedia
        try:
            results = await self._search_wikipedia(query, max_results)
            if results:
                return results
        except Exception as e:
            print(f"Wikipedia search failed: {e}")
        
        return results
    
    async def _search_ddg(self, query: str, max_results: int) -> list[SearchResult]:
        """Search using DuckDuckGo."""
        loop = asyncio.get_event_loop()
        
        def do_search():
            try:
                return list(self._ddgs.text(query, max_results=max_results))
            except Exception as e:
                print(f"DDG text search error: {e}")
                return []
        
        raw_results = await loop.run_in_executor(None, do_search)
        
        results = []
        for r in raw_results:
            url = r.get("href", r.get("link", ""))
            domain = self._extract_domain(url)
            results.append(SearchResult(
                title=r.get("title", ""),
                url=url,
                snippet=r.get("body", r.get("snippet", "")),
                domain=domain
            ))
        
        return results
    
    async def _search_wikipedia(self, query: str, max_results: int) -> list[SearchResult]:
        """Search Wikipedia as fallback."""
        encoded = urllib.parse.quote(query)
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&format=json&srlimit={max_results}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        results = []
        for item in data.get("query", {}).get("search", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
            page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
            
            results.append(SearchResult(
                title=title,
                url=page_url,
                snippet=snippet,
                domain="wikipedia.org"
            ))
        
        return results
    
    async def search_news(self, query: str, max_results: int = None) -> list[SearchResult]:
        """Search news (uses DDG news if available, else Wikipedia)."""
        max_results = max_results or self.max_results
        
        if self._ddgs:
            try:
                loop = asyncio.get_event_loop()
                raw = await loop.run_in_executor(
                    None,
                    lambda: list(self._ddgs.news(query, max_results=max_results))
                )
                results = []
                for r in raw:
                    url = r.get("url", r.get("link", ""))
                    results.append(SearchResult(
                        title=r.get("title", ""),
                        url=url,
                        snippet=r.get("body", ""),
                        domain=self._extract_domain(url)
                    ))
                if results:
                    return results
            except Exception as e:
                print(f"DDG news search failed: {e}")
        
        # Fall back to regular Wikipedia search
        return await self._search_wikipedia(query, max_results)
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except:
            return "unknown"


# For backwards compatibility
DuckDuckGoSearch = MultiSearch
