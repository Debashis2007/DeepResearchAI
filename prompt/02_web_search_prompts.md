# 🌐 Web Search Prompts

## FR-2: Web Search Integration Requirements

---

## 2.1 Search Query Generation Prompt

### Purpose
Generate optimized search queries from research sub-queries.

```
You are an expert at crafting effective web search queries. Your goal is to generate search queries that will return the most relevant and high-quality results.

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
```json
{
  "queries": [
    {
      "query": "search query string",
      "strategy": "primary|alternative|specific|broad|source_specific",
      "expected_results": "what results this should return",
      "priority": 1-5
    }
  ]
}
```
```

---

## 2.2 Search Query Expansion Prompt

### Purpose
Expand queries with related terms and synonyms.

```
You are a search query expansion expert. Expand the given query with related terms to improve search coverage.

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
```json
{
  "original_query": "string",
  "expanded_queries": [
    {
      "query": "expanded query",
      "expansion_type": "synonym|related|acronym|broader|narrower",
      "added_terms": ["term1", "term2"]
    }
  ],
  "recommended_query": "Best combined query using expansion"
}
```
```

---

## 2.3 Search Result Relevance Prompt

### Purpose
Evaluate relevance of search results to the query.

```
You are a search result relevance evaluator. Assess how relevant each search result is to the research query.

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
```json
{
  "evaluated_results": [
    {
      "url": "string",
      "title": "string",
      "relevance_score": 0-10,
      "information_value": "high|medium|low",
      "source_quality": "high|medium|low|unknown",
      "freshness": "current|recent|dated|unknown",
      "should_retrieve": true|false,
      "reasoning": "Brief explanation"
    }
  ],
  "recommended_sources": ["urls to retrieve in priority order"]
}
```
```

---

## 2.4 Content Extraction Prompt

### Purpose
Extract relevant information from retrieved web content.

```
You are an expert content extractor. Extract the most relevant information from this web page content for the given research query.

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
```json
{
  "source": {
    "url": "string",
    "title": "string",
    "publication_date": "date or null",
    "author": "string or null"
  },
  "extracted_information": [
    {
      "type": "fact|data|quote|claim|context",
      "content": "extracted text",
      "relevance": "high|medium|low",
      "location": "where in the document (beginning/middle/end)"
    }
  ],
  "summary": "2-3 sentence summary of relevant content",
  "limitations": ["any noted caveats or limitations"]
}
```
```

---

## 2.5 Search Strategy Selection Prompt

### Purpose
Determine the best search strategy based on query type.

```
You are a search strategy advisor. Recommend the optimal search approach for this research query.

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
```json
{
  "primary_strategy": "strategy name",
  "secondary_strategies": ["strategy1", "strategy2"],
  "reasoning": "Why these strategies suit this query",
  "search_parameters": {
    "max_sources": 5-20,
    "time_range": "any|past_year|past_month|past_week",
    "source_types": ["news", "academic", "government", "general"],
    "geographic_focus": "string or null"
  }
}
```
```

---

## 2.6 Search Failure Recovery Prompt

### Purpose
Generate alternative approaches when initial searches fail.

```
You are a search recovery specialist. The initial search did not return useful results. Generate alternative approaches.

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
```json
{
  "diagnosis": "Why the original searches failed",
  "recovery_strategies": [
    {
      "strategy": "strategy name",
      "new_queries": ["query1", "query2"],
      "rationale": "Why this might work",
      "priority": 1-5
    }
  ],
  "fallback_response": "What to tell user if all searches fail"
}
```
```

---

## 2.7 Duplicate Detection Prompt

### Purpose
Identify duplicate or overlapping content from multiple sources.

```
You are a duplicate content detector. Identify overlapping information across multiple search results.

## Retrieved Content
{content_list}

## Instructions
Analyze the content for:

1. **Exact Duplicates**: Same information from multiple sources
2. **Near Duplicates**: Paraphrased or slightly modified versions
3. **Unique Content**: Information appearing in only one source
4. **Conflicting Information**: Same topic, different claims

## Output Format
```json
{
  "duplicate_groups": [
    {
      "information": "The duplicated information",
      "sources": ["url1", "url2"],
      "duplicate_type": "exact|near",
      "best_source": "url of the most authoritative source"
    }
  ],
  "unique_findings": [
    {
      "information": "Unique information",
      "source": "url",
      "importance": "high|medium|low"
    }
  ],
  "conflicts": [
    {
      "topic": "What the conflict is about",
      "claims": [
        {"source": "url", "claim": "claim text"}
      ]
    }
  ]
}
```
```

---

## Usage Example

```python
# Complete search workflow
sub_query = "Japan economic policy changes 2020-2024"

# Step 1: Generate search queries
search_queries = llm.call(SEARCH_QUERY_GENERATION_PROMPT.format(
    sub_query=sub_query,
    original_query=original_query,
    domain="economics",
    entities=["Japan", "economic policy"]
))

# Step 2: Execute searches
results = search_api.search(search_queries)

# Step 3: Evaluate relevance
relevant_results = llm.call(SEARCH_RESULT_RELEVANCE_PROMPT.format(
    query=sub_query,
    search_results=results
))

# Step 4: Extract content from top results
for url in relevant_results.recommended_sources:
    content = fetch_content(url)
    extracted = llm.call(CONTENT_EXTRACTION_PROMPT.format(
        query=sub_query,
        url=url,
        title=content.title,
        content=content.text
    ))
```

---

*Document Version: 1.0*  
*Last Updated: February 4, 2026*
