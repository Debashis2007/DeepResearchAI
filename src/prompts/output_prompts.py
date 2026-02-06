"""
Output generation prompts for the Deep Research AI system.

These prompts handle the final synthesis and formatting of research results
into user-friendly, well-structured output formats.
"""

# Report Generation Prompt
REPORT_GENERATION_PROMPT = """You are an expert research report writer.

Your task is to generate a comprehensive, well-structured research report.

RESEARCH QUERY:
{query}

SYNTHESIZED FINDINGS:
{findings}

SOURCES USED:
{sources}

CONFIDENCE ASSESSMENT:
{confidence}

Generate a research report following this structure:

1. **Executive Summary**: Brief overview of key findings (2-3 paragraphs)

2. **Introduction**: 
   - Research question context
   - Scope and methodology used
   - Key terms defined

3. **Main Findings**:
   - Organized by theme or sub-question
   - Evidence-based claims with source references
   - Data and statistics where available

4. **Analysis**:
   - Synthesis of findings
   - Patterns and trends identified
   - Conflicting viewpoints addressed

5. **Limitations**:
   - Gaps in available information
   - Confidence levels explained
   - Areas needing further research

6. **Conclusion**:
   - Direct answer to research question
   - Key takeaways
   - Recommendations if applicable

Respond in JSON format:
{{
    "report": {{
        "title": "Report title",
        "executive_summary": "2-3 paragraph summary",
        "introduction": {{
            "context": "Research context",
            "scope": "Scope of research",
            "methodology": "Brief methodology",
            "key_terms": {{"term": "definition"}}
        }},
        "main_findings": [
            {{
                "theme": "Finding theme",
                "content": "Detailed findings",
                "evidence": ["supporting evidence"],
                "sources": ["source_ids"]
            }}
        ],
        "analysis": {{
            "synthesis": "Synthesized analysis",
            "patterns": ["identified patterns"],
            "conflicting_views": ["conflicts and how addressed"]
        }},
        "limitations": {{
            "information_gaps": ["gaps"],
            "confidence_notes": "confidence explanation",
            "further_research": ["suggested areas"]
        }},
        "conclusion": {{
            "answer": "Direct answer to query",
            "key_takeaways": ["takeaway points"],
            "recommendations": ["recommendations if any"]
        }}
    }},
    "metadata": {{
        "word_count": 0,
        "reading_time_minutes": 0,
        "complexity_level": "beginner|intermediate|advanced"
    }}
}}
"""

# Summary Generation Prompt
SUMMARY_GENERATION_PROMPT = """You are an expert at creating concise, informative summaries.

Your task is to create a summary of research findings at the specified detail level.

RESEARCH FINDINGS:
{findings}

SUMMARY LENGTH: {length}

Generate a summary following these guidelines:

1. **Brief** (1-2 paragraphs): Key answer only
2. **Standard** (3-5 paragraphs): Answer with main supporting points
3. **Detailed** (6-10 paragraphs): Comprehensive summary with nuance

Include:
- Direct answer to the research question
- Most important supporting evidence
- Key caveats or limitations
- Confidence level indication

Respond in JSON format:
{{
    "summary": {{
        "text": "The complete summary text",
        "key_points": ["bullet point takeaways"],
        "confidence_statement": "How confident we are in these findings",
        "caveats": ["important caveats"]
    }},
    "metadata": {{
        "length_type": "{length}",
        "word_count": 0,
        "source_count": 0
    }}
}}
"""

# Answer Formatting Prompt
ANSWER_FORMATTING_PROMPT = """You are an expert at formatting research answers for different audiences.

Your task is to format the research answer for the specified audience and format.

RESEARCH ANSWER:
{answer}

TARGET AUDIENCE: {audience}
OUTPUT FORMAT: {format}

Format the answer according to these specifications:

**Audience Levels:**
- general: Non-technical, accessible language
- professional: Business/industry appropriate
- academic: Scholarly, formal language
- technical: Technical details included

**Output Formats:**
- text: Plain text with paragraphs
- markdown: Full markdown formatting
- html: HTML formatted
- structured: Bullet points and sections

Respond in JSON format:
{{
    "formatted_answer": {{
        "content": "The formatted answer",
        "format": "{format}",
        "audience": "{audience}"
    }},
    "readability_metrics": {{
        "grade_level": "estimated reading grade level",
        "technical_density": "low|medium|high"
    }}
}}
"""

# Visualization Suggestion Prompt
VISUALIZATION_SUGGESTION_PROMPT = """You are an expert in data visualization and information design.

Your task is to suggest visualizations that would enhance the research presentation.

RESEARCH DATA:
{data}

FINDINGS:
{findings}

Suggest appropriate visualizations:

1. **Charts**: For numerical/statistical data
2. **Diagrams**: For relationships and processes
3. **Tables**: For comparisons
4. **Timelines**: For temporal information
5. **Maps**: For geographical data

Respond in JSON format:
{{
    "visualizations": [
        {{
            "type": "chart|diagram|table|timeline|map|infographic",
            "subtype": "bar|line|pie|flowchart|comparison|etc",
            "title": "Suggested title",
            "description": "What it would show",
            "data_requirements": ["data needed"],
            "priority": "high|medium|low",
            "implementation_notes": "How to create it"
        }}
    ],
    "recommended_count": 0,
    "data_visualization_potential": "low|medium|high"
}}
"""

# Multi-format Output Prompt
MULTI_FORMAT_OUTPUT_PROMPT = """You are an expert at generating research outputs in multiple formats.

Your task is to generate the research output in multiple formats simultaneously.

RESEARCH CONTENT:
{content}

CITATIONS:
{citations}

Generate outputs in these formats:

1. **Plain Text**: Simple, readable text
2. **Markdown**: With proper formatting
3. **HTML**: Web-ready format
4. **JSON**: Structured data format

Respond in JSON format:
{{
    "outputs": {{
        "plain_text": "Plain text version",
        "markdown": "Markdown version with ## headers, **bold**, etc",
        "html": "<html>HTML version</html>",
        "json": {{
            "structured": "data representation"
        }}
    }},
    "recommended_format": "most suitable format",
    "format_notes": {{
        "plain_text": "notes about this format",
        "markdown": "notes",
        "html": "notes",
        "json": "notes"
    }}
}}
"""

# Response Quality Assessment Prompt
RESPONSE_QUALITY_PROMPT = """You are an expert at assessing research output quality.

Your task is to evaluate the quality of the generated research response.

ORIGINAL QUERY:
{query}

GENERATED RESPONSE:
{response}

SOURCES USED:
{sources}

Evaluate the response on these criteria:

1. **Relevance**: How well does it answer the query?
2. **Completeness**: Are all aspects addressed?
3. **Accuracy**: Are claims properly supported?
4. **Clarity**: Is it well-written and clear?
5. **Citation Quality**: Are sources properly attributed?
6. **Objectivity**: Is it balanced and unbiased?

Respond in JSON format:
{{
    "quality_assessment": {{
        "overall_score": 0.0-1.0,
        "criteria_scores": {{
            "relevance": 0.0-1.0,
            "completeness": 0.0-1.0,
            "accuracy": 0.0-1.0,
            "clarity": 0.0-1.0,
            "citation_quality": 0.0-1.0,
            "objectivity": 0.0-1.0
        }},
        "strengths": ["identified strengths"],
        "weaknesses": ["identified weaknesses"],
        "improvement_suggestions": ["suggestions"]
    }},
    "confidence_level": "low|medium|high|very_high",
    "ready_for_delivery": true/false,
    "revision_needed": true/false
}}
"""

# Follow-up Question Generation Prompt
FOLLOWUP_QUESTIONS_PROMPT = """You are an expert at identifying valuable follow-up research questions.

Your task is to generate relevant follow-up questions based on the research.

ORIGINAL QUERY:
{query}

RESEARCH FINDINGS:
{findings}

INFORMATION GAPS:
{gaps}

Generate follow-up questions that would:
1. Deepen understanding of the topic
2. Address identified gaps
3. Explore related areas
4. Clarify ambiguities

Respond in JSON format:
{{
    "follow_up_questions": [
        {{
            "question": "The follow-up question",
            "rationale": "Why this question is valuable",
            "type": "deepening|gap_filling|related|clarification",
            "priority": "high|medium|low",
            "estimated_complexity": "simple|moderate|complex"
        }}
    ],
    "recommended_next_question": "most valuable next question",
    "research_continuation_score": 0.0-1.0
}}
"""

# Export Format Prompt
EXPORT_FORMAT_PROMPT = """You are an expert at preparing research for export and sharing.

Your task is to prepare the research output for the specified export format.

RESEARCH REPORT:
{report}

EXPORT FORMAT: {export_format}

Prepare the content for export considering:

1. **PDF**: Proper structure, headers, pagination hints
2. **DOCX**: Word-compatible formatting
3. **Slides**: Key points for presentation
4. **Email**: Professional email format
5. **Social**: Social media appropriate snippets

Respond in JSON format:
{{
    "export_ready": {{
        "content": "Formatted content for export",
        "format": "{export_format}",
        "sections": ["section breakdown"],
        "formatting_notes": "notes for the export format"
    }},
    "export_metadata": {{
        "suggested_filename": "filename",
        "estimated_pages": 0,
        "includes_citations": true/false
    }}
}}
"""
