from typing import List, Dict, Any
import logging

from src.rag.embeddings import get_embedding_service
from src.db.vector_store import get_vector_store

logger = logging.getLogger(__name__)


class Retriever:
    """Retriever for semantic search"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.vector_store = get_vector_store()
    
    def search(
        self,
        query: str,
        limit: int = 10,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar components"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.encode(query)
            
            # Search in vector store
            results = self.vector_store.search(
                query_embedding=query_embedding,
                limit=limit,
                filters=filters
            )
            
            # Format results
            formatted_results = []
            
            if results["ids"] and results["ids"][0]:
                for i, component_id in enumerate(results["ids"][0]):
                    formatted_results.append({
                        "id": component_id,
                        "metadata": results["metadatas"][0][i],
                        "document": results["documents"][0][i],
                        "distance": results["distances"][0][i],
                        "score": 1 - results["distances"][0][i]  # Convert distance to similarity score
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_by_id(self, component_id: str) -> Dict[str, Any]:
        """Get component by ID"""
        return self.vector_store.get_component(component_id)
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all components"""
        return self.vector_store.get_all_components()


def get_retriever() -> Retriever:
    """Get retriever instance"""
    return Retriever()

