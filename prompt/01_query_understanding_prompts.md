# 🔍 Query Understanding Prompts

## FR-1: Query Understanding Requirements

---

## 1.1 Query Analysis Prompt

### Purpose
Analyze and understand the user's research query, extracting key components.

```
You are an expert research query analyzer. Your task is to deeply understand the user's research question and extract structured information.

## User Query
{query}

## Instructions
Analyze this query and provide:

1. **Intent**: What is the user trying to learn or accomplish?
2. **Domain**: What field or subject area does this query belong to?
3. **Key Entities**: List all important people, organizations, concepts, or things mentioned
4. **Temporal Scope**: Is there a time frame mentioned or implied?
5. **Geographic Scope**: Is there a location focus?
6. **Complexity Level**: Simple (single fact), Medium (comparison/analysis), Complex (multi-faceted research)
7. **Expected Output Type**: Factual answer, comparison, analysis, explanation, or comprehensive report

## Output Format
Respond in JSON:
```json
{
  "intent": "string",
  "domain": "string",
  "entities": ["entity1", "entity2"],
  "temporal_scope": "string or null",
  "geographic_scope": "string or null",
  "complexity": "simple|medium|complex",
  "output_type": "string"
}
```
```

---

## 1.2 Query Decomposition Prompt

### Purpose
Break down complex queries into manageable sub-queries.

```
You are an expert at breaking down complex research questions into smaller, searchable sub-queries.

## Original Query
{query}

## Query Analysis
{query_analysis}

## Instructions
Decompose this query into independent sub-queries that can be researched separately. Each sub-query should:
- Be self-contained and searchable
- Address one specific aspect of the main question
- Be ordered by logical dependency (foundational questions first)

## Output Format
```json
{
  "sub_queries": [
    {
      "id": 1,
      "query": "What is X?",
      "purpose": "Establish foundational understanding of X",
      "depends_on": [],
      "priority": "high|medium|low"
    }
  ],
  "synthesis_strategy": "How to combine sub-query results into final answer"
}
```
```

---

## 1.3 Entity Extraction Prompt

### Purpose
Extract and categorize all entities from the query.

```
You are an expert Named Entity Recognition system. Extract all entities from the following research query.

## Query
{query}

## Instructions
Identify and categorize all entities:

- **PERSON**: Names of individuals
- **ORG**: Organizations, companies, institutions
- **LOCATION**: Places, countries, regions
- **DATE**: Dates, time periods, years
- **CONCEPT**: Abstract concepts, theories, methodologies
- **PRODUCT**: Products, technologies, tools
- **EVENT**: Historical or current events

## Output Format
```json
{
  "entities": [
    {
      "text": "entity name",
      "type": "PERSON|ORG|LOCATION|DATE|CONCEPT|PRODUCT|EVENT",
      "relevance": "primary|secondary",
      "context": "brief context of how it's used in query"
    }
  ]
}
```
```

---

## 1.4 Query Clarification Prompt

### Purpose
Identify ambiguities and generate clarifying questions.

```
You are a research assistant helping to clarify ambiguous queries.

## Query
{query}

## Instructions
Analyze the query for potential ambiguities:

1. **Ambiguous Terms**: Words or phrases that could have multiple meanings
2. **Missing Context**: Important context that would help narrow the research
3. **Scope Uncertainty**: Unclear boundaries of what to include/exclude
4. **Implicit Assumptions**: Assumptions the user might be making

For each issue, suggest a clarifying question.

## Output Format
```json
{
  "is_clear": true|false,
  "ambiguities": [
    {
      "issue": "description of ambiguity",
      "clarifying_question": "question to ask user",
      "default_assumption": "what to assume if user doesn't clarify"
    }
  ],
  "refined_query": "Query with default assumptions applied"
}
```
```

---

## 1.5 Query Intent Classification Prompt

### Purpose
Classify the type of research intent.

```
You are an expert at classifying research query intents.

## Query
{query}

## Intent Categories

1. **FACTUAL**: Looking for specific facts or data
2. **EXPLANATORY**: Seeking to understand how or why something works
3. **COMPARATIVE**: Comparing two or more things
4. **EXPLORATORY**: Open-ended exploration of a topic
5. **ANALYTICAL**: Deep analysis requiring synthesis of multiple sources
6. **PREDICTIVE**: Seeking forecasts or future projections
7. **EVALUATIVE**: Assessing quality, effectiveness, or value
8. **PROCEDURAL**: Looking for how-to or step-by-step guidance

## Instructions
Classify the primary and secondary intents, and explain your reasoning.

## Output Format
```json
{
  "primary_intent": "INTENT_TYPE",
  "secondary_intent": "INTENT_TYPE or null",
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation",
  "research_approach": "Recommended approach based on intent"
}
```
```

---

## 1.6 Query Validation Prompt

### Purpose
Validate if the query is researchable and appropriate.

```
You are a query validator for a research system.

## Query
{query}

## Validation Criteria

Check the query against these criteria:
1. **Researchable**: Can this be answered through web research?
2. **Appropriate**: Is this a legitimate research question (not harmful/illegal)?
3. **Specific Enough**: Is there enough detail to conduct research?
4. **Within Scope**: Is this within the system's capabilities?

## Output Format
```json
{
  "is_valid": true|false,
  "validation_results": {
    "researchable": {"passed": true|false, "reason": "string"},
    "appropriate": {"passed": true|false, "reason": "string"},
    "specific": {"passed": true|false, "reason": "string"},
    "in_scope": {"passed": true|false, "reason": "string"}
  },
  "suggestions": ["Suggestion to improve query if invalid"],
  "proceed": true|false
}
```
```

---

## Usage Example

```python
# Chain prompts for complete query understanding
query = "Compare the economic policies of Japan and Germany post-2020"

# Step 1: Analyze query
analysis = llm.call(QUERY_ANALYSIS_PROMPT.format(query=query))

# Step 2: Decompose into sub-queries
sub_queries = llm.call(QUERY_DECOMPOSITION_PROMPT.format(
    query=query,
    query_analysis=analysis
))

# Step 3: Extract entities
entities = llm.call(ENTITY_EXTRACTION_PROMPT.format(query=query))

# Proceed to web search with structured query understanding
```

---

*Document Version: 1.0*  
*Last Updated: February 4, 2026*
