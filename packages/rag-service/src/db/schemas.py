from typing import Dict, Any


class ComponentSchema:
    """Schema for component documents in ChromaDB"""
    
    @staticmethod
    def to_document(component: Dict[str, Any]) -> str:
        """Convert component to searchable document text"""
        parts = [
            f"Component: {component.get('name', '')}",
            f"Description: {component.get('description', '')}",
            f"Category: {component.get('category', 'Uncategorized')}",
        ]
        
        # Add props information
        props = component.get('props', [])
        if props:
            prop_names = [p.get('name', '') for p in props]
            parts.append(f"Props: {', '.join(prop_names)}")
        
        # Add tags
        tags = component.get('tags', [])
        if tags:
            parts.append(f"Tags: {', '.join(tags)}")
        
        # Add examples
        examples = component.get('examples', [])
        if examples:
            example_titles = [e.get('title', '') for e in examples]
            parts.append(f"Examples: {', '.join(example_titles)}")
        
        return "\n".join(parts)
    
    @staticmethod
    def to_metadata(component: Dict[str, Any]) -> Dict[str, Any]:
        """Convert component to metadata for ChromaDB"""
        return {
            "id": component.get("id", ""),
            "name": component.get("name", ""),
            "category": component.get("category", ""),
            "file_path": component.get("file_path", ""),
            "import_path": component.get("import_path", ""),
            "export_type": component.get("export_type", "named"),
            "theme_wrapper": component.get("theme_wrapper", ""),
            "num_props": len(component.get("props", [])),
            "num_examples": len(component.get("examples", [])),
            "tags": ",".join(component.get("tags", [])),
        }

