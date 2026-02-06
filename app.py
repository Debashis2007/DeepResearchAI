"""
Gradio App for Deep Research AI - Hugging Face Spaces Deployment

This creates a web interface for the research system that can be
deployed directly to Hugging Face Spaces.
"""

import asyncio
import os
from typing import Generator

import gradio as gr

# Use direct imports to avoid circular dependency issues
from src.llm_client_hf import HuggingFaceLLMClient, create_hf_client
from src.search_duckduckgo import DuckDuckGoSearch


# Configuration
HF_TOKEN = os.environ.get("HF_TOKEN", "")
MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-7B-Instruct")


class SimpleResearcher:
    """
    Simplified researcher for Hugging Face Spaces.
    
    Uses free models and DuckDuckGo search.
    """
    
    def __init__(self):
        self.llm = create_hf_client(
            model_size="medium",
            use_inference_api=True,
            hf_token=HF_TOKEN
        )
        self.search = DuckDuckGoSearch(max_results=5)
    
    async def research(
        self,
        query: str,
        num_sources: int = 5,
        include_news: bool = False
    ) -> dict:
        """
        Perform research on a query.
        
        Args:
            query: Research query
            num_sources: Number of sources to use
            include_news: Include news search
            
        Returns:
            Research results dictionary
        """
        results = {
            "query": query,
            "sources": [],
            "answer": "",
            "confidence": 0.0
        }
        
        try:
            # Step 1: Search for information
            search_results = await self.search.search(query, max_results=num_sources)
            
            if include_news:
                news_results = await self.search.search_news(query, max_results=3)
                search_results.extend(news_results)
            
            # Convert to sources
            sources = []
            for r in search_results[:num_sources]:
                sources.append({
                    "title": r.title,
                    "url": r.url,
                    "snippet": r.snippet,
                    "domain": r.domain
                })
            
            results["sources"] = sources
            
            # Step 2: Synthesize answer using LLM
            if sources:
                synthesis_prompt = self._build_synthesis_prompt(query, sources)
                answer = await self.llm.call(synthesis_prompt)
                results["answer"] = answer
                results["confidence"] = min(len(sources) / num_sources, 1.0)
            else:
                results["answer"] = "I couldn't find relevant information for this query."
                results["confidence"] = 0.0
            
        except Exception as e:
            results["answer"] = f"Research encountered an error: {str(e)}"
            results["confidence"] = 0.0
        
        return results
    
    def _build_synthesis_prompt(self, query: str, sources: list[dict]) -> str:
        """Build synthesis prompt from sources."""
        sources_text = "\n\n".join([
            f"**Source {i+1}: {s['title']}**\n{s['snippet']}\nURL: {s['url']}"
            for i, s in enumerate(sources)
        ])
        
        return f"""You are a research assistant. Based on the following sources, provide a comprehensive answer to the query.

QUERY: {query}

SOURCES:
{sources_text}

INSTRUCTIONS:
1. Synthesize information from all relevant sources
2. Provide a clear, well-structured answer
3. Cite sources using [1], [2], etc.
4. Acknowledge any limitations or conflicting information
5. Be objective and factual

ANSWER:"""


# Create researcher instance
researcher = SimpleResearcher()


def format_sources(sources: list[dict]) -> str:
    """Format sources for display."""
    if not sources:
        return "No sources found."
    
    formatted = []
    for i, s in enumerate(sources, 1):
        formatted.append(
            f"**[{i}] {s['title']}**\n"
            f"🔗 [{s['domain']}]({s['url']})\n"
            f"_{s['snippet'][:200]}..._\n"
        )
    
    return "\n".join(formatted)


def format_result(result: dict) -> tuple[str, str, str]:
    """Format research result for display."""
    answer = result.get("answer", "No answer generated.")
    sources = format_sources(result.get("sources", []))
    confidence = f"**Confidence:** {result.get('confidence', 0):.0%}"
    
    return answer, sources, confidence


async def research_async(
    query: str,
    num_sources: int,
    include_news: bool
) -> tuple[str, str, str]:
    """Async research function."""
    result = await researcher.research(
        query=query,
        num_sources=int(num_sources),
        include_news=include_news
    )
    return format_result(result)


def research(
    query: str,
    num_sources: int = 5,
    include_news: bool = False
) -> tuple[str, str, str]:
    """
    Main research function for Gradio.
    
    Args:
        query: Research query
        num_sources: Number of sources
        include_news: Include news search
        
    Returns:
        Tuple of (answer, sources, confidence)
    """
    if not query.strip():
        return "Please enter a research query.", "", ""
    
    return asyncio.run(research_async(query, num_sources, include_news))


# Create Gradio interface
def create_app() -> gr.Blocks:
    """Create the Gradio app."""
    
    with gr.Blocks(
        title="Deep Research AI",
        theme=gr.themes.Soft(),
        css="""
        .container { max-width: 900px; margin: auto; }
        .header { text-align: center; margin-bottom: 20px; }
        """
    ) as app:
        
        gr.Markdown(
            """
            # 🔍 Deep Research AI
            
            An AI-powered research assistant that searches the web and synthesizes 
            information to answer your questions.
            
            **Features:**
            - 🌐 Real-time web search (DuckDuckGo)
            - 🤖 AI-powered synthesis (Qwen 2.5)
            - 📰 Optional news search
            - 📚 Source citations
            """,
            elem_classes=["header"]
        )
        
        with gr.Row():
            with gr.Column(scale=3):
                query_input = gr.Textbox(
                    label="Research Query",
                    placeholder="Enter your research question...",
                    lines=2,
                    max_lines=4
                )
            
            with gr.Column(scale=1):
                num_sources = gr.Slider(
                    minimum=3,
                    maximum=10,
                    value=5,
                    step=1,
                    label="Number of Sources"
                )
                include_news = gr.Checkbox(
                    label="Include News",
                    value=False
                )
                research_btn = gr.Button(
                    "🔍 Research",
                    variant="primary",
                    size="lg"
                )
        
        with gr.Tabs():
            with gr.TabItem("📝 Answer"):
                answer_output = gr.Markdown(
                    label="Research Answer",
                    value="*Enter a query and click Research*"
                )
                confidence_output = gr.Markdown()
            
            with gr.TabItem("📚 Sources"):
                sources_output = gr.Markdown(
                    label="Sources",
                    value="*Sources will appear here*"
                )
        
        # Examples
        gr.Examples(
            examples=[
                ["What are the latest developments in quantum computing?"],
                ["Compare the benefits of Python vs Rust for systems programming"],
                ["Explain how large language models work"],
                ["What is the current state of renewable energy adoption?"],
                ["How does CRISPR gene editing work?"],
            ],
            inputs=query_input,
            label="Example Queries"
        )
        
        # Connect button
        research_btn.click(
            fn=research,
            inputs=[query_input, num_sources, include_news],
            outputs=[answer_output, sources_output, confidence_output]
        )
        
        # Also trigger on Enter
        query_input.submit(
            fn=research,
            inputs=[query_input, num_sources, include_news],
            outputs=[answer_output, sources_output, confidence_output]
        )
        
        gr.Markdown(
            """
            ---
            **Note:** This uses DuckDuckGo for search (no API key required) and 
            Qwen 2.5 for synthesis. Results may vary based on available sources.
            
            Made with ❤️ using Gradio and Hugging Face
            """
        )
    
    return app


# Create and launch app
app = create_app()

if __name__ == "__main__":
    app.launch()
