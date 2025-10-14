# Groq Quick Start Guide

Get up and running with Groq in 5 minutes!

## Step 1: Get Your Groq API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Click "Create API Key"
4. Copy your API key

## Step 2: Install Dependencies

```bash
# Install the project with Groq support
pip install -e .
```

## Step 3: Configure Environment

Add your Groq API key to `.env`:

```bash
# Copy example file
cp .env.example .env

# Edit .env and add:
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_ID=qwen/qwen3-32b
```

## Step 4: Test Your Setup

Run the example script:

```bash
python examples/groq_example.py
```

You should see three examples:
1. ✅ Basic synchronous completion
2. ✅ Streaming response
3. ✅ Async completion

## Step 5: Use Groq in Your Code

### Basic Example

```python
from agno_blog.infrastructure.llm_providers import get_groq_client, get_groq_model_id

# Initialize client
client = get_groq_client()
model_id = get_groq_model_id()

# Generate content
completion = client.chat.completions.create(
    model=model_id,
    messages=[
        {
            "role": "user",
            "content": "Write a blog post introduction about AI"
        }
    ],
    temperature=0.6,
    max_completion_tokens=4096,
    stream=False
)

print(completion.choices[0].message.content)
```

### Streaming Example

```python
from agno_blog.infrastructure.llm_providers import get_groq_client, get_groq_model_id

client = get_groq_client()
model_id = get_groq_model_id()

# Stream the response
completion = client.chat.completions.create(
    model=model_id,
    messages=[
        {
            "role": "user",
            "content": "Write a blog post about machine learning"
        }
    ],
    temperature=0.7,
    stream=True
)

for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## Available Models

Try different models by changing `GROQ_MODEL_ID` in `.env`:

| Model | Description | Best For |
|-------|-------------|----------|
| `qwen/qwen3-32b` | High-performance 32B model | General purpose (default) |
| `llama-3.3-70b-versatile` | Meta's Llama 3.3 70B | Complex tasks |
| `llama-3.1-8b-instant` | Fast 8B model | Quick responses |
| `mixtral-8x7b-32768` | Mixtral MoE | Long context |
| `gemma2-9b-it` | Google's Gemma 2 | Instruction following |

## Common Parameters

Customize your completions:

```python
completion = client.chat.completions.create(
    model=model_id,
    messages=[...],
    temperature=0.7,        # 0.0-2.0, higher = more creative
    max_completion_tokens=4096,  # Max tokens to generate
    top_p=0.95,            # Nucleus sampling
    stream=False,          # Enable streaming
    stop=None              # Stop sequences
)
```

## Troubleshooting

### Error: API Key Not Set

```
Error: GROQ_API_KEY environment variable not set
```

**Solution**: Add `GROQ_API_KEY` to your `.env` file

### Error: Model Not Found

```
Error: Model 'xyz' not found
```

**Solution**: Use a valid model ID from the table above

### Error: Rate Limit Exceeded

```
Error: Rate limit exceeded
```

**Solution**: Wait a moment and try again, or upgrade your Groq plan

## Next Steps

- 📖 Read the [Full Integration Guide](docs/guides/GROQ_INTEGRATION.md)
- 🤖 Learn about [Agent Integration](docs/guides/GROQ_AGENT_INTEGRATION.md)
- 🧪 Run the tests: `pytest tests/test_groq_provider.py`
- 💡 Explore more examples in `examples/groq_example.py`

## Performance Tips

1. **Use streaming** for long responses to improve UX
2. **Lower temperature** (0.3-0.5) for factual content
3. **Higher temperature** (0.7-0.9) for creative writing
4. **Set max_tokens** to control response length and cost

## Support

- 📚 [Documentation](docs/guides/GROQ_INTEGRATION.md)
- 🌐 [Groq Console](https://console.groq.com)
- 📖 [Groq Docs](https://console.groq.com/docs)
- 🐛 [Report Issues](https://github.com/CristianoLNPinto/agno-blog-post-generator/issues)

---

**That's it! You're now ready to use Groq for ultra-fast LLM inference! 🚀**
