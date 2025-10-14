"""Tests for Groq LLM provider."""

import os
from unittest.mock import MagicMock, patch

import pytest

from agno_blog.infrastructure.llm_providers import get_groq_client, get_groq_model_id


class TestGroqProvider:
    """Test suite for Groq provider functions."""

    def test_get_groq_model_id_default(self):
        """Test getting default Groq model ID."""
        model_id = get_groq_model_id()
        assert isinstance(model_id, str)
        assert len(model_id) > 0

    def test_get_groq_model_id_custom(self):
        """Test getting custom Groq model ID."""
        custom_model = "llama-3.3-70b-versatile"
        model_id = get_groq_model_id(custom_model)
        assert model_id == custom_model

    @patch.dict(os.environ, {"GROQ_API_KEY": "test_key_123"})
    def test_get_groq_client_with_env_key(self):
        """Test getting Groq client with environment API key."""
        client = get_groq_client()
        assert client is not None
        assert hasattr(client, "chat")

    def test_get_groq_client_with_custom_key(self):
        """Test getting Groq client with custom API key."""
        custom_key = "custom_test_key_456"
        client = get_groq_client(api_key=custom_key)
        assert client is not None
        assert hasattr(client, "chat")

    @patch("agno_blog.infrastructure.llm_providers.groq_provider.Groq")
    def test_get_groq_client_initialization(self, mock_groq):
        """Test that Groq client is initialized correctly."""
        mock_instance = MagicMock()
        mock_groq.return_value = mock_instance
        
        api_key = "test_api_key"
        client = get_groq_client(api_key=api_key)
        
        mock_groq.assert_called_once()
        assert client == mock_instance


class TestGroqIntegration:
    """Integration tests for Groq provider (requires API key)."""

    @pytest.mark.skipif(
        not os.getenv("GROQ_API_KEY"),
        reason="GROQ_API_KEY not set"
    )
    def test_groq_client_real_request(self):
        """Test making a real request to Groq API."""
        client = get_groq_client()
        model_id = get_groq_model_id()
        
        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'test successful' and nothing else."
                }
            ],
            temperature=0.1,
            max_completion_tokens=10
        )
        
        assert completion is not None
        assert len(completion.choices) > 0
        assert completion.choices[0].message.content is not None
        assert len(completion.choices[0].message.content) > 0

    @pytest.mark.skipif(
        not os.getenv("GROQ_API_KEY"),
        reason="GROQ_API_KEY not set"
    )
    def test_groq_streaming_request(self):
        """Test making a streaming request to Groq API."""
        client = get_groq_client()
        model_id = get_groq_model_id()
        
        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "user",
                    "content": "Count from 1 to 3."
                }
            ],
            temperature=0.1,
            max_completion_tokens=50,
            stream=True
        )
        
        chunks = []
        for chunk in completion:
            if chunk.choices[0].delta.content:
                chunks.append(chunk.choices[0].delta.content)
        
        assert len(chunks) > 0
        full_response = "".join(chunks)
        assert len(full_response) > 0
