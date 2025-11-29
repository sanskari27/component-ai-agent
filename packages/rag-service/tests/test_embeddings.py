import pytest
from src.rag.embeddings import EmbeddingService


@pytest.fixture
def embedding_service():
    return EmbeddingService()


def test_embedding_service_initialization(embedding_service):
    """Test that embedding service initializes correctly"""
    assert embedding_service.model is not None
    assert embedding_service.get_dimension() > 0


def test_encode_single_text(embedding_service):
    """Test encoding a single text"""
    text = "Hello world"
    embedding = embedding_service.encode(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == embedding_service.get_dimension()
    assert all(isinstance(x, float) for x in embedding)


def test_encode_multiple_texts(embedding_service):
    """Test encoding multiple texts"""
    texts = ["Hello world", "Component library", "React button"]
    embeddings = embedding_service.encode(texts)
    
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(texts)
    assert all(len(emb) == embedding_service.get_dimension() for emb in embeddings)


def test_embedding_similarity(embedding_service):
    """Test that similar texts have similar embeddings"""
    text1 = "Button component"
    text2 = "Button widget"
    text3 = "Database connection"
    
    emb1 = embedding_service.encode(text1)
    emb2 = embedding_service.encode(text2)
    emb3 = embedding_service.encode(text3)
    
    # Calculate cosine similarity
    def cosine_similarity(a, b):
        import math
        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(y * y for y in b))
        return dot_product / (magnitude_a * magnitude_b)
    
    sim_1_2 = cosine_similarity(emb1, emb2)
    sim_1_3 = cosine_similarity(emb1, emb3)
    
    # Similar texts should have higher similarity
    assert sim_1_2 > sim_1_3

