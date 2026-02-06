"""
Verification Module - Validates and verifies research findings.
"""

import logging
import json
from typing import Optional, Dict, Any, List

from ..models import (
    Source, Finding, Claim, VerificationResult, Conflict,
    VerificationStatus, ConfidenceLevel
)
from ..llm_client import llm_client
from ..prompts.verification_prompts import VERIFICATION_PROMPTS

logger = logging.getLogger(__name__)


class VerificationModule:
    """
    Verification module for validating research findings.
    
    Implements FR-4: Source Verification requirements.
    """
    
    def __init__(self):
        self.llm = llm_client
    
    async def verify(
        self,
        findings: List[Finding],
        sources: List[Source]
    ) -> VerificationResult:
        """
        Verify research findings against sources.
        
        Args:
            findings: List of findings to verify
            sources: List of sources used
            
        Returns:
            VerificationResult with verification details
        """
        logger.info(f"Verifying {len(findings)} findings against {len(sources)} sources")
        
        # Extract claims from findings
        all_claims = self._extract_claims(findings)
        
        # Cross-reference claims
        cross_ref_result = await self._cross_reference(all_claims, sources)
        
        # Assess source credibility
        credibility_result = await self._assess_credibility(sources)
        
        # Detect conflicts
        conflict_result = await self._detect_conflicts(findings, sources)
        
        # Flag uncertainties
        uncertainty_result = await self._flag_uncertainties(findings, sources)
        
        # Detect biases
        bias_result = await self._detect_bias(findings, sources)
        
        # Generate verification summary
        verification = await self._generate_summary(
            findings,
            cross_ref_result,
            credibility_result,
            conflict_result,
            uncertainty_result
        )
        
        # Update claims with verification status
        self._update_claim_status(all_claims, cross_ref_result)
        
        # Build verification result
        result = self._build_verification_result(
            findings,
            all_claims,
            conflict_result,
            verification
        )
        
        logger.info(f"Verification complete. Overall confidence: {result.overall_confidence:.2f}")
        return result
    
    async def _cross_reference(
        self,
        claims: List[Claim],
        sources: List[Source]
    ) -> Dict[str, Any]:
        """Cross-reference claims against sources."""
        claims_data = [
            {"id": c.id, "content": c.content}
            for c in claims
        ]
        
        sources_data = [
            {
                "url": s.url,
                "title": s.title,
                "content": s.content[:2000] if s.content else s.snippet,
                "credibility": s.credibility_level
            }
            for s in sources
        ]
        
        prompt = VERIFICATION_PROMPTS["cross_reference"].format(
            claims=json.dumps(claims_data, indent=2),
            sources=json.dumps(sources_data, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Cross-reference failed: {e}")
            return {"verified_claims": [], "verification_summary": {}}
    
    async def _assess_credibility(
        self,
        sources: List[Source]
    ) -> Dict[str, Any]:
        """Assess the credibility of sources."""
        sources_data = [
            {
                "url": s.url,
                "title": s.title,
                "domain": s.domain,
                "author": s.author,
                "publication_date": s.publication_date,
                "snippet": s.snippet[:500] if s.snippet else ""
            }
            for s in sources
        ]
        
        prompt = VERIFICATION_PROMPTS["credibility_assessment"].format(
            sources=json.dumps(sources_data, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            
            # Update source credibility scores
            assessments = {a["url"]: a for a in result.get("source_assessments", [])}
            for source in sources:
                if source.url in assessments:
                    assessment = assessments[source.url]
                    source.credibility_score = assessment.get("credibility_score", 50) / 100
                    source.credibility_level = assessment.get("credibility_level", "medium")
            
            return result
        except Exception as e:
            logger.error(f"Credibility assessment failed: {e}")
            return {"source_assessments": []}
    
    async def _detect_conflicts(
        self,
        findings: List[Finding],
        sources: List[Source]
    ) -> Dict[str, Any]:
        """Detect conflicts in findings."""
        findings_data = [
            {"title": f.title, "content": f.content}
            for f in findings
        ]
        
        sources_data = [
            {
                "url": s.url,
                "title": s.title,
                "content": s.content[:1500] if s.content else s.snippet
            }
            for s in sources
        ]
        
        prompt = VERIFICATION_PROMPTS["conflict_detection"].format(
            findings=json.dumps(findings_data, indent=2),
            sources=json.dumps(sources_data, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Conflict detection failed: {e}")
            return {"conflicts_detected": [], "overall_consistency": 75}
    
    async def _flag_uncertainties(
        self,
        findings: List[Finding],
        sources: List[Source]
    ) -> Dict[str, Any]:
        """Flag uncertain claims."""
        findings_data = [
            {"title": f.title, "content": f.content, "confidence": f.confidence_score}
            for f in findings
        ]
        
        sources_data = [
            {"url": s.url, "title": s.title}
            for s in sources
        ]
        
        prompt = VERIFICATION_PROMPTS["uncertainty_flagging"].format(
            findings=json.dumps(findings_data, indent=2),
            sources=json.dumps(sources_data, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Uncertainty flagging failed: {e}")
            return {"uncertain_claims": [], "caveats_to_include": []}
    
    async def _detect_bias(
        self,
        findings: List[Finding],
        sources: List[Source]
    ) -> Dict[str, Any]:
        """Detect potential biases."""
        findings_data = [
            {"title": f.title, "content": f.content}
            for f in findings
        ]
        
        sources_data = [
            {"url": s.url, "domain": s.domain, "title": s.title}
            for s in sources
        ]
        
        prompt = VERIFICATION_PROMPTS["bias_detection"].format(
            findings=json.dumps(findings_data, indent=2),
            sources=json.dumps(sources_data, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Bias detection failed: {e}")
            return {"biases_detected": [], "balance_assessment": {"is_balanced": True}}
    
    async def _generate_summary(
        self,
        findings: List[Finding],
        cross_ref: Dict[str, Any],
        credibility: Dict[str, Any],
        conflicts: Dict[str, Any],
        uncertainty: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate verification summary."""
        findings_data = [
            {"title": f.title, "content": f.content[:500]}
            for f in findings
        ]
        
        prompt = VERIFICATION_PROMPTS["verification_summary"].format(
            findings=json.dumps(findings_data, indent=2),
            cross_reference_results=json.dumps(cross_ref.get("verification_summary", {})),
            credibility_results=json.dumps(credibility.get("overall_source_quality", "medium")),
            conflict_results=json.dumps({"count": len(conflicts.get("conflicts_detected", []))}),
            uncertainty_results=json.dumps({"caveats": uncertainty.get("caveats_to_include", [])})
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Verification summary failed: {e}")
            return {
                "verification_summary": {
                    "overall_confidence": 0.7,
                    "trust_level": "medium"
                },
                "caveats": [],
                "flags": []
            }
    
    async def fact_check(
        self,
        claims: List[str],
        context: str,
        evidence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Perform fact-checking on specific claims."""
        prompt = VERIFICATION_PROMPTS["fact_check"].format(
            claims=json.dumps(claims, indent=2),
            context=context,
            evidence=json.dumps(evidence, indent=2)
        )
        
        try:
            result = await self.llm.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Fact check failed: {e}")
            return {"fact_checks": []}
    
    def _extract_claims(self, findings: List[Finding]) -> List[Claim]:
        """Extract all claims from findings."""
        claims = []
        
        for finding in findings:
            # Add existing claims
            claims.extend(finding.claims)
            
            # Create a claim from the finding content if no claims exist
            if not finding.claims:
                claim = Claim(
                    content=finding.content,
                    source_ids=finding.source_ids,
                    confidence_score=finding.confidence_score
                )
                claims.append(claim)
                finding.claims.append(claim)
        
        return claims
    
    def _update_claim_status(
        self,
        claims: List[Claim],
        cross_ref_result: Dict[str, Any]
    ):
        """Update claim verification status based on cross-reference results."""
        verified_claims = {
            vc.get("claim", ""): vc
            for vc in cross_ref_result.get("verified_claims", [])
        }
        
        for claim in claims:
            # Find matching verified claim
            for claim_text, vc in verified_claims.items():
                if claim.content in claim_text or claim_text in claim.content:
                    status = vc.get("status", "unverified")
                    
                    if status == "verified":
                        claim.verification_status = VerificationStatus.VERIFIED
                    elif status == "disputed":
                        claim.verification_status = VerificationStatus.DISPUTED
                    else:
                        claim.verification_status = VerificationStatus.UNVERIFIED
                    
                    claim.confidence_score = vc.get("confidence", claim.confidence_score)
                    
                    # Add supporting evidence
                    for support in vc.get("supporting_sources", []):
                        claim.supporting_evidence.append(support.get("quote", ""))
                    
                    # Add contradicting evidence
                    for contra in vc.get("contradicting_sources", []):
                        claim.contradicting_evidence.append(contra.get("quote", ""))
                    
                    break
    
    def _build_verification_result(
        self,
        findings: List[Finding],
        claims: List[Claim],
        conflict_result: Dict[str, Any],
        verification_summary: Dict[str, Any]
    ) -> VerificationResult:
        """Build the final verification result."""
        summary = verification_summary.get("verification_summary", {})
        
        # Build conflicts
        conflicts = []
        for conflict_data in conflict_result.get("conflicts_detected", []):
            conflict = Conflict(
                topic=conflict_data.get("topic", ""),
                conflict_type=conflict_data.get("type", "factual"),
                positions=conflict_data.get("positions", []),
                severity=conflict_data.get("severity", "medium"),
                resolution=conflict_data.get("resolution", {}).get("resolved_statement")
            )
            conflicts.append(conflict)
        
        # Build flags
        flags = []
        for flag in verification_summary.get("flags", []):
            flags.append({
                "type": flag.get("type", "uncertainty"),
                "message": flag.get("message", ""),
                "severity": flag.get("severity", "medium")
            })
        
        return VerificationResult(
            overall_confidence=summary.get("overall_confidence", 0.7),
            trust_level=summary.get("trust_level", "medium"),
            verified_claims=claims,
            conflicts=conflicts,
            caveats=verification_summary.get("caveats", []),
            flags=flags
        )


# Module instance
verification_module = VerificationModule()
