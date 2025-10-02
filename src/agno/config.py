"""Configuration management for the application."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Configuration
    model_id: str = "gemini-2.0-flash-exp"
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
