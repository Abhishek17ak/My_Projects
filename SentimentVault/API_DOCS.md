# API Documentation

## Overview

SentimentVault provides a high-performance REST API for sentiment analysis predictions. All endpoints use JSON for request/response.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production, implement OAuth2 or API keys as needed.

## Response Format

All successful responses return HTTP 200 with JSON:
```json
{
  "data": {...},
  "timestamp": "2025-01-12T10:30:00Z"
}
```

Error responses:
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## Endpoints

### 1. Predict Sentiment

Classify a single review as Positive or Negative.

**Endpoint:** `POST /predict`

**Request Body:**
```json
{
  "text": "This product exceeded my expectations!"
}
```

**Request Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | Yes | Review text (1-5000 chars) |

**Response:**
```json
{
  "sentiment": "POSITIVE",
  "confidence": 0.9876,
  "latency_ms": 7.2,
  "source": "cache",
  "timestamp": "2025-01-12T10:30:45.123456"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `sentiment` | string | Prediction: "POSITIVE" or "NEGATIVE" |
| `confidence` | float | Confidence score (0-1) |
| `latency_ms` | float | Inference latency in milliseconds |
| `source` | string | "cache" (Redis hit) or "model" (inference) |
| `timestamp` | string | ISO 8601 timestamp |

**Example Request:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Amazing product, highly recommend!"}'
```

**Example Response:**
```json
{
  "sentiment": "POSITIVE",
  "confidence": 0.9876,
  "latency_ms": 5.4,
  "source": "cache",
  "timestamp": "2025-01-12T10:30:45.123456"
}
```

**Status Codes:**
- `200` - Successful prediction
- `400` - Invalid input (empty or too long text)
- `422` - Validation error
- `503` - Model not loaded

---

### 2. Batch Predict

Classify multiple reviews in a single request.

**Endpoint:** `POST /batch-predict`

**Request Body:**
```json
[
  {"text": "Love it!"},
  {"text": "Terrible quality."},
  {"text": "Best purchase ever!"}
]
```

**Response:**
```json
[
  {
    "sentiment": "POSITIVE",
    "confidence": 0.98,
    "latency_ms": 5.2,
    "source": "cache",
    "timestamp": "2025-01-12T10:30:45.123456"
  },
  {
    "sentiment": "NEGATIVE",
    "confidence": 0.97,
    "latency_ms": 45.3,
    "source": "model",
    "timestamp": "2025-01-12T10:30:45.156789"
  },
  {
    "sentiment": "POSITIVE",
    "confidence": 0.99,
    "latency_ms": 6.1,
    "source": "cache",
    "timestamp": "2025-01-12T10:30:45.189012"
  }
]
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/batch-predict \
  -H "Content-Type: application/json" \
  -d '[{"text": "Great!"}, {"text": "Horrible"}]'
```

**Batch Limits:**
- Max batch size: 100 requests
- Max text length per item: 5000 characters

---

### 3. Health Check

Verify API and model health status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "redis_connected": true,
  "device": "cuda",
  "timestamp": "2025-01-12T10:30:45.123456"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "healthy" or "degraded" |
| `model_loaded` | boolean | Model availability |
| `redis_connected` | boolean | Redis connection status |
| `device` | string | "cuda" (GPU) or "cpu" |
| `timestamp` | string | Check timestamp |

**Example Request:**
```bash
curl http://localhost:8000/health
```

**Status Codes:**
- `200` - Healthy
- `503` - Service degraded

---

### 4. Get Statistics

Real-time API performance statistics.

**Endpoint:** `GET /stats`

**Response:**
```json
{
  "total_predictions": 12450,
  "cache_hits": 8715,
  "cache_hit_rate": 0.7,
  "average_latency_ms": 28.5
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `total_predictions` | integer | Total predictions served |
| `cache_hits` | integer | Number of cache hits |
| `cache_hit_rate` | float | Cache hit percentage (0-1) |
| `average_latency_ms` | float | Average response latency |

**Example Request:**
```bash
curl http://localhost:8000/stats
```

---

### 5. API Documentation

Interactive Swagger UI and OpenAPI specification.

**Endpoints:**
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc documentation
- `GET /openapi.json` - OpenAPI spec

**Access:** Open browser to `http://localhost:8000/docs`

---

## Error Codes

| Status | Error | Description |
|--------|-------|-------------|
| 400 | Bad Request | Invalid input (empty text, validation failed) |
| 422 | Validation Error | Pydantic validation failure |
| 503 | Service Unavailable | Model not loaded or Redis down |
| 500 | Internal Server Error | Unexpected server error |

**Error Response Format:**
```json
{
  "detail": "Text must be between 1 and 5000 characters"
}
```

---

## Rate Limiting

Current implementation has no built-in rate limiting. For production:

1. **Implement Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(request: PredictionRequest):
    ...
```

2. **Or use reverse proxy** (Nginx, CloudFlare):
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
```

---

## Performance Considerations

### Cache Hit Optimization

Cache hits are faster. To maximize hits:
- Use consistent text formatting
- Batch similar predictions together
- Cache TTL is 1 hour by default

### Latency

**Typical latencies:**
- Cache hit: 5-10ms
- Cold inference: 60-100ms (GPU), 200-300ms (CPU)

### Throughput

**Capacity:**
- Target: 5000+ predictions/hour
- ~1.4 req/second sustained
- Peak burst: 10+ req/second

---

## Examples

### Python Client

```python
import requests

API_URL = "http://localhost:8000"

def predict(text: str):
    response = requests.post(
        f"{API_URL}/predict",
        json={"text": text}
    )
    return response.json()

# Single prediction
result = predict("Amazing product!")
print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Latency: {result['latency_ms']:.1f}ms")

# Batch prediction
reviews = ["Love it!", "Terrible", "Good quality"]
batch = [{"text": r} for r in reviews]
results = requests.post(f"{API_URL}/batch-predict", json=batch).json()
for r in results:
    print(f"{r['sentiment']} ({r['confidence']:.1%})")
```

### JavaScript/Node.js

```javascript
const API_URL = "http://localhost:8000";

async function predict(text) {
  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
  return response.json();
}

// Usage
predict("Excellent service!").then(result => {
  console.log(`Sentiment: ${result.sentiment}`);
  console.log(`Confidence: ${(result.confidence * 100).toFixed(1)}%`);
});
```

### cURL

```bash
# Single prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}'

# Batch prediction
curl -X POST http://localhost:8000/batch-predict \
  -H "Content-Type: application/json" \
  -d '[{"text": "Great!"}, {"text": "Bad"}]'

# Health check
curl http://localhost:8000/health

# Statistics
curl http://localhost:8000/stats
```

---

## Troubleshooting

### Model Not Loading
```
Error: Model not loaded. Service unavailable.
```
Solution: Check if model exists at `models/sentiment_model/`

### Redis Connection Error
```
Error connecting to Redis
```
Solution: Ensure Redis is running on port 6379

### Timeout on Inference
```
Request timeout after 10 seconds
```
Solution: Model might be on CPU (slower). Check `/health` endpoint for device info.

---

## Support

- Documentation: See README.md
- Issues: GitHub Issues
- Email: support@sentimentvault.dev

---

**Last Updated:** January 2025 | Version: 1.0.0
