"""Tests for blog generation service."""

import pytest

from src.agno_blog.application.blog_generation_service import BlogGenerationService
from src.agno_blog.domain.models import NewsArticle, SearchResults


class TestBlogGenerationService:
    """Test cases for BlogGenerationService."""

    @pytest.fixture
    def service(self):
        """Create a blog generation service instance."""
        return BlogGenerationService()

    def test_service_initialization(self, service):
        """Test that service initializes correctly."""
        assert service is not None
        assert service.research_agent is not None
        assert service.scraper_agent is not None
        assert service.writer_agent is not None

    @pytest.mark.asyncio
    async def test_search_results_structure(self):
        """Test that search results have correct structure."""
        article = NewsArticle(
            title="Test Article",
            url="https://example.com",
            summary="Test summary"
        )
        results = SearchResults(articles=[article])
        
        assert len(results.articles) == 1
        assert results.articles[0].title == "Test Article"
