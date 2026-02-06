"""
Verification prompts for validating research findings.
"""

VERIFICATION_PROMPTS = {
    "cross_reference": """You are a fact-checking specialist. Cross-reference the following claims against multiple sources.

## Claims to Verify
{claims}

## Available Sources
{sources}

## Instructions
For each claim:

1. **Find Corroboration**: Which sources support this claim?
2. **Find Contradiction**: Which sources contradict this claim?
3. **Assess Agreement Level**: How many sources agree?
4. **Identify Source of Truth**: Which source is most authoritative?

## Verification Standards
- Claim verified: 2+ independent sources agree
- Claim disputed: Sources conflict
- Claim unverified: Only 1 source or no corroboration

## Output Format
{{
  "verified_claims": [
    {{
      "claim": "The claim text",
      "status": "verified|disputed|unverified",
      "supporting_sources": [
        {{"source": "url", "quote": "supporting text"}}
      ],
      "contradicting_sources": [
        {{"source": "url", "quote": "contradicting text"}}
      ],
      "confidence": 0.85,
      "notes": "Additional context"
    }}
  ],
  "verification_summary": {{
    "total_claims": 10,
    "verified": 7,
    "disputed": 2,
    "unverified": 1
  }}
}}""",

    "credibility_assessment": """You are a source credibility evaluator. Assess the trustworthiness of these sources.

## Sources to Evaluate
{sources}

## Instructions
Evaluate each source on:

1. **Domain Authority**: Is the domain/publication reputable?
2. **Author Credentials**: Is the author qualified?
3. **Publication Date**: Is the information current?
4. **Bias Indicators**: Are there signs of bias?
5. **Citation Quality**: Does the source cite its own sources?
6. **Content Quality**: Is the content well-researched?

## Credibility Indicators
- **High**: Government (.gov), Academic (.edu), established publications
- **Medium**: Established news outlets, professional organizations
- **Low**: Personal blogs, unknown sources, content farms
- **Unknown**: Cannot determine credibility

## Output Format
{{
  "source_assessments": [
    {{
      "url": "source url",
      "domain": "domain name",
      "credibility_score": 85,
      "credibility_level": "high|medium|low|unknown",
      "factors": {{
        "domain_authority": {{"score": 80, "reason": "string"}},
        "author_credentials": {{"score": 70, "reason": "string"}},
        "freshness": {{"score": 90, "publication_date": "date"}},
        "bias_level": {{"score": 85, "direction": "neutral"}},
        "citation_quality": {{"score": 75, "reason": "string"}}
      }},
      "red_flags": ["Any concerning indicators"],
      "recommendation": "use|use_with_caution|avoid"
    }}
  ],
  "overall_source_quality": "Assessment of source pool quality"
}}""",

    "conflict_detection": """You are a conflict detection specialist. Identify conflicts and contradictions in the research findings.

## Research Findings
{findings}

## Sources
{sources}

## Instructions
Detect and analyze conflicts:

1. **Identify Contradictions**: Find statements that contradict each other
2. **Classify Conflict Type**: Factual, interpretive, or temporal
3. **Analyze Root Cause**: Why might sources disagree?
4. **Suggest Resolution**: How to resolve or present the conflict

## Conflict Types
- **Factual**: Different facts stated (e.g., different numbers)
- **Interpretive**: Same facts, different conclusions
- **Temporal**: Information from different time periods
- **Scope**: Different scope or definitions used

## Output Format
{{
  "conflicts_detected": [
    {{
      "id": "conflict_1",
      "topic": "What the conflict is about",
      "type": "factual|interpretive|temporal|scope",
      "positions": [
        {{
          "source": "source url",
          "claim": "What this source says",
          "evidence": "Supporting quote or data"
        }}
      ],
      "severity": "high|medium|low",
      "root_cause": "Why sources might disagree",
      "resolution": {{
        "approach": "favor_authoritative|present_both|synthesize|flag_uncertain",
        "recommendation": "How to handle this conflict",
        "resolved_statement": "Suggested resolved statement if applicable"
      }}
    }}
  ],
  "conflict_free_claims": ["Claims with no conflicts"],
  "overall_consistency": 75
}}""",

    "fact_check": """You are a professional fact-checker. Verify the accuracy of these specific claims.

## Claims to Fact-Check
{claims}

## Context
{context}

## Available Evidence
{evidence}

## Instructions
For each claim:

1. **Identify Checkable Elements**: What specific facts can be verified?
2. **Find Evidence**: What evidence supports or refutes the claim?
3. **Rate Accuracy**: How accurate is the claim?
4. **Provide Correction**: If inaccurate, what is correct?

## Accuracy Ratings
- **True**: Claim is accurate and supported by evidence
- **Mostly True**: Claim is largely accurate with minor issues
- **Half True**: Claim has accurate and inaccurate elements
- **Mostly False**: Claim has significant inaccuracies
- **False**: Claim is inaccurate
- **Unverifiable**: Cannot determine accuracy

## Output Format
{{
  "fact_checks": [
    {{
      "claim": "The claim being checked",
      "checkable_elements": ["Specific facts to verify"],
      "verdict": "true|mostly_true|half_true|mostly_false|false|unverifiable",
      "evidence": [
        {{
          "source": "source url",
          "supports": true,
          "quote": "relevant quote"
        }}
      ],
      "explanation": "Why this verdict",
      "correction": "Correct information if claim is false",
      "confidence": 0.85
    }}
  ],
  "summary": {{
    "true_claims": 5,
    "false_claims": 2,
    "unverifiable_claims": 1
  }}
}}""",

    "uncertainty_flagging": """You are an uncertainty analyst. Identify claims that cannot be fully verified or have significant uncertainty.

## Research Findings
{findings}

## Sources
{sources}

## Instructions
Identify uncertainty by looking for:

1. **Single Source Claims**: Claims from only one source
2. **Speculative Language**: "might", "could", "possibly"
3. **Outdated Information**: Old data that may not be current
4. **Expert Disagreement**: Areas where experts disagree
5. **Missing Evidence**: Claims without supporting evidence
6. **Emerging Topics**: Areas where knowledge is evolving

## Output Format
{{
  "uncertain_claims": [
    {{
      "claim": "The uncertain claim",
      "uncertainty_type": "single_source|speculative|outdated|disputed|unsupported|emerging",
      "uncertainty_level": "high|medium|low",
      "reason": "Why this is uncertain",
      "available_evidence": "What evidence exists",
      "recommendation": "How to present this claim"
    }}
  ],
  "confidence_adjustments": [
    {{
      "finding": "Original finding",
      "original_confidence": 0.8,
      "adjusted_confidence": 0.6,
      "reason": "Why confidence was adjusted"
    }}
  ],
  "caveats_to_include": ["Caveats that should be mentioned in output"]
}}""",

    "bias_detection": """You are a bias detection specialist. Analyze these sources and findings for potential biases.

## Sources
{sources}

## Findings
{findings}

## Instructions
Check for:

1. **Source Bias**: Does the source have a known perspective or agenda?
2. **Selection Bias**: Are we missing important perspectives?
3. **Confirmation Bias**: Are findings skewed toward a particular conclusion?
4. **Recency Bias**: Over-reliance on recent information?
5. **Geographic Bias**: Over-representation of certain regions?
6. **Language Bias**: Loaded or emotional language?

## Output Format
{{
  "biases_detected": [
    {{
      "bias_type": "source|selection|confirmation|recency|geographic|language",
      "description": "What the bias is",
      "severity": "high|medium|low",
      "affected_findings": ["Which findings are affected"],
      "mitigation": "How to address this bias"
    }}
  ],
  "missing_perspectives": [
    {{
      "perspective": "What viewpoint is missing",
      "importance": "high|medium|low",
      "suggested_sources": ["Types of sources that would help"]
    }}
  ],
  "balance_assessment": {{
    "is_balanced": true,
    "skew_direction": "Direction of any skew",
    "recommendations": ["How to improve balance"]
  }}
}}""",

    "verification_summary": """You are a verification summarizer. Create a comprehensive verification summary for the research findings.

## Original Findings
{findings}

## Verification Results
Cross-reference: {cross_reference_results}
Credibility: {credibility_results}
Conflicts: {conflict_results}
Uncertainty: {uncertainty_results}

## Instructions
Create a comprehensive verification summary that:

1. **Overall Assessment**: How trustworthy are the findings?
2. **Verified Findings**: What can be stated with confidence?
3. **Caveats**: What limitations should be noted?
4. **Flags**: What needs user attention?

## Output Format
{{
  "verification_summary": {{
    "overall_confidence": 0.75,
    "trust_level": "high|medium|low",
    "verification_completeness": 85
  }},
  "verified_findings": [
    {{
      "finding": "string",
      "confidence": 0.85,
      "verification_status": "verified|partially_verified|unverified"
    }}
  ],
  "caveats": ["Important caveats for the user"],
  "flags": [
    {{
      "type": "conflict|bias|uncertainty|credibility",
      "message": "What the user should know",
      "severity": "high|medium|low"
    }}
  ],
  "recommendations": ["Recommendations for improving research quality"]
}}"""
}
