"""
Citation module for the Deep Research AI system.

This module handles citation generation, source attribution, and reference
list creation in multiple academic formats.
"""

import hashlib
from datetime import date
from typing import Any

from ..config import Config
from ..llm_client import LLMClient
from ..models import Source, Citation, CitationStyle
from ..prompts.citation_prompts import (
    CITATION_GENERATION_PROMPT,
    SOURCE_ATTRIBUTION_PROMPT,
    REFERENCE_LIST_PROMPT,
    INLINE_CITATION_PROMPT,
    CITATION_VALIDATION_PROMPT,
    SOURCE_METADATA_PROMPT,
    FOOTNOTE_GENERATION_PROMPT,
)


class CitationManager:
    """
    Manages citation generation, formatting, and source attribution.
    
    Provides comprehensive citation support including:
    - Multi-format citation generation (APA, MLA, Chicago, IEEE, Harvard)
    - Source attribution mapping
    - Reference list generation
    - Inline citation insertion
    - Citation validation
    """
    
    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize the CitationManager.
        
        Args:
            config: Configuration object. Uses default if not provided.
        """
        self.config = config or Config()
        self.llm_client = LLMClient(self.config.llm_config)
    
    async def generate_citations(
        self,
        sources: list[Source],
        content: str
    ) -> dict[str, Any]:
        """
        Generate citations for sources in multiple formats.
        
        Args:
            sources: List of Source objects to cite
            content: Content using these sources
            
        Returns:
            Dictionary containing citations in multiple formats with metadata
        """
        sources_text = self._format_sources_for_prompt(sources)
        
        prompt = CITATION_GENERATION_PROMPT.format(
            sources=sources_text,
            content=content[:5000]  # Limit content length
        )
        
        result = await self.llm_client.call_json(prompt)
        
        # Convert to Citation objects
        citations = []
        for cit_data in result.get("citations", []):
            citation = self._create_citation_from_data(cit_data)
            citations.append(citation)
        
        return {
            "citations": citations,
            "bibliography": result.get("bibliography", {}),
            "raw_response": result
        }
    
    async def attribute_sources(
        self,
        content: str,
        sources: list[Source]
    ) -> dict[str, Any]:
        """
        Map claims in content to their original sources.
        
        Args:
            content: Research content to analyze
            sources: Available sources for attribution
            
        Returns:
            Dictionary with claim-to-source attributions
        """
        sources_text = self._format_sources_for_prompt(sources)
        
        prompt = SOURCE_ATTRIBUTION_PROMPT.format(
            content=content,
            sources=sources_text
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "attributions": result.get("attributions", []),
            "unattributed_claims": result.get("unattributed_claims", []),
            "attribution_coverage": result.get("attribution_coverage", 0.0)
        }
    
    async def generate_reference_list(
        self,
        sources: list[Source],
        style: CitationStyle = CitationStyle.APA
    ) -> dict[str, Any]:
        """
        Generate a formatted reference list in specified style.
        
        Args:
            sources: Sources to include in reference list
            style: Citation style to use
            
        Returns:
            Dictionary with formatted reference list
        """
        sources_text = self._format_sources_for_prompt(sources)
        
        prompt = REFERENCE_LIST_PROMPT.format(
            sources=sources_text,
            citation_style=style.value
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "reference_list": result.get("reference_list", []),
            "formatted_output": result.get("formatted_output", ""),
            "style": style.value,
            "total_references": result.get("total_references", len(sources))
        }
    
    async def insert_inline_citations(
        self,
        content: str,
        attributions: list[dict],
        style: CitationStyle = CitationStyle.APA
    ) -> dict[str, Any]:
        """
        Insert inline citations into content.
        
        Args:
            content: Content to annotate
            attributions: Source attributions from attribute_sources()
            style: Citation style to use
            
        Returns:
            Dictionary with annotated content and citation details
        """
        prompt = INLINE_CITATION_PROMPT.format(
            content=content,
            attributions=str(attributions),
            citation_style=style.value
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "annotated_content": result.get("annotated_content", content),
            "citation_count": result.get("citation_count", 0),
            "citation_positions": result.get("citation_positions", []),
            "style_used": style.value
        }
    
    async def validate_citations(
        self,
        citations: list[Citation],
        sources: list[Source]
    ) -> dict[str, Any]:
        """
        Validate citations for accuracy and completeness.
        
        Args:
            citations: Citations to validate
            sources: Original sources for verification
            
        Returns:
            Dictionary with validation results and recommendations
        """
        citations_text = self._format_citations_for_prompt(citations)
        sources_text = self._format_sources_for_prompt(sources)
        
        prompt = CITATION_VALIDATION_PROMPT.format(
            citations=citations_text,
            sources=sources_text
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "validation_results": result.get("validation_results", []),
            "overall_quality": result.get("overall_quality", 0.0),
            "total_issues": result.get("total_issues", 0),
            "recommendations": result.get("recommendations", [])
        }
    
    async def extract_source_metadata(
        self,
        url: str,
        content: str
    ) -> dict[str, Any]:
        """
        Extract citation metadata from source content.
        
        Args:
            url: Source URL
            content: Source content to analyze
            
        Returns:
            Dictionary with extracted metadata
        """
        prompt = SOURCE_METADATA_PROMPT.format(
            url=url,
            content=content[:8000]  # Limit content length
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "metadata": result.get("metadata", {}),
            "extraction_confidence": result.get("extraction_confidence", {}),
            "inferred_fields": result.get("inferred_fields", []),
            "missing_fields": result.get("missing_fields", [])
        }
    
    async def generate_footnotes(
        self,
        content: str,
        sources: list[Source],
        attributions: list[dict]
    ) -> dict[str, Any]:
        """
        Generate footnotes for the content.
        
        Args:
            content: Content to annotate
            sources: Sources used
            attributions: Source attributions
            
        Returns:
            Dictionary with footnotes and annotated content
        """
        sources_text = self._format_sources_for_prompt(sources)
        
        prompt = FOOTNOTE_GENERATION_PROMPT.format(
            content=content,
            sources=sources_text,
            attributions=str(attributions)
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "footnotes": result.get("footnotes", []),
            "content_with_markers": result.get("content_with_markers", content),
            "footnote_section": result.get("footnote_section", "")
        }
    
    async def create_full_citation_package(
        self,
        content: str,
        sources: list[Source],
        style: CitationStyle = CitationStyle.APA
    ) -> dict[str, Any]:
        """
        Create a complete citation package for content.
        
        This method combines all citation operations into one comprehensive
        result including attributions, inline citations, and reference list.
        
        Args:
            content: Research content
            sources: Sources used in research
            style: Citation style to use
            
        Returns:
            Complete citation package with all components
        """
        # Step 1: Generate citations for all sources
        citation_result = await self.generate_citations(sources, content)
        
        # Step 2: Attribute sources to claims
        attribution_result = await self.attribute_sources(content, sources)
        
        # Step 3: Insert inline citations
        inline_result = await self.insert_inline_citations(
            content,
            attribution_result["attributions"],
            style
        )
        
        # Step 4: Generate reference list
        reference_result = await self.generate_reference_list(sources, style)
        
        # Step 5: Validate citations
        validation_result = await self.validate_citations(
            citation_result["citations"],
            sources
        )
        
        return {
            "citations": citation_result["citations"],
            "attributions": attribution_result["attributions"],
            "attribution_coverage": attribution_result["attribution_coverage"],
            "annotated_content": inline_result["annotated_content"],
            "reference_list": reference_result["formatted_output"],
            "citation_count": inline_result["citation_count"],
            "validation": {
                "quality": validation_result["overall_quality"],
                "issues": validation_result["total_issues"],
                "recommendations": validation_result["recommendations"]
            },
            "style": style.value
        }
    
    def _format_sources_for_prompt(self, sources: list[Source]) -> str:
        """Format sources for inclusion in prompts."""
        formatted = []
        for i, source in enumerate(sources, 1):
            source_text = f"""
Source {i}:
- ID: {source.source_id}
- URL: {source.url}
- Title: {source.title}
- Domain: {source.domain}
- Content Preview: {source.content[:500] if source.content else 'N/A'}...
- Credibility Score: {source.credibility_score}
"""
            formatted.append(source_text)
        return "\n".join(formatted)
    
    def _format_citations_for_prompt(self, citations: list[Citation]) -> str:
        """Format citations for inclusion in prompts."""
        formatted = []
        for citation in citations:
            cit_text = f"""
Citation for: {citation.source_id}
- Style: {citation.style.value}
- Formatted: {citation.formatted_citation}
- In-text: {citation.in_text_citation}
"""
            formatted.append(cit_text)
        return "\n".join(formatted)
    
    def _create_citation_from_data(self, data: dict) -> Citation:
        """Create a Citation object from parsed data."""
        source_id = data.get("source_id", "unknown")
        
        # Default to APA format
        formats = data.get("formats", {})
        formatted = formats.get("apa", "")
        
        in_text = data.get("in_text", {})
        in_text_citation = in_text.get("apa", "")
        
        return Citation(
            source_id=source_id,
            style=CitationStyle.APA,
            formatted_citation=formatted,
            in_text_citation=in_text_citation,
            metadata=data.get("metadata", {})
        )
    
    def generate_source_id(self, url: str) -> str:
        """
        Generate a unique source ID from URL.
        
        Args:
            url: Source URL
            
        Returns:
            Unique identifier for the source
        """
        return hashlib.md5(url.encode()).hexdigest()[:12]
    
    def format_access_date(self) -> str:
        """Get current date formatted for citations."""
        return date.today().strftime("%Y-%m-%d")


# Module singleton instance
citation_manager = CitationManager()
