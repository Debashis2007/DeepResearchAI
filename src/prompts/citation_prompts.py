"""
Citation prompts for the Deep Research AI system.

These prompts handle citation generation, formatting, and source attribution
to ensure proper academic-style references and source tracking.
"""

# Citation Generation Prompt
CITATION_GENERATION_PROMPT = """You are an expert citation and source attribution specialist.

Your task is to generate proper citations for the sources used in research.

SOURCES TO CITE:
{sources}

CONTENT USING THESE SOURCES:
{content}

Generate citations for each source following these guidelines:

1. **Citation Style**: Generate citations in multiple formats:
   - APA (7th edition)
   - MLA (9th edition)
   - Chicago (17th edition)
   - IEEE
   - Harvard

2. **Source Metadata**: Extract and include:
   - Author(s) or organization
   - Publication date
   - Title
   - Publisher/Website name
   - URL
   - Access date

3. **In-text Citations**: Generate appropriate in-text citation markers

4. **Citation Quality**:
   - Handle missing metadata gracefully
   - Indicate when information is inferred
   - Flag incomplete citations

Respond in JSON format:
{{
    "citations": [
        {{
            "source_id": "unique_id",
            "source_url": "original_url",
            "metadata": {{
                "authors": ["author names or null"],
                "title": "title",
                "publication_date": "date or null",
                "publisher": "publisher name",
                "access_date": "YYYY-MM-DD"
            }},
            "formats": {{
                "apa": "APA formatted citation",
                "mla": "MLA formatted citation",
                "chicago": "Chicago formatted citation",
                "ieee": "IEEE formatted citation",
                "harvard": "Harvard formatted citation"
            }},
            "in_text": {{
                "apa": "(Author, Year)",
                "mla": "(Author Page)",
                "numeric": "[1]"
            }},
            "completeness_score": 0.0-1.0,
            "missing_fields": ["list of missing metadata"]
        }}
    ],
    "bibliography": {{
        "apa": "Full APA bibliography",
        "mla": "Full MLA works cited",
        "chicago": "Full Chicago bibliography"
    }}
}}
"""

# Source Attribution Prompt
SOURCE_ATTRIBUTION_PROMPT = """You are an expert in source attribution and provenance tracking.

Your task is to map claims in the research content to their original sources.

RESEARCH CONTENT:
{content}

AVAILABLE SOURCES:
{sources}

For each significant claim or piece of information, attribute it to its source:

1. **Claim Identification**: Identify each factual claim or data point
2. **Source Mapping**: Map each claim to one or more sources
3. **Attribution Confidence**: Rate confidence in the attribution
4. **Quote vs Paraphrase**: Distinguish between direct quotes and paraphrased content

Respond in JSON format:
{{
    "attributions": [
        {{
            "claim": "The factual claim or information",
            "claim_type": "statistic|fact|quote|analysis|opinion",
            "sources": [
                {{
                    "source_id": "source_identifier",
                    "source_url": "url",
                    "relevance": "direct|supporting|background",
                    "is_quote": true/false,
                    "original_text": "text from source if quote",
                    "confidence": 0.0-1.0
                }}
            ],
            "location_in_content": "paragraph/section reference",
            "needs_citation": true/false
        }}
    ],
    "unattributed_claims": [
        {{
            "claim": "claim without clear source",
            "reason": "why it couldn't be attributed",
            "suggestion": "suggested action"
        }}
    ],
    "attribution_coverage": 0.0-1.0
}}
"""

# Reference List Generation Prompt
REFERENCE_LIST_PROMPT = """You are an expert in academic reference list generation.

Your task is to create a properly formatted reference list from the sources used.

SOURCES:
{sources}

CITATION STYLE: {citation_style}

Generate a complete reference list following these guidelines:

1. **Ordering**: 
   - Alphabetical by author surname (APA, MLA, Chicago, Harvard)
   - Numerical by order of appearance (IEEE)

2. **Formatting**:
   - Proper indentation (hanging indent where applicable)
   - Correct punctuation and italicization
   - Consistent date formatting

3. **Web Sources**:
   - Include retrieval dates for online sources
   - Format URLs appropriately
   - Handle DOIs when available

4. **Special Cases**:
   - Multiple authors (et al. rules)
   - No author (organization or title)
   - No date (n.d.)

Respond in JSON format:
{{
    "reference_list": [
        {{
            "number": 1,
            "formatted_reference": "complete formatted reference",
            "source_id": "source_identifier"
        }}
    ],
    "formatted_output": "Complete formatted reference list as text",
    "style": "{citation_style}",
    "total_references": 0
}}
"""

# Inline Citation Insertion Prompt
INLINE_CITATION_PROMPT = """You are an expert in inline citation insertion.

Your task is to insert proper inline citations into the research content.

CONTENT TO ANNOTATE:
{content}

SOURCE ATTRIBUTIONS:
{attributions}

CITATION STYLE: {citation_style}

Insert inline citations following these rules:

1. **Placement**:
   - Place citations immediately after the claim
   - Before punctuation for mid-sentence citations
   - After punctuation for end-of-sentence citations

2. **Format**:
   - Use appropriate format for the citation style
   - Handle multiple sources for same claim
   - Use "ibid" or "op. cit." where appropriate

3. **Readability**:
   - Don't over-cite (one citation per claim usually sufficient)
   - Group related citations
   - Maintain text flow

Respond in JSON format:
{{
    "annotated_content": "Full content with inline citations inserted",
    "citation_count": 0,
    "citation_positions": [
        {{
            "position": "character position",
            "citation": "citation text",
            "source_ids": ["source_id1", "source_id2"]
        }}
    ],
    "style_used": "{citation_style}"
}}
"""

# Citation Validation Prompt
CITATION_VALIDATION_PROMPT = """You are an expert citation validator and quality checker.

Your task is to validate the citations and ensure they meet academic standards.

CITATIONS TO VALIDATE:
{citations}

SOURCES:
{sources}

Validate each citation for:

1. **Accuracy**:
   - Correct author names and order
   - Accurate publication dates
   - Correct titles (no typos)
   - Valid URLs (format check)

2. **Completeness**:
   - All required fields present
   - Appropriate handling of missing information

3. **Formatting**:
   - Correct punctuation
   - Proper capitalization
   - Correct italicization indicators
   - Proper ordering

4. **Consistency**:
   - Same style throughout
   - Consistent abbreviations
   - Uniform date formats

Respond in JSON format:
{{
    "validation_results": [
        {{
            "source_id": "source_identifier",
            "is_valid": true/false,
            "issues": [
                {{
                    "type": "accuracy|completeness|formatting|consistency",
                    "field": "affected field",
                    "issue": "description of issue",
                    "suggestion": "how to fix"
                }}
            ],
            "corrected_citation": "corrected version if needed"
        }}
    ],
    "overall_quality": 0.0-1.0,
    "total_issues": 0,
    "recommendations": ["list of general recommendations"]
}}
"""

# Source Metadata Extraction Prompt
SOURCE_METADATA_PROMPT = """You are an expert in extracting metadata from web sources.

Your task is to extract citation-relevant metadata from source content.

SOURCE URL: {url}

SOURCE CONTENT:
{content}

Extract the following metadata:

1. **Authors**: 
   - Individual authors with full names
   - Corporate/organizational authors
   - Author affiliations if available

2. **Publication Info**:
   - Publication date (exact or approximate)
   - Last modified date
   - Publisher/organization
   - Publication type (article, report, webpage, etc.)

3. **Document Info**:
   - Full title
   - Subtitle if any
   - Section/chapter if applicable
   - DOI if available

4. **Web-specific**:
   - Canonical URL
   - Site name vs publisher name
   - Archive/version information

Respond in JSON format:
{{
    "metadata": {{
        "authors": [
            {{
                "name": "full name",
                "type": "individual|organization",
                "affiliation": "affiliation or null"
            }}
        ],
        "title": "document title",
        "subtitle": "subtitle or null",
        "publication_date": "YYYY-MM-DD or null",
        "last_modified": "YYYY-MM-DD or null",
        "publisher": "publisher name",
        "site_name": "website name",
        "publication_type": "article|report|webpage|blog|news|academic",
        "doi": "DOI or null",
        "url": "canonical URL",
        "language": "language code"
    }},
    "extraction_confidence": {{
        "authors": 0.0-1.0,
        "date": 0.0-1.0,
        "title": 0.0-1.0,
        "overall": 0.0-1.0
    }},
    "inferred_fields": ["list of fields that were inferred"],
    "missing_fields": ["list of fields that couldn't be found"]
}}
"""

# Footnote Generation Prompt
FOOTNOTE_GENERATION_PROMPT = """You are an expert in generating footnotes and endnotes.

Your task is to generate appropriate footnotes for the research content.

CONTENT:
{content}

SOURCES:
{sources}

ATTRIBUTIONS:
{attributions}

Generate footnotes following these guidelines:

1. **First Reference**: Full citation on first mention
2. **Subsequent References**: Shortened form (author, short title, page)
3. **Ibid Usage**: Use "Ibid." for immediately repeated sources
4. **Explanatory Notes**: Add brief explanatory notes where helpful

Respond in JSON format:
{{
    "footnotes": [
        {{
            "number": 1,
            "marker_position": "position in text",
            "footnote_text": "complete footnote text",
            "source_id": "source_identifier",
            "is_first_reference": true/false,
            "footnote_type": "citation|explanatory|both"
        }}
    ],
    "content_with_markers": "content with footnote markers [1], [2], etc.",
    "footnote_section": "formatted footnotes section"
}}
"""
