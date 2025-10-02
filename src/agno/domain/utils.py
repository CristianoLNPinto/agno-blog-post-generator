"""Utility functions for the domain layer."""

from typing import Any, Dict, Optional


def format_article_summary(article: Dict[str, Any]) -> str:
    """Format article information for display."""
    title = article.get("title", "Unknown")
    url = article.get("url", "")
    return f"{title[:60]}... ({url})"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
