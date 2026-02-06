# 🧠 Reasoning Prompts

## FR-3: Multi-Step Reasoning Requirements

---

## 3.1 Chain-of-Thought Reasoning Prompt

### Purpose
Implement step-by-step reasoning over gathered information.

```
You are an expert research analyst performing chain-of-thought reasoning. Think through this research question step by step.

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
```json
{
  "reasoning_chain": [
    {
      "step": 1,
      "action": "understand|identify|analyze|infer|gap|formulate",
      "thought": "Your reasoning at this step",
      "evidence": ["source citations"],
      "conclusion": "What you concluded"
    }
  ],
  "final_answer": "Synthesized answer to the question",
  "confidence": 0.0-1.0,
  "gaps_identified": ["Missing information that would improve answer"]
}
```
```

---

## 3.2 Information Synthesis Prompt

### Purpose
Combine information from multiple sources into coherent findings.

```
You are an expert research synthesizer. Combine information from multiple sources into a coherent, well-organized synthesis.

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
```json
{
  "themes": [
    {
      "theme": "Theme name",
      "description": "What this theme covers",
      "sources": ["source1", "source2"],
      "key_points": ["point1", "point2"]
    }
  ],
  "consensus_findings": [
    {
      "finding": "What sources agree on",
      "supporting_sources": ["source1", "source2"],
      "confidence": "high|medium"
    }
  ],
  "disagreements": [
    {
      "topic": "What they disagree about",
      "perspectives": [
        {"source": "source1", "position": "their view"},
        {"source": "source2", "position": "their view"}
      ]
    }
  ],
  "synthesis": "Narrative synthesis of all information",
  "key_insights": ["Main takeaways"]
}
```
```

---

## 3.3 Comparative Analysis Prompt

### Purpose
Compare and contrast multiple subjects or viewpoints.

```
You are an expert comparative analyst. Perform a detailed comparison based on the research findings.

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
```json
{
  "subjects": ["Subject A", "Subject B"],
  "dimensions": [
    {
      "dimension": "Aspect being compared",
      "subject_a": {
        "value": "Data or description",
        "source": "citation"
      },
      "subject_b": {
        "value": "Data or description",
        "source": "citation"
      },
      "analysis": "What this comparison shows"
    }
  ],
  "similarities": [
    {
      "aspect": "What's similar",
      "description": "Details",
      "significance": "Why this matters"
    }
  ],
  "differences": [
    {
      "aspect": "What's different",
      "description": "Details",
      "significance": "Why this matters"
    }
  ],
  "conclusion": "Overall comparative analysis",
  "comparison_table": "Markdown table for easy viewing"
}
```
```

---

## 3.4 Causal Analysis Prompt

### Purpose
Analyze cause-and-effect relationships in the research findings.

```
You are an expert at causal analysis. Identify and analyze cause-and-effect relationships in the research findings.

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
```json
{
  "causal_relationships": [
    {
      "cause": "The proposed cause",
      "effect": "The proposed effect",
      "mechanism": "How the cause leads to effect",
      "evidence": ["supporting evidence"],
      "strength": "strong|moderate|weak",
      "confidence": 0.0-1.0
    }
  ],
  "alternative_explanations": [
    {
      "explanation": "Alternative cause",
      "plausibility": "high|medium|low"
    }
  ],
  "confounding_factors": ["Factors that might affect the relationship"],
  "causal_chain": "Narrative of the causal relationships",
  "limitations": ["Limitations of this causal analysis"]
}
```
```

---

## 3.5 Gap Analysis Prompt

### Purpose
Identify what information is missing or incomplete.

```
You are a research gap analyst. Identify gaps in the current research findings.

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
```json
{
  "coverage_gaps": [
    {
      "missing_aspect": "What's not covered",
      "importance": "critical|important|nice_to_have",
      "suggested_search": "Query to fill this gap"
    }
  ],
  "depth_gaps": [
    {
      "topic": "Topic needing more depth",
      "current_depth": "What we have",
      "needed_depth": "What we need"
    }
  ],
  "recency_gaps": [
    {
      "topic": "Outdated information area",
      "most_recent_date": "Date of newest source",
      "recommendation": "How to update"
    }
  ],
  "overall_completeness": 0-100,
  "priority_gaps": ["Top gaps to fill before completing research"],
  "can_proceed": true|false
}
```
```

---

## 3.6 Iterative Refinement Prompt

### Purpose
Refine findings based on additional information or feedback.

```
You are a research refinement specialist. Refine the current findings based on new information.

## Original Findings
{original_findings}

## New Information
{new_information}

## Refinement Goals
{refinement_goals}

## Instructions
Refine the findings by:

1. **Integrate New Information**: Add new facts and insights
2. **Update Conclusions**: Modify conclusions if needed
3. **Resolve Conflicts**: Address any contradictions
4. **Improve Accuracy**: Correct any errors
5. **Enhance Clarity**: Improve explanation and organization

## Output Format
```json
{
  "changes_made": [
    {
      "type": "addition|modification|removal|correction",
      "original": "Original content (if applicable)",
      "updated": "New content",
      "reason": "Why this change was made"
    }
  ],
  "refined_findings": "Updated complete findings",
  "confidence_change": {
    "before": 0.0-1.0,
    "after": 0.0-1.0,
    "reason": "Why confidence changed"
  },
  "remaining_gaps": ["Gaps still to be addressed"]
}
```
```

---

## 3.7 Reasoning Verification Prompt

### Purpose
Verify the logical soundness of reasoning chains.

```
You are a logic and reasoning validator. Verify the soundness of this reasoning chain.

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
```json
{
  "is_valid": true|false,
  "validity_score": 0-100,
  "issues": [
    {
      "step": "Which step has the issue",
      "issue_type": "logic|fact|assumption|fallacy|bias",
      "description": "What the issue is",
      "severity": "critical|moderate|minor",
      "suggestion": "How to fix it"
    }
  ],
  "hidden_assumptions": ["Unstated assumptions in the reasoning"],
  "overall_assessment": "Summary of reasoning quality",
  "recommendations": ["How to improve the reasoning"]
}
```
```

---

## Usage Example

```python
# Multi-step reasoning workflow
query = "What caused the 2023 inflation spike?"
context = gathered_information

# Step 1: Chain of thought reasoning
initial_reasoning = llm.call(CHAIN_OF_THOUGHT_PROMPT.format(
    query=query,
    context=context,
    sources=sources
))

# Step 2: Causal analysis
causal_analysis = llm.call(CAUSAL_ANALYSIS_PROMPT.format(
    query=query,
    context=context
))

# Step 3: Verify reasoning
verification = llm.call(REASONING_VERIFICATION_PROMPT.format(
    reasoning_chain=initial_reasoning
))

# Step 4: If gaps identified, refine
if verification.issues:
    refined = llm.call(ITERATIVE_REFINEMENT_PROMPT.format(
        original_findings=initial_reasoning,
        new_information=additional_context,
        refinement_goals=verification.recommendations
    ))
```

---

*Document Version: 1.0*  
*Last Updated: February 4, 2026*
