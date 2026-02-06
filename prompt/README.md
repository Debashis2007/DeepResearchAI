# 🎯 Prompt Library

## Deep Research AI with Web Search & Reasoning

---

## Prompt Index

| # | Prompt File | Purpose |
|---|-------------|---------|
| 01 | [Query Understanding](./01_query_understanding_prompts.md) | Parse and decompose research queries |
| 02 | [Web Search](./02_web_search_prompts.md) | Generate and optimize search queries |
| 03 | [Reasoning](./03_reasoning_prompts.md) | Multi-step reasoning and synthesis |
| 04 | [Verification](./04_verification_prompts.md) | Validate and verify findings |
| 05 | [Citation](./05_citation_prompts.md) | Generate and format citations |
| 06 | [Output Generation](./06_output_generation_prompts.md) | Format final research reports |
| 07 | [System Prompts](./07_system_prompts.md) | Core system identity and behavior |
| 08 | [Error Handling](./08_error_handling_prompts.md) | Handle edge cases and failures |

---

## Usage Guidelines

### Prompt Variables

Variables are denoted with `{variable_name}` syntax:
- `{query}` - User's research query
- `{context}` - Retrieved information
- `{sources}` - List of sources
- `{findings}` - Current findings

### Prompt Chaining

```
Query Understanding → Web Search → Reasoning → Verification → Output
```

### Best Practices

1. **Always include system prompt** before task-specific prompts
2. **Provide context** from previous steps
3. **Use structured output** formats (JSON) for parsing
4. **Include examples** for complex tasks
5. **Set clear constraints** on response format

---

*Document Version: 1.0*  
*Last Updated: February 4, 2026*
