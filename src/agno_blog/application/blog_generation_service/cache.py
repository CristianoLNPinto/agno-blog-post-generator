"""Cache management for blog generation."""

from typing import Dict, Optional

from agno.utils.log import logger

from ...domain.models import ScrapedArticle, SearchResults


def get_cached_blog_post(session_state, topic: str) -> Optional[str]:
    """Get cached blog post from workflow session state."""
    logger.info("Checking if cached blog post exists")
    return session_state.get("blog_posts", {}).get(topic)


def cache_blog_post(session_state, topic: str, blog_post: str):
    """Cache blog post in workflow session state."""
    logger.info(f"Saving blog post for topic: {topic}")
    if "blog_posts" not in session_state:
        session_state["blog_posts"] = {}
    session_state["blog_posts"][topic] = blog_post


def get_cached_search_results(session_state, topic: str) -> Optional[SearchResults]:
    """Get cached search results from workflow session state."""
    logger.info("Checking if cached search results exist")
    search_results = session_state.get("search_results", {}).get(topic)
    if search_results and isinstance(search_results, dict):
        try:
            return SearchResults.model_validate(search_results)
        except Exception as e:
            logger.warning(f"Could not validate cached search results: {e}")
    return search_results if isinstance(search_results, SearchResults) else None


def cache_search_results(session_state, topic: str, search_results: SearchResults):
    """Cache search results in workflow session state."""
    logger.info(f"Saving search results for topic: {topic}")
    if "search_results" not in session_state:
        session_state["search_results"] = {}
    session_state["search_results"][topic] = search_results.model_dump()


def get_cached_scraped_articles(
    session_state, topic: str
) -> Optional[Dict[str, ScrapedArticle]]:
    """Get cached scraped articles from workflow session state."""
    logger.info("Checking if cached scraped articles exist")
    scraped_articles = session_state.get("scraped_articles", {}).get(topic)
    if scraped_articles and isinstance(scraped_articles, dict):
        try:
            return {
                url: ScrapedArticle.model_validate(article)
                for url, article in scraped_articles.items()
            }
        except Exception as e:
            logger.warning(f"Could not validate cached scraped articles: {e}")
    return scraped_articles if isinstance(scraped_articles, dict) else None


def cache_scraped_articles(
    session_state, topic: str, scraped_articles: Dict[str, ScrapedArticle]
):
    """Cache scraped articles in workflow session state."""
    logger.info(f"Saving scraped articles for topic: {topic}")
    if "scraped_articles" not in session_state:
        session_state["scraped_articles"] = {}
    session_state["scraped_articles"][topic] = {
        url: article.model_dump() for url, article in scraped_articles.items()
    }
