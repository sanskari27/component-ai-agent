from typing import Dict, Any, List
import logging

from src.rag.retriever import get_retriever
from src.rag.embeddings import get_embedding_service
from src.db.vector_store import get_vector_store
from src.db.schemas import ComponentSchema

logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG pipeline for component search and retrieval"""
    
    def __init__(self):
        self.retriever = get_retriever()
        self.embedding_service = get_embedding_service()
        self.vector_store = get_vector_store()
    
    def search_components(
        self,
        query: str,
        limit: int = 10,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Search for components using semantic search"""
        return self.retriever.search(query=query, limit=limit, filters=filters)
    
    def add_component(self, component: Dict[str, Any]) -> bool:
        """Add a component to the knowledge base"""
        try:
            # Convert component to document text
            document = ComponentSchema.to_document(component)
            
            # Generate embedding
            embedding = self.embedding_service.encode(document)
            
            # Extract metadata
            metadata = ComponentSchema.to_metadata(component)
            
            # Add to vector store
            success = self.vector_store.add_component(
                component_id=component["id"],
                document=document,
                embedding=embedding,
                metadata=metadata
            )
            
            if success:
                logger.info(f"Added component: {component['name']} ({component['id']})")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to add component: {e}")
            return False
    
    def update_component(self, component: Dict[str, Any]) -> bool:
        """Update a component in the knowledge base"""
        try:
            # Convert component to document text
            document = ComponentSchema.to_document(component)
            
            # Generate embedding
            embedding = self.embedding_service.encode(document)
            
            # Extract metadata
            metadata = ComponentSchema.to_metadata(component)
            
            # Update in vector store
            success = self.vector_store.update_component(
                component_id=component["id"],
                document=document,
                embedding=embedding,
                metadata=metadata
            )
            
            if success:
                logger.info(f"Updated component: {component['name']} ({component['id']})")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to update component: {e}")
            return False
    
    def delete_component(self, component_id: str) -> bool:
        """Delete a component from the knowledge base"""
        try:
            success = self.vector_store.delete_component(component_id)
            
            if success:
                logger.info(f"Deleted component: {component_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete component: {e}")
            return False
    
    def get_component(self, component_id: str) -> Dict[str, Any]:
        """Get a component by ID"""
        return self.retriever.get_by_id(component_id)
    
    def get_all_components(self) -> List[Dict[str, Any]]:
        """Get all components"""
        return self.retriever.get_all()
    
    def suggest_component_for_ui(
        self,
        ui_description: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Suggest components based on UI description"""
        # Enhance the query with common UI patterns
        enhanced_query = f"UI component for: {ui_description}"
        return self.search_components(query=enhanced_query, limit=limit)


def get_rag_pipeline() -> RAGPipeline:
    """Get RAG pipeline instance"""
    return RAGPipeline()

