# RAG-enabled LLM API

This API provides a RAG (Retrieval-Augmented Generation) system for processing PDF documents and querying them using LLMs. It includes support for tables and illustrations in PDFs, using Qdrant as a vector store and LlamaIndex for document processing.

## Features

- PDF document processing with table and image support
- Document chunking with 25% overlap for better context
- Vector storage using Qdrant
- OpenAI embeddings for semantic search
- Rate limiting and caching
- API key authentication
- Comprehensive logging
- Health monitoring

## Prerequisites

- Python 3.8+
- Redis server
- Qdrant server
- OpenAI API key

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis server:
```bash
redis-server
```

3. Start Qdrant server:
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

4. Set up environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Running the API

```bash
python app.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Upload Document
```http
POST /api/upload
Content-Type: multipart/form-data
X-API-Key: your_api_key

file: <pdf_file>
```

### Query Documents
```http
POST /api/query
Content-Type: application/json
X-API-Key: your_api_key

{
    "query": "your question here",
    "limit": 5,
    "score_threshold": 0.7
}
```

### Chat
```http
POST /api/chat
Content-Type: application/json
X-API-Key: your_api_key

{
    "developer_message": "system message",
    "user_message": "user message",
    "model": "gpt-4.1-mini"
}
```

### Health Check
```http
GET /api/health
```

## Rate Limits

- Upload: 5 requests per minute
- Query: 10 requests per minute
- Chat: 10 requests per minute

## Response Caching

- Chat responses are cached for 1 hour
- Document chunks are stored in Qdrant for persistent retrieval

## Error Handling

The API includes comprehensive error handling and logging. All errors are logged to `app.log` with stack traces for debugging.

## Security

- API key authentication required for all endpoints
- CORS enabled for cross-origin requests
- Rate limiting to prevent abuse
- Input validation using Pydantic models

## Directory Structure

```
api/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── data/              # Temporary storage for uploaded files
├── utils/
│   ├── document_processor.py  # PDF processing utilities
│   └── vector_store.py       # Vector store management
└── app.log            # Application logs
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## CORS Configuration

The API is configured to accept requests from any origin (`*`). This can be modified in the `app.py` file if you need to restrict access to specific domains.

## Error Handling

The API includes basic error handling for:
- Invalid API keys
- OpenAI API errors
- General server errors

All errors will return a 500 status code with an error message. 