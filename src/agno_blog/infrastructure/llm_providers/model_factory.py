"""Model factory for selecting LLM provider based on configuration."""

from typing import Union

from agno.models.google import Gemini
from agno.models.groq import Groq

from ...config import settings


def get_model(model_id: str = None, use_tools: bool = False) -> Union[Gemini, Groq]:
    """
    Get the appropriate model based on LLM_PROVIDER setting and tool requirements.
    
    IMPORTANT: Groq doesn't support JSON mode + tools together. If tools are needed,
    this function automatically uses Gemini regardless of LLM_PROVIDER setting.
    
    Args:
        model_id: Optional model ID override. If not provided, uses default from settings.
        use_tools: If True, forces Gemini (Groq doesn't support tools + structured output)
    
    Returns:
        Configured model instance (Gemini or Groq)
    
    Raises:
        ValueError: If LLM_PROVIDER is not supported
    """
    provider = settings.llm_provider.lower()
    
    # Force Gemini if tools are needed (Groq limitation)
    if use_tools:
        return Gemini(id=model_id or settings.model_id)
    
    # Otherwise use configured provider
    if provider == "gemini":
        return Gemini(id=model_id or settings.model_id)
    elif provider == "groq":
        return Groq(id=model_id or settings.groq_model_id)
    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. "
            f"Supported providers: 'gemini', 'groq'"
        )


def get_model_id(use_tools: bool = False) -> str:
    """
    Get the model ID based on LLM_PROVIDER setting and tool requirements.
    
    Args:
        use_tools: If True, returns Gemini model ID (Groq doesn't support tools + structured output)
    
    Returns:
        Model ID string for the configured provider
    """
    provider = settings.llm_provider.lower()
    
    # Force Gemini if tools are needed
    if use_tools:
        return settings.model_id
    
    if provider == "gemini":
        return settings.model_id
    elif provider == "groq":
        return settings.groq_model_id
    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. "
            f"Supported providers: 'gemini', 'groq'"
        )
