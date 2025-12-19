"""Prompt Library Viewer Node (WebFrame Pattern)."""


class PromptLibraryViewerNode:
    """
    A minimal node that displays the Prompt Library web interface in an iframe.
    Uses the webframe pattern - no inputs, no outputs, just a viewer.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
        }
    
    RETURN_TYPES = ()
    FUNCTION = "show_library"
    OUTPUT_NODE = False
    CATEGORY = "📚 Prompt Library"
    
    def show_library(self):
        """Dummy function - actual UI is handled by JavaScript."""
        return ()


NODE_CLASS_MAPPINGS = {
    "PromptLibraryViewer": PromptLibraryViewerNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptLibraryViewer": "📚 Prompt Library Viewer"
}
