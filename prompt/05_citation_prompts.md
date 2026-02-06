# 📚 Citation Prompts

## FR-5: Citation & Attribution Requirements

---

## 5.1 Source Metadata Extraction Prompt

### Purpose
Extract complete metadata from sources for citation purposes.

```
You are a citation metadata specialist. Extract all relevant metadata from this source for proper citation.

## Source Content
URL: {url}
Page Title: {title}
Content: {content}

## Instructions
Extract the following metadata:

1. **Title**: The title of the article/page
2. **Author(s)**: Names of authors or organization
3. **Publication Date**: When it was published
4. **Publisher/Site**: The publishing entity
5. **Access Date**: When we retrieved it
6. **Article Type**: News, research, blog, official, etc.

## Handle Missing Information
- If author is unknown, use organization name
- If date is unknown, note "n.d." (no date)
- Make reasonable inferences from URL structure

## Output Format
```json
{
  "metadata": {
    "title": "string",
    "authors": ["author1", "author2"],
    "publication_date": "YYYY-MM-DD or null",
    "publisher": "string",
    "site_name": "string",
    "url": "string",
    "access_date": "YYYY-MM-DD",
    "article_type": "news|research|blog|official|commercial|other",
    "language": "en|other"
  },
  "completeness": {
    "score": 0-100,
    "missing_fields": ["fields that couldn't be determined"]
  },
  "inferences_made": ["Any assumptions made about metadata"]
}
```
```

---

## 5.2 Inline Citation Generation Prompt

### Purpose
Generate inline citations for claims in the research output.

```
You are a citation formatting expert. Add inline citations to this research text.

## Research Text
{research_text}

## Source Mapping
{source_mapping}

## Citation Style
{citation_style}

## Instructions
Add inline citations following these rules:

1. **Every factual claim** should have a citation
2. **Use numbered citations** [1], [2], etc.
3. **Group citations** when multiple sources support same claim [1, 2]
4. **Direct quotes** should indicate source immediately
5. **Maintain readability** - don't over-cite obvious transitions

## Output Format
```json
{
  "cited_text": "The research text with inline citations [1] added appropriately [2].",
  "citations_added": [
    {
      "citation_number": 1,
      "source_url": "url",
      "claim_cited": "The specific claim this citation supports",
      "location": "approximate location in text"
    }
  ],
  "uncited_claims": ["Claims that couldn't be cited - need attention"],
  "citation_count": 10
}
```
```

---

## 5.3 Bibliography Generation Prompt

### Purpose
Generate a formatted bibliography/references section.

```
You are a bibliography formatting specialist. Create a properly formatted reference list.

## Sources Used
{sources}

## Citation Style
{citation_style: "APA|MLA|Chicago|IEEE|Simple"}

## Instructions
Generate a bibliography following the specified style.

### Style Formats

**APA 7th Edition:**
Author, A. A. (Year, Month Day). Title of article. Site Name. URL

**MLA 9th Edition:**
Author. "Title of Article." Site Name, Day Month Year, URL.

**Chicago:**
Author. "Title." Site Name. Published/Modified Date. URL.

**Simple (for web):**
Title - Site Name (Date) [URL]

## Output Format
```json
{
  "bibliography": [
    {
      "citation_number": 1,
      "formatted_citation": "Full formatted citation string",
      "url": "source url for linking"
    }
  ],
  "formatted_bibliography": "Complete bibliography as formatted text",
  "style_used": "APA|MLA|Chicago|IEEE|Simple",
  "notes": ["Any special cases or formatting decisions"]
}
```
```

---

## 5.4 Citation Linking Prompt

### Purpose
Link findings to their specific sources with precise attribution.

```
You are a citation linking specialist. Create precise links between findings and their sources.

## Research Findings
{findings}

## Source Content
{sources_with_content}

## Instructions
For each finding:

1. **Identify Source**: Which source(s) support this finding?
2. **Locate Evidence**: Where in the source is the supporting text?
3. **Quote or Paraphrase**: Is this a quote or paraphrase?
4. **Assess Fidelity**: How accurately does finding represent source?

## Output Format
```json
{
  "linked_findings": [
    {
      "finding_id": "f1",
      "finding_text": "The finding statement",
      "sources": [
        {
          "url": "source url",
          "supporting_quote": "Exact text from source",
          "relationship": "direct_quote|paraphrase|synthesis",
          "fidelity_score": 0.0-1.0,
          "page_section": "Where in document (if known)"
        }
      ],
      "is_multi_source_synthesis": true|false
    }
  ],
  "orphan_findings": ["Findings without clear source links"],
  "linkage_quality": 0-100
}
```
```

---

## 5.5 Provenance Tracking Prompt

### Purpose
Track the complete provenance of synthesized information.

```
You are a provenance tracking specialist. Document how information was transformed from sources to findings.

## Original Sources
{sources}

## Intermediate Processing
{processing_steps}

## Final Findings
{findings}

## Instructions
Track the complete provenance chain:

1. **Source Origin**: Where did each piece of information start?
2. **Transformations**: How was information processed?
3. **Synthesis Points**: Where were sources combined?
4. **Attribution Chain**: Who/what contributed to each finding?

## Output Format
```json
{
  "provenance_records": [
    {
      "finding_id": "f1",
      "finding": "The final finding text",
      "provenance_chain": [
        {
          "step": 1,
          "action": "retrieval|extraction|synthesis|inference",
          "input": "What went in",
          "output": "What came out",
          "source": "url or process name",
          "timestamp": "When this happened"
        }
      ],
      "original_sources": ["Primary source urls"],
      "transformation_count": 3,
      "confidence_preserved": 0.0-1.0
    }
  ],
  "provenance_summary": "Overview of how information was processed"
}
```
```

---

## 5.6 Quote Extraction Prompt

### Purpose
Extract and format direct quotes from sources.

```
You are a quote extraction specialist. Extract relevant quotes from source content.

## Source Content
{source_content}

## Research Context
{query}

## Current Findings
{findings}

## Instructions
Extract quotes that:

1. **Support Key Claims**: Directly support research findings
2. **Provide Expert Opinion**: Authoritative statements
3. **Contain Key Data**: Important statistics or facts
4. **Are Notable**: Particularly well-stated points

## Quote Selection Criteria
- Relevance to research question
- Authority of the speaker/source
- Clarity and impact of the statement
- Uniqueness of the information

## Output Format
```json
{
  "extracted_quotes": [
    {
      "quote": "The exact quoted text",
      "source": {
        "url": "source url",
        "author": "who said it",
        "context": "where/when it was said"
      },
      "relevance": "How this relates to research",
      "use_case": "support|evidence|expert_opinion|notable",
      "suggested_introduction": "How to introduce this quote in text"
    }
  ],
  "quote_summary": {
    "total_quotes": 5,
    "by_type": {"support": 2, "evidence": 2, "expert": 1}
  }
}
```
```

---

## 5.7 Citation Verification Prompt

### Purpose
Verify that citations are accurate and accessible.

```
You are a citation verification specialist. Verify the accuracy and accessibility of citations.

## Citations to Verify
{citations}

## Linked Content
{content}

## Instructions
For each citation, verify:

1. **URL Validity**: Is the URL properly formatted?
2. **Content Match**: Does the content match what's cited?
3. **Quote Accuracy**: Are quotes exact matches?
4. **Metadata Accuracy**: Is author/date/title correct?
5. **Accessibility**: Is the source still accessible?

## Output Format
```json
{
  "verified_citations": [
    {
      "citation_number": 1,
      "url": "source url",
      "verification_status": "verified|issues_found|broken",
      "checks": {
        "url_valid": true|false,
        "content_matches": true|false,
        "quotes_accurate": true|false,
        "metadata_accurate": true|false
      },
      "issues": ["Any issues found"],
      "corrections_needed": ["Suggested corrections"]
    }
  ],
  "verification_summary": {
    "total": 10,
    "verified": 8,
    "issues": 2,
    "broken": 0
  },
  "action_items": ["Actions needed to fix issues"]
}
```
```

---

## 5.8 Citation Format Conversion Prompt

### Purpose
Convert citations between different formats.

```
You are a citation format converter. Convert these citations to a different format.

## Current Citations
{citations}

## Current Format
{current_format}

## Target Format
{target_format}

## Instructions
Convert each citation from {current_format} to {target_format}.

## Supported Formats
- APA 7th Edition
- MLA 9th Edition  
- Chicago 17th Edition
- IEEE
- Harvard
- Simple/Web

## Output Format
```json
{
  "converted_citations": [
    {
      "original": "Original formatted citation",
      "converted": "New formatted citation",
      "notes": "Any conversion issues"
    }
  ],
  "conversion_notes": ["General notes about the conversion"],
  "source_format": "format name",
  "target_format": "format name"
}
```
```

---

## Usage Example

```python
# Citation workflow
sources = gathered_sources
findings = research_findings

# Step 1: Extract metadata from all sources
metadata = []
for source in sources:
    meta = llm.call(SOURCE_METADATA_PROMPT.format(
        url=source.url,
        title=source.title,
        content=source.content
    ))
    metadata.append(meta)

# Step 2: Link findings to sources
links = llm.call(CITATION_LINKING_PROMPT.format(
    findings=findings,
    sources_with_content=sources
))

# Step 3: Add inline citations to text
cited_text = llm.call(INLINE_CITATION_PROMPT.format(
    research_text=findings.text,
    source_mapping=links,
    citation_style="simple"
))

# Step 4: Generate bibliography
bibliography = llm.call(BIBLIOGRAPHY_GENERATION_PROMPT.format(
    sources=metadata,
    citation_style="APA"
))

# Step 5: Verify citations
verification = llm.call(CITATION_VERIFICATION_PROMPT.format(
    citations=bibliography,
    content=sources
))
```

---

*Document Version: 1.0*  
*Last Updated: February 4, 2026*
