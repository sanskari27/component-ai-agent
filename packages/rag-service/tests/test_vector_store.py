import pytest
from src.db.vector_store import VectorStore
import tempfile
import shutil


@pytest.fixture
def vector_store():
    """Create a temporary vector store for testing"""
    temp_dir = tempfile.mkdtemp()
    
    # Create vector store with temp directory
    store = VectorStore()
    store.settings.chroma_persist_directory = temp_dir
    store._initialize()
    
    yield store
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_vector_store_initialization(vector_store):
    """Test vector store initialization"""
    assert vector_store.client is not None
    assert vector_store.collection is not None
    assert vector_store.count() >= 0


def test_add_component(vector_store):
    """Test adding a component"""
    component_id = "test-component-1"
    document = "Test component for buttons"
    embedding = [0.1] * 384  # Mock embedding
    metadata = {
        "name": "TestButton",
        "category": "Actions",
        "file_path": "/test/Button.tsx"
    }
    
    success = vector_store.add_component(
        component_id=component_id,
        document=document,
        embedding=embedding,
        metadata=metadata
    )
    
    assert success is True
    assert vector_store.count() == 1


def test_get_component(vector_store):
    """Test retrieving a component"""
    component_id = "test-component-2"
    document = "Test card component"
    embedding = [0.2] * 384
    metadata = {"name": "Card", "category": "Layout"}
    
    vector_store.add_component(component_id, document, embedding, metadata)
    
    result = vector_store.get_component(component_id)
    
    assert result is not None
    assert result["id"] == component_id
    assert result["metadata"]["name"] == "Card"


def test_update_component(vector_store):
    """Test updating a component"""
    component_id = "test-component-3"
    
    # Add component
    vector_store.add_component(
        component_id,
        "Original description",
        [0.3] * 384,
        {"name": "Input"}
    )
    
    # Update component
    success = vector_store.update_component(
        component_id,
        "Updated description",
        [0.4] * 384,
        {"name": "InputField"}
    )
    
    assert success is True
    
    result = vector_store.get_component(component_id)
    assert result["metadata"]["name"] == "InputField"


def test_delete_component(vector_store):
    """Test deleting a component"""
    component_id = "test-component-4"
    
    vector_store.add_component(
        component_id,
        "To be deleted",
        [0.5] * 384,
        {"name": "TempComponent"}
    )
    
    initial_count = vector_store.count()
    success = vector_store.delete_component(component_id)
    
    assert success is True
    assert vector_store.count() == initial_count - 1
    assert vector_store.get_component(component_id) is None


def test_search(vector_store):
    """Test searching for components"""
    # Add multiple components
    components = [
        ("comp-1", "Button component for actions", {"name": "Button"}),
        ("comp-2", "Input field for forms", {"name": "Input"}),
        ("comp-3", "Action button with icon", {"name": "IconButton"}),
    ]
    
    for comp_id, doc, meta in components:
        vector_store.add_component(comp_id, doc, [0.1] * 384, meta)
    
    # Search for button-related components
    query_embedding = [0.1] * 384  # Mock query embedding
    results = vector_store.search(query_embedding, limit=2)
    
    assert len(results["ids"][0]) <= 2
    assert len(results["documents"][0]) <= 2


def test_health_check(vector_store):
    """Test health check"""
    assert vector_store.health_check() is True

