from typing import Dict, Any, List
import uuid
import logging

from src.intelligence.ast_parser import get_ast_parser
from src.intelligence.storybook_parser import get_storybook_parser

logger = logging.getLogger(__name__)


class MetadataExtractor:
    """
    Extracts and enriches component metadata
    
    Combines data from AST parsing, Storybook files, and other sources
    """
    
    def __init__(self):
        self.ast_parser = get_ast_parser()
        self.storybook_parser = get_storybook_parser()
    
    def extract_from_file(
        self,
        file_path: str,
        storybook_path: str = None
    ) -> Dict[str, Any]:
        """
        Extract complete metadata for a component
        
        Args:
            file_path: Path to the component file
            storybook_path: Optional path to storybook file
            
        Returns:
            Complete component metadata
        """
        # Parse AST
        ast_data = self.ast_parser.parse_file(file_path)
        if not ast_data:
            return None
        
        # Generate component ID
        component_id = str(uuid.uuid4())
        
        # Build base component metadata
        component = {
            "id": component_id,
            "name": ast_data.get("name", ""),
            "description": self._generate_description(ast_data),
            "file_path": file_path,
            "props": ast_data.get("props", []),
            "examples": [],
            "theme_wrapper": None,
            "category": self._infer_category(ast_data),
            "tags": self._generate_tags(ast_data),
            "import_path": self._generate_import_path(file_path),
            "export_type": ast_data.get("export_type", "named")
        }
        
        # Add storybook examples if available
        if storybook_path:
            storybook_data = self.storybook_parser.parse_file(storybook_path)
            if storybook_data:
                component["examples"] = self._convert_stories_to_examples(storybook_data)
        
        return component
    
    def _generate_description(self, ast_data: Dict[str, Any]) -> str:
        """Generate a description from AST data"""
        name = ast_data.get("name", "Component")
        props = ast_data.get("props", [])
        has_children = ast_data.get("has_children", False)
        
        description_parts = [f"React component {name}"]
        
        if props:
            prop_names = [p["name"] for p in props[:3]]
            description_parts.append(f"with props: {', '.join(prop_names)}")
        
        if has_children:
            description_parts.append("accepts children")
        
        return ". ".join(description_parts) + "."
    
    def _infer_category(self, ast_data: Dict[str, Any]) -> str:
        """Infer component category from metadata"""
        name = ast_data.get("name", "").lower()
        
        # Simple categorization based on name
        if any(keyword in name for keyword in ['button', 'link']):
            return "Actions"
        elif any(keyword in name for keyword in ['input', 'select', 'form', 'checkbox', 'radio']):
            return "Forms"
        elif any(keyword in name for keyword in ['modal', 'dialog', 'popup']):
            return "Overlays"
        elif any(keyword in name for keyword in ['card', 'panel', 'container']):
            return "Layout"
        elif any(keyword in name for keyword in ['text', 'heading', 'title', 'label']):
            return "Typography"
        elif any(keyword in name for keyword in ['icon', 'image', 'avatar']):
            return "Media"
        elif any(keyword in name for keyword in ['nav', 'menu', 'tab']):
            return "Navigation"
        else:
            return "General"
    
    def _generate_tags(self, ast_data: Dict[str, Any]) -> List[str]:
        """Generate tags for the component"""
        tags = []
        name = ast_data.get("name", "").lower()
        
        # Add tags based on component characteristics
        if ast_data.get("has_children"):
            tags.append("container")
        
        if ast_data.get("is_hoc"):
            tags.append("hoc")
        
        # Add tags based on name patterns
        if 'button' in name:
            tags.append("interactive")
        if 'form' in name or 'input' in name:
            tags.append("form")
        if 'layout' in name or 'container' in name:
            tags.append("layout")
        
        return tags
    
    def _generate_import_path(self, file_path: str) -> str:
        """
        Generate import path from file path
        
        This is a simplified version. In production, would need to handle
        proper module resolution.
        """
        # Try to extract relative path from common base directories
        import os
        
        # Remove file extension
        without_ext = os.path.splitext(file_path)[0]
        
        # Try to create a reasonable import path
        parts = without_ext.split(os.sep)
        
        # Find common base directories
        if 'components' in parts:
            idx = parts.index('components')
            return '/'.join(parts[idx:])
        elif 'src' in parts:
            idx = parts.index('src')
            return '/'.join(parts[idx:])
        else:
            # Fallback to filename
            return os.path.basename(without_ext)
    
    def _convert_stories_to_examples(self, storybook_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert Storybook stories to component examples"""
        examples = []
        
        for story in storybook_data.get("stories", []):
            examples.append({
                "title": story.get("name", "Example"),
                "code": story.get("code", ""),
                "description": f"Example from Storybook: {story.get('name')}",
                "source": "storybook"
            })
        
        return examples
    
    def enrich_with_usage_patterns(
        self,
        component: Dict[str, Any],
        usage_patterns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Enrich component metadata with usage patterns from monorepo analysis
        
        Args:
            component: Component metadata
            usage_patterns: List of usage patterns
            
        Returns:
            Enriched component metadata
        """
        # This will be used when monorepo analysis is implemented
        # For now, just return the component as-is
        return component


def get_metadata_extractor() -> MetadataExtractor:
    """Get metadata extractor instance"""
    return MetadataExtractor()

