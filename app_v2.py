"""
Deep Research AI - HuggingFace Spaces
Wikipedia search with robust error handling.
"""

import gradio as gr
import urllib.parse
import urllib.request
import json


def search_wikipedia(query: str, max_results: int = 5) -> list:
    """Search Wikipedia using urllib (more compatible)."""
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&format=json&srlimit={max_results}"
        
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'DeepResearchAI/1.0 (Educational Project)'}
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
        
        results = []
        for item in data.get("query", {}).get("search", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            snippet = snippet.replace('<span class="searchmatch">', "**")
            snippet = snippet.replace("</span>", "**")
            page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
            results.append({
                "title": title,
                "url": page_url,
                "snippet": snippet
            })
        
        return results, None
    except urllib.error.HTTPError as e:
        return [], f"HTTP Error: {e.code} - {e.reason}"
    except urllib.error.URLError as e:
        return [], f"URL Error: {e.reason}"
    except json.JSONDecodeError as e:
        return [], f"JSON Error: {e}"
    except Exception as e:
        return [], f"Error: {type(e).__name__}: {e}"


def research(query: str, num_sources: int = 5) -> tuple:
    """Research a query using Wikipedia."""
    if not query or not query.strip():
        return "Please enter a research query.", ""
    
    sources, error = search_wikipedia(query.strip(), int(num_sources))
    
    if error:
        return f"⚠️ Search failed: {error}", ""
    
    if not sources:
        return "No results found for this query.", ""
    
    # Format answer
    answer_lines = [f"# 🔍 Research Results: {query}", ""]
    source_lines = ["# 📚 Sources", ""]
    
    for i, s in enumerate(sources, 1):
        answer_lines.append(f"## [{i}] {s['title']}")
        answer_lines.append(f"{s['snippet']}")
        answer_lines.append("")
        
        source_lines.append(f"**[{i}] [{s['title']}]({s['url']})**")
        source_lines.append("")
    
    return "\n".join(answer_lines), "\n".join(source_lines)


# Create Gradio app
with gr.Blocks(title="Deep Research AI", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
# 🔍 Deep Research AI

Search Wikipedia and get curated research results.
    """)
    
    with gr.Row():
        with gr.Column(scale=4):
            query_input = gr.Textbox(
                label="Research Query",
                placeholder="Enter your research question...",
                lines=2
            )
        with gr.Column(scale=1):
            num_sources = gr.Slider(
                minimum=3,
                maximum=10,
                value=5,
                step=1,
                label="Sources"
            )
            search_btn = gr.Button("🔍 Search", variant="primary")
    
    with gr.Tabs():
        with gr.TabItem("📝 Results"):
            answer_output = gr.Markdown(value="*Enter a query and click Search*")
        with gr.TabItem("📚 Sources"):
            sources_output = gr.Markdown(value="*Sources will appear here*")
    
    gr.Examples(
        examples=[
            ["What is quantum computing?"],
            ["How does photosynthesis work?"],
            ["History of artificial intelligence"],
        ],
        inputs=query_input
    )
    
    search_btn.click(
        fn=research,
        inputs=[query_input, num_sources],
        outputs=[answer_output, sources_output]
    )
    
    query_input.submit(
        fn=research,
        inputs=[query_input, num_sources],
        outputs=[answer_output, sources_output]
    )
    
    gr.Markdown("---\n*Powered by Wikipedia API and Gradio*")


if __name__ == "__main__":
    app.launch()
