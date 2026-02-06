"""
Deep Research AI - Hugging Face Spaces
Simple, robust version that works reliably on HF Spaces.
"""

import asyncio
import os
import traceback

import gradio as gr

# Configuration
HF_TOKEN = os.environ.get("HF_TOKEN", "")
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

# Global clients
llm_client = None
search_client = None
init_status = {"llm": "not_init", "search": "not_init", "errors": []}


def initialize():
    """Initialize all components with detailed error tracking."""
    global llm_client, search_client, init_status
    
    # Initialize LLM
    try:
        from src.llm_client_hf import create_hf_client
        llm_client = create_hf_client(
            model_size="medium",
            use_inference_api=True,
            hf_token=HF_TOKEN if HF_TOKEN else None
        )
        init_status["llm"] = "ok"
    except Exception as e:
        init_status["llm"] = f"error: {e}"
        init_status["errors"].append(f"LLM: {e}")
    
    # Initialize Search (with fallback)
    try:
        from src.search_multi import MultiSearch
        search_client = MultiSearch(max_results=5)
        init_status["search"] = "ok (multi-backend)"
    except Exception as e:
        init_status["search"] = f"error: {e}"
        init_status["errors"].append(f"Search: {e}")


# Initialize on module load
initialize()


async def perform_search(query, num_results=5):
    """Perform web search with detailed error handling."""
    if search_client is None:
        return [], f"Search client not initialized: {init_status['search']}"
    
    try:
        results = await search_client.search(query, max_results=num_results)
        sources = []
        for r in results:
            sources.append({
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "domain": r.domain
            })
        return sources, None
    except Exception as e:
        error_details = traceback.format_exc()
        return [], f"Search failed: {e}\n{error_details}"


async def synthesize_answer(query, sources):
    """Synthesize answer from sources using LLM."""
    if llm_client is None:
        return f"LLM not available: {init_status['llm']}", "error"
    
    if not sources:
        return "No sources were found to synthesize an answer from.", "no_sources"
    
    try:
        # Build sources text
        sources_parts = []
        for i, s in enumerate(sources, 1):
            part = f"Source {i}: {s['title']}\n{s['snippet']}\nURL: {s['url']}"
            sources_parts.append(part)
        sources_text = "\n\n".join(sources_parts)
        
        prompt = f"""You are a research assistant. Based on the following sources, provide a comprehensive answer.

QUERY: {query}

SOURCES:
{sources_text}

Provide a clear, factual answer citing sources as [1], [2], etc."""

        answer = await llm_client.call(prompt)
        return answer, None
    except Exception as e:
        return f"LLM synthesis failed: {e}", "error"


async def research_async(query, num_sources, include_news):
    """Main async research function."""
    debug_info = []
    debug_info.append(f"Query: {query}")
    debug_info.append(f"Init status: LLM={init_status['llm']}, Search={init_status['search']}")
    
    # Check initialization
    if init_status["errors"]:
        error_msg = "Initialization errors:\n" + "\n".join(init_status["errors"])
        return error_msg, "No sources (init failed)", "0%"
    
    # Perform search
    debug_info.append("Starting search...")
    sources, search_error = await perform_search(query, int(num_sources))
    debug_info.append(f"Search returned {len(sources)} sources")
    
    if search_error:
        debug_info.append(f"Search error: {search_error}")
        return f"Search failed:\n{search_error}", "No sources", "0%"
    
    if not sources:
        debug_info.append("No sources found")
        return "No sources were found for this query. DuckDuckGo may not have results for this topic.", "No sources found", "0%"
    
    # Format sources for display
    source_lines = []
    for i, s in enumerate(sources, 1):
        title = s.get("title", "Unknown")
        url = s.get("url", "#")
        domain = s.get("domain", "unknown")
        snippet = s.get("snippet", "")[:150]
        source_lines.append(f"**[{i}] {title}**\n[{domain}]({url})\n_{snippet}..._")
    sources_display = "\n\n".join(source_lines)
    
    # Synthesize answer
    debug_info.append("Starting synthesis...")
    answer, synth_error = await synthesize_answer(query, sources)
    
    if synth_error:
        debug_info.append(f"Synthesis error: {synth_error}")
        # Still show sources even if synthesis fails
        return f"Could not synthesize answer: {answer}", sources_display, "0%"
    
    # Calculate confidence
    conf = min(len(sources) / int(num_sources), 1.0)
    confidence = f"**Confidence:** {conf:.0%} ({len(sources)} sources)"
    
    return answer, sources_display, confidence


def research(query, num_sources=5, include_news=False):
    """Sync wrapper for Gradio."""
    if not query or not query.strip():
        return "Please enter a research query.", "", ""
    
    try:
        return asyncio.run(research_async(query.strip(), num_sources, include_news))
    except Exception as e:
        error_trace = traceback.format_exc()
        return f"Error: {e}\n\nDetails:\n{error_trace}", "", ""


# Build Gradio UI
with gr.Blocks(title="Deep Research AI", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
# 🔍 Deep Research AI

AI-powered research assistant using web search and language models.

**How it works:**
1. Enter your research question
2. Click "Research" to search the web
3. AI synthesizes an answer from the sources
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="Research Query",
                placeholder="Enter your research question...",
                lines=2
            )
        with gr.Column(scale=1):
            num_sources = gr.Slider(3, 10, value=5, step=1, label="Sources")
            include_news = gr.Checkbox(label="Include News", value=False)
            research_btn = gr.Button("🔍 Research", variant="primary")
    
    with gr.Tabs():
        with gr.TabItem("📝 Answer"):
            answer_output = gr.Markdown(value="*Enter a query above*")
            confidence_output = gr.Markdown()
        with gr.TabItem("📚 Sources"):
            sources_output = gr.Markdown(value="*Sources will appear here*")
    
    gr.Examples(
        examples=[
            ["What are the benefits of renewable energy?"],
            ["How does machine learning work?"],
            ["What is quantum computing?"]
        ],
        inputs=query_input
    )
    
    research_btn.click(
        fn=research,
        inputs=[query_input, num_sources, include_news],
        outputs=[answer_output, sources_output, confidence_output]
    )
    
    query_input.submit(
        fn=research,
        inputs=[query_input, num_sources, include_news],
        outputs=[answer_output, sources_output, confidence_output]
    )
    
    gr.Markdown(f"""
---
**Status:** LLM={init_status['llm']}, Search={init_status['search']}

Uses DuckDuckGo (free) + Qwen 2.5 (HuggingFace)
    """)


if __name__ == "__main__":
    app.launch()
