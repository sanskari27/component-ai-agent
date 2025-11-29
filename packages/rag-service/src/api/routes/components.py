from fastapi import APIRouter, HTTPException, status, Body
from typing import List
import logging
import uuid

from src.api.models import Component as ComponentModel
from src.rag.pipeline import get_rag_pipeline
from src.db.vector_store import get_vector_store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/components", tags=["components"])


@router.get("", response_model=List[ComponentModel])
async def list_components():
    """List all components"""
    try:
        pipeline = get_rag_pipeline()
        components_data = pipeline.get_all_components()
        
        components = []
        for comp_data in components_data:
            metadata = comp_data.get("metadata", {})
            components.append(
                ComponentModel(
                    id=metadata.get("id", ""),
                    name=metadata.get("name", ""),
                    description=comp_data.get("document", "").split("\n")[1].replace("Description: ", "") if comp_data.get("document") else "",
                    file_path=metadata.get("file_path", ""),
                    props=[],
                    examples=[],
                    category=metadata.get("category"),
                    import_path=metadata.get("import_path"),
                    export_type=metadata.get("export_type", "named"),
                    tags=metadata.get("tags", "").split(",") if metadata.get("tags") else []
                )
            )
        
        return components
        
    except Exception as e:
        logger.error(f"Failed to list components: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list components: {str(e)}"
        )


@router.get("/{component_id}", response_model=ComponentModel)
async def get_component(component_id: str):
    """Get a component by ID"""
    try:
        pipeline = get_rag_pipeline()
        comp_data = pipeline.get_component(component_id)
        
        if not comp_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Component not found: {component_id}"
            )
        
        metadata = comp_data.get("metadata", {})
        return ComponentModel(
            id=metadata.get("id", ""),
            name=metadata.get("name", ""),
            description=comp_data.get("document", "").split("\n")[1].replace("Description: ", "") if comp_data.get("document") else "",
            file_path=metadata.get("file_path", ""),
            props=[],
            examples=[],
            category=metadata.get("category"),
            import_path=metadata.get("import_path"),
            export_type=metadata.get("export_type", "named"),
            tags=metadata.get("tags", "").split(",") if metadata.get("tags") else []
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get component: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get component: {str(e)}"
        )


@router.post("", response_model=ComponentModel, status_code=status.HTTP_201_CREATED)
async def create_component(component: ComponentModel):
    """Create a new component"""
    try:
        # Generate ID if not provided
        if not component.id:
            component.id = str(uuid.uuid4())
        
        pipeline = get_rag_pipeline()
        
        # Convert to dict
        component_dict = component.model_dump()
        
        # Add to pipeline
        success = pipeline.add_component(component_dict)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create component"
            )
        
        return component
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create component: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create component: {str(e)}"
        )


@router.put("/{component_id}", response_model=ComponentModel)
async def update_component(component_id: str, component: ComponentModel):
    """Update an existing component"""
    try:
        # Ensure ID matches
        component.id = component_id
        
        pipeline = get_rag_pipeline()
        
        # Convert to dict
        component_dict = component.model_dump()
        
        # Update in pipeline
        success = pipeline.update_component(component_dict)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update component"
            )
        
        return component
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update component: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update component: {str(e)}"
        )


@router.delete("/{component_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_component(component_id: str):
    """Delete a component"""
    try:
        pipeline = get_rag_pipeline()
        success = pipeline.delete_component(component_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Component not found: {component_id}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete component: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete component: {str(e)}"
        )


@router.get("/name/{component_name}", response_model=List[ComponentModel])
async def get_components_by_name(component_name: str):
    """Get components by name (fuzzy match)"""
    try:
        pipeline = get_rag_pipeline()
        
        # Search by name
        results = pipeline.search_components(
            query=f"Component: {component_name}",
            limit=10
        )
        
        components = []
        for result in results:
            metadata = result.get("metadata", {})
            components.append(
                ComponentModel(
                    id=metadata.get("id", ""),
                    name=metadata.get("name", ""),
                    description=result.get("document", "").split("\n")[1].replace("Description: ", "") if result.get("document") else "",
                    file_path=metadata.get("file_path", ""),
                    props=[],
                    examples=[],
                    category=metadata.get("category"),
                    import_path=metadata.get("import_path"),
                    export_type=metadata.get("export_type", "named"),
                    tags=metadata.get("tags", "").split(",") if metadata.get("tags") else []
                )
            )
        
        return components
        
    except Exception as e:
        logger.error(f"Failed to get components by name: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get components by name: {str(e)}"
        )

