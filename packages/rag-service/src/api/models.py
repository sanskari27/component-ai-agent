from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ComponentProp(BaseModel):
    """Component prop definition"""
    name: str
    type: str
    required: bool
    default_value: Optional[str] = None
    description: Optional[str] = None


class ComponentExample(BaseModel):
    """Component usage example"""
    title: str
    code: str
    description: Optional[str] = None
    source: Optional[str] = "manual"


class Component(BaseModel):
    """Component metadata and information"""
    id: str
    name: str
    description: str
    file_path: str
    props: List[ComponentProp] = []
    examples: List[ComponentExample] = []
    theme_wrapper: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    import_path: Optional[str] = None
    export_type: Optional[str] = "named"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class SearchRequest(BaseModel):
    """Search request"""
    query: str = Field(..., min_length=1)
    limit: Optional[int] = Field(default=10, ge=1, le=50)
    filters: Optional[Dict[str, Any]] = None


class SearchResult(BaseModel):
    """Search result item"""
    component: Component
    score: float
    matched_fields: List[str] = []


class SearchResponse(BaseModel):
    """Search response"""
    results: List[SearchResult]
    total: int
    query: str


class ExplainComponentRequest(BaseModel):
    """Component explanation request"""
    component_id: Optional[str] = None
    component_name: Optional[str] = None


class ScanComponentFolderRequest(BaseModel):
    """Scan component folder request"""
    folder_path: str
    include_storybooks: bool = True
    include_tests: bool = False
    recursive: bool = True


class ScanResult(BaseModel):
    """Scan result"""
    components_found: int
    components: List[Component]
    errors: List[str] = []


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    chroma_status: str
    embedding_model: str

