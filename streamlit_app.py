"""🎨 Streamlit Interface for Agno Blog Post Generator

A beautiful and interactive web interface for generating AI-powered blog posts
with real-time progress tracking and HTML output.
"""

import asyncio
import io
import sys
from contextlib import redirect_stdout
from datetime import datetime

import markdown
import streamlit as st
from agno.workflow.workflow import Workflow

from src.agno_blog.application.blog_generation_service import BlogGenerationService
from src.agno_blog.infrastructure.db import get_workflow_db
from src.agno_blog.infrastructure.observability import (
    get_comet_tracker,
    instrument_agno_globally,
)


# Page configuration
st.set_page_config(
    page_title="Agno Blog Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Opik LLM tracing globally (once at startup)
if "opik_instrumented" not in st.session_state:
    instrument_agno_globally()
    st.session_state.opik_instrumented = True

# Initialize workflow once and reuse it
if "workflow" not in st.session_state:
    st.session_state.workflow = None

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .phase-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .source-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    .blog-output {
        background: white;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


class ProgressCapture:
    """Captures print statements for progress tracking."""

    def __init__(self):
        self.output = []
        self.phase = None
        self.sources = []
        self.scraped_articles = []

    def write(self, text):
        """Capture output text."""
        if text.strip():
            self.output.append(text)

            # Parse phase information
            if "PHASE 1" in text:
                self.phase = "research"
            elif "PHASE 2" in text:
                self.phase = "extraction"
            elif "PHASE 3" in text:
                self.phase = "writing"

            # Capture source information
            if "Found" in text and "relevant articles" in text:
                pass  # Will be captured from search results
            elif "✅ Found" in text and "articles" in text:
                pass  # Already captured

    def flush(self):
        """Flush method required for file-like object."""
        pass


async def generate_blog_post_async(topic: str, progress_container, status_container):
    """Generate blog post with progress tracking."""

    # Initialize Comet ML tracker
    tracker = get_comet_tracker(force_new=True)
    
    # Initialize service with tracker
    service = BlogGenerationService(tracker=tracker)

    # Create workflow execution function
    async def blog_generation_execution(session_state, topic: str = None, **kwargs):
        """Workflow execution function with progress tracking."""
        return await service.generate_blog_post(session_state, topic, **kwargs)

    # Reuse workflow instance to maintain session state
    # Create workflow only if it doesn't exist
    if st.session_state.workflow is None:
        st.session_state.workflow = Workflow(
            name="Blog Post Generator",
            description="Advanced blog post generator with research and content creation capabilities",
            db=get_workflow_db(),
            steps=blog_generation_execution,
            session_id="streamlit_blog_generator",  # Fixed session ID for cache persistence
            session_state={},  # Initial state for new sessions
        )
    
    workflow = st.session_state.workflow

    # Capture stdout for progress tracking
    progress_capture = ProgressCapture()
    original_stdout = sys.stdout

    try:
        # Phase tracking
        with progress_container:
            st.markdown("### 🔄 Generation Progress")

            phase1_status = st.empty()
            phase1_details = st.empty()

            phase2_status = st.empty()
            phase2_details = st.empty()

            phase3_status = st.empty()
            phase3_details = st.empty()

        # Redirect stdout
        sys.stdout = progress_capture

        # Start generation
        phase1_status.info("🔍 **Phase 1:** Researching sources...")

        # Run workflow
        resp = await workflow.arun(
            topic=topic,
            use_search_cache=True,
            use_scrape_cache=True,
            use_blog_cache=True,
        )

        # Restore stdout
        sys.stdout = original_stdout

        # Parse output for progress information
        output_text = "\n".join(progress_capture.output)

        # Extract search results
        if "Found" in output_text and "relevant sources:" in output_text:
            phase1_status.success("✅ **Phase 1:** Research completed")
            sources_section = output_text.split("relevant sources:")[1].split("PHASE 2")[0]
            sources = [
                line.strip() for line in sources_section.split("\n") if line.strip()
            ]
            if sources:
                phase1_details.markdown("**Sources found:**")
                for source in sources[:5]:  # Show first 5
                    phase1_details.markdown(f"- {source}")

        # Extract scraping results
        if "Successfully extracted content" in output_text:
            phase2_status.success("✅ **Phase 2:** Content extraction completed")
            # Count scraped articles
            scraped_count = output_text.count("✅ Successfully scraped:")
            if scraped_count > 0:
                phase2_details.info(f"📄 Extracted content from {scraped_count} articles")

        # Writing phase
        if "Blog post generated successfully" in output_text:
            phase3_status.success("✅ **Phase 3:** Blog post created")
            # Extract stats
            if "Length:" in output_text:
                length_line = [
                    line for line in output_text.split("\n") if "Length:" in line
                ][0]
                phase3_details.info(f"📝 {length_line.strip()}")

        # Get the blog post content
        if resp and resp.content:
            # End the Comet ML experiment
            tracker.end()
            return resp.content
        else:
            tracker.log_metric("generation_failed", 1)
            tracker.end()
            return None

    except Exception as e:
        sys.stdout = original_stdout
        tracker.log_other("exception", str(e))
        tracker.log_metric("generation_error", 1)
        tracker.end()
        st.error(f"❌ Error generating blog post: {str(e)}")
        return None


def markdown_to_html(markdown_text: str) -> str:
    """Convert markdown to HTML with styling."""
    html = markdown.markdown(
        markdown_text,
        extensions=["extra", "codehilite", "toc"],
    )

    # Add custom styling
    styled_html = f"""
    <div class="blog-output">
        <style>
            .blog-output h1 {{
                color: #667eea;
                border-bottom: 3px solid #667eea;
                padding-bottom: 0.5rem;
                margin-bottom: 1.5rem;
            }}
            .blog-output h2 {{
                color: #764ba2;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }}
            .blog-output h3 {{
                color: #667eea;
                margin-top: 1.5rem;
            }}
            .blog-output p {{
                line-height: 1.8;
                margin-bottom: 1rem;
                color: #333;
            }}
            .blog-output ul, .blog-output ol {{
                line-height: 1.8;
                margin-bottom: 1rem;
            }}
            .blog-output a {{
                color: #667eea;
                text-decoration: none;
            }}
            .blog-output a:hover {{
                text-decoration: underline;
            }}
            .blog-output code {{
                background: #f4f4f4;
                padding: 0.2rem 0.4rem;
                border-radius: 0.25rem;
                font-family: monospace;
            }}
            .blog-output blockquote {{
                border-left: 4px solid #667eea;
                padding-left: 1rem;
                margin-left: 0;
                color: #666;
                font-style: italic;
            }}
        </style>
        {html}
    </div>
    """
    return styled_html


def main():
    """Main Streamlit application."""

    # Header
    st.markdown('<h1 class="main-header">🎨 Agno Blog Generator</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">AI-Powered Blog Post Generation with Real-Time Progress Tracking</p>',
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Settings")

        # Cache options
        st.markdown("### 💾 Cache Options")
        use_search_cache = st.checkbox("Use search cache", value=True)
        use_scrape_cache = st.checkbox("Use scrape cache", value=True)
        use_blog_cache = st.checkbox("Use blog cache", value=True)

        st.markdown("---")

        # Information
        st.markdown("### ℹ️ About")
        st.info(
            """
            This tool generates professional blog posts using AI:
            
            1. **Research:** Finds relevant sources
            2. **Extract:** Scrapes article content
            3. **Write:** Creates engaging blog post
            
            The process takes 1-3 minutes depending on the topic.
            """
        )

        st.markdown("---")

        # Example topics
        st.markdown("### 💡 Example Topics")
        example_topics = [
            "The Future of AI in Healthcare",
            "Sustainable Living Tips for 2024",
            "How Quantum Computing Works",
            "The Rise of Remote Work",
            "Space Tourism: Current State",
        ]

        for topic in example_topics:
            if st.button(topic, key=f"example_{topic}"):
                st.session_state.topic_input = topic

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Topic input
        topic = st.text_input(
            "📝 Enter your blog topic:",
            value=st.session_state.get("topic_input", ""),
            placeholder="e.g., The Impact of AI on Modern Education",
            key="topic_field",
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_button = st.button("🚀 Generate Blog Post", type="primary")

    # Progress and output containers
    progress_container = st.container()
    status_container = st.container()
    output_container = st.container()

    # Generate blog post
    if generate_button:
        if not topic:
            st.warning("⚠️ Please enter a topic for your blog post.")
        else:
            # Clear previous output
            st.session_state.blog_post = None

            with st.spinner("🎨 Generating your blog post..."):
                # Run async generation
                blog_post = asyncio.run(
                    generate_blog_post_async(topic, progress_container, status_container)
                )

                if blog_post:
                    st.session_state.blog_post = blog_post
                    st.session_state.generation_time = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    st.success("✅ Blog post generated successfully!")
                    st.rerun()

    # Display generated blog post
    if "blog_post" in st.session_state and st.session_state.blog_post:
        with output_container:
            st.markdown("---")
            st.markdown("## 📄 Generated Blog Post")

            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📖 HTML View", "📝 Markdown", "💾 Download"])

            with tab1:
                # HTML view
                html_content = markdown_to_html(st.session_state.blog_post)
                st.markdown(html_content, unsafe_allow_html=True)

            with tab2:
                # Markdown view
                st.markdown(st.session_state.blog_post)

            with tab3:
                # Download options
                st.markdown("### Download Options")

                col1, col2 = st.columns(2)

                with col1:
                    # Download as Markdown
                    st.download_button(
                        label="📥 Download as Markdown",
                        data=st.session_state.blog_post,
                        file_name=f"blog_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                    )

                with col2:
                    # Download as HTML
                    html_full = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Blog Post</title>
                        <style>
                            body {{
                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                                max-width: 800px;
                                margin: 0 auto;
                                padding: 2rem;
                                line-height: 1.6;
                            }}
                        </style>
                    </head>
                    <body>
                        {markdown_to_html(st.session_state.blog_post)}
                    </body>
                    </html>
                    """

                    st.download_button(
                        label="📥 Download as HTML",
                        data=html_full,
                        file_name=f"blog_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                    )

            # Metadata
            if "generation_time" in st.session_state:
                st.caption(f"Generated at: {st.session_state.generation_time}")


if __name__ == "__main__":
    main()
