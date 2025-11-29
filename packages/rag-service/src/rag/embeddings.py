from sentence_transformers import SentenceTransformer
from typing import List, Union
import logging

from src.config.settings import get_settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using sentence transformers"""
    
    def __init__(self):
        self.settings = get_settings()
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model"""
        try:
            logger.info(f"Loading embedding model: {self.settings.embedding_model}")
            self.model = SentenceTransformer(self.settings.embedding_model)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    def encode(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Generate embeddings for text"""
        try:
            embeddings = self.model.encode(text, convert_to_numpy=True)
            
            if isinstance(text, str):
                return embeddings.tolist()
            else:
                return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.model.get_sentence_embedding_dimension()


# Global embedding service instance
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """Get or create global embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service

