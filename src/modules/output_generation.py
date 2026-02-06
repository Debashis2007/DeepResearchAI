"""
Output generation module for the Deep Research AI system.

This module handles the final synthesis and formatting of research results
into user-friendly, well-structured outputs in various formats.
"""

from enum import Enum
from typing import Any

from ..config import Config
from ..llm_client import LLMClient
from ..models import Source, ResearchResult, OutputFormat
from ..prompts.output_prompts import (
    REPORT_GENERATION_PROMPT,
    SUMMARY_GENERATION_PROMPT,
    ANSWER_FORMATTING_PROMPT,
    VISUALIZATION_SUGGESTION_PROMPT,
    MULTI_FORMAT_OUTPUT_PROMPT,
    RESPONSE_QUALITY_PROMPT,
    FOLLOWUP_QUESTIONS_PROMPT,
    EXPORT_FORMAT_PROMPT,
)


class SummaryLength(Enum):
    """Summary length options."""
    BRIEF = "brief"
    STANDARD = "standard"
    DETAILED = "detailed"


class AudienceType(Enum):
    """Target audience types."""
    GENERAL = "general"
    PROFESSIONAL = "professional"
    ACADEMIC = "academic"
    TECHNICAL = "technical"


class ExportFormat(Enum):
    """Export format options."""
    PDF = "pdf"
    DOCX = "docx"
    SLIDES = "slides"
    EMAIL = "email"
    SOCIAL = "social"


class OutputGenerator:
    """
    Generates formatted output from research results.
    
    Provides comprehensive output generation including:
    - Full research reports
    - Summaries at various lengths
    - Multi-format output generation
    - Quality assessment
    - Follow-up question generation
    """
    
    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize the OutputGenerator.
        
        Args:
            config: Configuration object. Uses default if not provided.
        """
        self.config = config or Config()
        self.llm_client = LLMClient(self.config.llm_config)
    
    async def generate_report(
        self,
        query: str,
        findings: dict[str, Any],
        sources: list[Source],
        confidence: float
    ) -> dict[str, Any]:
        """
        Generate a comprehensive research report.
        
        Args:
            query: Original research query
            findings: Synthesized research findings
            sources: Sources used in research
            confidence: Overall confidence score
            
        Returns:
            Dictionary containing the full research report
        """
        sources_text = self._format_sources(sources)
        
        prompt = REPORT_GENERATION_PROMPT.format(
            query=query,
            findings=str(findings),
            sources=sources_text,
            confidence=f"{confidence:.2%}"
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "report": result.get("report", {}),
            "metadata": result.get("metadata", {}),
            "format": OutputFormat.MARKDOWN
        }
    
    async def generate_summary(
        self,
        findings: dict[str, Any],
        length: SummaryLength = SummaryLength.STANDARD
    ) -> dict[str, Any]:
        """
        Generate a summary of research findings.
        
        Args:
            findings: Research findings to summarize
            length: Desired summary length
            
        Returns:
            Dictionary containing the summary
        """
        prompt = SUMMARY_GENERATION_PROMPT.format(
            findings=str(findings),
            length=length.value
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "summary": result.get("summary", {}),
            "metadata": result.get("metadata", {})
        }
    
    async def format_answer(
        self,
        answer: str,
        audience: AudienceType = AudienceType.GENERAL,
        output_format: OutputFormat = OutputFormat.MARKDOWN
    ) -> dict[str, Any]:
        """
        Format an answer for a specific audience and format.
        
        Args:
            answer: The answer to format
            audience: Target audience
            output_format: Desired output format
            
        Returns:
            Dictionary containing the formatted answer
        """
        prompt = ANSWER_FORMATTING_PROMPT.format(
            answer=answer,
            audience=audience.value,
            format=output_format.value
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "formatted_answer": result.get("formatted_answer", {}),
            "readability_metrics": result.get("readability_metrics", {})
        }
    
    async def suggest_visualizations(
        self,
        data: dict[str, Any],
        findings: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Suggest visualizations for research data.
        
        Args:
            data: Numerical or structured data
            findings: Research findings
            
        Returns:
            Dictionary with visualization suggestions
        """
        prompt = VISUALIZATION_SUGGESTION_PROMPT.format(
            data=str(data),
            findings=str(findings)
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "visualizations": result.get("visualizations", []),
            "recommended_count": result.get("recommended_count", 0),
            "data_visualization_potential": result.get("data_visualization_potential", "low")
        }
    
    async def generate_multi_format(
        self,
        content: str,
        citations: str
    ) -> dict[str, Any]:
        """
        Generate output in multiple formats simultaneously.
        
        Args:
            content: Research content
            citations: Citation information
            
        Returns:
            Dictionary with content in multiple formats
        """
        prompt = MULTI_FORMAT_OUTPUT_PROMPT.format(
            content=content,
            citations=citations
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "outputs": result.get("outputs", {}),
            "recommended_format": result.get("recommended_format", "markdown"),
            "format_notes": result.get("format_notes", {})
        }
    
    async def assess_quality(
        self,
        query: str,
        response: str,
        sources: list[Source]
    ) -> dict[str, Any]:
        """
        Assess the quality of a generated response.
        
        Args:
            query: Original query
            response: Generated response
            sources: Sources used
            
        Returns:
            Dictionary with quality assessment
        """
        sources_text = self._format_sources(sources)
        
        prompt = RESPONSE_QUALITY_PROMPT.format(
            query=query,
            response=response,
            sources=sources_text
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "quality_assessment": result.get("quality_assessment", {}),
            "confidence_level": result.get("confidence_level", "medium"),
            "ready_for_delivery": result.get("ready_for_delivery", False),
            "revision_needed": result.get("revision_needed", True)
        }
    
    async def generate_followup_questions(
        self,
        query: str,
        findings: dict[str, Any],
        gaps: list[str]
    ) -> dict[str, Any]:
        """
        Generate relevant follow-up questions.
        
        Args:
            query: Original query
            findings: Research findings
            gaps: Identified information gaps
            
        Returns:
            Dictionary with follow-up questions
        """
        prompt = FOLLOWUP_QUESTIONS_PROMPT.format(
            query=query,
            findings=str(findings),
            gaps=str(gaps)
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "follow_up_questions": result.get("follow_up_questions", []),
            "recommended_next_question": result.get("recommended_next_question", ""),
            "research_continuation_score": result.get("research_continuation_score", 0.0)
        }
    
    async def prepare_for_export(
        self,
        report: dict[str, Any],
        export_format: ExportFormat
    ) -> dict[str, Any]:
        """
        Prepare research output for export.
        
        Args:
            report: Research report
            export_format: Target export format
            
        Returns:
            Dictionary with export-ready content
        """
        prompt = EXPORT_FORMAT_PROMPT.format(
            report=str(report),
            export_format=export_format.value
        )
        
        result = await self.llm_client.call_json(prompt)
        
        return {
            "export_ready": result.get("export_ready", {}),
            "export_metadata": result.get("export_metadata", {})
        }
    
    async def create_research_result(
        self,
        query: str,
        findings: dict[str, Any],
        sources: list[Source],
        confidence: float,
        audience: AudienceType = AudienceType.GENERAL
    ) -> ResearchResult:
        """
        Create a complete ResearchResult object.
        
        This method combines all output generation capabilities into
        a single comprehensive research result.
        
        Args:
            query: Original query
            findings: Research findings
            sources: Sources used
            confidence: Confidence score
            audience: Target audience
            
        Returns:
            Complete ResearchResult object
        """
        # Generate the main report
        report_result = await self.generate_report(
            query, findings, sources, confidence
        )
        
        # Generate summary
        summary_result = await self.generate_summary(
            findings, SummaryLength.STANDARD
        )
        
        # Assess quality
        report_text = self._report_to_text(report_result["report"])
        quality_result = await self.assess_quality(query, report_text, sources)
        
        # Generate follow-up questions
        gaps = findings.get("information_gaps", [])
        followup_result = await self.generate_followup_questions(
            query, findings, gaps
        )
        
        # Build the research result
        return ResearchResult(
            query=query,
            answer=summary_result["summary"].get("text", ""),
            confidence=confidence,
            sources=sources,
            reasoning_steps=findings.get("reasoning_steps", []),
            verification_status=findings.get("verification_status", "unverified"),
            metadata={
                "full_report": report_result["report"],
                "quality_assessment": quality_result["quality_assessment"],
                "follow_up_questions": followup_result["follow_up_questions"],
                "audience": audience.value
            }
        )
    
    def _format_sources(self, sources: list[Source]) -> str:
        """Format sources for prompts."""
        formatted = []
        for i, source in enumerate(sources, 1):
            formatted.append(f"""
Source {i}:
- Title: {source.title}
- URL: {source.url}
- Credibility: {source.credibility_score}
""")
        return "\n".join(formatted)
    
    def _report_to_text(self, report: dict) -> str:
        """Convert report dict to plain text."""
        parts = []
        
        if "title" in report:
            parts.append(f"# {report['title']}\n")
        
        if "executive_summary" in report:
            parts.append(f"## Executive Summary\n{report['executive_summary']}\n")
        
        if "main_findings" in report:
            parts.append("## Main Findings\n")
            for finding in report["main_findings"]:
                parts.append(f"### {finding.get('theme', 'Finding')}\n")
                parts.append(f"{finding.get('content', '')}\n")
        
        if "conclusion" in report:
            conclusion = report["conclusion"]
            parts.append("## Conclusion\n")
            parts.append(f"{conclusion.get('answer', '')}\n")
        
        return "\n".join(parts)
    
    def render_markdown(self, report: dict) -> str:
        """
        Render a report as markdown.
        
        Args:
            report: Report dictionary
            
        Returns:
            Markdown formatted string
        """
        return self._report_to_text(report)
    
    def render_html(self, report: dict) -> str:
        """
        Render a report as HTML.
        
        Args:
            report: Report dictionary
            
        Returns:
            HTML formatted string
        """
        md = self._report_to_text(report)
        # Basic markdown to HTML conversion
        html = md.replace("# ", "<h1>").replace("\n## ", "</h1>\n<h2>")
        html = html.replace("\n### ", "</h2>\n<h3>").replace("\n\n", "</p>\n<p>")
        return f"<html><body>{html}</body></html>"


# Module singleton instance
output_generator = OutputGenerator()
