"""
Web Search Module - Handles web search integration and content retrieval.
"""

import logging
import json
import httpx
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from urllib.parse import urlparse

from ..models import Source, QueryAnalysis, ExtractedInfo
from ..config import config
from ..llm_client import llm_client
from ..prompts.search_prompts import SEARCH_PROMPTS

logger = logging.getLogger(__name__)


class BaseSearchProvider(ABC):
    """Base class for search providers."""
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Execute a search query."""
        pass


class TavilySearchProvider(BaseSearchProvider):
    """Tavily search API provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.search.api_key
        self.base_url = "https://api.tavily.com"
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Execute a search using Tavily API."""
        if not self.api_key:
            logger.warning("Tavily API key not configured")
            return []
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "max_results": max_results,
                        "include_answer": True,
                        "include_raw_content": True,
                    },
                    timeout=config.search.timeout_seconds
                )
                response.raise_for_status()
                data = response.json()
                
                results = []
                for result in data.get("results", []):
                    results.append({
                        "url": result.get("url", ""),
                        "title": result.get("title", ""),
                        "snippet": result.get("content", ""),
                        "content": result.get("raw_content", result.get("content", "")),
                        "score": result.get("score", 0.5),
                    })
                
                return results
            except Exception as e:
                logger.error(f"Tavily search failed: {e}")
                return []


class SerperSearchProvider(BaseSearchProvider):
    """Serper (Google Search) API provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.search.fallback_api_key
        self.base_url = "https://google.serper.dev"
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Execute a search using Serper API."""
        if not self.api_key:
            logger.warning("Serper API key not configured")
            return []
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/search",
                    headers={"X-API-KEY": self.api_key},
                    json={"q": query, "num": max_results},
                    timeout=config.search.timeout_seconds
                )
                response.raise_for_status()
                data = response.json()
                
                results = []
                for result in data.get("organic", []):
                    results.append({
                        "url": result.get("link", ""),
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "content": result.get("snippet", ""),  # Serper doesn't provide full content
                        "score": 0.5,
                    })
                
                return results
            except Exception as e:
                logger.error(f"Serper search failed: {e}")
                return []


class WebSearch:
    """
    Web Search module for searching and retrieving content from the web.
    
    Implements FR-2: Web Search Integration requirements.
    """
    
    def __init__(self):
        self.llm = llm_client
        self.primary_provider = TavilySearchProvider()
        self.fallback_provider = SerperSearchProvider()
        self._use_fallback = False
    
    async def search(
        self, 
        query: str,
        query_analysis: Optional[QueryAnalysis] = None,
        max_results: int = 10
    ) -> List[Source]:
        """
        Search the web for information related to the query.
        
        Args:
            query: Search query string
            query_analysis: Optional query analysis for context
            max_results: Maximum number of results to return
            
        Returns:
            List of Source objects with retrieved content
        """
        logger.info(f"Searching for: {query[:100]}...")
        
        # Generate optimized search queries
        search_queries = await self._generate_search_queries(
            query, query_analysis
        )
        
        # Execute searches
        all_results = []
        for search_query in search_queries[:3]:  # Limit to top 3 queries
            results = await self._execute_search(
                search_query["query"],
                max_results=max_results // len(search_queries[:3])
            )
            all_results.extend(results)
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result["url"] not in seen_urls:
                seen_urls.add(result["url"])
                unique_results.append(result)
        
        # Evaluate relevance and convert to Source objects
        sources = await self._process_results(query, unique_results[:max_results])
        
        logger.info(f"Found {len(sources)} relevant sources")
        return sources
    
    async def search_sub_queries(
        self,
        sub_queries: List[str],
        query_analysis: Optional[QueryAnalysis] = None,
        max_results_per_query: int = 5
    ) -> List[Source]:
        """
        Search for multiple sub-queries and combine results.
        
        Args:
            sub_queries: List of sub-queries to search
            query_analysis: Optional query analysis for context
            max_results_per_query: Maximum results per sub-query
            
        Returns:
            Combined list of Source objects
        """
        all_sources = []
        seen_urls = set()
        
        for sub_query in sub_queries:
            sources = await self.search(
                sub_query,
                query_analysis,
                max_results=max_results_per_query
            )
            
            for source in sources:
                if source.url not in seen_urls:
                    seen_urls.add(source.url)
                    all_sources.append(source)
        
        return all_sources
    
    async def _generate_search_queries(
        self,
        query: str,
        query_analysis: Optional[QueryAnalysis] = None
    ) -> List[Dict[str, Any]]:
        """Generate optimized search queries."""
        entities = []
        domain = "general"
        
        if query_analysis:
            entities = [e.text for e in query_analysis.entities]
            domain = query_analysis.domain
        
        prompt = SEARCH_PROMPTS["query_generation"].format(
            sub_query=query,
            original_query=query,
            domain=domain,
            entities=json.dumps(entities)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result.get("queries", [{"query": query, "priority": 1}])
        except Exception as e:
            logger.error(f"Search query generation failed: {e}")
            return [{"query": query, "priority": 1}]
    
    async def _execute_search(
        self, 
        query: str, 
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Execute search using available provider."""
        provider = self.fallback_provider if self._use_fallback else self.primary_provider
        
        try:
            results = await provider.search(query, max_results)
            if not results and not self._use_fallback:
                # Try fallback
                logger.warning("Primary search returned no results, trying fallback")
                self._use_fallback = True
                results = await self.fallback_provider.search(query, max_results)
            return results
        except Exception as e:
            if not self._use_fallback:
                logger.warning(f"Primary search failed, trying fallback: {e}")
                self._use_fallback = True
                return await self._execute_search(query, max_results)
            logger.error(f"All search providers failed: {e}")
            return []
    
    async def _process_results(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> List[Source]:
        """Process and evaluate search results."""
        if not results:
            return []
        
        # Evaluate relevance
        results_json = json.dumps([
            {"url": r["url"], "title": r["title"], "snippet": r.get("snippet", "")}
            for r in results
        ], indent=2)
        
        prompt = SEARCH_PROMPTS["relevance_evaluation"].format(
            query=query,
            search_results=results_json
        )
        
        try:
            evaluation = await self.llm.generate_json(prompt)
            evaluated = {r["url"]: r for r in evaluation.get("evaluated_results", [])}
        except Exception as e:
            logger.error(f"Relevance evaluation failed: {e}")
            evaluated = {}
        
        # Convert to Source objects
        sources = []
        for result in results:
            url = result["url"]
            eval_data = evaluated.get(url, {})
            
            # Parse domain from URL
            try:
                domain = urlparse(url).netloc
            except:
                domain = ""
            
            # Determine credibility based on domain
            credibility_score = self._estimate_credibility(domain, eval_data)
            
            source = Source(
                url=url,
                title=result.get("title", ""),
                content=result.get("content", result.get("snippet", "")),
                snippet=result.get("snippet", ""),
                domain=domain,
                credibility_score=credibility_score,
                credibility_level=self._score_to_level(credibility_score),
                metadata={
                    "relevance_score": eval_data.get("relevance_score", 5),
                    "information_value": eval_data.get("information_value", "medium"),
                    "freshness": eval_data.get("freshness", "unknown"),
                }
            )
            sources.append(source)
        
        # Sort by relevance
        sources.sort(
            key=lambda s: s.metadata.get("relevance_score", 0),
            reverse=True
        )
        
        return sources
    
    async def extract_content(self, source: Source, query: str) -> List[ExtractedInfo]:
        """Extract relevant information from a source."""
        if not source.content:
            return []
        
        prompt = SEARCH_PROMPTS["content_extraction"].format(
            query=query,
            url=source.url,
            title=source.title,
            content=source.content[:10000]  # Limit content length
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            
            extracted = []
            for info in result.get("extracted_information", []):
                extracted.append(ExtractedInfo(
                    source_id=source.id,
                    content=info.get("content", ""),
                    info_type=info.get("type", "fact"),
                    relevance=info.get("relevance", "medium"),
                    location=info.get("location", "")
                ))
            
            # Update source metadata
            source_info = result.get("source", {})
            if source_info.get("author"):
                source.author = source_info["author"]
            if source_info.get("publication_date"):
                source.publication_date = source_info["publication_date"]
            
            return extracted
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            return []
    
    def _estimate_credibility(
        self, 
        domain: str, 
        eval_data: Dict[str, Any]
    ) -> float:
        """Estimate source credibility based on domain and evaluation."""
        # Base score from evaluation
        quality = eval_data.get("source_quality", "medium")
        quality_scores = {"high": 0.8, "medium": 0.5, "low": 0.3, "unknown": 0.4}
        base_score = quality_scores.get(quality, 0.5)
        
        # Adjust based on domain
        if any(ext in domain for ext in [".gov", ".edu"]):
            base_score = min(1.0, base_score + 0.2)
        elif any(ext in domain for ext in [".org"]):
            base_score = min(1.0, base_score + 0.1)
        elif any(term in domain for term in ["wikipedia", "reuters", "bbc", "nytimes"]):
            base_score = min(1.0, base_score + 0.15)
        
        return base_score
    
    def _score_to_level(self, score: float) -> str:
        """Convert numeric score to credibility level."""
        if score >= 0.8:
            return "high"
        elif score >= 0.5:
            return "medium"
        else:
            return "low"


# Module instance
web_search = WebSearch()
