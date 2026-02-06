"""
Research Orchestrator for the Deep Research AI system.

This module coordinates all research components to provide a unified
research pipeline from query to final output.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from enum import Enum

from .config import Config
from .models import (
    QueryAnalysis,
    SearchResult,
    Source,
    ReasoningStep,
    ResearchResult,
    OutputFormat,
    CitationStyle,
)
from .modules.query_understanding import QueryUnderstanding
from .modules.web_search import WebSearch
from .modules.reasoning_engine import ReasoningEngine
from .modules.verification import Verification
from .modules.citation import CitationManager
from .modules.output_generation import OutputGenerator, SummaryLength, AudienceType
from .modules.error_handling import (
    ErrorHandler,
    ErrorContext,
    ErrorSeverity,
    ComponentType,
    ResearchError,
)


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchStage(Enum):
    """Stages of the research pipeline."""
    QUERY_ANALYSIS = "query_analysis"
    WEB_SEARCH = "web_search"
    REASONING = "reasoning"
    VERIFICATION = "verification"
    CITATION = "citation"
    OUTPUT_GENERATION = "output_generation"
    COMPLETE = "complete"


@dataclass
class ResearchProgress:
    """Tracks research progress."""
    current_stage: ResearchStage
    stages_completed: list[ResearchStage] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    stage_times: dict[str, float] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    
    def complete_stage(self, stage: ResearchStage, duration: float) -> None:
        """Mark a stage as complete."""
        self.stages_completed.append(stage)
        self.stage_times[stage.value] = duration
    
    @property
    def progress_percentage(self) -> float:
        """Get completion percentage."""
        total_stages = len(ResearchStage) - 1  # Exclude COMPLETE
        return (len(self.stages_completed) / total_stages) * 100


@dataclass
class ResearchSession:
    """A research session with all intermediate results."""
    session_id: str
    query: str
    progress: ResearchProgress
    query_analysis: QueryAnalysis | None = None
    search_results: list[SearchResult] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    reasoning_steps: list[ReasoningStep] = field(default_factory=list)
    synthesis: dict | None = None
    verification: dict | None = None
    citations: dict | None = None
    final_result: ResearchResult | None = None
    metadata: dict = field(default_factory=dict)


class ResearchOrchestrator:
    """
    Orchestrates the complete research pipeline.
    
    Coordinates all modules to perform comprehensive research:
    1. Query Understanding - Analyze and decompose the query
    2. Web Search - Search and extract relevant content
    3. Reasoning - Synthesize and analyze findings
    4. Verification - Verify claims and assess credibility
    5. Citation - Generate proper citations
    6. Output Generation - Create formatted output
    """
    
    def __init__(self, config: Config | None = None) -> None:
        """
        Initialize the ResearchOrchestrator.
        
        Args:
            config: Configuration object. Uses default if not provided.
        """
        self.config = config or Config()
        
        # Initialize all modules
        self.query_understanding = QueryUnderstanding(self.config)
        self.web_search = WebSearch(self.config)
        self.reasoning_engine = ReasoningEngine(self.config)
        self.verification = Verification(self.config)
        self.citation_manager = CitationManager(self.config)
        self.output_generator = OutputGenerator(self.config)
        self.error_handler = ErrorHandler(self.config)
        
        # Session tracking
        self.active_sessions: dict[str, ResearchSession] = {}
        self._session_counter = 0
    
    async def research(
        self,
        query: str,
        audience: AudienceType = AudienceType.GENERAL,
        citation_style: CitationStyle = CitationStyle.APA,
        output_format: OutputFormat = OutputFormat.MARKDOWN,
        max_sources: int = 10,
        verify_claims: bool = True,
        progress_callback: callable | None = None
    ) -> ResearchResult:
        """
        Perform comprehensive research on a query.
        
        Args:
            query: The research query
            audience: Target audience type
            citation_style: Citation style to use
            output_format: Desired output format
            max_sources: Maximum sources to use
            verify_claims: Whether to verify claims
            progress_callback: Optional callback for progress updates
            
        Returns:
            Complete ResearchResult with findings
        """
        # Create session
        session = self._create_session(query)
        
        try:
            # Stage 1: Query Analysis
            await self._run_stage(
                session,
                ResearchStage.QUERY_ANALYSIS,
                self._analyze_query,
                query,
                progress_callback
            )
            
            # Stage 2: Web Search
            await self._run_stage(
                session,
                ResearchStage.WEB_SEARCH,
                self._search_web,
                session,
                max_sources,
                progress_callback
            )
            
            # Stage 3: Reasoning
            await self._run_stage(
                session,
                ResearchStage.REASONING,
                self._reason,
                session,
                progress_callback
            )
            
            # Stage 4: Verification (optional)
            if verify_claims:
                await self._run_stage(
                    session,
                    ResearchStage.VERIFICATION,
                    self._verify,
                    session,
                    progress_callback
                )
            
            # Stage 5: Citation
            await self._run_stage(
                session,
                ResearchStage.CITATION,
                self._generate_citations,
                session,
                citation_style,
                progress_callback
            )
            
            # Stage 6: Output Generation
            await self._run_stage(
                session,
                ResearchStage.OUTPUT_GENERATION,
                self._generate_output,
                session,
                audience,
                progress_callback
            )
            
            # Mark complete
            session.progress.current_stage = ResearchStage.COMPLETE
            if progress_callback:
                progress_callback(ResearchStage.COMPLETE, 100.0)
            
            return session.final_result
            
        except Exception as e:
            logger.error(f"Research failed: {e}")
            
            # Try to generate partial results
            partial_result = await self._handle_research_failure(session, e)
            return partial_result
        
        finally:
            # Clean up session
            self._cleanup_session(session.session_id)
    
    async def _run_stage(
        self,
        session: ResearchSession,
        stage: ResearchStage,
        stage_func: callable,
        *args,
        **kwargs
    ) -> None:
        """Run a research stage with error handling."""
        progress_callback = kwargs.pop('progress_callback', None)
        
        session.progress.current_stage = stage
        start_time = datetime.now()
        
        if progress_callback:
            progress_callback(stage, session.progress.progress_percentage)
        
        logger.info(f"Starting stage: {stage.value}")
        
        try:
            await stage_func(*args)
            duration = (datetime.now() - start_time).total_seconds()
            session.progress.complete_stage(stage, duration)
            logger.info(f"Completed stage: {stage.value} in {duration:.2f}s")
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            session.progress.errors.append(f"{stage.value}: {str(e)}")
            logger.error(f"Stage {stage.value} failed: {e}")
            raise
    
    async def _analyze_query(self, query: str) -> QueryAnalysis:
        """Analyze the research query."""
        session = self._get_current_session(query)
        
        analysis = await self.query_understanding.analyze(query)
        session.query_analysis = analysis
        
        return analysis
    
    async def _search_web(
        self,
        session: ResearchSession,
        max_sources: int
    ) -> list[Source]:
        """Search the web for relevant information."""
        if not session.query_analysis:
            raise ResearchError("Query analysis not available")
        
        # Generate search queries from sub-queries
        all_results = []
        
        for sub_query in session.query_analysis.sub_queries:
            results = await self.web_search.search(
                sub_query.query,
                max_results=max_sources // len(session.query_analysis.sub_queries) + 1
            )
            all_results.extend(results)
        
        # Also search main query
        main_results = await self.web_search.search(
            session.query,
            max_results=max_sources
        )
        all_results.extend(main_results)
        
        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        session.search_results = unique_results[:max_sources]
        
        # Convert to Sources with extracted content
        sources = []
        for result in session.search_results:
            content = await self.web_search.extract_content(result.url)
            source = Source(
                source_id=result.url[:32],
                url=result.url,
                title=result.title,
                content=content.get("main_content", result.snippet),
                domain=result.domain,
                credibility_score=0.7  # Default, will be updated
            )
            sources.append(source)
        
        session.sources = sources
        return sources
    
    async def _reason(self, session: ResearchSession) -> dict:
        """Perform reasoning on gathered information."""
        if not session.sources:
            raise ResearchError("No sources available for reasoning")
        
        # Prepare information for reasoning
        information = [
            {
                "source": source.title,
                "url": source.url,
                "content": source.content[:2000] if source.content else ""
            }
            for source in session.sources
        ]
        
        # Use chain of thought reasoning
        reasoning_result = await self.reasoning_engine.chain_of_thought(
            session.query,
            str(information)
        )
        
        session.reasoning_steps = reasoning_result.get("reasoning_chain", [])
        
        # Synthesize information
        synthesis_result = await self.reasoning_engine.synthesize_information(
            session.query,
            information
        )
        
        session.synthesis = synthesis_result
        
        return synthesis_result
    
    async def _verify(self, session: ResearchSession) -> dict:
        """Verify claims and assess source credibility."""
        if not session.synthesis:
            raise ResearchError("Synthesis not available for verification")
        
        # Extract claims from synthesis
        claims = session.synthesis.get("key_findings", [])
        
        # Verify claims
        verification_result = await self.verification.verify(
            claims,
            session.sources
        )
        
        # Assess source credibility
        for source in session.sources:
            credibility = await self.verification.assess_credibility(source)
            source.credibility_score = credibility.get("overall_score", 0.7)
        
        session.verification = verification_result
        
        return verification_result
    
    async def _generate_citations(
        self,
        session: ResearchSession,
        style: CitationStyle
    ) -> dict:
        """Generate citations for sources."""
        if not session.sources:
            raise ResearchError("No sources available for citation")
        
        synthesis_text = session.synthesis.get("synthesis", "") if session.synthesis else ""
        
        citations = await self.citation_manager.generate_citations(
            session.sources,
            synthesis_text
        )
        
        session.citations = citations
        
        return citations
    
    async def _generate_output(
        self,
        session: ResearchSession,
        audience: AudienceType
    ) -> ResearchResult:
        """Generate the final research output."""
        # Calculate confidence
        confidence = self._calculate_confidence(session)
        
        # Prepare findings
        findings = {
            "synthesis": session.synthesis,
            "verification": session.verification,
            "reasoning_steps": session.reasoning_steps,
            "information_gaps": session.synthesis.get("gaps", []) if session.synthesis else []
        }
        
        # Generate report
        report = await self.output_generator.generate_report(
            session.query,
            findings,
            session.sources,
            confidence
        )
        
        # Generate summary
        summary = await self.output_generator.generate_summary(
            findings,
            SummaryLength.STANDARD
        )
        
        # Build final result
        result = ResearchResult(
            query=session.query,
            answer=summary.get("summary", {}).get("text", ""),
            confidence=confidence,
            sources=session.sources,
            reasoning_steps=session.reasoning_steps,
            verification_status="verified" if session.verification else "unverified",
            metadata={
                "report": report,
                "citations": session.citations,
                "audience": audience.value,
                "session_id": session.session_id,
                "duration": session.progress.stage_times
            }
        )
        
        session.final_result = result
        
        return result
    
    def _calculate_confidence(self, session: ResearchSession) -> float:
        """Calculate overall confidence score."""
        factors = []
        
        # Source quality
        if session.sources:
            avg_credibility = sum(s.credibility_score for s in session.sources) / len(session.sources)
            factors.append(avg_credibility)
        
        # Verification status
        if session.verification:
            verification_score = session.verification.get("overall_confidence", 0.5)
            factors.append(verification_score)
        
        # Source count
        source_score = min(len(session.sources) / 10, 1.0)
        factors.append(source_score)
        
        # Error count
        error_penalty = len(session.progress.errors) * 0.1
        
        if factors:
            base_confidence = sum(factors) / len(factors)
            return max(0.0, min(1.0, base_confidence - error_penalty))
        
        return 0.5
    
    async def _handle_research_failure(
        self,
        session: ResearchSession,
        error: Exception
    ) -> ResearchResult:
        """Handle research failure and generate partial results."""
        logger.warning(f"Generating partial results due to: {error}")
        
        # Try to generate fallback content
        fallback = await self.error_handler.generate_fallback_content(
            session.query,
            session.synthesis,
            [str(error)],
            None
        )
        
        # Build partial result
        return ResearchResult(
            query=session.query,
            answer=fallback.get("fallback_content", {}).get("response", "Research could not be completed."),
            confidence=0.2,
            sources=session.sources,
            reasoning_steps=session.reasoning_steps,
            verification_status="failed",
            metadata={
                "error": str(error),
                "partial": True,
                "fallback": fallback
            }
        )
    
    def _create_session(self, query: str) -> ResearchSession:
        """Create a new research session."""
        self._session_counter += 1
        session_id = f"session_{self._session_counter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        session = ResearchSession(
            session_id=session_id,
            query=query,
            progress=ResearchProgress(current_stage=ResearchStage.QUERY_ANALYSIS)
        )
        
        self.active_sessions[session_id] = session
        return session
    
    def _get_current_session(self, query: str) -> ResearchSession:
        """Get the current session for a query."""
        for session in self.active_sessions.values():
            if session.query == query:
                return session
        raise ResearchError(f"No session found for query: {query}")
    
    def _cleanup_session(self, session_id: str) -> None:
        """Clean up a research session."""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    async def get_session_status(self, session_id: str) -> dict:
        """Get the status of a research session."""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        session = self.active_sessions[session_id]
        return {
            "session_id": session_id,
            "query": session.query,
            "current_stage": session.progress.current_stage.value,
            "progress": session.progress.progress_percentage,
            "stages_completed": [s.value for s in session.progress.stages_completed],
            "errors": session.progress.errors,
            "has_result": session.final_result is not None
        }


# Convenience function for quick research
async def research(query: str, **kwargs) -> ResearchResult:
    """
    Perform research on a query.
    
    This is a convenience function that creates an orchestrator
    and performs research.
    
    Args:
        query: The research query
        **kwargs: Additional arguments for research()
        
    Returns:
        ResearchResult with findings
    """
    orchestrator = ResearchOrchestrator()
    return await orchestrator.research(query, **kwargs)
