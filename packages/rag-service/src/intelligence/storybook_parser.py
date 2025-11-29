import os
import re
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class StorybookParser:
    """
    Parser for Storybook files (.stories.tsx, .stories.ts)
    
    Extracts story information and example usage
    """
    
    def parse_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parse a Storybook file
        
        Args:
            file_path: Path to the .stories.tsx file
            
        Returns:
            Dictionary with story information
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"Storybook file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract component name from file path
            file_name = os.path.basename(file_path)
            component_name = file_name.replace('.stories.tsx', '').replace('.stories.ts', '')
            
            # Extract stories
            stories = self._extract_stories(content)
            
            # Extract title from meta
            title = self._extract_title(content) or component_name
            
            return {
                "title": title,
                "component_name": component_name,
                "stories": stories,
                "file_path": file_path
            }
            
        except Exception as e:
            logger.error(f"Failed to parse storybook file {file_path}: {e}")
            return None
    
    def _extract_title(self, content: str) -> Optional[str]:
        """Extract title from Storybook meta"""
        # Look for title in meta object
        title_match = re.search(r'title:\s*[\'"]([^\'"]+)[\'"]', content)
        if title_match:
            return title_match.group(1)
        return None
    
    def _extract_stories(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract stories from content
        
        This is a simplified implementation. In production, would use proper AST parsing.
        """
        stories = []
        
        # Look for story exports
        # Pattern: export const StoryName = ...
        story_pattern = r'export const (\w+)(?:\s*:\s*\w+)?\s*=\s*\{([^}]+)\}'
        matches = re.finditer(story_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            story_name = match.group(1)
            story_content = match.group(2)
            
            # Skip meta exports
            if story_name == 'meta' or story_name == 'default':
                continue
            
            # Extract args if present
            args = self._extract_args(story_content)
            
            stories.append({
                "name": story_name,
                "code": match.group(0),
                "args": args
            })
        
        # Also look for Template.bind pattern (older Storybook format)
        template_pattern = r'export const (\w+) = .*\.bind\({}\)'
        template_matches = re.finditer(template_pattern, content)
        
        for match in template_matches:
            story_name = match.group(1)
            stories.append({
                "name": story_name,
                "code": match.group(0),
                "args": {}
            })
        
        return stories
    
    def _extract_args(self, story_content: str) -> Dict[str, Any]:
        """Extract args from story content"""
        args = {}
        
        # Look for args object
        args_match = re.search(r'args:\s*\{([^}]+)\}', story_content, re.DOTALL)
        if args_match:
            args_content = args_match.group(1)
            
            # Simple key-value extraction
            # This is very basic and would need improvement for complex objects
            arg_pattern = r'(\w+):\s*([^,\n]+)'
            for arg_match in re.finditer(arg_pattern, args_content):
                key = arg_match.group(1)
                value = arg_match.group(2).strip()
                args[key] = value
        
        return args
    
    def find_storybook_files(self, directory: str, recursive: bool = True) -> List[str]:
        """
        Find all Storybook files in a directory
        
        Args:
            directory: Directory to search
            recursive: Whether to search recursively
            
        Returns:
            List of file paths
        """
        storybook_files = []
        
        try:
            if recursive:
                for root, dirs, files in os.walk(directory):
                    # Skip node_modules and other common directories
                    dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', 'build']]
                    
                    for file in files:
                        if '.stories.' in file and (file.endswith('.tsx') or file.endswith('.ts')):
                            storybook_files.append(os.path.join(root, file))
            else:
                for file in os.listdir(directory):
                    if '.stories.' in file and (file.endswith('.tsx') or file.endswith('.ts')):
                        file_path = os.path.join(directory, file)
                        if os.path.isfile(file_path):
                            storybook_files.append(file_path)
            
            logger.info(f"Found {len(storybook_files)} storybook files in {directory}")
            return storybook_files
            
        except Exception as e:
            logger.error(f"Failed to find storybook files in {directory}: {e}")
            return []


def get_storybook_parser() -> StorybookParser:
    """Get Storybook parser instance"""
    return StorybookParser()

