"""API request and response models."""

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BlogGenerationRequest(BaseModel):
    """Request model for blog generation.
    
    This model defines the parameters for generating a blog post.
    The system will research the topic, extract content from relevant sources,
    and generate a professional blog post.
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "topic": "The Future of AI in Healthcare",
                    "use_search_cache": True,
                    "use_scrape_cache": True,
                    "use_blog_cache": True
                }
            ]
        }
    )
    
    topic: str = Field(
        ...,
        description="The topic for the blog post. Be specific for better results.",
        min_length=3,
        max_length=500,
        examples=["The Future of AI in Healthcare", "Sustainable Energy Solutions for 2025"]
    )
    use_search_cache: bool = Field(
        default=True,
        description="Whether to use cached search results. Improves performance for repeated topics."
    )
    use_scrape_cache: bool = Field(
        default=True,
        description="Whether to use cached scraped articles. Reduces external API calls."
    )
    use_blog_cache: bool = Field(
        default=True,
        description="Whether to use cached blog posts. Returns existing post if topic was previously generated."
    )


class BlogGenerationResponse(BaseModel):
    """Response model for blog generation.
    
    Contains the generated blog post and metadata about the generation process.
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "topic": "The Future of AI in Healthcare",
                    "blog_post": "# The Future of AI in Healthcare\n\nArtificial Intelligence is revolutionizing...",
                    "status": "success",
                    "message": None
                }
            ]
        }
    )
    
    topic: str = Field(
        ...,
        description="The topic of the generated blog post"
    )
    blog_post: str = Field(
        ...,
        description="The generated blog post in markdown format with proper formatting and structure"
    )
    status: str = Field(
        default="success",
        description="Status of the generation: 'success' or 'error'"
    )
    message: Optional[str] = Field(
        default=None,
        description="Additional message or error details if applicable"
    )


class HealthResponse(BaseModel):
    """Health check response.
    
    Provides information about the API health and version.
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "healthy",
                    "version": "2.0.0"
                }
            ]
        }
    )
    
    status: str = Field(
        default="healthy",
        description="Health status of the API: 'healthy' or 'unhealthy'"
    )
    version: str = Field(
        default="2.0.0",
        description="Current version of the API"
    )
