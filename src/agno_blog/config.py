"""Configuration management for the application."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # Comet ML Configuration
    comet_api_key: str = os.getenv("COMET_API_KEY", "")
    comet_project_name: str = os.getenv("COMET_PROJECT_NAME", "agno-blog-post-generator")
    comet_workspace: str = os.getenv("COMET_WORKSPACE", "")
    comet_enabled: bool = True  # Enable/disable Comet ML tracking
    
    # Opik Configuration (LLM Observability)
    opik_api_key: str = os.getenv("OPIK_API_KEY", "")
    opik_project_name: str = os.getenv("OPIK_PROJECT_NAME", "agno-blog-llm-tracing")
    opik_workspace: str = os.getenv("OPIK_WORKSPACE", "")
    opik_enabled: bool = True  # Enable/disable Opik LLM tracing
    
    # Model Configuration
    llm_provider: str = os.getenv("LLM_PROVIDER", "gemini")  # Options: "gemini", "groq"
    model_id: str = "gemini-2.0-flash-exp"
    groq_model_id: str = os.getenv("GROQ_MODEL_ID", "qwen/qwen3-32b")
    
    # Database Configuration
    db_file: str = "tmp/blog_generator.db"
    session_table: str = "workflow_session"
    
    # Cache Configuration
    use_search_cache: bool = True
    use_scrape_cache: bool = True
    use_blog_cache: bool = True
    
    # Search Configuration
    max_search_attempts: int = 3
    max_articles_to_scrape: int = 7
    
    # Project Paths
    project_root: Path = Path(__file__).parent.parent.parent
    data_dir: Path = project_root / "data"
    static_dir: Path = project_root / "static"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()
