from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from src.api.models import (
    SearchRequest,
    SearchResponse,
    SearchResult,
    Component as ComponentModel
)
from src.rag.pipeline import get_rag_pipeline

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
async def search_components(request: SearchRequest):
    """Search for components using semantic search"""
    try:
        pipeline = get_rag_pipeline()
        
        # Perform search
        results = pipeline.search_components(
            query=request.query,
            limit=request.limit or 10,
            filters=request.filters
        )
        
        # Convert to response format
        search_results = []
        for result in results:
            metadata = result.get("metadata", {})
            
            # Reconstruct component from metadata
            component = ComponentModel(
                id=metadata.get("id", ""),
                name=metadata.get("name", ""),
                description=result.get("document", "").split("\n")[1].replace("Description: ", ""),
                file_path=metadata.get("file_path", ""),
                props=[],
                examples=[],
                category=metadata.get("category"),
                import_path=metadata.get("import_path"),
                export_type=metadata.get("export_type", "named"),
                tags=metadata.get("tags", "").split(",") if metadata.get("tags") else []
            )
            
            search_results.append(
                SearchResult(
                    component=component,
                    score=result.get("score", 0.0),
                    matched_fields=["name", "description"]
                )
            )
        
        return SearchResponse(
            results=search_results,
            total=len(search_results),
            query=request.query
        )
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/suggest", response_model=SearchResponse)
async def suggest_components(request: SearchRequest):
    """Suggest components based on UI description"""
    try:
        pipeline = get_rag_pipeline()
        
        # Get suggestions
        results = pipeline.suggest_component_for_ui(
            ui_description=request.query,
            limit=request.limit or 5
        )
        
        # Convert to response format
        search_results = []
        for result in results:
            metadata = result.get("metadata", {})
            
            component = ComponentModel(
                id=metadata.get("id", ""),
                name=metadata.get("name", ""),
                description=result.get("document", "").split("\n")[1].replace("Description: ", ""),
                file_path=metadata.get("file_path", ""),
                props=[],
                examples=[],
                category=metadata.get("category"),
                import_path=metadata.get("import_path"),
                export_type=metadata.get("export_type", "named"),
                tags=metadata.get("tags", "").split(",") if metadata.get("tags") else []
            )
            
            search_results.append(
                SearchResult(
                    component=component,
                    score=result.get("score", 0.0),
                    matched_fields=["description"]
                )
            )
        
        return SearchResponse(
            results=search_results,
            total=len(search_results),
            query=request.query
        )
        
    except Exception as e:
        logger.error(f"Suggest failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Suggest failed: {str(e)}"
        )

