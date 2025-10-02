"""Blog generation service - main orchestration logic."""

import json
from typing import Dict, Optional

from agno.utils.log import logger

from ...config import settings
from ...domain.agents import blog_writer_agent, content_scraper_agent, research_agent
from ...domain.models import ScrapedArticle, SearchResults
from .cache import (
    cache_blog_post,
    cache_scraped_articles,
    cache_search_results,
    get_cached_blog_post,
    get_cached_scraped_articles,
    get_cached_search_results,
)


class BlogGenerationService:
    """Service for generating blog posts with research and content extraction."""

    def __init__(self):
        self.research_agent = research_agent
        self.scraper_agent = content_scraper_agent
        self.writer_agent = blog_writer_agent

    async def get_search_results(
        self, session_state, topic: str, use_cache: bool = True
    ) -> Optional[SearchResults]:
        """Get search results with caching support."""
        # Check cache first
        if use_cache:
            cached_results = get_cached_search_results(session_state, topic)
            if cached_results:
                logger.info(f"Found {len(cached_results.articles)} articles in cache.")
                return cached_results

        # Search for new results
        for attempt in range(settings.max_search_attempts):
            try:
                print(
                    f"🔍 Searching for articles about: {topic} (attempt {attempt + 1}/{settings.max_search_attempts})"
                )
                response = await self.research_agent.arun(topic)

                if (
                    response
                    and response.content
                    and isinstance(response.content, SearchResults)
                ):
                    article_count = len(response.content.articles)
                    logger.info(f"Found {article_count} articles on attempt {attempt + 1}")
                    print(f"✅ Found {article_count} relevant articles")

                    # Cache the results
                    cache_search_results(session_state, topic, response.content)
                    return response.content
                else:
                    logger.warning(
                        f"Attempt {attempt + 1}/{settings.max_search_attempts} failed: Invalid response type"
                    )

            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{settings.max_search_attempts} failed: {str(e)}"
                )

        logger.error(
            f"Failed to get search results after {settings.max_search_attempts} attempts"
        )
        return None

    async def scrape_articles(
        self,
        session_state,
        topic: str,
        search_results: SearchResults,
        use_cache: bool = True,
    ) -> Dict[str, ScrapedArticle]:
        """Scrape articles with caching support."""
        # Check cache first
        if use_cache:
            cached_articles = get_cached_scraped_articles(session_state, topic)
            if cached_articles:
                logger.info(f"Found {len(cached_articles)} scraped articles in cache.")
                return cached_articles

        scraped_articles: Dict[str, ScrapedArticle] = {}

        print(f"📄 Scraping {len(search_results.articles)} articles...")

        for i, article in enumerate(search_results.articles, 1):
            try:
                print(
                    f"📖 Scraping article {i}/{len(search_results.articles)}: {article.title[:50]}..."
                )
                response = await self.scraper_agent.arun(article.url)

                if (
                    response
                    and response.content
                    and isinstance(response.content, ScrapedArticle)
                ):
                    scraped_articles[response.content.url] = response.content
                    logger.info(f"Scraped article: {response.content.url}")
                    print(f"✅ Successfully scraped: {response.content.title[:50]}...")
                else:
                    print(f"❌ Failed to scrape: {article.title[:50]}...")

            except Exception as e:
                logger.warning(f"Failed to scrape {article.url}: {str(e)}")
                print(f"❌ Error scraping: {article.title[:50]}...")

        # Cache the scraped articles
        cache_scraped_articles(session_state, topic, scraped_articles)
        return scraped_articles

    async def generate_blog_post(
        self,
        session_state,
        topic: str,
        use_search_cache: bool = True,
        use_scrape_cache: bool = True,
        use_blog_cache: bool = True,
        **kwargs,  # Accept additional workflow kwargs
    ) -> str:
        """
        Generate a blog post about the given topic.

        Args:
            session_state: The shared session state
            topic: Blog post topic
            use_search_cache: Whether to use cached search results
            use_scrape_cache: Whether to use cached scraped articles
            use_blog_cache: Whether to use cached blog posts

        Returns:
            Generated blog post as markdown string
        """
        if not topic:
            return "❌ No blog topic provided. Please specify a topic."

        print(f"🎨 Generating blog post about: {topic}")
        print("=" * 60)

        # Check for cached blog post first
        if use_blog_cache:
            cached_blog = get_cached_blog_post(session_state, topic)
            if cached_blog:
                print("📋 Found cached blog post!")
                return cached_blog

        # Phase 1: Research and gather sources
        print("\n🔍 PHASE 1: RESEARCH & SOURCE GATHERING")
        print("=" * 50)

        search_results = await self.get_search_results(
            session_state, topic, use_search_cache
        )

        if not search_results or len(search_results.articles) == 0:
            return f"❌ Sorry, could not find any articles on the topic: {topic}"

        print(f"📊 Found {len(search_results.articles)} relevant sources:")
        for i, article in enumerate(search_results.articles, 1):
            print(f"   {i}. {article.title[:60]}...")

        # Phase 2: Content extraction
        print("\n📄 PHASE 2: CONTENT EXTRACTION")
        print("=" * 50)

        scraped_articles = await self.scrape_articles(
            session_state, topic, search_results, use_scrape_cache
        )

        if not scraped_articles:
            return f"❌ Could not extract content from any articles for topic: {topic}"

        print(f"📖 Successfully extracted content from {len(scraped_articles)} articles")

        # Phase 3: Blog post writing
        print("\n✍️ PHASE 3: BLOG POST CREATION")
        print("=" * 50)

        # Prepare input for the writer
        writer_input = {
            "topic": topic,
            "articles": [article.model_dump() for article in scraped_articles.values()],
        }

        print("🤖 AI is crafting your blog post...")
        writer_response = await self.writer_agent.arun(
            json.dumps(writer_input, indent=2)
        )

        if not writer_response or not writer_response.content:
            return f"❌ Failed to generate blog post for topic: {topic}"

        blog_post = writer_response.content

        # Cache the blog post
        cache_blog_post(session_state, topic, blog_post)

        print("✅ Blog post generated successfully!")
        print(f"📝 Length: {len(blog_post)} characters")
        print(f"📚 Sources: {len(scraped_articles)} articles")

        return blog_post
