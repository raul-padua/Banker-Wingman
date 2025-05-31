# Import required FastAPI components for building the API
from fastapi import FastAPI, HTTPException, Request, Depends, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
# Import Pydantic for data validation and settings management
from pydantic import BaseModel
# Import OpenAI client for interacting with OpenAI's API
from openai import OpenAI
import os
from typing import Optional, List
import time
import logging
from datetime import datetime
from pathlib import Path
import shutil
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from fastapi import status

# Import custom utilities
from .utils.document_processor import DocumentProcessor
from .utils.vector_store import VectorStoreManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with a title
app = FastAPI(title="OpenAI Chat API")

# --- Global variable definitions ---
vector_store: Optional[VectorStoreManager] = None
# Initialize document processor EARLY - before routes that use it
document_processor = DocumentProcessor(chunk_size=1024, chunk_overlap=0.25)
# --- End Global variable definitions ---

# API Key header for authentication
api_key_header = APIKeyHeader(name="X-API-Key")

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the API to be accessed from different domains/origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,  # Allows cookies to be included in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers in requests
)

# Cache for API key validation
def validate_api_key(api_key: str) -> bool:
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
        print(f"API key {api_key[:8]}... validated successfully.")
        return True
    except Exception as e:
        print(f"API key {api_key[:8]}... failed: {e}")
        return False

async def get_api_key(api_key: str = Depends(api_key_header)):
    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

# Define the data model for chat requests using Pydantic
# This ensures incoming request data is properly validated
class ChatRequest(BaseModel):
    developer_message: str  # Message from the developer/system
    user_message: str      # Message from the user
    model: Optional[str] = "gpt-4.1-mini"  # Optional model selection with default

class QueryRequest(BaseModel):
    query: str
    limit: Optional[int] = 5
    score_threshold: Optional[float] = 0.7

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {process_time:.2f}s"
    )
    return response

class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: StarletteRequest, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_upload_size:
            from starlette.responses import Response
            return Response("File too large", status_code=413)
        return await call_next(request)

# Add this middleware to your app (e.g., 100MB limit)
app.add_middleware(LimitUploadSizeMiddleware, max_upload_size=100 * 1024 * 1024)

# --- Dependency function DEFINITIONS must come BEFORE their use in route decorators ---
async def get_vector_store(api_key: str = Depends(get_api_key)) -> VectorStoreManager:
    """Dependency to get the initialized VectorStoreManager instance."""
    global vector_store
    if vector_store is None:
        logger.info("VectorStoreManager not initialized, initializing now.")
        vector_store = VectorStoreManager(openai_api_key=api_key)
    elif vector_store.embedding_model.api_key != api_key:
        logger.info("API key changed, re-initializing VectorStoreManager.")
        vector_store = VectorStoreManager(openai_api_key=api_key)
    return vector_store
# --- End of critical dependency function definitions ---

@app.on_event("startup")
async def startup_event():
    global vector_store
    vector_store = VectorStoreManager(openai_api_key=os.getenv("OPENAI_API_KEY", "your-default-api-key"))

# File upload endpoint
@app.post("/api/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
    current_vector_store: VectorStoreManager = Depends(get_vector_store)
):
    try:
        # Create data directory if it doesn't exist
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # Save uploaded file
        file_path = data_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process document
        documents = document_processor.process_file(file_path)
        chunks = document_processor.split_documents(documents)

        # Add to vector store - Clear any existing documents first for SimpleVectorStore
        current_vector_store.delete_collection()
        current_vector_store.add_documents(chunks)

        return {
            "message": "File processed successfully",
            "chunks": len(chunks),
            "filename": file.filename
        }

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Query endpoint
@app.post("/api/query")
async def query_documents(
    request: Request,
    query_request: QueryRequest,
    api_key: str = Depends(get_api_key),
    current_vector_store: VectorStoreManager = Depends(get_vector_store)
):
    try:
        results = current_vector_store.search(
            query=query_request.query,
            limit=query_request.limit,
            score_threshold=query_request.score_threshold
        )

        logger.info(f"Raw search results from vector_store.search: {results}")

        # De-duplicate results based on text content, keeping the one with the highest score if text is identical
        unique_results_dict = {}
        for result_item in results:
            text_content = result_item.get('text')
            current_score = result_item.get('score', 0)
            if text_content not in unique_results_dict or current_score > unique_results_dict[text_content].get('score', 0):
                unique_results_dict[text_content] = result_item
        
        deduplicated_results = list(unique_results_dict.values())
        # Sort by score again after de-duplication if needed, though dictionary preserves insertion order in Python 3.7+
        # For explicit sort by score (descending):
        # deduplicated_results.sort(key=lambda x: x.get('score', 0), reverse=True)

        logger.info(f"De-duplicated search results: {deduplicated_results}")

        return {
            "results": deduplicated_results,
            "query": query_request.query
        }

    except Exception as e:
        logger.error(f"Error querying documents: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Define the main chat endpoint that handles POST requests
@app.post("/api/chat")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    api_key: str = Depends(get_api_key),
    current_vector_store: VectorStoreManager = Depends(get_vector_store)
):
    try:
        retrieved_docs = []
        context_for_prompt = "No context from uploaded documents was available or retrieved."

        if current_vector_store:
            try:
                retrieved_docs = current_vector_store.search(query=chat_request.user_message, limit=3)
                logger.info(f"Retrieved {len(retrieved_docs)} documents for chat context.")
                if retrieved_docs:
                    context_for_prompt = "Relevant context from uploaded documents:\n\n"
                    for doc in retrieved_docs:
                        context_for_prompt += f"- Source: {doc.get('metadata', {}).get('file_name', 'N/A')}, Page: {doc.get('metadata', {}).get('page_label', 'N/A')}\n"
                        context_for_prompt += f"  Content: {doc.get('text', '')}\n\n"
                else:
                    context_for_prompt = "No relevant documents found for the query."
            except Exception as e:
                logger.error(f"Error during document search for chat: {e}", exc_info=True)
                context_for_prompt = "Error retrieving documents for context."
        else:
            logger.warning("Vector store not available. Skipping RAG for chat.")
            context_for_prompt = "Vector store not initialized. Cannot perform RAG."

        # Updated system prompt for "Busy Banker's Wingman" and CoT
        base_system_prompt = (
            "You are the busy banker's wingman, a helpful AI assistant. "
            "Your goal is to provide accurate and concise answers, especially for financial or mathematical queries. "
            "For any calculations or when a step-by-step thought process would be beneficial, "
            "please use Chain of Thought reasoning: break down the problem into smaller steps and explain each step "
            "before providing the final answer. If context from uploaded documents is available, "
            "prioritize using that information to answer the user's question."
        )

        final_system_prompt = f"{base_system_prompt}\n\n{context_for_prompt}"
        
        logger.info(f"Sending to OpenAI for chat. System prompt (truncated): {final_system_prompt[:500]}... User message: {chat_request.user_message}")

        client = OpenAI(api_key=api_key)

        async def generate():
            accumulated_response = ""
            try:
                stream = client.chat.completions.create(
                    model=chat_request.model,
                    messages=[
                        {"role": "system", "content": final_system_prompt},
                        {"role": "user", "content": chat_request.user_message}
                    ],
                    stream=True
                )
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        accumulated_response += content
                        yield content
                
            except Exception as e:
                logger.error(f"OpenAI API call failed: {str(e)}", exc_info=True)
                yield "Sorry, I encountered an error processing your request with the AI model."
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/api/health")
async def health_check_reverted():
    vector_store_active = False
    global vector_store

    try:
        if vector_store:
            vector_store_active = True
    except Exception as e:
        logger.warning(f"Health check: Vector store check failed: {e}")

    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "openai": "ready", # This is a general assumption
            "vector_store": "active" if vector_store_active else "not_initialized"
        }
    }

# Delete documents endpoint
@app.delete("/api/documents")
async def delete_all_documents(
    request: Request,
    api_key: str = Depends(get_api_key),
    current_vector_store: VectorStoreManager = Depends(get_vector_store)
):
    """Delete the current vector store contents."""
    try:
        # Clear vector store
        # The get_vector_store dependency already ensures vector_store is initialized if API key is valid
        # We use current_vector_store passed by Depends
        if not current_vector_store:
            # This case should ideally be caught by get_api_key or get_vector_store if API key is invalid
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={"detail": "Vector store not initialized. API key might be missing or invalid."}
            )

        deleted = current_vector_store.delete_collection()
        if not deleted:
            # Handle cases where deletion might not have occurred as expected
            logger.warning("Vector store might not have been cleared as expected.")
            # Still proceed to clear cache and frontend state if desired

        logger.info(f"Documents cleared for API key associated with: {api_key[:5]}...")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Documents cleared successfully."})

    except Exception as e:
        logger.error(f"Error deleting documents: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An error occurred while deleting documents."}
        )

# Entry point for running the application directly
if __name__ == "__main__":
    import uvicorn
    # Start the server on all network interfaces (0.0.0.0) on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
