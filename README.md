# Deep Research AI 🔍

An AI-powered research system that combines web search, reasoning, verification, and citation to deliver accurate, well-sourced research results.

## Features

- **🧠 Query Understanding**: Analyzes and decomposes complex research queries
- **🌐 Web Search**: Searches multiple sources and extracts relevant content
- **💭 Reasoning Engine**: Uses chain-of-thought reasoning to synthesize information
- **✅ Verification**: Cross-references claims and assesses source credibility
- **📚 Citation**: Generates proper citations in multiple academic formats (APA, MLA, Chicago, IEEE, Harvard)
- **📝 Output Generation**: Creates well-structured research reports

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/DeepResearchAI.git
cd DeepResearchAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Set your API keys as environment variables:

```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export SEARCH_API_KEY="your-search-api-key"  # Brave, Serper, or Tavily
```

Or create a `.env` file:

```env
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
SEARCH_API_KEY=your-search-api-key
```

### Usage

#### Command Line

```bash
# Basic research
python -m src.main "What is quantum computing?"

# With options
python -m src.main "Compare Python and Rust" \
    --audience professional \
    --citation-style apa \
    --max-sources 15

# Output as JSON
python -m src.main "Latest AI developments" --json-output
```

#### Python API

```python
import asyncio
from src import research, ResearchOrchestrator, Config

# Quick research
async def quick_research():
    result = await research("What is quantum computing?")
    print(result.answer)
    print(f"Confidence: {result.confidence:.1%}")

asyncio.run(quick_research())

# Advanced usage
async def advanced_research():
    from src import Config, AudienceType, CitationStyle
    
    config = Config()
    orchestrator = ResearchOrchestrator(config)
    
    result = await orchestrator.research(
        query="Compare Python and Rust programming languages",
        audience=AudienceType.PROFESSIONAL,
        citation_style=CitationStyle.APA,
        max_sources=15,
        verify_claims=True
    )
    
    print(result.answer)
    for source in result.sources:
        print(f"- {source.title}: {source.url}")

asyncio.run(advanced_research())
```

## Architecture

```
DeepResearchAI/
├── src/
│   ├── __init__.py           # Package exports
│   ├── config.py             # Configuration dataclasses
│   ├── models.py             # Data models
│   ├── llm_client.py         # LLM provider client
│   ├── orchestrator.py       # Research pipeline coordinator
│   ├── main.py               # CLI entry point
│   ├── modules/
│   │   ├── query_understanding.py  # Query analysis
│   │   ├── web_search.py           # Web search & extraction
│   │   ├── reasoning_engine.py     # Chain-of-thought reasoning
│   │   ├── verification.py         # Claim verification
│   │   ├── citation.py             # Citation generation
│   │   ├── output_generation.py    # Output formatting
│   │   └── error_handling.py       # Error handling
│   └── prompts/
│       ├── system_prompts.py       # System prompts
│       ├── query_prompts.py        # Query understanding prompts
│       ├── search_prompts.py       # Web search prompts
│       ├── reasoning_prompts.py    # Reasoning prompts
│       ├── verification_prompts.py # Verification prompts
│       ├── citation_prompts.py     # Citation prompts
│       ├── output_prompts.py       # Output generation prompts
│       └── error_prompts.py        # Error handling prompts
├── requirement/               # Requirements documentation
├── prompt/                    # Prompt templates documentation
├── tests/                     # Test files
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Research Pipeline

1. **Query Analysis**: Parse and understand the research query
2. **Sub-query Generation**: Break down complex queries into focused sub-queries
3. **Web Search**: Search multiple sources for each sub-query
4. **Content Extraction**: Extract and clean content from web pages
5. **Reasoning**: Apply chain-of-thought reasoning to synthesize findings
6. **Verification**: Cross-reference claims and assess source credibility
7. **Citation**: Generate properly formatted citations
8. **Output**: Create structured research report

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `llm_provider` | LLM provider (openai, anthropic) | openai |
| `llm_model` | Specific model to use | gpt-4o |
| `search_provider` | Search API (brave, serper, tavily) | brave |
| `max_sources` | Maximum sources to use | 10 |
| `verify_claims` | Enable claim verification | true |
| `audience` | Target audience | general |
| `citation_style` | Citation format | apa |

## API Reference

### Core Classes

#### `ResearchOrchestrator`
Main orchestrator that coordinates all research modules.

```python
orchestrator = ResearchOrchestrator(config)
result = await orchestrator.research(query, **options)
```

#### `QueryUnderstanding`
Analyzes and decomposes research queries.

```python
qu = QueryUnderstanding(config)
analysis = await qu.analyze(query)
```

#### `WebSearch`
Searches the web and extracts content.

```python
ws = WebSearch(config)
results = await ws.search(query, max_results=10)
content = await ws.extract_content(url)
```

#### `ReasoningEngine`
Performs chain-of-thought reasoning and synthesis.

```python
re = ReasoningEngine(config)
result = await re.chain_of_thought(query, context)
synthesis = await re.synthesize_information(query, sources)
```

#### `Verification`
Verifies claims and assesses source credibility.

```python
v = Verification(config)
result = await v.verify(claims, sources)
credibility = await v.assess_credibility(source)
```

#### `CitationManager`
Generates citations in multiple formats.

```python
cm = CitationManager(config)
citations = await cm.generate_citations(sources, content)
refs = await cm.generate_reference_list(sources, CitationStyle.APA)
```

#### `OutputGenerator`
Creates formatted research outputs.

```python
og = OutputGenerator(config)
report = await og.generate_report(query, findings, sources, confidence)
summary = await og.generate_summary(findings, SummaryLength.STANDARD)
```

## Error Handling

The system includes comprehensive error handling with graceful degradation:

```python
from src import ErrorHandler, ErrorSeverity

handler = ErrorHandler(config)

# Analyze errors
analysis = await handler.analyze_error(exception, context)

# Generate user-friendly messages
message = await handler.generate_user_message(error, user_action, severity)

# Retry with exponential backoff
result = await handler.retry_with_backoff(func, *args, max_attempts=3)
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_query_understanding.py
```

### Code Formatting

```bash
# Format code
black src tests
isort src tests

# Lint
ruff check src tests
```

### Type Checking

```bash
mypy src
```

## Requirements

- Python 3.10+
- OpenAI API key (for GPT models) or Anthropic API key (for Claude)
- Search API key (Brave Search, Serper, or Tavily)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- Brave Search, Serper, and Tavily for search APIs
