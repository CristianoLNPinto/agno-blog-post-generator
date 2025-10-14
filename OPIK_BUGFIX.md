# Opik Integration - Correct Implementation

## Initial Issues

### Issue 1: Wrong Exporter Type
Initially used gRPC exporter which caused errors:
```
E0000 00:00:1760451063.306936 1538536 filter_stack_call.cc:404] Metadata key 'Authorization' is invalid
```

### Issue 2: Wrong Endpoint
Used `https://opik.comet.com/v1/traces` which returned `StatusCode.UNAVAILABLE`

## Root Cause

The implementation didn't follow the official Opik documentation for Agno integration.

According to [Opik's official docs](https://www.comet.com/docs/opik/integrations/agno), the correct approach is:
- Use **HTTP exporter** (not gRPC)
- Use **environment variables** for configuration
- Use **SimpleSpanProcessor** (not BatchSpanProcessor)
- Use correct endpoint: `https://www.comet.com/opik/api/v1/private/otel`

## Correct Solution

### Implementation Changes

**File:** `src/agno_blog/infrastructure/observability/opik_tracer.py`

**Key Changes:**

1. **Changed exporter type:**
```python
# Before (wrong):
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# After (correct):
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
```

2. **Changed span processor:**
```python
# Before (wrong):
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# After (correct):
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
```

3. **Use environment variables:**
```python
# Set environment variables as per Opik docs
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://www.comet.com/opik/api/v1/private/otel"

# Headers format: Authorization=<key>,Comet-Workspace=<workspace>,projectName=<project>
headers_parts = [
    f"Authorization={self.api_key}",
    f"Comet-Workspace={self.workspace or 'default'}",
]
if self.project_name:
    headers_parts.append(f"projectName={self.project_name}")

os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = ",".join(headers_parts)
```

4. **Configure tracer provider:**
```python
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(tracer_provider=tracer_provider)
```

5. **Instrument Agno:**
```python
AgnoInstrumentor().instrument()
```

## Testing

After the fix, the app should work correctly with Opik tracing:

1. **Restart the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Generate a blog post**

3. **Check the console** - you should see:
   ```
   INFO Opik configured: project=agno-blog-llm-tracing, workspace=...
   INFO Agno instrumented successfully with Opik (project: agno-blog-llm-tracing)
   ```

4. **No errors:**
   - ✅ No `Metadata key 'Authorization' is invalid` errors
   - ✅ No `StatusCode.UNAVAILABLE` errors
   - ✅ No gRPC errors

5. **View traces** in Opik dashboard:
   - Go to https://www.comet.com/
   - Navigate to your workspace
   - Look for "Opik" or "LLM Tracing" section
   - Select project: `agno-blog-llm-tracing`
   - View detailed traces of all agent calls

## Status

✅ **Fixed** - Opik integration now follows official documentation

The implementation now correctly uses:
- HTTP exporter (not gRPC)
- Environment variables for configuration
- SimpleSpanProcessor for immediate export
- Correct Opik endpoint

## Reference

Official documentation: https://www.comet.com/docs/opik/integrations/agno
