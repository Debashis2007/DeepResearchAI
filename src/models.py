"""
Data models for Deep Research AI.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid


class QueryComplexity(Enum):
    """Query complexity levels."""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


class OutputFormat(Enum):
    """Output format options."""
    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"


class CitationStyle(Enum):
    """Citation style options."""
    APA = "APA"
    MLA = "MLA"
    CHICAGO = "CHICAGO"
    IEEE = "IEEE"
    HARVARD = "HARVARD"


@dataclass
class SubQuery:
    """A sub-query derived from the main query."""
    query: str
    purpose: str
    priority: int = 1
    
    
@dataclass
class SearchResult:
    """Search result from web search."""
    title: str
    url: str
    snippet: str
    domain: str
    relevance_score: float = 0.5


@dataclass
class ContentExtraction:
    """Extracted content from a source."""
    main_content: str = ""
    title: str = ""
    author: str = ""
    date: str = ""
    summary: str = ""


@dataclass
class ReasoningStep:
    """A step in the reasoning chain."""
    step_number: int
    thought: str
    evidence: str = ""
    conclusion: str = ""


class ResearchStatus(Enum):
    """Research operation status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class ConfidenceLevel(Enum):
    """Confidence level categories."""
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"


class VerificationStatus(Enum):
    """Verification status for claims."""
    VERIFIED = "verified"
    PARTIALLY_VERIFIED = "partially_verified"
    UNVERIFIED = "unverified"
    DISPUTED = "disputed"


@dataclass
class Entity:
    """Entity extracted from query."""
    name: str = ""
    entity_type: str = ""  # PERSON, ORG, LOCATION, DATE, CONCEPT, PRODUCT, EVENT
    context: Optional[str] = None
    relevance: str = "primary"  # primary, secondary
    
    # Alias for backwards compatibility
    @property
    def text(self) -> str:
        return self.name
    
    @property
    def type(self) -> str:
        return self.entity_type


@dataclass
class QueryAnalysis:
    """Analyzed query structure."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    raw_query: str = ""
    intent: str = ""
    domain: str = ""
    entities: List[Entity] = field(default_factory=list)
    temporal_scope: Optional[str] = None
    geographic_scope: Optional[str] = None
    complexity: QueryComplexity = QueryComplexity.MEDIUM
    output_type: str = "report"
    sub_queries: List["SubQuery"] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Source:
    """Web source information."""
    source_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: str = ""
    title: str = ""
    content: str = ""
    domain: str = ""
    credibility_score: float = 0.5
    snippet: str = ""
    author: Optional[str] = None
    publication_date: Optional[str] = None
    credibility_level: str = "medium"
    retrieved_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Alias for backwards compatibility
    @property
    def id(self) -> str:
        return self.source_id


@dataclass
class ExtractedInfo:
    """Information extracted from a source."""
    source_id: str = ""
    content: str = ""
    info_type: str = ""  # fact, data, quote, claim, context
    relevance: str = "medium"
    location: str = ""


@dataclass
class Claim:
    """A claim extracted from research."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    source_ids: List[str] = field(default_factory=list)
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    confidence_score: float = 0.5
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)


@dataclass
class Finding:
    """A research finding."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    category: str = ""
    confidence_score: float = 0.5
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM
    source_ids: List[str] = field(default_factory=list)
    claims: List[Claim] = field(default_factory=list)
    reasoning_chain: List[str] = field(default_factory=list)
    caveats: List[str] = field(default_factory=list)


@dataclass
class Conflict:
    """Conflicting information from sources."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = ""
    conflict_type: str = ""  # factual, interpretive, temporal, scope
    positions: List[Dict[str, str]] = field(default_factory=list)
    severity: str = "medium"
    resolution: Optional[str] = None


@dataclass
class Citation:
    """A source citation."""
    source_id: str = ""
    style: CitationStyle = CitationStyle.APA
    formatted_citation: str = ""
    in_text_citation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    url: str = ""
    title: str = ""
    author: Optional[str] = None
    date: Optional[str] = None
    formatted: str = ""


@dataclass
class VerificationResult:
    """Result of verification process."""
    overall_confidence: float = 0.5
    trust_level: str = "medium"
    verified_claims: List[Claim] = field(default_factory=list)
    conflicts: List[Conflict] = field(default_factory=list)
    caveats: List[str] = field(default_factory=list)
    flags: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class ResearchResult:
    """Complete research result."""
    query: str = ""
    answer: str = ""
    confidence: float = 0.5
    sources: List[Source] = field(default_factory=list)
    reasoning_steps: List[ReasoningStep] = field(default_factory=list)
    verification_status: str = "unverified"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Legacy fields for backwards compatibility
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: ResearchStatus = ResearchStatus.PENDING
    summary: str = ""
    findings: List[Finding] = field(default_factory=list)
    citations: List[Citation] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ResearchRequest:
    """Incoming research request."""
    query: str
    mode: str = "standard"  # quick, standard, deep
    max_sources: int = 10
    output_format: str = "markdown"
    include_sources: bool = True
    domain_hint: Optional[str] = None
