"""Configuration for ComfyUI Prompt Library."""
import os
from pathlib import Path


class PromptLibraryConfig:
    """Configuration settings for Prompt Library."""
    
    # Database settings
    DEFAULT_HISTORY_LIMIT = 500
    
    # Storage paths
    @staticmethod
    def get_output_dir():
        """Get ComfyUI output directory."""
        # Try to get ComfyUI's output directory
        try:
            import folder_paths
            output_dir = folder_paths.get_output_directory()
        except:
            # Fallback to default
            output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "output")
        
        return output_dir
    
    @staticmethod
    def get_library_dir():
        """Get Prompt Library storage directory."""
        output_dir = PromptLibraryConfig.get_output_dir()
        library_dir = os.path.join(output_dir, "Prompt History")
        os.makedirs(library_dir, exist_ok=True)
        return library_dir
    
    @staticmethod
    def get_database_path():
        """Get database file path."""
        library_dir = PromptLibraryConfig.get_library_dir()
        return os.path.join(library_dir, "prompt_library.db")
    
    @staticmethod
    def get_thumbnails_dir():
        """Get thumbnails directory."""
        library_dir = PromptLibraryConfig.get_library_dir()
        thumbnails_dir = os.path.join(library_dir, "thumbnails")
        os.makedirs(thumbnails_dir, exist_ok=True)
        return thumbnails_dir
    
    # Thumbnail settings
    THUMBNAIL_SIZE = 512
    THUMBNAIL_FORMAT = "WEBP"
    THUMBNAIL_QUALITY = 85
    
    # Performance settings
    MAX_SEARCH_RESULTS = 1000
    DEFAULT_PAGE_SIZE = 50
