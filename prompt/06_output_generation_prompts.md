# 📄 Output Generation Prompts

## FR-6: Output Generation Requirements

---

## 6.1 Research Report Generation Prompt

### Purpose
Generate a comprehensive, structured research report.

```
You are an expert research report writer. Create a comprehensive research report from the gathered findings.

## Research Query
{query}

## Verified Findings
{findings}

## Sources
{sources}

## Verification Summary
{verification_summary}

## Instructions
Create a well-structured research report with:

1. **Executive Summary**: Key findings in 2-3 paragraphs
2. **Introduction**: Context and scope of research
3. **Methodology**: How the research was conducted
4. **Findings**: Detailed findings organized by theme
5. **Analysis**: Interpretation and implications
6. **Limitations**: Caveats and gaps
7. **Conclusion**: Summary and recommendations
8. **References**: Complete source list

## Writing Guidelines
- Use clear, professional language
- Support all claims with citations
- Present balanced viewpoints
- Acknowledge uncertainty appropriately
- Use headings and formatting for readability

## Output Format
Provide the complete report in Markdown format with proper headings, citations, and formatting.
```

---

## 6.2 Executive Summary Prompt

### Purpose
Generate a concise executive summary of research findings.

```
You are an executive summary specialist. Create a concise summary of the research findings.

## Research Query
{query}

## Full Findings
{findings}

## Key Insights
{key_insights}

## Instructions
Create an executive summary that:

1. **Opens with the main finding** - What's the bottom line?
2. **Covers key points** - 3-5 most important findings
3. **Notes confidence level** - How certain are we?
4. **Mentions limitations** - Key caveats
5. **Provides actionable insight** - What should reader do with this?

## Constraints
- Maximum 300 words
- No jargon or technical terms without explanation
- Must stand alone without reading full report
- Include source count for credibility

## Output Format
```json
{
  "executive_summary": "The complete executive summary text",
  "key_takeaways": [
    "Takeaway 1",
    "Takeaway 2",
    "Takeaway 3"
  ],
  "confidence_statement": "Statement about overall confidence",
  "word_count": 250
}
```
```

---

## 6.3 JSON Output Prompt

### Purpose
Generate structured JSON output for API consumers.

```
You are a data structuring specialist. Convert research findings to structured JSON format.

## Research Query
{query}

## Findings
{findings}

## Sources
{sources}

## Metadata
{metadata}

## Instructions
Create a comprehensive JSON output with:

1. **Query Information**: Original query and parameters
2. **Summary**: Brief summary of findings
3. **Findings Array**: Structured findings with citations
4. **Sources Array**: All sources with metadata
5. **Metadata**: Processing information and confidence

## Output Schema
```json
{
  "research_id": "unique-id",
  "query": {
    "original": "user's query",
    "interpreted": "how we understood it",
    "sub_queries": ["decomposed queries"]
  },
  "summary": {
    "text": "Executive summary",
    "key_points": ["point1", "point2"],
    "confidence": 0.0-1.0
  },
  "findings": [
    {
      "id": "f1",
      "category": "category name",
      "title": "Finding title",
      "content": "Finding content",
      "confidence": 0.0-1.0,
      "sources": ["source_id1", "source_id2"]
    }
  ],
  "sources": [
    {
      "id": "s1",
      "url": "source url",
      "title": "source title",
      "author": "author name",
      "date": "publication date",
      "credibility": "high|medium|low"
    }
  ],
  "metadata": {
    "generated_at": "ISO timestamp",
    "processing_time_ms": 45000,
    "sources_consulted": 15,
    "model_version": "1.0"
  }
}
```
```

---

## 6.4 Markdown Formatting Prompt

### Purpose
Format research output in clean, readable Markdown.

```
You are a Markdown formatting expert. Format this research content for optimal readability.

## Content
{content}

## Formatting Requirements
{format_requirements}

## Instructions
Apply Markdown formatting:

1. **Headers**: Use appropriate header levels (##, ###)
2. **Lists**: Use bullets or numbers for lists
3. **Emphasis**: Bold for key terms, italics for titles
4. **Tables**: Use tables for comparative data
5. **Blockquotes**: Use for direct quotes
6. **Links**: Format citations as links
7. **Code blocks**: For any technical content

## Readability Guidelines
- Short paragraphs (3-4 sentences max)
- Clear section breaks
- Visual hierarchy with headers
- White space for breathing room

## Output
Provide the formatted Markdown content.
```

---

## 6.5 Confidence Scoring Prompt

### Purpose
Generate confidence scores and explanations for findings.

```
You are a confidence assessment specialist. Assign and explain confidence scores for research findings.

## Findings
{findings}

## Verification Data
{verification_data}

## Sources
{sources}

## Instructions
For each finding, calculate confidence based on:

1. **Source Count**: How many sources support this?
2. **Source Quality**: How credible are the sources?
3. **Consistency**: Do sources agree?
4. **Recency**: How current is the information?
5. **Verification Status**: Was it cross-referenced?

## Confidence Scale
- 90-100%: Very High - Multiple authoritative sources, fully verified
- 70-89%: High - Good source support, verified
- 50-69%: Medium - Limited sources or partial verification
- 30-49%: Low - Single source or concerns about accuracy
- 0-29%: Very Low - Unverified or conflicting information

## Output Format
```json
{
  "scored_findings": [
    {
      "finding_id": "f1",
      "finding": "The finding text",
      "confidence_score": 85,
      "confidence_level": "high",
      "factors": {
        "source_count": {"value": 3, "contribution": 20},
        "source_quality": {"value": "high", "contribution": 25},
        "consistency": {"value": "full", "contribution": 20},
        "recency": {"value": "current", "contribution": 10},
        "verification": {"value": "verified", "contribution": 10}
      },
      "explanation": "This finding has high confidence because...",
      "caveats": ["Any limitations to note"]
    }
  ],
  "overall_confidence": 78,
  "confidence_distribution": {
    "very_high": 2,
    "high": 5,
    "medium": 3,
    "low": 1,
    "very_low": 0
  }
}
```
```

---

## 6.6 Visualization Suggestions Prompt

### Purpose
Suggest appropriate visualizations for the research data.

```
You are a data visualization specialist. Suggest appropriate visualizations for this research content.

## Research Content
{content}

## Data Points
{data_points}

## Instructions
Identify opportunities for visualization:

1. **Comparisons**: Side-by-side comparisons → tables, bar charts
2. **Trends**: Time-series data → line charts
3. **Proportions**: Part-to-whole → pie charts
4. **Relationships**: Correlations → scatter plots
5. **Hierarchies**: Categories → tree diagrams
6. **Processes**: Steps → flowcharts

## Output Format
```json
{
  "visualization_suggestions": [
    {
      "data_description": "What data to visualize",
      "chart_type": "table|bar|line|pie|scatter|tree|flow",
      "reason": "Why this visualization works",
      "data_structure": {
        "labels": ["label1", "label2"],
        "values": [100, 200]
      },
      "implementation": "markdown|mermaid|description"
    }
  ],
  "tables_to_include": [
    {
      "title": "Table title",
      "headers": ["Col1", "Col2"],
      "rows": [["data1", "data2"]],
      "markdown": "| Col1 | Col2 |\n|------|------|\n| data1 | data2 |"
    }
  ]
}
```
```

---

## 6.7 Follow-up Questions Prompt

### Purpose
Generate relevant follow-up questions for the user.

```
You are a research assistant. Based on the completed research, suggest relevant follow-up questions.

## Original Query
{query}

## Research Findings
{findings}

## Gaps Identified
{gaps}

## Instructions
Generate follow-up questions that:

1. **Deepen Understanding**: Explore findings further
2. **Address Gaps**: Fill identified knowledge gaps
3. **Explore Implications**: What does this mean?
4. **Compare Alternatives**: Consider other angles
5. **Apply Knowledge**: How to use this information?

## Output Format
```json
{
  "follow_up_questions": [
    {
      "question": "The follow-up question",
      "purpose": "deepen|gap|implication|compare|apply",
      "relevance": "How this relates to original research",
      "complexity": "simple|medium|complex"
    }
  ],
  "recommended_next_steps": ["Action items for the user"],
  "related_topics": ["Topics the user might also be interested in"]
}
```
```

---

## 6.8 Multi-Format Output Prompt

### Purpose
Generate output in multiple formats simultaneously.

```
You are a multi-format output generator. Create the research output in multiple formats.

## Research Content
{content}

## Required Formats
- Markdown (full report)
- JSON (structured data)
- Plain text (summary)
- HTML (formatted) [optional]

## Instructions
Generate the same content optimized for each format:

1. **Markdown**: Full formatting with headers, lists, links
2. **JSON**: Structured data for programmatic access
3. **Plain Text**: Clean text without formatting
4. **HTML**: Web-ready formatted content

## Output Format
```json
{
  "markdown": "# Full markdown content...",
  "json": {
    "structured": "data object"
  },
  "plain_text": "Plain text version...",
  "html": "<article>HTML version...</article>",
  "format_metadata": {
    "markdown_word_count": 1500,
    "json_fields": 25,
    "plain_text_word_count": 1200
  }
}
```
```

---

## 6.9 Output Quality Check Prompt

### Purpose
Verify the quality of generated output before delivery.

```
You are an output quality reviewer. Review this research output for quality issues.

## Generated Output
{output}

## Quality Criteria
{criteria}

## Instructions
Check the output for:

1. **Completeness**: Does it answer the original question?
2. **Accuracy**: Are all claims properly cited?
3. **Clarity**: Is it easy to understand?
4. **Structure**: Is it well-organized?
5. **Formatting**: Is formatting correct and consistent?
6. **Tone**: Is language appropriate?
7. **Length**: Is it appropriately detailed?

## Output Format
```json
{
  "quality_assessment": {
    "overall_score": 0-100,
    "grade": "A|B|C|D|F",
    "ready_to_deliver": true|false
  },
  "criteria_scores": {
    "completeness": {"score": 0-100, "notes": "string"},
    "accuracy": {"score": 0-100, "notes": "string"},
    "clarity": {"score": 0-100, "notes": "string"},
    "structure": {"score": 0-100, "notes": "string"},
    "formatting": {"score": 0-100, "notes": "string"},
    "tone": {"score": 0-100, "notes": "string"},
    "length": {"score": 0-100, "notes": "string"}
  },
  "issues": [
    {
      "category": "category name",
      "issue": "description",
      "severity": "high|medium|low",
      "location": "where in output",
      "fix": "suggested fix"
    }
  ],
  "improvements": ["Suggested improvements"]
}
```
```

---

## Usage Example

```python
# Output generation workflow
query = original_query
findings = verified_findings
sources = source_list

# Step 1: Generate confidence scores
confidence = llm.call(CONFIDENCE_SCORING_PROMPT.format(
    findings=findings,
    verification_data=verification,
    sources=sources
))

# Step 2: Generate executive summary
summary = llm.call(EXECUTIVE_SUMMARY_PROMPT.format(
    query=query,
    findings=findings,
    key_insights=confidence.high_confidence_findings
))

# Step 3: Generate full report
report = llm.call(RESEARCH_REPORT_PROMPT.format(
    query=query,
    findings=findings,
    sources=sources,
    verification_summary=verification
))

# Step 4: Format in Markdown
formatted = llm.call(MARKDOWN_FORMATTING_PROMPT.format(
    content=report,
    format_requirements=user_preferences
))

# Step 5: Quality check
quality = llm.call(OUTPUT_QUALITY_CHECK_PROMPT.format(
    output=formatted,
    criteria=quality_criteria
))

# Step 6: If quality is good, deliver; otherwise, fix issues
if quality.ready_to_deliver:
    return formatted
else:
    # Fix issues and re-check
    pass
```

---

*Document Version: 1.0*  
*Last Updated: February 4, 2026*
