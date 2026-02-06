"""
Deep Research AI - Hugging Face Spaces
Self-contained version with no external dependencies on src modules.
"""

import asyncio
import os
import traceback
import urllib.parse
from dataclasses import dataclass

import httpx
import gradio as gr

# Configuration
HF_TOKEN = os.environ.get("HF_TOKEN", "")
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"


@dataclass
class SearchResult:
    """Search result."""
    title: str
    url: str
    snippet: str
    domain: str


class WikipediaSearch:
    """Wikipedia search - always works."""
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
    
    async def search(self, query: str, max_results: int = None) -> list[SearchResult]:
        """Search Wikipedia."""
        max_results = max_results or self.max_results
        
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&format=json&srlimit={max_results}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            results = []
            for item in data.get("query", {}).get("search", []):
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                # Clean HTML from snippet
                snippet = snippet.replace('<span class="searchmatch">', "")
                snippet = snippet.replace("</span>", "")
                page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                
                results.append(SearchResult(
                    title=title,
                    url=page_url,
                    snippet=snippet,
                    domain="wikipedia.org"
                ))
            
            return results
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []
    
    async def search_news(self, query: str, max_results: int = None) -> list[SearchResult]:
        """For news, just use regular search."""
        return await self.search(query, max_results)


class SimpleLLM:
    """Simple LLM client using HuggingFace Inference API."""
    
    def __init__(self, model_id: str = MODEL_ID, token: str = None):
        self.model_id = model_id
        self.token = token
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from huggingface_hub import InferenceClient
                self._client = InferenceClient(
                    model=self.model_id,
                    token=self.token if self.token else None
                )
            except Exception as e:
                print(f"Failed to create InferenceClient: {e}")
        return self._client
    
    async def call(self, prompt: str, max_tokens: int = 1024) -> str:
        """Call the LLM."""
        client = self._get_client()
        if client is None:
            return "LLM client not available"
        
        try:
            loop = asyncio.get_event_loop()
            
            def do_call():
                response = client.text_generation(
                    prompt,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    do_sample=True
                )
                return response
            
            result = await loop.run_in_executor(None, do_call)
            return result
        except Exception as e:
            return f"LLM error: {str(e)}"


# Initialize clients
search_client = WikipediaSearch(max_results=5)
llm_client = SimpleLLM(model_id=MODEL_ID, token=HF_TOKEN if HF_TOKEN else None)


async def perform_search(query: str, num_results: int = 5) -> tuple[list, str]:
    """Perform search."""
    try:
        results = await search_client.search(query, max_results=num_results)
        sources = [
            {
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "domain": r.domain
            }
            for r in results
        ]
        return sources, None
    except Exception as e:
        return [], f"Search error: {str(e)}"


async def synthesize_answer(query: str, sources: list) -> tuple[str, str]:
    """Synthesize answer from sources."""
    if not sources:
        return "No sources available to synthesize an answer.", "no_sources"
    
    try:
        # Build sources text
        parts = []
        for i, s in enumerate(sources, 1):
            parts.append(f"Source {i}: {s['title']}\n{s['snippet']}\nURL: {s['url']}")
        sources_text = "\n\n".join(parts)
        
        prompt = f"""Based on the following sources, provide a comprehensive answer to the query.

QUERY: {query}

SOURCES:
{sources_text}

Provide a clear, factual answer. Cite sources as [1], [2], etc.

ANSWER:"""

        answer = await llm_client.call(prompt)
        return answer, None
    except Exception as e:
        return f"Synthesis error: {str(e)}", "error"


async def research_async(query: str, num_sources: int, include_news: bool) -> tuple[str, str, str]:
    """Main async research function."""
    # Perform search
    sources, search_error = await perform_search(query, int(num_sources))
    
    if search_error:
        return f"Search failed: {search_error}", "No sources", "0%"
    
    if not sources:
        return "No sources found for this query.", "No sources found", "0%"
    
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
    answer, synth_error = await synthesize_answer(query, sources)
    
    if synth_error:
        return f"Could not synthesize answer: {answer}", sources_display, "0%"
    
    # Calculate confidence
    conf = min(len(sources) / int(num_sources), 1.0)
    confidence = f"**Confidence:** {conf:.0%} ({len(sources)} sources)"
    
    return answer, sources_display, confidence


def research(query: str, num_sources: int = 5, include_news: bool = False) -> tuple[str, str, str]:
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

AI-powered research assistant using Wikipedia search and language models.

**How it works:**
1. Enter your research question
2. Click "Research" to search Wikipedia
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
            ["What is artificial intelligence?"],
            ["How does renewable energy work?"],
            ["What is quantum computing?"],
            ["Explain climate change"],
            ["What are black holes?"]
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
    
    gr.Markdown("""
---
**Powered by:** Wikipedia API + Qwen 2.5 (HuggingFace Inference)

*This is a demo using free-tier services. For better results, deploy with API keys.*
    """)


if __name__ == "__main__":
    app.launch()
