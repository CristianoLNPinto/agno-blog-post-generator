"""Content scraper agent for extracting article content."""

from textwrap import dedent

from agno.agent import Agent
from agno.tools.newspaper4k import Newspaper4kTools

from ...infrastructure.llm_providers import get_model
from ..models import ScrapedArticle


# Scraper agent uses tools, so get_model(use_tools=True) automatically selects Gemini
# (Groq doesn't support JSON mode + tools together)
content_scraper_agent = Agent(
    name="Content Scraper Agent",
    model=get_model(use_tools=True),  # Smart factory: uses Gemini for tools
    tools=[Newspaper4kTools()],
    description=dedent("""\
    You are ContentBot-X, a specialist in extracting and processing digital content
    for blog creation. Your expertise includes:

    - Efficient content extraction
    - Smart formatting and structuring
    - Key information identification
    - Quote and statistic preservation
    - Maintaining source attribution
    """),
    instructions=dedent("""\
    1. Content Extraction 📑
       - Extract content from the article
       - Preserve important quotes and statistics
       - Maintain proper attribution
       - Handle paywalls gracefully
    2. Content Processing 🔄
       - Format text in clean markdown
       - Preserve key information
       - Structure content logically
    3. Quality Control ✅
       - Verify content relevance
       - Ensure accurate extraction
       - Maintain readability
    """),
    output_schema=ScrapedArticle,
)
