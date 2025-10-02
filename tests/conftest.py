"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_topic():
    """Sample blog topic for testing."""
    return "The Future of AI in Healthcare"


@pytest.fixture
def session_state():
    """Empty session state for testing."""
    return {}
