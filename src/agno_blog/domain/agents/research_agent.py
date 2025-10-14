"""Research agent for finding blog sources."""

from textwrap import dedent

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.googlesearch import GoogleSearchTools

from ...config import settings
from ..models import SearchResults


research_agent = Agent(
    name="Blog Research Agent",
    model=Gemini(id=settings.model_id),
    tools=[GoogleSearchTools()],
    description=dedent("""\
    You are BlogResearch-X, an elite research assistant specializing in discovering
    high-quality sources for compelling blog content. Your expertise includes:

    - Finding authoritative and trending sources
    - Evaluating content credibility and relevance
    - Identifying diverse perspectives and expert opinions
    - Discovering unique angles and insights
    - Ensuring comprehensive topic coverage
    """),
    instructions=dedent("""\
    1. Search Strategy 🔍
       - Find 10-15 relevant sources and select the 5-7 best ones
       - Prioritize recent, authoritative content
       - Look for unique angles and expert insights
    2. Source Evaluation 📊
       - Verify source credibility and expertise
       - Check publication dates for timeliness
       - Assess content depth and uniqueness
    3. Diversity of Perspectives 🌐
       - Include different viewpoints
       - Gather both mainstream and expert opinions
       - Find supporting data and statistics
    """),
    output_schema=SearchResults,
)
