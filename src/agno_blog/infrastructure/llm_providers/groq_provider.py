"""Groq LLM provider configuration."""

import os
from typing import Optional

from groq import Groq

from ...config import settings


def get_groq_client(api_key: Optional[str] = None) -> Groq:
    """
    Get configured Groq client.
    
    Args:
        api_key: Optional API key. If not provided, uses GROQ_API_KEY from settings.
    
    Returns:
        Configured Groq client instance.
    """
    return Groq(
        api_key=api_key or settings.groq_api_key or os.getenv("GROQ_API_KEY")
    )


def get_groq_model_id(model_id: Optional[str] = None) -> str:
    """
    Get Groq model ID.
    
    Args:
        model_id: Optional model ID. If not provided, uses default from settings.
    
    Returns:
        Model ID string.
    """
    return model_id or settings.groq_model_id or "qwen/qwen3-32b"
