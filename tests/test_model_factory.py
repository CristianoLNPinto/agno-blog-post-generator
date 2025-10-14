"""Tests for model factory."""

import pytest
from unittest.mock import patch

from agno.models.google import Gemini
from agno.models.groq import Groq

from agno_blog.infrastructure.llm_providers import get_model, get_model_id


class TestModelFactory:
    """Test suite for model factory functions."""

    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_get_model_gemini(self, mock_settings):
        """Test getting Gemini model without tools."""
        mock_settings.llm_provider = "gemini"
        mock_settings.model_id = "gemini-2.0-flash-exp"
        
        model = get_model(use_tools=False)
        
        assert isinstance(model, Gemini)
        assert model.id == "gemini-2.0-flash-exp"

    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_get_model_groq(self, mock_settings):
        """Test getting Groq model without tools."""
        mock_settings.llm_provider = "groq"
        mock_settings.groq_model_id = "llama-3.3-70b-versatile"
        
        model = get_model(use_tools=False)
        
        assert isinstance(model, Groq)
        assert model.id == "llama-3.3-70b-versatile"
    
    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_get_model_with_tools_forces_gemini(self, mock_settings):
        """Test that use_tools=True always returns Gemini regardless of LLM_PROVIDER."""
        mock_settings.llm_provider = "groq"  # Set to Groq
        mock_settings.model_id = "gemini-2.0-flash-exp"
        mock_settings.groq_model_id = "llama-3.3-70b-versatile"
        
        model = get_model(use_tools=True)  # But request tools
        
        # Should return Gemini, not Groq
        assert isinstance(model, Gemini)
        assert model.id == "gemini-2.0-flash-exp"

    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_get_model_with_override(self, mock_settings):
        """Test getting model with ID override."""
        mock_settings.llm_provider = "groq"
        mock_settings.groq_model_id = "llama-3.3-70b-versatile"
        
        model = get_model(model_id="qwen/qwen3-32b")
        
        assert isinstance(model, Groq)
        assert model.id == "qwen/qwen3-32b"

    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_get_model_unsupported_provider(self, mock_settings):
        """Test error handling for unsupported provider."""
        mock_settings.llm_provider = "unsupported"
        
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            get_model()

    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_get_model_id_gemini(self, mock_settings):
        """Test getting Gemini model ID."""
        mock_settings.llm_provider = "gemini"
        mock_settings.model_id = "gemini-2.0-flash-exp"
        
        model_id = get_model_id()
        
        assert model_id == "gemini-2.0-flash-exp"

    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_get_model_id_groq(self, mock_settings):
        """Test getting Groq model ID."""
        mock_settings.llm_provider = "groq"
        mock_settings.groq_model_id = "llama-3.3-70b-versatile"
        
        model_id = get_model_id()
        
        assert model_id == "llama-3.3-70b-versatile"

    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_get_model_id_unsupported_provider(self, mock_settings):
        """Test error handling for unsupported provider."""
        mock_settings.llm_provider = "invalid"
        
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            get_model_id()

    @patch("agno_blog.infrastructure.llm_providers.model_factory.settings")
    def test_case_insensitive_provider(self, mock_settings):
        """Test that provider name is case-insensitive."""
        mock_settings.llm_provider = "GROQ"
        mock_settings.groq_model_id = "llama-3.3-70b-versatile"
        
        model = get_model()
        
        assert isinstance(model, Groq)
