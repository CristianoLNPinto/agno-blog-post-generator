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


# Create FastAPI app
app = FastAPI(
    title="Agno Blog Generator API",
    description="AI-powered blog post generation with research and content extraction",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.post("/generate", response_model=BlogGenerationResponse)
async def generate_blog_post(request: BlogGenerationRequest):
    """
    Generate a blog post based on the provided topic.
    
    Args:
        request: Blog generation request with topic and cache settings
        
    Returns:
        Generated blog post in markdown format
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


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "agno.infrastructure.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
