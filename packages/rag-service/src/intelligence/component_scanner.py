import os
from typing import List, Dict, Any
import logging

from src.intelligence.metadata_extractor import get_metadata_extractor
from src.intelligence.ast_parser import get_ast_parser
from src.intelligence.storybook_parser import get_storybook_parser
from src.rag.pipeline import get_rag_pipeline

logger = logging.getLogger(__name__)


class ComponentScanner:
    """
    Scans a directory for React components and indexes them
    
    Handles:
    - Finding component files
    - Parsing component metadata
    - Finding associated Storybook files
    - Adding components to the RAG pipeline
    """
    
    def __init__(self):
        self.metadata_extractor = get_metadata_extractor()
        self.ast_parser = get_ast_parser()
        self.storybook_parser = get_storybook_parser()
        self.rag_pipeline = get_rag_pipeline()
    
    def scan_folder(
        self,
        folder_path: str,
        include_storybooks: bool = True,
        include_tests: bool = False,
        recursive: bool = True
    ) -> Dict[str, Any]:
        """
        Scan a folder for components
        
        Args:
            folder_path: Path to the folder to scan
            include_storybooks: Whether to parse Storybook files
            include_tests: Whether to include test files
            recursive: Whether to scan recursively
            
        Returns:
            Scan results with components found and any errors
        """
        logger.info(f"Scanning folder: {folder_path}")
        
        components = []
        errors = []
        
        try:
            # Find all component files
            component_files = self._find_component_files(
                folder_path,
                recursive,
                include_tests
            )
            
            logger.info(f"Found {len(component_files)} component files")
            
            # Find Storybook files if requested
            storybook_map = {}
            if include_storybooks:
                storybook_files = self.storybook_parser.find_storybook_files(
                    folder_path,
                    recursive
                )
                logger.info(f"Found {len(storybook_files)} storybook files")
                
                # Map storybook files to components
                storybook_map = self._map_storybooks_to_components(storybook_files)
            
            # Process each component file
            for file_path in component_files:
                try:
                    # Get associated storybook if exists
                    storybook_path = storybook_map.get(file_path)
                    
                    # Extract metadata
                    component = self.metadata_extractor.extract_from_file(
                        file_path,
                        storybook_path
                    )
                    
                    if component:
                        # Add to RAG pipeline
                        success = self.rag_pipeline.add_component(component)
                        
                        if success:
                            components.append(component)
                            logger.info(f"Indexed component: {component['name']}")
                        else:
                            errors.append(f"Failed to index component: {component['name']}")
                    
                except Exception as e:
                    error_msg = f"Error processing {file_path}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            
            return {
                "components_found": len(components),
                "components": components,
                "errors": errors
            }
            
        except Exception as e:
            error_msg = f"Scan failed: {str(e)}"
            logger.error(error_msg)
            return {
                "components_found": 0,
                "components": [],
                "errors": [error_msg]
            }
    
    def _find_component_files(
        self,
        folder_path: str,
        recursive: bool,
        include_tests: bool
    ) -> List[str]:
        """Find all component files in a folder"""
        component_files = []
        
        try:
            if recursive:
                for root, dirs, files in os.walk(folder_path):
                    # Skip node_modules and other common directories
                    dirs[:] = [d for d in dirs if d not in [
                        'node_modules', '.git', 'dist', 'build', '.next', 'coverage'
                    ]]
                    
                    for file in files:
                        if self._is_component_file(file, include_tests):
                            component_files.append(os.path.join(root, file))
            else:
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path) and self._is_component_file(file, include_tests):
                        component_files.append(file_path)
            
            return component_files
            
        except Exception as e:
            logger.error(f"Error finding component files: {e}")
            return []
    
    def _is_component_file(self, filename: str, include_tests: bool) -> bool:
        """Check if a file is a component file"""
        # Skip test files unless requested
        if not include_tests and ('.test.' in filename or '.spec.' in filename):
            return False
        
        # Skip storybook files (they're handled separately)
        if '.stories.' in filename:
            return False
        
        # Include .tsx and .jsx files (React components)
        # Exclude .d.ts files (type definitions)
        if filename.endswith('.tsx') or filename.endswith('.jsx'):
            return True
        
        # Optionally include .ts/.js files that look like components
        # (start with uppercase letter)
        if filename.endswith('.ts') and not filename.endswith('.d.ts'):
            name_part = os.path.splitext(filename)[0]
            return name_part[0].isupper() if name_part else False
        
        return False
    
    def _map_storybooks_to_components(
        self,
        storybook_files: List[str]
    ) -> Dict[str, str]:
        """
        Map Storybook files to their corresponding component files
        
        Returns:
            Dictionary mapping component file path to storybook file path
        """
        storybook_map = {}
        
        for storybook_file in storybook_files:
            # Extract component name from storybook filename
            # e.g., Button.stories.tsx -> Button.tsx
            base_name = os.path.basename(storybook_file)
            component_name = base_name.replace('.stories.tsx', '.tsx').replace('.stories.ts', '.ts')
            
            # Look for corresponding component file in same directory
            component_dir = os.path.dirname(storybook_file)
            component_file = os.path.join(component_dir, component_name)
            
            if os.path.exists(component_file):
                storybook_map[component_file] = storybook_file
            else:
                # Try .jsx extension
                component_file_jsx = component_file.replace('.tsx', '.jsx').replace('.ts', '.js')
                if os.path.exists(component_file_jsx):
                    storybook_map[component_file_jsx] = storybook_file
        
        return storybook_map
    
    def rescan_component(self, file_path: str) -> Dict[str, Any]:
        """
        Rescan a single component file
        
        Args:
            file_path: Path to the component file
            
        Returns:
            Updated component metadata
        """
        try:
            # Check if component exists in RAG pipeline
            # Extract metadata
            component = self.metadata_extractor.extract_from_file(file_path)
            
            if component:
                # Update in RAG pipeline
                success = self.rag_pipeline.update_component(component)
                
                if success:
                    logger.info(f"Rescanned component: {component['name']}")
                    return component
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to rescan component {file_path}: {e}")
            return None


def get_component_scanner() -> ComponentScanner:
    """Get component scanner instance"""
    return ComponentScanner()

