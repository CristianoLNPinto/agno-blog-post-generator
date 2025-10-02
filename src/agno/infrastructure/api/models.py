"""API request and response models."""

from typing import Optional

from pydantic import BaseModel, Field


class BlogGenerationRequest(BaseModel):
    """Request model for blog generation."""
    
    topic: str = Field(..., description="The topic for the blog post")
    use_search_cache: bool = Field(
        default=True, description="Whether to use cached search results"
    )
    use_scrape_cache: bool = Field(
        default=True, description="Whether to use cached scraped articles"
    )
    use_blog_cache: bool = Field(
        default=True, description="Whether to use cached blog posts"
    )


class BlogGenerationResponse(BaseModel):
    """Response model for blog generation."""
    
    topic: str = Field(..., description="The topic of the generated blog post")
    blog_post: str = Field(..., description="The generated blog post in markdown")
    status: str = Field(default="success", description="Status of the generation")
    message: Optional[str] = Field(
        default=None, description="Additional message or error details"
    )


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(default="healthy")
    version: str = Field(default="1.0.0")
