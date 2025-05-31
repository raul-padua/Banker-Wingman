from typing import List, Dict, Any
import logging
from llama_index.vector_stores.simple import SimpleVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import Document, QueryBundle
from llama_index.core.vector_stores import VectorStoreQuery
import os

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(
        self,
        openai_api_key: str = None
    ):
        self.embedding_model = OpenAIEmbedding(api_key=openai_api_key)
        self.vector_store = SimpleVectorStore()
        logger.info("Initialized SimpleVectorStore")

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        try:
            # Set embedding for each document
            for doc in documents:
                doc.embedding = self.embedding_model.get_text_embedding(doc.text)

            self.vector_store.add(nodes=documents)

            logger.info(f"Added {len(documents)} documents to vector store")

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}", exc_info=True)
            raise

    def search(self, query: str, limit: int = 5, score_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Search the vector store for similar documents."""
        try:
            # Compute embedding for the query string
            query_embedding = self.embedding_model.get_text_embedding(query)
            
            # Create VectorStoreQuery
            vector_store_query = VectorStoreQuery(
                query_embedding=query_embedding,
                similarity_top_k=limit,
                mode="default",
            )

            # Search vector store
            results = self.vector_store.query(
                query=vector_store_query,
                query_str=query
            )

            # Filter by score threshold
            filtered_results = []
            for node in results.nodes:
                score = node.score if hasattr(node, 'score') else 1.0
                if score >= score_threshold:
                    filtered_results.append({
                        'text': node.get_content(),
                        'score': score,
                        'metadata': getattr(node, 'metadata', {})
                    })

            return filtered_results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}", exc_info=True)
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the vector store."""
        return {
            "status": "active",
            "type": "SimpleVectorStore",
            "message": "In-memory vector store is active"
        }

    def delete_collection(self) -> bool:
        """Clear the vector store."""
        try:
            self.vector_store = SimpleVectorStore()
            logger.info("Vector store cleared successfully.")
            return True
        except Exception as e:
            logger.error(f"Error clearing vector store: {e}")
            return False

    @property
    def qdrant_client(self):
        """Compatibility property for existing code that checks qdrant_client."""
        return None

    @property
    def collection_name(self):
        """Compatibility property for existing code that checks collection_name."""
        return "simple_vector_store" 