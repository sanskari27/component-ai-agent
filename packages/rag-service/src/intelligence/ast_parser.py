import os
import json
import subprocess
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class ASTParser:
    """
    TypeScript/TSX AST parser using ts-morph via Node.js
    
    This parser extracts component metadata from TypeScript/React files
    """
    
    def __init__(self):
        self.parser_script = self._get_parser_script_path()
    
    def _get_parser_script_path(self) -> str:
        """Get path to the Node.js parser script"""
        # Script will be in the same directory
        return os.path.join(os.path.dirname(__file__), "parser.js")
    
    def parse_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parse a TypeScript/TSX file and extract component metadata
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            Dictionary with component metadata or None if parsing fails
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            # For now, return a simple mock result
            # In production, this would call Node.js with ts-morph
            logger.info(f"Parsing file: {file_path}")
            
            # Mock implementation - extract basic info from file
            return self._mock_parse(file_path)
            
        except Exception as e:
            logger.error(f"Failed to parse file {file_path}: {e}")
            return None
    
    def _mock_parse(self, file_path: str) -> Dict[str, Any]:
        """
        Mock parser implementation
        TODO: Replace with actual ts-morph implementation
        """
        file_name = os.path.basename(file_path)
        component_name = os.path.splitext(file_name)[0]
        
        # Try to read file to extract some basic info
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple heuristics
            has_default_export = 'export default' in content
            has_props = 'Props' in content or 'interface' in content
            has_children = 'children' in content.lower()
            
            props = []
            if has_props:
                # Try to extract prop names (very basic)
                if 'interface' in content:
                    # This is a very simplified extraction
                    props = self._extract_props_simple(content)
            
            return {
                "name": component_name,
                "file_path": file_path,
                "export_type": "default" if has_default_export else "named",
                "props": props,
                "dependencies": [],
                "has_children": has_children,
                "is_hoc": False
            }
            
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return {
                "name": component_name,
                "file_path": file_path,
                "export_type": "named",
                "props": [],
                "dependencies": [],
                "has_children": False,
                "is_hoc": False
            }
    
    def _extract_props_simple(self, content: str) -> List[Dict[str, Any]]:
        """
        Simple prop extraction (placeholder)
        TODO: Implement proper AST-based extraction
        """
        props = []
        
        # Very basic regex-like extraction
        lines = content.split('\n')
        in_interface = False
        
        for line in lines:
            stripped = line.strip()
            
            if 'interface' in stripped and 'Props' in stripped:
                in_interface = True
                continue
            
            if in_interface:
                if '}' in stripped:
                    in_interface = False
                    break
                
                if ':' in stripped and not stripped.startswith('//'):
                    # Try to extract prop name and type
                    parts = stripped.split(':')
                    if len(parts) >= 2:
                        prop_name = parts[0].strip().replace('?', '')
                        prop_type = parts[1].strip().rstrip(';').rstrip(',')
                        required = '?' not in parts[0]
                        
                        props.append({
                            "name": prop_name,
                            "type": prop_type,
                            "required": required,
                            "default_value": None,
                            "description": None
                        })
        
        return props
    
    def parse_directory(self, directory_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Parse all TypeScript/TSX files in a directory
        
        Args:
            directory_path: Path to the directory
            recursive: Whether to search recursively
            
        Returns:
            List of component metadata dictionaries
        """
        components = []
        
        try:
            if recursive:
                for root, dirs, files in os.walk(directory_path):
                    # Skip node_modules and other common directories
                    dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', 'build']]
                    
                    for file in files:
                        if file.endswith(('.tsx', '.ts', '.jsx')):
                            file_path = os.path.join(root, file)
                            metadata = self.parse_file(file_path)
                            if metadata:
                                components.append(metadata)
            else:
                for file in os.listdir(directory_path):
                    if file.endswith(('.tsx', '.ts', '.jsx')):
                        file_path = os.path.join(directory_path, file)
                        if os.path.isfile(file_path):
                            metadata = self.parse_file(file_path)
                            if metadata:
                                components.append(metadata)
            
            logger.info(f"Parsed {len(components)} components from {directory_path}")
            return components
            
        except Exception as e:
            logger.error(f"Failed to parse directory {directory_path}: {e}")
            return []


def get_ast_parser() -> ASTParser:
    """Get AST parser instance"""
    return ASTParser()

