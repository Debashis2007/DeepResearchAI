"""
Reasoning Engine Module - Multi-step reasoning and information synthesis.
"""

import logging
import json
from typing import Optional, Dict, Any, List

from ..models import (
    QueryAnalysis, Source, Finding, Claim, 
    ConfidenceLevel, VerificationStatus
)
from ..llm_client import llm_client
from ..prompts.reasoning_prompts import REASONING_PROMPTS

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """
    Reasoning Engine for multi-step reasoning over gathered information.
    
    Implements FR-3: Multi-Step Reasoning requirements.
    """
    
    def __init__(self):
        self.llm = llm_client
    
    async def reason(
        self,
        query: QueryAnalysis,
        sources: List[Source],
        extracted_info: Optional[List[Dict[str, Any]]] = None
    ) -> List[Finding]:
        """
        Perform multi-step reasoning over gathered information.
        
        Args:
            query: Analyzed query
            sources: List of sources with content
            extracted_info: Optional pre-extracted information
            
        Returns:
            List of findings from reasoning
        """
        logger.info(f"Starting reasoning for query: {query.raw_query[:50]}...")
        
        # Prepare context from sources
        context = self._prepare_context(sources, extracted_info)
        
        # Perform chain-of-thought reasoning
        reasoning_result = await self._chain_of_thought(
            query.raw_query,
            context,
            sources
        )
        
        # Synthesize across sources
        synthesis = await self._synthesize(query.raw_query, sources)
        
        # Check if this is a comparative query
        if query.intent in ["COMPARATIVE", "EVALUATIVE"]:
            comparison = await self._comparative_analysis(
                query.raw_query,
                sources,
                context
            )
            synthesis["comparison"] = comparison
        
        # Build findings from reasoning results
        findings = self._build_findings(
            reasoning_result,
            synthesis,
            sources
        )
        
        # Identify gaps
        gaps = await self._identify_gaps(
            query.raw_query,
            findings,
            sources
        )
        
        # Add gap information to findings
        if gaps.get("priority_gaps"):
            for finding in findings:
                finding.caveats.extend(gaps.get("priority_gaps", [])[:2])
        
        logger.info(f"Reasoning complete. Generated {len(findings)} findings")
        return findings
    
    async def _chain_of_thought(
        self,
        query: str,
        context: str,
        sources: List[Source]
    ) -> Dict[str, Any]:
        """Perform chain-of-thought reasoning."""
        sources_summary = self._summarize_sources(sources)
        
        prompt = REASONING_PROMPTS["chain_of_thought"].format(
            query=query,
            context=context,
            sources=sources_summary
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Chain-of-thought reasoning failed: {e}")
            return {
                "reasoning_chain": [],
                "final_answer": "",
                "confidence": 0.5,
                "gaps_identified": []
            }
    
    async def _synthesize(
        self,
        query: str,
        sources: List[Source]
    ) -> Dict[str, Any]:
        """Synthesize information across sources."""
        sources_with_content = []
        for source in sources:
            sources_with_content.append({
                "url": source.url,
                "title": source.title,
                "content": source.content[:3000] if source.content else source.snippet,
                "credibility": source.credibility_level
            })
        
        prompt = REASONING_PROMPTS["synthesis"].format(
            query=query,
            sources_with_content=json.dumps(sources_with_content, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            return {
                "themes": [],
                "consensus_findings": [],
                "disagreements": [],
                "synthesis": "",
                "key_insights": []
            }
    
    async def _comparative_analysis(
        self,
        query: str,
        sources: List[Source],
        context: str
    ) -> Dict[str, Any]:
        """Perform comparative analysis if query involves comparison."""
        # Extract subjects to compare from query
        subjects = self._extract_comparison_subjects(query)
        
        prompt = REASONING_PROMPTS["comparative_analysis"].format(
            query=query,
            subjects=json.dumps(subjects),
            context=context
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Comparative analysis failed: {e}")
            return {}
    
    async def _causal_analysis(
        self,
        query: str,
        context: str
    ) -> Dict[str, Any]:
        """Perform causal analysis if applicable."""
        prompt = REASONING_PROMPTS["causal_analysis"].format(
            query=query,
            context=context
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Causal analysis failed: {e}")
            return {}
    
    async def _identify_gaps(
        self,
        query: str,
        findings: List[Finding],
        sources: List[Source]
    ) -> Dict[str, Any]:
        """Identify gaps in current research."""
        findings_summary = [
            {"title": f.title, "content": f.content[:500]}
            for f in findings
        ]
        sources_summary = [
            {"url": s.url, "title": s.title}
            for s in sources
        ]
        
        prompt = REASONING_PROMPTS["gap_analysis"].format(
            query=query,
            findings=json.dumps(findings_summary, indent=2),
            sources=json.dumps(sources_summary, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            return {"can_proceed": True, "priority_gaps": []}
    
    async def verify_reasoning(
        self,
        reasoning_chain: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Verify the logical soundness of a reasoning chain."""
        prompt = REASONING_PROMPTS["reasoning_verification"].format(
            reasoning_chain=json.dumps(reasoning_chain, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Reasoning verification failed: {e}")
            return {"is_valid": True, "validity_score": 70}
    
    def _prepare_context(
        self,
        sources: List[Source],
        extracted_info: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Prepare context string from sources and extracted info."""
        context_parts = []
        
        for i, source in enumerate(sources, 1):
            content = source.content if source.content else source.snippet
            if content:
                context_parts.append(
                    f"[Source {i}: {source.title}]\n"
                    f"URL: {source.url}\n"
                    f"Content: {content[:2000]}\n"
                )
        
        if extracted_info:
            context_parts.append("\n[Extracted Key Information]")
            for info in extracted_info:
                context_parts.append(f"- {info.get('content', '')}")
        
        return "\n".join(context_parts)
    
    def _summarize_sources(self, sources: List[Source]) -> str:
        """Create a summary of sources for prompts."""
        summaries = []
        for i, source in enumerate(sources, 1):
            summaries.append(
                f"[{i}] {source.title} ({source.url}) - "
                f"Credibility: {source.credibility_level}"
            )
        return "\n".join(summaries)
    
    def _extract_comparison_subjects(self, query: str) -> List[str]:
        """Extract subjects being compared from query."""
        # Simple extraction - in real implementation, use NLP
        comparison_words = ["vs", "versus", "compare", "between", "and"]
        subjects = []
        
        query_lower = query.lower()
        for word in comparison_words:
            if word in query_lower:
                # Very basic extraction
                parts = query_lower.split(word)
                if len(parts) >= 2:
                    subjects = [parts[0].strip(), parts[1].strip()]
                    break
        
        return subjects if subjects else ["Subject A", "Subject B"]
    
    def _build_findings(
        self,
        reasoning_result: Dict[str, Any],
        synthesis: Dict[str, Any],
        sources: List[Source]
    ) -> List[Finding]:
        """Build Finding objects from reasoning results."""
        findings = []
        source_ids = [s.id for s in sources]
        
        # Create finding from main answer
        if reasoning_result.get("final_answer"):
            confidence = reasoning_result.get("confidence", 0.5)
            
            main_finding = Finding(
                title="Main Finding",
                content=reasoning_result["final_answer"],
                category="main",
                confidence_score=confidence,
                confidence_level=self._score_to_level(confidence),
                source_ids=source_ids[:5],  # Top 5 sources
                reasoning_chain=[
                    step.get("thought", "")
                    for step in reasoning_result.get("reasoning_chain", [])
                ],
                caveats=reasoning_result.get("gaps_identified", [])
            )
            findings.append(main_finding)
        
        # Create findings from themes
        for theme in synthesis.get("themes", []):
            finding = Finding(
                title=theme.get("theme", "Theme"),
                content=theme.get("description", ""),
                category="theme",
                confidence_score=0.7,
                confidence_level=ConfidenceLevel.HIGH,
                source_ids=source_ids[:3],
            )
            
            # Add key points as claims
            for point in theme.get("key_points", []):
                claim = Claim(
                    content=point,
                    source_ids=source_ids[:2],
                    verification_status=VerificationStatus.PARTIALLY_VERIFIED,
                    confidence_score=0.7
                )
                finding.claims.append(claim)
            
            findings.append(finding)
        
        # Create findings from consensus
        for consensus in synthesis.get("consensus_findings", []):
            confidence = 0.9 if consensus.get("confidence") == "high" else 0.7
            
            finding = Finding(
                title="Consensus Finding",
                content=consensus.get("finding", ""),
                category="consensus",
                confidence_score=confidence,
                confidence_level=self._score_to_level(confidence),
                source_ids=source_ids[:3],
            )
            findings.append(finding)
        
        # Note disagreements
        for disagreement in synthesis.get("disagreements", []):
            finding = Finding(
                title=f"Disputed: {disagreement.get('topic', 'Topic')}",
                content=self._format_disagreement(disagreement),
                category="disagreement",
                confidence_score=0.5,
                confidence_level=ConfidenceLevel.MEDIUM,
                source_ids=source_ids[:3],
                caveats=["Sources disagree on this topic"]
            )
            findings.append(finding)
        
        # Add key insights
        if synthesis.get("key_insights"):
            finding = Finding(
                title="Key Insights",
                content="\n".join(f"• {insight}" for insight in synthesis["key_insights"]),
                category="insights",
                confidence_score=0.8,
                confidence_level=ConfidenceLevel.HIGH,
                source_ids=source_ids[:5],
            )
            findings.append(finding)
        
        return findings
    
    def _format_disagreement(self, disagreement: Dict[str, Any]) -> str:
        """Format a disagreement for display."""
        parts = [f"Topic: {disagreement.get('topic', 'Unknown')}"]
        
        for perspective in disagreement.get("perspectives", []):
            parts.append(
                f"• {perspective.get('source', 'Source')}: {perspective.get('position', '')}"
            )
        
        return "\n".join(parts)
    
    def _score_to_level(self, score: float) -> ConfidenceLevel:
        """Convert numeric score to confidence level."""
        if score >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif score >= 0.7:
            return ConfidenceLevel.HIGH
        elif score >= 0.5:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.3:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW


# Module instance
reasoning_engine = ReasoningEngine()
