from typing import List, Dict, Any
import logging
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import Document, QueryBundle
from llama_index.core.vector_stores import VectorStoreQuery
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(
        self,
        collection_name: str = "documents",
        qdrant_url: str = "http://localhost:6333",
        openai_api_key: str = None
    ):
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(url=qdrant_url)
        self.embedding_model = OpenAIEmbedding(api_key=openai_api_key)
        self._initialize_collection()

    def _initialize_collection(self):
        """Initialize the Qdrant collection if it doesn't exist."""
        try:
            collections = self.qdrant_client.get_collections().collections
            collection_names = [collection.name for collection in collections]

            if self.collection_name not in collection_names:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # OpenAI embedding dimension
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created new collection: {self.collection_name}")

        except Exception as e:
            logger.error(f"Error initializing collection: {str(e)}", exc_info=True)
            raise

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        try:
            vector_store = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=self.collection_name
            )

            # Set embedding for each document
            for doc in documents:
                doc.embedding = self.embedding_model.get_text_embedding(doc.text)

            vector_store.add(nodes=documents)

            logger.info(f"Added {len(documents)} documents to vector store")

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}", exc_info=True)
            raise

    def search(self, query: str, limit: int = 5, score_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Search the vector store for similar documents."""
        try:
            vector_store = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=self.collection_name
            )

            # Compute embedding for the query string
            query_embedding = self.embedding_model.get_text_embedding(query)
            
            # Create VectorStoreQuery
            vector_store_query = VectorStoreQuery(
                query_embedding=query_embedding,
                similarity_top_k=limit,
                mode="default",
            )

            # Search vector store
            results = vector_store.query(
                query=vector_store_query,
                score_threshold=score_threshold,
                query_str=query
            )

            return [
                {
                    'text': node.get_content(),
                    'score': node.score if hasattr(node, 'score') else 1.0,
                    'metadata': getattr(node, 'metadata', {})
                }
                for node in results.nodes
            ]
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}", exc_info=True)
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the Qdrant collection."""
        if not self.qdrant_client.collection_exists(collection_name=self.collection_name):
            return {"status": "not_found", "message": f"Collection '{self.collection_name}' does not exist."}
        return self.qdrant_client.get_collection(collection_name=self.collection_name).model_dump()

    def delete_collection(self) -> bool:
        """Delete the Qdrant collection."""
        try:
            if self.qdrant_client.collection_exists(collection_name=self.collection_name):
                self.qdrant_client.delete_collection(collection_name=self.collection_name)
                logger.info(f"Collection '{self.collection_name}' deleted successfully.")
                # Optionally, re-initialize or clear local state if this manager instance is long-lived
                # For now, we assume a new manager might be created or API key re-validated which handles re-init.
                return True
            else:
                logger.info(f"Collection '{self.collection_name}' does not exist, no action taken.")
                return False # Or True, depending on whether not existing is an error for deletion
        except Exception as e:
            logger.error(f"Error deleting collection '{self.collection_name}': {e}")
            return False 