"""Pydantic models for blog generation."""

from typing import Optional

from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    """Model for a news article search result."""
    
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        ..., description="Summary of the article if available."
    )


class SearchResults(BaseModel):
    """Model for search results containing multiple articles."""
    
    articles: list[NewsArticle]


class ScrapedArticle(BaseModel):
    """Model for a scraped article with full content."""
    
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        ..., description="Summary of the article if available."
    )
    content: Optional[str] = Field(
        ...,
        description="Full article content in markdown format. None if content is unavailable.",
    )
