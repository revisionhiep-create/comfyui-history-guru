"""Main Prompt Library Node for ComfyUI."""
import os
import time
import hashlib
import json
from typing import Dict, Any, Tuple

from .py.database import PromptLibraryDatabase
from .py.image_processor import ImageProcessor
from .py.metadata_extractor import MetadataExtractor
from .py.config import PromptLibraryConfig
from .utils.helpers import generate_hash


class PromptLibraryNode:
    """
    A ComfyUI node that records prompt history with thumbnails and metadata.
    Displays a browsable library of past prompts with LoRA tracking.
    """
    
    def __init__(self):
        self.db = PromptLibraryDatabase()
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            }
        }
    
    RETURN_TYPES = ()
    FUNCTION = "record_prompt"
    OUTPUT_NODE = True
    CATEGORY = "📚 Prompt Library"
    
    def record_prompt(self, 
                     images,
                     prompt=None,
                     extra_pnginfo=None,
                     unique_id=None):
        """
        Record prompt and generate thumbnail automatically.
        
        Args:
            images: Image tensor from ComfyUI
            prompt: Hidden - workflow prompt data (auto-extracted)
            extra_pnginfo: Hidden - extra PNG info (auto-extracted)
            unique_id: Hidden - node unique ID
        
        Returns:
            Empty dict (output node)
        """
        try:
            # Extract all metadata automatically from workflow
            workflow_metadata = {}
            if prompt:
                workflow_metadata = MetadataExtractor.extract_from_prompt_dict(prompt)
            
            # Use workflow metadata (no manual inputs)
            final_prompt = workflow_metadata.get('prompt_text', '')
            final_negative = workflow_metadata.get('negative_prompt', '')
            final_checkpoint = workflow_metadata.get('checkpoint', '')
            final_seed = workflow_metadata.get('seed', None)
            
            # Extract LoRAs from workflow and text
            workflow_loras = workflow_metadata.get('loras', [])
            text_loras = MetadataExtractor.extract_loras_from_text(final_prompt)
            final_loras = MetadataExtractor.merge_lora_data(workflow_loras, text_loras)
            
            # Generate hash for deduplication
            hash_string = f"{final_prompt}|{final_negative}|{final_checkpoint}|{json.dumps(final_loras, sort_keys=True)}"
            hash_value = generate_hash(hash_string)
            
            # Generate unique filename
            timestamp = int(time.time() * 1000)
            filename = f"prompt_{timestamp}_{hash_value[:8]}"
            
            # Create thumbnail
            thumbnail_path, width, height = ImageProcessor.create_thumbnail(
                images, filename
            )
            
            if thumbnail_path:
                # Add to database
                prompt_id = self.db.add_prompt(
                    prompt_text=final_prompt,
                    negative_prompt=final_negative,
                    checkpoint=final_checkpoint,
                    seed=final_seed,
                    width=width,
                    height=height,
                    thumbnail_path=thumbnail_path,
                    loras=final_loras,
                    hash_value=hash_value
                )
                
                if prompt_id:
                    # Get history limit from config (can be made node parameter)
                    history_limit = PromptLibraryConfig.DEFAULT_HISTORY_LIMIT
                    
                    # Cleanup old prompts
                    self.db.cleanup_old_prompts(history_limit)
                    
                    print(f"[Prompt Library] Successfully recorded prompt #{prompt_id}")
                else:
                    print("[Prompt Library] Skipped duplicate prompt")
            
        except Exception as e:
            print(f"[Prompt Library] Error in record_prompt: {e}")
            import traceback
            traceback.print_exc()
        
        # Always return empty dict for output node
        return {"ui": {"text": ["Prompt recorded to library"]}}


NODE_CLASS_MAPPINGS = {
    "PromptLibrary": PromptLibraryNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptLibrary": "📚 Prompt Library"
}
