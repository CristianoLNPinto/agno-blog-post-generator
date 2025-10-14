# API Reference

## Overview

The Agno Blog Generator API provides RESTful endpoints for generating AI-powered blog posts. The API uses FastAPI and includes comprehensive OpenAPI/Swagger documentation.

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

Once the API is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Authentication

Currently, the API does not require authentication. For production deployments, implement proper API key authentication.

## Endpoints

### Health Check

#### GET `/`

Root endpoint that returns basic health status.

**Response**: `200 OK`

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### GET `/health`

Comprehensive health check endpoint for monitoring and load balancers.

**Response**: `200 OK`

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Blog Generation

#### POST `/generate`

Generate a professional blog post on any topic using AI agents.

**Request Body**:

```json
{
  "topic": "The Future of AI in Healthcare",
  "use_search_cache": true,
  "use_scrape_cache": true,
  "use_blog_cache": true
}
```

**Parameters**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `topic` | string | Yes | - | The topic for the blog post (3-500 characters) |
| `use_search_cache` | boolean | No | true | Whether to use cached search results |
| `use_scrape_cache` | boolean | No | true | Whether to use cached scraped articles |
| `use_blog_cache` | boolean | No | true | Whether to use cached blog posts |

**Response**: `200 OK`

```json
{
  "topic": "The Future of AI in Healthcare",
  "blog_post": "# The Future of AI in Healthcare\n\nArtificial Intelligence is revolutionizing healthcare...",
  "status": "success",
  "message": null
}
```

**Error Response**: `500 Internal Server Error`

```json
{
  "detail": "Error generating blog post: Connection timeout"
}
```

## Response Times

- **With cache**: ~1-5 seconds
- **Without cache**: ~30-60 seconds (depends on research depth)

## Caching System

The API supports three levels of caching:

1. **Search Cache**: Stores search results for topics
2. **Scrape Cache**: Stores extracted article content
3. **Blog Cache**: Stores generated blog posts

Enable caching to improve performance for repeated or similar topics.

## Best Practices

1. **Be Specific**: Use specific topics for better results
2. **Use Caching**: Enable caching in production environments
3. **Topic Length**: Keep topics between 3-500 characters
4. **Error Handling**: Implement proper error handling in your client
5. **Timeouts**: Set appropriate timeouts (60+ seconds for non-cached requests)

## Example Usage

### cURL

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of AI in Healthcare",
    "use_search_cache": true,
    "use_scrape_cache": true,
    "use_blog_cache": true
  }'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "topic": "The Future of AI in Healthcare",
        "use_search_cache": True,
        "use_scrape_cache": True,
        "use_blog_cache": True
    }
)

data = response.json()
print(data["blog_post"])
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    topic: 'The Future of AI in Healthcare',
    use_search_cache: true,
    use_scrape_cache: true,
    use_blog_cache: true
  })
});

const data = await response.json();
console.log(data.blog_post);
```

## Rate Limiting

Currently, no rate limiting is enforced. Consider implementing rate limiting in production environments.

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 422 | Validation Error (invalid request body) |
| 500 | Internal Server Error |

## Support

For issues or questions:
- GitHub Issues: [Report an issue](https://github.com/CristianoLNPinto/agno-blog-post-generator/issues)
- Documentation: See other docs in the `/docs` directory
