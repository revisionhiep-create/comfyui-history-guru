"""
Standard Trigger Words Loader - ComfyUI Custom Node
Interactive button-based trigger word management with clickable tags.
"""

from .standard_trigger_node_v2 import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# ComfyUI will use this to register the node
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Specify web directory for JavaScript files
WEB_DIRECTORY = "./js"
