# Deep Research AI - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DEEP RESEARCH AI                                       │
│                    AI-Powered Research Assistant                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                      │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐              │
│  │   Gradio Web    │    │   CLI Interface │    │   Python API    │              │
│  │   (HF Spaces)   │    │   (main.py)     │    │   (Programmatic)│              │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘              │
└───────────┼──────────────────────┼──────────────────────┼───────────────────────┘
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            ORCHESTRATOR LAYER                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                      ResearchOrchestrator                                │    │
│  │  • Coordinates all research pipeline stages                              │    │
│  │  • Manages async execution and error handling                            │    │
│  │  • Aggregates results from all modules                                   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PROCESSING PIPELINE                                    │
│                                                                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│  │    STAGE 1   │   │    STAGE 2   │   │    STAGE 3   │   │    STAGE 4   │      │
│  │    Query     │──▶│     Web      │──▶│   Reasoning  │──▶│ Verification │      │
│  │Understanding │   │    Search    │   │    Engine    │   │              │      │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘      │
│         │                  │                  │                  │               │
│         ▼                  ▼                  ▼                  ▼               │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│  │ • Parse query│   │ • Search web │   │ • Synthesize │   │ • Cross-check│      │
│  │ • Extract    │   │ • Fetch pages│   │ • Reason     │   │ • Validate   │      │
│  │   entities   │   │ • Extract    │   │ • Analyze    │   │ • Score      │      │
│  │ • Identify   │   │   content    │   │ • Connect    │   │   confidence │      │
│  │   intent     │   │ • Rank       │   │   evidence   │   │              │      │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘      │
│                                                                                  │
│  ┌──────────────┐   ┌──────────────┐                                            │
│  │    STAGE 5   │   │    STAGE 6   │                                            │
│  │   Citation   │──▶│    Output    │                                            │
│  │  Management  │   │  Generation  │                                            │
│  └──────────────┘   └──────────────┘                                            │
│         │                  │                                                     │
│         ▼                  ▼                                                     │
│  ┌──────────────┐   ┌──────────────┐                                            │
│  │ • Format refs│   │ • Structure  │                                            │
│  │ • Link to    │   │   response   │                                            │
│  │   sources    │   │ • Apply      │                                            │
│  │ • Validate   │   │   formatting │                                            │
│  │   URLs       │   │ • Add meta   │                                            │
│  └──────────────┘   └──────────────┘                                            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                      │
│                                                                                  │
│  ┌─────────────────────────────┐    ┌─────────────────────────────┐             │
│  │        SEARCH APIs          │    │          LLM APIs           │             │
│  │  ┌─────────┐ ┌─────────┐   │    │  ┌─────────┐ ┌─────────┐   │             │
│  │  │Wikipedia│ │DuckDuck │   │    │  │HuggingFace│ │ OpenAI │   │             │
│  │  │   API   │ │   Go    │   │    │  │Inference │ │  API   │   │             │
│  │  └─────────┘ └─────────┘   │    │  └─────────┘ └─────────┘   │             │
│  │  ┌─────────┐ ┌─────────┐   │    │  ┌─────────┐ ┌─────────┐   │             │
│  │  │  Brave  │ │ Serper  │   │    │  │Anthropic│ │  Local  │   │             │
│  │  │ Search  │ │   API   │   │    │  │  Claude │ │  Model  │   │             │
│  │  └─────────┘ └─────────┘   │    │  └─────────┘ └─────────┘   │             │
│  └─────────────────────────────┘    └─────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
                           USER QUERY
                               │
                               ▼
                    ┌──────────────────┐
                    │ Query Analysis   │
                    │ ────────────────│
                    │ • Intent         │
                    │ • Entities       │
                    │ • Sub-queries    │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌───────────┐  ┌───────────┐  ┌───────────┐
       │Sub-query 1│  │Sub-query 2│  │Sub-query 3│
       └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
             │              │              │
             ▼              ▼              ▼
       ┌───────────┐  ┌───────────┐  ┌───────────┐
       │  Search   │  │  Search   │  │  Search   │
       │ Results 1 │  │ Results 2 │  │ Results 3 │
       └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                 ┌──────────────────┐
                 │ Content Extraction│
                 │ & Aggregation    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Reasoning Engine │
                 │ ────────────────│
                 │ • Analysis       │
                 │ • Synthesis      │
                 │ • Conclusions    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Verification   │
                 │ ────────────────│
                 │ • Fact-checking  │
                 │ • Consistency    │
                 │ • Confidence     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Output Generation│
                 │ ────────────────│
                 │ • Formatting     │
                 │ • Citations      │
                 │ • Metadata       │
                 └────────┬─────────┘
                          │
                          ▼
                   RESEARCH RESULT
                   ┌─────────────┐
                   │ • Answer    │
                   │ • Sources   │
                   │ • Confidence│
                   │ • Citations │
                   └─────────────┘
```

## Module Architecture

```
src/
├── __init__.py              # Package initialization
├── config.py                # Configuration dataclasses
├── models.py                # Data models (Entity, Citation, etc.)
├── orchestrator.py          # Main research orchestrator
├── main.py                  # CLI entry point
│
├── modules/                 # Core processing modules
│   ├── query_understanding.py   # Query parsing & analysis
│   ├── web_search.py           # Web search integration
│   ├── reasoning_engine.py     # AI reasoning & synthesis
│   ├── verification.py         # Fact verification
│   ├── citation.py             # Citation management
│   ├── output_generation.py    # Output formatting
│   └── error_handling.py       # Error recovery
│
├── prompts/                 # LLM prompt templates
│   ├── system_prompts.py
│   ├── query_prompts.py
│   ├── search_prompts.py
│   ├── reasoning_prompts.py
│   ├── verification_prompts.py
│   ├── citation_prompts.py
│   └── output_prompts.py
│
├── llm_client.py            # OpenAI/Anthropic client
├── llm_client_hf.py         # HuggingFace Inference client
├── search_duckduckgo.py     # DuckDuckGo search
└── search_multi.py          # Multi-backend search
```

## Component Interaction

```
┌────────────────────────────────────────────────────────────────┐
│                     CONFIGURATION                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  LLMConfig   │  │ SearchConfig │  │ResearchConfig│          │
│  │ • model      │  │ • provider   │  │ • max_sources│          │
│  │ • temperature│  │ • max_results│  │ • verify     │          │
│  │ • max_tokens │  │ • timeout    │  │ • citations  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────────────────────────────────────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                    RESEARCH ORCHESTRATOR                        │
│                                                                 │
│  async def research(query: str) -> ResearchResult:              │
│      1. query_analysis = await query_module.analyze(query)      │
│      2. search_results = await search_module.search(query)      │
│      3. reasoning = await reasoning_module.reason(results)      │
│      4. verified = await verify_module.verify(reasoning)        │
│      5. cited = await citation_module.add_citations(verified)   │
│      6. output = await output_module.format(cited)              │
│      return output                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    HUGGING FACE SPACES                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Docker Container                        │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                   Gradio App                         │  │  │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐   │  │  │
│  │  │  │  Query UI   │  │  Results UI │  │ Sources UI │   │  │  │
│  │  │  └─────────────┘  └─────────────┘  └────────────┘   │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                           │                                │  │
│  │                           ▼                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │              Research Functions                      │  │  │
│  │  │  • search_wikipedia()  - Wikipedia API calls         │  │  │
│  │  │  • research()          - Main research function      │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  URL: https://debashis2007-deep-research-ai.hf.space            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EXTERNAL APIS                                │
│  ┌─────────────────┐              ┌─────────────────┐           │
│  │  Wikipedia API  │              │ HuggingFace API │           │
│  │  (Free, No Key) │              │ (Inference)     │           │
│  └─────────────────┘              └─────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY STACK                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FRONTEND                    BACKEND                             │
│  ─────────                   ───────                             │
│  • Gradio 5.11               • Python 3.8+                       │
│  • Markdown rendering        • asyncio                           │
│  • Responsive UI             • dataclasses                       │
│                                                                  │
│  SEARCH                      LLM                                 │
│  ──────                      ───                                 │
│  • Wikipedia API             • HuggingFace Inference             │
│  • DuckDuckGo                • Qwen 2.5 7B Instruct              │
│  • urllib/httpx              • OpenAI (optional)                 │
│                              • Anthropic (optional)              │
│                                                                  │
│  DEPLOYMENT                  DEVELOPMENT                         │
│  ──────────                  ───────────                         │
│  • HuggingFace Spaces        • pytest                            │
│  • Docker                    • Git/GitHub                        │
│  • Gradio SDK                • VS Code                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Error Handling Flow

```
                         ┌─────────────┐
                         │   Request   │
                         └──────┬──────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Try Processing      │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
              ┌─────▼─────┐          ┌──────▼──────┐
              │  Success  │          │   Error     │
              └─────┬─────┘          └──────┬──────┘
                    │                       │
                    ▼                       ▼
             ┌────────────┐         ┌─────────────────┐
             │  Return    │         │ Error Handler   │
             │  Result    │         │ • Log error     │
             └────────────┘         │ • Retry logic   │
                                    │ • Fallback      │
                                    │ • User message  │
                                    └────────┬────────┘
                                             │
                              ┌──────────────┼──────────────┐
                              ▼              ▼              ▼
                       ┌──────────┐   ┌──────────┐   ┌──────────┐
                       │  Retry   │   │ Fallback │   │  Fail    │
                       │ (3 max)  │   │ Response │   │ Graceful │
                       └──────────┘   └──────────┘   └──────────┘
```

---

## Quick Reference

| Component | File | Purpose |
|-----------|------|---------|
| Orchestrator | `src/orchestrator.py` | Coordinates research pipeline |
| Query Module | `src/modules/query_understanding.py` | Parses user queries |
| Search Module | `src/modules/web_search.py` | Web search integration |
| Reasoning | `src/modules/reasoning_engine.py` | AI reasoning & synthesis |
| Verification | `src/modules/verification.py` | Fact-checking |
| Citations | `src/modules/citation.py` | Source management |
| Output | `src/modules/output_generation.py` | Response formatting |
| LLM Client | `src/llm_client_hf.py` | HuggingFace API |
| Search Client | `src/search_multi.py` | Multi-backend search |
| Web App | `app.py` | Gradio interface |

---

*Live Demo: https://debashis2007-deep-research-ai.hf.space*
