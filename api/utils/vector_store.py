from typing import List, Dict, Any
import logging
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.schema import Document
import numpy as np
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class VectorStoreNode:
    """Simple node for storing document chunks with embeddings."""
    doc_id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]
    score: float = 0.0

class SimpleInMemoryVectorStore:
    """Simple in-memory vector store implementation using cosine similarity."""
    
    def __init__(self):
        self.nodes: List[VectorStoreNode] = []
    
    def add_nodes(self, nodes: List[VectorStoreNode]) -> None:
        """Add nodes to the vector store."""
        self.nodes.extend(nodes)
    
    def query(self, query_embedding: List[float], top_k: int = 5) -> List[VectorStoreNode]:
        """Query the vector store using cosine similarity."""
        if not self.nodes:
            return []
        
        # Calculate cosine similarity for each node
        for node in self.nodes:
            similarity = self._cosine_similarity(query_embedding, node.embedding)
            node.score = similarity
        
        # Sort by similarity score (descending) and return top_k
        sorted_nodes = sorted(self.nodes, key=lambda x: x.score, reverse=True)
        return sorted_nodes[:top_k]
    
    def clear(self) -> None:
        """Clear all nodes from the vector store."""
        self.nodes = []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        # Convert to numpy arrays for easier computation
        a = np.array(vec1)
        b = np.array(vec2)
        
        # Calculate cosine similarity
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)

class VectorStoreManager:
    def __init__(self, openai_api_key: str = None):
        self.embedding_model = OpenAIEmbedding(api_key=openai_api_key)
        self.vector_store = SimpleInMemoryVectorStore()
        logger.info("Initialized custom SimpleInMemoryVectorStore")

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        try:
            nodes = []
            for i, doc in enumerate(documents):
                # Get embedding for the document
                embedding = self.embedding_model.get_text_embedding(doc.text)
                
                # Create a vector store node
                node = VectorStoreNode(
                    doc_id=f"doc_{i}_{id(doc)}",
                    text=doc.text,
                    embedding=embedding,
                    metadata=getattr(doc, 'metadata', {})
                )
                nodes.append(node)
            
            self.vector_store.add_nodes(nodes)
            logger.info(f"Added {len(documents)} documents to vector store")

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}", exc_info=True)
            raise

    def search(self, query: str, limit: int = 5, score_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Search the vector store for similar documents."""
        try:
            # Compute embedding for the query string
            query_embedding = self.embedding_model.get_text_embedding(query)
            
            # Search vector store
            results = self.vector_store.query(query_embedding, top_k=limit)

            # Filter by score threshold and format results
            filtered_results = []
            for node in results:
                if node.score >= score_threshold:
                    filtered_results.append({
                        'text': node.text,
                        'score': float(node.score),
                        'metadata': node.metadata
                    })

            return filtered_results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}", exc_info=True)
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the vector store."""
        return {
            "status": "active",
            "type": "SimpleInMemoryVectorStore",
            "document_count": len(self.vector_store.nodes),
            "message": "Custom in-memory vector store is active"
        }

    def delete_collection(self) -> bool:
        """Clear the vector store."""
        try:
            self.vector_store.clear()
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