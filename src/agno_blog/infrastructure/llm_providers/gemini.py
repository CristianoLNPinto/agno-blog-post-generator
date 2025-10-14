"""Gemini LLM provider configuration."""

from agno.models.google import Gemini

from ...config import settings


def get_gemini_model(model_id: str = None) -> Gemini:
    """Get configured Gemini model."""
    return Gemini(id=model_id or settings.model_id)
