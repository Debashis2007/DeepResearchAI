"""
Reasoning prompts for multi-step analysis.
"""

REASONING_PROMPTS = {
    "chain_of_thought": """You are an expert research analyst performing chain-of-thought reasoning. Think through this research question step by step.

## Research Question
{query}

## Gathered Information
{context}

## Sources
{sources}

## Instructions
Reason through this step by step:

1. **Understand the Question**: What exactly is being asked?
2. **Identify Key Information**: What relevant facts do we have?
3. **Analyze Relationships**: How do the pieces of information connect?
4. **Draw Inferences**: What can we conclude from the evidence?
5. **Identify Gaps**: What information is missing?
6. **Formulate Answer**: What is the best answer based on available evidence?

## Rules
- Show your reasoning explicitly
- Cite sources for each claim
- Acknowledge uncertainty when present
- Distinguish facts from inferences

## Output Format
{{
  "reasoning_chain": [
    {{
      "step": 1,
      "action": "understand|identify|analyze|infer|gap|formulate",
      "thought": "Your reasoning at this step",
      "evidence": ["source citations"],
      "conclusion": "What you concluded"
    }}
  ],
  "final_answer": "Synthesized answer to the question",
  "confidence": 0.85,
  "gaps_identified": ["Missing information that would improve answer"]
}}""",

    "synthesis": """You are an expert research synthesizer. Combine information from multiple sources into a coherent, well-organized synthesis.

## Research Question
{query}

## Source Information
{sources_with_content}

## Instructions
Synthesize the information by:

1. **Identifying Common Themes**: What topics appear across multiple sources?
2. **Finding Consensus**: Where do sources agree?
3. **Noting Disagreements**: Where do sources conflict?
4. **Filling Gaps**: How do sources complement each other?
5. **Building Narrative**: Create a coherent story from the pieces

## Synthesis Rules
- Prioritize information from multiple corroborating sources
- Clearly attribute claims to sources
- Present balanced view when sources disagree
- Do not add information not present in sources

## Output Format
{{
  "themes": [
    {{
      "theme": "Theme name",
      "description": "What this theme covers",
      "sources": ["source1", "source2"],
      "key_points": ["point1", "point2"]
    }}
  ],
  "consensus_findings": [
    {{
      "finding": "What sources agree on",
      "supporting_sources": ["source1", "source2"],
      "confidence": "high|medium"
    }}
  ],
  "disagreements": [
    {{
      "topic": "What they disagree about",
      "perspectives": [
        {{"source": "source1", "position": "their view"}},
        {{"source": "source2", "position": "their view"}}
      ]
    }}
  ],
  "synthesis": "Narrative synthesis of all information",
  "key_insights": ["Main takeaways"]
}}""",

    "comparative_analysis": """You are an expert comparative analyst. Perform a detailed comparison based on the research findings.

## Comparison Query
{query}

## Subjects to Compare
{subjects}

## Gathered Information
{context}

## Instructions
Create a structured comparison:

1. **Identify Comparison Dimensions**: What aspects should be compared?
2. **Extract Data Points**: Find comparable data for each subject
3. **Analyze Similarities**: Where are the subjects alike?
4. **Analyze Differences**: Where do they differ?
5. **Draw Conclusions**: What does the comparison reveal?

## Output Format
{{
  "subjects": ["Subject A", "Subject B"],
  "dimensions": [
    {{
      "dimension": "Aspect being compared",
      "subject_a": {{
        "value": "Data or description",
        "source": "citation"
      }},
      "subject_b": {{
        "value": "Data or description",
        "source": "citation"
      }},
      "analysis": "What this comparison shows"
    }}
  ],
  "similarities": [
    {{
      "aspect": "What's similar",
      "description": "Details",
      "significance": "Why this matters"
    }}
  ],
  "differences": [
    {{
      "aspect": "What's different",
      "description": "Details",
      "significance": "Why this matters"
    }}
  ],
  "conclusion": "Overall comparative analysis"
}}""",

    "causal_analysis": """You are an expert at causal analysis. Identify and analyze cause-and-effect relationships in the research findings.

## Research Question
{query}

## Context
{context}

## Instructions
Perform causal analysis:

1. **Identify Potential Causes**: What factors might cause the phenomenon?
2. **Identify Effects**: What are the outcomes or consequences?
3. **Establish Relationships**: How do causes link to effects?
4. **Evaluate Evidence**: How strong is the evidence for each causal claim?
5. **Consider Alternatives**: What other explanations exist?

## Causal Reasoning Rules
- Correlation does not imply causation
- Consider confounding variables
- Look for temporal ordering (cause before effect)
- Seek multiple sources of evidence

## Output Format
{{
  "causal_relationships": [
    {{
      "cause": "The proposed cause",
      "effect": "The proposed effect",
      "mechanism": "How the cause leads to effect",
      "evidence": ["supporting evidence"],
      "strength": "strong|moderate|weak",
      "confidence": 0.75
    }}
  ],
  "alternative_explanations": [
    {{
      "explanation": "Alternative cause",
      "plausibility": "high|medium|low"
    }}
  ],
  "confounding_factors": ["Factors that might affect the relationship"],
  "causal_chain": "Narrative of the causal relationships",
  "limitations": ["Limitations of this causal analysis"]
}}""",

    "gap_analysis": """You are a research gap analyst. Identify gaps in the current research findings.

## Research Question
{query}

## Current Findings
{findings}

## Sources Consulted
{sources}

## Instructions
Analyze gaps in the research:

1. **Coverage Gaps**: What aspects of the question aren't addressed?
2. **Depth Gaps**: Where is information superficial?
3. **Recency Gaps**: Is information outdated?
4. **Source Gaps**: Are important source types missing?
5. **Perspective Gaps**: Are viewpoints underrepresented?

## Output Format
{{
  "coverage_gaps": [
    {{
      "missing_aspect": "What's not covered",
      "importance": "critical|important|nice_to_have",
      "suggested_search": "Query to fill this gap"
    }}
  ],
  "depth_gaps": [
    {{
      "topic": "Topic needing more depth",
      "current_depth": "What we have",
      "needed_depth": "What we need"
    }}
  ],
  "recency_gaps": [
    {{
      "topic": "Outdated information area",
      "most_recent_date": "Date of newest source",
      "recommendation": "How to update"
    }}
  ],
  "overall_completeness": 75,
  "priority_gaps": ["Top gaps to fill before completing research"],
  "can_proceed": true
}}""",

    "reasoning_verification": """You are a logic and reasoning validator. Verify the soundness of this reasoning chain.

## Reasoning Chain
{reasoning_chain}

## Instructions
Check for:

1. **Logical Validity**: Do conclusions follow from premises?
2. **Factual Accuracy**: Are stated facts correct?
3. **Hidden Assumptions**: Are there unstated assumptions?
4. **Logical Fallacies**: Are there reasoning errors?
5. **Bias Detection**: Are there signs of bias?

## Common Fallacies to Check
- Hasty generalization
- False causation
- Appeal to authority (without merit)
- Cherry picking
- Circular reasoning

## Output Format
{{
  "is_valid": true,
  "validity_score": 85,
  "issues": [
    {{
      "step": "Which step has the issue",
      "issue_type": "logic|fact|assumption|fallacy|bias",
      "description": "What the issue is",
      "severity": "critical|moderate|minor",
      "suggestion": "How to fix it"
    }}
  ],
  "hidden_assumptions": ["Unstated assumptions in the reasoning"],
  "overall_assessment": "Summary of reasoning quality",
  "recommendations": ["How to improve the reasoning"]
}}"""
}
