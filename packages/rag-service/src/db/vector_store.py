import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import logging

from src.config.settings import get_settings

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB vector store wrapper"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        self.collection = None
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create ChromaDB client with persistent storage
            self.client = chromadb.Client(
                ChromaSettings(
                    persist_directory=self.settings.chroma_persist_directory,
                    anonymized_telemetry=False,
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.settings.chroma_collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"Initialized ChromaDB collection: {self.settings.chroma_collection_name}")
            logger.info(f"Collection count: {self.collection.count()}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def add_component(
        self,
        component_id: str,
        document: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """Add a component to the vector store"""
        try:
            self.collection.add(
                ids=[component_id],
                embeddings=[embedding],
                documents=[document],
                metadatas=[metadata]
            )
            return True
        except Exception as e:
            logger.error(f"Failed to add component {component_id}: {e}")
            return False
    
    def update_component(
        self,
        component_id: str,
        document: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """Update a component in the vector store"""
        try:
            self.collection.update(
                ids=[component_id],
                embeddings=[embedding],
                documents=[document],
                metadatas=[metadata]
            )
            return True
        except Exception as e:
            logger.error(f"Failed to update component {component_id}: {e}")
            return False
    
    def delete_component(self, component_id: str) -> bool:
        """Delete a component from the vector store"""
        try:
            self.collection.delete(ids=[component_id])
            return True
        except Exception as e:
            logger.error(f"Failed to delete component {component_id}: {e}")
            return False
    
    def search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search for similar components"""
        try:
            where = None
            if filters:
                # Convert filters to ChromaDB where clause
                where = self._build_where_clause(filters)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where,
                include=["documents", "metadatas", "distances"]
            )
            
            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def get_component(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get a component by ID"""
        try:
            result = self.collection.get(
                ids=[component_id],
                include=["documents", "metadatas"]
            )
            
            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "document": result["documents"][0],
                    "metadata": result["metadatas"][0]
                }
            return None
        except Exception as e:
            logger.error(f"Failed to get component {component_id}: {e}")
            return None
    
    def get_all_components(self) -> List[Dict[str, Any]]:
        """Get all components"""
        try:
            result = self.collection.get(include=["documents", "metadatas"])
            
            components = []
            for i, component_id in enumerate(result["ids"]):
                components.append({
                    "id": component_id,
                    "document": result["documents"][i],
                    "metadata": result["metadatas"][i]
                })
            
            return components
        except Exception as e:
            logger.error(f"Failed to get all components: {e}")
            return []
    
    def count(self) -> int:
        """Get total number of components"""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Failed to get count: {e}")
            return 0
    
    def _build_where_clause(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Build ChromaDB where clause from filters"""
        where = {}
        
        if "category" in filters:
            where["category"] = filters["category"]
        
        # Add more filter handling as needed
        
        return where if where else None
    
    def health_check(self) -> bool:
        """Check if vector store is healthy"""
        try:
            self.collection.count()
            return True
        except Exception:
            return False


# Global vector store instance
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get or create global vector store instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store

