"""CLI for blog post generation."""

import asyncio
import random

from agno.utils.pprint import pprint_run_response
from agno.workflow.workflow import Workflow

from .application.blog_generation_service import BlogGenerationService
from .infrastructure.db import get_workflow_db


async def main():
    """Main CLI function."""
    # Fun example topics to showcase the generator's versatility
    example_topics = [
        "The Rise of Artificial General Intelligence: Latest Breakthroughs",
        "How Quantum Computing is Revolutionizing Cybersecurity",
        "Sustainable Living in 2024: Practical Tips for Reducing Carbon Footprint",
        "The Future of Work: AI and Human Collaboration",
        "Space Tourism: From Science Fiction to Reality",
        "Mindfulness and Mental Health in the Digital Age",
        "The Evolution of Electric Vehicles: Current State and Future Trends",
        "Why Cats Secretly Run the Internet",
        "The Science Behind Why Pizza Tastes Better at 2 AM",
        "How Rubber Ducks Revolutionized Software Development",
    ]

    # Test with a random topic
    topic = random.choice(example_topics)

    print("🧪 Testing Blog Post Generator v2.0")
    print("=" * 60)
    print(f"📝 Topic: {topic}")
    print()

    # Initialize service
    service = BlogGenerationService()

    # Create workflow execution function
    async def blog_generation_execution(session_state, topic: str = None, **kwargs):
        """Workflow execution function."""
        return await service.generate_blog_post(session_state, topic, **kwargs)

    # Create workflow with persistent session
    # Use a fixed session_id to persist cache across runs
    workflow = Workflow(
        name="Blog Post Generator",
        description="Advanced blog post generator with research and content creation capabilities",
        db=get_workflow_db(),
        steps=blog_generation_execution,
        session_id="cli_blog_generator",  # Fixed session ID for cache persistence
        session_state={},  # Initial state for new sessions
    )

    # Generate the blog post
    resp = await workflow.arun(
        topic=topic,
        use_search_cache=True,
        use_scrape_cache=True,
        use_blog_cache=True,
    )

    pprint_run_response(resp, markdown=True, show_time=True)


if __name__ == "__main__":
    asyncio.run(main())
