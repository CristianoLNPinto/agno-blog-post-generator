"""FastAPI application for blog generation API."""

from contextlib import asynccontextmanager

from agno.workflow.workflow import Workflow
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ...application.blog_generation_service import BlogGenerationService
from ...config import settings
from ..db import get_workflow_db
from .models import BlogGenerationRequest, BlogGenerationResponse, HealthResponse

# Global workflow instance
workflow = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    global workflow
    
    # Startup: Initialize workflow
    service = BlogGenerationService()
    
    async def blog_generation_execution(session_state, topic: str = None, **kwargs):
        """Workflow execution function."""
        return await service.generate_blog_post(session_state, topic, **kwargs)
    
    workflow = Workflow(
        name="Blog Post Generator",
        description="Advanced blog post generator with research and content creation capabilities",
        db=get_workflow_db(),
        steps=blog_generation_execution,
        session_state={},
    )
    
    yield
    
    # Shutdown: Cleanup if needed
    workflow = None


# Create FastAPI app with comprehensive OpenAPI documentation
app = FastAPI(
    title="Agno Blog Generator API",
    description="""# 🎨 AI-Powered Blog Post Generator

## Overview
This API provides intelligent blog post generation using AI agents that:
- 🔍 **Research**: Automatically find and evaluate high-quality sources
- 📄 **Extract**: Scrape and process content from relevant articles
- ✍️ **Write**: Generate professional, SEO-optimized blog posts

## Features
- **Multi-Agent System**: Specialized agents for research, scraping, and writing
- **Smart Caching**: Efficient caching at each stage for faster generation
- **Domain-Driven Design**: Clean architecture with separation of concerns
- **Observability**: Full experiment tracking with Comet ML and Opik

## How It Works
1. **Research Phase**: The research agent searches for relevant articles
2. **Extraction Phase**: The scraper agent extracts full content
3. **Writing Phase**: The writer agent synthesizes a professional blog post
4. **Caching**: Results are cached at each stage for efficiency

## Authentication
Currently, this API does not require authentication. In production, implement proper API key authentication.

## Rate Limiting
No rate limiting is currently enforced. Consider implementing rate limiting in production.

## Support
For issues or questions, please visit the [GitHub repository](https://github.com/CristianoLNPinto/agno-blog-post-generator).
    """,
    version="2.0.0",
    lifespan=lifespan,
    contact={
        "name": "Cristiano Lacerda Nunes Pinto",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and system status endpoints",
        },
        {
            "name": "generation",
            "description": "Blog post generation endpoints",
        },
    ],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    response_model=HealthResponse,
    tags=["health"],
    summary="Root endpoint",
    description="Returns basic health status and API version information.",
)
async def root():
    """Root endpoint - health check.
    
    Returns:
        HealthResponse: Basic health status and version
    """
    return HealthResponse(status="healthy", version="2.0.0")


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Health check",
    description="Comprehensive health check endpoint for monitoring and load balancers.",
    responses={
        200: {
            "description": "API is healthy and operational",
            "content": {
                "application/json": {
                    "example": {"status": "healthy", "version": "1.0.0"}
                }
            },
        },
    },
)
async def health():
    """Health check endpoint.
    
    Use this endpoint for:
    - Load balancer health checks
    - Monitoring systems
    - Verifying API availability
    
    Returns:
        HealthResponse: Detailed health status and version information
    """
    return HealthResponse(status="healthy", version="2.0.0")


@app.post(
    "/generate",
    response_model=BlogGenerationResponse,
    tags=["generation"],
    summary="Generate blog post",
    description="""Generate a professional blog post on any topic using AI agents.
    
    ## Process
    1. **Research**: Searches for relevant, high-quality sources
    2. **Extraction**: Scrapes and processes article content
    3. **Writing**: Generates a professional, SEO-optimized blog post
    
    ## Caching
    The system supports three levels of caching:
    - **Search Cache**: Stores search results for topics
    - **Scrape Cache**: Stores extracted article content
    - **Blog Cache**: Stores generated blog posts
    
    Enable caching to improve performance for repeated or similar topics.
    
    ## Response Time
    - With cache: ~1-5 seconds
    - Without cache: ~30-60 seconds (depends on research depth)
    
    ## Best Practices
    - Be specific with your topic for better results
    - Use caching for production environments
    - Topics should be 3-500 characters
    """,
    responses={
        200: {
            "description": "Blog post generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "topic": "The Future of AI in Healthcare",
                        "blog_post": "# The Future of AI in Healthcare\n\nArtificial Intelligence is revolutionizing healthcare...",
                        "status": "success",
                        "message": None,
                    }
                }
            },
        },
        500: {
            "description": "Internal server error during generation",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error generating blog post: Connection timeout"
                    }
                }
            },
        },
    },
)
async def generate_blog_post(request: BlogGenerationRequest):
    """Generate a blog post based on the provided topic.
    
    This endpoint orchestrates multiple AI agents to:
    1. Research relevant sources on the topic
    2. Extract and process content from found articles
    3. Synthesize information into a professional blog post
    
    Args:
        request: Blog generation request with topic and cache settings
        
    Returns:
        BlogGenerationResponse: Generated blog post in markdown format
        
    Raises:
        HTTPException: If workflow is not initialized or generation fails
    """
    try:
        if not workflow:
            raise HTTPException(status_code=500, detail="Workflow not initialized")
        
        # Run the workflow
        response = await workflow.arun(
            topic=request.topic,
            use_search_cache=request.use_search_cache,
            use_scrape_cache=request.use_scrape_cache,
            use_blog_cache=request.use_blog_cache,
        )
        
        if not response or not response.content:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate blog post"
            )
        
        return BlogGenerationResponse(
            topic=request.topic,
            blog_post=response.content,
            status="success",
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating blog post: {str(e)}"
        )


def main():
    """Main entry point for running the API server."""
    import uvicorn
    
    uvicorn.run(
        "agno_blog.infrastructure.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
