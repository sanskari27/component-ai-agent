from fastapi import APIRouter, HTTPException, status
import logging
import os

from src.api.models import ScanComponentFolderRequest, ScanResult
from src.intelligence.component_scanner import get_component_scanner

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/scan", tags=["scan"])


@router.post("", response_model=ScanResult)
async def scan_component_folder(request: ScanComponentFolderRequest):
    """Scan a component folder and index components"""
    try:
        # Validate folder path
        if not os.path.exists(request.folder_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Folder not found: {request.folder_path}"
            )
        
        if not os.path.isdir(request.folder_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Path is not a directory: {request.folder_path}"
            )
        
        # Scan the folder
        scanner = get_component_scanner()
        result = scanner.scan_folder(
            folder_path=request.folder_path,
            include_storybooks=request.include_storybooks,
            include_tests=request.include_tests,
            recursive=request.recursive
        )
        
        return ScanResult(
            components_found=result["components_found"],
            components=result["components"],
            errors=result.get("errors", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scan failed: {str(e)}"
        )

