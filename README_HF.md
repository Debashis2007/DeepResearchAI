---
title: Deep Research AI
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 🔍 Deep Research AI

An AI-powered research assistant that searches the web and synthesizes information to answer your questions.

## Features

- 🌐 **Real-time web search** using DuckDuckGo (no API key required)
- 🤖 **AI-powered synthesis** using Qwen 2.5 (free via Inference API)
- 📰 **Optional news search** for current events
- 📚 **Source citations** with links

## How it Works

1. **Enter a query** - Ask any research question
2. **Web search** - The system searches DuckDuckGo for relevant sources
3. **AI synthesis** - Qwen 2.5 analyzes sources and generates a comprehensive answer
4. **View results** - See the synthesized answer with citations and source links

## Example Queries

- "What are the latest developments in quantum computing?"
- "Compare Python vs Rust for systems programming"
- "How does CRISPR gene editing work?"
- "What is the current state of renewable energy?"

## Technology Stack

- **LLM**: Qwen 2.5 7B Instruct (via Hugging Face Inference API)
- **Search**: DuckDuckGo (free, no API key)
- **Frontend**: Gradio
- **Hosting**: Hugging Face Spaces

## Local Development

```bash
# Clone the repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/deep-research-ai

# Install dependencies
pip install -r requirements_hf.txt

# Run locally
python app.py
```

## Environment Variables (Optional)

- `HF_TOKEN`: Hugging Face token for Inference API (optional, increases rate limits)
- `MODEL_ID`: Custom model ID (default: `Qwen/Qwen2.5-7B-Instruct`)

## License

MIT License
