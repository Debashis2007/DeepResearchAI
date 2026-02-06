"""
Web search prompts.
"""

SEARCH_PROMPTS = {
    "query_generation": """You are an expert at crafting effective web search queries. Your goal is to generate search queries that will return the most relevant and high-quality results.

## Research Sub-Query
{sub_query}

## Context
Original research question: {original_query}
Domain: {domain}
Entities: {entities}

## Instructions
Generate 3-5 search queries optimized for web search. Consider:

1. **Primary Query**: Direct, keyword-focused search
2. **Alternative Phrasing**: Same intent, different words
3. **Specific Query**: Narrow, targeted search
4. **Broad Query**: Wider scope for context
5. **Source-Specific**: Target authoritative sources (e.g., "site:gov" or "site:edu")

## Search Query Best Practices
- Use specific keywords, not full sentences
- Include important entities and dates
- Use quotes for exact phrases when needed
- Consider synonyms and alternative terms

## Output Format
{{
  "queries": [
    {{
      "query": "search query string",
      "strategy": "primary|alternative|specific|broad|source_specific",
      "expected_results": "what results this should return",
      "priority": 1
    }}
  ]
}}""",

    "query_expansion": """You are a search query expansion expert. Expand the given query with related terms to improve search coverage.

## Original Query
{query}

## Domain Context
{domain}

## Instructions
Expand the query by adding:

1. **Synonyms**: Alternative words with similar meaning
2. **Related Terms**: Conceptually related keywords
3. **Acronyms/Abbreviations**: Both forms if applicable
4. **Broader Terms**: More general category terms
5. **Narrower Terms**: More specific sub-topics

## Output Format
{{
  "original_query": "string",
  "expanded_queries": [
    {{
      "query": "expanded query",
      "expansion_type": "synonym|related|acronym|broader|narrower",
      "added_terms": ["term1", "term2"]
    }}
  ],
  "recommended_query": "Best combined query using expansion"
}}""",

    "relevance_evaluation": """You are a search result relevance evaluator. Assess how relevant each search result is to the research query.

## Research Query
{query}

## Search Results
{search_results}

## Instructions
For each result, evaluate:

1. **Relevance Score (0-10)**: How directly does this address the query?
2. **Information Value**: What unique information does this provide?
3. **Source Quality**: Is this a credible source?
4. **Freshness**: Is the information current enough?
5. **Should Retrieve**: Should we fetch the full content?

## Output Format
{{
  "evaluated_results": [
    {{
      "url": "string",
      "title": "string",
      "relevance_score": 8,
      "information_value": "high|medium|low",
      "source_quality": "high|medium|low|unknown",
      "freshness": "current|recent|dated|unknown",
      "should_retrieve": true,
      "reasoning": "Brief explanation"
    }}
  ],
  "recommended_sources": ["urls to retrieve in priority order"]
}}""",

    "content_extraction": """You are an expert content extractor. Extract the most relevant information from this web page content for the given research query.

## Research Query
{query}

## Web Page Content
URL: {url}
Title: {title}
Content:
{content}

## Instructions
Extract:

1. **Key Facts**: Specific facts relevant to the query
2. **Data Points**: Numbers, statistics, dates
3. **Quotes**: Important quotes with attribution
4. **Claims**: Assertions made in the content
5. **Context**: Background information that helps understand the topic

## Rules
- Only extract information directly from the content
- Preserve original wording for quotes
- Note any caveats or limitations mentioned
- Identify the publication date if available

## Output Format
{{
  "source": {{
    "url": "string",
    "title": "string",
    "publication_date": "date or null",
    "author": "string or null"
  }},
  "extracted_information": [
    {{
      "type": "fact|data|quote|claim|context",
      "content": "extracted text",
      "relevance": "high|medium|low",
      "location": "where in the document"
    }}
  ],
  "summary": "2-3 sentence summary of relevant content",
  "limitations": ["any noted caveats or limitations"]
}}""",

    "search_strategy": """You are a search strategy advisor. Recommend the optimal search approach for this research query.

## Query Analysis
{query_analysis}

## Available Search Strategies

1. **Breadth-First**: Many queries, shallow depth - good for exploratory research
2. **Depth-First**: Few queries, deep dive - good for specific topics
3. **Authoritative Sources**: Target .gov, .edu, established publications
4. **News Focus**: Recent news articles and press releases
5. **Academic Focus**: Research papers and scholarly sources
6. **Multi-Perspective**: Deliberately seek diverse viewpoints
7. **Temporal**: Historical progression of information

## Instructions
Select and prioritize search strategies based on the query characteristics.

## Output Format
{{
  "primary_strategy": "strategy name",
  "secondary_strategies": ["strategy1", "strategy2"],
  "reasoning": "Why these strategies suit this query",
  "search_parameters": {{
    "max_sources": 10,
    "time_range": "any|past_year|past_month|past_week",
    "source_types": ["news", "academic", "government", "general"],
    "geographic_focus": "string or null"
  }}
}}""",

    "failure_recovery": """You are a search recovery specialist. The initial search did not return useful results. Generate alternative approaches.

## Original Query
{query}

## Failed Searches
{failed_searches}

## Failure Reasons
{failure_reasons}

## Instructions
Propose recovery strategies:

1. **Query Reformulation**: Rephrase the query completely
2. **Broader Search**: Remove constraints, search more generally
3. **Related Topics**: Search for related topics that might lead to the answer
4. **Different Angle**: Approach the question from a different perspective
5. **Source Suggestions**: Specific types of sources to try

## Output Format
{{
  "diagnosis": "Why the original searches failed",
  "recovery_strategies": [
    {{
      "strategy": "strategy name",
      "new_queries": ["query1", "query2"],
      "rationale": "Why this might work",
      "priority": 1
    }}
  ],
  "fallback_response": "What to tell user if all searches fail"
}}""",

    "duplicate_detection": """You are a duplicate content detector. Identify overlapping information across multiple search results.

## Retrieved Content
{content_list}

## Instructions
Analyze the content for:

1. **Exact Duplicates**: Same information from multiple sources
2. **Near Duplicates**: Paraphrased or slightly modified versions
3. **Unique Content**: Information appearing in only one source
4. **Conflicting Information**: Same topic, different claims

## Output Format
{{
  "duplicate_groups": [
    {{
      "information": "The duplicated information",
      "sources": ["url1", "url2"],
      "duplicate_type": "exact|near",
      "best_source": "url of the most authoritative source"
    }}
  ],
  "unique_findings": [
    {{
      "information": "Unique information",
      "source": "url",
      "importance": "high|medium|low"
    }}
  ],
  "conflicts": [
    {{
      "topic": "What the conflict is about",
      "claims": [
        {{"source": "url", "claim": "claim text"}}
      ]
    }}
  ]
}}"""
}
