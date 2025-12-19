from .lora_frame import LoraWebFrame

NODE_CLASS_MAPPINGS = {
    "LoraWebFrame": LoraWebFrame
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraWebFrame": "✨ Lora Manager Web Frame"
}

# CHANGED: We now point directly to the "./js" folder
WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]