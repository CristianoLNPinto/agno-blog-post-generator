# Groq Provider Limitations and Workarounds

This guide documents known limitations when using Groq as the LLM provider and how they're handled in the application.

## Known Limitations

### 1. JSON Mode + Tool Calling Incompatibility ⚠️

**Issue**: Groq does not support combining JSON mode (`output_schema`) with tool/function calling.

**Error Message**:
```
Error: json mode cannot be combined with tool/function calling
Type: invalid_request_error
```

**Impact**: Affects agents that use both:
- `output_schema` (for structured JSON output)
- `tools` (like GoogleSearchTools, Newspaper4kTools)

**Affected Agents**:
- ✅ Research Agent (uses GoogleSearchTools)
- ✅ Scraper Agent (uses Newspaper4kTools)
- ✅ Writer Agent (no tools, not affected)

### Workaround Implementation

The application automatically handles this limitation by conditionally configuring agents based on the `LLM_PROVIDER` setting.

#### Research Agent

```python
# Configure agent based on provider
_agent_config = {
    "name": "Blog Research Agent",
    "model": get_model(),
    "tools": [GoogleSearchTools()],
    "description": "...",
    "instructions": "...",
}

# Only add output_schema for Gemini
if settings.llm_provider.lower() == "gemini":
    _agent_config["output_schema"] = SearchResults

research_agent = Agent(**_agent_config)
```

**Result**:
- **Gemini**: Uses both `output_schema` and `tools` (structured JSON output)
- **Groq**: Uses only `tools` (relies on prompt engineering for structure)

#### Scraper Agent

Same pattern applied:
```python
# Only add output_schema for Gemini
if settings.llm_provider.lower() == "gemini":
    _agent_config["output_schema"] = ScrapedArticle

content_scraper_agent = Agent(**_agent_config)
```

### 2. Output Format Differences

**With Gemini** (output_schema enabled):
- Guaranteed JSON structure matching the schema
- Type validation at the model level
- Consistent field names and types

**With Groq** (output_schema disabled):
- Relies on prompt instructions for structure
- May require additional parsing
- Slightly less consistent formatting

**Mitigation**: The application's prompt engineering is designed to work well with both approaches.

## Comparison Table

| Feature | Gemini | Groq |
|---------|--------|------|
| **JSON Mode** | ✅ Supported | ✅ Supported |
| **Tool Calling** | ✅ Supported | ✅ Supported |
| **JSON Mode + Tools** | ✅ Supported | ❌ Not Supported |
| **Workaround** | N/A | Conditional config |

## Testing

### Verify Groq Configuration

Run the debug script to check agent configuration:

```bash
python debug_config.py
```

Expected output for Groq:
```
LLM_PROVIDER: groq
Model type: Groq
Model ID: qwen/qwen3-32b
```

### Test Blog Generation

1. Set Groq as provider:
   ```bash
   LLM_PROVIDER=groq
   ```

2. Generate a blog post and verify:
   - ✅ Search phase completes successfully
   - ✅ Articles are found and scraped
   - ✅ Blog post is generated
   - ✅ No "json mode cannot be combined" errors

## Best Practices

### When Using Groq

1. **Monitor Output Quality**: Check if responses maintain expected structure
2. **Add Validation**: Implement additional validation if needed
3. **Clear Prompts**: Ensure prompts clearly specify expected output format
4. **Error Handling**: Add fallback logic for malformed responses

### When Using Gemini

1. **Use Output Schema**: Take advantage of structured output validation
2. **Type Safety**: Leverage Pydantic models for type checking
3. **Consistent Format**: Rely on guaranteed JSON structure

## Future Improvements

### Potential Solutions

1. **Groq API Updates**: Monitor Groq for JSON mode + tools support
2. **Alternative Approaches**:
   - Use separate agents (one with tools, one with JSON mode)
   - Implement post-processing validation
   - Use structured prompts with regex parsing

3. **Provider-Specific Agents**: Create specialized agent variants per provider

## Troubleshooting

### Error: "json mode cannot be combined with tool/function calling"

**Cause**: Using Groq with agents that have both `output_schema` and `tools`

**Solution**: Already implemented! The agents automatically adapt based on provider.

**Verify Fix**:
```bash
# Check agent configuration
grep -A 5 "output_schema" src/agno_blog/domain/agents/research_agent.py
```

Should show conditional logic:
```python
if settings.llm_provider.lower() == "gemini":
    _agent_config["output_schema"] = SearchResults
```

### Search Not Working with Groq

**Symptoms**: No search results, empty article list

**Possible Causes**:
1. ❌ Old agent code without conditional config
2. ❌ Cache from previous failed attempts

**Solutions**:
1. Verify agents have conditional `output_schema` logic
2. Clear cache:
   ```bash
   rm -rf tmp/blog_generator.db
   ```
3. Restart application

### Inconsistent Output Format

**Symptoms**: Parsing errors, missing fields

**Cause**: Without `output_schema`, Groq relies on prompt instructions

**Solutions**:
1. **Enhance Prompts**: Add explicit format instructions
2. **Add Validation**: Implement response validation
3. **Use Gemini**: Switch to Gemini for guaranteed structure

## Code Examples

### Conditional Agent Configuration Pattern

```python
# Pattern for agents with tools
_agent_config = {
    "name": "Agent Name",
    "model": get_model(),
    "tools": [SomeTool()],
    "description": "...",
    "instructions": "...",
}

# Only add output_schema for providers that support it
if settings.llm_provider.lower() == "gemini":
    _agent_config["output_schema"] = MySchema

agent = Agent(**_agent_config)
```

### Checking Current Configuration

```python
from agno_blog.config import settings

print(f"Provider: {settings.llm_provider}")
print(f"Supports JSON + Tools: {settings.llm_provider.lower() == 'gemini'}")
```

## Related Documentation

- [Switching LLM Providers](SWITCHING_LLM_PROVIDERS.md)
- [Groq Integration Guide](GROQ_INTEGRATION.md)
- [Groq Agent Integration](GROQ_AGENT_INTEGRATION.md)

## Summary

**Key Points**:
- ✅ Groq limitation is automatically handled
- ✅ No code changes needed when switching providers
- ✅ Agents adapt configuration based on provider
- ✅ Both providers work seamlessly

**The application intelligently adapts to each provider's capabilities!** 🚀
