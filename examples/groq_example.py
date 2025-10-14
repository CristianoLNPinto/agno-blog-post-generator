"""Example of using Groq LLM provider with the blog generator."""

import asyncio
import os
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agno_blog.infrastructure.llm_providers import get_groq_client, get_groq_model_id


def basic_groq_example():
    """Basic example using Groq client directly."""
    print("=" * 60)
    print("Basic Groq Example")
    print("=" * 60)
    
    # Get Groq client
    client = get_groq_client()
    model_id = get_groq_model_id()
    
    print(f"Using model: {model_id}\n")
    
    # Create a chat completion
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of low latency LLMs in 2 sentences."
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=False
    )
    
    print("Response:")
    print(completion.choices[0].message.content)
    print()


def streaming_groq_example():
    """Example using Groq with streaming."""
    print("=" * 60)
    print("Streaming Groq Example")
    print("=" * 60)
    
    # Get Groq client
    client = get_groq_client()
    model_id = get_groq_model_id()
    
    print(f"Using model: {model_id}\n")
    print("Response (streaming):")
    
    # Create a streaming chat completion
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": "Write a haiku about AI and speed."
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=True
    )
    
    # Stream the response
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print("\n")


async def async_groq_example():
    """Example using Groq with async client."""
    from groq import AsyncGroq
    
    print("=" * 60)
    print("Async Groq Example")
    print("=" * 60)
    
    # Get async Groq client
    async with AsyncGroq(api_key=os.getenv("GROQ_API_KEY")) as client:
        model_id = get_groq_model_id()
        
        print(f"Using model: {model_id}\n")
        
        # Create an async chat completion
        completion = await client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "user",
                    "content": "What are the benefits of async programming in Python?"
                }
            ],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=False
        )
        
        print("Response:")
        print(completion.choices[0].message.content)
        print()


def main():
    """Run all examples."""
    # Check if API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY environment variable not set!")
        print("Please set your Groq API key in the .env file or environment.")
        return
    
    # Run basic example
    basic_groq_example()
    
    # Run streaming example
    streaming_groq_example()
    
    # Run async example
    asyncio.run(async_groq_example())
    
    print("=" * 60)
    print("✅ All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
