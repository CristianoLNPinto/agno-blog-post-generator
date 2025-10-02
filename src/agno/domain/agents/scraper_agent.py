"""Content scraper agent for extracting article content."""

from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.newspaper4k import Newspaper4kTools

from ...config import settings
from ..models import ScrapedArticle


content_scraper_agent = Agent(
    name="Content Scraper Agent",
    model=Gemini(id=settings.model_id),
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
