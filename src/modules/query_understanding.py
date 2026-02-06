"""
Query Understanding Module - Parses and analyzes research queries.
"""

import logging
from typing import Optional, Dict, Any, List

from ..models import QueryAnalysis, Entity, QueryComplexity
from ..llm_client import llm_client
from ..prompts.query_prompts import QUERY_PROMPTS

logger = logging.getLogger(__name__)


class QueryUnderstanding:
    """
    Query Understanding module for analyzing and decomposing research queries.
    
    Implements FR-1: Query Understanding requirements.
    """
    
    def __init__(self):
        self.llm = llm_client
    
    async def analyze_query(self, query: str) -> QueryAnalysis:
        """
        Analyze a research query to understand intent, entities, and structure.
        
        Args:
            query: Raw natural language research query
            
        Returns:
            QueryAnalysis object with parsed query information
        """
        logger.info(f"Analyzing query: {query[:100]}...")
        
        # First, validate the query
        validation = await self._validate_query(query)
        if not validation.get("proceed", True):
            logger.warning(f"Query validation failed: {validation}")
            # Create minimal analysis for invalid query
            analysis = QueryAnalysis(raw_query=query)
            analysis.sub_queries = []
            return analysis
        
        # Analyze the query
        analysis_result = await self._analyze(query)
        
        # Extract entities
        entities = await self._extract_entities(query)
        
        # Classify intent
        intent_result = await self._classify_intent(query)
        
        # Build QueryAnalysis object
        analysis = self._build_analysis(
            query=query,
            analysis_result=analysis_result,
            entities=entities,
            intent_result=intent_result
        )
        
        # Decompose into sub-queries if complex
        if analysis.complexity in [QueryComplexity.MEDIUM, QueryComplexity.COMPLEX]:
            sub_queries = await self._decompose_query(query, analysis_result)
            analysis.sub_queries = sub_queries
        else:
            analysis.sub_queries = [query]
        
        logger.info(f"Query analysis complete. Complexity: {analysis.complexity.value}, "
                   f"Sub-queries: {len(analysis.sub_queries)}")
        
        return analysis
    
    async def _validate_query(self, query: str) -> Dict[str, Any]:
        """Validate if the query is researchable and appropriate."""
        prompt = QUERY_PROMPTS["validation"].format(query=query)
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Query validation failed: {e}")
            return {"proceed": True, "is_valid": True}
    
    async def _analyze(self, query: str) -> Dict[str, Any]:
        """Perform main query analysis."""
        prompt = QUERY_PROMPTS["analysis"].format(query=query)
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Query analysis failed: {e}")
            return {
                "intent": "unknown",
                "domain": "general",
                "entities": [],
                "complexity": "medium",
                "output_type": "report"
            }
    
    async def _extract_entities(self, query: str) -> List[Entity]:
        """Extract named entities from the query."""
        prompt = QUERY_PROMPTS["entity_extraction"].format(query=query)
        
        try:
            result = await self.llm.generate_json(prompt)
            entities = []
            
            for entity_data in result.get("entities", []):
                entity = Entity(
                    text=entity_data.get("text", ""),
                    type=entity_data.get("type", "CONCEPT"),
                    relevance=entity_data.get("relevance", "secondary"),
                    context=entity_data.get("context")
                )
                entities.append(entity)
            
            return entities
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []
    
    async def _classify_intent(self, query: str) -> Dict[str, Any]:
        """Classify the query intent."""
        prompt = QUERY_PROMPTS["intent_classification"].format(query=query)
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return {
                "primary_intent": "EXPLORATORY",
                "confidence": 0.5,
                "research_approach": "general"
            }
    
    async def _decompose_query(
        self, 
        query: str, 
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Decompose a complex query into sub-queries."""
        import json
        
        prompt = QUERY_PROMPTS["decomposition"].format(
            query=query,
            query_analysis=json.dumps(analysis, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            sub_queries = []
            
            for sq in result.get("sub_queries", []):
                sub_queries.append(sq.get("query", ""))
            
            # Ensure we have at least the original query
            if not sub_queries:
                sub_queries = [query]
            
            return sub_queries
        except Exception as e:
            logger.error(f"Query decomposition failed: {e}")
            return [query]
    
    async def check_clarity(self, query: str) -> Dict[str, Any]:
        """Check if the query needs clarification."""
        prompt = QUERY_PROMPTS["clarification"].format(query=query)
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Clarity check failed: {e}")
            return {"is_clear": True, "ambiguities": []}
    
    def _build_analysis(
        self,
        query: str,
        analysis_result: Dict[str, Any],
        entities: List[Entity],
        intent_result: Dict[str, Any]
    ) -> QueryAnalysis:
        """Build a QueryAnalysis object from component results."""
        # Map complexity string to enum
        complexity_map = {
            "simple": QueryComplexity.SIMPLE,
            "medium": QueryComplexity.MEDIUM,
            "complex": QueryComplexity.COMPLEX
        }
        
        complexity_str = analysis_result.get("complexity", "medium").lower()
        complexity = complexity_map.get(complexity_str, QueryComplexity.MEDIUM)
        
        # Combine entities from analysis and extraction
        all_entities = entities.copy()
        for entity_data in analysis_result.get("entities", []):
            if isinstance(entity_data, dict):
                entity = Entity(
                    text=entity_data.get("text", ""),
                    type=entity_data.get("type", "CONCEPT"),
                    relevance=entity_data.get("relevance", "secondary")
                )
                # Avoid duplicates
                if not any(e.text == entity.text for e in all_entities):
                    all_entities.append(entity)
        
        return QueryAnalysis(
            raw_query=query,
            intent=intent_result.get("primary_intent", analysis_result.get("intent", "")),
            domain=analysis_result.get("domain", "general"),
            entities=all_entities,
            temporal_scope=analysis_result.get("temporal_scope"),
            geographic_scope=analysis_result.get("geographic_scope"),
            complexity=complexity,
            output_type=analysis_result.get("output_type", "report")
        )


# Module instance
query_understanding = QueryUnderstanding()
